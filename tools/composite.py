#!/usr/bin/env python3
"""Median picture of a repeated cell, to see through dirt and etch residue.

usage: composite.py NAME x0,y0:x1,y1 (--cell CELL | --offsets "dx,dy dx,dy ...")

Takes the rectangle (metal-shot pixels, in the master's frame) at every instance,
brings each patch into the master's orientation and takes the per-pixel median over
the instances, for both shots. Residue, debris and interference fringes sit in
different places on each copy, so they drop out; the layout itself stays. Each patch
is first nudged by up to a few pixels to line up with the master.

Writes cache/comp/NAME_metal.npy, NAME_acid.npy and NAME.json (the rectangle).
View with:  view.py x y w h --comp NAME ...   (coordinates in the master's frame)

With --cell the instances are the @inst lines of that trace cell plus the master.
"""
import argparse
import json
import os
import sys
import numpy as np
import cv2

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tracelib
from cellcheck import tmatrix, patch

ROOT = tracelib.ROOT
CACHE = os.path.join(ROOT, 'cache')


def nudge(ref, img, maxshift=6):
    """Shift img by whole pixels to best match ref (grey, blurred)."""
    a = cv2.GaussianBlur(cv2.cvtColor(ref, cv2.COLOR_RGB2GRAY).astype(np.float32), (0, 0), 2)
    b = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY).astype(np.float32), (0, 0), 2)
    m = maxshift
    res = cv2.matchTemplate(b, a[m:-m, m:-m], cv2.TM_CCOEFF_NORMED)
    _, score, _, loc = cv2.minMaxLoc(res)
    dx, dy = loc[0] - m, loc[1] - m
    M = np.float32([[1, 0, -dx], [0, 1, -dy]])
    return cv2.warpAffine(img, M, (img.shape[1], img.shape[0])), (dx, dy, score)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('name')
    ap.add_argument('bbox')
    ap.add_argument('--cell')
    ap.add_argument('--offsets')
    a = ap.parse_args()
    p, q = a.bbox.split(':')
    x0, y0 = map(int, p.split(','))
    x1, y1 = map(int, q.split(','))
    Ts = [np.eye(3)]
    if a.cell:
        tr = tracelib.load()
        for name_, dx, dy, mx, my, tag, src, rot, o in tr.insts:
            if name_ == a.cell:
                Ts.append(tmatrix(mx, my, rot, o, dx, dy))
    else:
        for t in a.offsets.split():
            dx, dy = map(float, t.split(','))
            if dx or dy:
                Ts.append(tmatrix(None, None, 0, (0, 0), dx, dy))
    os.makedirs(os.path.join(CACHE, 'comp'), exist_ok=True)
    for layer, fname in (('metal', 'metal.npy'), ('acid', 'acid_aligned.npy')):
        arr = np.load(os.path.join(CACHE, fname), mmap_mode='r')
        ref = patch(arr, Ts[0], x0, y0, x1, y1)
        stack = [ref]
        for T in Ts[1:]:
            img, (dx, dy, s) = nudge(ref, patch(arr, T, x0, y0, x1, y1))
            stack.append(img)
        med = np.median(np.stack(stack), axis=0).astype(np.uint8)
        np.save(os.path.join(CACHE, 'comp', f'{a.name}_{layer}.npy'), med)
    with open(os.path.join(CACHE, 'comp', f'{a.name}.json'), 'w') as f:
        json.dump({'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1, 'n': len(Ts)}, f)
    print(f'{a.name}: median of {len(Ts)} instances, {x1 - x0} x {y1 - y0} px')


if __name__ == '__main__':
    main()
