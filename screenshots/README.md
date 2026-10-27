# Screenshots

Captured in a `debian:trixie` Docker container with the TDE trixie repo,
`tde-refresh-desktop-base-trinity` installed, and TDE running on Xvfb
(1280x800).

| File | What it shows |
| --- | --- |
| `desktop.png` | TDE session started with only the package's `/etc/trinity` profile: Ceratopsian wallpaper from `desktop-base`'s SVG, rendered at build time. |
| `ksplash.png` | The `ceratopsian` KSplash theme (`ksplash --test --theme ceratopsian`) over the desktop. |

## Not captured

- **TDM login screen**: `tdm` would not start a greeter inside the container
  (no VT/real X server). The package override was verified to produce
  `Theme=/opt/trinity/share/apps/tdm/themes/ceratopsian` in the generated
  `tdmrc`, but the greeter itself has not been seen rendered. Check this on a
  real machine.
- **Plymouth**: the boot splash is Debian's own Ceratopsian theme from
  `desktop-base`, not part of this package. Plymouth's X11 renderer would not
  activate in the container, so there is no capture.
