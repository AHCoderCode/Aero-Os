#!/usr/bin/env python3
"""Structural and release checks for the AeroOS image configuration."""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []


def require(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def read(path: str) -> str:
    file = ROOT / path
    require(file.is_file(), f"Required file missing: {path}")
    return file.read_text(encoding="utf-8") if file.is_file() else ""


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
    size = panel.find("./property[@name='size']") if panel is not None else None
    alpha = panel.find("./property[@name='background-alpha']") if panel is not None else None
    require(size is not None and size.get("value") == "54",
            "The Aero taskbar must use a 54 px panel size.")
    require(alpha is not None and alpha.get("value") == "28",
            "The Aero taskbar must use the translucent 28% panel background.")

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

    # The expanding spacers on both sides keep the app dock centred.
    for spacer_id in ("plugin-2", "plugin-4"):
        spacer = plugin_nodes.get(spacer_id)
        expand = spacer.find("./property[@name='expand']") if spacer is not None else None
        require(expand is not None and expand.get("value") == "true",
                f"{spacer_id} must expand to centre the app dock.")

    start_plugin = plugin_nodes.get("plugin-1")
    require(start_plugin is not None, "The Start button is missing.")
    if start_plugin is not None:
        start_values = {p.get("name"): p.get("value") for p in start_plugin.findall("./property")}
        require(start_values.get("button-title") == "Start",
                "The left taskbar button must be named Start.")
        require(start_values.get("button-icon") == "aeroos-start",
                "The Start button must use the custom Aero four-pane icon.")
        require(start_values.get("show-button-title") == "false",
                "The Start button must be icon-only.")
except (ET.ParseError, OSError) as exc:
    ERRORS.append(f"Cannot validate panel configuration: {exc}")

packages = read("config/package-lists/aeroos.list.chroot")
required_packages = (
    "xfce4", "xfce4-whiskermenu-plugin", "xfce4-docklike-plugin",
    "network-manager", "firmware-amd-graphics", "firefox-esr",
    "parted", "e2fsprogs", "zenity", "synaptic", "galculator",
    "mousepad", "parole", "xfce4-taskmanager"
)
for package in required_packages:
    require(re.search(rf"(?m)^{re.escape(package)}$", packages) is not None,
            f"Required package missing: {package}")
require(re.search(r"(?m)^gparted$", packages) is None,
        "Do not include a general-purpose partition editor in the initial live image.")

dock_text = read("config/includes.chroot/etc/xdg/xfce4/panel/docklike.rc")
dock_pins = (
    "firefox-esr.desktop", "thunar.desktop", "xfce4-terminal.desktop",
    "galculator.desktop", "org.xfce.mousepad.desktop",
    "org.xfce.Parole.desktop", "synaptic.desktop", "aeroos-control-center.desktop"
)
for desktop_id in dock_pins:
    require(desktop_id in dock_text, f"Centred app dock pin missing: {desktop_id}")
for value in ("showPreviews=false", "forceIconSize=true", "iconSize=38"):
    require(value in dock_text, f"Docklike must include {value}")

auto = read("auto/config")
require("--distribution trixie" in auto and "--architectures amd64" in auto,
        "The image must target Debian Trixie amd64.")
require("persistence" in auto, "The Live image must enable persistence boot discovery.")

desktop_dir = ROOT / "config/includes.chroot/etc/skel/Desktop"
launchers = {
    "File-Manager.desktop": ("Exec=thunar", "thunar"),
    "Settings.desktop": ("Exec=aeroos-control-center", "xfce4"),
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

autostart = read("config/includes.chroot/etc/xdg/autostart/aeroos-welcome.desktop")
require("Exec=aeroos-welcome --autostart" in autostart,
        "Welcome autostart must use the one-time mode.")

welcome_text = read("config/includes.chroot/usr/local/bin/aeroos-welcome")
require("welcome-shown" in welcome_text,
        "Welcome autostart must remember dismissal when persistence is enabled.")
require("0.3.1-rc1" in welcome_text and "Windows/Super key" in welcome_text,
        "Welcome guide must describe the new Start menu and current version.")

parser = read("config/includes.chroot/usr/local/lib/aeroos/persistence-free-space.awk")
require("free_end + 0 > free_start + 0" in parser,
        "Persistence parser must compare byte offsets numerically.")

persistence_script = read("config/includes.chroot/usr/local/sbin/aeroos-setup-persistence")
for guard in ("toram", "AEROOS_LIVE", "blockdev --getsize64", "RM", "parted", "mkfs.ext4", "/ union"):
    require(guard in persistence_script, f"Persistence setup is missing safety/configuration check: {guard}")

control_center = read("config/includes.chroot/usr/local/bin/aeroos-control-center")
for option in ("Theme and accent color", "Wallpaper and desktop icons",
               "Taskbar and Start menu", "Display and screen resolution",
               "Keyboard and shortcuts", "Power and battery",
               "Performance profile", "All system settings"):
    require(option in control_center, f"Control Center option missing: {option}")

theme_tool = read("config/includes.chroot/usr/local/bin/aeroos-theme-picker")
for preset in ("Aero Dark - Blue", "Aero Dark - Violet", "Aero Dark - Teal",
               "Aero Light - Blue", "Aero Light - Violet", "Aero Light - Teal"):
    require(preset in theme_tool, f"Appearance preset missing: {preset}")
for value in ("rgba(11,18,32,0.28)", "rgba(16,13,32,0.28)", "rgba(9,27,32,0.28)",
              "rgba(237,242,251,0.32)", "rgba(243,239,251,0.32)", "rgba(234,245,244,0.32)"):
    require(value in theme_tool, f"Theme preset must preserve taskbar transparency: {value}")

performance_tool = read("config.includes.chroot/usr/local/bin/aeroos-performance") if False else read("config/includes.chroot/usr/local/bin/aeroos-performance")
require("Transparent taskbar (recommended)" in performance_tool and
        "Solid taskbar (maximum battery/compatibility)" in performance_tool,
        "Performance tool must offer transparent and solid taskbar modes.")
require("compositing=true" in performance_tool and "compositing=false" in performance_tool,
        "Both taskbar rendering modes must set the compositor explicitly.")

xfwm = ET.parse(ROOT / "config/includes.chroot/etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfwm4.xml").getroot()
composite = xfwm.find("./property[@name='general']/property[@name='use_compositing']")
require(composite is not None and composite.get("value") == "true",
        "Xfwm compositing must be enabled for true taskbar transparency.")

css = read("config/includes.chroot/etc/skel/.config/gtk-3.0/gtk.css")
require("rgba(11, 18, 32, 0.28)" in css,
        "The default panel CSS must use a translucent background.")
require("#whiskermenu-window" in css and "border-radius: 18px" in css,
        "The Aero Start menu must have rounded transparent styling.")

menu_text = read("config/includes.chroot/etc/skel/.config/xfce4/panel/whiskermenu-1.rc")
menu_settings = dict(
    line.split("=", 1) for line in menu_text.splitlines()
    if "=" in line and not line.lstrip().startswith("#")
)
for key, expected_value in {
    "button-title": "Start",
    "button-icon": "aeroos-start",
    "show-button-title": "false",
    "display-recent-default": "false",
    "recent-items-max": "8",
    "menu-width": "620",
    "menu-height": "600",
    "menu-opacity": "94",
}.items():
    require(menu_settings.get(key) == expected_value,
            f"Start menu setting {key} must be {expected_value}.")
for desktop_id in dock_pins:
    require(desktop_id in menu_settings.get("favorites", "").split(","),
            f"Start menu favorite missing: {desktop_id}")

start_icon_path = ROOT / "config/includes.chroot/usr/share/icons/hicolor/scalable/apps/aeroos-start.svg"
require(start_icon_path.is_file(), "Custom Aero Start icon is missing.")
if start_icon_path.is_file():
    try:
        ET.parse(start_icon_path)
    except ET.ParseError as exc:
        ERRORS.append(f"Invalid Start icon SVG: {exc}")

if ERRORS:
    print("AeroOS configuration validation failed:", file=sys.stderr)
    for error in ERRORS:
        print(f" - {error}", file=sys.stderr)
    sys.exit(1)

print("AeroOS configuration validation passed.")
