# mra: mid-right vertical array (x 11700-13320, y 7200-17050)

## Status

**What it is (fourth run, serial session 2026-11-15): 19 bits of synchronous two-phase
counter**, in the chain groups the first run found (r18..r11: eight bits, carry in at r18;
r10..r4 and r3..r0: carry in at r10, see A1 for the r3/r4 link). Each row is one counter
bit: a master latch `a` loaded during `ck_b`, a slave node `q` loaded during `ck_a`, and
the toggle logic `m` between them. The earlier statement that "`q` is not made in the row"
was wrong: the `q` poly ends in a buried contact on the `ck_a` pass gate.

- Traced, placed 19 times, checked instance by instance, 629 transistors with
  `trace/trunks.txt` loaded, extraction clean (0 errors, 0 warnings):
  - `mra_chain` (first run): the chain column x 11730-12060, group lines at x 11700, rails.
  - `mra_col2` (second and third runs): x 12000-12470. `g1 = NOT q`, the network on `m`,
    routes of `p3`, `q`, `n1`, `m`; the hold device between `q` and net `z`.
  - `mra_col3` (third run): x 12470-12770. Loads of `na` and `nb`, `nb = NOT m`, the `ck_b`
    pass gate `na <-> a`, the `ck_a` pull-down of `na`, the pull-down of `p3`.
  - `mra_col4` (fourth run): x 12750-13045. `nb`'s pull-down of `na`; node `a` and its
    second `ck_b` gate to node `b`; `p3 = NOT a` with its load; `d = NOT p3` with its load;
    the `ck_a` gate `d <-> q`; the long feedback device `d <-> a` gated by `b`; `z` and `n1`
    on to the right edge.
- NOT traced: load 1 and its node (B2) and the unresolved branch of `m` (B3, B4): **`m` still
  has no pull-up and only half its pull-down network**, so the toggle function is believed
  (XOR), not extracted. The wiring channel x 13040-13375 (where `n1` and `z` go), the
  routing channels and both ends of the array; the line x 12767-12782.

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
| hold device (third run) | gate: VSS-land tongue onto poly pad (12183,10122); poly y 10119-10135, up at x 12263-12279 into the block 12264-12346 x 10056-10101; strip y 10072-10088 from the q box to the lower box | `mra_col2` |
| net `z` | lower box 12350-12408 x 10066-10132, contact (12376,10098); metal "line C" x 12362-12390; upper box 12355-12402 x 9963-10008, contact (12374,9982); strip y 9957-9969 to x 12750 | `mra_col2`, `mra_col3` |
| p3 route | INV1 gate poly continues right at y 9972-9994 to pad + contact (12325,9982); metal "line B" x 12320-12338 (12331-12349 below y 10152) down to contact (12337,10240) on a poly pad; poly y 10231-10248 to the right | `mra_col2` |
| stack on node m | diffusion R 12079-12136 x 10153-10279 under the VSS rail, crossed by band-2 (y 10175-10196, = n2: its stub under the metal strap is joined to the INV2 load gate block by poly 11932-11962 x 10207-10228) and band-3 (y 10233-10256, = cin); middle of R -> neck -> box with contact (12014,10213) -> metal x 12003-12031 -> contact (12019,10353) on the pad of the bottom line (poly y 10364-10381, from x 12003 to the right) | `mra_col2` |
| VSS diffusion ring | bottom band 12100-12220 x 10325-10356 (joins the VSS box at (12068,10335)); strip 12205-12222 x 10153-10330; top band 12079-12222 x 10153-10168 (uncertain corner) | `mra_col2` |
| load 1, NOT traced | gate block 12361-12400 x 10142-10200, VCC box 12405-12473 x 10150-10198 with contact (12433,10172), output diffusion 12325-12360 x 10168-10199 | - |

## Logic (traced)

One row N as equations, state after the third run. **Traced** (extracted from the trace):

```
g1  = NOT q                      q: line from outside (right), hold device q <-> z, gate VSS
x   = cin AND q                  cin = x of the row below, or a group line, or external (table below)
n2  = NOT cin
n1  = NOT p3                     p3: line from the right-hand part; n1 goes back right
m   : pulled low through [n2] -> [g1 52/17] -> VSS (the band joining the two is `?D`, B4)
      and through [cin] -> node rb (not resolved, B3); no pull-up found
nb  = NOT m                      load 4; nb gates something not resolved (C4)
na  = NOT ck_a                   load 3, pull-down gated by L3 (ck_a by trunks.md)
u  <-> na  while ck_b            pass gate 63/21 on L1
d2  : pulled low by gb           neither followed
```

**Believed, not traced**: `m = NOT(cin XOR q)` or a similar function of cin and q (second
run); u = node A, joined to node B by a second, larger `ck_b` pass gate; the `ck_a` rail
gates a third big pass gate at x 12947. Not known: what q is outside the array, what is
stored and where, what leaves the row besides `n1`.

Tools of the third run: `tools/mra_prof.py` (colours along a cut, raw or as class runs;
use `--raw`, the classes are rough) and `tools/mra_runs.py` (metal runs along cuts of the
median or of the die; lines over poly and diffusion drop out, so read several cuts).


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
  row (y 9977-9997) and, third run, on to x 13045 (y 9957-9974 from x 12784) with no
  transistor on it. Nothing in the row drives it; the hold device is its only other
  connection. It arrives from the wiring channel on the right.
- `p3` (gate of INV1, so `n1 = NOT p3`) also arrives from the right: poly y 10231-10248,
  pad (12337,10240), metal line B, pad (12325,9982), poly y 9972-9994.
- Node `m` (the row's bottom line, poly y 10364-10381, which the first run called "H0" of
  the next row) has a two-branch network on the diffusion R under the VSS rail. The two
  gates are complementary: band-3 is `cin`, band-2 is `n2 = NOT cin` (the band-2 stub is
  joined to the INV2 load gate block, which is tied to n2; found at 6x, view `a2b.png`).
  - gate `n2` (57/21): `m` <-> the top part of R, which (by the uncertain `?D` pieces, B4)
    continues along the top and down the right side of the g1 pad, under the g1 poly
    (17/17, gate `g1`), to the VSS strip. As drawn: `m` is pulled to VSS when
    `NOT cin AND NOT q`.
  - gate `cin` (57/23): `m` <-> the bottom part of R (`mra_rb`), whose continuation is not
    resolved (B3).
  `m` leaves to the right (port at x 12470); no load on it was found left of x 12470.
