#!/usr/bin/env python3
"""Classify what lies along a horizontal or vertical track (cdp1 helper).

usage: cdp1_line.py h Y X0 X1 [--half 5] [--step 6] [--layer acid1b]
       cdp1_line.py v X Y0 Y1 [--half 5] [--step 6]

Samples boxes of `step` along the track and 2*half+1 across it, on the single shot, and
prints one class letter per box (same classes as the map of tools/cdp1_px.py):
  D diffusion under metal  F field under metal  P poly under metal  C poly over channel
  g metal contact (greenish)  o field/diffusion in the open  p poly in the open  # dark
plus a second row from the metal shot: M metal, - none.
Use it to find where a long poly line has contacts or ends; check each find by eye.
"""
import argparse, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view
REF = {'D': (197, 175, 131), 'F': (187, 117, 123), 'P': (207, 150, 110), 'C': (238, 170, 124),
       'g': (160, 163, 100), 'o': (143, 130, 95), 'p': (141, 83, 51), '#': (75, 55, 45)}
ap = argparse.ArgumentParser()
ap.add_argument('dir'); ap.add_argument('c', type=int); ap.add_argument('a', type=int); ap.add_argument('b', type=int)
ap.add_argument('--half', type=int, default=5); ap.add_argument('--step', type=int, default=6)
ap.add_argument('--layer', default='acid1b')
a = ap.parse_args()
keys = list(REF); refs = np.array([REF[k] for k in keys], np.float32)
h, s = a.half, a.step
out, met = '', ''
for t in range(a.a, a.b, s):
    if a.dir == 'h':
        box = (t, a.c - h, s, 2 * h + 1)
    else:
        box = (a.c - h, t, 2 * h + 1, s)
    c = view.raw(a.layer, *box).reshape(-1, 3).astype(np.float32).mean(0)
    out += keys[int(((refs - c) ** 2).sum(1).argmin())]
    m = view.raw('metal', *box).reshape(-1, 3).astype(np.float32).mean(0)
    met += 'M' if (m[0] > 180 and m[1] > 140) else '-'
n = 100
for i in range(0, len(out), n):
    print('%6d  %s' % (a.a + i * s, out[i:i + n]))
    print('%6s  %s' % ('metal', met[i:i + n]))
