#!/usr/bin/env python3
"""Is there metal along a vertical (or horizontal) track? Compact text profile.

usage: cdp2_mcol.py col X Y0 Y1 [--half 3] [--step 3] [--shift dx,dy] [--comp NAME]
       cdp2_mcol.py row Y X0 X1 [...]
For each step prints one character per metal shot (chip 2 first line, chip 1 second):
  M bright metal (R>186,G>148)   m probable (R>176,G>138)   . not metal   # dark (edge)
A dark line across a metal wire is usually the edge of something underneath, so a short
run of '#' between M's is not a break; a run of '.' (plain or brown, not dark) is.
The third line is the clean shot's class under it: P poly, C poly over channel (bright),
D diffusion(tan), F field(pink), k khaki, # dark, ? other.
"""
import argparse, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view
ap = argparse.ArgumentParser()
ap.add_argument('mode'); ap.add_argument('a', type=int); ap.add_argument('b', type=int); ap.add_argument('c', type=int)
ap.add_argument('--half', type=int, default=3); ap.add_argument('--step', type=int, default=3)
ap.add_argument('--shift'); ap.add_argument('--comp')
a = ap.parse_args()
if a.comp: view.use_comp(a.comp)
if a.shift: view._shift = tuple(int(v) for v in a.shift.split(','))
h = a.half
def cls_m(c):
    if c[0] > 186 and c[1] > 148: return 'M'
    if c[0] > 176 and c[1] > 138: return 'm'
    if c[0] < 120: return '#'
    return '.'
REF = {'P': (221,164,120), 'C': (240,172,124), 'D': (196,178,134), 'F': (195,117,126), 'k': (150,142,96), '#': (80,55,45), '?': (150,100,70)}
def cls_a(c):
    return min(REF, key=lambda k: sum((c[i]-REF[k][i])**2 for i in range(3)))
out = {'metal': '', 'metal1': '', 'acid1b': ''}
pos = range(a.b, a.c + 1, a.step)
for p in pos:
    for l in out:
        if a.mode == 'col':
            r = view.raw(l, a.a - h, p - 1, 2 * h + 1, 3)
        else:
            r = view.raw(l, p - 1, a.a - h, 3, 2 * h + 1)
        c = r.reshape(-1, 3).astype(float).mean(0)
        out[l] += cls_a(c) if l == 'acid1b' else cls_m(c)
n = 20
for i in range(0, len(out['metal']), n * 1):
    print(f'{a.mode} {a.a}  from {a.b + i * a.step:5d}:  c2 {out["metal"][i:i+n]}  c1 {out["metal1"][i:i+n]}  a1b {out["acid1b"][i:i+n]}')
