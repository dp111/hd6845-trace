#!/usr/bin/env python3
"""Text cross-sections of a vertical line: brightness across x at each y, as digits.

usage: rde_xs.py LAYER XC Y0 Y1 [STEP] [HALF]
Each row is one y (mean over STEP rows); each character is one x pixel from XC-HALF to
XC+HALF; digit = (R+G)/2 scaled 0-9 (9 bright). Lets the two dark edge lines of a thin
metal be followed through a stretch where the metal itself is dim.
"""
import sys, numpy as np, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lay, xc, y0, y1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
step = int(sys.argv[5]) if len(sys.argv) > 5 else 4
half = int(sys.argv[6]) if len(sys.argv) > 6 else 22
a = np.load(os.path.join(ROOT, 'cache', lay + '.npy'), mmap_mode='r')
print('x %d..%d (centre column marked |)' % (xc - half, xc + half))
for y in range(y0, y1, step):
    s = a[y:y + step, xc - half:xc + half + 1, :2].astype(float).mean(axis=(0, 2))
    d = np.clip((s - 40) / 18, 0, 9).astype(int)
    row = ''.join(str(v) for v in d)
    print('%5d %s|%s  c=%3d' % (y, row[:half], row[half:], s[half - 3:half + 4].mean()))
