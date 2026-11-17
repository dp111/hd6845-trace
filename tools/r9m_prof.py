#!/usr/bin/env python3
"""Colour profile along a row or column in the chip-2 metal, chip-2 stripped and clean shots.

usage: r9m_prof.py col X Y0 Y1 [STEP] [--r R]     (also: row Y X0 X1 [STEP])
Prints R/G/B means of a (2R+1)^2 patch per step, and R-G for the two stripped shots
(poly and diffusion read redder than field there; see tools/classmap.py --open).
A variant of tools/larr_px.py that needs only the three shots this clone has cached.
"""
import os, sys
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = {'metal': 'metal.npy', 'acid': 'acid_aligned.npy', 'acid1b': 'acid1b.npy'}
A = {k: np.load(os.path.join(ROOT, 'cache', v), mmap_mode='r') for k, v in F.items()}
args = sys.argv[1:]
r = 1
if '--r' in args:
    i = args.index('--r'); r = int(args[i + 1]); del args[i:i + 2]
mode, fixed, a, b = args[0], int(args[1]), int(args[2]), int(args[3])
st = int(args[4]) if len(args) > 4 else 3
print('%11s  %-11s  %-11s  %-11s  rg_acid rg_1b' % ('', 'metal', 'acid', 'acid1b'))
for v in range(a, b + 1, st):
    x, y = (fixed, v) if mode == 'col' else (v, fixed)
    m = {k: A[k][y - r:y + r + 1, x - r:x + r + 1].reshape(-1, 3).astype(float).mean(0) for k in A}
    print('%5d,%5d  %s  %5d %5d' % (x, y, '  '.join('%3d/%3d/%3d' % tuple(m[k]) for k in F),
                                    m['acid'][0] - m['acid'][1], m['acid1b'][0] - m['acid1b'][1]))
