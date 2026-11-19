# AeroOS customization

AeroOS Settings brings the main desktop and device controls together without requiring terminal commands.

## Open AeroOS Settings

- Open **Aero** at the left of the taskbar, then choose **AeroOS Settings**, or
- Double-click **AeroOS Settings** on the desktop, or
- Press **Windows/Aero + I**.

## Taskbar

The default native Xfce panel is arranged as follows:

- **Left:** Aero Start button.
- **Centre:** pinned application launchers and running-window buttons.
- **Right:** system tray, battery/power, volume, clock and session/power menu.

The application buttons are individual Xfce launchers, not a third-party dock. Running windows appear in the tasklist; click a running-window button to bring its window forward. Use **Alt+Tab** to switch between open windows and **Alt+F4** to close the active window.

The default panel has a restrained translucent background. The **Performance** option in AeroOS Settings can switch to a solid panel if compositing is slow or visually unstable on older graphics hardware.

## Start menu and keyboard shortcuts

Click **Aero** at the left of the taskbar, press either Windows/Super key, or use **Ctrl+Esc** as a fallback.

The menu includes installed applications, favorites, search and application categories. To pin an app, find it in Start, right-click it and choose **Add to Favorites**.

Default shortcuts:

- **Windows/Aero** or **Ctrl+Esc:** Start.
- **Win+E:** File Explorer.
- **Win+W:** Firefox ESR.
- **Win+T:** Terminal.
- **Win+I:** AeroOS Settings.
- **Win+R:** application finder.
- **Alt+Tab:** switch windows.
- **Alt+F4:** close the active window.
- **Win+D:** show the desktop.
- **Ctrl+Shift+Esc:** Task Manager.

## Personalization

In AeroOS Settings, open **Personalization**:

- **Appearance:** native GTK theme, icons and fonts.
- **AeroOS themes:** choose one of six Dark/Light Blue, Violet or Teal presets.
- **Wallpaper:** change the desktop background and desktop icons.
- **Taskbar and Start:** open Xfce panel preferences.
- **Performance:** choose the translucent or solid-panel profile.

The default AeroOS wallpaper is applied when the desktop session starts. User changes are stored in the home directory and survive restarts only when USB persistence is configured.

## Devices and connectivity

In AeroOS Settings:

- **Devices:** display, keyboard, mouse/touchpad and Bluetooth tools.
- **Connectivity:** NetworkManager connections and Blueman.
- **Sound and notifications:** PulseAudio mixer, output and microphone controls, and notification settings.
- **System:** power/battery, default applications, session startup, window behavior and system monitor.

These cards open installed system tools. Device availability still depends on the exact hardware and firmware in the laptop. In particular, Wi-Fi, Bluetooth, audio, battery and graphics behavior must be tested on the target HP ProBook.

## Full Xfce customization

Open **All settings** on the Overview page to use the complete Xfce Settings Manager. Its native tools cover appearance, display, keyboard, mouse, window manager, sessions and other desktop preferences.

With full-root USB persistence enabled, themes, wallpaper, taskbar layout, favorites and personal files can be retained across normal reboots.
