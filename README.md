# AeroOS

**AeroOS 0.4.1-rc1** is a Debian 13 Live operating system with a lightweight, Windows-inspired desktop. Its first hardware target is the HP ProBook 4520s: Intel Core i5-480M, 8 GB RAM, Legacy BIOS and a user-reported Radeon HD 64xx-family GPU.

AeroOS runs from a USB drive. The Live image does not install to, repartition or intentionally modify the laptop's internal Windows drive.

## Build and verification status

- Debian 13 Trixie amd64 ISO: built successfully by GitHub Actions.
- Legacy BIOS hybrid boot image: checked with xorriso.
- Source/configuration checks and persistence-parser tests: run during each build.
- The native taskbar dependencies, including the separate Xfce power-manager panel plugin, are included and checked by CI.
- **Actual HP ProBook hardware testing is still required.** CI cannot certify Wi-Fi, sound, Bluetooth, graphics acceleration, battery reporting, suspend/resume, brightness keys or USB compatibility on the physical laptop.

This is a release candidate, not a claim of hardware certification or a bug-free final release.

## Desktop

The desktop uses Xfce and LightDM with a native Xfce panel:

- **Left:** Aero Start button.
- **Centre:** individual pinned application launchers and running-window buttons.
- **Right:** system tray, battery/power indicator, volume control, clock and session/power menu.

The panel uses Xfce's built-in launcher and tasklist plugins instead of a third-party dock. The Start menu provides favorites, installed applications, categories and search. A restrained translucent theme is enabled by default; a solid-panel performance profile is available for older graphics hardware.

## Included applications and tools

- **File Explorer:** Thunar, removable-drive browsing and archive support.
- **Web browser:** Firefox ESR.
- **App Store:** Synaptic package manager.
- **Settings:** AeroOS Settings hub plus the native Xfce settings tools.
- **Terminal:** Xfce Terminal.
- **Calculator:** Galculator.
- **Text editor:** Mousepad.
- **Media player:** Parole.
- **System monitor:** Xfce Task Manager.
- **Networking:** NetworkManager and supported Wi-Fi firmware packages.
- **Bluetooth:** Blueman.
- **Audio:** PulseAudio controls and mixer.
- **Power:** Xfce power manager and its panel plugin.

## Keyboard shortcuts

- **Windows/Aero key** or **Ctrl+Esc:** open Start.
- **Win+E:** File Explorer.
- **Win+W:** browser.
- **Win+T:** Terminal.
- **Win+I:** AeroOS Settings.
- **Win+R:** application finder.
- **Alt+Tab:** switch windows.
- **Alt+F4:** close the active window.
- **Win+D:** show the desktop.
- **Ctrl+Shift+Esc:** Task Manager.

Some laptop function keys depend on the specific keyboard and firmware.

## AeroOS Settings

Open **AeroOS Settings** from the Start menu or desktop shortcut. It provides sections for Overview, Personalization, Devices, Connectivity, Sound and notifications, System, and About AeroOS. The cards open real installed Xfce and device configuration tools; they are not simulated settings.

## USB Live use

AeroOS is designed to be tested as a Live USB before any persistence setup. Do not select an installer or an internal disk. To return to Windows, shut down AeroOS, wait until the laptop is fully off, remove the USB and power on normally.

Read [docs/USB-AND-PERSISTENCE.md](docs/USB-AND-PERSISTENCE.md) before writing the image or setting up persistence. **Writing the ISO erases the selected USB device.** Verify the selected drive by its capacity and label; never select the laptop's internal disk. Windows cannot read the ext4 persistence partition; cancel any Windows prompt to format it.

The full-persistence utility is optional and is only intended for the AeroOS USB. It requires a one-time `toram` boot and performs strict checks before creating a persistence partition.

## Build the ISO

GitHub Actions runs **Build AeroOS ISO** on pushes to `main` and on manual dispatch. The successful run publishes an ISO, SHA-256 file and BIOS boot report as release assets.

The build scripts validate the source configuration, parse XML, check application launchers and keyboard shortcuts, check persistence-safety requirements, and verify the generated hybrid ISO's BIOS boot record. Those checks do not replace testing on the target laptop.

## Hardware profile

- Architecture: amd64 (64-bit Intel).
- Desktop: Xfce + LightDM.
- Firmware: Legacy BIOS / Syslinux hybrid media.
- Memory: zram uses a conservative 25% RAM cap with zstd compression.
- Graphics: Intel and legacy Radeon X.Org drivers plus Debian firmware packages.

The exact Radeon PCI ID and Wi-Fi adapter are not yet confirmed. See [docs/HARDWARE-TARGET.md](docs/HARDWARE-TARGET.md).

## License

The repository's MIT license applies to original AeroOS project files. Debian packages and their artwork remain under their respective upstream licenses.
