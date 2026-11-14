#!/usr/bin/env python3
"""False-colour class map of a composite, from the colour of the chip-2 stripped shot.

usage: larr_cls.py COMP x y w h [--scale S] [--grid N] [--out FILE] [--layer acid|metal]

In the median composite the stripped shot has stable colours: field R/G about 1.03,
diffusion about 1.16, poly about 1.28 with a low blue. The map paints
  field grey, diffusion green, poly red, dark edges black, very bright (contact ghost) white.
A reading aid: borders are a few pixels uncertain and contacts/fringes fool it.
"""
import argparse, json, os, sys
import numpy as np, cv2
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('comp'); ap.add_argument('x', type=int); ap.add_argument('y', type=int)
ap.add_argument('w', type=int); ap.add_argument('h', type=int)
ap.add_argument('--scale', type=float, default=3); ap.add_argument('--grid', type=int, default=50)
ap.add_argument('--out', default='cls.png'); ap.add_argument('--layer', default='acid')
a = ap.parse_args()
d = os.path.join(ROOT, 'cache', 'comp')
j = json.load(open(os.path.join(d, a.comp + '.json')))
b = np.load(os.path.join(d, f'{a.comp}_{a.layer}.npy'))[a.y - j['y0']:a.y - j['y0'] + a.h, a.x - j['x0']:a.x - j['x0'] + a.w].astype(np.float32)
b = cv2.GaussianBlur(b, (0, 0), 1.0)
R, G, B = b[:, :, 0], b[:, :, 1], b[:, :, 2]
lum = (R + G + B) / 3
rg = R / np.maximum(G, 1)
out = np.zeros(b.shape, np.uint8)
out[:] = (150, 150, 150)
out[(rg > 1.095)] = (60, 200, 80)
out[(rg > 1.225)] = (230, 70, 50)
out[lum < 95] = (0, 0, 0)
out[lum > 175] = (255, 255, 255)
# keep some of the photo's shading
shade = np.clip(lum / 130.0, 0.55, 1.15)[:, :, None]
out = np.clip(out * shade, 0, 255).astype(np.uint8)
S = a.scale; W, H = int(a.w * S), int(a.h * S)
im = Image.fromarray(cv2.resize(out, (W, H), interpolation=cv2.INTER_NEAREST))
dr = ImageDraw.Draw(im); f = view.font(12)
gx = (a.x // a.grid + 1) * a.grid
while gx < a.x + a.w:
    X = (gx - a.x) * S; dr.line([(X, 0), (X, H)], fill=(0, 255, 255), width=1)
    dr.text((X + 2, 2), str(gx), fill=(255, 255, 0), font=f, stroke_width=2, stroke_fill=(0, 0, 0)); gx += a.grid
gy = (a.y // a.grid + 1) * a.grid
while gy < a.y + a.h:
    Y = (gy - a.y) * S; dr.line([(0, Y), (W, Y)], fill=(0, 255, 255), width=1)
    dr.text((2, Y + 2), str(gy), fill=(255, 255, 0), font=f, stroke_width=2, stroke_fill=(0, 0, 0)); gy += a.grid
p = view.scratch_path(a.out); im.save(p); print(p, im.size)
