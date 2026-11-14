# mra: mid-right vertical array (x 11700-13320, y 7200-17050)

## Status

- Surveyed: 19 rows at 477 px, in groups of 4, 3, 4, 4, 4 separated by routing channels.
- Traced, placed 19 times and checked instance by instance: the left ("chain") column of
  every row, x 11730-12200, with its per-row variations, the two group lines at x 11700
  and the three supply rails at x 11828, 11917, 12081. 153 transistors, extraction clean.
- NOT traced: everything right of x 12200 (the register/latch columns, about 3/4 of each
  row), the vertical signal lines there, the bus field x 13000-13320, the routing
  channels. So the questions "which column is which register" and "which row is which
  bit" are still open; see Not done.

## Survey

- Rows (tag, dy from the master row r5 at y 9912-10389, dx):
  r0 -2646, r1 -2169, r2 -1692, r3 -1215 | r4 -477, r5 0, r6 +477 | r7 +1040,
  r8 +1518 (dx 1), r9 +1995, r10 +2472 | r11 +3123, r12 +3601, r13 +4077, r14 +4554 |
  r15 +5097, r16 +5574, r17 +6051, r18 +6528 (dx 2). (dx 1 from r8 on.)
- All 19 rows score 0.87-0.89 against each other in `findcell.py` over x 11750-12950, so
  the row is one cell to first order. Median composite of the 19 rows:
  `composite.py mrarow 11660,9880:13060,10440`; view with `--comp mrarow`.
- Routing channels between groups: y 9182-9435 (six horizontal poly bus lines at
  y 9230, 9272, 9315, 9357, 9402 and one more, crossing the whole array and leaving left
  past x 11700), y 10874-10952, y 12869-13035, y 14951-15009.
- Vertical metal through all rows: VSS x 11803-11852, VCC x 11893-11942, VSS
  x 12055-12105 (traced); wide rails at x 12412-12455, 12700-12745, 12935-12990 and thin
  signal lines at about x 12265-12300, 12490-12620 (three or four, jogging), 12760-12830,
  12890-12915 (not traced, not identified).
- x 13000-13320: about 8 vertical metal lines (believed the internal data bus), not traced.
- Per row there are three horizontal poly lines along the top (y 9882-9900, 9924-9945,
  9970-9995 in the master) and three in the middle (y 10112-10133, 10158-10178,
  10245-10262) that run from the chain column to the right into the untraced columns.

## Local colour legend for `acid1b` in this array

Under metal: poly salmon, diffusion pale tan, field magenta-pink. In the open: poly dark
red-brown with a green rim, diffusion mauve, field olive/green. The gaps between the
vertical metals show as columns of green ovals (field) and dark ovals (poly crossing).
Contacts to poly show a clear ring in both metal shots (compare 11762,9927).

## Inventory (master coordinates; add the row's dy)

| Piece | Where | Cell |
|---|---|---|
| INV1 | active strip 11893-12192 x 10003-10088, buried contact 12003-12035 x 9960-9998 | `mra_chain` |
| spare driver finger + tab | 11735-11872 x 10022-10095 | `mra_chain` (+ `mra_tabx` in r7-r10, r15-r18) |
| NOR driver (node x) | 11745-11935 x 10112-10378 | `mra_chain` |
| INV2 | 11862-12100 x 10142-10360 | `mra_chain` |
| chain poly / strap to the next row | x 11958-11992 | `mra_link` (13 rows), explicit pieces for r3, r6, r10, r14, r18 |
| group line A | metal x 11689-11711, y 10888-12575 | explicit |
| group line B + load | metal x 11689-11711, y 14960-17062; load 11780-11955 x 17008-17088 | explicit |

## Logic (traced)

Per row N (names `mra_<net>_rN`):

- `n1 = NOT p3`. INV1: pull-down gate is the diagonal poly `p3` from the right (W/L
  109/22), strong depletion load (85/39) from the VCC rail. `n1` leaves to the right in
  poly at y 9924-9945 (H1') and also runs left as a dead-end poly stub (H2, y 9965-9988,
  ends at x 11737).
