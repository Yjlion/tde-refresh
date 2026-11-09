#!/usr/bin/python3
"""Generate the committed KSplash/TDM PNGs for a new Debian release theme.

Not run at package build time. Run it once when adding a theme, look at the
result and commit it:

    rsvg-convert -w 1920 -h 1200 \\
        /usr/share/desktop-base/NAME-theme/wallpaper/contents/images/1920x1200.svg -o wp.png
    rsvg-convert -w 1920 -h 1200 \\
        /usr/share/desktop-base/NAME-theme/login/background.svg -o login.png   # or background-nologo.svg
    tde-theme/make-theme-art.py NAME wp.png login.png R,G,B

R,G,B is the colour of the KSplash icon bar. The icon bars are the Ceratopsian
ones with their background moved to that colour. Needs python3-pil and
fonts-dejavu-core.
"""
import os
import shutil
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REF_KSPLASH = os.path.join(HERE, "ksplash", "ceratopsian")
REF_TDM = os.path.join(HERE, "tdm", "ceratopsian")
# The two background tones of the Ceratopsian icon bars.
REF_BG = ((69, 100, 116), (53, 86, 105))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def rebase(src, bar):
    """Shift the bar background to `bar`, leaving the icons alone.

    Each pixel is moved by (bar - old background), scaled by how close it is
    to the old background, so icon edges and shadows follow smoothly.
    """
    im = Image.open(src).convert("RGB")
    delta = [bar[i] - REF_BG[0][i] for i in range(3)]
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            p = px[x, y]
            dist = min(sum((p[i] - bg[i]) ** 2 for i in range(3)) ** 0.5 for bg in REF_BG)
            weight = 1.0 - min(max((dist - 6.0) / 42.0, 0.0), 1.0)
            px[x, y] = tuple(min(max(round(p[i] + weight * delta[i]), 0), 255) for i in range(3))
    return im


def main():
    name, wallpaper, login, colour = sys.argv[1:5]
    bar = tuple(int(c) for c in colour.split(","))
    ksplash = os.path.join(HERE, "ksplash", name)
    tdm = os.path.join(HERE, "tdm", name)
    os.makedirs(ksplash, exist_ok=True)
    os.makedirs(tdm, exist_ok=True)

    # KSplash: the middle of the wallpaper, then the icon bars.
    wp = Image.open(wallpaper).convert("RGB").resize((800, 500), Image.LANCZOS)
    top = wp.crop((200, 126, 600, 374))
    top.save(os.path.join(ksplash, "splash_top.png"))
    bars = {}
    for part in ("splash_active_bar", "splash_inactive_bar", "splash_bottom"):
        bars[part] = rebase(os.path.join(REF_KSPLASH, part + ".png"), bar)
        bars[part].save(os.path.join(ksplash, part + ".png"))

    preview = Image.new("RGB", (400, 331))
    preview.paste(top, (0, 0))
    preview.paste(bars["splash_active_bar"], (0, 248))
    preview.paste(bars["splash_bottom"], (0, 312))
    ImageDraw.Draw(preview).text((6, 232), "TDE is ready", font=font(11, True), fill="white")
    preview.save(os.path.join(ksplash, "Preview.png"))

    # TDM: the box and icons do not depend on the theme; draw a mock screenshot.
    for part in ("boundingbox.png", "icon-session.png", "icon-reboot.png"):
        shutil.copy(os.path.join(REF_TDM, part), os.path.join(tdm, part))
    shot = Image.open(login).convert("RGB").resize((480, 300), Image.LANCZOS).crop((40, 0, 440, 300))
    box = Image.open(os.path.join(REF_TDM, "boundingbox.png")).convert("RGBA")
    box = box.resize((130, 92), Image.LANCZOS)
    shot.paste(box, (135, 104), box)
    draw = ImageDraw.Draw(shot)
    draw.text((200, 121), "Welcome to debian", font=font(10), fill="white", anchor="mm")
    for label, y in (("Username:", 146), ("Password:", 159)):
        draw.text((191, y), label, font=font(6), fill="white", anchor="rm")
        draw.rectangle((193, y - 5, 251, y + 4), fill="white")
    small = font(7)
    draw.text((24, 291), "Session Type", font=small, fill="white", anchor="lm")
    draw.text((84, 291), "Menu", font=small, fill="white", anchor="lm")
    draw.text((392, 291), "Sat 10 June 09:58", font=small, fill="white", anchor="rm")
    for icon, x in (("icon-session.png", 6), ("icon-reboot.png", 70)):
        im = Image.open(os.path.join(REF_TDM, icon)).convert("RGBA").resize((11, 11), Image.LANCZOS)
        shot.paste(im, (x, 286), im)
    shot.save(os.path.join(tdm, "screenshot.png"))


if __name__ == "__main__":
    main()
