#!/usr/bin/env python3
"""T7 of the comparator XOR: is its strip diffusion? Per slice, R-G of the strip left of
the q poly against a field reference and a diffusion reference of the same cell, in the
chip-2 stripped shot, the chip-2 metal shot (the area is not under metal) and the clean
shot. usage: tools/t.sh rdp3 rdp3_t7.py
Points (master = slice s2 of band A): strip 14845,12147; field 14868,12064 and
14850,12180; diffusion 14839,12003 (node x, left of G1). Box 9x9 (strip: 21x13)."""
import os, numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = {'acid': 'acid_aligned.npy', 'metal': 'metal.npy', 'acid1b': 'acid1b.npy'}
A = {k: np.load(os.path.join(ROOT, 'cache', v), mmap_mode='r') for k, v in F.items()}
def rg(l, x, y, rx=4, ry=4):
    c = A[l][y - ry:y + ry + 1, x - rx:x + rx + 1].reshape(-1, 3).astype(float).mean(0)
    return c[0] - c[1]
offs = [(-782, 0), (-391, 0), (0, 0), (390, 0), (780, -1), (1170, -1), (1560, -1), (1951, -1)]
print('slice      | chip-2 stripped: strip field field diff | chip-2 metal: strip field field diff | clean: strip field field diff')
tot = {}
for band, dyb in (('A', 0), ('B', -846)):
    for k, (dx, dy) in enumerate(offs):
        row = []
        for l in ('acid', 'metal', 'acid1b'):
            v = [rg(l, 14845 + dx, 12147 + dy + dyb, 10, 6), rg(l, 14868 + dx, 12064 + dy + dyb),
                 rg(l, 14850 + dx, 12180 + dy + dyb), rg(l, 14839 + dx, 12003 + dy + dyb)]
            row.append(v); tot.setdefault(l, []).append(v)
        print('band %s s%d | ' % (band, k) + ' | '.join('  '.join('%+4d' % t for t in v) for v in row))
for l in tot:
    m = np.array(tot[l]); print('%-7s mean %s   sd %s' % (l, m.mean(0).round(1), m.std(0).round(1)))
