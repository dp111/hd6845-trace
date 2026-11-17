# rdp1: upper right datapath, top rows (x 13350-17050, y 5560-8050)

Serial work, 2026-11-16. Trace: `trace/rdp1.txt`. Views: `cache/scratch/rdp1/`.

## Status

All five rows are built from the cells of the rows below (`rdp3_lat`, `rdp2_xor`,
`rdp3_mpd`, `rdp3_mpd1`) and are instanced, wired and extracted: 284 transistors, no
errors. From the top:

| y | What | Slices | Compared with |
|---|---|---|---|
| 5710-6090 | comparator of **R5** (5 bits) and, 477 px to its right, comparator of **R3** (4 bits) | 5 + 4 | scan line counter `sl0`-`sl4`; horizontal sync width counter `hsw0`-`hsw3` |
| 6095-6365 | register **R5** (5 latches) and register **R3**, one nibble (4 latches) | 5 + 4 | |
| 6365-6900 | routing zone | | |
| 6902-7282 | comparator of **R7** | 7 | the seven counter lines `uc_b0`-`uc_b6` of the array below |
| 7289-7559 | register **R7** (7 latches) | 7 | |
| 7662-8042 | comparator of **R6** (its register row is rdp2's, below) | 7 | `uc_b0`-`uc_b6` |

Results: `sl_eq_r5`, `hsw_eq_r3`, `uc_eq_r7`, `uc_eq_r6` (each high when all its bits
match: a row-wide NOR of the per-bit XORs, as in the rows below).

Not done: where `sl_eq_r5` (leaves north), `hsw_eq_r3` and `uc_eq_r7` (leaves west along
y 6820) go; the data lines of R3 below their latch row; the tops of the data lines
(they go north in poly under the wide supply metal y 5450-5545); the tops of `ubus_b5`
and `ubus_b6`; the strap tracks that tap single register bits (below).

## How the rows were found and checked

`tools/findcell.py` with the latch cell (`rdp3_lat`, 14597,13010 to 14987,13280) finds two
rows of upside-down latches in this region (scores 0.66-0.72 in the clean shot): 7 at
y 7424 and 9 at y 6231; with the comparator slice (14410,10090 to 14790,10470) three rows
(scores 0.58-0.95). Overlays of the instanced cells sit on the metal shot
(`mid_m.png`, `top_m.png`, `top_m2.png`). The top rows are two groups: five slices on the
pitch of the array below and four more, 477 px (not 390) further right.

## What identifies the registers

- **R7**: its strobe poly (y 7529-7545) arrives from the wiring channel at (13425,7541),
  where `trace/mrach.txt` brings `wr_r7` up track T3.
- **R6's comparator**: its match line leaves west along y 7572-7588 to (13425,7585), the
  line the wiring channel takes down track T5 to the strobe channel's track k4. That
  track is therefore `uc_eq_r6`.
- **R5** (the five latches): the wiring channel's track T2 (`wr_r5`) ends on a contact
  (13170,6345); its poly runs east along y 6335-6355 into the first latch's strobe loop.
  The strobe line ends, rounded, at x 15355, after the fifth latch (3x view `stb1.png`).
- **R3** (the four latches): the line `wr_r3` from the north at x 13327 ends on a contact
  (13310,6387); its poly runs east along y 6377-6395 *below* the row to x 15437 and turns
  up into the strobe loop of the first of the four latches (`stb1.png`, `stb2.png`).

R5 shares the data lines `ubus_b0`-`ubus_b4` with R7, R6 and R4 (one metal each from
y 5632 to y 8815). R3 has four data lines of its own.

## What identifies the counters, and the bit order

- **R3's comparator against the mid-right 4-bit counter.** The four outputs of that
  counter leave the wiring channel northwards on tracks T0, T1, T3, T4. Each ends on a
  contact (y 6560, 6472, 6515, 6430) and goes east as a poly line across the routing
  zone to a contact under the counter track of one comparator slice: slice 0 takes bit
  0, ... slice 3 takes bit 3 (four 1.25x metal views of the zone, `rz1m`-`rz4m.png`).
  A 4-bit counter on the character clock compared with R3: the **horizontal sync width
  counter**, now `hsw0`-`hsw3`. That the nibble here is R3's *low* one (bits 0-3) now follows
  from the trace: its four data lines are data bus bits 0-3 (`notes/blocks/r3d.md`).
- **R5's comparator against the left array's 5-bit counter.** That counter's five output
  lines were followed and drawn 9,000 px from the left array to here
  (`trace/slbus.txt`, `notes/blocks/slbus.md`). Each ends on a contact under one counter
  track: slices 0-4 (left to right) take bits 0-4. A 5-bit counter compared with R5
  (vertical total adjust): the **scan line counter**, now `sl0`-`sl4`.
- **Bit order of the upper right array**: with that, the slices of this array (which the
  notes of `rdp2` call sm1, s0, ... s5 from the left) are bits 0 to 6, left to right. The
  names of R4, R6, R7, their comparators, `ubus` and `uc` now carry bit numbers.

One slip on the way, kept for the record: the first extraction gave "x = NOT nor" for the
last slice of each group. The last slice's series pair ends on a VSS land that belongs to
the *next* slice's rail; at the right end of a group that land is separate and had not
been placed. The two right-end lands (and the latch rows') are placed by analogy with the
rows below and marked uncertain in the trace.

## The routing zone (y 6365-6900): what was read

Ten horizontal poly lines enter from the west: `hsw3` (y 6430), `hsw2` (6472), `hsw1`
(6515), `hsw0` (6560), then `sl3` (6603), `sl2` (6645), `sl1` (6690), `sl4` (6732), `sl0`
(6775), and one more at y 6820 (R7's match line going out west, by the cell's exit; not
followed).

Seen, not drawn:

- The right group's rails shift 88 px west by diagonals at y 6560-6680 to become the
  rails of the array below.
- R3's four data lines below the latch row: drawn by `r3d` to the data bus (bits 0-3).
  `r3_b0_d` and `r3_b1_d` end on contacts (15490,6775) and (15880,6735) on poly lines east;
  `r3_b2_d` turns east as metal to a contact (16362,6688); `r3_b3_d` runs straight on. The
  metals south are x 16274, 16404, 16620, 16664 (`notes/blocks/r3d.md`).
- A thin metal on the strap track of the last R5 slice (x 15250-15277) comes down to a
  contact (15255,6815); poly east to a contact (15385,6815) at the top of a metal at
  x 15390 (`ubus_b5`'s position). So that track may be how `ubus_b5` reaches the north.
- The seven `uc` lines end at y 6864-6872, just above R7's comparator: nothing in this
  block drives them. They are fed in the routing zone of `rdp2` (y 9080-9560).

## Not done

Listed under Status. The routing zone deserves a full pass at 2.5x (about forty wires).
