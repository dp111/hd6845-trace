#!/usr/bin/env python3
"""Check drawn metal against the metal shots: for each M item of the named trace files,
the fraction of its area that reads as metal (red > 177 and green > 128 in either chip's
metal shot, the test of tools/follow.py, on a 3x3-blurred image), sampled on a 4 px grid.
Lists the items under --min (default 0.55). Contact rings and poly crossings darken a
real line locally, so a short item can read low and still be right: look at those.

usage: bust_mcheck.py FILE [FILE ...] [--min 0.55]
"""
import os, sys
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tracelib
from shapely.geometry import Point
ROOT = tracelib.ROOT
A = [np.load(os.path.join(ROOT, 'cache', f), mmap_mode='r') for f in ('metal.npy', 'metal1.npy')]
args = sys.argv[1:]
mn = 0.55
if '--min' in args:
    i = args.index('--min'); mn = float(args[i + 1]); del args[i:i + 2]
os.environ['TRACE'] = ','.join(args)
t = tracelib.Trace()
bad = 0; n = 0
for it in t.items:
    src = getattr(it, 'src', '')
    if it.layer != 'M' or not any(('trace/%s.txt' % f) in src.split(' <- ')[0] for f in args):
        continue
    x0, y0, x1, y1 = [int(v) for v in it.geom.bounds]
    g = it.geom.buffer(-3)
    if g.is_empty:
        g = it.geom
    pts = [(x, y) for x in range(x0, x1 + 1, 4) for y in range(y0, y1 + 1, 4) if g.contains(Point(x, y))]
    if not pts:
        continue
    ok = 0
    for (x, y) in pts:
        m = False
        for a in A:
            p = a[y - 1:y + 2, x - 1:x + 2].reshape(-1, 3).astype(int).mean(0)
            if p[0] > 177 and p[1] > 128:
                m = True; break
        ok += m
    f = ok / len(pts); n += 1
    if f < mn:
        bad += 1
        print('%.2f  %s  [%d,%d %d,%d]  %d pts' % (f, src, x0, y0, x1, y1, len(pts)))
print('%d metal items checked, %d under %.2f' % (n, bad, mn))
