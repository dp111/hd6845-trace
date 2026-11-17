#!/usr/bin/env python3
"""Mean cross-profile of a vertical line over a y range, per slice and per shot.

usage: rde_edge.py XC Y0 Y1 [HALF] [--dx 0,390,...]
Prints (R+G)/2 averaged over y Y0..Y1 for each x from XC-HALF to XC+HALF (one row per
shot and slice). A metal edge is a dark dip; if the dip is there in the metal shots and
the stripped shots are flat at the same x, the dip is the metal's own edge.
"""
import sys, os, numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = [a for a in sys.argv[1:] if not a.startswith('--')]
xc, y0, y1 = int(args[0]), int(args[1]), int(args[2])
half = int(args[3]) if len(args) > 3 else 16
dxs = [0, 390, 780, 1170, 1560]
for i, a in enumerate(sys.argv):
    if a == '--dx':
        dxs = [int(v) for v in sys.argv[i + 1].split(',')]
print('x-xc:      ' + ' '.join('%3d' % d for d in range(-half, half + 1, 2)))
for lay in ('metal', 'metal1', 'acid1b', 'acid_aligned'):
    a = np.load(os.path.join(ROOT, 'cache', lay + '.npy'), mmap_mode='r')
    for dx in dxs:
        s = a[y0:y1, xc + dx - half:xc + dx + half + 1, :2].astype(float).mean(axis=(0, 2))
        print('%-7s %5d ' % (lay[:7], xc + dx) + ' '.join('%3d' % v for v in s[::2]))
