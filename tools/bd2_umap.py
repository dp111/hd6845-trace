#!/usr/bin/env python3
"""Character map of the clean stripped shot (acid1b) for areas that were UNDER METAL.

usage: bd2_umap.py x0 y0 x1 y1 [xstep] [ystep]

Under metal the clean shot has three flat colours (calibrated under the ground rail
x 16008-16058 at y 15490-15660, where the ground land, two gate bands and the field
above them are known):
   f  field      pink    R 180-200, G 115-130, B about equal to G
   d  diffusion  tan     R 185-210, G 155-185, B 40 or more below G, R-G under 48
   p  poly       salmon  R 215-250, G 150-185, R-G 48 or more
   .  dark (outline, edge)  R < 150 or G < 95 with R < 190
   ?  none of these (in the open the map is meaningless: open areas come out '?', '.')
"""
import os, sys
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = np.load(os.path.join(ROOT, 'cache', 'acid1b.npy'), mmap_mode='r')
x0, y0, x1, y1 = map(int, sys.argv[1:5])
xs_ = int(sys.argv[5]) if len(sys.argv) > 5 else 2
ys_ = int(sys.argv[6]) if len(sys.argv) > 6 else 3
def cls(m):
    r, g, b = m
    if r < 150 or (g < 95 and r < 190):
        return '.'
    if g - b < 14 and r - g > 40:
        return 'f'
    if g - b >= 22 and r - g < 48:
        return 'd'
    if r - g >= 48 and g - b >= 14 and r >= 205:
        return 'p'
    return '?'
xs = list(range(x0, x1, xs_))
print('x from %d step %d; header digit = tens of x' % (x0, xs_))
print('%6s  %s' % ('', ''.join(str((x // 10) % 10) if x % 10 < xs_ else ' ' for x in xs)))
for y in range(y0, y1, ys_):
    print('%6d  %s' % (y, ''.join(cls(np.asarray(B[y:y + ys_, x:x + xs_]).reshape(-1, 3).mean(0)) for x in xs)))
