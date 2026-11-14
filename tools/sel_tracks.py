#!/usr/bin/env python3
"""Where is there metal along a vertical (or horizontal) track?

usage: sel_tracks.py v X [X ...] --a Y0 --b Y1 [--hw 5] [--win 12]
       sel_tracks.py h Y [Y ...] --a X0 --b X1

For each track centre it slides a window along the track and calls it metal where the
metal shot is both bright and grainy (bare field is smooth, poly is darker). Prints the
runs. Meant for wiring bundles on a regular pitch: it tells where each line starts and
stops, which is where to look for a contact or a jog. Short gaps (a poly or diffusion
edge passing under the metal shows as a dark line) are bridged up to --gap pixels.
"""
import argparse
import os
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dir', choices=['h', 'v'])
    ap.add_argument('c', type=int, nargs='+')
    ap.add_argument('--a', type=int, required=True)
    ap.add_argument('--b', type=int, required=True)
    ap.add_argument('--hw', type=int, default=5)
    ap.add_argument('--win', type=int, default=12)
    ap.add_argument('--gap', type=int, default=14)
    ap.add_argument('--bright', type=float, default=150)
    ap.add_argument('--grain', type=float, default=9)
    ap.add_argument('--layer', default='metal')
    a = ap.parse_args()
    arr = np.load(os.path.join(ROOT, 'cache', a.layer + '.npy'), mmap_mode='r')
    for c in a.c:
        if a.dir == 'v':
            s = np.asarray(arr[a.a:a.b, c - a.hw:c + a.hw + 1]).astype(np.float32)
        else:
            s = np.asarray(arr[c - a.hw:c + a.hw + 1, a.a:a.b]).astype(np.float32).transpose(1, 0, 2)
        g = (s[..., 0] + s[..., 1]) / 2          # along, across
        n = g.shape[0]
        on = np.zeros(n, bool)
        for i in range(0, n - a.win):
            w = g[i:i + a.win]
            if w.mean() > a.bright and w.std() > a.grain:
                on[i:i + a.win] = True
        runs = []
        i = 0
        while i < n:
            if on[i]:
                j = i
                while j < n and on[j]:
                    j += 1
                if runs and i - runs[-1][1] <= a.gap:
                    runs[-1][1] = j
                else:
                    runs.append([i, j])
                i = j
            else:
                i += 1
        print(f'{c}: ' + ' '.join(f'{a.a + r[0]}-{a.a + r[1]}' for r in runs if r[1] - r[0] >= 20))


if __name__ == '__main__':
    main()
