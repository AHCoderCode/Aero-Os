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
                "network-manager", "firmware-amd-graphics", "firefox-esr"):
    require(re.search(rf"(?m)^{re.escape(package)}$", packages) is not None,
            f"Required package missing: {package}")
require(re.search(r"(?m)^gparted$", packages) is None,
        "Do not include the partition editor in the initial live image.")

dock_file = ROOT / "config/includes.chroot/etc/xdg/xfce4/panel/docklike.rc"
dock_text = dock_file.read_text(encoding="utf-8")
for value in ("showPreviews=false", "firefox-esr.desktop", "thunar.desktop", "xfce4-terminal.desktop"):
    require(value in dock_text, f"Docklike defaults must include {value}")

auto = (ROOT / "auto/config").read_text(encoding="utf-8")
require("--distribution trixie" in auto and "--architectures amd64" in auto,
        "The image must target Debian Trixie amd64.")
require("persistence" in auto, "The Live image must enable persistence boot discovery.")

if ERRORS:
    print("AeroOS configuration validation failed:", file=sys.stderr)
    for error in ERRORS:
        print(f" - {error}", file=sys.stderr)
    sys.exit(1)

print("AeroOS configuration validation passed.")
