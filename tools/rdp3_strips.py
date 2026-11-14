#!/usr/bin/env python3
"""Montage of vertical strips, for following per-slice vertical lines.

usage: tools/t.sh rdp3 rdp3_strips.py Y0 Y1 X1 X2 ... [--hw 60] [--scale 1.0]
       [--layer metal] [--grid 100] [--trace] --out FILE
Each strip is centred on one X and labelled with it; all share the y axis.
"""
import argparse, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view

ap = argparse.ArgumentParser()
ap.add_argument('y0', type=int); ap.add_argument('y1', type=int)
ap.add_argument('xs', type=int, nargs='+')
ap.add_argument('--hw', type=int, default=60)
ap.add_argument('--scale', type=float, default=1.0)
ap.add_argument('--layer', default='metal')
ap.add_argument('--grid', type=int, default=100)
ap.add_argument('--trace', action='store_true')
ap.add_argument('--out', default='strips.png')
a = ap.parse_args()
ps = []
for x in a.xs:
    im = view.panel(a.layer, x - a.hw, a.y0, 2 * a.hw, a.y1 - a.y0, a.scale, a.grid,
                    trace=a.trace, fill=False)
    ImageDraw.Draw(im).text((2, im.size[1] - 14), str(x), fill=(255, 255, 255),
                            font=view.font(11), stroke_width=2, stroke_fill=(0, 0, 0))
    ps.append(im)
W = sum(p.size[0] for p in ps) + 4 * (len(ps) - 1)
o = Image.new('RGB', (W, ps[0].size[1]), (255, 0, 255))
px = 0
for p in ps:
    o.paste(p, (px, 0)); px += p.size[0] + 4
out = view.scratch_path(a.out)
o.save(out); print(out, o.size)
