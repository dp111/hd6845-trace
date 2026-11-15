#!/usr/bin/env python3
"""A tall, narrow region as consecutive strips side by side (for long wiring channels).

usage: strips.py x y w h --n N [--scale S] [--layer L] [--grid G] [--trace] [--horizontal]
                 --out FILE

The region (x, y, w, h) is cut into N strips of equal height (or, with --horizontal, a
wide low region into N strips of equal width, stacked top to bottom) and the strips are
laid out left to right in reading order. Each strip keeps its own coordinate grid, and
neighbouring strips overlap by 20 px so that nothing is lost in the cut.
"""
import argparse
import os
import sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('x', type=int)
    ap.add_argument('y', type=int)
    ap.add_argument('w', type=int)
    ap.add_argument('h', type=int)
    ap.add_argument('--n', type=int, default=2)
    ap.add_argument('--scale', type=float, default=1.0)
    ap.add_argument('--layer', default='metal')
    ap.add_argument('--grid', type=int, default=100)
    ap.add_argument('--trace', action='store_true')
    ap.add_argument('--horizontal', action='store_true')
    ap.add_argument('--out', default='strips.png')
    a = ap.parse_args()
    ov = 20
    panels = []
    for i in range(a.n):
        if a.horizontal:
            step = a.w / a.n
            px, pw = int(a.x + i * step), int(step) + ov
            panels.append(view.panel(a.layer, px, a.y, pw, a.h, a.scale, a.grid, a.trace, None, False))
        else:
            step = a.h / a.n
            py, ph = int(a.y + i * step), int(step) + ov
            panels.append(view.panel(a.layer, a.x, py, a.w, ph, a.scale, a.grid, a.trace, None, False))
    gap = 6
    if a.horizontal:
        W = max(p.size[0] for p in panels)
        H = sum(p.size[1] for p in panels) + gap * (len(panels) - 1)
        out = Image.new('RGB', (W, H), (255, 0, 255))
        y = 0
        for p in panels:
            out.paste(p, (0, y))
            y += p.size[1] + gap
    else:
        W = sum(p.size[0] for p in panels) + gap * (len(panels) - 1)
        H = max(p.size[1] for p in panels)
        out = Image.new('RGB', (W, H), (255, 0, 255))
        x = 0
        for p in panels:
            out.paste(p, (x, 0))
            x += p.size[0] + gap
    path = view.scratch_path(a.out)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    out.save(path)
    print(path, out.size)


if __name__ == '__main__':
    main()
