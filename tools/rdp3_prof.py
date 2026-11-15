#!/usr/bin/env python3
"""Colour profile along a row or a column, one line per step, columns that line up.

usage: tools/t.sh rdp3 rdp3_prof.py COMP|- row Y X0 X1 STEP [--r 1] [--layers acid,acid1b]
       tools/t.sh rdp3 rdp3_prof.py COMP|- col X Y0 Y1 STEP [--shift dx,dy]
Prints R G B and R-G per layer. COMP is a composite name (cache/comp) or - for the die.
(tools/larr_px.py does the same but its output cannot be cut into columns.)
"""
import sys, os, json, argparse
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('comp'); ap.add_argument('dir', choices=['row', 'col'])
ap.add_argument('c', type=int); ap.add_argument('a', type=int); ap.add_argument('b', type=int); ap.add_argument('step', type=int)
ap.add_argument('--r', type=int, default=1); ap.add_argument('--layers', default='acid,acid1b')
ap.add_argument('--shift', default='0,0')
a = ap.parse_args()
L = a.layers.split(',')
dx, dy = map(int, a.shift.split(','))
if a.comp == '-':
    f = {'metal': 'metal.npy', 'acid': 'acid_aligned.npy', 'metal1': 'metal1.npy', 'acid1b': 'acid1b.npy'}
    A = {l: np.load(os.path.join(ROOT, 'cache', f[l]), mmap_mode='r') for l in L}; x0 = y0 = 0
else:
    d = os.path.join(ROOT, 'cache', 'comp'); j = json.load(open(os.path.join(d, a.comp + '.json')))
    A = {l: np.load(os.path.join(d, f'{a.comp}_{l}.npy')) for l in L}; x0, y0 = j['x0'], j['y0']
def m(l, x, y):
    x += dx - x0; y += dy - y0; r = a.r
    return A[l][y - r:y + r + 1, x - r:x + r + 1].reshape(-1, 3).astype(float).mean(0)
print('%13s  ' % '' + '   '.join('%-20s' % l for l in L))
for v in range(a.a, a.b + 1, a.step):
    x, y = (v, a.c) if a.dir == 'row' else (a.c, v)
    print('%6d,%6d  ' % (x, y) + '   '.join('%3d %3d %3d (%+4d)  ' % (*m(l, x, y), m(l, x, y)[0] - m(l, x, y)[1]) for l in L))
