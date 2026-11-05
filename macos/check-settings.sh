#!/bin/sh
# The Theme Manager XML and the helper's settings.conf must describe the same
# look. Fails the build if a colour, widget style or window decoration differs.
# Usage: check-settings.sh <theme.xml> <settings.conf>
xml=$1 conf=$2 bad=0
need() {
	grep -qxF "$1" "$conf" || { echo "$conf: missing or different: $1 (from $xml)" >&2; bad=1; }
}
tab=$(sed -n 's/.*<\([a-zA-Z]*\) rgb="#\(..\)\(..\)\(..\)" object="\(global\|twin\)".*/\1 \2 \3 \4 \5/p' "$xml")
[ -n "$tab" ] || { echo "$xml: no colours found" >&2; exit 1; }
while read -r key r g b obj; do
	[ "$obj" = global ] && group=General || group=WM
	need "kdeglobals|$group|$key|$(printf '%d,%d,%d' "0x$r" "0x$g" "0x$b")"
done <<LIST
$tab
LIST
need "kdeglobals|General|widgetStyle|$(sed -n 's/.*<widgets name="\([^"]*\)".*/\1/p' "$xml")"
need "twinrc|Style|PluginLib|$(sed -n 's/.*<wm type="builtin" name="\([^"]*\)".*/\1/p' "$xml")"
need "twinrc|Style|ButtonsOnLeft|$(sed -n 's/.*<buttons left="\([^"]*\)".*/\1/p' "$xml")"
need "twinrc|Style|ButtonsOnRight|$(sed -n 's/.*<buttons left="[^"]*" right="\([^"]*\)".*/\1/p' "$xml")"
need "kdeglobals|KDE|macStyle|true"
exit $bad
