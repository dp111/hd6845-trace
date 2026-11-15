#!/usr/bin/env python3
"""Where metal is present along vertical (or horizontal) tracks, from the chip-2 metal shot.

usage: tla_tracks.py y0 y1 x [x ...] [--half 4] [--gap 14] [--horizontal]

For each track centre x, the metal shot is sampled in a strip 2*half+1 px wide from y0 to y1
(with --horizontal the roles of x and y are swapped: tla_tracks.py x0 x1 y ...). A row counts
as metal when its blurred mean green is above --gmin (152) and red above --rmin (180) (metal 200/178/95, open
ground 150-175/110-145/60-90, measured west of the counters). Runs of metal are printed with
their ends; a run is split only where at least --gap rows in a row are not metal, so the dark
edge lines of poly crossings and contact rings (6-10 px) do not split it.

This finds where a line is INTERRUPTED. It says nothing about contacts, and a piece end is
good to about 8 px. Check every end it reports in the photos before drawing.
"""
import argparse
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view

ap = argparse.ArgumentParser()
ap.add_argument('a0', type=int)
ap.add_argument('a1', type=int)
ap.add_argument('tracks', type=int, nargs='+')
ap.add_argument('--half', type=int, default=4)
ap.add_argument('--gap', type=int, default=14)
ap.add_argument('--horizontal', action='store_true')
ap.add_argument('--gmin', type=int, default=152)
ap.add_argument('--rmin', type=int, default=180)
ap.add_argument('--minrun', type=int, default=8)
a = ap.parse_args()
for t in a.tracks:
    if a.horizontal:
        rgb = view.raw('metal', a.a0, t - a.half, a.a1 - a.a0, 2 * a.half + 1).mean(0)
    else:
        rgb = view.raw('metal', t - a.half, a.a0, 2 * a.half + 1, a.a1 - a.a0).mean(1)
    k = np.ones(5) / 5
    r = np.convolve(rgb[:, 0], k, 'same')
    g = np.convolve(rgb[:, 1], k, 'same')
    m = (g > a.gmin) & (r > a.rmin)
    runs = []
    start = None
    last = None
    for i, v in enumerate(m):
        if v:
            if start is None:
                start = i
            elif i - last > a.gap:
                runs.append((start, last))
                start = i
            last = i
    if start is not None:
        runs.append((start, last))
    runs = [(s, e) for s, e in runs if e - s >= a.minrun]
    print('%5d: ' % t + '  '.join('%d-%d' % (a.a0 + s, a.a0 + e) for s, e in runs))
