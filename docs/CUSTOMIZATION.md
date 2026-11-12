# AeroOS customization

AeroOS includes a Control Center so common desktop changes do not require terminal commands.

## Open the Control Center

- Double-click **Settings** on the desktop, or
- Open the **Start** button on the taskbar and choose **AeroOS Control Center**.

## Aero taskbar

The default taskbar is arranged as follows:

- **Left:** the AeroOS four-pane Start button.
- **Centre:** pinned and running app icons in the Docklike group.
- **Right:** system tray, volume and clock.

The taskbar spans the bottom edge, but its background is highly translucent so the app icons remain visually prominent. The two expanding separators around Docklike keep the app group centred between Start and the system tray. The existing wallpaper is deliberately unchanged.

The taskbar uses Xfwm compositing to render real transparency. The **Transparent taskbar (recommended)** performance profile keeps compositing enabled but leaves GTK animations off. The **Solid taskbar (maximum battery/compatibility)** profile disables compositing if the older graphics hardware struggles; this makes the taskbar background solid.

## Start menu

Click the Start icon at the left of the taskbar or press the **Windows/Super** key.

The menu opens with your pinned/favorite applications. It also includes search, application categories and a recently-used list. To pin an application, browse to it, right-click it and choose **Add to Favorites**. Drag favorites to reorder them.

The default favorites include Firefox, File Explorer, Terminal, Calculator, Text Editor, Media Player, Synaptic and AeroOS Control Center. These applications are also pinned to the centred taskbar dock.

## Appearance and accent colors

Open **Theme and accent color** and select one of six presets:

- Aero Dark - Blue
- Aero Dark - Violet
- Aero Dark - Teal
- Aero Light - Blue
- Aero Light - Violet
- Aero Light - Teal

The selection changes the GTK theme, Papirus icon theme and AeroOS accent palette while keeping the taskbar translucent. It is saved in your home directory and remains with full USB persistence. Already-open applications may need to be closed and reopened to use the new GTK colors.

## Wallpaper and desktop icons

The default wallpaper is unchanged in this taskbar update. The existing **Wallpaper and desktop icons** option remains available for users who choose to change their own wallpaper, icon visibility or icon size.

## Taskbar and Start menu settings

Open **Taskbar and Start menu** to change panel position, size, appearance, items and launchers. Xfce saves those changes in your user profile. Start-menu favorites can be managed from the Start menu itself.

## Display, keyboard and power

The Control Center opens the native Xfce dialogs for screen resolution, keyboard shortcuts and power/battery behavior. Choose only display modes supported by your laptop screen.

## Performance

The transparent taskbar requires compositing. The recommended profile enables lightweight compositing without GTK animations. If the old Intel/Radeon graphics become slow or show visual glitches, choose **Solid taskbar (maximum battery/compatibility)** to disable compositing; the panel will become solid.

## Full customization

**All system settings** opens Xfce Settings Manager. It includes appearance, icons, fonts, mouse, keyboard, display, window manager and other desktop preferences. These are native Xfce settings, not simulated controls.

With full-root USB persistence enabled, your theme, taskbar, Start-menu favorites, wallpaper, keyboard and other user preferences are saved across reboots.
