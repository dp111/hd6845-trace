#!/usr/bin/env python3
"""Several layers of one region side by side, the last with the trace outlined on it.

usage: quad.py x y w h [--scale S] [--grid N] [--out FILE] [--layers a,b[,c,d]] [--notrace]
               [--traceall] [--comp NAME] [--shift dx,dy]

Default panels: metal | acid1b + trace outlines. An image costs context in proportion
to its area, so two panels are the default; ask for four (in a 2 x 2 block) with
--layers metal,acid,acid1b,acid1b only when the extra shots are needed. Three layers
go side by side in one row (keep w*scale under 430 then). Keep w*scale under about
640 for two panels so the result stays under 1400 px wide.
"""
import argparse
import os
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view

LABEL = {'metal': 'metal (chip 2)', 'acid': 'stripped (chip 2)', 'acid1b': 'clean (chip 1)', 'edges': 'edges',
         'metal1': 'metal (chip 1)', 'acid1': 'stripped (chip 1)', 'edges': 'edges'}


def quad(x, y, w, h, scale=1.7, grid=50, layers=('metal', 'acid1b'), trace=True, traceall=False):
    ims = []
    for i, l in enumerate(layers):
        tr = trace and (traceall or i == len(layers) - 1)
        im = view.panel(l, x, y, w, h, scale, grid, trace=tr, fill=False)
        d = ImageDraw.Draw(im)
        d.text((48, 16), LABEL.get(l, l) + (' + trace' if tr else ''), fill=(255, 255, 0),
               font=view.font(14), stroke_width=3, stroke_fill=(0, 0, 0))
        ims.append(im)
    W, H = ims[0].size
    cols = len(ims) if len(ims) <= 3 else 2          # up to three in one row, four as 2 x 2
    rows = (len(ims) + cols - 1) // cols
    o = Image.new('RGB', (W * cols + 6 * (cols - 1), H * rows + 6 * (rows - 1)), (255, 0, 255))
    for i, im in enumerate(ims):
        o.paste(im, ((i % cols) * (W + 6), (i // cols) * (H + 6)))
    return o


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('x', type=int)
    ap.add_argument('y', type=int)
    ap.add_argument('w', type=int)
    ap.add_argument('h', type=int)
    ap.add_argument('--scale', type=float, default=1.7)
    ap.add_argument('--grid', type=int, default=50)
    ap.add_argument('--layers', default='metal,acid1b')
    ap.add_argument('--notrace', action='store_true')
    ap.add_argument('--traceall', action='store_true', help='outline the trace on every panel, not only the last')
    ap.add_argument('--out', default='quad.png')
    ap.add_argument('--comp', default=None, help='use this median composite where it has the layer')
    ap.add_argument('--shift', default=None, help='dx,dy: look at another instance in the master frame')
    a = ap.parse_args()
    a.out = view.scratch_path(a.out)
    if a.comp:
        view.use_comp(a.comp)
    if a.shift:
        view._shift = tuple(int(v) for v in a.shift.split(','))
    o = quad(a.x, a.y, a.w, a.h, a.scale, a.grid, a.layers.split(','), not a.notrace, a.traceall)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    o.save(a.out)
    print(a.out, o.size)


if __name__ == '__main__':
    main()
