#!/usr/bin/env python3
"""Candidate metal contacts along a track, from the clean shot (acid1b).

usage: tla_contacts.py y0 y1 x [x ...] [--horizontal] [--win 4] [--side 8] [--thr 24]

Under a metal line the clean shot shows field as pink (red minus green about 65), poly as
salmon (50 or more) and the hole of a metal contact as a dull green-tan patch (red minus
green under 15: measured on thirteen points beside the step gate cluster, 2026-11-16). For
each track the mean red minus green of a (2*win+1) square is taken along the line, at the
track centre and at +-side px to either side (contacts sit up to 8 px off centre), and runs
of at least 7 rows below --thr are printed with their centre and the offset where the
minimum was found.

Only candidates with metal on the track within 16-70 px above or below (40 % of that stretch) (chip-2 metal shot:
green over 140 and red over 170 on the track centre) are kept, since open ground where a
track has no metal is green as well. --nometal lists them all.

A candidate is not a contact until seen: open field between two lines is green too, so a
track position that is wrong by 15 px gives false hits all along, and a contact to
diffusion (not poly) can look different. Use it to know WHERE to look.
"""
import argparse
import os
import sys
import numpy as np
import cv2

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import view

ap = argparse.ArgumentParser()
ap.add_argument('a0', type=int)
ap.add_argument('a1', type=int)
ap.add_argument('tracks', type=int, nargs='+')
ap.add_argument('--horizontal', action='store_true')
ap.add_argument('--win', type=int, default=4)
ap.add_argument('--side', type=int, default=8)
ap.add_argument('--thr', type=float, default=24)
ap.add_argument('--nometal', action='store_true')
a = ap.parse_args()
pad = a.side + a.win + 2
for t in a.tracks:
    if a.horizontal:
        rgb = view.raw('acid1b', a.a0, t - pad, a.a1 - a.a0, 2 * pad + 1).astype(np.float32)
        rgb = rgb.transpose(1, 0, 2)
    else:
        rgb = view.raw('acid1b', t - pad, a.a0, 2 * pad + 1, a.a1 - a.a0).astype(np.float32)
    if a.horizontal:
        mt = view.raw('metal', a.a0, t - 3, a.a1 - a.a0, 7).astype(np.float32).mean(0)
    else:
        mt = view.raw('metal', t - 3, a.a0, 7, a.a1 - a.a0).astype(np.float32).mean(1)
    kk = np.ones(5) / 5
    ism = (np.convolve(mt[:, 0], kk, 'same') > 170) & (np.convolve(mt[:, 1], kk, 'same') > 140)
    d = rgb[..., 0] - rgb[..., 1]
    k = 2 * a.win + 1
    d = cv2.blur(d, (k, k))
    cols = [pad - a.side, pad, pad + a.side]
    prof = np.stack([d[:, c] for c in cols], 1)
    lo = prof.min(1)
    arg = prof.argmin(1)
    hits = []
    i = 0
    n = len(lo)
    while i < n:
        if lo[i] < a.thr:
            j = i
            while j < n and lo[j] < a.thr:
                j += 1
            c = (i + j) // 2
            near = ism[max(0, c - 70):max(0, c - 16)].mean() > 0.4 if c > 20 else False
            near = near or (ism[c + 16:c + 70].mean() > 0.4 if c + 70 < n else False)
            if j - i >= 7 and (near or a.nometal):
                m = i + int(np.argmin(lo[i:j]))
                hits.append('%d(%+d,%d)' % (a.a0 + (i + j) // 2, (arg[m] - 1) * a.side, round(float(lo[m]))))
            i = j
        else:
            i += 1
    print('%5d: ' % t + '  '.join(hits))
