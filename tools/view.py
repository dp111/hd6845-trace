#!/usr/bin/env python3
"""Render a view of the die in metal-shot coordinates.

usage: view.py x y w h [options]
  x y w h        region in metal-shot pixels (top-left corner and size)
  --scale S      output scale (default 1)
  --layers L     comma list from: metal, acid, blend   (default metal,acid)
  --stack v|h    stack the layer panels vertically or horizontally (default h)
  --grid N       draw a labelled coordinate grid every N pixels
  --trace        overlay the trace geometry (all files in trace/)
  --only LAYERS  with --trace: restrict to these trace layers, e.g. M,P,D,C
  --nofill       with --trace: outlines only
  --comp NAME    show the median composite NAME (tools/composite.py) instead of the
                 die itself; coordinates are still those of the master
  --shift dx,dy  show the die at (x+dx, y+dy) but label the grid as x, y: looks at
                 another instance of a cell in the master's coordinates
  --out FILE     output png (default: scratch/view.png under cache/)

The acid panel uses cache/acid_aligned.npy, so both panels share coordinates.
"""
import argparse
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, 'cache')
_arr = {}
_comp = None      # (metal array, acid array, x0, y0) when --comp is in use
_shift = (0, 0)   # --shift


def use_comp(name):
    global _comp
    import json
    d = os.path.join(CACHE, 'comp')
    j = json.load(open(os.path.join(d, name + '.json')))
    _comp = (np.load(os.path.join(d, name + '_metal.npy')),
             np.load(os.path.join(d, name + '_acid.npy')), j['x0'], j['y0'])


def arr(layer):
    if layer not in _arr:
        name = {'metal': 'metal.npy', 'acid': 'acid_aligned.npy'}[layer]
        _arr[layer] = np.load(os.path.join(CACHE, name), mmap_mode='r')
    return _arr[layer]


def raw(layer, x, y, w, h):
    """RGB uint8 array of the region, zero-padded outside the image."""
    if layer == 'blend':
        return ((raw('metal', x, y, w, h).astype(np.uint16) +
                 raw('acid', x, y, w, h)) // 2).astype(np.uint8)
    if _comp is not None:
        a = _comp[0] if layer == 'metal' else _comp[1]
        ox, oy = _comp[2], _comp[3]
    else:
        a = arr(layer)
        ox, oy = -_shift[0], -_shift[1]
    H, W = a.shape[:2]
    out = np.zeros((h, w, 3), np.uint8)
    x0, y0, x1, y1 = max(ox, x), max(oy, y), min(ox + W, x + w), min(oy + H, y + h)
    if x1 > x0 and y1 > y0:
        out[y0 - y:y1 - y, x0 - x:x1 - x] = a[y0 - oy:y1 - oy, x0 - ox:x1 - ox]
    return out


def font(size=11):
    for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
              '/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf'):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def draw_grid(im, x, y, w, h, scale, step):
    d = ImageDraw.Draw(im)
    f = font(11)
    gx = (x // step + 1) * step
    while gx < x + w:
        px = (gx - x) * scale
        d.line([(px, 0), (px, im.size[1])], fill=(0, 255, 255), width=1)
        d.text((px + 2, 1), str(gx), fill=(255, 255, 0), font=f,
               stroke_width=2, stroke_fill=(0, 0, 0))
        gx += step
    gy = (y // step + 1) * step
    while gy < y + h:
        py = (gy - y) * scale
        d.line([(0, py), (im.size[0], py)], fill=(0, 255, 255), width=1)
        d.text((2, py + 1), str(gy), fill=(255, 255, 0), font=f,
               stroke_width=2, stroke_fill=(0, 0, 0))
        gy += step


def panel(layer, x, y, w, h, scale=1.0, grid=0, trace=False, only=None, fill=True):
    im = Image.fromarray(raw(layer, x, y, w, h))
    if scale != 1.0:
        im = im.resize((max(1, round(w * scale)), max(1, round(h * scale))),
                       Image.LANCZOS if scale < 1 else Image.BICUBIC)
    if trace:
        sys.path.insert(0, os.path.join(ROOT, 'tools'))
        import tracelib
        im = tracelib.overlay(im, x, y, w, h, scale, only=only, fill=fill)
    if grid:
        draw_grid(im, x, y, w, h, scale, grid)
    return im


def render(x, y, w, h, scale=1.0, layers=('metal', 'acid'), stack='h', grid=0,
           trace=False, only=None, fill=True):
    panels = [panel(l, x, y, w, h, scale, grid, trace, only, fill) for l in layers]
    gap = 6
    if stack == 'h':
        W = sum(p.size[0] for p in panels) + gap * (len(panels) - 1)
        Hh = max(p.size[1] for p in panels)
        out = Image.new('RGB', (W, Hh), (255, 0, 255))
        px = 0
        for p in panels:
            out.paste(p, (px, 0))
            px += p.size[0] + gap
    else:
        W = max(p.size[0] for p in panels)
        Hh = sum(p.size[1] for p in panels) + gap * (len(panels) - 1)
        out = Image.new('RGB', (W, Hh), (255, 0, 255))
        py = 0
        for p in panels:
            out.paste(p, (0, py))
            py += p.size[1] + gap
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('x', type=int)
    ap.add_argument('y', type=int)
    ap.add_argument('w', type=int)
    ap.add_argument('h', type=int)
    ap.add_argument('--scale', type=float, default=1.0)
    ap.add_argument('--layers', default='metal,acid')
    ap.add_argument('--stack', default='h')
    ap.add_argument('--grid', type=int, default=0)
    ap.add_argument('--trace', action='store_true')
    ap.add_argument('--only', default=None)
    ap.add_argument('--nofill', action='store_true')
    ap.add_argument('--comp', default=None)
    ap.add_argument('--shift', default=None)
    ap.add_argument('--out', default=os.path.join(CACHE, 'scratch', 'view.png'))
    a = ap.parse_args()
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    if a.comp:
        use_comp(a.comp)
    if a.shift:
        global _shift
        _shift = tuple(int(v) for v in a.shift.split(','))
    im = render(a.x, a.y, a.w, a.h, a.scale, a.layers.split(','), a.stack, a.grid,
                a.trace, a.only.split(',') if a.only else None, not a.nofill)
    im.save(a.out)
    print(a.out, im.size)


if __name__ == '__main__':
    main()
