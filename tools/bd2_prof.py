#!/usr/bin/env python3
"""Is there metal here?  Colour and grain of the two metal shots, as numbers.

usage: bd2_prof.py map  x0 y0 x1 y1 [step]      character map of a rectangle, both metal shots
       bd2_prof.py stat x0,y0:x1,y1[=name] ...  mean R/G/B, G/R and grain of rectangles
       bd2_prof.py col  x y0 y1 [hw] [step]     profile down a column: mean of x-hw..x+hw
       bd2_prof.py row  y x0 x1 [hw] [step]     profile along a row: mean of y-hw..y+hw

Metal in the metal shots is bright yellow and grainy: R about 200, G/R about 0.8-0.9,
pixel-to-pixel spread (grain) of 15 or more. Bare poly is orange: G/R 0.55-0.7, smooth.
Field is khaki, smooth. Edge lines are dark (R below 110).
Classes of the map (per cell of step x step px, from the cell's mean colour):
   M  metal     R >= 170 and G/R >= 0.74
   o  orange    R >= 120 and G/R < 0.74          (bare poly)
   f  field     110 <= R < 170 and G/R >= 0.74   (bare field / diffusion, khaki)
   .  dark      R < 110                          (edge line, contact ring)
'stat' and 'col' also print grain = standard deviation of (R+G)/2 over the patch.
"""
import os
import sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = ('metal', 'metal1')
A = {l: np.load(os.path.join(ROOT, 'cache', l + '.npy'), mmap_mode='r') for l in L}


def cls(r, g):
    if r < 110:
        return '.'
    q = g / max(r, 1)
    if q < 0.74:
        return 'o' if r >= 120 else '.'
    return 'M' if r >= 170 else 'f'


def patch(l, x0, y0, x1, y1):
    return np.asarray(A[l][y0:y1, x0:x1]).astype(np.float32)


def desc(p):
    m = p.reshape(-1, 3).mean(0)
    g = ((p[..., 0] + p[..., 1]) / 2).std()
    return '%3d/%3d/%3d g/r %.2f grain %4.1f %s' % (m[0], m[1], m[2], m[1] / max(m[0], 1), g, cls(m[0], m[1]))


def main():
    cmd = sys.argv[1]
    if cmd == 'map':
        x0, y0, x1, y1 = map(int, sys.argv[2:6])
        st = int(sys.argv[6]) if len(sys.argv) > 6 else 3
        xs = list(range(x0, x1, st))
        print('columns x = %d .. %d step %d' % (xs[0], xs[-1], st))
        print('%7s  %-*s  %s' % ('y', len(xs), L[0], L[1]))
        for y in range(y0, y1, st):
            row = []
            for l in L:
                s = ''
                for x in xs:
                    m = patch(l, x, y, x + st, y + st).reshape(-1, 3).mean(0)
                    s += cls(m[0], m[1])
                row.append(s)
            print('%7d  %s  %s' % (y, row[0], row[1]))
    elif cmd == 'stat':
        for t in sys.argv[2:]:
            name = ''
            if '=' in t:
                t, name = t.split('=')
            a, b = t.split(':')
            x0, y0 = map(int, a.split(','))
            x1, y1 = map(int, b.split(','))
            print('%-28s %s' % (t, '   '.join(l + ' ' + desc(patch(l, x0, y0, x1, y1)) for l in L)), name)
    elif cmd in ('col', 'row'):
        c, a, b = map(int, sys.argv[2:5])
        hw = int(sys.argv[5]) if len(sys.argv) > 5 else 5
        st = int(sys.argv[6]) if len(sys.argv) > 6 else 3
        for v in range(a, b, st):
            if cmd == 'col':
                r = (c - hw, v, c + hw + 1, v + st)
            else:
                r = (v, c - hw, v + st, c + hw + 1)
            print('%6d  %s' % (v, '   '.join(l + ' ' + desc(patch(l, *r)) for l in L)))


main()
