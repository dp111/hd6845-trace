#!/usr/bin/env python3
"""Crop a region from a die shot (full-res pixel coords of that image).

usage: crop.py <acid|metal> x y w h out.png [scale] [--grid N]
  x,y   top-left corner in full-resolution pixel coordinates
  w,h   size in full-resolution pixels
  scale output scale factor (default 1.0)
  --grid N  overlay a labelled coordinate grid every N full-res pixels
"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load(layer):
    return np.load(os.path.join(ROOT, 'cache', f'{layer}.npy'), mmap_mode='r')

def crop(layer, x, y, w, h, scale=1.0, grid=0):
    a = load(layer)
    H, W = a.shape[:2]
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W, x + w), min(H, y + h)
    im = Image.fromarray(np.ascontiguousarray(a[y0:y1, x0:x1]))
    if scale != 1.0:
        im = im.resize((max(1, round(im.size[0] * scale)), max(1, round(im.size[1] * scale))),
                       Image.LANCZOS if scale < 1 else Image.BICUBIC)
    if grid:
        d = ImageDraw.Draw(im)
        gx = (x0 // grid + 1) * grid
        while gx < x1:
            px = (gx - x0) * scale
            d.line([(px, 0), (px, im.size[1])], fill=(0, 255, 255), width=1)
            d.text((px + 2, 2), str(gx), fill=(255, 255, 0))
            gx += grid
        gy = (y0 // grid + 1) * grid
        while gy < y1:
            py = (gy - y0) * scale
            d.line([(0, py), (im.size[0], py)], fill=(0, 255, 255), width=1)
            d.text((2, py + 2), str(gy), fill=(255, 255, 0))
            gy += grid
    return im

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    grid = 0
    if '--grid' in sys.argv:
        grid = int(sys.argv[sys.argv.index('--grid') + 1])
        args.remove(str(grid))
    layer, x, y, w, h, out = args[0], int(args[1]), int(args[2]), int(args[3]), int(args[4]), args[5]
    scale = float(args[6]) if len(args) > 6 else 1.0
    crop(layer, x, y, w, h, scale, grid).save(out)
    print(out)
