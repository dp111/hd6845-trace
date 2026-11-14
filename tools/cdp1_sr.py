#!/usr/bin/env python3
"""Super-resolved median of a repeated cell (cdp1 helper).

usage: cdp1_sr.py x y w h --offsets "0,0 391,0 ..." [--layers metal,acid1b] [--up 3]
                  [--grid 25] [--sharp 1.0] [--out NAME.png] [--stat median|mean]

Each instance's patch (x+dx, y+dy, w, h) is upsampled, aligned to the first one to a
fraction of a pixel (phase correlation on brightness) and the stack is combined per
pixel. The result is sharpened a little and written with a grid labelled in the
master's coordinates, panels side by side (two per row).
"""
import argparse
import os
import sys
import numpy as np
import cv2
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view


def sr(layer, x, y, w, h, offs, up, stat):
    pad = 6
    ref = None
    stack = []
    for dx, dy in offs:
        a = view.raw(layer, x + dx - pad, y + dy - pad, w + 2 * pad, h + 2 * pad).astype(np.float32)
        a = cv2.resize(a, None, fx=up, fy=up, interpolation=cv2.INTER_CUBIC)
        g = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)
        g = cv2.GaussianBlur(g, (0, 0), 1.0)
        if ref is None:
            ref = g
        else:
            (sx, sy), _ = cv2.phaseCorrelate(ref, g, cv2.createHanningWindow(g.shape[::-1], cv2.CV_32F))
            if abs(sx) < 8 * up and abs(sy) < 8 * up:
                M = np.float32([[1, 0, -sx], [0, 1, -sy]])
                a = cv2.warpAffine(a, M, (a.shape[1], a.shape[0]), flags=cv2.INTER_CUBIC,
                                   borderMode=cv2.BORDER_REPLICATE)
        stack.append(a)
    st = np.stack(stack)
    out = np.median(st, axis=0) if stat == 'median' else st.mean(axis=0)
    p = pad * up
    return out[p:-p, p:-p]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('x', type=int)
    ap.add_argument('y', type=int)
    ap.add_argument('w', type=int)
    ap.add_argument('h', type=int)
    ap.add_argument('--offsets', required=True)
    ap.add_argument('--layers', default='metal,acid1b')
    ap.add_argument('--up', type=int, default=3)
    ap.add_argument('--grid', type=int, default=25)
    ap.add_argument('--sharp', type=float, default=1.0)
    ap.add_argument('--stat', default='median')
    ap.add_argument('--out', default='sr.png')
    a = ap.parse_args()
    offs = [tuple(int(v) for v in o.split(',')) for o in a.offsets.split()]
    ims = []
    for l in a.layers.split(','):
        o = sr(l, a.x, a.y, a.w, a.h, offs, a.up, a.stat)
        if a.sharp > 0:
            bl = cv2.GaussianBlur(o, (0, 0), 1.2 * a.up)
            o = o + a.sharp * (o - bl)
        im = Image.fromarray(np.clip(o, 0, 255).astype(np.uint8))
        if a.grid:
            view.draw_grid(im, a.x, a.y, a.w, a.h, a.up, a.grid)
        d = ImageDraw.Draw(im)
        d.text((48, 16), l, fill=(255, 255, 0), font=view.font(14), stroke_width=3, stroke_fill=(0, 0, 0))
        ims.append(im)
    W, H = ims[0].size
    cols = 2 if len(ims) > 1 else 1
    rows = (len(ims) + 1) // 2
    o = Image.new('RGB', (W * cols + 6 * (cols - 1), H * rows + 6 * (rows - 1)), (255, 0, 255))
    for i, im in enumerate(ims):
        o.paste(im, ((i % 2) * (W + 6), (i // 2) * (H + 6)))
    out = view.scratch_path(a.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    o.save(out)
    print(out, o.size)


if __name__ == '__main__':
    main()
