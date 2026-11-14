#!/usr/bin/env python3
"""Colour of the clean stripped shot (and of the metal shot) at given points, with the
nearest reference class.  usage: cdp2_pt.py [--comp NAME] [--shift dx,dy] x,y x,y ...
Classes are calibrated in row A of the central datapath (y 6000-6300); a viewing aid."""
import sys, os, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view
REF = {'poly_um': (221, 164, 121), 'diff_um': (191, 164, 124), 'field_um': (195, 117, 126),
       'field_open': (157, 137, 101), 'poly_open': (136, 86, 60), 'dark': (70, 50, 40),
       'green': (120, 190, 80)}
ap = argparse.ArgumentParser()
ap.add_argument('pts', nargs='+')
ap.add_argument('--comp')
ap.add_argument('--shift')
ap.add_argument('-r', type=int, default=3)
a = ap.parse_args()
if a.comp:
    view.use_comp(a.comp)
if a.shift:
    view._shift = tuple(int(v) for v in a.shift.split(','))
r = a.r
for p in a.pts:
    x, y = (int(v) for v in p.split(','))
    ac = view.raw('acid1b', x - r, y - r, 2 * r + 1, 2 * r + 1).reshape(-1, 3).astype(float)
    me = view.raw('metal', x - r, y - r, 2 * r + 1, 2 * r + 1).reshape(-1, 3).astype(float)
    c = ac.mean(0)
    best = min(REF, key=lambda k: sum((c[i] - REF[k][i]) ** 2 for i in range(3)))
    mm = me.mean(0)
    metal = 'METAL' if mm[0] > 186 and mm[1] > 148 else ('metal?' if mm[0] > 178 else '-')
    print(f'{x},{y}  acid1b {c.round(0)} sd {ac.std(0).mean():.0f}  {best:10s}  metal {mm.round(0)} {metal}')
