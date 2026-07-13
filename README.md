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
  `cervisia`/CVS support, `lisa`/`kpf` (legacy LAN file/network discovery),
  `tdebindings` (dev-only language bindings), and similar cruft.
- **Not forcing the Redmond look-and-feel** — ships TDE's own stock defaults.
- **Not depending on the stock metapackages** — `tde-refresh-trinity` stands
  entirely on its own; it can be installed without pulling in any of
  `tde-trinity`'s or the `redmond-default-settings(-ii)-trinity` packages'
  dependencies.
- **Adding modern-stack integration** the stock packages lack: `plymouth`
  (boot splash), `pipewire-audio`, `xsettingsd`, `xdg-desktop-portal-trinity`,
  `polkitd` + `pkexec` + `polkit-agent-tde`, `tdesudo`, `network-manager` +
  `network-manager-tde`, `tdebluez-trinity`, `tde-ebook-reader`, and
  `kdbusnotication-trinity`.
- Demoting bulky-but-optional pieces (`tdegames-trinity`, `tdetoys-trinity`,
  `dolphin-trinity`, `koffice-trinity`) to `Recommends`, and niche dev tools
  (`tdewebdev-trinity`) to `Suggests`, rather than hard `Depends`.

## Building

```
dpkg-buildpackage -us -uc
```

## Known caveats

This packaging was authored without live access to the Debian/TDE trixie
archive (the sandbox this was built in has no route to
trinitydesktop.org / packages.debian.org / salsa.debian.org). The dependency
list is best-effort based on TDE's known module structure. In particular,
the following package names have **not** been verified against the real
trixie archive and may need correcting once tested against a system with
the TDE trixie repo enabled:

- `xdg-desktop-portal-trinity`
- `polkit-agent-tde`
- `tdesudo`
- `network-manager-tde`
- `tdebluez-trinity`
- `tde-ebook-reader`
- `kdbusnotication-trinity`

If any of these don't exist or are named differently, update
`debian/control` accordingly.
