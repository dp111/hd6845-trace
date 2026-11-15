#!/usr/bin/env python3
"""Where does one copy of a cell differ from the median of the others? (cdp1 helper)

usage: cdp1_diff.py x0 y0 x1 y1 --ref "0,0 390,0 780,0" --test "-390,0" [--step 4] [--layer acid1b] [--thr 45]

Builds the sharp median of the reference copies (as tools/cdp1_sr.py), aligns the test
copy to it the same way, and prints a text map: '.' where the block's mean colour is
within --thr of the median's, 'x' where it differs, 'X' where it differs by twice that.
Coordinates along the top are the master's. A cheap way to see which parts of an end
slice are not the common cell before spending an image on it.
"""
import argparse, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cdp1_sr

ap = argparse.ArgumentParser()
ap.add_argument('x0', type=int); ap.add_argument('y0', type=int)
ap.add_argument('x1', type=int); ap.add_argument('y1', type=int)
ap.add_argument('--ref', required=True); ap.add_argument('--test', required=True)
ap.add_argument('--step', type=int, default=4); ap.add_argument('--layer', default='acid1b')
ap.add_argument('--thr', type=float, default=45)
a = ap.parse_args()
P = lambda s: [tuple(int(v) for v in o.split(',')) for o in s.split()]
ref, test = P(a.ref), P(a.test)
UP = 2
w, h = a.x1 - a.x0, a.y1 - a.y0
for t in test:
    st = np.stack([cdp1_sr.sr(a.layer, a.x0, a.y0, w, h, [ref[0], o], UP, 'mean') * 2 for o in ref[1:]] )
    # each element is ref0 + other; recover the aligned others and take the median with ref0
    r0 = cdp1_sr.sr(a.layer, a.x0, a.y0, w, h, [ref[0]], UP, 'mean')
    others = [s - r0 for s in st]
    med = np.median(np.stack([r0] + others), axis=0)
    tt = cdp1_sr.sr(a.layer, a.x0, a.y0, w, h, [ref[0], t], UP, 'mean') * 2 - r0
    print('test copy %+d,%+d against the median of %d copies; step %d, x from %d' % (t[0], t[1], len(ref), a.step, a.x0))
    hdr = '      '
    for cx in range(a.x0, a.x1, a.step):
        hdr += str((cx // 10) % 10) if cx % 50 < a.step else ('|' if cx % 25 < a.step else ' ')
    print(hdr)
    s = a.step
    for cy in range(0, h, s):
        row = ''
        for cx in range(0, w, s):
            m = med[cy * UP:(cy + s) * UP, cx * UP:(cx + s) * UP].reshape(-1, 3).mean(0)
            v = tt[cy * UP:(cy + s) * UP, cx * UP:(cx + s) * UP].reshape(-1, 3).mean(0)
            d = np.abs(m - v).sum()
            row += 'X' if d > 2 * a.thr else ('x' if d > a.thr else '.')
        print('%5d %s' % (a.y0 + cy, row))
