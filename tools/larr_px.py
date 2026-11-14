#!/usr/bin/env python3
"""Print mean colours of small patches of a composite (or of the die) in all layers.

usage: larr_px.py COMP|- x,y[,r] [x,y[,r] ...]      r = half-size of the patch (default 3)
       larr_px.py COMP|- row y x0 x1 step           profile along a row
       larr_px.py COMP|- col x y0 y1 step           profile down a column
"""
import json, os, sys
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = ('metal', 'metal1', 'acid', 'acid1b')
def load(comp):
    if comp == '-':
        f = {'metal': 'metal.npy', 'acid': 'acid_aligned.npy', 'metal1': 'metal1.npy', 'acid1b': 'acid1b.npy'}
        return {l: np.load(os.path.join(ROOT, 'cache', f[l]), mmap_mode='r') for l in L}, 0, 0
    d = os.path.join(ROOT, 'cache', 'comp')
    j = json.load(open(os.path.join(d, comp + '.json')))
    return {l: np.load(os.path.join(d, f'{comp}_{l}.npy')) for l in L}, j['x0'], j['y0']
def main():
    A, x0, y0 = load(sys.argv[1])
    def s(x, y, r=3):
        return '  '.join('%3d/%3d/%3d' % tuple(A[l][y - y0 - r:y - y0 + r + 1, x - x0 - r:x - x0 + r + 1].reshape(-1, 3).mean(0)) for l in L)
    print('%14s  %s' % ('', '  '.join('%-11s' % l for l in L)))
    if sys.argv[2] == 'row':
        y, a, b, st = map(int, sys.argv[3:7])
        for x in range(a, b + 1, st):
            print('%6d,%6d   %s' % (x, y, s(x, y, 1)))
    elif sys.argv[2] == 'col':
        x, a, b, st = map(int, sys.argv[3:7])
        for y in range(a, b + 1, st):
            print('%6d,%6d   %s' % (x, y, s(x, y, 1)))
    else:
        for t in sys.argv[2:]:
            p = list(map(int, t.split(',')))
            r = p[2] if len(p) > 2 else 3
            print('%6d,%6d   %s' % (p[0], p[1], s(p[0], p[1], r)))
main()
