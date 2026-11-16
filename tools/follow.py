#!/usr/bin/env python3
"""Follow one metal line from a point on it, using both chips' metal shots.

usage: follow.py x y DIR [--gap 24] [--max 30000] [--gmin 128] [--rmin 177] [--trace] [--one]
       DIR is N, S, E or W: the way to set off.

The line is walked in 2 px steps. At each step the metal run across the line is found and
the walk re-centres on it, so jogs and 45-degree diagonals are followed. Dark bars across
the line (the edges of poly underneath, contact rings) up to --gap px are bridged. Where
the metal stops, the two sideways directions are tried (a right-angle corner); if neither
has 35 px of metal the line has ended. With a single metal layer a line cannot cross another, so what
comes out is one piece of metal from the start point to an end.

Printed: every corner, every stretch where the line was more than twice its width (a pad,
a T junction or a merge: LOOK at those), contact candidates from the clean shot (red minus
green under 24 on or beside the centre line: the green-tan of a contact hole), and the end.
`--trace` prints the piece as a trace-file M line.

The metal test is per pixel on a barely blurred image: red over --rmin and green over
--gmin (metal 181-215 / 140-200, bare ground 156-173 / 129-147, measured in three places;
red is the discriminator). It must not be blurred along the line: where a line crosses poly
the metal shows two dark edge lines 8 and 14 px wide with 8 px of bright metal between, and
a real break between two pieces on one track can be as short as 35 px, so the gap that is
bridged has to stay well under that: 24 (a crossing's dark run measures up to 18).

A pixel counts as metal if EITHER chip's metal shot says so (chip 1's bare ground is much
darker, red 105-140, so the same thresholds are safe there): dirt on one chip then does not
end a line, while a real break is bare in both. --one uses chip 2 only.

A corner is looked for the moment the metal stops, before any gap is bridged. (First
version bridged first and so stepped from one line of a staircase onto the next, 12 px
beyond its corner: the same mistake as sel_tracks.py. Check staircases by eye regardless.)

Limits. It follows metal, not nets: at the end look at the clean shot to see what the
contact there joins. A T junction is reported as a wide stretch and the walk goes straight
on. Dirt can end a line early: check the end in the other chip's metal shot. Contact
candidates are candidates. Check the result against one overlay before drawing it.
"""
import argparse
import os
import sys
import numpy as np
import cv2

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view

DIRS = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
NAME = {v: k for k, v in DIRS.items()}


class Tile:
    """A moving window of the metal mask and of the clean shot's red-minus-green."""

    def __init__(self, gmin, rmin, one=False, size=700):
        self.size = size
        self.one = one
        self.gmin, self.rmin = gmin, rmin
        self.x0 = self.y0 = None

    def load(self, x, y):
        s = self.size
        self.x0, self.y0 = int(x) - s // 2, int(y) - s // 2
        m = cv2.GaussianBlur(view.raw('metal', self.x0, self.y0, s, s).astype(np.float32), (0, 0), 0.8)
        self.mask = (m[..., 1] > self.gmin) & (m[..., 0] > self.rmin)
        if not self.one:
            m = cv2.GaussianBlur(view.raw('metal1', self.x0, self.y0, s, s).astype(np.float32), (0, 0), 0.8)
            self.mask |= (m[..., 1] > self.gmin) & (m[..., 0] > self.rmin - 2)
        a = view.raw('acid1b', self.x0, self.y0, s, s).astype(np.float32)
        self.rg = cv2.blur(a[..., 0] - a[..., 1], (7, 7))

    def ensure(self, x, y):
        if self.x0 is None or not (self.x0 + 90 < x < self.x0 + self.size - 90 and
                                   self.y0 + 90 < y < self.y0 + self.size - 90):
            self.load(x, y)

    def m(self, x, y):
        self.ensure(x, y)
        return bool(self.mask[int(round(y)) - self.y0, int(round(x)) - self.x0])

    def green(self, x, y):
        self.ensure(x, y)
        return float(self.rg[int(round(y)) - self.y0, int(round(x)) - self.x0])


def cut(t, x, y, p, half=34):
    """Metal run across the line through (x, y): (centre offset, width) or None."""
    vals = [t.m(x + k * p[0], y + k * p[1]) for k in range(-half, half + 1)]
    best = None
    k = 0
    n = len(vals)
    while k < n:
        if vals[k]:
            j = k
            while j < n and vals[j]:
                j += 1
            lo, hi = k - half, j - 1 - half
            if lo <= 7 and hi >= -7:
                d = 0 if lo <= 0 <= hi else min(abs(lo), abs(hi))
                if best is None or d < best[0]:
                    best = (d, (lo + hi) / 2.0, hi - lo + 1)
            k = j
        else:
            k += 1
    return None if best is None else (best[1], best[2])


