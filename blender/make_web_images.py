"""Convert the Blender renders into responsive WebP assets for the site.

Run:
  python3 blender/make_web_images.py
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RENDERS = os.path.join(ROOT, "blender", "renders")
IMAGES = os.path.join(ROOT, "assets", "img")
ROOMS = ("oak-and-light", "quiet-quarters", "warm-kitchen", "reading-nook", "dining-corner")


def save_webp(img, path, quality=82):
    img.save(path, "WEBP", quality=quality, method=6)
    print("Wrote", os.path.relpath(path, ROOT), os.path.getsize(path), "bytes")


for name in ROOMS:
    src = Image.open(os.path.join(RENDERS, name + ".png")).convert("RGB")
    for width in (1280, 800):
        height = round(src.height * width / src.width)
        img = src if width == src.width else src.resize((width, height), Image.LANCZOS)
        save_webp(img, os.path.join(IMAGES, f"{name}-{width}.webp"))

    crop = (src.width - round(src.width * 630 / src.height)) // 2
    og = src.crop((crop, 0, src.width - crop, src.height)).resize((1200, 630), Image.LANCZOS)
    save_webp(og, os.path.join(IMAGES, f"{name}-og.webp"))
