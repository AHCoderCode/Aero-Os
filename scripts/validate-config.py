#!/usr/bin/env python3
"""Structural and release checks for AeroOS configuration."""
from pathlib import Path
import ast, re, sys, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
INC=ROOT/"config/includes.chroot"
ERRORS=[]
def require(ok,msg):
    if not ok: ERRORS.append(msg)
def read(path):
    p=ROOT/path
    require(p.is_file(),f"Required file missing: {path}")
    return p.read_text(encoding="utf-8") if p.is_file() else ""
for p in INC.rglob("*.xml"):
    try: ET.parse(p)
    except ET.ParseError as e: ERRORS.append(f"Invalid XML in {p.relative_to(ROOT)}: {e}")
panel=INC/"etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml"
try:
    ch=ET.parse(panel).getroot(); ps=ch.find("./property[@name='panels']")
    p1=ps.find("./property[@name='panel-1']") if ps is not None else None
    ids=[] if p1 is None else [int(x.get("value","-1")) for x in p1.findall("./property[@name='plugin-ids']/value")]
    require(ids==list(range(1,18)),"Panel IDs must be 1 through 17.")
    pr=ch.find("./property[@name='plugins']"); plugins={} if pr is None else {x.get("name"):x for x in pr.findall("./property")}
    expected={1:"whiskermenu",2:"separator",3:"launcher",4:"launcher",5:"launcher",6:"launcher",7:"launcher",8:"launcher",9:"launcher",10:"launcher",11:"tasklist",12:"separator",13:"systray",14:"power-manager-plugin",15:"pulseaudio",16:"clock",17:"actions"}
    require(len(plugins)==17,"Panel must define exactly 17 plugins.")
    for i,k in expected.items():
        q=plugins.get(f"plugin-{i}"); require(q is not None and q.get("value")==k,f"Panel plugin {i} must be {k}.")
    launcher_ids={3:"aeroos-browser.desktop",4:"aeroos-files.desktop",5:"aeroos-terminal.desktop",6:"aeroos-calculator.desktop",7:"aeroos-editor.desktop",8:"aeroos-media.desktop",9:"aeroos-store.desktop",10:"aeroos-settings.desktop"}
    for i,f in launcher_ids.items():
        q=plugins.get(f"plugin-{i}"); item=q.find("./property[@name='items']/value") if q is not None else None
        require(item is not None and item.get("value")==f,f"Launcher {i} must use {f}.")
    for i in (2,12):
        q=plugins.get(f"plugin-{i}"); ex=q.find("./property[@name='expand']") if q is not None else None
        require(ex is not None and ex.get("value")=="true",f"Panel spacer {i} must expand.")
except (ET.ParseError,OSError,ValueError) as e: ERRORS.append(f"Cannot validate panel: {e}")
packages=read("config/package-lists/aeroos.list.chroot")
for name in ("xfce4","xfce4-whiskermenu-plugin","xfce4-power-manager","xfce4-power-manager-plugins","xfce4-pulseaudio-plugin","network-manager","network-manager-gnome","blueman","firmware-amd-graphics","python3-gi","gir1.2-gtk-3.0","exo-utils","firefox-esr","thunar","synaptic","galculator","mousepad","parole","zenity","parted","e2fsprogs"):
    require(re.search(rf"(?m)^{re.escape(name)}$",packages) is not None,f"Missing package {name}.")
require(re.search(r"(?m)^xfce4-docklike-plugin$",packages) is None,"Third-party Docklike must not be required.")
require(re.search(r"(?m)^gparted$",packages) is None,"Do not include a general partition editor.")
auto=read("auto/config")
require("--distribution trixie" in auto and "--architectures amd64" in auto and "username=aero" in auto and "persistence" in auto,"Live image configuration lacks architecture, username or persistence.")
expected_exec={"aeroos-browser.desktop":"Exec=firefox-esr %u","aeroos-files.desktop":"Exec=thunar","aeroos-terminal.desktop":"Exec=xfce4-terminal","aeroos-calculator.desktop":"Exec=galculator","aeroos-editor.desktop":"Exec=mousepad %F","aeroos-media.desktop":"Exec=parole %U","aeroos-store.desktop":"Exec=synaptic-pkexec","aeroos-settings.desktop":"Exec=aeroos-control-center"}
for f,command in expected_exec.items():
    p=INC/"usr/share/applications"/f
    require(p.is_file(),f"Missing launcher {f}")
    if p.is_file(): require(command in p.read_text(encoding="utf-8"),f"Incorrect Exec in {f}")
keys=read("config/includes.chroot/etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml")
for token in ('name="Super_L"','name="Super_R"','value="xfce4-popup-whiskermenu"','name="&lt;Primary&gt;Escape"','value="aeroos-control-center"','value="thunar"'):
    require(token in keys,f"Missing shortcut {token}")
require('name="&lt;Alt&gt;F4"' in keys and 'value="close_window_key"' in keys,"Alt+F4 must close windows.")
cc=read("config/includes.chroot/usr/local/bin/aeroos-control-center")
try: ast.parse(cc)
except SyntaxError as e: ERRORS.append(f"Settings Python syntax error: {e}")
for app in ("xfce4-display-settings","nm-connection-editor","pavucontrol","xfce4-power-manager-settings","blueman-manager","synaptic-pkexec","xfce4-keyboard-settings","xfce4-mouse-settings","xfce4-session-settings"):
    require(app in cc,f"Settings hub missing integration for {app}.")
welcome=read("config/includes.chroot/usr/local/bin/aeroos-welcome")
require("0.4.0-rc1" in welcome and "Ctrl+Esc" in welcome and "welcome-shown" in welcome,"Welcome screen needs release, shortcut and first-run marker.")
init=read("config/includes.chroot/usr/local/bin/aeroos-desktop-init")
require("xfconf-query" in init and "xfdesktop --reload" in init,"Desktop init must apply wallpaper.")
init_desktop=read("config/includes.chroot/etc/xdg/autostart/aeroos-desktop-init.desktop")
require("Exec=aeroos-desktop-init" in init_desktop,"Wallpaper initializer must autostart.")
persist=read("config/includes.chroot/usr/local/sbin/aeroos-setup-persistence")
for x in ("toram","AEROOS_LIVE","blockdev --getsize64","RM","parted","mkfs.ext4","/ union"):
    require(x in persist,f"Persistence safety check missing: {x}")
wall=INC/"usr/share/backgrounds/aeroos/aeroos-wallpaper.svg"
require(wall.is_file(),"Wallpaper is missing.")
if wall.is_file():
    try: ET.parse(wall)
    except ET.ParseError as e: ERRORS.append(f"Invalid wallpaper SVG: {e}")
if ERRORS:
    print("AeroOS configuration validation failed:",file=sys.stderr)
    for e in ERRORS: print(" - "+e,file=sys.stderr)
    sys.exit(1)
print("AeroOS configuration validation passed.")
