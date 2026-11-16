# ur: upper rows of the left array (x 2918-4240, y 6543-10924): two more counters

Serial work, 2026-11-17. Trace: `trace/ur.txt`. Views: `cache/scratch/ur/`.

## Status

The nine rows are **nine more copies of the counter bit cell of the mid-right array**
(`trace/mra.txt`, `notes/blocks/mra.md`). Instanced, with their supply rails and clock
lines drawn: 252 transistors, extraction clean. They form

- a **4-bit counter**, rows u0-u3 (y 6543-8452): `c4l3` ... `c4l0` from the top;
- a **5-bit counter**, rows u4-u8 (y 8539-10924): `c5l4` ... `c5l0` from the top;

with an 87 px channel between them (y 8452-8539). Which counters they are is not
established by the trace yet (a 5-bit and a 4-bit counter next to the vertical logic: my
expectation is the scan line counter and the vertical sync width counter, to be confirmed
from their outputs and clocks).

Not done: the carry-ins of `c4l0` and `c5l0` (they enter from the left column at rows u3
and u8), where the nine master outputs go (they leave the rows to the east), the sources
of the six clock and control lines, the pieces of the line x 3478 (the mid-right array's
"la" line), and everything the mid-right array's cell itself still lacks (the unresolved
branch of the next-value network).

## How it was found

`tools/findcell.py` with the master rectangle of each of the four columns of the counter
cell (chain, col2, col3, col4) against the left array: nine hits each at dx -8807,
dy -3339, -2862, -2384, -1907, -1343, -866, -389, +88, +566 from the master row, scores
0.88-0.92 in the clean shot (0.67-0.78 for two columns of the bottom row, where the
bottom row of a group differs as it does in the mid-right array). An overlay of a whole
instanced row on the metal shot sits on the photo (`row_chk.png`).

Mosaics of the nine row boundaries (`lk1.png`, `lk2.png`, `tb1.png`, `tb2.png`):

- carry links row N -> row N+1 exist below u0, u1, u2 and below u4, u5, u6, u7; not below
  u3 and u8. So the carry runs upward inside each group, bit 0 at the bottom, as in the
  mid-right array;
- no row has the drain-tab extension: there are **no look-ahead lines** here. The 5-bit
  counter is a plain ripple chain;
- at u3 and u8 a poly arrives from the left (the left column): the carry-in of each
  counter. Not drawn yet.

## Clock and control lines (read in the metal shot at 2.1x at both ends and in the channel)

| Line | 4-bit counter (u0-u3) | 5-bit counter (u4-u8) |
|---|---|---|
| master clock, L1 (x 3693) | `lc_ck_m` | the same line, unbroken through the channel |
| slave clock, rail x 4218 | `lc_ck_s` | the same rail, unbroken through the channel |
| L3 (second pull-down of `_nx_g`, x 3780) | `c4l_l3`: from the north, ends plainly at y 8500 | `c5l_l3`: the line that passes the 4-bit rows on the L2 position steps right in the channel onto L3 |
| pass-gate line "gab" (x 4095) | `c4l_gab`: from the north, ends plainly at y 8505 | `c5l_gab`: the line that passes the 4-bit rows at x 3968 turns east in the channel and comes down the gab position |

So unlike the three counters of the mid-right array, **these two share one master and one
slave clock**; they differ in their L3 and gab lines.

Top ends (y 6330-6580): four horizontal poly lines come from the west along y 6365, 6410,
6455 and 6500.

- y 6500: ends on a contact (3715,6497) at the top of L1: the master clock.
- y 6455: runs on east to a contact (4212,6455) at the top of the slave rail.
- y 6410: contact (3757,6410) at the top of the line that becomes the 5-bit counter's L3;
  and a second contact (3968,6410) under a metal that arrives from the north.
- y 6365: not looked at.
- `c5l_gab`'s line starts on a contact (3968,6520) fed by a poly from the east along
  y 6510-6530, and ends at the bottom on a contact (4087,11005).

The supply rails are named by structure (the cells are identical to the mid-right
array's): VSS x 3021, 3274, 3913; VCC x 3110, 3630, 4150. At the bottom the VSS rail
x 3913 runs into a wide horizontal metal (y 10930-10975).
