# Hardware target and known unknowns

## Confirmed target

| Item | Value |
| --- | --- |
| Laptop | HP ProBook 4520s |
| CPU | Intel Core i5-480M, 2.67 GHz |
| CPU layout | 2 cores / 4 logical processors |
| RAM | 8 GB |
| Firmware | Legacy BIOS |
| Graphics | User-reported AMD Radeon HD 64xx-family; exact PCI device unknown |

## Design choices

- Debian 13 Trixie amd64 is the stable base.
- Syslinux/ISOLINUX hybrid media targets traditional BIOS boot.
- Xfce and LightDM keep the desktop relatively light.
- zram provides compressed swap, capped at 25% RAM in this first profile.
- Debian firmware packages cover common AMD graphics and Broadcom, Intel, Realtek and Atheros networking devices.

## Must be checked on the actual laptop

- Exact graphics PCI ID and Radeon firmware/acceleration.
- Exact Wi-Fi adapter and firmware.
- Ethernet, audio codec, microphone, webcam, Bluetooth and card reader.
- Brightness/volume function keys.
- Suspend/resume, lid switch and battery reporting.
- USB boot behavior on this BIOS.
- Responsiveness with Firefox and multiple tabs.

## Identify Wi-Fi and graphics in Windows

Open **Device Manager** → expand **Network adapters** or **Display adapters** → right-click the device → **Properties** → **Details** → **Hardware Ids**. Share only the first hardware-ID line, not a serial number or other personal identifier.
