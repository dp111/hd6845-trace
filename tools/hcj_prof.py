#!/usr/bin/env python3
"""Metal profile down a vertical line, both chips' metal shots (follow.py's metal test).

usage: hcj_prof.py X Y0 Y1 [--gapcol] [--min N]

Prints, per chip, the runs along y at column X (mean of 7 px across) that are NOT metal
and at least --min px long (default 8); with --gapcol the runs that ARE metal (to show
that nothing crosses a gap between two tracks). Used for the bundle tracks between rdp3
and bd1 (notes/blocks/hcj.md). It says where metal is, not what it connects.
"""
import argparse, os
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('x', type=int); ap.add_argument('y0', type=int); ap.add_argument('y1', type=int)
ap.add_argument('--gapcol', action='store_true'); ap.add_argument('--min', type=int, default=8)
ap.add_argument('--horizontal', action='store_true', help='X is a y; Y0 Y1 are x0 x1')
a = ap.parse_args()
for nm in ('metal', 'metal1'):
    im = np.load(os.path.join(ROOT, 'cache', nm + '.npy'), mmap_mode='r')
    if a.horizontal:
        s = im[a.x - 3:a.x + 4, a.y0:a.y1].astype(int).mean(0)
    else:
        s = im[a.y0:a.y1, a.x - 3:a.x + 4].astype(int).mean(1)
    m = (s[:, 0] > 170) & (s[:, 1] > 125)
    want = m if a.gapcol else ~m
    runs = []; st = None
    for i, v in enumerate(want):
        if v and st is None: st = i
        if not v and st is not None:
            if i - st >= a.min: runs.append((a.y0 + st, a.y0 + i - 1))
            st = None
    if st is not None and len(want) - st >= a.min: runs.append((a.y0 + st, a.y1 - 1))
    print(nm, 'x' if not a.horizontal else 'y', a.x, 'metal' if a.gapcol else 'not metal', ' '.join('%d-%d(%d)' % (p, q, q - p + 1) for p, q in runs))
