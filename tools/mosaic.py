#!/usr/bin/env python3
"""Side-by-side panels of the same rectangle at several offsets (to compare repeats).

usage: mosaic.py x y w h --offsets "dx,dy dx,dy ..." [--scale S] [--layer L] [--grid N] --out NAME
Grid labels are those of the master (offset 0,0).
"""
import argparse, os, sys
import numpy as np, cv2
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = {'metal': 'metal.npy', 'acid1b': 'acid1b.npy', 'metal1': 'metal1.npy', 'acid': 'acid_aligned.npy'}
ap = argparse.ArgumentParser()
ap.add_argument('x', type=int); ap.add_argument('y', type=int)
ap.add_argument('w', type=int); ap.add_argument('h', type=int)
ap.add_argument('--offsets', required=True)
ap.add_argument('--scale', type=float, default=1.0)
ap.add_argument('--layer', default='acid1b')
ap.add_argument('--grid', type=int, default=0)
ap.add_argument('--out', required=True)
a = ap.parse_args()
arr = np.load(os.path.join(ROOT, 'cache', F[a.layer]), mmap_mode='r')
panels = []
for off in a.offsets.split():
    dx, dy = map(int, off.split(','))
    p = np.ascontiguousarray(arr[a.y + dy:a.y + dy + a.h, a.x + dx:a.x + dx + a.w])
    p = cv2.resize(p, (int(a.w * a.scale), int(a.h * a.scale)), interpolation=cv2.INTER_AREA if a.scale < 1 else cv2.INTER_CUBIC)
    p = cv2.cvtColor(p, cv2.COLOR_RGB2BGR)
    if a.grid:
        g = a.grid
        for gx in range((a.x // g + 1) * g, a.x + a.w, g):
            X = int((gx - a.x) * a.scale); cv2.line(p, (X, 0), (X, p.shape[0]), (255, 255, 0), 1)
            cv2.putText(p, str(gx), (X + 2, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.33, (0, 255, 255), 1)
        for gy in range((a.y // g + 1) * g, a.y + a.h, g):
            Y = int((gy - a.y) * a.scale); cv2.line(p, (0, Y), (p.shape[1], Y), (255, 255, 0), 1)
            cv2.putText(p, str(gy), (2, Y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.33, (0, 255, 255), 1)
    cv2.putText(p, off, (4, p.shape[0] - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
    panels.append(p)
    panels.append(np.full((p.shape[0], 4, 3), (255, 0, 255), np.uint8))
img = np.hstack(panels[:-1])
d = os.environ.get('HD_SCRATCH') or os.path.join(ROOT, 'cache', 'scratch')
if not os.path.isabs(d): d = os.path.join(ROOT, d)
out = a.out if os.path.dirname(a.out) else os.path.join(d, a.out)
cv2.imwrite(out, img)
print(out, img.shape[1], img.shape[0])
