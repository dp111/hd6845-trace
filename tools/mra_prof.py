#!/usr/bin/env python3
"""Classified colour profile along a cut of a composite: a reading aid for junctions.

usage: mra_prof.py COMP|- h Y X0 X1 [STEP]      along y = Y   (several Y: comma separated)
       mra_prof.py COMP|- v X Y0 Y1 [STEP]      along x = X
       add --raw to print the colours (metal, acid, acid1b) of every sample instead of runs

Each sample is the mean of a 3x3 patch. Classes (calibrated in the mid-right array on
the traced q / n1 poly, the VCC boxes and the field between the lines; see
notes/blocks/mra.md):
  metal shot:   M metal present (bright), - none
  clean shot, where metal was above:  P poly (salmon)   D diffusion (tan)   . field (pink)
  clean shot, in the open:            p poly (dark red) d diffusion (mauve) , field (green/olive)
  #  dark (an edge line, a contact pit)        ? none of these
Output without --raw: runs "x0-x1:c" of equal class, one line per cut.
Borders are uncertain by the step; an edge line is 6-8 px wide and separates everything,
so 'P#P' is not evidence of two pieces, and neither is 'P#D' evidence of a junction.
"""
import json, os, sys
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = ('metal', 'metal1', 'acid', 'acid1b')


def load(comp):
    if comp == '-':
        f = {'metal': 'metal.npy', 'acid': 'acid_aligned.npy', 'metal1': 'metal1.npy', 'acid1b': 'acid1b.npy'}
        return {l: np.load(os.path.join(ROOT, 'cache', f[l]), mmap_mode='r') for l in L}, 0, 0
    d = os.path.join(ROOT, 'cache', 'comp')
    j = json.load(open(os.path.join(d, comp + '.json')))
    return {l: np.load(os.path.join(d, f'{comp}_{l}.npy')) for l in L}, j['x0'], j['y0']


def cls(m, m1, b):
    """m, m1: metal shots; b: clean shot (RGB means)."""
    metal = (m[0] > 176 and m[1] > 138) or (m1[0] > 176 and m1[1] > 138)
    r, g, bl = b
    if r < 125 and g < 95:
        c = '#'
    elif r > 170:
        # protected colours (metal above or near)
        d = r - g
        if d > 62: c = '.'
        elif d > 36: c = 'P'
        else: c = 'D'
    else:
        if g > r + 5: c = ','
        elif r - g > 30: c = 'p'
        elif r > 125: c = 'd'
        else: c = '?'
    return ('M' if metal else '-'), c


def main():
    raw = '--raw' in sys.argv
    args = [a for a in sys.argv[1:] if a != '--raw']
    comp, d, cs, a, b = args[0], args[1], args[2], int(args[3]), int(args[4])
    st = int(args[5]) if len(args) > 5 else 2
    A, x0, y0 = load(comp)
    def s(l, x, y):
        return np.asarray(A[l][y - y0 - 1:y - y0 + 2, x - x0 - 1:x - x0 + 2]).reshape(-1, 3).mean(0)
    for c in map(int, cs.split(',')):
        pts = [(t, c) if d == 'h' else (c, t) for t in range(a, b + 1, st)]
        if raw:
            print(('y' if d == 'h' else 'x') + f'={c}   metal / acid / acid1b / class')
            for (x, y) in pts:
                m, m1, ac, cb = s('metal', x, y), s('metal1', x, y), s('acid', x, y), s('acid1b', x, y)
                k = cls(m, m1, cb)
                print('%6d  %3d %3d %3d  %3d %3d %3d  %3d %3d %3d  %s%s' % ((x if d == 'h' else y,) + tuple(m) + tuple(ac) + tuple(cb) + k))
            continue
        runs = []
        for (x, y) in pts:
            k = cls(s('metal', x, y), s('metal1', x, y), s('acid1b', x, y))
            t = x if d == 'h' else y
            for i in (0, 1):
                pass
            if runs and runs[-1][2] == k[1]:
                runs[-1][1] = t
            else:
                runs.append([t, t, k[1]])
        print(('y' if d == 'h' else 'x') + f'={c}: ' + ' '.join(f'{r[0]}-{r[1]}{r[2]}' if r[1] > r[0] else f'{r[0]}{r[2]}' for r in runs))


main()
