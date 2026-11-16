#!/usr/bin/env python3
"""Contacts in a crossing field (vertical metal lines over horizontal poly lines).

usage: xfield.py x0 y0 x1 y1 [--thr 28] [--cols x,x,...] [--rows y,y,...]

Finds the metal columns (chip-2 metal shot, column sums) and the poly rows (clean shot:
rows where most of the under-metal pixels are salmon or contact-green), then prints for
every crossing the clean shot's red minus green over a 9 x 9 patch. Poly under metal is
salmon (45-60); a contact hole is dull green-tan (under about 25: marked '#'); in between
is marked '?'. In these fields a tap has NO widened pad and no ring that stands out in the
metal shot among the crossing shadows, so the colour is the only quick test.
Check a '#' at 5x before drawing it.
"""
import argparse
import os
import sys
import numpy as np
import cv2

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view

ap = argparse.ArgumentParser()
ap.add_argument('x0', type=int)
ap.add_argument('y0', type=int)
ap.add_argument('x1', type=int)
ap.add_argument('y1', type=int)
ap.add_argument('--thr', type=float, default=28)
ap.add_argument('--cols', default=None)
ap.add_argument('--rows', default=None)
a = ap.parse_args()
w, h = a.x1 - a.x0, a.y1 - a.y0
m = view.raw('metal', a.x0, a.y0, w, h).astype(np.float32)
c = view.raw('acid1b', a.x0, a.y0, w, h).astype(np.float32)
ism = (m[..., 0] > 177) & (m[..., 1] > 128)
col = cv2.blur(ism.mean(0).reshape(1, -1), (5, 1)).ravel()
cols = []
i = 0
while i < w:
    if col[i] > 0.22:
        j = i
        while j < w and col[j] > 0.22:
            j += 1
        if j - i >= 8:
            cols.append((i + j) // 2)
        i = j
    else:
        i += 1
if a.cols:
    cols = [int(v) - a.x0 for v in a.cols.split(',')]
r, g, b = c[..., 0], c[..., 1], c[..., 2]
polyish = (r > 165) & ((g - b) > 22)          # salmon or contact-green, not pink field
if cols:
    under = np.stack([polyish[:, max(0, x - 5):x + 6].mean(1) for x in cols], 1).mean(1)
else:
    under = polyish.mean(1)
under = cv2.blur(under.reshape(-1, 1), (1, 5)).ravel()
rows = []
i = 0
while i < h:
    if under[i] > 0.35:
        j = i
        while j < h and under[j] > 0.35:
            j += 1
        if j - i >= 8:
            rows.append((i + j) // 2)
        i = j
    else:
        i += 1
if a.rows:
    rows = [int(v) - a.y0 for v in a.rows.split(',')]
d = cv2.blur(r - g, (9, 9))
print('        ' + ' '.join('%5d' % (a.x0 + x) for x in cols))
for y in rows:
    out = []
    for x in cols:
        v = float(d[max(0, y - 2):y + 3, max(0, x - 6):x + 7].min())
        out.append('%3d%s ' % (v, '#' if v < a.thr else ('?' if v < a.thr + 10 else ' ')))
    print('%6d  ' % (a.y0 + y) + ' '.join(out))
