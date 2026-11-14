#!/usr/bin/env python3
"""Find the other places on the die that look like a given rectangle of it.

usage: findcell.py x0 y0 x1 y1 [--min SCORE] [--region x0,y0:x1,y1] [--layer metal|acid]
                   [--orient LIST] [--cell NAME]

The rectangle (metal-shot pixels) is the master. It is tried in all eight
orientations (mirror about a vertical line or not, then turned 0/90/180/270 degrees
clockwise) against the whole die at 1/4 scale, and each hit is refined at full
resolution. Output is one line per hit, ready to paste as an @inst line:

  @inst NAME dx,dy [mx=CX] [rot=DEG o=CX,CY]     # score, centre of the instance

where CX,CY is the centre of the master rectangle. Scores are normalised
cross-correlation: 1.0 is identical, and the master itself shows up as 0,0.
--orient restricts the orientations, e.g. --orient 0,m0,90 (m = mirrored).
"""
import argparse
import os
import numpy as np
import cv2

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, 'cache')
Q = 4   # coarse scale


def gray_small(layer):
    """Whole die, grey, 1/Q scale; cached on disk."""
    path = os.path.join(CACHE, f'{layer}_g{Q}.npy')
    if os.path.exists(path):
        return np.load(path)
    name = {'metal': 'metal.npy', 'acid': 'acid_aligned.npy'}[layer]
    a = np.load(os.path.join(CACHE, name), mmap_mode='r')
    H, W = a.shape[:2]
    hh, ww = H // Q * Q, W // Q * Q
    out = np.zeros((hh // Q, ww // Q), np.uint8)
    for y0 in range(0, hh, Q * 512):
        y1 = min(hh, y0 + Q * 512)
        g = cv2.cvtColor(np.ascontiguousarray(a[y0:y1, :ww]), cv2.COLOR_RGB2GRAY)
        out[y0 // Q:y1 // Q] = cv2.resize(g, (ww // Q, (y1 - y0) // Q), interpolation=cv2.INTER_AREA)
    np.save(path, out)
    return out


def full(layer):
    name = {'metal': 'metal.npy', 'acid': 'acid_aligned.npy'}[layer]
    return np.load(os.path.join(CACHE, name), mmap_mode='r')


def orient(img, mirror, rot):
    if mirror:
        img = np.fliplr(img)
    k = {0: 0, 90: -1, 180: 2, 270: 1}[rot]
    return np.ascontiguousarray(np.rot90(img, k))


def find(x0, y0, x1, y1, layer='metal', min_score=0.5, region=None, orients=None):
    small = gray_small(layer)
    big = full(layer)
    H, W = big.shape[:2]
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    master = cv2.cvtColor(np.ascontiguousarray(big[y0:y1, x0:x1]), cv2.COLOR_RGB2GRAY)
    hits = []
    for mirror in (False, True):
        for rot in (0, 90, 180, 270):
            tag = ('m' if mirror else '') + str(rot)
            if orients and tag not in orients:
                continue
            t_full = orient(master, mirror, rot)
            t_small = cv2.resize(t_full, (t_full.shape[1] // Q, t_full.shape[0] // Q),
                                 interpolation=cv2.INTER_AREA)
            res = cv2.matchTemplate(small, t_small, cv2.TM_CCOEFF_NORMED)
            th, tw = t_small.shape
            while True:
                _, score, _, loc = cv2.minMaxLoc(res)
                if score < min_score * 0.85:
                    break
                px, py = loc
                # suppress this neighbourhood
                res[max(0, py - th // 2):py + th // 2 + 1, max(0, px - tw // 2):px + tw // 2 + 1] = -1
                # refine at full resolution
                fh, fw = t_full.shape
                ax, ay = px * Q, py * Q
                pad = 2 * Q + 4
                sx0, sy0 = max(0, ax - pad), max(0, ay - pad)
                sx1, sy1 = min(W, ax + fw + pad), min(H, ay + fh + pad)
                if sx1 - sx0 < fw or sy1 - sy0 < fh:
                    continue
                win = cv2.cvtColor(np.ascontiguousarray(big[sy0:sy1, sx0:sx1]), cv2.COLOR_RGB2GRAY)
                r2 = cv2.matchTemplate(win, t_full, cv2.TM_CCOEFF_NORMED)
                _, s2, _, l2 = cv2.minMaxLoc(r2)
                fx, fy = sx0 + l2[0], sy0 + l2[1]
                icx, icy = fx + fw / 2, fy + fh / 2
                if region and not (region[0] <= icx <= region[2] and region[1] <= icy <= region[3]):
                    continue
                if s2 >= min_score:
                    hits.append(dict(score=s2, mirror=mirror, rot=rot, dx=icx - cx, dy=icy - cy,
                                     cx=icx, cy=icy))
    # drop duplicates (same place found in two orientations): keep the best
    hits.sort(key=lambda h: -h['score'])
    keep = []
    for h in hits:
        if all(abs(h['cx'] - k['cx']) > (x1 - x0) / 3 or abs(h['cy'] - k['cy']) > (y1 - y0) / 3
               for k in keep):
            keep.append(h)
    return keep, (cx, cy)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('x0', type=int)
    ap.add_argument('y0', type=int)
    ap.add_argument('x1', type=int)
    ap.add_argument('y1', type=int)
    ap.add_argument('--min', type=float, default=0.5)
    ap.add_argument('--region', default=None)
    ap.add_argument('--layer', default='metal')
    ap.add_argument('--orient', default=None)
    ap.add_argument('--cell', default='NAME')
    a = ap.parse_args()
    region = None
    if a.region:
        p, q = a.region.split(':')
        region = tuple(map(float, p.split(','))) + tuple(map(float, q.split(',')))
    hits, (cx, cy) = find(a.x0, a.y0, a.x1, a.y1, a.layer, a.min, region,
                          a.orient.split(',') if a.orient else None)
    for h in hits:
        parts = [f'@inst {a.cell} {h["dx"]:.0f},{h["dy"]:.0f}']
        if h['mirror']:
            parts.append(f'mx={cx:g}')
        if h['rot']:
            parts.append(f'rot={h["rot"]} o={cx:g},{cy:g}')
        print(f'{" ".join(parts):60s} # score {h["score"]:.2f} at {h["cx"]:.0f},{h["cy"]:.0f}')
    print(f'{len(hits)} hits')


if __name__ == '__main__':
    main()
