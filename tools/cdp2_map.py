#!/usr/bin/env python3
"""Text map of a region: colour class of the clean stripped shot, and where the metal is.
usage: cdp2_map.py x y w h [--step N] [--comp NAME] [--shift dx,dy] [--what acid|metal|both]
Classes (calibrated in row A of the central datapath, a viewing aid, not a measurement):
  P poly under metal   p poly in the open   D diffusion under metal   . field under metal
  ' ' field in the open   # dark line   g green (open diffusion or gap rim)
Metal map: M metal, m probably, - none."""
import sys, os, argparse
import numpy as np
import cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view
REF = {'P': (221, 164, 119), 'D': (194, 174, 130), '.': (195, 117, 126),
       ' ': (157, 138, 100), 'p': (136, 86, 60), '#': (70, 50, 40), 'g': (125, 185, 82),
       'k': (100, 98, 58)}
ap = argparse.ArgumentParser()
ap.add_argument('x', type=int); ap.add_argument('y', type=int)
ap.add_argument('w', type=int); ap.add_argument('h', type=int)
ap.add_argument('--step', type=int, default=5)
ap.add_argument('--comp'); ap.add_argument('--shift'); ap.add_argument('--what', default='both')
a = ap.parse_args()
if a.comp:
    view.use_comp(a.comp)
if a.shift:
    view._shift = tuple(int(v) for v in a.shift.split(','))
s = a.step
ac = view.raw('acid1b', a.x, a.y, a.w, a.h).astype(np.float32)
me = cv2.GaussianBlur(view.raw('metal', a.x, a.y, a.w, a.h).astype(np.float32), (0, 0), 1.5)
keys = list(REF)
refs = np.array([REF[k] for k in keys], np.float32)
def header():
    line = '      '
    for cx in range(a.x, a.x + a.w, s):
        line += str((cx // 10) % 10) if cx % 50 == 0 else ('|' if cx % 25 == 0 else ' ')
    return line
if a.what in ('acid', 'both'):
    print('acid1b classes, step', s, ' x from', a.x, '(digit = tens digit at multiples of 50)')
    print(header())
    for cy in range(a.y, a.y + a.h, s):
        row = ''
        for cx in range(a.x, a.x + a.w, s):
            c = ac[cy - a.y:cy - a.y + s, cx - a.x:cx - a.x + s].reshape(-1, 3).mean(0)
            d = ((refs - c) ** 2).sum(1)
            row += keys[int(d.argmin())]
        print(f'{cy:5d} {row}')
if a.what in ('metal', 'both'):
    print('metal, step', s)
    print(header())
    for cy in range(a.y, a.y + a.h, s):
        row = ''
        for cx in range(a.x, a.x + a.w, s):
            c = me[cy - a.y:cy - a.y + s, cx - a.x:cx - a.x + s].reshape(-1, 3).mean(0)
            row += 'M' if (c[0] > 186 and c[1] > 148) else ('m' if c[0] > 176 and c[1] > 140 else '-')
        print(f'{cy:5d} {row}')
