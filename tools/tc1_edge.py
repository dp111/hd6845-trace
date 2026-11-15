#!/usr/bin/env python3
"""Find a band's edges along a cut: prints runs where a colour test holds.

usage: tc1_edge.py row Y X0 X1 [layer] [test]
       tc1_edge.py col X Y0 Y1 [layer] [test]
layer: acid1b (default), acid, metal, metal1
test:  salmon (default; poly under metal in acid1b: R>205, R-G>45)
       poly   (salmon or open poly in acid1b: R-G>40 and R>120, not tan)
       metal  (bright and yellow in the metal shots: (R+G)/2>165)
       dark   (R+G+B < 300)
Each sample is the mean over 5 px across the cut. Runs shorter than 4 px are dropped.
"""
import os, sys
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = {'metal': 'metal.npy', 'acid': 'acid_aligned.npy', 'metal1': 'metal1.npy', 'acid1b': 'acid1b.npy'}
def main():
    a = sys.argv[1:]
    mode, c, p0, p1 = a[0], int(a[1]), int(a[2]), int(a[3])
    layer = a[4] if len(a) > 4 else 'acid1b'
    test = a[5] if len(a) > 5 else 'salmon'
    A = np.load(os.path.join(ROOT, 'cache', F[layer]), mmap_mode='r')
    if mode == 'row':
        s = np.asarray(A[c - 2:c + 3, p0:p1]).astype(float).mean(0)
    else:
        s = np.asarray(A[p0:p1, c - 2:c + 3]).astype(float).mean(1)
    R, G, B = s[:, 0], s[:, 1], s[:, 2]
    if test == 'salmon':
        on = (R > 205) & (R - G > 45)
    elif test == 'poly':
        on = (R - G > 40) & (R > 120)
    elif test == 'metal':
        on = (R + G) / 2 > 165
    else:
        on = (R + G + B) < 300
    runs = []
    i = 0
    n = len(on)
    while i < n:
        if on[i]:
            j = i
            while j < n and on[j]:
                j += 1
            if j - i >= 4:
                runs.append((p0 + i, p0 + j - 1))
            i = j
        else:
            i += 1
    print(f'{mode} {c} {layer} {test}: ' + ' '.join(f'{u}-{v}' for u, v in runs))
main()
