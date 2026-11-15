#!/usr/bin/env python3
"""Compare copies of a rectangle with their median, block by block, as text.

usage: tools/t.sh rdp3 rdp3_cmp.py x0,y0:x1,y1 --offsets "dx,dy ..." [--layer acid1b]
       [--bs 40] [--thr 80] [--save NAME]

Each copy (the rectangle moved by dx,dy; 0,0 is the master) is nudged onto the master
by up to 6 px, the per-pixel median is taken, and each copy is compared with the median
in blocks of --bs px (normalised cross-correlation x 99, block allowed to slide 5 px).
Prints one map per copy; blocks at or above --thr print as '.', featureless ones as ' '.
--save NAME also writes the median as a composite (cache/comp/NAME_<layer>.npy) for
view.py --comp. Numbers only say where to look; dirt shows up too.
"""
import argparse, json, os, sys
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tracelib
from cellcheck import tmatrix, patch
from composite import nudge

CACHE = os.path.join(tracelib.ROOT, 'cache')
FILES = {'metal': 'metal.npy', 'acid': 'acid_aligned.npy', 'acid1b': 'acid1b.npy', 'metal1': 'metal1.npy'}

ap = argparse.ArgumentParser()
ap.add_argument('bbox'); ap.add_argument('--offsets', required=True)
ap.add_argument('--layer', default='acid1b'); ap.add_argument('--bs', type=int, default=40)
ap.add_argument('--thr', type=int, default=80); ap.add_argument('--save')
a = ap.parse_args()
p, q = a.bbox.split(':')
x0, y0 = map(int, p.split(',')); x1, y1 = map(int, q.split(','))
offs = [tuple(map(float, t.split(','))) for t in a.offsets.split()]
layers = list(FILES) if a.save else [a.layer]
for layer in layers:
    arr = np.load(os.path.join(CACHE, FILES[layer]), mmap_mode='r')
    ref = patch(arr, tmatrix(None, None, 0, (0, 0), *offs[0]), x0, y0, x1, y1)
    stack = [ref]; nud = [(0, 0, 1.0)]
    for o in offs[1:]:
        img, n = nudge(ref, patch(arr, tmatrix(None, None, 0, (0, 0), *o), x0, y0, x1, y1))
        stack.append(img); nud.append(n)
    med = np.median(np.stack(stack), axis=0).astype(np.uint8)
    if a.save:
        os.makedirs(os.path.join(CACHE, 'comp'), exist_ok=True)
        np.save(os.path.join(CACHE, 'comp', f'{a.save}_{layer}.npy'), med)
        with open(os.path.join(CACHE, 'comp', f'{a.save}.json'), 'w') as f:
            json.dump({'x0': x0 + int(offs[0][0]), 'y0': y0 + int(offs[0][1]),
                       'x1': x1 + int(offs[0][0]), 'y1': y1 + int(offs[0][1]), 'n': len(offs)}, f)
    if layer != a.layer:
        continue
    m = med.astype(np.float32).mean(axis=2)
    H, W = m.shape; bs = a.bs
    print(f'layer {layer}; columns start at x {x0}, step {bs}; rows labelled by y (master frame)')
    for o, img, n in zip(offs, stack, nud):
        g = img.astype(np.float32).mean(axis=2)
        bad = 0; lines = []
        for y in range(0, H - bs + 1, bs):
            row = ''
            for x in range(0, W - bs + 1, bs):
                A = m[y:y + bs, x:x + bs]
                if A.std() < 6:
                    row += '   '; continue
                B = g[max(0, y - 5):y + bs + 5, max(0, x - 5):x + bs + 5]
                r = int(cv2.matchTemplate(B, A, cv2.TM_CCOEFF_NORMED).max() * 99)
                if r >= a.thr:
                    row += '  .'
                else:
                    row += '%3d' % max(r, 0); bad += 1
            lines.append('y%5d %s' % (y0 + y, row))
        print(f'--- copy at {o[0]:+.0f},{o[1]:+.0f}  nudge {n[0]},{n[1]}  bad blocks {bad}')
        if bad:
            print('\n'.join(l for l in lines if any(c.isdigit() for c in l[6:])))