- **Hold device (third run).** The poly from the pad on the tongue of the VSS land is the gate
  of a load-shaped device, W/L 16/82, between the q box and the lower of two diffusion
  boxes at x 12350-12408. The boxes are joined by metal line C and the upper one continues
  as a narrow diffusion strip to x 12750: net `z`. Gate at VSS means a depletion device (as
  in cdp2, rdp3, larr: tagged `kind=hold`): a weak link `q <-> z`. Nothing else was found on
  `z` (C2), so what the link is for is not shown.

Third-run pieces (`mra_col3`), traced:

- `nb = NOT m`: pull-down 30/23 gated by the end of the `m` line, depletion load 27/73 (load 4).
  `nb` leaves by a metal strap to a poly that runs up at x 12653-12680, y 10030-10108, and is a
  gate there; what it crosses is not resolved (C4).
- `na`: depletion load 27/48 (load 3); pulled to VSS through a transistor 40/22 gated by L3
  (`mra_cka2`, believed `ck_a`); connected to node `u` through a pass transistor 63/21 gated
  by L1 (`ck_b`). As extracted: `na = NOT ck_a`, and `u <-> na` while `ck_b`.
- `d2` is pulled to VSS by a transistor 62/17 whose gate `gb` is the vertical poly under the
  rail; neither `d2` nor `gb` has been followed.
- `q`, `p3`, `n1` pass through this column as plain poly: no transistor on them here.

Believed (not traced): `u` is node A of the right-hand part, which a second, larger `ck_b`
pass gate joins to node B; so during `ck_b` the nodes B, A (= u) and `na` are connected, and
during `ck_a` `na` is held low. That makes `na`/`u` a precharged or discharged line rather
than a stored bit, but it cannot be stated until A, B and the `ck_a` gate at x 12947 are
traced.

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
  (r18-r15 feeding r14-r11; r10-r7 feeding r6-r0). In every row the chain value and its
  inverse gate the two branches of a network on the row node `m`, one branch of which also
  goes through a transistor gated by `g1 = NOT q`.
- Third run: `q` is not a bit stored in the row but a line from outside, and `m` feeds an
  inverter and the clocked part, so the "counter bit" reading below is no better supported
  than "comparator with its result latched"; neither is shown.
- Believed by the second run: this is a counter (incrementer), not a comparator. A network on a per-row node
  with one branch enabled by cin and the other by NOT cin, combined with q, is the shape of
  the bit's toggle logic (next = q XOR carry-in: `m` = NOT(NOT cin . NOT q + cin . q) if the
  unresolved cin branch ends in a transistor gated by q). An equality chain has no use for
  its own running value inside the bit. The carry would then enter at r18 and at r10
  (`mra_cin_r18`, `mra_cin_r10`), least significant bit at the bottom of each chain.
- Not shown: the cin branch beyond R (B3), the load of `m`, and what `q` and `p3` are
  (stored bit, its master, a match?). That is in x 12470-13000: follow `q` (y 9977-9997),
  `p3` (y 10231-10248) and `m` (y 10364-10381) to the right.

## Ports

Coordinates are where the wire crosses the edge of what is traced (not always the region
boundary). Per-row ports are given for the master row r5; add the row's dy (Survey).

| Name | Layer | Where | Dir | What |
|---|---|---|---|---|
| vcc (rail) | M | x 11893-11942 at y 7130 (top, continues up) | in | VCC |
| vcc (bus) | M | y 17038-17066 at x 12230 (continues right) | in | VCC feed of the rail |
| vcc (rail 2) | M | x 12412-12462. Top: continues up past y 7090. Bottom: runs into the horizontal VCC bus y 17035-17093 | in | VCC of the two loads per row |
| vss (rail) | M | x 12055-12115 at y 7130 (top, continues up) | in | VSS |
| vss (rail x 11828) | M | ends at y 7265 and y 16940 | - | how it is fed was not found (A4) |
| `mra_la`, `mra_la2`, `mra_la3` | M | x 12276-12294, **three pieces** (y 7110-12885, 13030-14965, 15010-16940; found 2026-11-16 from block wl). Top piece: contact (12285,7124) onto band H2 east, which ends on the gate of inverter I1 in `wl`. No contact found in any row or at the other ends: re-read item R8 | ? | not one through-line as first drawn; something on it has been missed |
| `mra_q_rN` | P | 12840, 9965 (y 9957-9974); seen to x 13045 | in | node q, from the wiring channel on the right |
| `mra_p3_rN` | P | 12765, 10286 (y 10277-10296, under the rail) | in | gate of INV1, from the right-hand columns |
| `mra_n1_rN` | P | 12765, 9913 (y 9905-9922); seen to x 13045 | out | NOT p3, to the right |
| `mra_m_rN` | P | internal: ends at x 12649 as the gate of `nb` | - | row node; its pull-up has not been found |
| `mra_nb_rN` | P | 12666, 10030 (top of the poly x 12653-12680) | out | NOT m; gate of something not resolved (C4) |
| `mra_u_rN` | D | 12610, 10024 (y 10012-10036); band y 10012-10026 on to x 12790 | ? | node above the `ck_b` gate; believed node A |
| `mra_d2_rN` | D | 12770, 10150 | ? | drain of the `gb` transistor |
| `mra_gb_rN` | P | 12738, 10050 and 10194 (both ends of the poly) | in | gate under the rail; source not found (C3) |
| `mra_z_rN` | D | strip y 9957-9969 ends at x 12750 | ? | far side of the hold device (C2) |
| `mra_n1_r10` | P | 11700, 12459 | out | r10 only: the H2 stub is extended left to a contact at (11590,12460) on a vertical metal x 11580-11600 that runs up to about (11600,10500) and on, outside this block |
| `mra_cin_r10` | P | 11700, 12911 | in | leaves the region to the left |
| `mra_cin_r18` | P | 12215, 17016 | in | continues right |
| `mra_cin_r3` | M/P | strap x 11967-11989, y 9035-9518 | ? | see A1 |
| `mra_rb_rN` | D | 12100, 10268 | ? | bottom part of R, internal; continuation not resolved (B3) |
| gap-1 bus (6 poly lines) | P | y 9220-9425 at x 11700 | ? | not traced, pass under the rails |

**Vertical lines through the rows, third run** (x measured on the median of the rows with
`tools/mra_runs.py`, body of the row y 10045-10290; ends measured on the die at y 7200-7330
and y 16880-17010). "T" = position in the top 100 px of a row, where the thin lines jog.

