# tde-refresh-trinity

A custom, independent Debian metapackage for the [Trinity Desktop
Environment](https://trinitydesktop.org/) (TDE), targeting Debian trixie.

## Why not just use `tde-trinity`?

The stock `tde-trinity`, `redmond-default-settings-trinity` and
`redmond-default-settings-ii-trinity` metapackages are outdated: they pull in
software that's no longer needed or no longer packaged in Debian, they force
a "Redmond" (Windows-like) default look-and-feel, and they're missing
integration with the modern Linux desktop stack. `tde-refresh-trinity`
installs a complete TDE desktop while:

- **Dropping legacy/no-longer-needed components:**
  `kfloppy` (floppy disk formatter), `k3b` (optical disc burning),
  `cervisia`/CVS support and the rest of the `tdesdk` dev-tools module,
  `lisa`/`kpf` (legacy LAN file/network discovery), `tdebindings`
  (dev-only language bindings), and similar cruft.
- **Not forcing the Redmond look-and-feel** — ships TDE's own stock defaults.
- **Not depending on the stock metapackages** — `tde-refresh-trinity` stands
  entirely on its own; it can be installed without pulling in any of
  `tde-trinity`'s or the `redmond-default-settings(-ii)-trinity` packages'
  dependencies.
- **Adding modern-stack integration** the stock packages lack: `plymouth`
  (boot splash), `pipewire-audio`, `xsettingsd`, `xdg-desktop-portal-tde`,
  `polkitd` + `pkexec` + `polkit-agent-tde`, `tdesudo`, `network-manager` +
  `network-manager-tde`, `tdebluez-trinity`, `tde-ebook-reader`, and
  `kdbusnotification-trinity`.
- Demoting bulky-but-optional pieces (`tdegames-trinity`, `tdetoys-trinity`,
  `dolphin-trinity`, `koffice-trinity`) and hardware/preference-specific
  pieces (`plymouth`, `plymouth-themes`, `tdebluez-trinity`,
  `tde-ebook-reader`) to `Recommends`, and niche dev tools
  (`tdewebdev-trinity`) to `Suggests`, rather than hard `Depends`.
  `Recommends` are still installed by default by apt, but can be removed
  without removing the metapackage.

## `tde-refresh-desktop-base-trinity` (Ceratopsian theme)

The stock `desktop-base-trinity` is a Debian 5/6-era fork of `desktop-base`:
it conflicts with (and replaces) the real `desktop-base`, ships MoreBlue/Nightly
artwork and has no Plymouth theme. This repo's second binary package,
`tde-refresh-desktop-base-trinity`, instead **depends on Debian's
`desktop-base`** and adds only the TDE pieces, re-skinned with the trixie
**Ceratopsian** artwork (the same theme as the Plymouth boot splash):

- default TDE wallpaper and system-wide profile (`/etc/trinity/{kdesktoprc,ksplashrc,twinrc}`)
- KSplash theme `ceratopsian`
- TDM login theme `ceratopsian`
- kompmgr/`compton-tde` compositor settings in `/etc/skel`

The wallpaper and login background are rendered at build time from
desktop-base's own SVGs. `tde-refresh-trinity` recommends it in place of
`desktop-base-trinity`. See `screenshots/`.

## `tde-refresh-win9x-trinity` (Windows 9x themes)

An optional third binary package (`Suggests` of the metapackage, nothing is
activated on install). It adds two themes to the **TDE Theme Manager**
(Control Center → Appearance & Themes → Theme Manager):

- **Chicago95** — Windows 95 look: Chicago95 Tux icons (Tux instead of a Windows logo) and cursors, teal desktop,
  Win95 grey/navy colour scheme, Redmond window decoration, Windows widget
  style, Chicago95 sounds.
- **Win9x** — the same layout and colours, but keeping TDE's own icons and
  cursors.

Also installed: Chicago95 GTK2/GTK3 themes (`/usr/share/themes`), wallpapers
and patterns (`/usr/share/wallpapers/Chicago95`), `chicago95` KSplash and TDM
themes (pick them in the Splash Screen and Login Manager modules), the
RetroTux Plymouth theme (inactive; Ceratopsian stays the default), and
`tde-win9x-panel`, which gives the panel a labelled **Start** button (the Theme
Manager cannot set that; run `tde-win9x-panel revert` to undo).

Sources: artwork is a trimmed, vendored copy of
[Chicago95](https://github.com/grassmunk/Chicago95) (`win9x/chicago95/`,
commit in `UPSTREAM_COMMIT`, GPL-3+/MIT). The TDE settings layout follows
`redmond-default-settings-ii-trinity`, but none of that package's
Kubuntu-specific artwork or dependencies are used. The KSplash/TDM artwork is
drawn from SVGs in `win9x/` and contains no Microsoft logo. No Windows logo is shipped: the Tux icon variant and the RetroTux
Plymouth theme are used. The Chicago95 sounds do imitate Windows' (see
`debian/copyright`).

## Building

```
dpkg-buildpackage -us -uc
```

## Known caveats

Most dependency names have been checked against TDE's published changelogs
and documentation (`xdg-desktop-portal-tde`, `polkit-agent-tde`,
`network-manager-tde`, `tdebluez-trinity`, `tde-ebook-reader`,
`kdbusnotification-trinity`), but the following have **not** yet been
verified against the real trixie archive and may need correcting once
tested against a system with the TDE trixie repo enabled:

- `plymouth-label` (Recommends of the theme package; confirm it resolves via CI)

The CI workflow in `.github/workflows/build.yml` dry-run installs the built
package against the live TDE trixie apt repository, so a green build means
every dependency name resolves. If any name is wrong, update
`debian/control` accordingly.
