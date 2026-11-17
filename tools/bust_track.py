#!/usr/bin/env python3
"""Track horizontal poly lines across an open field in the clean shot (acid1b).

usage: bust_track.py X0 X1 Y [Y ...] [--step 2] [--win 8]
For each start y at x X0, walks east in --step px; at each x takes the poly rows
(clean shot: red > 150 and red - green > 15, i.e. orange poly, not the green field) and
moves to the centre of the poly run nearest the current y within --win px. Prints, per
line, the y every 10 px and the points where the line bends (a run of y change), as a
trace path. Only for poly in the open: under metal the colours are different.
"""
import argparse, os
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = np.load(os.path.join(ROOT, 'cache', 'acid1b.npy'), mmap_mode='r')
ap = argparse.ArgumentParser()
ap.add_argument('x0', type=int); ap.add_argument('x1', type=int); ap.add_argument('ys', type=int, nargs='+')
ap.add_argument('--step', type=int, default=2); ap.add_argument('--win', type=int, default=8)
a = ap.parse_args()
for y0 in a.ys:
    y = float(y0); pts = []; lost = None
    for x in range(a.x0, a.x1 + 1, a.step):
        col = C[int(y) - 30:int(y) + 31, x - 1:x + 2].astype(int).mean(1)
        m = (col[:, 0] > 150) & (col[:, 0] - col[:, 1] > 15)
        runs = []; on = None
        for i, b in enumerate(m):
            if b and on is None: on = i
            if (not b or i == len(m) - 1) and on is not None:
                e = i if not b else i + 1
                if e - on >= 6: runs.append((on + e - 1) / 2 + int(y) - 30)
                on = None
        near = [r for r in runs if abs(r - y) <= a.win]
        if not near:
            lost = x; break
        y = min(near, key=lambda r: abs(r - y))
        pts.append((x, y))
    # bends: keep points where the slope changes
    path = [pts[0]]
    for i in range(1, len(pts) - 1):
        d1 = pts[i][1] - pts[i - 1][1]; d2 = pts[i + 1][1] - pts[i][1]
        if (abs(d1) < 0.6) != (abs(d2) < 0.6):
            path.append(pts[i])
    path.append(pts[-1])
    s = ' '.join('%d,%d' % (px, round(py)) for px, py in path)
    print('y0 %d: %s%s' % (y0, s, ('   LOST at x %d' % lost) if lost else ''))
