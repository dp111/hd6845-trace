#!/usr/bin/env python3
"""Follow horizontal poly lines by colour in the clean stripped shot.

usage: cdp2_lines.py x0 x1 y [y ...] [--half N] [--mingap G]
For each y (centre of a line) prints the x ranges where poly colour is present in the
band y-half..y+half (poly: R-G > 30 and G-B > 12, in the open or under metal; tan
diffusion, pink and khaki field and dark outlines fail the test). Gaps shorter than
--mingap are bridged (outlines of metal edges cut every line). A measurement aid: check
each reported end by eye.
"""
import sys, os, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view
ap = argparse.ArgumentParser()
ap.add_argument('x0', type=int); ap.add_argument('x1', type=int)
ap.add_argument('ys', type=int, nargs='+')
ap.add_argument('--half', type=int, default=4)
ap.add_argument('--mingap', type=int, default=14)
ap.add_argument('--frac', type=float, default=0.6)
a = ap.parse_args()
for y in a.ys:
    im = view.raw('acid1b', a.x0, y - a.half, a.x1 - a.x0, 2 * a.half + 1).astype(np.int32)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    poly = ((r - g) > 30) & ((g - b) > 12)
    col = poly.mean(axis=0) >= a.frac
    runs = []
    start = None
    for i, v in enumerate(col):
        if v and start is None:
            start = i
        if not v and start is not None:
            runs.append([start + a.x0, i - 1 + a.x0]); start = None
    if start is not None:
        runs.append([start + a.x0, a.x1 - 1])
    merged = []
    for s in runs:
        if merged and s[0] - merged[-1][1] <= a.mingap:
            merged[-1][1] = s[1]
        else:
            merged.append(s)
    merged = [m for m in merged if m[1] - m[0] >= 12]
    print(y, ' '.join(f'{m[0]}-{m[1]}' for m in merged))
