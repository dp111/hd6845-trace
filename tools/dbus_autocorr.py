#!/usr/bin/env python3
"""Vertical autocorrelation of a strip: dbus_autocorr.py x0 x1 y0 y1 [layer]"""
import sys, os
import numpy as np, cv2
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
x0, x1, y0, y1 = map(int, sys.argv[1:5])
layer = sys.argv[5] if len(sys.argv) > 5 else 'acid1b'
f = {'metal': 'metal.npy', 'acid1b': 'acid1b.npy', 'metal1': 'metal1.npy'}[layer]
a = np.load(os.path.join(ROOT, 'cache', f), mmap_mode='r')
g = cv2.cvtColor(np.ascontiguousarray(a[y0:y1, x0:x1]), cv2.COLOR_RGB2GRAY).astype(np.float32)
g = cv2.GaussianBlur(g, (0, 0), 2)
g -= g.mean()
H = g.shape[0]
res = []
for lag in range(100, H // 2, 2):
    A = g[:-lag]; B = g[lag:]
    c = (A * B).sum() / np.sqrt((A * A).sum() * (B * B).sum())
    res.append((c, lag))
res.sort(reverse=True)
seen = []
for c, lag in res:
    if all(abs(lag - s) > 20 for s in seen):
        seen.append(lag)
        print(f'lag {lag:5d}  corr {c:.3f}')
    if len(seen) >= 25:
        break
