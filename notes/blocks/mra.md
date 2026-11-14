# mra: mid-right vertical array (x 11700-13320, y 7200-17050)

## Status

- Surveyed: 19 rows at 477 px, in groups of 4, 3, 4, 4, 4 separated by routing channels.
- Traced, placed 19 times and checked instance by instance (two runs):
  - `mra_chain` (first run): the chain column x 11730-12060, the two group lines at x 11700,
    the supply rails at x 11828, 11917, 12081.
  - `mra_col2` (second run): x 12000-12470. The source of `g1` (an inverter from node `q`),
    the three-transistor stack between the chain and the row's bottom line `m`, the routes of
    `p3`, `q`, `n1`, `m` to x 12470, the VCC rail x 12412-12462 and signal line A x 12276-12294.
  - 248 transistors, extraction clean (0 errors, 0 warnings).
- NOT traced: one load at 12361-12400 x 10142-10200 and what it loads; what is under the poly
  block 12263-12350 x 10056-10091; everything right of x 12470 (about half of each row: where
  `q`, `p3` and `m` are made); the vertical lines there; the bus field x 13000-13320; the
  routing channels and both ends of the array.
- So the question "counter carry or comparator chain" is narrowed but not closed: the chain
  is an AND chain of the per-row node `q` (x(N) = x(N+1) AND q(N)); what `q` is (a counter
  bit, or a per-bit match) is decided right of x 12470. See Logic.

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

## Local colour legend for `acid1b` in this array (corrected in the second run)

Checked on the traced INV1 (view `cal_open.png`) and on the VSS ring of `mra_col2`.

| | under metal (and within about 10 px of a metal edge) | in the open |
|---|---|---|
| poly | bright smooth salmon, red outline | dark red / dark orange, textured; in the row median (`--comp mrarow`) often orange with a dark-red border |
| diffusion | flat tan / khaki, dark outline, specks at contacts | dull mauve to pale pink-tan, dark outline |
| field | pink | green in narrow gaps, olive elsewhere |

Traps met here:
- **Salmon is poly only under metal.** Bright salmon in the open next to a narrow metal line is
  still poly (the riser 12175-12192 x 10188-10290 next to the g1 strip): the chip-2 metal shot
  shows it brown. Pale tan in the open can be diffusion (the strip 12205-12222 x 10153-10330):
  decide with chip-2 `acid`, where poly is orange and diffusion is plain inside a dark outline.
- A metal line 18 px wide over field leaves a pink tongue with its own thin outline (under the
  g1 strip, 12155-12175 x 10170-10282). That outline is not layout.
- Straight dark lines the full height of a view in chip-2 `acid` are ghosts of metal edges.
  The VSS rail's right edge is at x 12115, not 12105 as drawn (harmless).
- Metal-contact discs: on poly a green disc on salmon; on diffusion grey specks on tan.
- The row median is sharper than a single row at 4-5x; `view.py ... --comp mrarow` in `metal`
  at 2-2.2x is the easiest way to read the metal.

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

| g1 route | band-1 pad 12110-12152 x 10105-10140, contact (12136,10122); metal strip x 12157-12175 down to contact (12171,10296) on poly pad 12152-12192 x 10281-10314; poly riser x 12175-12192, then right at y 10188-10205, down under line A (x 12281-12303) to buried contact 12279-12313 x 10281-10312 | `mra_col2` |
| inverter g1 = NOT q | gate 12227-12251 x 10270-10343 (hangs from the M1 pad); output diffusion 12251-12312 x 10283-10336; load block 12315-12375 x 10276-10338; VCC contact (12433,10305) | `mra_col2` |
| node q | metal M1 x 12226-12250, y 10047-10276; diffusion box 12209-12260 x 10045-10092, contact (12226,10066); neck and buried contact 12234-12266 x 10010-10038; poly y 10015-10034 to x 12437, up, then y 9977-9997 to the right | `mra_col2` |
| VSS link | VSS-land tongue onto poly pad (12183,10122); poly y 10119-10135, up at x 12283-12299, y 10096-10112; lower box 12350-12408 x 10066-10132, contact (12376,10098); metal "line C" x 12362-12390; upper box 12355-12402 x 9963-10008, contact (12374,9982) | `mra_col2` |
| p3 route | INV1 gate poly continues right at y 9972-9994 to pad + contact (12325,9982); metal "line B" x 12320-12338 (12331-12349 below y 10152) down to contact (12337,10240) on a poly pad; poly y 10231-10248 to the right | `mra_col2` |
| stack on node m | diffusion R 12079-12136 x 10153-10279 under the VSS rail, crossed by band-2 (y 10175-10196) and band-3 (y 10233-10256); middle of R -> neck -> box with contact (12014,10213) -> metal x 12003-12031 -> contact (12019,10353) on the pad of the bottom line (poly y 10364-10381, from x 12003 to the right) | `mra_col2` |
| VSS diffusion ring | bottom band 12100-12220 x 10325-10356 (joins the VSS box at (12068,10335)); strip 12205-12222 x 10153-10330; top band 12079-12222 x 10153-10168 (uncertain corner) | `mra_col2` |
| load 1, NOT traced | gate block 12361-12400 x 10142-10200, VCC box 12405-12473 x 10150-10198 with contact (12433,10172), output diffusion 12325-12360 x 10168-10199 | - |
| poly block, drawn `?P` only | 12263-12350 x 10056-10091, under lines A and B, between the q box and the lower VSS box | `mra_col2` |

