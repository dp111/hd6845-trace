#!/usr/bin/env python3
"""Find the jogs of a bundle of vertical metal tracks: where is there metal BETWEEN tracks?

usage: tools/t.sh rdp3 rdp3_jogs.py X0 PITCH N --a Y0 --b Y1 [--layer metal] [--hw 3]
       [--bright 150] [--min 8]

Tracks stand at X0 + k*PITCH (k = 0..N-1). For each gap between neighbouring tracks the
tool looks at a narrow column at the gap's centre and prints the y-runs where the metal
shot is bright (a horizontal piece of metal crossing the gap: a jog, or a line leaving
the bundle). It also prints, per track, the y-runs where the track itself is NOT metal
(gaps of any length, not bridged). tools/sel_tracks.py bridges gaps of up to 14 px, so a
track on which one net ends and another starts 20 px further on reads as one line
there: that is how run 2 took two different nets for one.
Numbers say where to look; confirm by a view.
"""
import argparse, os
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('x0', type=float); ap.add_argument('pitch', type=float); ap.add_argument('n', type=int)
ap.add_argument('--a', type=int, required=True); ap.add_argument('--b', type=int, required=True)
ap.add_argument('--layer', default='metal'); ap.add_argument('--hw', type=int, default=3)
ap.add_argument('--bright', type=float, default=166); ap.add_argument('--min', type=int, default=8)
a = ap.parse_args()
arr = np.load(os.path.join(ROOT, 'cache', a.layer + '.npy'), mmap_mode='r')
def prof(x):
    """row means of a column 2*hw+1 wide, lightly smoothed. Metal is above about 175,
    bare field between tracks 150-160 (and smooth), poly and edges below 130."""
    x = int(round(x))
    s = np.asarray(arr[a.a:a.b, x - a.hw:x + a.hw + 1]).astype(np.float32)
    g = ((s[..., 0] + s[..., 1]) / 2).mean(1)
    return np.convolve(g, np.ones(3) / 3, 'same')
def runs(on, minlen):
    out = []; i = 0; n = len(on)
    while i < n:
        if on[i]:
            j = i
            while j < n and on[j]: j += 1
            if j - i >= minlen: out.append((a.a + i, a.a + j))
            i = j
        else: i += 1
    return out
print('metal between tracks (jogs):')
for k in range(a.n - 1):
    x = a.x0 + (k + 0.5) * a.pitch
    # a jog can be narrow or slanted: take the brightest of three columns across the gap
    p = np.maximum(np.maximum(prof(x - 7), prof(x)), prof(x + 7))
    r = runs(p > a.bright, a.min)
    print('  L%d|L%d x %d: %s' % (k, k + 1, x, ' '.join('%d-%d' % t for t in r)))
print('no metal on track (breaks):')
for k in range(a.n):
    x = a.x0 + k * a.pitch
    p = prof(x)
    r = runs(p < 135, a.min)
    print('  L%d x %d: %s' % (k, x, ' '.join('%d-%d' % t for t in r)))
