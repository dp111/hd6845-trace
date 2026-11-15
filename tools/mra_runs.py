#!/usr/bin/env python3
"""Runs of metal along cuts of a median composite (or of the die), as text.

usage: mra_runs.py COMP|- h Y0 Y1 STEP X0 X1     horizontal cuts at y = Y0, Y0+STEP, .. : runs in x
       mra_runs.py COMP|- v X0 X1 STEP Y0 Y1     vertical cuts at x = X0, X0+STEP, ..   : runs in y
       options: --hw 2 (half-width of the cut), --min 6 (shortest run kept),
                --thr R,G (default 190,152), --one (metal shot of chip 2 only)

Metal = R > thr and G > thr in BOTH metal shots (chip 2 `metal`, chip 1 `metal1`),
mean over the cut's width. A poly or diffusion edge under a line is a dark bar 6-10 px
wide, so a line is broken into pieces at every edge underneath: read the pieces of one
column together. Contact rings break a run twice. Runs are printed as x0-x1 (inclusive
start, exclusive end).
"""
import json, os, sys
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(comp):
    if comp == '-':
        f = {'metal': 'metal.npy', 'metal1': 'metal1.npy'}
        return {l: np.load(os.path.join(ROOT, 'cache', f[l]), mmap_mode='r') for l in f}, 0, 0
    d = os.path.join(ROOT, 'cache', 'comp')
    j = json.load(open(os.path.join(d, comp + '.json')))
    return {l: np.load(os.path.join(d, f'{comp}_{l}.npy')) for l in ('metal', 'metal1')}, j['x0'], j['y0']


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    opt = sys.argv[1:]
    def o(name, default):
        return opt[opt.index(name) + 1] if name in opt else default
    hw = int(o('--hw', 2)); mn = int(o('--min', 6))
    tr, tg = map(int, o('--thr', '190,152').split(','))
    one = '--one' in opt
    args = [a for a in args if a not in (o('--hw', ''), o('--min', ''), o('--thr', ''))] if False else args
    comp, d = args[0], args[1]
    c0, c1, st, a, b = map(int, args[2:7])
    A, x0, y0 = load(comp)
    for c in range(c0, c1 + 1, st):
        m = None
        for l in (('metal',) if one else ('metal', 'metal1')):
            if d == 'h':
                s = np.asarray(A[l][c - y0 - hw:c - y0 + hw + 1, a - x0:b - x0]).astype(float).mean(0)
            else:
                s = np.asarray(A[l][a - y0:b - y0, c - x0 - hw:c - x0 + hw + 1]).astype(float).mean(1)
            k = (s[:, 0] > tr) & (s[:, 1] > tg)
            m = k if m is None else (m & k)
        runs = []; i = 0; n = len(m)
        while i < n:
            if m[i]:
                j = i
                while j < n and m[j]: j += 1
                if j - i >= mn: runs.append((a + i, a + j))
                i = j
            else: i += 1
        print(('y' if d == 'h' else 'x') + f'{c}: ' + ' '.join(f'{r[0]}-{r[1]}' for r in runs))


main()
