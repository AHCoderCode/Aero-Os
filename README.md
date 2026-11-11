# AeroOS

**AeroOS 0.2.0-alpha** is a real Debian Live operating system with a lightweight, Windows-inspired desktop. Its first hardware target is the HP ProBook 4520s: Intel Core i5-480M, 8 GB RAM, Legacy BIOS and a user-reported Radeon HD 64xx-family GPU.

It is a bootable operating-system image, not a website or desktop mock-up. It runs from a USB drive and does not install to or repartition the laptop's internal Windows drive.

## Build and verification status

- Debian 13 Trixie amd64 Live ISO: built successfully by GitHub Actions.
- Legacy BIOS hybrid ISO: produced by the current build configuration.
- Source/configuration checks: run during every build.
- Actual HP ProBook hardware test: still required. Wi-Fi, audio, graphics acceleration, suspend/resume, brightness keys and USB boot behavior cannot be certified by CI alone.

Until the HP is tested, this remains an experimental alpha rather than a finished, hardware-certified OS.

## Desktop and included apps

The desktop uses Xfce and LightDM, customized with AeroOS wallpaper, dark blue styling, a centered Docklike taskbar, an Aero Start menu, system tray, volume control and clock. Compositing and GTK animations are disabled by default to reduce overhead on the older graphics hardware.

Included applications and tools:

- **File Explorer:** Thunar, removable-drive browsing and archive support.
- **Web browser:** Firefox ESR.
- **App Store / package manager:** Synaptic.
- **Settings:** Xfce Settings Manager, display, keyboard, power and desktop controls.
- **Terminal:** Xfce Terminal.
- **Calculator:** Galculator.
- **Text editor:** Mousepad.
- **Media player:** Parole.
- **System monitor:** Xfce Task Manager.
- **Power menu:** Xfce session logout/shutdown controls.
- **Networking and devices:** NetworkManager, Wi-Fi firmware families, Bluetooth utilities, audio controls and removable storage support.

A one-time **Set Up Persistence** utility is included for creating the full-persistence area on the AeroOS USB.

## Hardware profile

- Architecture: amd64 (64-bit Intel).
- Desktop: Xfce + LightDM.
- Firmware: Legacy BIOS / Syslinux hybrid media.
- Memory: zram uses a conservative 25% RAM cap with zstd compression.
- Graphics: Intel and legacy Radeon X.Org drivers plus Debian firmware packages.
- Performance defaults: compositing disabled, GTK animations disabled, dock previews disabled.

The exact Radeon PCI ID and Wi-Fi adapter are not yet confirmed. See [docs/HARDWARE-TARGET.md](docs/HARDWARE-TARGET.md).

## Build the ISO

GitHub Actions runs **Build AeroOS ISO** on pushes to `main` and on manual dispatch.

1. Open the repository's **Actions** tab.
2. Open the newest successful **Build AeroOS ISO** run.
3. Download and extract the `AeroOS-ISO` artifact.
4. Verify the ISO using `live-image-amd64.hybrid.iso.sha256`.
5. The ISO is `live-image-amd64.hybrid.iso`.

The artifact also includes the build log and El Torito boot report. The workflow retains artifacts for 30 days.

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

The new setup utility can create that partition in the unused space at the end of the same USB. For safety, it requires a one-time `toram` boot so the USB is not in use while its partition table is changed. It will only proceed when it identifies the AeroOS-labeled removable drive, the capacity is between 8 and 32 GiB, and every partition on that drive is unmounted. It refuses ambiguous or unsupported layouts.

Full persistence saves the writable system overlay: personal files, settings, installed packages and system changes. The USB's capacity is finite; the persistence partition uses the available space left after the ISO.

**Writing the ISO erases the USB.** Back up its contents first. Never select the laptop's internal disk in a disk tool. Windows normally cannot read the resulting ext4 persistence partition; do not format it when Windows prompts.

## Default Live account

The temporary account is `aero`. Debian Live's default password is `live`; the desktop auto-logs in for this USB session. Open Terminal and run `passwd` to set a private password. With full persistence enabled, the password change is retained across restarts.

## Layout

- `auto/config` — reproducible Debian Live configuration
- `config/package-lists/` — desktop, firmware and utility packages
- `config/includes.chroot/` — AeroOS theme, launchers and system defaults
- `config/hooks/` — image finalization
- `scripts/` — source/configuration validation
- `.github/workflows/` — automated ISO builder
- `docs/` — hardware and USB/persistence instructions

## License

The repository's MIT license applies to original AeroOS project files. Debian packages and their artwork remain under their respective upstream licenses.