## Logic (traced)

Per row N (names `mra_<net>_rN`). First-run pieces (chain column):

- `n1 = NOT p3`. INV1: pull-down 109/22, strong depletion load 85/39. `n1` runs right along
  the top of the row in poly (y 9924-9945) and left as a dead-end stub (H2).
- `n2 = NOT cin`, `cin` = chain poly from the row below.
- `x = NOR(g1, n2)` = cin AND NOT g1. Two pull-downs 57/22, load 32/42.
- Spare finger: third pull-down gated by `g1` from VSS to a tab; on a group line in rows
  r7-r10 and r15-r18, dead elsewhere.

Second-run pieces (`mra_col2`):

- **`g1 = NOT q`.** Inverter: pull-down 53/24 from the output diffusion to the VSS strip,
  gate = the poly hanging from the M1 pad (node `q`); depletion load 23/51 from the VCC rail
  x 12412-12462 (tie drawn `?B`). The output reaches the chain's band-1 by a buried
  contact, poly, a poly pad at (12171,10296), the metal strip x 12157-12175 and the pad at
  (12136,10122). So **x(N) = x(N+1) AND q(N)**: the chain is an AND chain of `q`.
- `q` is the node of metal M1: a diffusion box (12226,10066) + a buried contact to poly that
  runs right (y 10015-10034), up at x 12410-12437 and on to the right along the top of the
  row (y 9977-9997, port at x 12470). Nothing in x < 12470 drives it except whatever the
  untraced poly block 12263-12350 x 10056-10091 does (B1). It arrives from the right.
- `p3` (gate of INV1, so `n1 = NOT p3`) also arrives from the right: poly y 10231-10248,
  pad (12337,10240), metal line B, pad (12325,9982), poly y 9972-9994.
- Node `m` (the row's bottom line, poly y 10364-10381, which the first run called "H0" of
  the next row) has two transistors on the diffusion R under the VSS rail:
  - gate band-3 = `cin` (57/23): `m` <-> the bottom part of R (`mra_rb`), whose continuation
    is not resolved (B3);
  - gate band-2 = `b2` (57/21): `m` <-> the top part of R, which (by the uncertain `?D`
    pieces) continues along the top and down the right side of the g1 pad, under the g1
    poly (17/17, gate `g1`), to the VSS strip. As drawn: `m` is pulled to VSS when
    `b2 AND g1`, i.e. `b2 AND NOT q`.
  `m` leaves to the right (port at x 12470); no load on it was found left of x 12470.
- The VSS reaches two diffusion boxes at x 12350-12408 (lower, upper; joined by metal line C)
  through a poly link from a pad on a tongue of the VSS land. Nothing was found that uses
  the upper box; the lower box borders the untraced poly block (B1).

Chain (`cin` of each row), unchanged from the first run:

| Row | cin is | How |
|---|---|---|
| r0-r2, r4, r5, r7-r9, r11-r13, r15-r17 | x of the row below | poly straight down from band-3 into the next row's H1 blob |
| r3 | `mra_cin_r3`, undetermined | chain poly ends in a pad with a metal contact (11976,9187); see A1 |
| r6 | group line A | poly y 10893-10910 from the contact at (11699,10899) |
| r10 | `mra_cin_r10`, from outside | poly y 12897-12925 leaving left at x 11700 |
| r14 | group line B | poly y 14962-14985 from the contact at (11699,14972) |
| r18 | `mra_cin_r18`, from outside | poly down to y 17016, then right beyond x 12215 |