| Line | x in the body | T / jog | Top end of the array | Bottom end | Net |
|---|---|---|---|---|---|
| VCC rail | 12412-12462 | straight | continues up | into the VCC bus y 17035 | `vcc` |
| L1 | 12493-12507 | T 12496-12508, out to 12508-12528 at y 9916-9964 | seen at 12512-12520, y 7320; not seen above y 7310 | 12519-12532 at y 16920-16990, turns right along y 17000 | **`ck_b`** (joined to `trunks.txt`) |
| L2 | 12536-12550 | T 12559-12572 | seen at 12562-12571, y 7320; not above | 12563-12575, ends about y 16940 | `mra_l2`, **no contact in the rows as far as traced**; not identified |
| L3 | 12580-12594 | T 12606-12615 | 12604-12616, continues up past y 7240 | 12607-12618, ends about y 16940 at the contact (12631,16954) | `mra_cka2`; `ck_a` by `trunks.md` (second route, not drawn there) |
| rail | 12696-12744 | straight | continues up (12696-12739 at y 7240) | 12700-12742, ends about y 16935 | `vss` (by structure) |
| line | 12767-12782 | jogs to 12761-12790 at y 9950-9990 | not seen | 12773-12792, ends about y 16935 | not traced |
| line | 12810-12821 | from the contact (12847,10006) down | - | - | node A of each row? (per row or through: not established) |
| line | 12852-12868 | from the contact (12857,10087) down | - | - | node B? (same) |
| line | 12896-12908 | straight | 12890-12897 at y 7240 | 12889-12898, down to the contact (12893,16989) | `ck_b` (by the bottom contact; not drawn) |
| wide rail | 12936-12978 | straight | continues up | 12938-12980, continues down | VCC? (contact (12957,10161) per row) |
| `ck_a` rail | 13013-13037 | straight | 13016-13032 at y 7300 | 13018-13032 | `ck_a` (`trunks.txt`; taps (13017,10043) per row not drawn) |

Older table (second run, 1x views):

Vertical metal right of x 12470, seen at 1x at the two ends (views `end_t2.png`,
`end_b2.png`) and by `sel_cut.py`; none of it is traced, x to about 3 px:

| Line | In the rows | Top end (y 7090-7330) | Bottom end (y 16860-17110) |
|---|---|---|---|
| x 12505-12534 | one of the jogging lines | not followed | turns right at y 16986-17005 and runs to a contact at (12893,16989) |
| x 12559-12578 | jogging line | not followed | ends at y 16942 |
| x 12600-12619 | straight line | continues up past y 7090 | contact at (12628,16952) onto poly that runs right to x 12733 |
| x 12690-12750 | wide rail | continues up, widening to the right (x 12690-12800 at y 7090-7140) | ends at y 16940 |
| x 12767-12797 | line | not followed | ends at y 16942 |
| x 12874-12912 | line | contact at (12889,7214) onto the poly line y 7200-7225 | down to the contact at (12893,16989) |
| x 12928-12986 | wide rail | continues up past y 7090 | continues down and meets the horizontal VCC bus (so probably VCC) |
| x 13010-13038 | row line, contact (13017,10043) in every row | contact at (13023,7277), poly y 7265-7285 right to a contact at (13258,7275) | contact at (13023,16989); a line x 13049-13074 leaves downward |
| x 13078-13097, 13117-13136, 13160-13180, 13204-13224, 13248-13267 | wiring channel | continue up past y 7090 (13248-13267 has the contact at (13258,7275)) | 13117-13136, 13160-13180, 13204-13224 continue down past y 17110; the other two have ended |
| x 13292-13315, 13337-13357 | wiring channel | absent at the top | continue down past y 17110 |
| x 13316-13335 | - | a line present only at the top | - |

Three horizontal poly lines cross the whole width above the top row: y 7120-7138 (from the
line A contact leftward), y 7158-7187 and y 7200-7225.

No horizontal line leaves a row at the left edge (x 11700) except the two r10 lines above
and the group-line contacts: the bottom line `m` starts at its pad (x 12003) and the top
lines start inside the chain column.

## Row-to-row differences (measured with `cellcheck.py`)

- Chain cell (x 11725-12210): all 18 instances match the master; the only differences are
  the tab extension (r7-r10, r15-r18) and the row above/below at group edges.
- `mra_col2` (`--bbox 12000,9960:12470,10385`): all 18 instances match in both shots (bad
  blocks 0-2.2 % in `metal`, 1.1-4.5 % in `acid1b`, median correlation 0.95-0.97), including
  the bottom rows of the groups, so the bottom line `m` exists in r3, r6, r10, r14 and r18 too.
  Third run: the difference pictures of r0, r3, r4, r6, r7, r10, r11, r14, r15, r18 were
  looked at as one montage (`cc2_acid1b.png`): the same structure in all; isolated bad blocks
  at the contact (12337,10240), at the bottom edge near x 12365 and along the top edge.
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
  Second run (views `a1b.png`, r4 at 4.5x in three shots, and `a1c.png`, the same place in
  the median of all rows at 6x): still no ring in either metal shot and no disc in `acid1b`
  on r4's H1 blob or on H2 under the strap. In r4 alone `acid1b` shows a slightly paler patch
  on the blob under the strap (11972-11990 x 9438-9463); the median of the rows does not.
  What has changed is the argument: A2 shows that in ordinary rows the strap touches nothing
  at its head, so there it can be dead metal; in r3 its head is on the chain poly, so the
  strap is the only possible source of cin(r3) and must end on a driven node. A foot contact
  in r4 therefore exists; H1 blob (x of r4, reading (a)) is the reading that continues the
  chain, H2 (n1 of r4) the alternative. Still not drawn, `mra_cin_r3` stays an open port.
- A2. The same metal strap exists in every row (from the band-2 stub of row N, y 10160,
  down to H2 of row N+1, y 9995+477), lying exactly over the chain poly, with no contact
  visible at either end. Drawn as isolated metal (`mra_md_rN`; `mra_mt_r0/r11/r15` where
  only the lower part exists). If it does connect to anything unseen, the candidates are
  the band-2 stub at its head and H1 or H2 at its tail. A thin strip (x 11985-11996,
  y 9990-10100) along the right edge of the INV1 load gate, visible in both stripped
  shots, starts where the strap ends; it was read as part of the load's active area.
  Second run (views `a2.png`, `a2b.png`): there is no contact at the strap's head. The
  contacts at (12014,10213) and (12019,10353) in the same view show a clear ring in both
  metal shots and a disc in `acid1b`; the strap over the stub shows neither. The stub is
  not a contact pad: it is where band-2 turns down and joins, by poly at y 10207-10228,
  the INV2 load gate block (so band-2 = n2). Between the stub's foot (y 10228) and band-3
  (y 10245) `acid1b` is pink (field under metal). The strap therefore stays isolated metal
  with no known function; its lower end (y 10440-10470, over H2 of the next row) was not
  looked at again.
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

