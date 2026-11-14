#!/usr/bin/env python3
"""view.py with an unsharp mask and a contrast stretch, for judging junctions.

usage: tools/t.sh rdp3 rdp3_sharp.py x y w h --scale S --layers a,b [--comp NAME]
       [--shift dx,dy] [--grid N] [--trace] [--amount A] [--sigma G] --out FILE

Same coordinates and layer names as view.py. Sharpening invents nothing: it only makes
the edges that are in the photo easier to see at 3-5x. Always compare with view.py.
"""
import argparse
import os
import sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view  # noqa: E402


def sharp_panel(layer, x, y, w, h, scale, grid, trace, amount, sigma):
    import cv2
    pad = 8
    a = view.raw(layer, x - pad, y - pad, w + 2 * pad, h + 2 * pad).astype(np.float32)
    W, H = round((w + 2 * pad) * scale), round((h + 2 * pad) * scale)
    up = cv2.resize(a, (W, H), interpolation=cv2.INTER_LANCZOS4)
    bl = cv2.GaussianBlur(up, (0, 0), sigma * scale)
    sh = up + amount * (up - bl)
    p = round(pad * scale)
    sh = sh[p:p + round(h * scale), p:p + round(w * scale)]
    lo, hi = np.percentile(sh, 1), np.percentile(sh, 99)
    sh = np.clip((sh - lo) / max(1.0, hi - lo) * 255, 0, 255).astype(np.uint8)
    im = Image.fromarray(sh)
    if trace:
        import tracelib
        im = tracelib.overlay(im, x, y, w, h, scale, only=None, fill=False)
    if grid:
        view.draw_grid(im, x, y, w, h, scale, grid)
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('x', type=int)
    ap.add_argument('y', type=int)
    ap.add_argument('w', type=int)
    ap.add_argument('h', type=int)
    ap.add_argument('--scale', type=float, default=3.0)
    ap.add_argument('--layers', default='acid1b,metal')
    ap.add_argument('--stack', default='h')
    ap.add_argument('--grid', type=int, default=25)
    ap.add_argument('--trace', action='store_true')
    ap.add_argument('--comp', default=None)
    ap.add_argument('--shift', default=None)
    ap.add_argument('--amount', type=float, default=1.5)
    ap.add_argument('--sigma', type=float, default=2.5)
    ap.add_argument('--out', default='sharp.png')
    a = ap.parse_args()
    out = view.scratch_path(a.out)
    if a.comp:
        view.use_comp(a.comp)
    if a.shift:
        view._shift = tuple(int(v) for v in a.shift.split(','))
    panels = [sharp_panel(l, a.x, a.y, a.w, a.h, a.scale, a.grid, a.trace, a.amount, a.sigma)
              for l in a.layers.split(',')]
    gap = 6
    if a.stack == 'h':
        o = Image.new('RGB', (sum(p.size[0] for p in panels) + gap * (len(panels) - 1),
                              max(p.size[1] for p in panels)), (255, 0, 255))
        px = 0
        for p in panels:
            o.paste(p, (px, 0))
            px += p.size[0] + gap
    else:
        o = Image.new('RGB', (max(p.size[0] for p in panels),
                              sum(p.size[1] for p in panels) + gap * (len(panels) - 1)), (255, 0, 255))
        py = 0
        for p in panels:
            o.paste(p, (0, py))
            py += p.size[1] + gap
    os.makedirs(os.path.dirname(out), exist_ok=True)
    o.save(out)
    print(out, o.size)


if __name__ == '__main__':
    main()
