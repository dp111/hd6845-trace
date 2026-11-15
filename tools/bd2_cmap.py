#!/usr/bin/env python3
"""Character map of a small area in the metal shots and chip 2's stripped shot, to tell
poly from plain areas where no metal covers them.

usage: bd2_cmap.py x0 y0 x1 y1 [step] [layers]     layers default metal,metal1,acid

Per cell of step x step px, from the mean colour:
   .  dark (edge line, outline)            max(R,G) < 105 (metal shots) / < 95 (acid)
   M  metal: R >= 185 and G >= 150 (metal shots only)
   o  orange = poly:  R - G >= T          T = 40 for metal, 45 for metal1, 28 for acid
   k  plain (khaki / tan: field or diffusion): everything else
The thresholds were set on patches of known layers at x 15900-16100, y 15540-15700
(see notes/blocks/bd2.md); re-check them before using the map elsewhere.
"""
import os, sys
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = {'metal': 'metal.npy', 'metal1': 'metal1.npy', 'acid': 'acid_aligned.npy', 'acid1b': 'acid1b.npy'}
T = {'metal': 40, 'metal1': 45, 'acid': 28}
x0, y0, x1, y1 = map(int, sys.argv[1:5])
st = int(sys.argv[5]) if len(sys.argv) > 5 else 2
layers = sys.argv[6].split(',') if len(sys.argv) > 6 else ['metal', 'metal1', 'acid']
A = {l: np.load(os.path.join(ROOT, 'cache', F[l]), mmap_mode='r') for l in layers}
xs = list(range(x0, x1, st))
def cls(l, m):
    r, g, b = m
    if max(r, g) < (95 if l == 'acid' else 105):
        return '.'
    if l != 'acid' and r >= 185 and g >= 150:
        return 'M'
    return 'o' if r - g >= T[l] else 'k'
hdr = ''.join(str((x // 10) % 10) if x % 10 < st else ' ' for x in xs)
print('x from %d step %d; header digit = tens of x' % (x0, st))
print('%6s  %s' % ('', '  '.join(hdr for _ in layers)))
print('%6s  %s' % ('y', '  '.join(l.ljust(len(xs)) for l in layers)))
for y in range(y0, y1, st):
    rows = []
    for l in layers:
        rows.append(''.join(cls(l, np.asarray(A[l][y:y + st, x:x + st]).reshape(-1, 3).mean(0)) for x in xs))
    print('%6d  %s' % (y, '  '.join(rows)))
