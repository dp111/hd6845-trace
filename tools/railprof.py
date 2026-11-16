#!/usr/bin/env python3
"""What lies under a vertical rail, as text: railprof.py x0 x1 y0 y1 [--min N] [--horizontal]

Classifies the strip x0..x1 of the clean shot (acid1b) with the class map's rules (valid where
metal was above, i.e. under a rail) and prints the runs along y of the majority class:
  D diffusion   C poly over a channel (a gate)   P poly over field   . field   # dark
A run of '#' or mixed classes inside diffusion is usually a contact pit or an edge; it is
printed with the share of dark pixels. Runs shorter than --min px (default 6) are merged into
their neighbours. With --horizontal the strip is y0..y1 and the runs are along x (a horizontal
rail). It is a reading aid: check every gate it reports on a view before drawing it.
"""
import argparse
import os
import sys
from collections import Counter
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view
import classmap


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('x0', type=int); ap.add_argument('x1', type=int)
    ap.add_argument('y0', type=int); ap.add_argument('y1', type=int)
    ap.add_argument('--min', type=int, default=6)
    ap.add_argument('--horizontal', action='store_true')
    a = ap.parse_args()
    rgb = view.raw('acid1b', a.x0, a.y0, a.x1 - a.x0, a.y1 - a.y0)
    cls = classmap.classify(rgb[..., :3])
    if a.horizontal:
        cls = cls.T
        base = a.x0
    else:
        base = a.y0
    rows = []
    for i in range(cls.shape[0]):
        c = Counter(cls[i])
        n = sum(c.values())
        dark = c.get('#', 0) / n
        rest = [(k, v) for k, v in c.items() if k != '#']
        top = max(rest, key=lambda kv: kv[1])[0] if rest and dark < 0.7 else '#'
        if top in ('d', 'p', ',', '?'):          # open-area classes do not apply under a rail
            top = {'d': 'D', 'p': 'P', ',': '.', '?': '?'}[top]
        rows.append((top, dark))
    runs = []
    for i, (k, dk) in enumerate(rows):
        if runs and runs[-1][0] == k:
            runs[-1][2] = i; runs[-1][3].append(dk)
        else:
            runs.append([k, i, i, [dk]])
    # merge short runs into the previous one
    merged = []
    for r in runs:
        if merged and (r[2] - r[1] + 1) < a.min:
            merged[-1][2] = r[2]; merged[-1][3] += r[3]; merged[-1][4] += r[0]
        elif merged and merged[-1][0] == r[0]:
            merged[-1][2] = r[2]; merged[-1][3] += r[3]
        else:
            merged.append(r + [''])
    names = {'D': 'diffusion', 'C': 'GATE (poly over channel)', 'P': 'poly over field',
             '.': 'field', '#': 'dark', '?': '?'}
    for k, i0, i1, dks, extra in merged:
        note = f'  dark {max(dks):.0%}' if k in ('D', 'C') and max(dks) > 0.25 else ''
        print(f'{base + i0}-{base + i1}  {names[k]}{note}')


if __name__ == '__main__':
    main()
