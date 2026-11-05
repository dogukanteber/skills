#!/usr/bin/env python3
"""Split a photo grid into one image per view.

Example (a 2x2 grid: front and right profile on top, left profile and top-down view below):
  python3 split_grid.py photos/grid.jpg --grid 2x2 --outdir photos --names front,right,left,top
"""
import argparse
import sys
from pathlib import Path

from PIL import Image


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("image")
    p.add_argument("--grid", default="2x2", help="COLSxROWS, default 2x2")
    p.add_argument("--outdir", required=True)
    p.add_argument("--names", help="comma-separated panel names, row by row")
    args = p.parse_args()

    if not Path(args.image).exists():
        sys.exit(f"no such image: {args.image}")
    try:
        cols, rows = (int(v) for v in args.grid.lower().split("x"))
    except ValueError:
        sys.exit(f"--grid must look like 2x2 or 3x1, got {args.grid!r}")
    names = args.names.split(",") if args.names else [f"panel{i + 1}" for i in range(cols * rows)]
    if len(names) != cols * rows:
        sys.exit(f"--names has {len(names)} entries for {cols * rows} panels")

    im = Image.open(args.image).convert("RGB")
    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    w, h = im.width // cols, im.height // rows
    for i, name in enumerate(names):
        r, c = divmod(i, cols)
        path = out / f"{name}.jpg"
        im.crop((c * w, r * h, (c + 1) * w, (r + 1) * h)).save(path, quality=95)
        print(f"wrote {path.resolve()}")


if __name__ == "__main__":
    main()
