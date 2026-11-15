#!/usr/bin/env python3
"""False-colour class map of the clean shot (acid1b): a reading aid.

usage: classmap.py x y w h [--scale S] [--grid N] [--comp NAME] [--shift dx,dy]
                           [--trace] [--out FILE]

Tan (diffusion) and pink (field under metal) are hard to tell apart by eye in the
clean shot, and so are salmon (poly) and tan. This paints each pixel by class, from the
thresholds of tools/mra_prof.py, with pink told from salmon by green minus blue (calibrated in the mid-right array; the colours
of the clean shot drift across the die, so check a known device before trusting it
elsewhere):

  red      poly where metal was above (salmon)         dark red   poly in the open
  orange   the same, brighter: poly over a channel (in the mid-right array)
  yellow   diffusion where metal was above (tan)       olive      diffusion in the open (mauve)
  white    field where metal was above (pink)          pale green field in the open
  black    dark: an edge line, a contact pit           blue       none of these

The class is taken on a lightly blurred image, so a border is good to about 2 px. An
edge line is 6-8 px wide and separates everything: two patches of one colour either
side of a black line are not shown to be joined, or to be separate.
"""
import argparse
import os
import sys
import numpy as np
import cv2
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view

PAL = {
    'P': (225, 40, 60), 'C': (255, 140, 0), 'p': (140, 20, 20),
    'D': (250, 220, 60), 'd': (150, 140, 40),
    '.': (245, 245, 245), ',': (170, 225, 170),
    '#': (0, 0, 0), '?': (60, 90, 230),
}


def classify(rgb):
    a = cv2.GaussianBlur(rgb.astype(np.float32), (0, 0), 1.0)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    out = np.full(r.shape, '?', dtype='<U1')
    dark = (r < 125) & (g < 95)
    hi = r > 170
    d = r - g
    pink = (g - b) < 18
    out[hi & pink] = '.'
    out[hi & ~pink & (d > 36)] = 'P'
    out[hi & ~pink & (d > 36) & (r >= 226)] = 'C'
    out[hi & ~pink & (d <= 36)] = 'D'
    lo = ~hi & ~dark
    out[lo & (r > 125)] = 'd'
    out[lo & (d > 30)] = 'p'
    out[lo & (g > r + 5)] = ','
    out[dark] = '#'
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('x', type=int)
    ap.add_argument('y', type=int)
    ap.add_argument('w', type=int)
    ap.add_argument('h', type=int)
    ap.add_argument('--scale', type=float, default=4.0)
    ap.add_argument('--grid', type=int, default=50)
    ap.add_argument('--comp', default=None)
    ap.add_argument('--shift', default=None)
    ap.add_argument('--trace', action='store_true')
    ap.add_argument('--out', default='classmap.png')
    a = ap.parse_args()
    if a.comp:
        view.use_comp(a.comp)
    if a.shift:
        view._shift = tuple(int(v) for v in a.shift.split(','))
    rgb = view.raw('acid1b', a.x, a.y, a.w, a.h)
    c = classify(rgb)
    img = np.zeros(rgb.shape, np.uint8)
    for k, col in PAL.items():
        img[c == k] = col
    im = Image.fromarray(img).resize((round(a.w * a.scale), round(a.h * a.scale)), Image.NEAREST)
    if a.trace:
        import tracelib
        im = tracelib.overlay(im, a.x, a.y, a.w, a.h, a.scale, fill=False)
    if a.grid:
        view.draw_grid(im, a.x, a.y, a.w, a.h, a.scale, a.grid)
    out = view.scratch_path(a.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out)
    print(out, im.size)


if __name__ == '__main__':
    main()
