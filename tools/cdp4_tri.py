#!/usr/bin/env python3
"""Panels of one region in a single row, one per layer (cdp4 helper; quad.py makes a 2 x 2 block).

usage: cdp4_tri.py x y w h [--scale S] [--grid N] [--layers a,b,c] [--trace LIST] [--comp NAME]
                   [--shift dx,dy] --out FILE
--trace LIST: indices (0-based, comma separated) of the panels that get the trace outlined.
"""
import argparse, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view
ap = argparse.ArgumentParser()
ap.add_argument('x', type=int); ap.add_argument('y', type=int)
ap.add_argument('w', type=int); ap.add_argument('h', type=int)
ap.add_argument('--scale', type=float, default=2.0)
ap.add_argument('--grid', type=int, default=50)
ap.add_argument('--layers', default='metal,acid,acid1b')
ap.add_argument('--trace', default='')
ap.add_argument('--comp', default=None)
ap.add_argument('--shift', default=None)
ap.add_argument('--out', required=True)
a = ap.parse_args()
a.out = view.scratch_path(a.out)
if a.comp:
    view.use_comp(a.comp)
if a.shift:
    view._shift = tuple(int(v) for v in a.shift.split(','))
tr = set(int(v) for v in a.trace.split(',') if v != '')
ims = []
for i, l in enumerate(a.layers.split(',')):
    im = view.panel(l, a.x, a.y, a.w, a.h, a.scale, a.grid, trace=(i in tr), fill=False)
    ImageDraw.Draw(im).text((48, 16), l + (' + trace' if i in tr else ''), fill=(255, 255, 0),
                            font=view.font(14), stroke_width=3, stroke_fill=(0, 0, 0))
    ims.append(im)
W, H = ims[0].size
o = Image.new('RGB', (W * len(ims) + 6 * (len(ims) - 1), H), (255, 0, 255))
for i, im in enumerate(ims):
    o.paste(im, (i * (W + 6), 0))
os.makedirs(os.path.dirname(a.out), exist_ok=True)
o.save(a.out)
print(a.out, o.size)
