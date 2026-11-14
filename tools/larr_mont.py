#!/usr/bin/env python3
"""Montage of several die crops in one picture (to compare instances cheaply).

usage: larr_mont.py --scale S --grid N --cols C --out FILE  layer:x,y,w,h [layer:x,y,w,h ...]
Each crop is rendered with view.panel (same grid labels as view.py) and tiled C per row.
"""
import argparse, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view
ap = argparse.ArgumentParser()
ap.add_argument('--scale', type=float, default=1.5); ap.add_argument('--grid', type=int, default=50)
ap.add_argument('--cols', type=int, default=2); ap.add_argument('--out', default='mont.png')
ap.add_argument('--trace', action='store_true')
ap.add_argument('crops', nargs='+')
a = ap.parse_args()
ims = []
for c in a.crops:
    l, r = c.split(':'); x, y, w, h = map(int, r.split(','))
    ims.append(view.panel(l, x, y, w, h, a.scale, a.grid, trace=a.trace, fill=False))
W = max(i.size[0] for i in ims); H = max(i.size[1] for i in ims)
rows = (len(ims) + a.cols - 1) // a.cols
o = Image.new('RGB', (a.cols * (W + 6), rows * (H + 6)), (255, 0, 255))
for k, i in enumerate(ims):
    o.paste(i, ((k % a.cols) * (W + 6), (k // a.cols) * (H + 6)))
p = view.scratch_path(a.out); o.save(p); print(p, o.size)
