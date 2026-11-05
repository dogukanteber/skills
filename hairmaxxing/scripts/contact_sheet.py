#!/usr/bin/env python3
"""Combine renders into one labeled comparison sheet.

Example:
  python3 contact_sheet.py sheets/round1-top.jpg renders/r001.png renders/r002.png \
      renders/r003.png renders/r004.png --labels "1 Quiff,2 Crop,3 Flow,4 Curtains"
"""
import argparse
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def load_font(size):
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("out", help="output image path")
    p.add_argument("images", nargs="+", help="images to place, in order")
    p.add_argument("--labels", help="comma-separated labels; defaults to file names")
    p.add_argument("--cols", type=int, help="columns; defaults to 2 for 4 images, else up to 3")
    p.add_argument("--height", type=int, default=640, help="cell image height in px (default 640)")
    args = p.parse_args()

    paths = [Path(i) for i in args.images]
    missing = [str(x) for x in paths if not x.exists()]
    if missing:
        sys.exit(f"missing images: {', '.join(missing)}")

    labels = [s.strip() for s in args.labels.split(",")] if args.labels else [x.stem for x in paths]
    if len(labels) != len(paths):
        sys.exit(f"got {len(labels)} labels for {len(paths)} images")

    n = len(paths)
    cols = args.cols or (2 if n == 4 else min(n, 3))
    rows = math.ceil(n / cols)

    ims = []
    for x in paths:
        im = Image.open(x).convert("RGB")
        w = round(im.width * args.height / im.height)
        ims.append(im.resize((w, args.height), Image.LANCZOS))
    cell_w = max(im.width for im in ims)

    bar = max(36, args.height // 14)
    pad = 12
    font = load_font(int(bar * 0.6))
    sheet = Image.new("RGB", (cols * cell_w + (cols + 1) * pad, rows * (args.height + bar) + (rows + 1) * pad), "white")
    draw = ImageDraw.Draw(sheet)

    for i, (im, label) in enumerate(zip(ims, labels)):
        r, c = divmod(i, cols)
        x0 = pad + c * (cell_w + pad)
        y0 = pad + r * (args.height + bar + pad)
        sheet.paste(im, (x0 + (cell_w - im.width) // 2, y0))
        draw.rectangle([x0, y0 + args.height, x0 + cell_w, y0 + args.height + bar], fill=(25, 25, 25))
        tw = draw.textlength(label, font=font)
        draw.text((x0 + (cell_w - tw) / 2, y0 + args.height + bar * 0.18), label, fill="white", font=font)

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.out, quality=92)
    print(f"wrote {args.out} ({n} images, {cols}x{rows})")


if __name__ == "__main__":
    main()
