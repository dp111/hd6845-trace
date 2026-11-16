#!/usr/bin/env python3
"""The same horizontal strip at several y positions, stacked (to follow one line per array row).

usage: rowstrips.py x w h --ys y1,y2,... [--scale S] [--layer L] [--grid G] [--trace] --out FILE

Each strip is x..x+w wide and h tall, centred on one of the given y values; strips are stacked
top to bottom in the order given, each with its own grid. Use it for the same wire in every row
of an array (the output line of each counter bit, say): one image instead of one per row.
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
    ap.add_argument('w', type=int)
    ap.add_argument('h', type=int)
    ap.add_argument('--ys', required=True)
    ap.add_argument('--scale', type=float, default=1.0)
    ap.add_argument('--layer', default='acid1b')
    ap.add_argument('--grid', type=int, default=50)
    ap.add_argument('--trace', action='store_true')
    ap.add_argument('--out', default='rowstrips.png')
    a = ap.parse_args()
    panels = [view.panel(a.layer, a.x, int(y) - a.h // 2, a.w, a.h, a.scale, a.grid, a.trace, None, False)
              for y in a.ys.split(',')]
    gap = 5
    out = Image.new('RGB', (max(p.size[0] for p in panels), sum(p.size[1] for p in panels) + gap * (len(panels) - 1)),
                    (255, 0, 255))
    y = 0
    for p in panels:
        out.paste(p, (0, y))
        y += p.size[1] + gap
    path = view.scratch_path(a.out)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    out.save(path)
    print(path, out.size)


if __name__ == '__main__':
    main()
