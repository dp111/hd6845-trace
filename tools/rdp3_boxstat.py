#!/usr/bin/env python3
"""Mean colour (clean shot, and both metal shots) of small boxes, as a table with R-G.

usage: tools/t.sh rdp3 rdp3_boxstat.py [-r 4] LABEL:x,y[:dx,dy;dx,dy;...] ...
Each argument is one class of points: a master point and the offsets of its copies.
Used to compare a doubtful contact with known metal contacts and known buried contacts:
in the clean shot a metal contact on poly is olive (G >= R), a buried contact and
diffusion under metal are tan (R - G about 35-45), poly under metal salmon (R - G > 55).
"""
import sys, os
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = {'acid1b': 'acid1b.npy', 'metal': 'metal.npy', 'metal1': 'metal1.npy', 'acid': 'acid_aligned.npy'}
A = {k: np.load(os.path.join(ROOT, 'cache', v), mmap_mode='r') for k, v in F.items()}
r = 4
args = sys.argv[1:]
if args and args[0] == '-r':
    r = int(args[1]); args = args[2:]
def m(l, x, y):
    return A[l][y - r:y + r + 1, x - r:x + r + 1].reshape(-1, 3).astype(float).mean(0)
print('%-10s %-13s %-22s %-16s %-16s %-16s' % ('class', 'at', 'acid1b  (R-G)', 'acid', 'metal', 'metal1'))
for a in args:
    p = a.split(':')
    lab = p[0]; x, y = map(int, p[1].split(','))
    offs = [(0, 0)]
    if len(p) > 2:
        offs = [tuple(map(int, o.split(','))) for o in p[2].split(';')]
    for dx, dy in offs:
        c = m('acid1b', x + dx, y + dy)
        print('%-10s %6d,%-6d %3d/%3d/%3d (%+4d)   %s' % (lab, x + dx, y + dy, c[0], c[1], c[2], c[0] - c[1],
              '   '.join('%3d/%3d/%3d' % tuple(m(l, x + dx, y + dy)) for l in ('acid', 'metal', 'metal1'))))
