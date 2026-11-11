# USB boot and full persistence

## Before writing the image

- Back up anything on the USB. Writing a hybrid image overwrites its current partition layout and contents.
- The target must be the **USB device**, not a partition and not the laptop's internal drive.
- The first boot is a Live USB test only. Do not install AeroOS to the internal disk.
- A successful ISO build does not prove the laptop's hardware works.

## Full persistence

AeroOS enables these Debian Live boot options:

```text
boot=live components persistence username=aero
```

For full-root persistence, the separate persistence volume must:
1. Use an ext4 filesystem.
2. Have the filesystem label `persistence`.
3. Contain a file named `persistence.conf` at the filesystem root.
4. Have this exact line in that file:

```text
/ union
```

This saves runtime changes across reboots, including the live user's home, desktop settings and package changes. Installed applications and updates use the same finite USB space.

Official Debian Live documentation:
https://live-team.pages.debian.net/live-manual/html/live-manual.en.html#persistence

## Using the space left on the USB

After copying a hybrid ISO to a USB, its initial partition contains the live system. The remaining unallocated space can be made into a new ext4 partition and labelled `persistence`. Debian Live documents this workflow:
https://live-team.pages.debian.net/live-manual/html/live-manual.en.html#using-the-space-left-on-a-usb-stick

Windows normally does not read ext4 in File Explorer. That is expected. Do not format an ext4 persistence partition just because Windows prompts you to.

## Your 14.6 GB USB

The reported capacity is about 14.6 GB. The system image and full-root persistence must share this capacity. We must measure the final ISO before deciding how much space remains. Do not assume all 14.6 GB is available for personal files.

Windows has no built-in ext4 formatter. A safe preparation workflow must be confirmed after the image has built. Until then, do not format, resize or repartition the USB.

## Boot the HP ProBook 4520s

1. Shut the laptop down completely.
2. Insert the AeroOS USB.
3. Power on and tap **F9** to open the HP boot-device menu (the key can vary by BIOS revision).
4. Select the USB device.
5. Choose the normal AeroOS Live entry.
6. To return to Windows, shut down and remove the USB before powering on again.

If the USB is not listed, check that USB boot is enabled in BIOS. Do not change SATA mode or edit the internal drive's partitions.

## Shutdown

Use the desktop power menu and wait for the laptop to turn off before removing the USB. Removing it while AeroOS is running can corrupt the persistence filesystem and lose recent changes.