- `n2 = NOT cin`, where `cin` is the chain poly from below (gate x 11963-11986 crossing
  the strip y 10268-10321).
- `x = NOR(g1, n2)` = cin AND NOT g1. Two pull-downs 57/22 under the VSS rail, depletion
  load 32/42. `g1` is the poly "band-1" (y 10112-10133) that arrives from the right.
- `x` goes by metal (x 11752-11790) to poly H1 (y 9922-9943) and ends in a blob at
  x 11960-11998, y 9908-9945.
- Spare finger: a third pull-down gated by `g1` (70/20) from the VSS rail to a diffusion
  tab at the left edge. In rows r0-r6 and r11-r14 the tab ends at x 11735 with no contact
  (dead). In rows r7-r10 and r15-r18 it is extended to a contact on a group line.

Chain (`cin` of each row):

| Row | cin is | How |
|---|---|---|
| r0-r2, r4, r5, r7-r9, r11-r13, r15-r17 | x of the row below | poly straight down from band-3 (y 10245-10262) into the next row's H1 blob |
| r3 | `mra_cin_r3`, undetermined | chain poly ends in a pad with a metal contact (11976,9187); see ambiguity A1 |
| r6 | group line A | poly y 10893-10910 from the contact at (11699,10899) |
| r10 | `mra_cin_r10`, from outside | poly y 12897-12925 leaving left at x 11700 |
| r14 | group line B | poly y 14962-14985 from the contact at (11699,14972) |
| r18 | `mra_cin_r18`, from outside | poly down to y 17016, then right beyond x 12215 |

- Group line B = NOR(g1 of r15, r16, r17, r18): four spare fingers pull it down, a
  depletion load at its bottom end (11780-11955 x 17018-17062, gate tied by the buried
  contact 11803-11834 x 17058-17088) pulls it up to the VCC rail.
- Group line A = wired NOR of g1 of r7, r8, r9, r10 by the same construction, but no load
  was found on it (see A3).
- x of r0, r7, r11 and r15 (the top row of each chain group) end at their H1 blob and are
  used by nothing in the chain column.

Believed (not traced): this is a ripple chain with group look-ahead, bottom row first:
"all rows below me in my group have g1 low, and the group's carry-in is high". With
g1 = NOT q it is the carry chain of a counter whose least significant bit is r18 and
which is split r18-r15, r14-r11, r10-r7, r6-r0; with g1 = bit mismatch it is the equality
chain of a comparator. The look-ahead lines (which skip a whole group) favour a counter,
and r0's unused output would be the carry out of the top bit. Which one it is depends on
what drives g1 in the untraced columns. If it is a counter, this array is itself an
address counter rather than only registers, which contradicts the working assumption
that the left array holds the memory address counter: check against that block.

## Ports

Coordinates are where the wire crosses the edge of what is traced (not always the region
boundary).

| Name | Layer | Where | Dir | What |
|---|---|---|---|---|
| vcc (rail) | M | x 11893-11942 at y 7130 (top, continues up) | in | VCC |
| vcc (bus) | M | y 17038-17066 at x 12230 (continues right) | in | VCC feed of the rail |
| vss (rail) | M | x 12055-12105 at y 7130 (top, continues up) | in | VSS |
| vss (rail x 11828) | M | ends at y 7265 and y 16940 | - | how it is fed was not found (A4) |
| `mra_p3_rN` | P | 12200, 9982+dy | in | from the right-hand columns |
| `mra_n1_rN` | P | 12130, 9934+dy | out | to the right-hand columns |
| `mra_g1_rN` | P | 12130, 10122+dy | in | from the right-hand columns |
| `mra_b2_rN` | P | 12130, 10168+dy | ? | band-2, ends in a stub under the strap at x 11950-11985 |
| `mra_x_r(N+1)` on band-3 of row N | P | 12130, 10253+dy | out | the row's cin, continuing to the right-hand columns |
| `mra_cin_r10` | P | 11700, 12911 | in | leaves the region to the left |
| `mra_cin_r18` | P | 12215, 17016 | in | continues right |
| `mra_cin_r3` | M/P | strap x 11967-11989, y 9035-9518 | ? | see A1 |
| gap-1 bus (6 poly lines) | P | y 9220-9425 at x 11700 | ? | not traced, pass under the rails |

