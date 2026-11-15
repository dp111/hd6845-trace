#!/usr/bin/env python3
"""Mean colour and grain of rectangles in all four main shots, for telling layers apart.

usage: bd2_patch.py x0,y0:x1,y1[=name] ...
Prints, per rectangle and per shot (metal, metal1, acid, acid1b): mean R/G/B, and the
standard deviation of (R+G+B)/3 over the rectangle (texture: poly is granular, diffusion
and field are flat). Compare unknown patches with patches of known layers nearby; the
colours drift across the die, so absolute values mean nothing.
"""
import os, sys
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = {'metal': 'metal.npy', 'metal1': 'metal1.npy', 'acid': 'acid_aligned.npy', 'acid1b': 'acid1b.npy'}
A = {l: np.load(os.path.join(ROOT, 'cache', f), mmap_mode='r') for l, f in F.items()}
print('%-26s' % '' + ''.join('%-22s' % l for l in F))
for t in sys.argv[1:]:
    name = ''
    if '=' in t:
        t, name = t.split('=')
    a, b = t.split(':')
    x0, y0 = map(int, a.split(',')); x1, y1 = map(int, b.split(','))
    s = ''
    for l in F:
        p = np.asarray(A[l][y0:y1, x0:x1]).astype(np.float32)
        m = p.reshape(-1, 3).mean(0)
        s += '%3d/%3d/%3d s%4.1f      ' % (m[0], m[1], m[2], p.mean(2).std())
    print('%-26s%s%s' % (t, s, name))
