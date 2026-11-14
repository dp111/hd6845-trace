#!/usr/bin/env python3
"""Metal lines along a cut: prints the bright (metal) runs of the metal shot.

usage: sel_cut.py h Y X0 X1 [--dy 4] [--thr T] [--layer metal|metal1]   horizontal cut at y=Y
       sel_cut.py v X Y0 Y1 [--dx 4] ...                                 vertical cut at x=X

For each run of pixels brighter than the threshold (default: Otsu over the cut) it
prints start, end, centre and width. A quick way to list the vertical metal lines of
a wiring bundle at a given y, or to see where one line starts and stops.
"""
import argparse
import os
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dir', choices=['h', 'v'])
    ap.add_argument('c', type=int)
    ap.add_argument('a', type=int)
    ap.add_argument('b', type=int)
    ap.add_argument('--d', type=int, default=4)
    ap.add_argument('--thr', type=float, default=None)
    ap.add_argument('--layer', default='metal')
    ap.add_argument('--min', type=int, default=8)
    ap.add_argument('--metal', type=float, default=4.5, help='runs whose grain (std across the cut) is above this are called metal; field is smooth')
    ap.add_argument('--all', action='store_true', help='print the non-metal runs too')
    ap.add_argument('--brief', action='store_true', help='centres only, on one line')
    a = ap.parse_args()
    arr = np.load(os.path.join(ROOT, 'cache', a.layer + '.npy'), mmap_mode='r')
    if a.dir == 'h':
        s = np.asarray(arr[a.c - a.d:a.c + a.d + 1, a.a:a.b]).astype(np.float32)
        # yellowness: metal is bright in R and G, lower in B
        v = (s[..., 0] + s[..., 1]).mean(axis=0) / 2
        sd = s[..., 1].std(axis=0)
    else:
        s = np.asarray(arr[a.a:a.b, a.c - a.d:a.c + a.d + 1]).astype(np.float32)
        v = (s[..., 0] + s[..., 1]).mean(axis=1) / 2
        sd = s[..., 1].std(axis=1)
    thr = a.thr
    if thr is None:
        import cv2
        t, _ = cv2.threshold(np.clip(v, 0, 255).astype(np.uint8).reshape(1, -1), 0, 255,
                             cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        thr = t
    on = v > thr
    runs = []
    i = 0
    n = len(on)
    while i < n:
        if on[i]:
            j = i
            while j < n and on[j]:
                j += 1
            if j - i >= a.min:
                runs.append((a.a + i, a.a + j - 1))
            i = j
        else:
            i += 1
    out = []
    for r in runs:
        i0, i1 = r[0] - a.a, r[1] - a.a + 1
        m = v[i0:i1].mean()
        kind = 'METAL' if sd[i0:i1].mean() > a.metal else 'field'
        if a.all or kind == 'METAL':
            out.append(f'{(r[0] + r[1]) / 2:.0f}' if a.brief else f'  {r[0]}-{r[1]}  centre {(r[0] + r[1]) / 2:.0f}  width {r[1] - r[0] + 1}  mean {m:.0f} grain {sd[i0:i1].mean():.0f} {kind}')
    print((' ' if a.brief else '\n').join(out))


if __name__ == '__main__':
    main()

