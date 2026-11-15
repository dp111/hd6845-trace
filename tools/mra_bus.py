#!/usr/bin/env python3
"""mra: where do the rows touch the vertical bus lines at x 13000-13340?

usage: mra_bus.py [--x0 13040 --x1 13345] [--layer metal]

1. Finds the bus-line centres from the column-mean brightness over the whole array.
2. For every row (19 rows, offsets from the trace file) and every line, takes the strip
   of the line (centre +-9 px) over the row's height and compares it with the median strip
   of all lines in that row. A contact (or anything else that only one line has) shows as
   a run of large differences. Prints, per row, each line's largest anomaly and where it is.
Numbers only say where to look.
"""
import argparse, os
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROWS = [('r0', 0, -2646), ('r1', 0, -2169), ('r2', 0, -1692), ('r3', 0, -1215), ('r4', 0, -477),
        ('r5', 0, 0), ('r6', 0, 477), ('r7', 0, 1040), ('r8', 1, 1518), ('r9', 1, 1995),
        ('r10', 1, 2472), ('r11', 1, 3123), ('r12', 1, 3601), ('r13', 1, 4077), ('r14', 1, 4554),
        ('r15', 1, 5097), ('r16', 1, 5574), ('r17', 1, 6051), ('r18', 2, 6528)]
Y0, Y1 = 9885, 10362          # master row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--x0', type=int, default=13040)
    ap.add_argument('--x1', type=int, default=13345)
    ap.add_argument('--layer', default='metal')
    ap.add_argument('--hw', type=int, default=9)
    a = ap.parse_args()
    arr = np.load(os.path.join(ROOT, 'cache', a.layer + '.npy'), mmap_mode='r')
    big = np.asarray(arr[7265:16940, a.x0:a.x1]).astype(np.float32)
    g = (big[..., 0] + big[..., 1]) / 2
    prof = g.mean(axis=0)
    sm = np.convolve(prof, np.ones(9) / 9, mode='same')
    thr = (sm.max() + sm.min()) / 2
    runs = []
    on = False
    for i, v in enumerate(sm):
        if v > thr and not on:
            s = i; on = True
        elif v <= thr and on:
            on = False
            if i - s >= 8:
                runs.append((s + a.x0, i + a.x0))
    print('bus lines (bright runs of the column mean over y 7265-16940):')
    for s, e in runs:
        print('  x %d-%d  centre %d  width %d' % (s, e, (s + e) // 2, e - s))
    cen = [(s + e) // 2 for s, e in runs]
    print()
    print('per row: for each line, peak |difference from the median line| (smoothed over 12 px) and its y in master coordinates')
    for tag, dx, dy in ROWS:
        strips = []
        for c in cen:
            st = np.asarray(arr[Y0 + dy:Y1 + dy, c + dx - a.hw:c + dx + a.hw + 1]).astype(np.float32)
            strips.append(((st[..., 0] + st[..., 1]) / 2).mean(axis=1))
        S = np.array(strips)                       # line, y
        med = np.median(S, axis=0)
        out = []
        for i, c in enumerate(cen):
            d = np.abs(S[i] - med)
            d = np.convolve(d, np.ones(12) / 12, mode='same')
            j = int(d.argmax())
            out.append('%d:%3.0f@%d' % (c, d[j], Y0 + j))
        print('  %-4s %s' % (tag, '  '.join(out)))


if __name__ == '__main__':
    main()
