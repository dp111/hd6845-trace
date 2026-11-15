#!/usr/bin/env python3
"""ASCII class map of a region, from measured colours (cheap to read, no eyeballing).

usage: larr_asc.py COMP|- x y w h [--step N] [--layers a,m]

Samples every N px (default 4; mean of 3x3 px) and prints one character per sample.
Map 'a' (clean shot acid1b; classes calibrated in the left array, rows s0-s13):
   P  poly under metal (salmon)            p  poly in the open (dark red-brown)
   D  diffusion under metal (tan)          d  diffusion in the open (green, bright)
   .  field under metal (pink)             ,  field in the open (dark olive)
   #  dark edge / outline                  ?  none of these (mixed pixel, contact, dirt)
Map 'm' (metal shot):  M metal, o dark (ring, edge), blank no metal.
Map 'c' (chip-2 stripped shot of a composite, R/G ratio): P >1.24, D 1.10-1.24, . <1.10, # dark
Column header: x of every 10th sample.  A reading aid: borders are a few px uncertain,
and a feature narrower than about 12 px is mostly '#' or '?'.
"""
import argparse, json, os, sys
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('comp'); ap.add_argument('x', type=int); ap.add_argument('y', type=int)
ap.add_argument('w', type=int); ap.add_argument('h', type=int)
ap.add_argument('--step', type=int, default=4); ap.add_argument('--layers', default='a,m')
a = ap.parse_args()
L = ('metal', 'acid', 'acid1b')
if a.comp == '-':
    f = {'metal': 'metal.npy', 'acid': 'acid_aligned.npy', 'acid1b': 'acid1b.npy'}
    A = {l: np.load(os.path.join(ROOT, 'cache', f[l]), mmap_mode='r') for l in L}; x0 = y0 = 0
else:
    d = os.path.join(ROOT, 'cache', 'comp'); j = json.load(open(os.path.join(d, a.comp + '.json')))
    A = {l: np.load(os.path.join(d, f'{a.comp}_{l}.npy')) for l in L}; x0, y0 = j['x0'], j['y0']
def px(l, x, y):
    return A[l][y - y0 - 1:y - y0 + 2, x - x0 - 1:x - x0 + 2].reshape(-1, 3).astype(float).mean(0)
def cls_a(x, y):
    r, g, b = px('acid1b', x, y)
    if max(r, g, b) < 78: return '#'
    if r > 200 and r - g > 42 and b < 135: return 'P'
    if r >= 150 and r - g >= 40 and b >= g - 12: return '.'
    if 95 < r < 185 and r / max(g, 1) > 1.33 and b < g - 3: return 'p'
    if g > r + 8 and g > 105: return 'd'
    if 155 <= r <= 212 and r - g < 36 and g >= 140: return 'D'
    if r < 112 and g < 112 and g >= r - 8: return ','
    return '?'
def cls_m(x, y):
    r, g, b = px('metal', x, y)
    if r > 188 and g > 145: return 'M'
    if max(r, g, b) < 90: return 'o'
    return ' '
def cls_c(x, y):
    r, g, b = px('acid', x, y)
    if max(r, g, b) < 85: return '#'
    q = r / max(g, 1)
    return 'P' if q > 1.24 else ('D' if q > 1.10 else '.')
F = {'a': cls_a, 'm': cls_m, 'c': cls_c}
xs = list(range(a.x, a.x + a.w, a.step)); ys = list(range(a.y, a.y + a.h, a.step))
for l in a.layers.split(','):
    print(f'--- map {l}  x {a.x}..{a.x + a.w} step {a.step}')
    for dgt in range(4):
        print('      ' + ''.join(str(x).rjust(4)[dgt] if i % 5 == 0 else ' ' for i, x in enumerate(xs)))
    for y in ys:
        print('%5d ' % y + ''.join(F[l](x, y) for x in xs))
