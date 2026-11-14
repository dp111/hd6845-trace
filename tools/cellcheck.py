#!/usr/bin/env python3
"""Compare every instance of a cell with its master, in the photos.

usage: cellcheck.py CELL [--layer metal|acid] [--block N] [--scale S] [--only TAG,TAG]
                         [--bbox x0,y0:x1,y1]

For each @inst of CELL the instance's patch of the die is brought back into the
master's orientation and compared with the master's patch block by block (normalised
cross-correlation, each block allowed to slide a few pixels). Writes one picture per
instance to cache/scratch/cellcheck_CELL_TAG.png:

    master | instance | instance with poorly matching blocks tinted red

and prints the share of textured blocks that match badly. A block is skipped when the
master is featureless there. Bond debris and dirt show up as differences too, so the
pictures need a look; the numbers only say where to look first.
"""
import argparse
import os
import sys
import numpy as np
import cv2

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tracelib

ROOT = tracelib.ROOT
CACHE = os.path.join(ROOT, 'cache')


def tmatrix(mx, my, rot, o, dx, dy):
    """3x3 matrix taking master coordinates to instance coordinates."""
    T = np.eye(3)
    if mx is not None:
        T = np.array([[-1, 0, 2 * mx], [0, 1, 0], [0, 0, 1]]) @ T
    if my is not None:
        T = np.array([[1, 0, 0], [0, -1, 2 * my], [0, 0, 1]]) @ T
    if rot:
        a = np.radians(rot)
        c, s = np.cos(a), np.sin(a)
        ox, oy = o
        R = np.array([[c, -s, ox - c * ox + s * oy], [s, c, oy - s * ox - c * oy], [0, 0, 1]])
        T = R @ T
    return np.array([[1, 0, dx], [0, 1, dy], [0, 0, 1]]) @ T


def patch(arr, T, x0, y0, x1, y1):
    """Die patch for master rectangle (x0,y0)-(x1,y1) seen through transform T."""
    H, W = arr.shape[:2]
    corners = np.array([[x0, y0, 1], [x1, y0, 1], [x0, y1, 1], [x1, y1, 1]]).T
    q = T @ corners
    sx0 = int(np.floor(q[0].min())) - 3
    sy0 = int(np.floor(q[1].min())) - 3
    sx1 = int(np.ceil(q[0].max())) + 3
    sy1 = int(np.ceil(q[1].max())) + 3
    cx0, cy0, cx1, cy1 = max(0, sx0), max(0, sy0), min(W, sx1), min(H, sy1)
    src = np.zeros((sy1 - sy0, sx1 - sx0, 3), np.uint8)
    if cx1 > cx0 and cy1 > cy0:
        src[cy0 - sy0:cy1 - sy0, cx0 - sx0:cx1 - sx0] = arr[cy0:cy1, cx0:cx1]
    M = np.array([[1, 0, -sx0], [0, 1, -sy0], [0, 0, 1]]) @ T @ np.array(
        [[1, 0, x0], [0, 1, y0], [0, 0, 1]])
    return cv2.warpAffine(src, M[:2], (x1 - x0, y1 - y0),
                          flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP)


def block_ncc(master, inst, B=32, slide=5):
    """Per-block best NCC of master blocks inside the instance; nan where master is flat."""
    # blur first: the grain of the metal is random and would never correlate
    gm = cv2.GaussianBlur(cv2.cvtColor(master, cv2.COLOR_RGB2GRAY).astype(np.float32), (0, 0), 3)
    gi = cv2.GaussianBlur(cv2.cvtColor(inst, cv2.COLOR_RGB2GRAY).astype(np.float32), (0, 0), 3)
    h, w = gm.shape
    ny, nx = h // B, w // B
    out = np.full((ny, nx), np.nan, np.float32)
    for j in range(ny):
        for i in range(nx):
            y, x = j * B, i * B
            t = gm[y:y + B, x:x + B]
            if t.std() < 7:
                continue
            y0, x0 = max(0, y - slide), max(0, x - slide)
            win = gi[y0:min(h, y + B + slide), x0:min(w, x + B + slide)]
            out[j, i] = cv2.matchTemplate(win, t, cv2.TM_CCOEFF_NORMED).max()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cell')
    ap.add_argument('--layer', default='metal')
    ap.add_argument('--block', type=int, default=32)
    ap.add_argument('--scale', type=float, default=0.5)
    ap.add_argument('--only', default=None)
    ap.add_argument('--bbox', default=None)
    ap.add_argument('--bad', type=float, default=0.55)
    a = ap.parse_args()
    tr = tracelib.load()
    if a.cell not in tr.cells:
        raise SystemExit(f'no cell {a.cell}')
    if a.bbox:
        p, q = a.bbox.split(':')
        x0, y0 = map(int, p.split(','))
        x1, y1 = map(int, q.split(','))
    else:
        bs = np.array([it.geom.bounds for it in tr.cells[a.cell][2]])
        x0, y0 = int(bs[:, 0].min()) - 10, int(bs[:, 1].min()) - 10
        x1, y1 = int(bs[:, 2].max()) + 10, int(bs[:, 3].max()) + 10
    name = {'metal': 'metal.npy', 'acid': 'acid_aligned.npy', 'acid1b': 'acid1b.npy', 'metal1': 'metal1.npy'}[a.layer]
    arr = np.load(os.path.join(CACHE, name), mmap_mode='r')
    master = patch(arr, np.eye(3), x0, y0, x1, y1)
    only = a.only.split(',') if a.only else None
    os.makedirs(os.path.join(CACHE, 'scratch'), exist_ok=True)
    print(f'cell {a.cell}: master {x0},{y0}:{x1},{y1}')
    for name_, dx, dy, mx, my, tag, src, rot, o in tr.insts:
        if name_ != a.cell or (only and tag not in only):
            continue
        T = tmatrix(mx, my, rot, o, dx, dy)
        inst = patch(arr, T, x0, y0, x1, y1)
        ncc = block_ncc(master, inst, a.block)
        valid = ~np.isnan(ncc)
        bad = (ncc < a.bad) & valid
        tint = inst.copy().astype(np.float32)
        B = a.block
        for j, i in zip(*np.nonzero(bad)):
            blk = tint[j * B:(j + 1) * B, i * B:(i + 1) * B]
            blk[:] = blk * 0.45 + np.array([255, 0, 0]) * 0.55
        row = np.hstack([master, np.full((master.shape[0], 8, 3), 255, np.uint8), inst,
                         np.full((master.shape[0], 8, 3), 255, np.uint8), tint.astype(np.uint8)])
        row = cv2.resize(row, None, fx=a.scale, fy=a.scale, interpolation=cv2.INTER_AREA)
        sd = os.environ.get('HD_SCRATCH') or os.path.join(CACHE, 'scratch')
        sd = sd if os.path.isabs(sd) else os.path.join(ROOT, sd)
        os.makedirs(sd, exist_ok=True)
        out = os.path.join(sd, f'cellcheck_{a.cell}_{tag or "x"}.png')
        cv2.imwrite(out, cv2.cvtColor(row, cv2.COLOR_RGB2BGR))
        c = T @ np.array([(x0 + x1) / 2, (y0 + y1) / 2, 1])
        print(f'  {tag or "?":10s} centre {c[0]:6.0f},{c[1]:6.0f}  bad blocks {bad.sum():4d}/{valid.sum():4d} '
              f'({100 * bad.sum() / max(1, valid.sum()):4.1f}%)  median ncc {np.nanmedian(ncc):.2f}  -> {os.path.relpath(out, ROOT)}')


if __name__ == '__main__':
    main()