- B1 (12263-12350 x 10056-10101). **Resolved in the third run: a hold device.** Profiles
  down x 12285 and x 12329 (under lines A and B): dull poly y 10058-10064, edge, bright
  (channel) y 10073-10085, edge, dull y 10094-10100. Along y 10081 the bright band runs
  from x 12266 to 12344, between the q box (tan to x 12256) and the lower box (tan from
  x 12352). So it is a poly block over a diffusion strip that joins the two boxes: channel
  17 wide, 82-86 long. The block's lower margin is what the second run drew as the "link"
  at y 10096-10112; the link from the pad (12183,10122) comes up at x 12263-12279 (poly
  continuous down x 12270 from y 10095 to 10134) into the block's lower left corner, so the
  block's gate is on that pad (VSS if B7 holds). The poly along y 10097 ends at x 12344 and
  is followed by 12 px of green (field) before the box: the buried contact B6 does not
  exist. Remaining doubt: B7, and what net `z` is (C2).
- B2 (12262-12410 x 10130-10200). Load 1, third-run readings (view `b2z.png`, profiles), **not
  drawn**: gate block x 12350-12401, y 10142-10197 (open, orange; a dark line across it at
  y 10162-10170; bright where line B's margin covers its left end, x 12350-12360); VCC box
  with contact (12433,10172) on its right (now drawn, it also feeds load 3); output diffusion
  x 12325-12350, y 10170-10192. The block's upper part continues left as a poly arm over
  field (the "salmon box", x 12338-12360, y 10140-10153) to a tan box with a double outline,
  x 12311-12334, y 10135-10160: read as the load's buried-contact tie. Under line A there is
  more diffusion, x 12270-12308, y 10149-10175 (tan down x 12290), right above the horizontal
  run of the g1 poly; between it and the output diffusion, in the gap between lines A and
  B, the clean shot is dark (not green) at y 10171-10192, so the two are probably one
  region. Down x 12343 the output diffusion is **not** continuous with the lower box of
  line C: the poly arm (dull, over field) lies between. Not found: the pull-down of this
  node and where the node goes. Candidate: an inverter of `g1` (the g1 poly runs along its
  lower edge), which would give a restored copy of `q`; with B4 this is the place to look
  for the driver of `m` or of `z`.
- B3 (12111-12140 x 10271-10310). The bottom part of R (`mra_rb`, below the cin gate) has a
  small tab at 12111-12132 x 10271-10282 towards the poly tab of the g1 pad (12127-12155 x
  10285-10308, dark-red blob in `acid1b`, orange in `acid`). Either R's bottom is a dead end
  (then the cin transistor does nothing), or it continues under that tab (a transistor gated
  by g1) or straight down into the VSS bottom band (then `m` is pulled low by cin alone).
  Drawn as a dead end with the tab as plain poly. A 7.5x view (`b3.png`) did not resolve it:
  a pale strip 12121-12127 x 10282-10307 lies between the rail-edge ghost and the poly tab,
  and below it (y 10309-10324) is field, so a straight run down into the VSS band is unlikely.
- B4 (12140-12250 x 10153-10215). Third run, by profiles: the g1 device exists and is wider
  than drawn before. Down x 12213 the clean shot is mauve (open diffusion) at y 10155-10175
  and again at y 10209-10230, with the g1 poly between; along y 10197 the g1 poly is bright
  (over a channel) under M1, x 12224-12248, and there is tan under M1 above it (y 10160,
  y 10182). Drawn now as diffusion x 12198-12250 through under the poly: W/L 52/17, down to
  the VSS strip. Still `?D`: the band along the top from there to R. Along y 10160 it is tan
  at x 12084-12136 and mauve at x 12196-12212, but olive-tan (174/169/112: neither the pink of
  field nor clean tan) at x 12140-12184 although the g1 metal covers part of that. If the
  band is open there, R's top part is a dead end and `m` has no pull-down through g1.
- B5 (12306-12327 x 10277-10332). The tie of the load-2 gate to the output: drawn `?B` at the
  left end of the block over the strip; what is visible is a dark-outlined blob at the
  block's upper left corner (12312-12327 x 10277-10297) next to a green (field) spot. The
  gate is on the output side either way.
- B6 (12346-12362 x 10094-10114). Withdrawn in the third run: there is no buried contact
  from the poly into the lower box (see B1).
- B7 (now decides the gate of the hold device). That the pad at (12183,10122) is on the VSS land: metal is visible between the land's
  bottom edge and the contact in both metal shots, and `acid1b` is pink (under metal) between
  them, whereas above the neighbouring g1 pad it is green; the g1 pad's metal goes down
  instead. The contact rings themselves hide the join. If this is wrong, line C and the two
  boxes are some other net and B1 changes.
- B8. The loop of dark line 7-9 px wide round the g1 pad (12137-12205 x 10165-10324) is read
  as the inner edge of the VSS diffusion ring (its bottom and right sides certainly are);
  along the left side (x 12137-12145) it runs next to R's right edge. Inside it: field, the
  g1 poly pad, riser and tab.

- C1 (12676-12690 x 10152-10190). The diffusion right of the `ck_a` gate (under the strap
  bar) and the diffusion column under the rail are drawn as one region. Between them, in
  the 28 px gap between the bar (ends x 12668) and the rail (from x 12696), the clean shot
  has a dark line 7 px wide (x 12680-12687) with one pale-green sample at x 12678; above,
  beside the pad (y 10105-10150), the same gap is plainly green (field). Tan resumes at
  x 12690 only for y 10154-10186 (down x 12693), exactly the height of the left-hand region,
  and the bottom edge line runs on to x 12699. The gap between L2 and L3 over `na` has the
  same signature. If they were two regions 10 px apart, the left one would be an island
  (the "box" 12651-12687 x 10200-10217 under it is open field: olive in the clean shot,
  R/G 1.01 in chip-2 `acid`). Consequence of the reading: `ck_a` pulls `na` to VSS. The
  functionally tempting alternative (a dynamic node under the bar feeding a gate) has no
  support in the photos.
- C2 (12750-12766 x 9955-9970). The strip of net `z` ends at x 12750; then 12 px of dark and
  from x 12766 the poly of `q` (its jog up), dull along y 9963 and down x 12772, i.e. over
  field. No box, no overlap: not joined as far as measured. That leaves `z` with only the
  hold device on it, which cannot be the whole story: look for a branch of the strip
  (350 px long, y 9957-9969, between the `n1` and `q` lines) or of the two boxes.
- C3. The gate `gb` (x 12730-12747) has a free-looking top end at y 10048 and a foot at
  y 10185-10207 (rounded outline 12718-12750) that was not resolved.
- C4 (12610-12690 x 10030-10100). The poly driven by `nb` runs up beside the rail's column
  (x 12688-12716, VSS) with a region on its left (x 12610-12650, y 10052-10100, outlined in
  the metal shot, R/G like field in chip-2 `acid`) that may or may not be diffusion joined
  to `na`. If it is, `nb` pulls `na` low and `na = NOR(ck_a, NOT m)`. Not drawn.
- C5. L1 and L3 carry the clocks by the routes of `trunks.md`; only L1's join is drawn. The
  line x 12896-12908 is taken as `ck_b` from the second run's 1x view of its bottom end.

## Third column `mra_col3`, x 12470-12770 (third run)

Colour key that made this column readable (clean shot, median of the rows, measured with
`tools/mra_prof.py --raw`): under metal, **poly over a channel is bright orange-salmon
(about 240/170/120), poly over field a duller salmon (217/163/116)**, diffusion tan
(200/180/132), field pink (202/122/131); under the middle of the VCC rail field is grey. A
diffusion edge under poly is a dark line across it. A load therefore shows, down its length,
as dull / edge / bright / edge / dull. In the 25-35 px gaps between metal lines the clean shot
shows a bright green strip over field (140/170/85 for 12 px) but a dark bar over diffusion
or poly (often with one pale-green sample at its edge); chip-2 `acid` shows only the ghosts
of the two metal edges there and cannot tell.

| Piece | Where (master row) | How sure |
|---|---|---|
| L1 = `ck_b` | metal x 12493-12507 in the body; contact (12493,10041) on poly pad 12480-12510 x 10028-10058 | joined to the `ck_b` metal of `trunks.txt` below r18 |
| `ck_b` pass gate | poly band y 10036-10057, x 12505-12612 (ends rounded); bright at x 12547-12610 over a diffusion: `u` above (y 10012-10036), `na` below (y 10057-10088) | measured |
| L3 = `ck_a` (second route) | metal x 12580-12594; contact (12592,10113) on pad 12578-12619 x 10093-10131 | identity by position at the bottom end only (name `mra_cka2`) |
| `ck_a` pull-down of `na` | gate x 12578-12600, y 10125-10203 between `na` (x 12535-12577) and the diffusion under the strap bar (x 12613-12682, y 10152-10190), which runs on under the rail to its contact (12714,10237) | the join to the rail's diffusion is C1 below |
| load 3 -> `na` | VCC box 12405-12475 x 10150-10198, contact (12433,10172); strip y 10163-10190; block 12481-12529 x 10148-10206; tie box 12509-12541 x 10118-10147 | profile down x 12502; tie stem `?P` |
| load 4 -> `nb` | VCC box of `mra_col2` (12433,10305); strip y 10303-10330; block 12474-12548 x 10286-10332; `nb` = D 12552-12622 x 10300-10347; buried contact 12577-12599 x 10267-10299 to the pad 12575-12651 x 10252-10290 | profile down x 12502; arm of the block to the pad `?P` |
| strap `nb` | contact (12629,10271); metal x 12624-12641 up to a bar x 12622-12668, y 10159-10188; up to contact (12655,10124) on pad 12638-12676 x 10105-10146; poly up x 12653-12680, y 10030-10108 (open, orange) | measured: the bar stops 28 px short of the rail |
| `m` gate | `m` (y 10364-10381) ends by turning up, x 12626-12649, y 10300-10381, between `nb` and an open (mauve) diffusion x 12650-12690 that runs under the rail to contact (12713,10340) | poly continuous along y 10372 from x 12599 to 12645 |
| rail | x 12696-12744, named `vss`; diffusion column under it x 12688-12727, y 10048-10262 | VSS by structure (source of both pull-downs) |
| gate `gb` | vertical poly x 12730-12747, y 10050-10194; dull y 10052-10108, bright (channel) y 10120-10180 between the rail's column and `d2` (x 12752-12770) | measured; its source is not found (C3) |
| `p3` | y 10231-10246 to x 12689, down x 12670-12689 to y 10296, right under the rail y 10277-10296 | orange in chip-2 `acid`; continues right |
| `q` | y 9977-9997 to x 12784, up at x 12762-12784, right along y 9957-9974 (seen to x 13045) | continues right into the wiring channel |
| `n1` | y 9924-9945, up at x 12700-12720, right along y 9905-9922 (seen to x 13045) | continues right |
| strip of net `z` | diffusion y 9957-9969 from the upper box of line C to x 12750 | ends there: 12 px of dark, then q's poly from x 12766 lying over field (dull); no join measured (C2) |

Row-to-row check (`cellcheck.py mra_col3`, both shots, pictures of r0, r3, r4, r6, r7, r10,
r11, r14, r15, r18 looked at as montages `cc3_acid1b.png`, `cc3_metal.png`): all 18
instances match (bad blocks 0.5-5.7 %, median correlation 0.94-0.97). Differences: the top
edge of r0, r4, r7, r11, r15 (no row above), grain on the wide rails, the rail contact at
(12725-12745,10225) in several rows (pits), and in r18 the clean shot only along the `p3`
line at x 12556-12646 (not in the metal shot; taken as residue, not looked at closer).

## Fourth column `mra_col4`, x 12750-13045 (fourth run)

Read from the median of the 19 rows (`--comp mrarow`) with the false-colour class map
(`tools/classmap.py`, also `view.py --layers class`) and colour profiles
(`tools/larr_px.py`); every junction below that decides connectivity was measured.

One row as extracted (names `mra_<net>_rN`; `a` is what the third run called `u` and `gb`,
`p3` is also its `d2`):

```
nb  = NOT m
na  = NOR(ck_a, nb)                  load 27/48; pull-downs 40/22 (ck_a, line L3) and 48/27 (nb)
a  <-> na   while ck_b               pass gate 63/21
a  <-> b    while ck_b               pass gate, L-shaped, about 120/21
p3  = NOT a                          pull-down 62/17 (the third run's gb gate), load 37/40
n1  = NOT p3                         chain column: 109/22, load 85/39; leaves right, to the wiring channel
d   = NOT p3                         pull-down about 106/21 + 20/14 (gate wraps the end of a vss band), load 40/32
q  <-> d    while ck_a               pass gate, L-shaped, about 107/21
d  <-> a    through 19/82, gate b    long device under the large poly of node b
q  <-> z    through 16/82, gate vss  (mra_col2's hold device)
```

So during `ck_b` (with `ck_a` low) `a` takes `NOT nb = m`; `p3`, `d` and `n1` follow at once
(static); during `ck_a` `q` takes `d = a`. `a` is a latch, `q` a clocked node: a
master-slave bit with `m` as its next value. `n1` is a buffered copy of the **master**
(`a`), and it is `n1`, not `q`, that leaves the row to the right.

The feedback device `d <-> a` (W 19, L 80, the same shape as the hold device on `q`): its
gate is the big poly on node `b`, and `b` is `a` passed through a second `ck_b` gate. If
the device is a depletion one, `a` is simply held from `d` whenever `ck_b` is low and `b`
does not matter. If it is an enhancement one, `b` remembers `a` while `ck_b` is low and
turns the feedback on only for a stored 1 (restoring the high level, which a pass gate
cannot deliver in full), a stored 0 being held by the capacitance alone. The photographs
cannot tell these apart (AMB-002). Either way: a latch, transparent during `ck_b`. Tagged
`kind=hold` in the trace.

| Piece | Where (master row) | How sure |
|---|---|---|
| `nb` pull-down of `na` (C4) | diffusion strip y 10070-10084 from `na` (x 12602), flaring to y 10052-10100 at x 12637; `nb` poly x 12653-12680; far side x 12680-12690 joins the column under the vss rail | **plain in the chip-2 metal shot**, where no metal lies above (view `c4b.png`) |
| `a`: band, box, finger | band y 10012-10027 (the third run's `u`) on to the contact box 12825-12875 x 9988-10034, contact (12847,10006); round the gate to the left strip x 12797-12813; finger 12764-12800 x 10049-10065 | band to box: the gap x 12790-12826 is reddish dark in the clean shot, not the olive of field |
| `a` to the `p3` pull-down gate | the vertical poly x 12730-12747 (third run's `gb`) has a free top end at y 10049; the finger of `a` reaches x 12766 beside it | `?`: the 14 px between are in the gap between two metal lines; reddish dark there at y 10058, green (field) at y 10040 and y 10196. Read as poly end + buried contact. Nothing else can drive that gate |
| `ck_b` gate `a <-> b` | bar y 10033-10052, x 12813-12886; leg x 12813-12835 to y 10114; pad 12882-12916 x 10022-10050, contact (12896,10035) to the line x 12896-12908 | bright (channel) in the clean shot; the line ends on the contact (12892,16991) of the `ck_b` route in `trunks.txt` |
| `b` | box 12838-12880 x 10055-10108, contact (12857,10087); metal x 12852-12868 down to contact (12858,10292) on the large poly | contact discs seen in both metal shots and the clean shot |
| strap of `a` | pad on the box; over the gate (y 10030-10048, x 12808-12866); down x 12806-12822; pad with contact (12840,10340) on the box 12828-12870 x 10320-10364 | the join of the column to the bottom pad is not resolved by eye (a topography line runs between); taken because the column ends there and the pad has no other feed |
| large poly of `b` | body y 10285-10315 from x 12797 to 12965 (right of x 12900 only y 10297-10315); left leg x 12797-12812 to y 10355 (over field, under the strap of `a`; purpose unknown); over the device x 12882-12964, y 10297-10353 | profile: dull / edge / bright y 10320-10336 / edge / dull |
| feedback device | diffusion y 10319-10338 from the box of `a` under the poly to the strip under the `ck_a` rail | measured across the gap x 12992-13010: reddish dark at y 10328, green at y 10300 |
| `q` end | poly y 9957-9974 to x 12915, heavy box 12893-12928 x 9976-10003 with the tab of the outer diffusion in it | profile down x 12904: poly to y 9972, edge, dull tan y 9986-9996 (as inside the known buried contact at (12588,10280)), edge, field |
| `ck_a` gate `d <-> q` | square 12927-12998 x 10004-10107; bar y 10030-10050; leg x 12947-12968 to y 10118; pad with contact (13017,10043) on the `ck_a` rail | bright in the clean shot; below y 10108 the clean shot is pink (field) for 20 px, so the gate's diffusions are **not** joined to the vcc diffusion under them (they look joined by eye) |
| `d` | inner diffusion of the gate; across the gap to the strip x 13010-13036, y 10074-10338 under the `ck_a` rail; the "boot" under the wide rail y 10256-10282; diagonal to the band y 10248-10270 below the `p3` gate | gap at y 10090 reddish dark; boot-to-strip at y 10268 is hidden by the heavy outline of the load's tie (`?D`) |
| `d` load | gate band y 10222-10254 under the wide rail (bright x 12945-12975), from vcc (contact (12957,10161)) down to the boot; right end in a heavy double outline on `d` | tie `?B`: inferred |
| `p3` node and load | diffusion 12752-12870 x 10131-10168 (narrow, y 10131-10150, left of x 12815); poly strip x 12834-12849 ends in it (nested arcs: buried contact); block 12872-12912 x 10110-10196 is the load gate (bright y 10136-10164), joined to the strip by the bar y 10175-10196 | profiles along y 10150 and down x 12899 |
| `p3` gate of `d` | band y 10225-10247 (bright x 12752-12830) between a vss band above (y 10205-10224, from the rail column) and `d` below; right end = the strip; left leg x 12742-12757 down into the `p3` line y 10277-10296 | the leg: poly-like at x 12753 only for y 10226-10244, odd colour at x 12746; the channel under it is `?D` |
| `z` | diffusion y 9932-9948 from x 12752 to a buried contact 12960-12992 x 9950-9980 on a poly that leaves right at y 9955-9977 | band is pale (not orange) in chip-2 `acid`; the jog from the strip of `mra_col3` (y 9957-9969) is `?D`, not looked at closely |
| `n1` | poly y 9903-9923 to x 13005, jog down to y 9924-9945, leaves right | orange in chip-2 `acid` |
| wide rail x 12936-12978 | named `vcc`: drain of both loads | ends not looked at again (second run: meets the VCC bus at the bottom) |

Row-to-row check (`cellcheck.py mra_col4 --bbox 12750,9895:13045,10385`, both shots): all
18 instances match (bad blocks 0-4.4 %, median correlation 0.95-0.97).

Corrections to the earlier runs:
- `q` is the slave node of the bit, not a line from outside. The poly the third run followed
  "to x 13045" along y 9957-9974 is two pieces: `q` ends at x 12915, and the piece from
  x 12962 on is net `z`'s.
- `u`, `gb` and node A are one net (`a`); `d2` is `p3`. `p3` does not "arrive from the
  right": it is made here.
- C4 resolved (`nb` pulls `na` low). C3 resolved (the `gb` gate is on `a`). C2: the strip
  of `z` does not end at x 12750, it jogs up and runs on right.

Reading aids found in this run:
- Tan (diffusion), pink (field) and salmon (poly) under where metal was cannot be told
  apart reliably by eye in the clean shot; twice the eye joined two diffusions that a
  profile showed to be 20 px of field apart. Use the class map, then a profile.
- In the class map, black over a large open area is not an edge: open field is a dark
  olive (about 88/98/57, green >= red) that falls under the "dark" threshold. In a gap
  between two metal lines compare red with green: reddish dark = diffusion or poly, olive
  or green = field.
- **Where no metal lies above, the chip-2 metal shot shows diffusion directly** (pinkish
  tan against yellow-green field, poly orange): the clearest view of an open device.

## Clock lines and routing channels (fourth run)

**The three counters do not share their clocks.** The thin lines L1, L2, L3, the line
x 12775 and the rail x 13025 were drawn by the earlier runs as lines through all 19 rows;
they are cut and re-arranged in the routing channels y 9182-9435 (between r3 and r4) and
y 12869-13035 (between r10 and r11). Extracted, per group:

| | rows r0-r3 (4 bits) | rows r4-r10 (7 bits) | rows r11-r18 (8 bits) |
|---|---|---|---|
| master gate `na -> a` (L1) | `ck_b` | **`mra_m7`**: bus line E, from the west | `ck_b` |
| slave gate `d -> q` (rail x 13025) | `ck_a` | **`mra_s7`**: bus line D, from the west | `ck_a` |
| second pull-down of `na` (L3) | `mra_l3n`: leaves north past y 7130 | `mra_l3m`: from the west on a metal line along y 13005 (contact (11765,13005), poly, contact (12567,13005)) | `mra_cka2`: from the contact (12631,16954); trunks' notes take the poly behind it for a second `ck_a` route (seen at 0.9x only) |
| gate `a <-> b` (line x 12902) | `mra_gab` | `mra_gab` | `mra_gab` |

So the 8-bit counter (believed horizontal) and the 4-bit counter step on every clock
cycle, and the 7-bit counter (believed character rows) steps only when the logic to the
west pulses its two clock lines. `mra_gab` is not `ck_b` as the third run believed: the
line x 12902 ends free 55 px above trunks' `ck_b` contact at the bottom and is fed at the
top, from a contact at (12889,7214) on a poly line that crosses the array along
y 7200-7225 from the west. What it is has to be found there; if it is simply a supply or a
clock, node `b` is the bootstrapped gate of the feedback device (see above).

How the lines run (metal unless noted; views `gapA_m.png`, `gapA_b.png`, `gaps_m.png`,
`gaps2.png`, `l3ends.png`, `rail_gap.png`):

- `ck_b` comes in at the bottom (trunks), is L1 of r18-r11, steps right at y 12907-12927
  onto the L2 position, runs through r10-r4 there without a tap, steps left at
  y 9242-9258 and is L1 of r3-r0 (top end free at y 7275).
- L1 of r4-r10: from a contact at (12521,9360) on bus line E to a free end at y 12885.
- L2 elsewhere is unused, three pieces with no contact: r0-r3 (y 7275-9196), r11-r14
  (y 13037-14970), r15-r18 (y 15012-16940).
- L3: r0-r3 continues north; r4-r10 has a free top end at y 9440 (over the `n1` line of r4,
  no contact) and at the bottom widens into a foot that turns west onto the contact
  (12567,13005) (`l3foot.png`, 6.5x, all four shots; first read as L2's contact, which
  left this piece without a feed: AMB-008, resolved); r11-r18 starts at y 13040 and ends on
  the contact (12631,16954).
- **What L3 is for.** `na = NOR(L3, nb)`, and `a` takes `na` on the master clock, so while
  L3 is high every bit of its group presents 0 to its master. One L3 per counter, each fed
  from a different place. I first read that as each counter's synchronous clear. **For the
  8-bit counter it is not: its L3 is `ck_a`** (verified: the poly x 12733-12757 was
  followed in the clean shot from the route at (12631,16954) south to clock.txt's `ck_a`
  bus line at (12740,18471)). There L3 is a clock phase: `na` is forced low during `ck_a`
  and is `NOT nb` otherwise, i.e. `na` is valid only outside `ck_a`, when the master
  (clocked by `ck_b`) samples it. So the horizontal counter's clear is elsewhere (in the
  untraced part of node `m`'s network, or in `m`'s inputs). What the L3 lines of the row
  counter (metal from the west along y 13005) and of the 4-bit counter (leaves north) carry
  is not known; they may be that counter's slave phase too, or a real clear.
- Rail x 13013-13037: south piece from trunks up to a contact at (13021,12939); middle
  piece y 9326-12887 from a contact at (13021,9340) on bus line D; north piece y 7268-9290
  from a contact at (13021,9276) on bus line C. The earlier note of a contact at
  (13023,7277) onto the `n1` line of r0 is wrong: the rail just ends over that poly.
- `ck_a` to the north piece: from the south piece's top contact a **diffusion** strip
  (y 12932-12948, pale with a heavy outline, contact boxes at both ends) runs west to a
  contact at (12784,12940) on the line x 12775; that line runs north past r10-r4 with no
  tap to a contact at (12784,9275) on bus line C. Line C also runs on west across the
  whole array.
- The other pieces of the line x 12775: r0-r3 from a free top end to a contact at
  (12783,9178) on bus line A; r11-r14 and r15-r18 pieces, ends not looked at closely (`?M`).

Bus lines of the channel y 9182-9435, all poly, straight, followed from x 11640 to their
east ends in the clean shot (`bus_w.png`):

| Line | y | West | East |
|---|---|---|---|
| A | 9178-9195 | starts under the vss rail at x 12700 (not resolved) | wiring channel, leaves at (13420,9405) |
| B | 9222-9240 | contact at about (11656,9230) | wiring channel, leaves at (13420,9447) |
| C | 9266-9284 | runs on west of x 11640 | contacts (12784,9275) and (13021,9276): `ck_a` |
| D | 9310-9328 | contact at about (11656,9317) | contact (13021,9340): `mra_s7` |
| E | 9351-9369 | runs on west of x 11640 | contact (12521,9360): `mra_m7` |
| G/F | 9397-9413, stepping up at x 12650-12670 to 9373-9391 | (contact near x 11656?) | wiring channel, leaves at (13420,9707): the R2 match line `rdp3_cb_eq` |

In the channel y 12869-13035: the carry-in of r10 (`mra_cin_r10`, y 12905-12920, from the
west), the poly line to L3's contact (y 12996-13014), and the diffusion strip above.

## Right-hand part, x 12770-13040: third-run readings (superseded by the section above)

From `c_top.png` (3.2x), `q4.png`, `t3.png`, `t4.png` and metal runs; master row.

- Vertical metal: line x 12767-12782 (jogs), **x 12810-12821**, **x 12852-12868**,
  **x 12896-12908** (believed `ck_b`: at the bottom it ends on the contact (12893,16989) of the
  `ck_b` route), wide rail x 12936-12978 (believed VCC), `ck_a` rail x 13013-13037.
- Node A: diffusion 12822-12877 x 9991-10032 with contact (12847,10006); its metal goes left
  and down as the line x 12810-12821. A also wraps down the left side (x 12790-12811) of
- a Γ-shaped gate: bar y 10033-10052 from x 12813 to 12882, leg x 12813-12835 down to y 10112,
  round the top and left of node B: diffusion box 12835-12888 x 10055-10110, contact
  (12857,10087), metal down as the line x 12852-12868. The gate's bar ends on a poly pad
  12883-12916 x 10022-10047 with contact (12896,10035) to the line x 12896-12908. **A pass
  transistor of W about 115 between A and B, clocked by that line (`ck_b`).**
- The band of `u` (y 10012-10026) runs right under the rail to x 12790 and appears to turn
  down into A's left part (so u = A); not measured.
- A second Γ gate under the wide rail: leg x 12947-12969, y 10027-10110, bar y 10027-10050
  to the pad of the `ck_a` rail's contact (13017,10043). Diffusion left of and above it
  (x 12927-12947, y 9990-10110), and right of the leg (x 12969-12990, y 10052-10104).
  **A pass transistor clocked by `ck_a`.**
- A large poly, salmon: x 12875-12912, y 10117-10200 with a bar y 10172-10200 from x 12803;
  the orange stripe x 12838-12847, y 10172-10245 is poly seen in the gap between the two
  metal lines. Diffusion with the rail contact (12957,10161) at x 12927-12990, y 10117-10200.
- A poly line y 10224-10248 ends rounded at x 12862 (the continuation of `p3`?); poly under
  the wide rail y 10222-10250 (x 12928-12990); contacts (12858,10292), (12840,10340).

## Not done

In the order that would pay most:

1. **x 12770-13040 of every row** (readings under "Right-hand part"): nodes A and B and the
   Γ gate between them, the `ck_a` gate at x 12947, the large poly at 12803-12912 x
   10117-10200, the lower part y 10200-10390 (contacts (12858,10292), (12840,10340); poly
   under the wide rail y 10222-10250 and y 10300-10340), and where `p3` is made (it runs
   right under the VSS rail along y 10277-10296; a line y 10224-10248 ends at x 12862).
   Views to start from: `c_top.png` (3.2x, x 12790-12990, y 9985-10275), `t3.png`, `t4.png`.
   Draw the three lines x 12815, 12860, 12902 and the two rails once the contacts are placed.
2. **Where `nb` acts** (C4) and whether `u` is node A: 12610-12800 x 10005-10100.
3. **Load 1 and its node** (B2), the corner B4 and the tab B3 in `mra_col2`: with the colour
   key of the third run (bright = channel) a profile along the g1 poly's horizontal run
   (y 10188-10205, x 12175-12300) and one down x 12213 will say whether g1 is a gate there.
   `m` still has no pull-up: this is where it should be.
4. **Net `z`** (C2): follow the strip y 9957-9969 for a branch.
5. `gb` and `d2` (C3); the foot of the `gb` poly at 12718-12750 x 10185-10207.
6. The second `ck_a` route into L3 and the `ck_b` join of the line x 12902, at the bottom end
   (y 16940-17000), at tracing zoom; the top ends of L1 and L2 (they are not seen above
   y 7310: do they end inside r0?).
7. The wiring channel x 13040-13375 (second-run notes below), the routing channels
   (y 9182-9435 etc.) and the six-line poly bus in the first one; A1.

Wiring channel, from the second run: seven vertical metal lines
  at centres 13087, 13130, 13174, 13217, 13261, 13304, 13348 (16-20 wide, pitch 43.5), which
  start and stop at different rows. Low-zoom mosaics of all 19 rows (`bm1.png`..`bm3.png`,
  0.45x) show contacts or jogs on the lines only in r0, r3, r4, r10, r14, r15, r16, r17 and
  r18, at about (13263,7274) (13129,7363) (13129,7429) (13214,7463) (13207,7534) (13300,7578)
  in r0; (13096,8705) (13092,8836) in r3; (13340,9658) in r4; (13129,12567) and a staircase
  down to (13347,12825) in r10; (13092,14856) in r14; (13129,15232) in r15; (13092,15558)
  (13174,15558) in r16; (13129,16404) in r17; several in r18. In the other rows the lines
  run straight. Each row also sends poly lines under the channel: in r5 the n1 line
  (y 9910-9935) ends at x 13155 between two channel lines with no contact seen, and a
  diagonal poly from (13035-13085,10390) (the n1 line of r6) runs up to (13315,10170), up
  between two lines to y 10035 and leaves at (13375,9975). `tools/mra_bus.py` lists the line
  centres and per-row anomalies, but its numbers are dominated by the poly underneath and
  did not identify taps. Which row drives which line was not established.
- The routing channels (y 9182-9435 etc.) and what the six-line poly bus in the first one
  connects; whether the top rows of the groups have a line in the place of `m` of the row above.
- Above the top row (y 7130-7265) and below the bottom row (y 16945-17050): three
  horizontal poly lines at y 7155, 7205 and the row's own top lines; not traced.
