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

- `tdesudo` (the app exists upstream; the binary package may be named
  `tdesudo-trinity`)

The CI workflow in `.github/workflows/build.yml` dry-run installs the built
package against the live TDE trixie apt repository, so a green build means
every dependency name resolves. If any name is wrong, update
`debian/control` accordingly.
