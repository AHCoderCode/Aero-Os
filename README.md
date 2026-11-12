# AeroOS

**AeroOS 0.3.1-rc1** is a real Debian Live operating system with a lightweight, Windows-inspired desktop. Its first hardware target is the HP ProBook 4520s: Intel Core i5-480M, 8 GB RAM, Legacy BIOS and a user-reported Radeon HD 64xx-family GPU.

It is a bootable operating-system image, not a website or desktop mock-up. It runs from a USB drive and does not install to or repartition the laptop's internal Windows drive.

## Build and verification status

- Debian 13 Trixie amd64 Live ISO: built successfully by GitHub Actions.
- Legacy BIOS hybrid ISO: produced by the build and checked with xorriso.
- Source/configuration checks and persistence-parser tests: run during every build.
- Actual HP ProBook hardware test: still required. Wi-Fi, audio, graphics acceleration, suspend/resume, brightness keys and USB boot behavior cannot be certified by CI alone.

Until the HP is tested, this remains a release candidate rather than a finished, hardware-certified OS.

## Desktop and included apps

The desktop uses Xfce and LightDM with an AeroOS translucent taskbar. The Start button is at the left, pinned and running app icons are centred in a Docklike group, and the system tray, volume and clock are at the right. The Start menu provides favorites, recent applications, categories and search.

Xfwm compositing is enabled for actual panel transparency. GTK animations and Docklike previews remain disabled to limit overhead on the older graphics hardware. A solid-taskbar profile is available if the graphics adapter struggles.

Included applications and tools:

- **File Explorer:** Thunar, removable-drive browsing and archive support.
- **Web browser:** Firefox ESR.
- **App Store / package manager:** Synaptic.
- **Settings:** AeroOS Control Center and Xfce Settings Manager.
- **Terminal:** Xfce Terminal.
- **Calculator:** Galculator.
- **Text editor:** Mousepad.
- **Media player:** Parole.
- **System monitor:** Xfce Task Manager.
- **Power menu:** Xfce session logout/shutdown controls.
- **Networking and devices:** NetworkManager, Wi-Fi firmware families, Bluetooth utilities, audio controls and removable storage support.

The Control Center provides six light/dark theme and accent presets, wallpaper and icon settings, taskbar configuration, display, keyboard, power and performance options. A one-time **Set Up Persistence** utility creates the full-persistence area on the AeroOS USB.

## Hardware profile

- Architecture: amd64 (64-bit Intel).
- Desktop: Xfce + LightDM.
- Firmware: Legacy BIOS / Syslinux hybrid media.
- Memory: zram uses a conservative 25% RAM cap with zstd compression.
- Graphics: Intel and legacy Radeon X.Org drivers plus Debian firmware packages.
- Performance defaults: lightweight compositing enabled for transparency, GTK animations disabled, dock previews disabled.

The exact Radeon PCI ID and Wi-Fi adapter are not yet confirmed. See [docs/HARDWARE-TARGET.md](docs/HARDWARE-TARGET.md).

## Customize AeroOS

Open **AeroOS Control Center** from the desktop Settings shortcut or Start menu. The taskbar has a Start button at the left, app icons in the centre, and indicators at the right. Click Start or press the Windows/Super key for favorites, recent apps, categories and search. Right-click an app in Start and choose **Add to Favorites** to pin it.

The existing desktop wallpaper is unchanged by this taskbar update. See [docs/CUSTOMIZATION.md](docs/CUSTOMIZATION.md) for appearance, taskbar and menu settings.

## Build the ISO

GitHub Actions runs **Build AeroOS ISO** on pushes to `main` and on manual dispatch.

1. Open the repository's **Actions** tab.
2. Open the newest successful **Build AeroOS ISO** run.
3. Download and extract the `AeroOS-ISO` artifact.
4. Verify the ISO using `live-image-amd64.hybrid.iso.sha256`.
5. The ISO is `live-image-amd64.hybrid.iso`.

The artifact also includes the build log and El Torito boot report. Each workflow artifact is retained for 30 days.

Build locally on Debian Trixie amd64 with root access:

```bash
sudo apt update
sudo apt install live-build debootstrap xorriso isolinux syslinux-common squashfs-tools dosfstools mtools ca-certificates gpgv libxml2-utils python3
./auto/config
sudo lb build
```

## USB boot and maximum practical persistence

Read [docs/USB-AND-PERSISTENCE.md](docs/USB-AND-PERSISTENCE.md) before writing the image.

AeroOS boots with Debian Live's `persistence` option. Full-root persistence uses an ext4 partition labelled `persistence` with a root-level `persistence.conf` containing:

```text
/ union
```

The setup utility can create that partition in the unused space at the end of the same USB. For safety, it requires a one-time `toram` boot so the USB is not in use while its partition table is changed. It will only proceed when it identifies the AeroOS-labeled removable drive, the capacity is between 8 and 32 GiB, and every partition on that drive is unmounted. It refuses ambiguous or unsupported layouts.

Full persistence saves the writable system overlay: personal files, settings, installed packages and system changes. The USB's capacity is finite; the persistence partition uses the available space left after the ISO.

**Writing the ISO erases the USB.** Back up its contents first. Never select the laptop's internal drive in a disk tool. Windows normally cannot read the resulting ext4 persistence partition; do not format it when Windows prompts.

## Default Live account

The temporary account is `aero`. Debian Live's default password is `live`; the desktop auto-logs in for this USB session. Open Terminal and run `passwd` to set a private password. With full persistence enabled, the password change is retained across restarts.

## Layout

- `auto/config` — reproducible Debian Live configuration
- `config/package-lists/` — desktop, firmware and utility packages
- `config/includes.chroot/` — AeroOS theme, launchers and system defaults
- `config/hooks/` — image finalization
- `scripts/` — source/configuration validation and tests
- `.github/workflows/` — automated ISO builder
- `docs/` — hardware, customization and USB/persistence instructions

## License

The repository's MIT license applies to original AeroOS project files. Debian packages and their artwork remain under their respective upstream licenses.
