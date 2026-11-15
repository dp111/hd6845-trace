#!/usr/bin/env python3
"""Colours of the sharp median of a repeated cell (cdp1 helper), for measuring junctions.

usage: cdp1_px.py --offsets "0,0 390,0 ..." box x0,y0:x1,y1 [x0,y0:x1,y1 ...]
       cdp1_px.py --offsets "..." row y0 y1 x0 x1 step     profile along x, mean over y0..y1
       cdp1_px.py --offsets "..." col x0 x1 y0 y1 step     profile along y, mean over x0..x1
       cdp1_px.py --offsets "..." map x0 y0 x1 y1 step     text map of colour classes (acid1b)
       [--layers acid1b,acid,metal,metal1] [--each]

Map classes (calibrated in row B of this block, y 3650-3900; a viewing aid):
  D diffusion under metal   F field under metal (pink)   P poly under metal (salmon)
  C poly over a channel under metal (brighter)   g metal contact (greenish)
  o field or diffusion in the open (the two cannot be told apart by colour here)
  p poly in the open   # dark outline

The copies are aligned to a fraction of a pixel and combined by the median exactly as
tools/cdp1_sr.py does (same function), so the numbers are those of its pictures before
sharpening; coordinates are the master's. A single shot is too grainy to profile at
this scale (neighbouring 3 px samples differ by 40 levels inside one poly gate); the
median over three to five copies is not.
Prints mean R/G/B per layer (and the s.d. of the patch for the first layer). --each
prints the first layer for every copy separately instead of the median (integer
offsets only), to see whether one slice differs.
"""
import argparse
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view
import cdp1_sr

UP = 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--offsets', default='0,0')
    ap.add_argument('--layers', default='acid1b,acid,metal')
    ap.add_argument('--each', action='store_true')
    ap.add_argument('mode')
    ap.add_argument('args', nargs='+')
    a = ap.parse_args()
    offs = [tuple(int(v) for v in o.split(',')) for o in a.offsets.split()]
    layers = a.layers.split(',')
    if a.mode == 'box':
        boxes = []
        for t in a.args:
            p, q = t.split(':')
            x0, y0 = map(int, p.split(','))
            x1, y1 = map(int, q.split(','))
            boxes.append((x0, y0, x1, y1))
    elif a.mode == 'row':
        y0, y1, x0, x1, st = map(int, a.args)
        boxes = [(x, y0, x + st, y1) for x in range(x0, x1, st)]
    elif a.mode == 'col':
        x0, x1, y0, y1, st = map(int, a.args)
        boxes = [(x0, y, x1, y + st) for y in range(y0, y1, st)]
    elif a.mode == 'map':
        x0, y0, x1, y1, st = map(int, a.args)
        REF = {'D': (197, 175, 131), 'F': (187, 117, 123), 'P': (207, 150, 110), 'C': (238, 170, 124),
               'g': (160, 163, 100), 'o': (143, 130, 95), 'p': (141, 83, 51), '#': (75, 55, 45)}
        keys = list(REF)
        refs = np.array([REF[k] for k in keys], np.float32)
        med = cdp1_sr.sr('acid1b', x0, y0, x1 - x0, y1 - y0, offs, UP, 'median')
        hdr = '      '
        for cx in range(x0, x1, st):
            hdr += str((cx // 10) % 10) if cx % 50 < st else ('|' if cx % 25 < st else ' ')
        print('acid1b classes, step', st, ' x from', x0, ' (digit = tens digit at multiples of 50, | at 25)')
        print(hdr)
        for cy in range(y0, y1, st):
            row = ''
            for cx in range(x0, x1, st):
                c = med[(cy - y0) * UP:(cy - y0 + st) * UP, (cx - x0) * UP:(cx - x0 + st) * UP].reshape(-1, 3).mean(0)
                row += keys[int(((refs - c) ** 2).sum(1).argmin())]
            print('%5d %s' % (cy, row))
        return
    else:
        sys.exit('mode must be box, row, col or map')
    X0 = min(b[0] for b in boxes) - 30
    Y0 = min(b[1] for b in boxes) - 30
    X1 = max(b[2] for b in boxes) + 30
    Y1 = max(b[3] for b in boxes) + 30

    def patch(img, b, up):
        return img[(b[1] - Y0) * up:(b[3] - Y0) * up, (b[0] - X0) * up:(b[2] - X0) * up].reshape(-1, 3)

    if a.each:
        l = layers[0]
        print('%-22s %s' % ('box', '  '.join('%-11s' % ('%+d,%+d' % o) for o in offs)))
        ims = [view.raw(l, X0 + dx, Y0 + dy, X1 - X0, Y1 - Y0).astype(np.float32) for dx, dy in offs]
        for b in boxes:
            print('%5d,%5d:%5d,%5d  %s' % (b + ('  '.join('%3d/%3d/%3d' % tuple(patch(im, b, 1).mean(0)) for im in ims),)))
        return
    med = {l: cdp1_sr.sr(l, X0, Y0, X1 - X0, Y1 - Y0, offs, UP, 'median') for l in layers}
    print('%-22s %s' % ('box', '  '.join('%-11s' % l for l in layers)) + '  sd(' + layers[0] + ')')
    for b in boxes:
        cols = '  '.join('%3d/%3d/%3d' % tuple(patch(med[l], b, UP).mean(0)) for l in layers)
        sd = patch(med[layers[0]], b, UP).std(0).mean()
        print('%5d,%5d:%5d,%5d  %s  %4.1f' % (b + (cols, sd)))


if __name__ == '__main__':
    main()