- Group line B = NOR(g1 of r15..r18) = AND(q of r15..r18), with a depletion load at its
  bottom end. Group line A = the same for r7..r10; no load found (A3).
- x of r0, r7, r11 and r15 end at their H1 blob and are used by nothing in the chain column.

What the traced logic shows, and what it does not:

- Traced: a ripple AND chain over `q`, bottom row first, with 4-row look-ahead lines
  (r18-r15 feeding r14-r11; r10-r7 feeding r6-r0). `cin` also gates a transistor on `m` in
  every row, so the chain value is used inside the row and not only passed up.
- Not shown: what `q` is. If `q` is a stored counter bit, x is the carry of an incrementer
  and `m` would be part of the toggle logic (m low when `b2 AND NOT q`, and something with
  `cin`). If `q` is a per-bit match (stored bit XNOR compare bit), x is a comparator's
  equality chain. Both fit everything traced so far. The decision is in x 12470-13000:
  follow `q` (y 9977-9997) and `m` (y 10364-10381) to the right.
- `b2` is driven by nothing found: its only other end is the stub under the metal strap of
  ambiguity A2, so the strap must contact it (see A2, now with this evidence).

## Ports

Coordinates are where the wire crosses the edge of what is traced (not always the region
boundary). Per-row ports are given for the master row r5; add the row's dy (Survey).

| Name | Layer | Where | Dir | What |
|---|---|---|---|---|
| vcc (rail) | M | x 11893-11942 at y 7130 (top, continues up) | in | VCC |
| vcc (bus) | M | y 17038-17066 at x 12230 (continues right) | in | VCC feed of the rail |
| vcc (rail 2) | M | x 12412-12462, drawn y 7265-16940; ends not followed | in | VCC of the two loads per row |
| vss (rail) | M | x 12055-12115 at y 7130 (top, continues up) | in | VSS |
| vss (rail x 11828) | M | ends at y 7265 and y 16940 | - | how it is fed was not found (A4) |
| `mra_la` | M | x 12276-12294, drawn y 7265-16940; ends not followed | ? | signal line through all rows, no contact in any row body |
| `mra_q_rN` | P | 12470, 9987 (y 9977-9997) | in | node q, from the right-hand columns |
| `mra_p3_rN` | P | 12470, 10240 (y 10231-10248) | in | gate of INV1, from the right-hand columns |
| `mra_n1_rN` | P | 12470, 9934 (y 9924-9945) | out | NOT p3, to the right-hand columns (jogs up to y 9905-9922 at x 12700-12720) |
| `mra_m_rN` | P | 12470, 10372 (y 10364-10381) | ? | bottom line of the row, to the right-hand columns |
| `mra_n1_r10` | P | 11700, 12459 | out | r10 only: the H2 stub is extended left to a contact at (11590,12460) on a vertical metal x 11580-11600 that runs up to about (11600,10500) and on, outside this block |
| `mra_cin_r10` | P | 11700, 12911 | in | leaves the region to the left |
| `mra_cin_r18` | P | 12215, 17016 | in | continues right |
| `mra_cin_r3` | M/P | strap x 11967-11989, y 9035-9518 | ? | see A1 |
| `mra_rb_rN` | D | 12100, 10268 | ? | bottom part of R, internal; continuation not resolved (B3) |
| `mra_qblk_rN` | P | 12300, 10075 | ? | poly block, internal; connection not resolved (B1) |
| gap-1 bus (6 poly lines) | P | y 9220-9425 at x 11700 | ? | not traced, pass under the rails |

No horizontal line leaves a row at the left edge (x 11700) except the two r10 lines above
and the group-line contacts: the bottom line `m` starts at its pad (x 12003) and the top
lines start inside the chain column.

## Row-to-row differences (measured with `cellcheck.py`)

- Chain cell (x 11725-12210): all 18 instances match the master; the only differences are
  the tab extension (r7-r10, r15-r18) and the row above/below at group edges.
- `mra_col2` (`--bbox 12000,9960:12470,10385`): all 18 instances match in both shots (bad
  blocks 0-2.2 % in `metal`, 1.1-4.5 % in `acid1b`, median correlation 0.95-0.97), including
  the bottom rows of the groups, so the bottom line `m` exists in r3, r6, r10, r14 and r18 too.
  The pictures were not looked at one by one (numbers only).
- Left margin (x 11545-11750): nothing is attached to the rows except the group-line
  contacts and, in r10 only, the extended n1 stub.
