#!/usr/bin/env python3
"""Metal runs along a horizontal or vertical cut of the metal shot (fixed colour threshold).

usage: larr_cut.py h Y X0 X1 [--hw 3] [--min 8] [--gap 0]     runs of metal along y=Y
       larr_cut.py v X Y0 Y1 [--hw 3] [--min 8] [--gap 14]    runs of metal along x=X
Metal = R>180 and G>138 on the mean over +-hw px across the cut. Runs shorter than --min
are dropped; breaks shorter than --gap are bridged (a poly or diffusion edge under the
metal is a dark line 6-10 px wide; a contact ring is two of them).
--layer metal|metal1.  Several Y (or X) may be given separated by commas.
"""
import argparse, os
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('dir', choices=['h', 'v']); ap.add_argument('c'); ap.add_argument('a', type=int); ap.add_argument('b', type=int)
ap.add_argument('--hw', type=int, default=3); ap.add_argument('--min', type=int, default=8); ap.add_argument('--gap', type=int, default=None)
ap.add_argument('--layer', default='metal')
a = ap.parse_args()
gap = a.gap if a.gap is not None else (0 if a.dir == 'h' else 14)
arr = np.load(os.path.join(ROOT, 'cache', a.layer + '.npy'), mmap_mode='r')
for c in map(int, a.c.split(',')):
    if a.dir == 'h':
        s = np.asarray(arr[c - a.hw:c + a.hw + 1, a.a:a.b]).astype(float).mean(0)
    else:
        s = np.asarray(arr[a.a:a.b, c - a.hw:c + a.hw + 1]).astype(float).mean(1)
    m = (s[:, 0] > 180) & (s[:, 1] > 138)
    runs = []; i = 0; n = len(m)
    while i < n:
        if m[i]:
            j = i
            while j < n and m[j]: j += 1
            runs.append([i, j]); i = j
        else: i += 1
    out = []
    for r in runs:
        if out and r[0] - out[-1][1] <= gap: out[-1][1] = r[1]
        else: out.append(r)
    out = [r for r in out if r[1] - r[0] >= a.min]
    print(('y' if a.dir == 'h' else 'x') + f'={c}: ' + '  '.join(f'{a.a + r[0]}-{a.a + r[1]}' for r in out))
