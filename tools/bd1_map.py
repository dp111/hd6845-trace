#!/usr/bin/env python3
"""ASCII maps of a region: where the metal is, and a rough colour class of the clean
stripped shot. Costs no images; a companion to a sharpened view, not a replacement.

usage: tools/t.sh bd1 bd1_map.py X Y W H [--cell 5] [--what metal|acid|both] [--layer metal|metal1]

metal map:  M metal (bright and yellow), m weaker (edge of a line, or a dark line under
            the metal), . no metal
acid map (acid1b):
            # dark outline            p pink (field under metal: R well above G, B near G)
            s salmon (poly under metal: bright, R well above G, G above B)
            r red-brown (poly in the open: darker, R well above G)
            t tan (diffusion under metal, bright)
            . khaki (open field or open diffusion)   g green
Each character is one cell of --cell pixels; the ruler gives die x every 10 cells and
each row starts with its die y. Colours drift; calibrate on a known feature first.
"""
import argparse
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view  # noqa: E402


def blocks(a, c):
    h, w = a.shape[:2]
    h2, w2 = h // c, w // c
    a = a[:h2 * c, :w2 * c].astype(np.float32)
    return a.reshape(h2, c, w2, c, -1)


def metal_map(x, y, w, h, c, layer):
    a = view.raw(layer, x, y, w, h)
    b = blocks(a, c)
    br = (b[..., 0] + b[..., 1]) / 2
    med = np.median(br.reshape(br.shape[0], c, br.shape[2], c).transpose(0, 2, 1, 3).reshape(br.shape[0], br.shape[2], -1), axis=2)
    hi = np.percentile(br.transpose(0, 2, 1, 3).reshape(br.shape[0], br.shape[2], -1), 80, axis=2)
    out = []
    for j in range(med.shape[0]):
        row = ''
        for i in range(med.shape[1]):
            if med[j, i] > 172:
                row += 'M'
            elif hi[j, i] > 178:
                row += 'm'
            else:
                row += '.'
        out.append(row)
    return out


def acid_map(x, y, w, h, c):
    a = view.raw('acid1b', x, y, w, h)
    b = blocks(a, c)
    m = np.median(b.transpose(0, 2, 1, 3, 4).reshape(b.shape[0], b.shape[2], c * c, 3), axis=2)
    out = []
    for j in range(m.shape[0]):
        row = ''
        for i in range(m.shape[1]):
            r, g, bl = m[j, i]
            if max(r, g, bl) < 100:
                ch = '#'
            elif g > r + 6:
                ch = 'g'
            elif r - g > 30:
                if bl >= g - 6 and r >= 165:
                    ch = 'p'
                elif r >= 185:
                    ch = 's'
                else:
                    ch = 'r'
            elif r > 180:
                ch = 't'
            else:
                ch = '.'
            row += ch
        out.append(row)
    return out


def show(title, rows, x, y, c):
    print(title)
    n = len(rows[0]) if rows else 0
    ruler = [' '] * n
    for i in range(0, n, 10):
        s = str(x + i * c)
        for k, ch in enumerate(s):
            if i + k < n:
                ruler[i + k] = ch
    print('      ' + ''.join(ruler))
    for j, r in enumerate(rows):
        print(f'{y + j * c:5d} {r}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('x', type=int)
    ap.add_argument('y', type=int)
    ap.add_argument('w', type=int)
    ap.add_argument('h', type=int)
    ap.add_argument('--cell', type=int, default=5)
    ap.add_argument('--what', default='both')
    ap.add_argument('--layer', default='metal')
    a = ap.parse_args()
    if a.what in ('metal', 'both'):
        show(f'{a.layer} map', metal_map(a.x, a.y, a.w, a.h, a.cell, a.layer), a.x, a.y, a.cell)
    if a.what in ('acid', 'both'):
        show('acid1b map', acid_map(a.x, a.y, a.w, a.h, a.cell), a.x, a.y, a.cell)


if __name__ == '__main__':
    main()
