#!/usr/bin/env python3
"""Runs of metal-looking (or poly-looking) pixels along scan lines (cdp3 helper).

usage: cdp3_prof.py h Y X0 X1 [Y ...]  [--band 6] [--mode metal|poly|dark] [--thr T] [--layer L]
       cdp3_prof.py v X Y0 Y1 [X ...]  ...
  h: scan along x at each given y (list of y values after X0 X1: "h X0 X1 y1 y2 ...")
  v: scan along y at each given x ("v Y0 Y1 x1 x2 ...")
  metal: min(R,G) of the metal shot >= thr (default 150): bright yellow metal
  poly:  orange metric of the chip-2 stripped shot (r-g > 12, g-b > 20) >= thr (0.5)
  dark:  brightness (max RGB) <= thr (default 70): outlines
The value is averaged over +-band pixels across the scan direction.
Prints start-end(mean) of every run at least --min long.
"""
import argparse, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view

ap = argparse.ArgumentParser()
ap.add_argument('dir', choices=['h', 'v'])
ap.add_argument('a0', type=int)
ap.add_argument('a1', type=int)
ap.add_argument('pos', type=int, nargs='+')
ap.add_argument('--band', type=int, default=6)
ap.add_argument('--mode', default='metal')
ap.add_argument('--thr', type=float, default=None)
ap.add_argument('--layer', default=None)
ap.add_argument('--min', type=int, default=5)
a = ap.parse_args()

layer = a.layer or {'metal': 'metal', 'poly': 'acid', 'dark': 'metal'}[a.mode]
thr = a.thr if a.thr is not None else {'metal': 150, 'poly': 0.5, 'dark': 70}[a.mode]


def metric(im):
    im = im.astype(np.float32)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    if a.mode == 'metal':
        return np.minimum(r, g)
    if a.mode == 'poly':
        return np.clip(((r - g) - 12) / 30.0, 0, 1) * np.clip((g - b - 20) / 30.0, 0, 1) * 4
    return -im.max(axis=2)


for p in a.pos:
    if a.dir == 'h':
        im = view.raw(layer, a.a0, p - a.band, a.a1 - a.a0, 2 * a.band + 1)
        prof = metric(im).mean(axis=0)
    else:
        im = view.raw(layer, p - a.band, a.a0, 2 * a.band + 1, a.a1 - a.a0)
        prof = metric(im).mean(axis=1)
    t = -thr if a.mode == 'dark' else thr
    runs = []
    s = None
    for i, v in enumerate(prof):
        if v >= t and s is None:
            s = i
        if v < t and s is not None:
            if i - s >= a.min:
                runs.append((a.a0 + s, a.a0 + i - 1, abs(prof[s:i].mean())))
            s = None
    if s is not None and len(prof) - s >= a.min:
        runs.append((a.a0 + s, a.a1 - 1, abs(prof[s:].mean())))
    print(('y' if a.dir == 'h' else 'x') + str(p) + ':', ' '.join(f'{p0}-{p1}({m:.0f})' if a.mode != 'poly' else f'{p0}-{p1}' for p0, p1, m in runs))
