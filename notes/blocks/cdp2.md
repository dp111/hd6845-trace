# cdp2: central datapath, rows y 5700-8450 (x 7600-10850)

Trace: `trace/cdp2.txt`. Scratch: `cache/scratch/cdp2/`. Tools: `tools/cdp2_pt.py`
(colour at points, both chips; used to test for contacts), `tools/cdp2_map.py` (text map
of colour classes), `tools/cdp2_lines.py` (follow a horizontal poly line by colour),
`tools/cdp2_mo.py` (stripped shot with the metal outline). `tools/rdp3_sharp.py` (unsharp
mask) at 3.3-5x on a median composite (`--comp cdp2_a`) is what made the junctions readable.

## Status

- Row A (y 6020-6345, five latch cells, slices s3..s7): cell traced, placed five times,
  overlaid on both layers, extracts as 5 x 6 transistors, no errors. Shipped.
- Channel 1 above it (y 5720-6060): every wire that leaves row A upward is traced to
  the top of the region or to where it turns into a long horizontal line; all contacts
  tested. The long lines themselves are followed only between x 8480 and x 10850.
- Row C (y 7500-7825, seven latch cells, slices s1..s7): the same cell (correlation
  0.92-0.94, cellcheck 0-6 % bad blocks on the core), placed seven times, contacts
  tested in all seven; tops of s3..s7 traced, tops of s1 and s2 only described. Shipped.
- Rows B1, B2, D and channels 2, 3: surveyed only (Inventory, Not done).

## Conventions

- Slices numbered as in cdp4: s0 leftmost, pitch 390.3. My master slice is **s4**
  (VSS rail x 9161-9207, VCC rail x 9375-9425). Offsets from findcell: s3 -390, s4 0,
  s5 390, s6 780, s7 1170 (same for every row here). Bit order not established.
- Rails (traced in row A, by the loads and pull-downs): **VSS = the wide rail at
  x 9184 + 390k, VCC = the rail at x 9400 + 390k.** In cdp4's frame that makes its rail
  at x 8385-8425 (s2) VSS and x 8597-8641 VCC, if the rails run straight down (not
  followed).
- Colours in the clean shot here (measured, `cdp2_pt.py`): poly under metal salmon
  (221,164,120); poly over a channel under metal brighter (235,168,120); poly in the open
  dark red-brown, textured; diffusion under metal or in a contact window tan (198,176,133);
  field under metal pink, in the open khaki. **A metal contact (to poly or diffusion) is a
  greenish, speckled patch: mean about (150,150,90), s.d. over 12; plain poly or
  diffusion under metal has s.d. 3-6.** That test was used for every "no contact" below.

## Inventory (rows, top to bottom)

| y | What | Slices | State |
|---|---|---|---|
| 5720-6060 | channel 1: horizontal poly lines at y 5826, 5870, 5913, 5956, 6000 (long), 6042 and 5783 (short), pads at y 5740; row A's output tracks cross them | - | traced between x 8480 and 10850 |
| 6020-6345 | **row A: five static latch bits** `cdp2_lat` | s3..s7 (x 8790-10745) | traced |
| 6000-6310, x 7700-8300 | random logic left of row A | - | not traced |
| 6314-6334 | row A's load strobe `cdp2_a_ld` (poly, loops through every cell) | - | traced inside the row; ends not followed |
| 6350-6900 | channel 2: 13 horizontal poly lines, pitch 43.3, at y 6366, 6410, 6456, 6498, 6542, 6584, 6626, 6672, 6714, 6756, 6802, 6844, 6888. Per-slice metal lines and rails cross over them | - | not traced |
| 6930-7200 | row B1: cell, 5 copies (findcell 0.88-0.90) | s3..s7 | not traced |
| 7200-7480 | row B2: cell, 5 copies | s3..s7 | not traced |
| 6900-7480, x 7900-8750 | irregular logic left of rows B | - | not traced |
| 7500-7825 | **row C: seven static latch bits**, same cell as row A (dy 1476; dx -1171, -781, -391, 0, 390, 781, 1171) | s1..s7 | traced (tops of s1, s2 not) |
| 7830-7960 | channel 3: horizontal poly lines; at the left (x 7700-7950) bundles turn down | - | not traced |
| 7980-8450+ | row D: cell, 5 copies + a weaker sixth at dx -781 (0.73); may extend below 8450 | s3..s7 (+s2?) | not traced |

