#!/usr/bin/env python3
"""Mean brightness (R+G+B)/3 across a metal track, in both chips' metal shots.

usage: r9m_bright.py col X Y0 Y1 [--half H]   (or: row Y X0 X1)
Averages a strip 2H+1 px wide across the track at each step of 1 px. A break between two
metal pieces is dark in BOTH shots over its whole length; an edge of something underneath
printing through is a short dip, often in one shot more than the other.
"""
import os, sys
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = {k: np.load(os.path.join(ROOT, 'cache', k + '.npy'), mmap_mode='r') for k in ('metal', 'metal1')}
a = sys.argv[1:]
h = 3
if '--half' in a:
    i = a.index('--half'); h = int(a[i + 1]); del a[i:i + 2]
mode, f, s0, s1 = a[0], int(a[1]), int(a[2]), int(a[3])
for v in range(s0, s1 + 1):
    if mode == 'col':
        vals = [A[k][v, f - h:f + h + 1].astype(float).mean() for k in A]
    else:
        vals = [A[k][f - h:f + h + 1, v].astype(float).mean() for k in A]
    print('%5d  %5.0f %5.0f  %s' % (v, vals[0], vals[1], '#' * int(min(vals) / 6)))
