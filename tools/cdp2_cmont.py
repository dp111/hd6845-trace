#!/usr/bin/env python3
"""Montage of small windows, metal above acid1b, to compare where one feature (a contact)
sits in the two shots.  usage: cdp2_cmont.py [--comp NAME] [--half 30] [--scale 5] [--layers metal,acid1b] --out F x,y x,y ...
Each column is one point; a cross marks the given point in every panel; grid every 10 px."""
import argparse, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view, rdp3_sharp
ap = argparse.ArgumentParser()
ap.add_argument('pts', nargs='+'); ap.add_argument('--comp'); ap.add_argument('--half', type=int, default=30)
ap.add_argument('--scale', type=float, default=5); ap.add_argument('--layers', default='metal,acid1b')
ap.add_argument('--out', default='cmont.png')
a = ap.parse_args()
if a.comp:
    view.use_comp(a.comp)
h = a.half; s = a.scale; L = a.layers.split(',')
cols = []
for p in a.pts:
    x, y = (int(v) for v in p.split(','))
    ims = []
    for l in L:
        im = rdp3_sharp.sharp_panel(l, x - h, y - h, 2 * h, 2 * h, s, 10, False, 1.0, 2.5)
        d = ImageDraw.Draw(im); c = h * s
        d.line((c - 8, c, c + 8, c), fill=(255, 255, 255)); d.line((c, c - 8, c, c + 8), fill=(255, 255, 255))
        ims.append(im)
    cols.append(ims)
W, H = cols[0][0].size
o = Image.new('RGB', ((W + 4) * len(cols), (H + 4) * len(L)), (255, 0, 255))
for i, ims in enumerate(cols):
    for j, im in enumerate(ims):
        o.paste(im, (i * (W + 4), j * (H + 4)))
f = view.scratch_path(a.out); o.save(f); print(f, o.size)
