#!/usr/bin/env python3
"""Print a coarse brightness table of a window (cdp1 helper): rows = y, columns = x bins.
usage: cdp1_tab.py x0 x1 y0 y1 [--offsets "..."] [--layer metal] [--xb 4] [--yb 6] [--chan min|r|g|b|rg]
Median over instances first. Values 0..99 (brightness/2.56)."""
import argparse, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view
ap = argparse.ArgumentParser()
ap.add_argument('x0', type=int); ap.add_argument('x1', type=int)
ap.add_argument('y0', type=int); ap.add_argument('y1', type=int)
ap.add_argument('--offsets', default='0,0')
ap.add_argument('--layer', default='metal')
ap.add_argument('--xb', type=int, default=4)
ap.add_argument('--yb', type=int, default=6)
ap.add_argument('--chan', default='min')
a = ap.parse_args()
offs = [tuple(int(v) for v in o.split(',')) for o in a.offsets.split()]
st = np.stack([view.raw(a.layer, a.x0 + dx, a.y0 + dy, a.x1 - a.x0, a.y1 - a.y0).astype(np.float32) for dx, dy in offs])
m = np.median(st, axis=0)
if a.chan == 'min': b = np.minimum(m[..., 0], m[..., 1])
elif a.chan == 'r': b = m[..., 0]
elif a.chan == 'g': b = m[..., 1]
elif a.chan == 'b': b = m[..., 2]
elif a.chan == 'rg': b = m[..., 0] - m[..., 1] + 128
print('     ' + ' '.join(f'{(a.x0 + x) % 1000:03d}' for x in range(0, b.shape[1], a.xb)))
for y in range(0, b.shape[0], a.yb):
    r = b[y:y + a.yb]
    print(a.y0 + y, ' '.join(f'{int(r[:, x:x + a.xb].mean() / 2.56):3d}' for x in range(0, b.shape[1], a.xb)))
