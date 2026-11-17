#!/usr/bin/env python3
"""Dim stretches along a vertical thin metal, per slice and shot.

usage: rde_dim.py XC Y0 Y1 [THR] [MINLEN] [--dx 0,390,...]
At each y takes the brightest 7 px window ((R+G)/2) within XC-6..XC+10 and lists the
stretches where it is below THR for at least MINLEN px. Poly/diffusion edges under the
metal give stretches of 4-9 px; anything longer is to be looked at.
"""
import sys, os, numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = [a for a in sys.argv[1:] if not a.startswith('--')]
xc, y0, y1 = int(args[0]), int(args[1]), int(args[2])
thr = int(args[3]) if len(args) > 3 else 115
minlen = int(args[4]) if len(args) > 4 else 3
dxs = [0, 390, 780, 1170, 1560]
if '--dx' in sys.argv:
    dxs = [int(v) for v in sys.argv[sys.argv.index('--dx') + 1].split(',')]
for lay in ('metal', 'metal1'):
    a = np.load(os.path.join(ROOT, 'cache', lay + '.npy'), mmap_mode='r')
    for dx in dxs:
        p = a[y0:y1, xc + dx - 9:xc + dx + 14, :2].astype(float).mean(axis=2)
        k = np.ones(7) / 7
        best = np.array([np.convolve(r, k, 'valid').max() for r in p])
        out, st = [], None
        for i, v in enumerate(best < thr):
            if v and st is None: st = i
            if not v and st is not None:
                if i - st >= minlen: out.append('%d-%d(%d)' % (y0 + st, y0 + i - 1, i - st))
                st = None
        if st is not None: out.append('%d-%d(%d)' % (y0 + st, y1 - 1, y1 - y0 - st))
        print('%-6s %5d  %s' % (lay, xc + dx, ' '.join(out)))