## Ambiguities

- A1 (11978, 9187-9518). The chain poly of r3 cannot go straight down (six poly bus lines
  cross the channel), so it ends in a pad with a metal contact at (11976,9187) and a
  metal strap (x 11967-11989) carries on down to r4, over r4's H1 blob (y 9431-9468) and
  H2 (y 9488-9511), ending at y 9518. For the chain to continue the strap must contact
  r4's H1 blob (x of r4). No contact ring is visible there in either metal shot and no
  pale disc in the stripped shots, whereas the contacts at (11976,9187) and (11762,9927)
  are obvious. Working assumption: none drawn; `mra_cin_r3` is left as an open port.
  Candidates: (a) a contact to r4's H1 blob that does not show (then cin(r3) = x(r4) and
  r0-r6 is one seven-row ripple group); (b) cin(r3) is driven through band-3 of r3 from
  the right-hand columns. Tracing band-3 of r3 to the right settles (b).
- A2. The same metal strap exists in every row (from the band-2 stub of row N, y 10160,
  down to H2 of row N+1, y 9995+477), lying exactly over the chain poly, with no contact
  visible at either end. Drawn as isolated metal (`mra_md_rN`; `mra_mt_r0/r11/r15` where
  only the lower part exists). If it does connect to anything unseen, the candidates are
  the band-2 stub at its head and H1 or H2 at its tail. A thin strip (x 11985-11996,
  y 9990-10100) along the right edge of the INV1 load gate, visible in both stripped
  shots, starts where the strap ends; it was read as part of the load's active area.
- A3. Group line A (rows r7-r10) has pull-downs but no load anywhere along its metal or
  along the poly to r6. Its net continues on band-3 of r6 into the right-hand columns;
  look there for the load (and for a term that brings in the carry of the lower groups).
- A4. The VSS rail at x 11828 ends at both ends of the array (y 7265, y 16940). It must be
  fed sideways (not found). Named vss because it is the source of all NOR pull-downs.
- A5 (11893-11912, 10258-10305). The load gate of INV2 is tied to n2 at the buried contact
  11882-11912 x 10278-10305; the stem from the gate block down into that contact is not
  resolved (drawn `?P`). The foot of the group-line-B load gate (11815-11870 x
  17066-17086) likewise.
- A6. In `acid1b` the INV1 load gate (x 11945-11984) is two-toned (textured left half,
  smooth right half) although no metal covers it in either metal shot. Read as one poly.

## Not done

- Columns x 12200-13000 of the row (the bulk: latches, read gates, whatever drives `p3`
  and `g1`, the loads). Start from the composite; views `c2_*.png` in the scratch folder
  show x 12050-12420. Landmarks seen but not traced: VSS land contacts at (12160,10022)
  (12118,10063) (12160,10063); metal x 12003-12032 from a diffusion contact (12014,10213)
  to a poly contact (12016,10352); contacts at (12135,10120), (12183,10120),
  (12170,10295), (12225,10052), (12238,10255), (12325,9977), (12372,9980), (12372,10095);
  rail contacts (12432,10170), (12432,10305), (12712,10240), (12712,10345), (12955,10157).
- The vertical signal lines in those columns and where they leave at y 7200 and y 17050.
- The bus field x 13000-13320 and the connections of each row to it (this is what would
  give the bit order).
- The routing channels (y 9182-9435 etc.) and what the six-line poly bus in the first one
  connects.
- Above the top row (y 7130-7265) and below the bottom row (y 16945-17050): three
  horizontal poly lines at y 7155, 7205 and the row's own top lines; not traced.
- Row-to-row differences right of x 12210 were not checked (`cellcheck.py` was only run
  on the chain cell).
