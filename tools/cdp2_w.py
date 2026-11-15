#!/usr/bin/env python3
"""Working view: sharpened panels (rdp3_sharp) with the outline of the metal (cdp2_mo)
drawn in blue on the stripped ones.

usage: cdp2_w.py x y w h [--scale S] [--grid N] [--layers acid,acid1b] [--comp NAME]
                 [--shift dx,dy] [--trace] [--stack h|v] [--nomo] --out FILE

In a median composite the `acid` panel shows poly orange even under metal and the
`acid1b` panel shows diffusion (tan under metal, pink in the open) against field (pink
under metal, khaki in the open); the blue outline says which of the two colour tables
applies. Metal panels get no outline. A viewing aid: the mask breaks up over contacts.
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
import cdp2_mo  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('x', type=int)
    ap.add_argument('y', type=int)
    ap.add_argument('w', type=int)
    ap.add_argument('h', type=int)
    ap.add_argument('--scale', type=float, default=2.75)
    ap.add_argument('--grid', type=int, default=25)
    ap.add_argument('--layers', default='acid,acid1b')
    ap.add_argument('--comp', default=None)
    ap.add_argument('--shift', default=None)
    ap.add_argument('--trace', action='store_true')
    ap.add_argument('--nomo', action='store_true')
    ap.add_argument('--stack', default='h')
    ap.add_argument('--amount', type=float, default=1.5)
    ap.add_argument('--sigma', type=float, default=2.5)
    ap.add_argument('--out', default='w.png')
    a = ap.parse_args()
    if a.comp:
        view.use_comp(a.comp)
    if a.shift:
        view._shift = tuple(int(v) for v in a.shift.split(','))
    mask = cdp2_mo.metal_mask(a.x, a.y, a.w, a.h)
    W, H = round(a.w * a.scale), round(a.h * a.scale)
    big = cv2.resize(mask, (W, H), interpolation=cv2.INTER_NEAREST)
    cs, _ = cv2.findContours(big, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    panels = []
    for l in a.layers.split(','):
        im = rdp3_sharp.sharp_panel(l, a.x, a.y, a.w, a.h, a.scale, 0, a.trace, a.amount, a.sigma)
        arr = np.array(im.convert('RGB'))
        if not a.nomo and not l.startswith('metal'):
            cv2.drawContours(arr, cs, -1, (40, 90, 255), 1)
        im = Image.fromarray(arr)
        if a.grid:
            view.draw_grid(im, a.x, a.y, a.w, a.h, a.scale, a.grid)
        panels.append(im)
    gap = 6
    if a.stack == 'h':
        out = Image.new('RGB', (sum(p.size[0] for p in panels) + gap * (len(panels) - 1), H), (255, 0, 255))
        px = 0
        for p in panels:
            out.paste(p, (px, 0))
            px += p.size[0] + gap
    else:
        out = Image.new('RGB', (W, sum(p.size[1] for p in panels) + gap * (len(panels) - 1)), (255, 0, 255))
        py = 0
        for p in panels:
            out.paste(p, (0, py))
            py += p.size[1] + gap
    f = view.scratch_path(a.out)
    out.save(f)
    print(f, out.size)


if __name__ == '__main__':
    main()
