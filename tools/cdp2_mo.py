#!/usr/bin/env python3
"""A stripped shot with the outline of the metal drawn on it.

usage: cdp2_mo.py x y w h [--scale S] [--grid N] [--layers acid1b[,metal,...]]
                  [--comp NAME] [--shift dx,dy] [--trace] [--out FILE]

The metal is found in the metal shot by colour (bright, yellow) after a small blur,
and its outline is drawn in blue on every panel. What a feature looks like in acid1b
depends on whether metal was above it, and the edge of the metal itself prints as a
dark line, so knowing where the metal was removes most of the guessing. The mask is
a viewing aid only: it breaks up over contacts and where poly edges print through.
"""
import argparse
import os
import sys
import numpy as np
import cv2
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view


def metal_mask(x, y, w, h):
    pad = 8
    m = view.raw('metal', x - pad, y - pad, w + 2 * pad, h + 2 * pad).astype(np.float32)
    b = cv2.GaussianBlur(m, (0, 0), 2.0)
    r, g, bl = b[..., 0], b[..., 1], b[..., 2]
    mask = ((r > 186) & (g > 148)).astype(np.uint8)
    se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, se)
    return mask[pad:-pad, pad:-pad]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('x', type=int)
    ap.add_argument('y', type=int)
    ap.add_argument('w', type=int)
    ap.add_argument('h', type=int)
    ap.add_argument('--scale', type=float, default=3.0)
    ap.add_argument('--grid', type=int, default=25)
    ap.add_argument('--layers', default='acid1b')
    ap.add_argument('--comp', default=None)
    ap.add_argument('--shift', default=None)
    ap.add_argument('--trace', action='store_true')
    ap.add_argument('--out', default='mo.png')
    a = ap.parse_args()
    if a.comp:
        view.use_comp(a.comp)
    if a.shift:
        view._shift = tuple(int(v) for v in a.shift.split(','))
    mask = metal_mask(a.x, a.y, a.w, a.h)
    W, H = round(a.w * a.scale), round(a.h * a.scale)
    big = cv2.resize(mask, (W, H), interpolation=cv2.INTER_NEAREST)
    cs, _ = cv2.findContours(big, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    panels = []
    for l in a.layers.split(','):
        im = view.panel(l, a.x, a.y, a.w, a.h, a.scale, 0, trace=a.trace, fill=False)
        arr = np.array(im.convert('RGB'))
        cv2.drawContours(arr, cs, -1, (40, 90, 255), 1)
        im = Image.fromarray(arr)
        if a.grid:
            view.draw_grid(im, a.x, a.y, a.w, a.h, a.scale, a.grid)
        panels.append(im)
    out = Image.new('RGB', (sum(p.size[0] for p in panels) + 6 * (len(panels) - 1), H), (255, 0, 255))
    px = 0
    for p in panels:
        out.paste(p, (px, 0))
        px += p.size[0] + 6
    f = view.scratch_path(a.out)
    out.save(f)
    print(f, out.size)


if __name__ == '__main__':
    main()
