#!/usr/bin/env python3
"""False-colour class map of the clean stripped shot where metal protected it.

usage: cdp2_cls.py x y w h [--scale S] [--grid N] [--comp NAME] [--shift dx,dy]
                   [--trace] [--left metal|acid1b|none] --out FILE

Left panel: the metal shot (sharpened). Right panel: acid1b, with every pixel that lay
under metal (either chip's metal, grown by the 10 px the metal protects) repainted by
its nearest reference colour:
    red     poly over a channel (bright salmon, 240/172/124)
    orange  poly over field (salmon, 221/164/120)
    green   diffusion (tan, 196/178/134)
    blue    field (pink, 195/117/126)
    yellow  contact (greenish speckle, 150/150/90)
    black   dark outline
Pixels in the open are repainted in pale colours from a second table (measured in the
open): brown = poly (low blue, 160/105/60), pale green = diffusion (mauve-pink,
172/124/106), grey = field (khaki, 150/142/96), dark grey = green rim, black = outline.
The open classes are much less reliable than the protected ones (narrow open features
show only their outlines): check against the metal shot, where open poly is orange-brown.
--photo keeps the photo (dimmed) in the open instead.
References measured in rows A and B of cdp2 (y 6000-7500); a viewing aid, not a
measurement. Check a deciding junction with larr_px.py / cdp2_pt.py.
"""
import argparse
import os
import sys
import numpy as np
import cv2
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view  # noqa: E402
import rdp3_sharp  # noqa: E402

REF = [((240, 172, 124), (255, 40, 40)),
       ((221, 164, 120), (255, 165, 30)),
       ((196, 178, 134), (40, 200, 80)),
       ((195, 117, 126), (70, 90, 200)),
       ((150, 150, 90), (255, 255, 0)),
       ((90, 60, 50), (0, 0, 0)),
       ((140, 90, 80), (0, 0, 0))]


OPEN = [((160, 105, 60), (150, 75, 0)),
        ((140, 88, 58), (150, 75, 0)),
        ((172, 124, 106), (170, 255, 170)),
        ((186, 121, 107), (170, 255, 170)),
        ((150, 142, 96), (150, 150, 150)),
        ((115, 140, 88), (90, 90, 90)),
        ((120, 180, 85), (90, 90, 90)),
        ((70, 50, 40), (0, 0, 0))]


def protected(x, y, w, h, grow=9):
    pad = 16
    m = np.zeros((h + 2 * pad, w + 2 * pad), np.uint8)
    for l in ('metal', 'metal1'):
        a = view.raw(l, x - pad, y - pad, w + 2 * pad, h + 2 * pad).astype(np.float32)
        b = cv2.GaussianBlur(a, (0, 0), 2.0)
        m |= ((b[..., 0] > 180) & (b[..., 1] > 143)).astype(np.uint8)
    se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, se)
    se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * grow + 1, 2 * grow + 1))
    m = cv2.dilate(m, se)
    return m[pad:-pad, pad:-pad].astype(bool)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('x', type=int)
    ap.add_argument('y', type=int)
    ap.add_argument('w', type=int)
    ap.add_argument('h', type=int)
    ap.add_argument('--scale', type=float, default=2.75)
    ap.add_argument('--grid', type=int, default=25)
    ap.add_argument('--comp', default=None)
    ap.add_argument('--shift', default=None)
    ap.add_argument('--trace', action='store_true')
    ap.add_argument('--left', default='metal')
    ap.add_argument('--grow', type=int, default=9)
    ap.add_argument('--photo', action='store_true')
    ap.add_argument('--out', default='cls.png')
    a = ap.parse_args()
    if a.comp:
        view.use_comp(a.comp)
    if a.shift:
        view._shift = tuple(int(v) for v in a.shift.split(','))
    x, y, w, h = a.x, a.y, a.w, a.h
    prot = protected(x, y, w, h, a.grow)
    ac = cv2.GaussianBlur(view.raw('acid1b', x, y, w, h).astype(np.float32), (0, 0), 1.0)
    refs = np.array([r for r, _ in REF], np.float32)
    cols = np.array([c for _, c in REF], np.uint8)
    d = ((ac[:, :, None, :] - refs[None, None]) ** 2).sum(-1)
    k = d.argmin(-1)
    if a.photo:
        out = (ac * 0.75).clip(0, 255).astype(np.uint8)
    else:
        orefs = np.array([r for r, _ in OPEN], np.float32)
        ocols = np.array([c for _, c in OPEN], np.uint8)
        ko = ((ac[:, :, None, :] - orefs[None, None]) ** 2).sum(-1).argmin(-1)
        out = ocols[ko]
    out[prot] = cols[k][prot]
    edge = cv2.morphologyEx(prot.astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)).astype(bool)
    out[edge] = (255, 255, 255)
    W, H = round(w * a.scale), round(h * a.scale)
    im = Image.fromarray(cv2.resize(out, (W, H), interpolation=cv2.INTER_NEAREST))
    if a.trace:
        import tracelib
        im = tracelib.overlay(im, x, y, w, h, a.scale, only=None, fill=False)
    if a.grid:
        view.draw_grid(im, x, y, w, h, a.scale, a.grid)
    panels = [im]
    if a.left != 'none':
        panels.insert(0, rdp3_sharp.sharp_panel(a.left, x, y, w, h, a.scale, a.grid, a.trace, 1.5, 2.5))
    o = Image.new('RGB', (sum(p.size[0] for p in panels) + 6 * (len(panels) - 1), H), (255, 0, 255))
    px = 0
    for p in panels:
        o.paste(p, (px, 0))
        px += p.size[0] + 6
    f = view.scratch_path(a.out)
    o.save(f)
    print(f, o.size)


if __name__ == '__main__':
    main()
