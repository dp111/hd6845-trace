#!/usr/bin/env python3
"""Colour profiles of the die, one line per sample, for settling what a strip is.

usage: tc1_px.py col X Y0 Y1 STEP [layers]     samples down a column
       tc1_px.py row Y X0 X1 STEP [layers]     samples along a row
       tc1_px.py pt X,Y [X,Y ...]              single points (5x5 mean)
layers: comma list from metal,metal1,acid,acid1b (default acid1b,metal)
Each sample is the mean of a 3x3 patch, printed as R G B per layer.
"""
import os, sys
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = {'metal': 'metal.npy', 'acid': 'acid_aligned.npy', 'metal1': 'metal1.npy', 'acid1b': 'acid1b.npy'}
def main():
    a = sys.argv[1:]
    mode = a[0]
    if mode == 'pt':
        pts = [tuple(map(int, t.split(','))) for t in a[1:] if ',' in t and t[0].isdigit()]
        rest = [t for t in a[1:] if not (',' in t and t[0].isdigit())]
        layers = rest[0].split(',') if rest else ['acid1b', 'metal']
        r = 2
    else:
        c, p0, p1, st = map(int, a[1:5])
        layers = a[5].split(',') if len(a) > 5 else ['acid1b', 'metal']
        pts = [(c, v) if mode == 'col' else (v, c) for v in range(p0, p1 + 1, st)]
        r = 1
    A = {l: np.load(os.path.join(ROOT, 'cache', F[l]), mmap_mode='r') for l in layers}
    print('     x     y  ' + '  '.join('%-11s' % l for l in layers))
    for x, y in pts:
        print('%6d %5d  ' % (x, y) + '  '.join('%3d %3d %3d' % tuple(A[l][y - r:y + r + 1, x - r:x + r + 1].reshape(-1, 3).mean(0)) for l in layers))
main()