Per-slice vertical metal in channel 2 (measured at y 6542/6563, master slice): VSS rail
x 9165-9205, line a x 9243-9252, a line at x 9333-9340, VCC x 9378-9402, a narrow line
at about x 9411-9420. Nothing between x 9423 and 9550.

## Logic

### Row A: five static latch bits (traced)

Cell `cdp2_lat`, master s4 at x 9160-9560, y 6020-6345. It is the cell of rdp3's row AR
(`rdp3_lat`) turned upside down: x' = x - 5379, y' = 19351 - y maps every feature of
that cell onto this one within a few px. Each feature was nevertheless placed from this
row's photos. Six transistors:

```
a   <- bus    pass transistor T1 (36/23 at 9246,6278), gate cdp2_a_ld
n2  = NOT a   pull-down T2 50/22 at 9243,6175; load 16/51 at 9345,6224
q   = NOT n2  pull-down T1' 53/22 at 9534,6226; load 28/54 at 9445,6266
a  <-> q      hold device 15/83 at 9390,6120, gate tied to VSS
```

- **Bus** `cdp2_a_sK_bus`: vertical metal x 9238-9254 (16 wide), runs through the cell
  top to bottom. Contact (9244,6313) to a land; the strip from the land goes up through
  the strobe gate and ends on a buried contact (9226-9264 x 6208-6230) to the poly that
  runs up under the bus line (gate of T2, node a) and on to the right (y 6119-6139) to a
  second buried contact on the feedback land (9300-9346 x 6110-6138).
