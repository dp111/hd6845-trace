#!/usr/bin/env python3
"""Fused view of a composite: a stripped layer with the outline of the metal drawn on it.

usage: larr_fuse.py COMP x y w h [--scale S] [--base acid|acid1b] [--grid N] [--out FILE]
                    [--thr G] [--trace]

The metal mask is taken from the metal composite (metal is the only thing there with a
bright green channel), cleaned up a little, and its outline is drawn in blue on the base
layer. It is a reading aid only: edges of poly and diffusion under the metal cut the
mask into pieces, so never take connectivity of metal from it; check in the metal shot.
--trace also outlines the trace geometry (master coordinates).
"""
import argparse
import json
import os
import sys
import numpy as np
import cv2
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('comp')
    ap.add_argument('x', type=int)
    ap.add_argument('y', type=int)
    ap.add_argument('w', type=int)
    ap.add_argument('h', type=int)
    ap.add_argument('--scale', type=float, default=3)
    ap.add_argument('--base', default='acid')
    ap.add_argument('--grid', type=int, default=50)
    ap.add_argument('--thr', type=float, default=156)
    ap.add_argument('--out', default='fuse.png')
    ap.add_argument('--trace', action='store_true')
    ap.add_argument('--only', default=None)
    a = ap.parse_args()
    d = os.path.join(ROOT, 'cache', 'comp')
    j = json.load(open(os.path.join(d, a.comp + '.json')))
    x0, y0 = j['x0'], j['y0']
    met = np.load(os.path.join(d, f'{a.comp}_metal.npy'))
    base = np.load(os.path.join(d, f'{a.comp}_{a.base}.npy'))
    sl = (slice(a.y - y0, a.y - y0 + a.h), slice(a.x - x0, a.x - x0 + a.w))
    m = met[sl].astype(np.float32)
    b = base[sl]
    g = cv2.GaussianBlur(m[:, :, 1], (0, 0), 1.5)
    mask = (g > a.thr).astype(np.uint8)
    S = a.scale
    W, H = int(a.w * S), int(a.h * S)
    big = cv2.resize(b, (W, H), interpolation=cv2.INTER_CUBIC)
    mb = cv2.resize(mask, (W, H), interpolation=cv2.INTER_NEAREST)
    mb = cv2.morphologyEx(mb, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    cs, _ = cv2.findContours(mb, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    big = np.ascontiguousarray(big)
    cv2.drawContours(big, cs, -1, (40, 90, 255), 2)
    im = Image.fromarray(big)
    dr = ImageDraw.Draw(im)
    if a.trace:
        import tracelib
        tr = tracelib.Trace()
        only = a.only.split(',') if a.only else None
        for it in tr.items:
            if only and it.layer not in only:
                continue
            gx0, gy0, gx1, gy1 = it.geom.bounds
            if gx1 < a.x or gx0 > a.x + a.w or gy1 < a.y or gy0 > a.y + a.h:
                continue
            col = tracelib.COLOURS[it.layer]
            if it.uncertain:
                col = (255, 255, 0)
            polys = [it.geom] if it.geom.geom_type == 'Polygon' else list(it.geom.geoms)
            for p in polys:
                pts = [((px - a.x) * S, (py - a.y) * S) for px, py in p.exterior.coords]
                dr.line(pts, fill=col, width=2)
    if a.grid:
        f = view.font(12)
        gx = (a.x // a.grid + 1) * a.grid
        while gx < a.x + a.w:
            X = (gx - a.x) * S
            dr.line([(X, 0), (X, H)], fill=(0, 255, 255), width=1)
            dr.text((X + 2, 2), str(gx), fill=(255, 255, 0), font=f, stroke_width=2, stroke_fill=(0, 0, 0))
            gx += a.grid
        gy = (a.y // a.grid + 1) * a.grid
        while gy < a.y + a.h:
            Y = (gy - a.y) * S
            dr.line([(0, Y), (W, Y)], fill=(0, 255, 255), width=1)
            dr.text((2, Y + 2), str(gy), fill=(255, 255, 0), font=f, stroke_width=2, stroke_fill=(0, 0, 0))
            gy += a.grid
    out = view.scratch_path(a.out)
    im.save(out)
    print(out, im.size)


if __name__ == '__main__':
    main()
