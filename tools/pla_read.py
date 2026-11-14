#!/usr/bin/env python3
"""Read the register decode array (14230-15760 x 13500-14660) from the clean shot.

The array is a NOR plane: 18 metal columns, 10 poly rows in five pairs, a ground
diffusion rail between the two rows of each pair, and contact pads on the columns
in six bands (above row 1, between the pairs, below row 10). A transistor exists
where a pad's diffusion runs under a row to the rail.

Two things are measured in the clean shot of chip 1 (layer acid1b), where both show
as colour under the column metal:
  pads         diffusion pad present (tan) or field (pink) at each column and band
  transistors  poly over diffusion (redder) or over field at each column and row

Each row's values fall in two clusters; the threshold is put in the largest gap. A
transistor also needs a pad beside it; disagreements are reported, not hidden.

Writes trace/decode_matrix.json and prints the table and the address each column
decodes. Run tools/gen_decode.py afterwards to regenerate trace/decode.txt.
"""
import json
import os
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COL0, PITCH = 14260.5, 86.66                 # column centres, from the metal shot
ROWS = [13766, 13851, 13940, 14024, 14112, 14196, 14284, 14369, 14456, 14543]
BANDS = {'A': 13720, 'B': 13891, 'C': 14062, 'D': 14234, 'E': 14405, 'F': 14580}
BAND_OF_ROW = 'ABBCCDDEEF'


def main():
    B = np.load(os.path.join(ROOT, 'cache', 'acid1b.npy'), mmap_mode='r')
    cols = [COL0 + PITCH * k for k in range(18)]

    def rg(x, y, hw, hh):
        p = np.asarray(B[int(y - hh):int(y + hh), int(x - hw):int(x + hw)]).reshape(-1, 3).astype(float).mean(0)
        return p[0] - p[1]

    pads = {b: [int(rg(x, y, 9, 14) < 40) for x in cols] for b, y in BANDS.items()}
    raw = [[rg(x, y, 7, 6) for x in cols] for y in ROWS]
    T, notes = [], []
    for r, vals in enumerate(raw):
        s = sorted(vals)
        gaps = [(s[i + 1] - s[i], (s[i + 1] + s[i]) / 2) for i in range(len(s) - 1)]
        gap, thr = max(gaps)
        row = []
        for c, v in enumerate(vals):
            t = int(v > thr)
            if t and not pads[BAND_OF_ROW[r]][c]:
                notes.append(f'row {r + 1} column {c + 1}: colour {v:.0f} is above the threshold '
                             f'{thr:.0f} but there is no pad beside it; taken as no transistor')
                t = 0
            row.append(t)
        T.append(row)
        print(f'row {r + 1:2d}  threshold {thr:4.1f}  gap {gap:4.1f}   ' + ' '.join(str(t) for t in row)
              + '   values ' + ' '.join('%2.0f' % v for v in vals))
    for b in BANDS:
        print(f'pads {b}                           ' + ' '.join(str(p) for p in pads[b]))

    # decode: pair k is rows 2k+1 (true line) and 2k+2 (complement line), k = address bit
    addr, bad = [], []
    for c in range(18):
        a = 0
        for k in range(5):
            t, n = T[2 * k][c], T[2 * k + 1][c]
            if t + n != 1:
                bad.append(f'column {c + 1}, pair {k + 1}: {t + n} transistors')
            if n:
                a |= 1 << k
        addr.append(a)
    print('column decodes address:', addr)
    print('one transistor per pair in every column:', 'yes' if not bad else 'NO: ' + '; '.join(bad))
    print('addresses distinct and exactly 0-17:', sorted(addr) == list(range(18)))
    for n in notes:
        print('note:', n)
    with open(os.path.join(ROOT, 'trace', 'decode_matrix.json'), 'w') as f:
        json.dump({'columns_x': [round(x, 1) for x in cols], 'rows_y': ROWS, 'bands_y': BANDS,
                   'pads': pads, 'transistors': T, 'address_of_column': addr,
                   'measured_r_minus_g': [[round(v, 1) for v in row] for row in raw],
                   'notes': notes}, f, indent=1)


if __name__ == '__main__':
    main()
