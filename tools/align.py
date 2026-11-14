#!/usr/bin/env python3
"""Register the acid shot to the metal shot and resample it into the metal frame.

Measures the local offset between the two shots on a grid of patches (phase
correlation of edge images), fits an affine map metal(x, y) -> acid(x', y'), reports
the residuals, and writes

  trace/align.json         the affine and its fit statistics (kept in git)
  cache/acid_aligned.npy   the acid shot resampled so that pixel (x, y) shows the
                           same place as pixel (x, y) of the metal shot

After this every tool can use metal-shot coordinates for both layers.
"""
import json
import os
import numpy as np
import cv2

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, 'cache')
N = 768        # patch size
STEP = 1100    # grid step


def edges(a):
    g = cv2.cvtColor(np.ascontiguousarray(a), cv2.COLOR_RGB2GRAY).astype(np.float32)
    g = cv2.GaussianBlur(g, (0, 0), 2)
    e = cv2.magnitude(cv2.Sobel(g, cv2.CV_32F, 1, 0), cv2.Sobel(g, cv2.CV_32F, 0, 1))
    return (e - e.mean()) / (e.std() + 1e-6)


def measure(M, A):
    H = min(M.shape[0], A.shape[0])
    W = min(M.shape[1], A.shape[1])
    win = cv2.createHanningWindow((N, N), cv2.CV_32F)
    pts = []
    for cy in range(N, H - N, STEP):
        for cx in range(N, W - N, STEP):
            m = edges(M[cy - N // 2:cy + N // 2, cx - N // 2:cx + N // 2])
            a = edges(A[cy - N // 2:cy + N // 2, cx - N // 2:cx + N // 2])
            (dx, dy), resp = cv2.phaseCorrelate(m, a, win)
            # phaseCorrelate returns the shift of a relative to m:
            # a feature at m(x, y) is at a(x + dx, y + dy)
            pts.append((cx, cy, dx, dy, resp))
    return np.array(pts)


def fit(P):
    """Robust affine fit of the offset field; returns 2x3 matrix for metal->acid."""
    keep = P[:, 4] > 0.05
    for _ in range(4):
        Q = P[keep]
        X = np.c_[Q[:, 0], Q[:, 1], np.ones(len(Q))]
        cx, *_ = np.linalg.lstsq(X, Q[:, 2], rcond=None)
        cy, *_ = np.linalg.lstsq(X, Q[:, 3], rcond=None)
        Xa = np.c_[P[:, 0], P[:, 1], np.ones(len(P))]
        r = np.hypot(P[:, 2] - Xa @ cx, P[:, 3] - Xa @ cy)
        keep = (P[:, 4] > 0.05) & (r < 1.5)
    return cx, cy, r, keep


def main():
    M = np.load(os.path.join(CACHE, 'metal.npy'), mmap_mode='r')
    A = np.load(os.path.join(CACHE, 'acid.npy'), mmap_mode='r')
    P = measure(M, A)
    cx, cy, r, keep = fit(P)
    print(f'patches {len(P)}, used {keep.sum()}')
    print('acid_x = x + %.6f*x + %.6f*y + %.3f' % tuple(cx))
    print('acid_y = y + %.6f*x + %.6f*y + %.3f' % tuple(cy))
    print('residual of used patches: rms %.3f px, max %.3f px' % (
        np.sqrt((r[keep] ** 2).mean()), r[keep].max()))
    rej = P[~keep]
    print('rejected patches (cx, cy, dx, dy, response):')
    for row in rej:
        print('   %6d %6d  %+7.2f %+7.2f  %.3f' % tuple(row))

    # metal (x, y) -> acid (x', y')
    T = np.array([[1 + cx[0], cx[1], cx[2]],
                  [cy[0], 1 + cy[1], cy[2]]])
    with open(os.path.join(ROOT, 'trace', 'align.json'), 'w') as f:
        json.dump({'metal_to_acid': T.tolist(),
                   'patches_used': int(keep.sum()),
                   'residual_rms_px': float(np.sqrt((r[keep] ** 2).mean())),
                   'residual_max_px': float(r[keep].max())}, f, indent=1)

    # Resample in horizontal bands to keep memory down.
    H, W = M.shape[:2]
    out = np.lib.format.open_memmap(os.path.join(CACHE, 'acid_aligned.npy'), mode='w+',
                                    dtype=np.uint8, shape=(H, W, 3))
    BAND = 2048
    PAD = 32
    for y0 in range(0, H, BAND):
        y1 = min(H, y0 + BAND)
        # source rows needed for this band
        ys = [T[1, 0] * x + T[1, 1] * y + T[1, 2] for x in (0, W) for y in (y0, y1)]
        s0 = max(0, int(min(ys)) - PAD)
        s1 = min(A.shape[0], int(max(ys)) + PAD)
        src = np.ascontiguousarray(A[s0:s1])
        Tb = T.copy()
        Tb[1, 2] += T[1, 1] * y0 - s0     # dst row j is metal row y0 + j; src row is acid row - s0
        Tb[0, 2] += T[0, 1] * y0
        out[y0:y1] = cv2.warpAffine(src, Tb, (W, y1 - y0),
                                    flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP,
                                    borderMode=cv2.BORDER_CONSTANT)
    out.flush()
    print('wrote cache/acid_aligned.npy', out.shape)


if __name__ == '__main__':
    main()
