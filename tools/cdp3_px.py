#!/usr/bin/env python3
"""Classify material along scan lines from colour (cdp3 helper).

usage: cdp3_px.py COMP|- row Y X0 X1 [STEP]      one line of class letters per layer pair
       cdp3_px.py COMP|- col X Y0 Y1 [STEP]
       cdp3_px.py COMP|- pt x,y [x,y ...]        raw mean colours (5x5) in metal, acid, acid1b
       --shift dx,dy  look at another instance (die only)

Two strings are printed per scan line:
  c2: from the chip-2 shots (metal + stripped).  M metal above, P poly, D diffusion,
      F field, '.' dark (an edge), '?' none of these.  Valid only where no metal lies.
  c1: from the clean chip-1 shot.  p/d/f = poly/diffusion/field as they look where metal
      was above (salmon / tan / pink); P/D/F = in the open (dark red / mauve / khaki),
      g = bright green rim, '.' dark.
Thresholds were set on the row C cell of the central datapath (x 9545-9950, y 9200-9500)
and are only meant for that neighbourhood. Edges are 6-8 px wide, so letters next to a
'.' are unreliable.
"""
import json, os, sys
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = ('metal', 'acid', 'acid1b')
def load(comp):
    if comp == '-':
        f = {'metal': 'metal.npy', 'acid': 'acid_aligned.npy', 'acid1b': 'acid1b.npy'}
        return {l: np.load(os.path.join(ROOT, 'cache', f[l]), mmap_mode='r') for l in L}, 0, 0
    d = os.path.join(ROOT, 'cache', 'comp')
    j = json.load(open(os.path.join(d, comp + '.json')))
    return {l: np.load(os.path.join(d, f'{comp}_{l}.npy')) for l in L}, j['x0'], j['y0']
args = sys.argv[1:]
sh = (0, 0)
if '--shift' in args:
    i = args.index('--shift'); sh = tuple(map(int, args[i + 1].split(','))); del args[i:i + 2]
A, X0, Y0 = load(args[0])
def px(l, x, y, r=1):
    x += sh[0]; y += sh[1]
    return A[l][y - Y0 - r:y - Y0 + r + 1, x - X0 - r:x - X0 + r + 1].reshape(-1, 3).astype(float).mean(0)
def c2(x, y):
    m = px('metal', x, y); a = px('acid', x, y)
    if m.max() < 115: return '.'
    if m[0] > 185 and m[1] > 150: return 'M'
    if m[2] < 68 and m[0] - m[1] > 22: return 'P'
    if a[1] >= a[0] - 4 and m[2] > 70: return 'F'
    if m[2] > 72 and m[0] - m[1] > 22: return 'D'
    return '?'
def c1(x, y):
    r, g, b = px('acid1b', x, y)
    if max(r, g, b) < 105: return '.'
    if g > r + 18: return 'g'
    if r > 180:                       # was under metal: bright
        if b > 0.58 * r and g < 0.72 * r: return 'f'   # pink
        if g < 0.775 * r: return 'p'                   # salmon
        return 'd'                                     # tan
    if g >= r - 8: return 'F'
    if b < 0.47 * r: return 'P'
    return 'D'
if args[1] == 'pt':
    for t in args[2:]:
        x, y = map(int, t.split(','))
        print('%6d,%6d  ' % (x, y) + '  '.join('%s %3d/%3d/%3d' % ((l,) + tuple(px(l, x, y, 2))) for l in L))
else:
    st = int(args[5]) if len(args) > 5 else 3
    p, a, b = int(args[2]), int(args[3]), int(args[4])
    pts = [(v, p) if args[1] == 'row' else (p, v) for v in range(a, b + 1, st)]
    print('%s=%d from %d step %d' % ('y' if args[1] == 'row' else 'x', p, a, st))
    print(' c2 ' + ''.join(c2(x, y) for x, y in pts))
    print(' c1 ' + ''.join(c1(x, y) for x, y in pts))
