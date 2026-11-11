# USB boot and full persistence

## Before writing the image

- Back up anything on the USB. Writing a hybrid image overwrites its current partition layout and contents.
- The target must be the **USB device**, not a partition and not the laptop's internal drive.
- The first boot is a Live USB test only. Do not install AeroOS to the internal disk.
- A successful ISO build does not prove the laptop's hardware works.

## Download and verify the ISO from Windows 10

1. Open the repository's **Actions** tab.
2. Open the newest successful **Build AeroOS ISO** run.
3. Download the `AeroOS-ISO` artifact and extract the ZIP.
4. Open PowerShell in the extracted folder and run:

```powershell
$line = Get-Content .\live-image-amd64.hybrid.iso.sha256 | Select-Object -First 1
$expected = ($line -split '\s+')[0].ToLowerInvariant()
$actual = (Get-FileHash .\live-image-amd64.hybrid.iso -Algorithm SHA256).Hash.ToLowerInvariant()
if ($expected -ne $actual) { throw "ISO checksum does not match. Do not write this file to USB." }
"ISO checksum verified."
```

The ISO file is named `live-image-amd64.hybrid.iso`.

## Write the bootable USB

1. Open Rufus and select the USB by its capacity (your drive was reported as about 14.6 GB).
2. Select `live-image-amd64.hybrid.iso` as the boot selection.
3. Start the write. If Rufus asks for ISO mode or DD mode, choose **DD mode** for this hybrid image.
4. Confirm only after checking that the selected target is your USB. This erases the USB.
5. Wait for Rufus to finish and safely eject the USB.

Do not select the laptop's internal drive at any stage.

## First boot on the HP ProBook 4520s

1. Shut down Windows completely.
2. Insert the AeroOS USB.
3. Power on and tap **F9** to open the HP boot-device menu (the key can vary by BIOS revision).
4. Select the USB device.
5. Choose the normal AeroOS Live entry.
6. The desktop automatically signs in to the temporary user `aero`.

To return to Windows, shut down AeroOS, wait for the laptop to turn off, remove the USB, and power on again.

## Set up maximum persistence on the same USB

The ISO enables Debian Live's `persistence` boot option, but full persistence becomes active only after a separate ext4 area labelled `persistence` has been created with a root-level `persistence.conf` containing exactly:

```text
/ union
```

AeroOS includes a guarded utility to create this area in the unused space at the end of the same USB. Use this one-time procedure:

1. Restart and boot the AeroOS USB again.
2. At the Syslinux boot menu, highlight the normal AeroOS entry and press **TAB** to edit its boot line.
3. Add one space and the word `toram` to the end of the line, then press **Enter**.
4. Wait for the desktop. The `toram` option copies the read-only live medium into RAM, so the USB can be safely partitioned. It makes this one boot slower and uses extra RAM; do not use it for normal daily boots.
5. Open **Set Up Persistence** on the desktop. When the authorization prompt appears, enter the AeroOS user's password (`live` unless you have already changed it).
6. Read the device summary carefully. The utility only continues for the removable drive containing the `AEROOS_LIVE` volume, with a capacity between 8 and 32 GiB, and only when all of that drive's partitions are unmounted. It creates an ext4 partition in trailing unallocated space and writes `persistence.conf` with `/ union`.
7. When the success message appears, restart normally. Do not add `toram` on everyday boots.

The setup tool is deliberately conservative. If your USB does not report itself as removable, the volume label is missing, the partition table is unsupported, or the free space cannot be verified, it refuses to make changes. Do not work around that refusal by selecting another disk or typing a guessed device path.

After the next normal boot, the Welcome screen should report **Full persistence is active**. Create a small test file in your home folder, restart normally, and check that it remains.

## What full persistence saves

With the separate ext4 volume and `/ union` configuration, the writable Live system overlay is retained. This includes:

- Personal files and folders.
- Desktop settings, wallpaper and preferences.
- Browser profile and saved browser settings.
- Installed applications and package updates.
- System configuration changes and your changed user password.

All of this uses the USB's finite capacity. The ISO occupies about 1.3 GiB in the current build; the rest of the drive is available for the persistence area, subject to partition alignment and filesystem overhead.

Windows normally cannot read ext4. If Windows asks to format the persistence volume, choose **Cancel**. Formatting it in Windows would erase persistence.

## Important notes

- Do not remove the USB while AeroOS is running. Shut down fully first.
- The setup utility creates a partition only in the unused trailing area. It does not resize the ISO partition.
- Full persistence is not encryption. Anyone with physical access to the USB may be able to access its saved data.
- If the persistence setup utility refuses to continue, stop and share the exact message. Do not use Disk Management or another partition tool to guess at device numbers.
- There is no automatic installer for the laptop's internal drive. The Windows installation is not modified by the USB boot process.

## Debian Live references

- [Debian Live Manual — persistence](https://live-team.pages.debian.net/live-manual/html/live-manual.en.html#persistence)
- [Debian live-boot manual — toram](https://manpages.debian.org/trixie/live-boot-doc/live-boot.7.en.html)

The Debian Live manual explains that `/ union` makes the complete writable overlay persistent and that `toram` copies the read-only medium into RAM before the root filesystem is mounted.
