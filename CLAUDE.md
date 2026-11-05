# CLAUDE.md

Guidance for AI assistants (and humans) working in this repository.

## What this repo is

`tde-refresh` builds a Debian **metapackage**, `tde-refresh-trinity`: a curated,
self-contained way to install the [Trinity Desktop Environment](https://trinitydesktop.org/)
(TDE) R14.1.7 on Debian **trixie**. A metapackage ships no real content of its own
— it is just a package whose `Depends`/`Recommends`/`Suggests` fields pull in the
set of TDE packages we consider a good default desktop.

The same source also builds optional theme packages, which do ship content:

| Package | Content lives in | Helper |
| --- | --- | --- |
| `tde-refresh-desktop-base-trinity` | `tde-theme/` | none (postinst edits `tdmrc`) |
| `tde-refresh-win9x-trinity` | `win9x/` | `tde-win9x-panel`, `tde-win9x-tdm` |
| `tde-refresh-macclassic-trinity` | `macos/classic/` | `tde-macclassic` |
| `tde-refresh-macosx-trinity` | `macos/osx/` | `tde-macosx` |

It is an independent alternative to the stock `tde-trinity`,
`redmond-default-settings-trinity`, and `redmond-default-settings-ii-trinity`
metapackages. Compared to those, `tde-refresh-trinity`:

- drops legacy/no-longer-needed components (`kfloppy`, `k3b`, `cvs`/`cervisia`
  and the rest of `tdesdk`, `lisa`/`kpf`, `tdebindings`, etc.);
- does **not** force the "Redmond" (Windows-like) default look-and-feel — it
  ships TDE's own stock defaults;
- does **not** depend on the stock metapackages, so none of their unwanted
  dependencies get pulled in;
- adds modern desktop-stack integration (pipewire-audio, xsettingsd,
  xdg-desktop-portal, polkit, network-manager integration, D-Bus
  notifications, etc.);
- demotes bulky-but-optional and hardware/preference-specific pieces to
  `Recommends`, and niche dev tooling to `Suggests`.

The rationale is documented in more detail in `README.md`.

## Repository layout

```
.
├── README.md                 # Human-facing rationale + build/caveat notes
├── .gitignore                # Ignores debhelper build artifacts and /out/
├── debian/
│   ├── control               # THE core file: package metadata + dependency lists
│   ├── changelog             # Package version history (drives the build version)
│   ├── copyright             # DEP-5 copyright/licensing (GPL-2+)
│   ├── rules                 # Build recipe — renders artwork, installs the themes
│   └── source/format         # "3.0 (native)" — native package, no separate orig tarball
├── tde-theme/                # Ceratopsian theme data
├── win9x/                    # Windows 9x theme data and helpers
├── macos/                    # Mac OS Classic and Mac OS X theme data
│   ├── bin/tde-mac-theme.in  # Template for tde-macclassic and tde-macosx
│   ├── check-settings.sh     # Build-time check: XML and settings.conf must agree
│   ├── classic/  osx/        # theme/ (Theme Manager), settings.conf, kickerrc, profile
├── screenshots/
└── .github/workflows/
    ├── build.yml             # CI: build + lintian + dependency-resolution check
    └── release.yml           # Publishes the .debs when a v* tag is pushed
```

There is no compiled code here, only packaging, theme data and small shell
helpers. For the metapackage, `debian/control` is where the work happens.

## The one file that matters: `debian/control`

Almost every change to this repo is an edit to the dependency lists in
`debian/control`. Its structure:

- **`Depends:`** — packages that make up the core desktop; always installed.
- **`Recommends:`** — installed by default by apt, but removable without
  removing the metapackage. Use for bulky/optional or hardware/preference
  -specific pieces (games, toys, koffice, plymouth, bluetooth, ebook reader).
- **`Suggests:`** — not installed by default. Use for niche/dev-only tooling.
- `${misc:Depends}` must stay in `Depends` — debhelper substitutes it.

### Conventions when editing dependencies

- **TDE binary package names are usually suffixed `-trinity`** (e.g.
  `tdebase-trinity`, `xdg-desktop-portal-trinity`, `tdesudo-trinity`,
  `network-manager-tde` — note some upstream pieces use the `-tde` suffix
  instead). Do not guess: an upstream *application* name (`tdesudo`,
  `xdg-desktop-portal-tde`) is often **not** the *Debian binary package* name.
  Both of those were corrected to `-trinity`/`-trinity` in the git history —
  see commits `25f6c82` and `de313d8`.
- Verify any new/changed dependency name resolves against the live TDE trixie
  apt repo. The CI `dep-check` job does exactly this; a green build means every
  name resolves.
- Keep the `Description:` in `debian/control` and the summary in `README.md`
  roughly in sync when you add/remove notable dependencies.

### Bumping the version

Add a new top entry to `debian/changelog` (the topmost version is what
`dpkg-buildpackage` builds). Because the source format is `3.0 (native)`, the
version has no Debian revision (`1.0`, not `1.0-1`). Prefer `dch` if available;
otherwise mirror the existing entry's exact format, including the RFC-2822
timestamp line beginning with ` -- `.

## Building locally

Requires a Debian/Ubuntu-like environment with packaging tools
(`build-essential`, `debhelper`, `desktop-base`, `librsvg2-bin`, `fonts-dejavu-core`,
and `lintian` for the lint step):

```
dpkg-buildpackage -us -uc      # -us -uc = don't sign the source/changes
lintian ../tde-refresh-trinity_*.changes
```

The build drops artifacts (`.deb`, `.changes`, `.buildinfo`) in the **parent**
directory. `.gitignore` covers the in-tree debhelper detritus
(`debian/.debhelper/`, `debian/files`, `debian/*.substvars`, etc.) and an
optional `/out/` dir; never commit build artifacts.

Note the dependencies mostly live only in the TDE trixie repository, so a plain
`dpkg-buildpackage` succeeds (the build does not need TDE present) but *installing* the result requires that repo enabled —
see the CI `dep-check` job for how it's added.

## CI (`.github/workflows/build.yml`)

Runs on every `push` and `pull_request`, in a `debian:trixie` container, in two
jobs:

1. **`build`** — installs the build tools listed above, runs
   `dpkg-buildpackage -us -uc`, moves artifacts into `out/`, runs `lintian`,
   and uploads the `.deb` as an artifact.
2. **`dep-check`** (needs `build`) — downloads the artifact, enables the TDE
   trixie apt repo (installs `trinity-keyring`, adds the sources list), and runs
   `apt-get install -s ./tde-refresh-*_all.deb` (a `-s` **simulate**).
   This is the real gate on dependency-name correctness: if any name in
   `debian/control` doesn't resolve, this job fails.

When you change dependency names, expect `dep-check` to be the job that catches
mistakes. `lintian` in the `build` job catches packaging-metadata problems.

## Working conventions for this repo

- **Scope is small and packaging-focused.** Most tasks are "add/remove/re-tier a
  dependency" or "fix a metadata field." Keep changes minimal and targeted.
- **Match existing style** in `debian/control`: one dependency per line, aligned
  and comma-terminated, trailing `${misc:Depends}` last in `Depends`.
- **Keep `README.md` and `debian/control` consistent.** If you change the
  dependency set, update the README's rationale and the control `Description:`
  and clear/adjust any stale entries in the README "Known caveats" section.
- `debian/rules` overrides exist to render and install theme artwork. Don't add
  more unless a package genuinely needs them.

## Mac theme notes

- The Theme Manager has no CLI and cannot set the global menu (`kdeglobals [KDE]
  macStyle`), panel applets or Konqueror layout, so the helpers write those.
- `settings.conf` repeats values from the theme XML. Change both:
  `macos/check-settings.sh` fails the build if they disagree.
- A new file written by `apply` must be added to `LOCAL_FILES` or `HOME_FILES` in
  the template, or `revert` will not restore it.
- To test, start TDE under Xvfb with a throwaway `HOME` containing
  `[General] FirstLogin=false` in `kpersonalizerrc`. Log out and back in after
  `apply` before judging: running programs keep the old settings.

## Git & workflow

- Development happens on feature branches; changes land on `main` via pull
  request (see the merge commits in `git log`).
- Do not commit build output. Commit only the tracked packaging/doc files.
- Trust CI's `dep-check` over local reasoning for whether a dependency name is
  correct against the trixie archive.