- Right-hand columns (`--bbox 12200,9880:13010,10400`, first run): identical in all 19 rows;
  bad blocks only along the top edge of r0, r4, r7, r11, r15 and the bottom edge of r3, r6,
  r10, r14, r18 (the routing channels). Not checked: whether the top rows of the groups
  (r0, r4, r7, r11, r15) have a poly line where the others have the `m` line of the row above.

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
  the right-hand columns. (b) is unlikely: the right-hand columns of r3 are identical to
  those of every other row. (a) is the reading to test first, e.g. on a better metal
  shot of (11978,9450).
- A2. The same metal strap exists in every row (from the band-2 stub of row N, y 10160,
  down to H2 of row N+1, y 9995+477), lying exactly over the chain poly, with no contact
  visible at either end. Drawn as isolated metal (`mra_md_rN`; `mra_mt_r0/r11/r15` where
  only the lower part exists). If it does connect to anything unseen, the candidates are
  the band-2 stub at its head and H1 or H2 at its tail. A thin strip (x 11985-11996,
  y 9990-10100) along the right edge of the INV1 load gate, visible in both stripped
  shots, starts where the strap ends; it was read as part of the load's active area.
  Second run: band-2 is a real gate (it crosses the diffusion R at 12079-12136 x
  10175-10196, between `m` and the VSS ring) and its poly has no other end than this stub
  (it stops at x 12153 on the right). A gate cannot float, so the strap must contact the
  stub (the stub, 35 x 74 px, is the size of a contact pad). Then `b2(N)` = whatever the
  strap's lower end is on: H2 of row N+1 (= `n1(N+1)` = NOT p3 of the row below) or the H1
  blob (= `x(N+1)` = cin(N), which would make band-2 and band-3 the same signal and is
  unlikely). Not drawn: no contact is visible. To settle: 5x views of (11978,10195) and
  (11978,10455) in `metal`, `metal1` and `acid1b`.
- A3. Group line A (rows r7-r10) has pull-downs but no load anywhere along its metal or
  along the poly to r6. Its net continues on band-3 of r6 into the right-hand columns;
  look there for the load (and for a term that brings in the carry of the lower groups).
  The right-hand columns of r6 are identical to the other rows', so if the load is there
  every row has one on band-3 (then x has two loads in ordinary rows).
- A4. The VSS rail at x 11828 ends at both ends of the array (y 7265, y 16940). It must be
  fed sideways (not found). Named vss because it is the source of all NOR pull-downs.
- A5 (11893-11912, 10258-10305). The load gate of INV2 is tied to n2 at the buried contact
  11882-11912 x 10278-10305; the stem from the gate block down into that contact is not
  resolved (drawn `?P`). The foot of the group-line-B load gate (11815-11870 x
  17066-17086) likewise.
- A6. In `acid1b` the INV1 load gate (x 11945-11984) is two-toned (textured left half,
  smooth right half) although no metal covers it in either metal shot. Read as one poly.

- B1 (12263-12350 x 10056-10091). A poly block under lines A and B, between the q diffusion
  box (left, 12209-12260) and the lower VSS box (right, 12350-12408). In `acid1b` it shows
  an upper band y 10054-10067 (tan-pink), a dark line, a lower band y 10070-10089 (bright
  salmon) and a thin tan strip y 10092-10100 below; in chip-2 `acid` both bands are orange,
  the upper one duller. No contact on it, no poly leaves it. Readings: (a) one poly block over
  a diffusion strip that joins the q box to the VSS box (channel 87 long, 19 wide): a weak
  pull-down of `q`, depletion if it is to do anything, gate tied at one end by a buried
  contact; (b) a gate y 10070-10089 between a diffusion strip above (part of the q box) and one
  below (part of the VSS box), W 87, L 19, gate connection unknown; (c) a capacitor from `q`
  to VSS. Drawn as an isolated `?P` (`mra_qblk`), no transistor. To settle: where its poly
  is tied (5x at its two ends, (12262,10075) and (12351,10080)), and whether line C really is
  VSS (B7).
- B2 (12301-12400 x 10134-10200). Load 1: gate block 12361-12400 x 10142-10200, VCC box with
  contact (12433,10172), output diffusion 12325-12360 x 10168-10199 under line B. Left of it,
  under line B's jog and line A: a pale box with a double outline (12301-12331 x 10136-10160),
  a salmon box with a heavy outline (12337-12359 x 10134-10162) and a tan area 12275-12305 x
  10150-10190 above the bend of the g1 poly. What the load pulls up was not resolved (it may
  be the load of `q`, of `m`, or of a node of the stack). Not drawn.
