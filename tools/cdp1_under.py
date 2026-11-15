#!/usr/bin/env python3
"""Which horizontal poly lines pass under a vertical metal rail? (cdp1 helper)

usage: cdp1_under.py Y0 Y1 X [X ...] [--half 12]
       cdp1_under.py --across X0 X1 Y [Y ...] [--half 12]     (vertical lines under a horizontal rail)

For each rail centre it averages the clean shot over +-half across the rail and walks
along it; under metal, poly is salmon (R > 195, G 135-185, B < 128 here), field is pink
(G < 130) and diffusion tan (B > 125, G > 160). Prints the runs of poly and of diffusion.
Only meaningful where metal really covers the band: check the rail's extent first.
"""
import argparse, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view
ap = argparse.ArgumentParser()
ap.add_argument('--across', action='store_true')
ap.add_argument('a', type=int); ap.add_argument('b', type=int)
ap.add_argument('c', type=int, nargs='+'); ap.add_argument('--half', type=int, default=12)
a = ap.parse_args()
for c in a.c:
    if a.across:
        im = view.raw('acid1b', a.a, c - a.half, a.b - a.a, 2 * a.half + 1).astype(np.float32).mean(0)
    else:
        im = view.raw('acid1b', c - a.half, a.a, 2 * a.half + 1, a.b - a.a).astype(np.float32).mean(1)
    cls = []
    for r, g, b in im:
        if r > 195 and 133 <= g <= 186 and b < 128 and r - g > 38:
            cls.append('P')
        elif g > 158 and b > 118 and r - g < 38:
            cls.append('D')
        else:
            cls.append('.')
    out = {'P': [], 'D': []}
    i = 0
    while i < len(cls):
        j = i
        while j < len(cls) and cls[j] == cls[i]:
            j += 1
        if cls[i] in out and j - i >= 5:
            out[cls[i]].append('%d-%d' % (a.a + i, a.a + j - 1))
        i = j
    print('%s %d  poly: %s' % ('y' if a.across else 'x', c, ' '.join(out['P'])))
    if out['D']:
        print('%8s diff: %s' % ('', ' '.join(out['D'])))