- **Strobe** `cdp2_a_ld`: one poly line, y 6314-6334, through the whole row. In each cell
  it turns up at x 9196-9219, crosses the strip at y 6266-6289 (T1's gate) and comes
  down at x 9298-9320, so the bus contact sits inside the loop. All five bits load
  together when it is high. The line runs on to the right past s7 (seen to x 10884 at
  least); at the left it reaches about x 8520. Ends not traced.
- **Loads**: both hang from the VCC land (9334-9412 x 6251-6302, contact 9378,6276).
  Load of n2: strip x 9337-9353 up to the n2 land; gate block 9322-9370 x 6198-6250,
  tied to n2 through the tab and the buried contact at 9281-9313 x 6183-6211. The same
  poly runs on under the VCC rail (x 9366-9398), right along y 6166-6189 and down at
  x 9523-9545 as the gate of q's pull-down. Load of q: strip y 6252-6280, gate block
  9418-9472 x 6203-6292 whose upper half is a contact pad; tied to q by a tab onto the q
  drain (buried contact 9476-9504 x 6203-6240) and, through the strap (contacts
  9446,6223 and 9460,6135), to the output land 9436-9490 x 6110-6160.
- **q's pull-down** has its source on the *next* slice's VSS land (x 9550-9611); s7 uses
  a sixth VSS rail at x 10744.
- **Output**: output land -> buried contact 9495-9524 x 6106-6133 -> poly strip up to a
  contact (9508,6044) -> metal x 9499-9519 going up out of the cell. q is in the same
  sense as the bus.
- **Track c** (metal x 9499-9519, y 6084-6338): sits on the q drain, with a long narrow
  contact (speckled strip in the clean shot, in all five slices: s.d. 15-18). Its lower
  end lies over the strobe line with **no contact** (plain poly colour, s.d. 4-8, in all
  five slices, against s.d. 13-27 on the three known poly contacts of the cell). A dark
  line crosses the metal at y 6073-6082 between the output contact and the track; whether
  the metal is cut there does not matter, both pieces are q.
- **Track b** (metal x 9325-9347) is the **n2 output**: it ends on the n2 land with a
  small contact at the very end of the track (9337,6184; greenish and speckled over
  y 6180-6188 in all five slices, while 6 px higher the land is flat tan, which first
  read as "no contact"). It runs up into channel 1.
- **Hold device** (same structure as rdp3's AMB-1, same reading adopted): the poly band
  along the cell top (y 6082-6103, contact to the VSS rail at 9182,6096, confirmed by
  the contact test) widens under the VCC rail into a block (9348-9431 x 6083-6142) over
  a diffusion strip (y 6113-6128) that joins the feedback land (node a) to the output
  land (q). Vertical colour profile under the rail: poly over field 6084-6104, dark edge
  6106-6112, brighter "poly over channel" 6114-6126, dark edge 6128-6134, a thin poly
  overhang 6136-6140. In the open gap at x 9360 the poly is continuous over y 6086-6130.
  A gate at VSS only makes sense for a depletion device: a weak q -> a feedback that
  the bus overpowers while the strobe is high. Believed, not provable from the photos:
  the implant. The strip is drawn `?D`, the device is marked `A kind=hold`.

All five instances compared (cellcheck, both layers): s5, s6, s7 identical (0-3 % bad
blocks); s3 differs only above the cell (y 5985-6105), by the channel-1 wiring below.

### Channel 1: where row A's outputs go (traced)

Each crossing of a track with a poly line was tested with the contact test
(Conventions); the contacts listed are the only ones, and each also shows as a ring in
the metal shot.

| Slice | q (track c, x 9509 + 390(K-4)) | n2 (track b, x 9336 + 390(K-4)) |
|---|---|---|
| s3 | up to a contact at (9118,5740) | contact (8943,6044) to **line 6042**; top end contact (8943,5782) to a poly jumper (y 5783) that runs right to a contact (9332,5782) on the metal that comes down in s4's column from above y 5700 |
| s4 | up to (9508,5740) | starts at contact (9332,5869) on **line 5870**. Line 5870 also has a contact at (9463,5869) to a short metal link up to (9463,5782), from where a poly goes up out of the region at x 9463 |
| s5 | up to (9897,5740) | contact (9725,5916) on **line 5913**; runs on up to a contact at (9725,5740) |
| s6 | up to (10287,5740) | contact (10113,5958) on **line 5956**; up to (10113,5740) |
| s7 | up to (10677,5740) | contact (10502,6000) on **line 6000** (which ends there); up to (10502,5740) |

- So every bit sends q and n2 upward (the pads at y 5740 lead, in poly, to the right
  and up across y 5700: seen at 1x only, drawn as `?P` pads), and n2 also sideways on
  one long poly line per bit.
- Lines 5870, 5913, 5956 run on to the right past x 10850 and all four (with 6000) to
  the left past x 8480, where they jog up-left around the s2 VSS rail (x 8377-8427)
  and continue towards x 8150 at about y 5885, 5910, 5933. Not followed.
- Line 6042 (s3's n2) runs left to a contact at (8335,6042) on a metal line going down
  into the logic left of row A.
- **Line 5826 is not connected to row A.** In s3 an extra metal line e (x 8892-8908) has
  contacts to it at (8900,5825) and to a poly pad at (8900,5739), from which a poly
  band runs right to x 9086 and (seen at 1.4x) turns up across y 5700. Below the line
  e runs on as a stub to y 6115, where it ends over field just above the node-a poly of
  s3's latch: pink field colour under the end, no green speckle, metal ends 4 px short
  of the poly band in both metal shots. Named `cdp2_ch1_5826`.
- The bus lines cross channel 1 without any contact and leave the region upward.

Believed: a 5-bit register written from five bus lines when its strobe is high; its
true and inverted outputs feed the row above (a comparator would want both), and the
inverted outputs also go out sideways. s3's wiring differs from the regular staircase
of s4..s7, so s3 may be a separate bit rather than part of a 5-bit value. Which
register it is is not established.

### Row C: seven more latch bits (traced)

`findcell` with the core of the row A cell finds seven copies at dy = 1476
(scores 0.92-0.94), and `cellcheck` on the core (master y 6080-6345) gives 0-6 % bad
blocks in both layers. The cell was therefore split: `cdp2_lat` is the core (everything
below the grounded band), `cdp2_lat_top` what joins it in row A, `cdp2_lat_ctop` what
joins it in row C. Nets of row C are named `cdp2_a_c_sK_a / _n2 / _q` (cell prefix + tag).

Tested in all seven slices (contact test): track b's contact to the n2 land, the long
contact of track c on the q drain, the band's contact to the VSS rail are there; track
c's lower end over the strobe line has no contact.

- Strobe `cdp2_c_ld`: poly line y 7790-7810, loops through the seven cells as in row A.
  By colour it runs from about x 7650 to past x 10885. Ends not traced.
- Top of the cell, s3..s7 (identical, cellcheck 0-6 %; from a 7-instance composite
  `--comp cdp2_ctop`): the **output q leaves upward in poly** (x 9502-9520, no metal, no
  contact) and crosses y 7425 into row B2. **Track b (n2)** has a contact at (9334,7517)
  to a poly that runs right under the VCC rail (y 7506-7526) and then up at
  x 9453-9474 across y 7425; the metal of track b itself also runs on up. The bus line
  runs on up.
- Top of the cell, **s1 and s2: different, not traced.** Seen at 1.6x: s2's output poly
  (x 8721-8739) turns left at y 7463-7479 and runs left across s1 to x < 7960; s1's
  output poly (x 8331-8349) turns left at y 7503-7522 and also runs to x < 7960. s1's
  track b (x 8153-8175) runs on up past y 7390 with no contact at y 7517 (plain poly
  under it: s1's own output line crossing); s2's track b has no metal at y 7517. Both
  bus lines jog about 55 px to the right at y 7507-7526 (metal) and go on up at
  x 8109-8131 (s1) and x 8517-8536 (s2). A metal line lies over s1's track-c column
  (x 8330-8350) from above y 7390 down to the cell.
- The bus lines of row C are named separately (`cdp2_c_sK_bus`): between row A and row
  C the metal at the bus position is interrupted inside row B2 (no metal at x 9236-9258
  for y 7190-7240 and 7317-7371), so whether it is the same wire is for row B2's trace.

Believed: a 7-bit register (R4, R6 and R7 are 7 bits wide); two of its bits (s1, s2)
are used to the left of the array, five (s3..s7) by the rows above (B1/B2).

## Ports

| Name | Layer | Where it crosses | Direction | What |
|---|---|---|---|---|
| `cdp2_a_sK_bus` (K=3..7) | metal | x 8856, 9246, 9636, 10026, 10416 at y 5700 (top edge, no contact in channel 1) and at y 6345 (down into channel 2, not followed) | into the row | data for the latch |
| `cdp2_a_sK_q` | metal, contact at y 5740 | (9118,5740), (9508,5740), (9897,5740), (10287,5740), (10677,5740); beyond the contact not traced (metal seems to run on up in s4) | out, to the row above | latch output, same sense as the bus |
| `cdp2_a_s3_n2` | metal | x 9334, y 5700 (the metal in s4's column) | out, to the row above | inverted output of s3 |
| `cdp2_a_s3_n2` | metal | (8335,6066) going down | out | same net, via line 6042, to the logic left of row A |
| `cdp2_a_s4_n2` | poly | x 9463, y 5700 going up | out | inverted output of s4 |
| `cdp2_a_s5_n2`, `s6`, `s7` | poly pads | (9725,5740), (10113,5740), (10502,5740); poly on from there right and up, not traced | out | inverted outputs |
| `cdp2_a_s4_n2` | poly | line y 5870: x 8480 (continues left) and x 10850 (continues right) | out | inverted output on a long line |
| `cdp2_a_s5_n2` | poly | line y 5913: x 8480 and x 10850 | out | |
| `cdp2_a_s6_n2` | poly | line y 5956: x 8480 and x 10850 | out | |
| `cdp2_a_s7_n2` | poly | line y 6000: x 8480 (ends at x 10518) | out | |
| `cdp2_ch1_5826` | poly | line y 5826: x 8480 and x 10850; band at y 5730 to x 9086, then up across y 5700 at x 9080 (`?`) | unknown | not connected to row A |
| `cdp2_c_sK_bus` (K=1..7) | metal | x 9246 + dx at y 7425 (s3..s7; s1, s2 end at the cell top, y 7551, in the trace) and y 7821 (down, not followed) | into the row | data for row C's latches |
| `cdp2_a_c_sK_q` (K=3..7) | poly | x 9511 + dx, y 7425, going up | out, to row B2 | row C latch output |
| `cdp2_a_c_sK_n2` (K=3..7) | metal and poly | metal x 9336 + dx and poly x 9463 + dx, both at y 7425 going up | out, to row B2 | inverted output |
| `cdp2_a_c_s1_q`, `cdp2_a_c_s2_q` | poly | drawn only to the cell top (x 8340 / 8730, y 7554); beyond: see row C, s1 and s2 | out, to the left | not traced |
| `cdp2_c_ld` | poly | y 7800; about x 7650 at the left, runs on right of x 10850 | into the row | load strobe of row C |
| `cdp2_a_ld` | poly | y 6324; runs on right of x 10850; left end about x 8520 | into the row | load strobe of row A |
| `vss` | metal | x 8794, 9184, 9574, 9964, 10354, 10744 (46 wide) at y 5960 and y 6350 | - | rails, run on both ways |
| `vcc` | metal | x 9010 + 390k (50 wide) at y 5960; x 8998 + 390k (54 wide) at y 6350 | - | rails, run on both ways; narrower (x 9378-9402) in channel 2 |

## Ambiguities

1. **Hold device** (9341-9446 x 6083-6142): see Logic. Same open question as rdp3's
   AMB-1. Between the block's right end (x 9431) and the output land (x 9436) there is
   one dark line, at the edge of the VCC rail; read as the metal-edge artefact over a
   continuous strip. If the strip did not reach the land the latch would be dynamic.
2. **Load of n2** (9320-9366 x 6188-6247): in the clean shot the strip under the gate
   block is smooth bright salmon (243,170,122) although no metal covers it on either
   chip, while q's load, also in the open, is textured orange. The geometry is drawn as
   in rdp3's cell (strip, block, gate tie); the connectivity (n2 land - strip - VCC
   land, gate tied to n2) is the only one that gives n2 a load. A thin bright line
   (x 9335-9343, y 6191-6246) shows in both metal shots over the strip; it is too narrow
   (8 px) for metal and is read as the strip itself.
3. **Below the end of track b**: metal at x 9326-9348 is certain down to y 6190 and
   again at y 6348 and below (the line at x 9333-9340 in channel 2). Between, over the
   n2 load and the left part of the VCC land, the metal shots disagree (chip 2 bright,
   chip 1 not). Drawn: nothing below y 6190. If the metal is continuous the line in
   channel 2 is n2 as well. Needs a look at y 6250-6400 on both metal shots.
5. **End of line e in s3** (8900,6115): see channel 1. A metal line that ends is
   expected to end on a contact; none is seen, as with track c over the strobe line.
4. Small dark boxes in the open beside the strobe gate (9270-9297 x 6244-6260 and
   9277-9298 x 6288-6313): read as bulges of the strobe poly over field. No diffusion
   there, so no device.

## Not done

- **Channel 1, left part**: follow lines 5826-6000 left of x 8480 (they jog at
  x 8300-8470 and go on to x < 8150) and the metal from (8335,6042) down. Right of
  x 10850 the lines belong to whoever has that area. The poly from the y 5740 pads
  upward (x 9080, 9463 and right of each pad) crosses into cdp1's rows.
- **Ends of `cdp2_a_ld`**: right of x 10850 at y 6324; left end near x 8520, y 6324.
- **Channel 2 (y 6350-6900)**: 13 poly lines, their ends and contacts. `cdp2_lines.py`
  gives a first pass but breaks at every metal edge; check ends by eye. The far left
  (x 7600-8700) has contacts at about y 6690 (x 8120, 8300, 8700) and y 6800-6850.
- **Row C, tops of s1 and s2** (x 7990-8770, y 7390-7560): see row C. Two views at 3x
  would do it.
- **Ends of `cdp2_c_ld`** (y 7800): left about x 7650, right past x 10850.
- Rows B1, B2 (y 6930-7480), channel 3 (y 7830-7960), row D (y 7980-8450): not
  started. Rows B take q and n2 of row C's s3..s7 from below (ports) and the bus and
  n2 lines of row A from above. They are not the latch cell (findcell finds no copy). Composite of row A: `--comp cdp2_a` (master frame
  9150,5940:9590,6350, five instances).
- Logic left of the rows (x 7600-8750).
- Rails are drawn only over row A (y 5960-6350) and row C (y 7425-7830); x of the VSS
  rails 8013, 8403, 8793, 9184, 9574, 9965, 10355, 10745, of the VCC rails 8229 ... 10571.
