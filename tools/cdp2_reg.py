#!/usr/bin/env python3
"""Measure the local offset between two shots (default acid1b against metal) in windows.

usage: cdp2_reg.py x y w h [--a metal] [--b acid1b] [--comp NAME] [--shift dx,dy] [--max 14]
Both windows are reduced to "dark line" maps (outlines print dark in every shot) and the
shift of b that best matches a is found by normalised correlation over +-max px.
Prints dx, dy (b is displaced by dx,dy relative to a: a feature at x in a appears at
x+dx in b) and the correlation. In the arrays acid1b is only interpolated; this says
by how much it is off at a given place.
"""
import argparse, os, sys
import numpy as np
import cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view

def dark(a):
    g = cv2.GaussianBlur(a.astype(np.float32).mean(2), (0, 0), 1.2)
    bg = cv2.GaussianBlur(g, (0, 0), 8)
    d = np.clip(bg - g, 0, None)
    return d

ap = argparse.ArgumentParser()
ap.add_argument('x', type=int); ap.add_argument('y', type=int)
ap.add_argument('w', type=int); ap.add_argument('h', type=int)
ap.add_argument('--a', default='metal'); ap.add_argument('--b', default='acid1b')
ap.add_argument('--comp'); ap.add_argument('--shift'); ap.add_argument('--max', type=int, default=14)
a = ap.parse_args()
if a.comp:
    view.use_comp(a.comp)
if a.shift:
    view._shift = tuple(int(v) for v in a.shift.split(','))
m = a.max
A = dark(view.raw(a.a, a.x, a.y, a.w, a.h))
B = dark(view.raw(a.b, a.x - m, a.y - m, a.w + 2 * m, a.h + 2 * m))
r = cv2.matchTemplate(B, A, cv2.TM_CCOEFF_NORMED)
_, mx, _, loc = cv2.minMaxLoc(r)
print(f'{a.b} vs {a.a} at {a.x},{a.y} {a.w}x{a.h}: dx {loc[0]-m:+d} dy {loc[1]-m:+d}  corr {mx:.2f}')
