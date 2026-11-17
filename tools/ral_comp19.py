#!/usr/bin/env python3
"""Median of the nineteen ral_cell copies (five RA, fourteen MA turned 90 degrees, eleven
of those mirrored) in the master's frame, written as composite ral_c19 for view.py --comp.

usage: ral_comp19.py
The MA copies are undone with the inverse of their @inst transform (their placements are
listed below; they are drawn in trace/mal.txt on branch mal):
a master point p maps to the copy at R90(mirror(p)) + offset, about o = (14235,4395).
"""
import json, os
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
X0, Y0, X1, Y1 = 13990, 4240, 14460, 4600
O = (14235, 4395)
RA = [0, 434, 868, 1431, 1865]
MA = [(-11576, 3760, 1), (-11576, 4366, 1), (-11576, 4973, 1), (-11576, 5581, 1),
      (-11576, 6232, 1), (-11576, 6839, 1), (-11576, 7641, 1), (-11575, 8335, 1),
      (-11575, 8987, 1), (-11575, 11111, 1), (-11575, 11806, 1), (-11574, 12880, 0),
      (-11574, 13530, 0), (-11574, 14181, 0)]
F = {'metal': 'metal.npy', 'acid': 'acid_aligned.npy', 'acid1b': 'acid1b.npy', 'metal1': 'metal1.npy'}
ys, xs = np.mgrid[Y0:Y1, X0:X1]
out = {}
for lay, fn in F.items():
    A = np.load(os.path.join(ROOT, 'cache', fn), mmap_mode='r')
    stack = []
    for dx in RA:
        stack.append(np.asarray(A[Y0:Y1, X0 + dx:X1 + dx]))
    for dx, dy, mx in MA:
        px = (2 * O[0] - xs) if mx else xs
        py = ys
        # rotate 90 degrees clockwise about O (as seen on the photo: x' = ox - (y-oy), y' = oy + (x-ox))
        rx = O[0] - (py - O[1]); ry = O[1] + (px - O[0])
        sx = (rx + dx).astype(int); sy = (ry + dy).astype(int)
        stack.append(np.asarray(A[sy, sx]))
    out[lay] = np.median(np.stack(stack), axis=0).astype(np.uint8)
d = os.path.join(ROOT, 'cache', 'comp'); os.makedirs(d, exist_ok=True)
for lay, a in out.items():
    np.save(os.path.join(d, 'ral_c19_%s.npy' % lay), a)
json.dump({'x0': X0, 'y0': Y0, 'w': X1 - X0, 'h': Y1 - Y0, 'n': 19}, open(os.path.join(d, 'ral_c19.json'), 'w'))
print('ral_c19: median of 19 copies,', X1 - X0, 'x', Y1 - Y0)