- B3 (12111-12140 x 10271-10310). The bottom part of R (`mra_rb`, below the cin gate) has a
  small tab at 12111-12132 x 10271-10282 towards the poly tab of the g1 pad (12127-12155 x
  10285-10308, dark-red blob in `acid1b`, orange in `acid`). Either R's bottom is a dead end
  (then the cin transistor does nothing), or it continues under that tab (a transistor gated
  by g1) or straight down into the VSS bottom band (then `m` is pulled low by cin alone).
  Drawn as a dead end with the tab as plain poly.
- B4 (12185-12222 x 10153-10215). The diffusion strip right of the g1 pad (12205-12222) is
  certain from y 10210 down to the VSS bottom band (one outlined region in chip-2 `acid`).
  Its continuation up under the g1 poly (y 10188-10205) and round the corner into the band
  along the top (y 10153-10168) to R is drawn `?D`: the corner is under the flare of the g1
  metal and was not resolved. If the corner is open, R's top part is a dead end and the
  17/17 transistor does not exist.
- B5 (12306-12327 x 10277-10332). The tie of the load-2 gate to the output: drawn `?B` at the
  left end of the block over the strip; what is visible is a dark-outlined blob at the
  block's upper left corner (12312-12327 x 10277-10297) next to a green (field) spot. The
  gate is on the output side either way.
- B6 (12346-12362 x 10094-10114). The VSS poly link ends at the left edge of the lower box
  with a rounded dark end; the buried contact is drawn `?B`.
- B7. That the pad at (12183,10122) is on the VSS land: metal is visible between the land's
  bottom edge and the contact in both metal shots, and `acid1b` is pink (under metal) between
  them, whereas above the neighbouring g1 pad it is green; the g1 pad's metal goes down
  instead. The contact rings themselves hide the join. If this is wrong, line C and the two
  boxes are some other net and B1 changes.
- B8. The loop of dark line 7-9 px wide round the g1 pad (12137-12205 x 10165-10324) is read
  as the inner edge of the VSS diffusion ring (its bottom and right sides certainly are);
  along the left side (x 12137-12145) it runs next to R's right edge. Inside it: field, the
  g1 poly pad, riser and tab.

## Not done

- x 12470-13000 of every row: where `q`, `p3` and `m` come from, the storage, the read
  gates. Seen but not traced (master row): n1 jogs up to y 9905-9922 at x 12700-12720; `q`
  (y 9977-9997) continues at least to x 12760; vertical metal at x 12472-12487, 12488-12502
  (contact (12493,10043)), 12520-12533, 12553-12573, 12597-12617 with diagonal jogs at
  y 9900-10010; contact (12592,10113); wide rail x 12701-12750 with contacts (12715,10233)
  and (12715,10338); line x 12766-12790; contacts (12847,10006), (12896,10036), (12857,10087)
  inside a U-shaped gate 12813-12882 x 10033-10113, (12957,10161) on the wide rail
  x 12931-12982, (12858,10292), (12840,10340), (13017,10043) on the line x 13012-13038; a
  second U-shaped gate at 12950-13000 x 10029-10108. Large diffusion areas under metal there
  (big transistors).
- Load 1 and the poly block (B1, B2); the continuation of R's bottom part (B3).
- Both ends of the array: where line A (x 12276-12294) and the VCC rail x 12412-12462 go
  above y 7265 and below y 16940, and the other vertical lines.
- The bus field: about ten vertical metal lines at x 13050-13330 (centres found by
  `sel_cut.py` in the master row: 13086, 13130, 13173, 13216, 13260, 13303, pitch 43.5). At
  the top (y 7330-7560) they end in a staircase of contacts ((13125,7350) (13125,7395)
  (13170,7445) (13170,7515) (13210,7555) ...), i.e. the bundle turns left there. Rows send
  horizontal lines under it to the right (for example from (12990,10395) diagonally to
  (13330,10000); several at y 10900-10960, 11400, 11890). Which row taps which line was
  not read.
- The routing channels (y 9182-9435 etc.) and what the six-line poly bus in the first one
  connects; whether the top rows of the groups have a line in the place of `m` of the row above.
- Above the top row (y 7130-7265) and below the bottom row (y 16945-17050): three
  horizontal poly lines at y 7155, 7205 and the row's own top lines; not traced.
- The instance pictures of `cellcheck.py` for `mra_col2` were not looked at (numbers only).
