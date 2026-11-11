#!/usr/bin/env python3
"""Structural checks for the AeroOS image configuration."""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []


def require(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


# Parse every XML file and report the precise file that is malformed.
for path in (ROOT / "config" / "includes.chroot").rglob("*.xml"):
    try:
        ET.parse(path)
    except ET.ParseError as exc:
        ERRORS.append(f"Invalid XML in {path.relative_to(ROOT)}: {exc}")

panel_path = ROOT / "config/includes.chroot/etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml"
try:
    channel = ET.parse(panel_path).getroot()
    require(channel.tag == "channel" and channel.get("name") == "xfce4-panel",
            "Panel config must be the xfce4-panel Xfconf channel.")
    panel_root = channel.find("./property[@name='panels']")
    require(panel_root is not None and panel_root.get("type") == "array",
            "Panel IDs must be stored in the panels array.")
    panel = panel_root.find("./property[@name='panel-1']") if panel_root is not None else None
    require(panel is not None, "panel-1 must be nested in the panels array.")
    ids = [] if panel is None else [
        int(v.get("value", "-1")) for v in panel.findall("./property[@name='plugin-ids']/value")
    ]
    require(ids == [1, 2, 3, 4, 5, 6, 7],
            "The panel must list plugin IDs 1 through 7 in taskbar order.")
    plugins_root = channel.find("./property[@name='plugins']")
    plugin_nodes = {} if plugins_root is None else {
        p.get("name"): p for p in plugins_root.findall("./property")
    }
    expected = {
        "plugin-1": "whiskermenu",
        "plugin-2": "separator",
        "plugin-3": "docklike",
        "plugin-4": "separator",
        "plugin-5": "systray",
        "plugin-6": "pulseaudio",
        "plugin-7": "clock",
    }
    for key, value in expected.items():
        require(key in plugin_nodes and plugin_nodes[key].get("value") == value,
                f"{key} must be the {value} panel plugin.")
    require(len(plugin_nodes) == len(expected),
            "Panel plugin entries must be unique and match the ID list.")
except (ET.ParseError, OSError) as exc:
    ERRORS.append(f"Cannot validate panel configuration: {exc}")

packages = (ROOT / "config/package-lists/aeroos.list.chroot").read_text(encoding="utf-8")
for package in ("xfce4", "xfce4-whiskermenu-plugin", "xfce4-docklike-plugin",
                "network-manager", "firmware-amd-graphics", "firefox-esr",
                "parted", "e2fsprogs", "zenity", "synaptic", "galculator",
                "mousepad", "parole", "xfce4-taskmanager"):
    require(re.search(rf"(?m)^{re.escape(package)}$", packages) is not None,
            f"Required package missing: {package}")
require(re.search(r"(?m)^gparted$", packages) is None,
        "Do not include a general-purpose partition editor in the live image.")

dock_file = ROOT / "config/includes.chroot/etc/xdg/xfce4/panel/docklike.rc"
dock_text = dock_file.read_text(encoding="utf-8")
for value in ("showPreviews=false", "firefox-esr.desktop", "thunar.desktop", "xfce4-terminal.desktop"):
    require(value in dock_text, f"Docklike defaults must include {value}")

auto = (ROOT / "auto/config").read_text(encoding="utf-8")
require("--distribution trixie" in auto and "--architectures amd64" in auto,
        "The image must target Debian Trixie amd64.")
require("persistence" in auto, "The Live image must enable persistence boot discovery.")

# Verify the desktop shortcuts point to applications present in the image.
desktop_dir = ROOT / "config/includes.chroot/etc/skel/Desktop"
launchers = {
    "File-Manager.desktop": ("Exec=thunar", "thunar"),
    "Settings.desktop": ("Exec=xfce4-settings-manager", "xfce4"),
    "Web-Browser.desktop": ("Exec=firefox-esr %u", "firefox-esr"),
    "Welcome-to-AeroOS.desktop": ("Exec=aeroos-welcome", "zenity"),
    "App-Store.desktop": ("Exec=synaptic-pkexec", "synaptic"),
    "Calculator.desktop": ("Exec=galculator", "galculator"),
    "Text-Editor.desktop": ("Exec=mousepad %F", "mousepad"),
    "Media-Player.desktop": ("Exec=parole %U", "parole"),
    "System-Monitor.desktop": ("Exec=xfce4-taskmanager", "xfce4-taskmanager"),
    "Set-Up-Persistence.desktop": ("Exec=pkexec /usr/local/sbin/aeroos-setup-persistence", "parted"),
}
for filename, (exec_line, package) in launchers.items():
    path = desktop_dir / filename
    require(path.is_file(), f"Missing desktop launcher: {filename}")
    if path.is_file():
        content = path.read_text(encoding="utf-8")
        require("[Desktop Entry]" in content and exec_line in content,
                f"{filename} has an invalid desktop entry or Exec command.")
    require(re.search(rf"(?m)^{re.escape(package)}$", packages) is not None,
            f"{filename} requires missing package {package}.")

autostart = ROOT / "config/includes.chroot/etc/xdg/autostart/aeroos-welcome.desktop"
require(autostart.is_file(), "AeroOS first-start welcome autostart is missing.")
if autostart.is_file():
    auto_text = autostart.read_text(encoding="utf-8")
    require("Exec=aeroos-welcome --autostart" in auto_text,
            "Welcome autostart must use the one-time mode.")

welcome = (ROOT / "config/includes.chroot/usr/local/bin/aeroos-welcome").read_text(encoding="utf-8")
require("welcome-shown" in welcome, "Welcome autostart must remember dismissal when persistence is enabled.")

parser_path = ROOT / "config/includes.chroot/usr/local/lib/aeroos/persistence-free-space.awk"
require(parser_path.is_file(), "The persistence free-space parser is missing.")
if parser_path.is_file():
    require("free_end + 0 > free_start + 0" in parser_path.read_text(encoding="utf-8"),
            "Persistence parser must compare byte offsets numerically.")

persistence_script = ROOT / "config/includes.chroot/usr/local/sbin/aeroos-setup-persistence"
require(persistence_script.is_file(), "The guarded persistence setup utility is missing.")
if persistence_script.is_file():
    setup_text = persistence_script.read_text(encoding="utf-8")
    for guard in ("toram", "AEROOS_LIVE", "blockdev --getsize64", "RM", "parted", "mkfs.ext4", "/ union"):
        require(guard in setup_text, f"Persistence setup is missing safety/configuration check: {guard}")

if ERRORS:
    print("AeroOS configuration validation failed:", file=sys.stderr)
    for error in ERRORS:
        print(f" - {error}", file=sys.stderr)
    sys.exit(1)

print("AeroOS configuration validation passed.")
