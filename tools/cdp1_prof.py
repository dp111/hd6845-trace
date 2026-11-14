#!/usr/bin/env python3
"""Print, for each y step, the x-runs of 'metal-looking' pixels in a window (cdp1 helper).
usage: cdp1_prof.py x0 x1 y0 y1 [--offsets "..."] [--layer metal] [--step 4] [--thr 150]
Uses the median over instances (integer offsets) of the brightness (min of R,G).
"""
import argparse, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view
ap = argparse.ArgumentParser()
ap.add_argument('x0', type=int); ap.add_argument('x1', type=int)
ap.add_argument('y0', type=int); ap.add_argument('y1', type=int)
ap.add_argument('--offsets', default='0,0')
ap.add_argument('--layer', default='metal')
ap.add_argument('--step', type=int, default=4)
ap.add_argument('--thr', type=float, default=150)
a = ap.parse_args()
offs = [tuple(int(v) for v in o.split(',')) for o in a.offsets.split()]
st = np.stack([view.raw(a.layer, a.x0 + dx, a.y0 + dy, a.x1 - a.x0, a.y1 - a.y0).astype(np.float32) for dx, dy in offs])
m = np.median(st, axis=0)
b = np.minimum(m[..., 0], m[..., 1])
for y in range(0, b.shape[0], a.step):
    row = b[y:y + a.step].mean(axis=0)
    runs = []
    s = None
    for x, v in enumerate(row):
        if v >= a.thr and s is None:
            s = x
        if v < a.thr and s is not None:
            if x - s >= 4:
                runs.append((a.x0 + s, a.x0 + x - 1, int(row[s:x].mean())))
            s = None
    if s is not None:
        runs.append((a.x0 + s, a.x1 - 1, int(row[s:].mean())))
    print(a.y0 + y, ' '.join(f'{p}-{q}({w})' for p, q, w in runs))
