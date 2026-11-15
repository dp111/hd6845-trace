#!/usr/bin/env python3
"""Colour profile along a row or a column in several shots, one line per step.

usage: tools/t.sh bd1 bd1_prof.py row Y X0 X1 [STEP] [--hw 2] [--layers acid1b,acid,metal,metal1]
       tools/t.sh bd1 bd1_prof.py col X Y0 Y1 [STEP]

Each line: the coordinate, then R/G/B of each shot averaged over a patch STEP long and
2*hw+1 across. For acid1b a class letter follows (same classes as bd1_map.py):
s poly under metal, r poly in the open, p pink field under metal, t tan diffusion under metal, . khaki, # dark, g green.
"""
import argparse
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view  # noqa: E402


def cls(r, g, b):
    if max(r, g, b) < 100:
        return '#'
    if g > r + 6:
        return 'g'
    if r - g > 30:
        if b >= g - 6 and r >= 165:
            return 'p'
        return 's' if r >= 185 else 'r'
    if r > 180:
        return 't'
    return '.'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dir', choices=['row', 'col'])
    ap.add_argument('c', type=int)
    ap.add_argument('a', type=int)
    ap.add_argument('b', type=int)
    ap.add_argument('step', type=int, nargs='?', default=3)
    ap.add_argument('--hw', type=int, default=2)
    ap.add_argument('--layers', default='acid1b,acid,metal,metal1')
    a = ap.parse_args()
    layers = a.layers.split(',')
    print(('x' if a.dir == 'row' else 'y') + '      ' + ''.join(f'{l:>15s}' for l in layers))
    for t in range(a.a, a.b, a.step):
        s = f'{t:6d} '
        for l in layers:
            if a.dir == 'row':
                p = view.raw(l, t, a.c - a.hw, a.step, 2 * a.hw + 1)
            else:
                p = view.raw(l, a.c - a.hw, t, 2 * a.hw + 1, a.step)
            r, g, b = p.reshape(-1, 3).mean(0)
            s += f'  {r:3.0f}/{g:3.0f}/{b:3.0f}'
            s += (' ' + cls(r, g, b)) if l == 'acid1b' else '  '
        print(s)


if __name__ == '__main__':
    main()
