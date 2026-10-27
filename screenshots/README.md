# Screenshots

Captured in a `debian:trixie` Docker container with the TDE trixie repo,
`tde-refresh-desktop-base-trinity` installed, and TDE running on Xvfb
(1280x800).

| File | What it shows |
| --- | --- |
| `desktop.png` | TDE session started with only the package's `/etc/trinity` profile: Ceratopsian wallpaper from `desktop-base`'s SVG, rendered at build time. |
| `win9x-chicago95-desktop.png` | After applying the **Chicago95** theme in the Theme Manager, plus `tde-win9x-panel`: teal desktop, Chicago95 icons, Start button. |
| `win9x-chicago95-theme-manager.png` | The Theme Manager with the Chicago95 theme applied (Windows widget style, Redmond decoration). |
| `win9x-tde-icons-desktop.png` | After applying the **Win9x** theme: same layout and colours, TDE's own icons. |
| `win9x-tde-icons-theme-manager.png` | The Theme Manager listing the Win9x theme. |
| `ksplash.png` | The `ceratopsian` KSplash theme (`ksplash --test --theme ceratopsian`) over the desktop. |

The `win9x-*` shots were taken with `tde-refresh-win9x-trinity` installed by
selecting each theme in the Theme Manager and clicking OK.

## Not captured

- **Win9x KSplash, TDM and Plymouth themes** (same limits as below; the KSplash
  and TDM artwork was built but not rendered in a session).

- **TDM login screen**: `tdm` would not start a greeter inside the container
  (no VT/real X server). The package override was verified to produce
  `Theme=/opt/trinity/share/apps/tdm/themes/ceratopsian` in the generated
  `tdmrc`, but the greeter itself has not been seen rendered. Check this on a
  real machine.
- **Plymouth**: the boot splash is Debian's own Ceratopsian theme from
  `desktop-base`, not part of this package. Plymouth's X11 renderer would not
  activate in the container, so there is no capture.