def run_len(t, x, y, d, limit=70):
    """How far metal goes from (x, y) along d, bridging gaps of 10 px (the dark line where
    metal steps off a poly edge measures 4-8 px)."""
    n = miss = 0
    for k in range(1, limit):
        if t.m(x + k * d[0], y + k * d[1]):
            n = k
            miss = 0
        else:
            miss += 1
            if miss > 10:
                break
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('x', type=float)
    ap.add_argument('y', type=float)
    ap.add_argument('dir')
    ap.add_argument('--gap', type=int, default=24)
    ap.add_argument('--max', type=int, default=30000)
    ap.add_argument('--gmin', type=int, default=128)
    ap.add_argument('--rmin', type=int, default=177)
    ap.add_argument('--trace', action='store_true')
    ap.add_argument('--one', action='store_true', help='chip-2 metal shot only')
    a = ap.parse_args()
    t = Tile(a.gmin, a.rmin, a.one)
    d = DIRS[a.dir.upper()]
    p = (-d[1], d[0])
    x, y = a.x, a.y
    c = cut(t, x, y, p)
    if c is None:
        print('no metal at the start point')
        return
    x, y = x + c[0] * p[0], y + c[0] * p[1]
    width = c[1]
    widths = [width]
    pts = [(x, y)]
    print('start %d,%d %s  width %d' % (x, y, NAME[d], width))
    step, miss, total = 2, 0, 0
    good = (x, y)
    wide_from = None
    cont = []
    lowrun = 0
    turns = 0
    corners = []
    while total < a.max:
        nx, ny = x + step * d[0], y + step * d[1]
        c = cut(t, nx, ny, p)
        if c is not None:
            off, w = c
            nominal = float(np.median(widths[-40:]))
            if w > 2.2 * nominal and w > 40:
                if wide_from is None:
                    wide_from = (nx, ny)
                x, y = nx, ny
            else:
                if wide_from is not None:
                    print('  wide from %d,%d to %d,%d' % (wide_from[0], wide_from[1], nx, ny))
                    wide_from = None
                off = max(-step - 1.0, min(step + 1.0, off))
                x, y = nx + off * p[0], ny + off * p[1]
                widths.append(w)
            good = (x, y)
            miss = 0
            g = min(t.green(x, y), t.green(x + 8 * p[0], y + 8 * p[1]), t.green(x - 8 * p[0], y - 8 * p[1]))
            if g < 24:
                lowrun += step
            else:
                if lowrun >= 8:
                    cont.append((x - (lowrun // 2 + step) * d[0], y - (lowrun // 2 + step) * d[1]))
                lowrun = 0
        else:
            miss += step
            x, y = nx, ny
            if miss == 6 or miss > a.gap:
                # a corner is looked for as soon as the metal stops, BEFORE any gap is bridged:
                # in a staircase the next line lies 12-20 px beyond the corner of this one
                bx, by = good
                best = None
                for q in (p, (-p[0], -p[1])):
                    for back in (0, 6, 12, 18):
                        sx, sy = bx - back * d[0], by - back * d[1]
                        n = run_len(t, sx, sy, q)
                        if n >= 35 and (best is None or n > best[0]):
                            best = (n, q, sx, sy)
                if best is None:
                    if miss <= a.gap:
                        total += step
                        continue
                    print('end %d,%d  (no metal for %d px beyond; %d px followed)' % (bx, by, a.gap, total))
                    break
                n, q, sx, sy = best
                pts.append((sx, sy))
                d = q
                p = (-d[1], d[0])
                x, y = sx + 10 * d[0], sy + 10 * d[1]
                c = cut(t, x, y, p)
                if c is not None:
                    x, y = x + c[0] * p[0], y + c[0] * p[1]
                print('  corner %d,%d -> %s' % (sx, sy, NAME[d]))
                miss = 0
                good = (x, y)
                wide_from = None
                turns += 1
                if any(abs(sx - cx) < 8 and abs(sy - cy) < 8 for cx, cy in corners):
                    print('back at a corner already turned: stopped (the start point was probably on a wide rail)')
                    break
                corners.append((sx, sy))
                if turns > 60:
                    print('more than 60 corners: stopped')
                    break
        total += step
    else:
        print('stopped at %d,%d after %d px (limit)' % (x, y, total))
    pts.append(good)
    if cont:
        uniq = []
        for cx, cy in cont:
            if not any(abs(cx - ux) < 12 and abs(cy - uy) < 12 for ux, uy in uniq):
                uniq.append((cx, cy))
        print('contact candidates: ' + '  '.join('%d,%d' % (cx, cy) for cx, cy in uniq[:40]))
    if a.trace and len(pts) <= 40:
        out = 'M %d,%d' % pts[0]
        for (px, py), (qx, qy) in zip(pts, pts[1:]):
            out += ' x%d' % qx if abs(qy - py) < abs(qx - px) else ' y%d' % qy
        print(out + ' w=%d' % round(float(np.median(widths))))


if __name__ == '__main__':
    main()
