#!/usr/bin/env python3
"""A long horizontal strip of the die cut into pieces and stacked, to follow a through line.

usage: cdp3_strips.py X0 X1 Y H N [--scale S] [--layer L] [--grid G] [--trace] --out NAME
Cuts x X0..X1 into N equal pieces of height H starting at y Y and stacks them top to bottom
(west piece on top). Run through tools/t.sh so that the trace and scratch folder are set.
"""
import argparse, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view
ap = argparse.ArgumentParser()
ap.add_argument('x0', type=int); ap.add_argument('x1', type=int)
ap.add_argument('y', type=int); ap.add_argument('h', type=int); ap.add_argument('n', type=int)
ap.add_argument('--scale', type=float, default=1.4)
ap.add_argument('--layer', default='acid1b')
ap.add_argument('--grid', type=int, default=50)
ap.add_argument('--trace', action='store_true')
ap.add_argument('--out', required=True)
a = ap.parse_args()
w = (a.x1 - a.x0) // a.n
ims = [view.panel(a.layer, a.x0 + i * w, a.y, w, a.h, a.scale, a.grid, trace=a.trace, fill=False) for i in range(a.n)]
W, H = ims[0].size
o = Image.new('RGB', (W, (H + 4) * a.n), (255, 0, 255))
for i, im in enumerate(ims):
    o.paste(im, (0, i * (H + 4)))
out = view.scratch_path(a.out)
o.save(out)
print(out, o.size)
