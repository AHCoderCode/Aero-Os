# AeroOS

**AeroOS is an experimental lightweight, Windows-inspired Linux desktop for older 64-bit laptops.**

First hardware target: HP ProBook 4520s — Intel Core i5-480M (2 cores / 4 threads, 2.67 GHz), 8 GB RAM, Legacy BIOS, and a user-reported AMD Radeon HD 64xx-family GPU (exact PCI model still unknown).

## What this repository builds

A Debian 13 (Trixie) Live system using Debian's official Live toolchain:
- amd64 Linux kernel and Syslinux/ISOLINUX hybrid media for Legacy BIOS boot
- Xfce + LightDM for a comparatively light graphical desktop
- AeroOS dark-blue styling, custom wallpaper, Aero launcher and desktop shortcuts
- Windows-key Start menu shortcut, task list, system tray, volume and clock controls
- NetworkManager, sound controls, Bluetooth utilities, power tools and everyday applications
- zram configured with a conservative 25% RAM cap
- Debian Live persistence enabled; the intended full-persistence setting is `/ union`

Debian 13 Trixie is the current stable Debian release: https://www.debian.org/releases/stable/

## Status: experimental alpha

This is a genuine Linux Live OS build configuration, not a browser mock-up. It is **not yet a finished or hardware-verified operating system**. A successful CI build proves only that an ISO was produced. Wi-Fi, graphics acceleration, audio, suspend/resume, brightness keys and other devices must be tested on the actual HP.

The image has no automatic internal-drive installer. The first milestone is USB-only testing, leaving Windows untouched.

## Build the ISO

GitHub Actions runs **Build AeroOS ISO** on pushes to `main` and on manual dispatch.

1. Open the repository's **Actions** tab.
2. Open the newest **Build AeroOS ISO** run.
3. Download the `AeroOS-ISO` artifact and extract it.
4. Verify the ISO with its included SHA-256 file.

Expected ISO: `live-image-amd64.hybrid.iso`.

Build locally on Debian Trixie amd64 with root access:

```bash
sudo apt update
sudo apt install live-build debootstrap xorriso isolinux syslinux-common squashfs-tools dosfstools mtools
./auto/config
sudo lb build
```

## USB and persistence

Read [docs/USB-AND-PERSISTENCE.md](docs/USB-AND-PERSISTENCE.md) **before writing the image**.

The ISO enables the `persistence` boot option. For full-root persistence, Debian Live requires a separate ext4 volume labelled `persistence` with a root-level `persistence.conf` containing:

```text
/ union
```

The partition must be created in the space left after writing the hybrid ISO. Windows normally cannot browse ext4; this is expected.

**Writing a hybrid ISO erases the USB.** Back up the USB and verify the artifact first. Never select the laptop's internal drive in a disk/partition tool.

## Hardware notes

- `amd64` is the correct architecture for the 64-bit Intel Core i5-480M.
- The build uses Debian's generic kernel, not a custom patched kernel.
- Intel and Radeon X.Org drivers plus common Debian firmware packages are included.
- Exact Wi-Fi hardware is still unknown; its Windows Device Manager hardware ID is needed to confirm the right firmware.
- zram is compressed swap, not extra physical RAM.
- The old CPU and USB flash drive will not perform like a modern SSD; browser-heavy workloads can still use significant memory.

## Default Live account

The temporary account is `aero`; the default Debian Live password is `live`. Change it immediately after startup with `passwd`. Persistence means this password change is retained across reboots, so choose a password you will remember.

## Layout

- `auto/config` — reproducible Debian Live configuration
- `config/package-lists/` — desktop, firmware and utility packages
- `config/includes.chroot/` — AeroOS theme and system defaults
- `config/hooks/` — branding and image cleanup
- `.github/workflows/` — automated ISO builder
- `docs/` — hardware and USB/persistence notes

## License

The repository's MIT license applies to original AeroOS project files. Debian packages and their artwork remain under their respective upstream licenses.
