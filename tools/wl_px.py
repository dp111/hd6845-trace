#!/usr/bin/env python3
"""Mean colour of small patches in several shots: wl_px.py x,y[,r] ... [--layers a,b]
Prints, per point, the mean RGB over a (2r+1) square (default r=4) in each layer, and the
class the class map gives to the clean-shot value."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view, classmap

layers = ['acid1b', 'metal', 'acid']
pts = []
args = sys.argv[1:]
while args:
    a = args.pop(0)
    if a == '--layers':
        layers = args.pop(0).split(',')
    else:
        v = [int(t) for t in a.split(',')]
        pts.append((v[0], v[1], v[2] if len(v) > 2 else 4))
for x, y, r in pts:
    out = []
    for l in layers:
        rgb = view.raw(l, x - r, y - r, 2 * r + 1, 2 * r + 1).reshape(-1, 3).mean(0)
        s = '%s %3d %3d %3d' % (l, *rgb)
        if l == 'acid1b':
            s += ' [%s]' % classmap.classify(np.tile(rgb, (9, 9, 1)))[4, 4]
        out.append(s)
    print('%5d,%5d  ' % (x, y) + '   '.join(out))
