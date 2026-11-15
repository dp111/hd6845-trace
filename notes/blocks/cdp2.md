# cdp2: central datapath, rows y 5700-8450 (x 7600-10850)

Trace: `trace/cdp2.txt`. Scratch: `cache/scratch/cdp2/`. Tools: `tools/cdp2_pt.py`
(colour at points, both chips; used to test for contacts), `tools/cdp2_map.py` (text map
of colour classes), `tools/cdp2_lines.py` (follow a horizontal poly line by colour),
`tools/cdp2_mo.py` (stripped shot with the metal outline), `tools/cdp2_cls.py` (false-colour
class map), `tools/cdp2_reg.py` and `tools/cdp2_cmont.py` (registration of the clean shot
against the metal shot), `tools/cdp2_w.py` (sharpened panels with the metal outline). `tools/rdp3_sharp.py` (unsharp
mask) at 3.3-5x on a median composite (`--comp cdp2_a`) is what made the junctions readable.

## Status

- Row A (y 6020-6345, five latch cells, slices s3..s7): cell traced, placed five times,
  overlaid on both layers, extracts as 5 x 6 transistors, no errors. Shipped.
- Channel 1 above it (y 5720-6060): every wire that leaves row A upward is traced to
  the top of the region or to where it turns into a long horizontal line; all contacts
  tested. The long lines themselves are followed only between x 8480 and x 10850.
- Row C (y 7500-7825, seven latch cells, slices s1..s7): the same cell (correlation
  0.92-0.94, cellcheck 0-6 % bad blocks on the core), placed seven times, contacts
  tested in all seven; tops of all seven traced. Shipped.
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
| 7500-7825 | **row C: seven static latch bits**, same cell as row A (dy 1476; dx -1171, -781, -391, 0, 390, 781, 1171) | s1..s7 | traced |
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
- Top of the cell, **s1 and s2 are different** (traced from two views at 2.9x, every
  crossing tested, no contacts): the outputs leave **to the left** in poly. s2's output
  poly (x 8720-8740) turns left at y 7463-7481 (line L1) and runs across s1; s1's
  (x 8329-8349) turns left at y 7504-7522 (line L2). Both run on left of x 7990, where
  they join the bundle that bends down at x 7700-7950 (not followed). In s1 the metal
  on the track-c column also runs on up past y 7395 (q of s1 in metal), and so does
  track b (n2 of s1). s2's track b ends at the cell top: its n2 is not used outside
  the cell. Both bus lines jog right at y 7510-7528 (s1: x 8075 -> 8118, s2: x 8465 ->
  8535) and run on up; s1's jog lies on top of L2 without a contact.
- The bus lines of row C are named separately (`cdp2_c_sK_bus`): between row A and row
  C the metal at the bus position is interrupted inside row B2 (no metal at x 9236-9258
  for y 7190-7240 and 7317-7371), so whether it is the same wire is for row B2's trace.

Believed: a 7-bit register of which two bits (s1, s2) are used to the left of the array
and five (s3..s7) by the rows above (B1/B2). That 5 + 2 split fits **R10** (cursor
start raster in bits 0-4, blink mode in bits 5-6) better than R4, R6 or R7; row A
(5 bits, outputs to the row above it) would then be a 5-bit raster-type register (R9
or R11) and rows B a 5-bit comparator. A guess from widths only.

### Channel 2 (surveyed, tested)

13 poly lines at y 6366 ... 6888. In slices s3..s7 the per-slice metal over them is: VSS
rail, bus line (x 9243-9254), the line at x 9329-9340 (Ambiguities 3), VCC rail
(x 9379-9421, with a dark line down its middle). Every crossing of the bus line, the
x 9337 line and x 9415 with the 13 lines was put through the contact test in s3..s7:
all plain poly, **no contact**. So in the sliced part channel 2 only passes through: its
lines join things left of x 8780 or right of x 10790. (One contact-like reading in s2:
(8556,6888).)

### Rows B1/B2 (in progress: established so far, NOT yet in the trace file)

One cell about 390 x 560 per slice (s3..s7), composite `--comp cdp2_b` (master frame
9150,6890:9590,7500, slice s4). Not the latch. Coordinates are the master's.

Reading the clean shot here (measured, second run): under metal poly over field is
salmon (221,164,120), **poly over a channel under metal is brighter (240,172,124)**,
diffusion tan (196,178,134), field pink (195,117,126). In the open: poly over a channel
is dark orange and textured, poly over field can be smooth bright salmon (the same
colour as a channel under metal, so the metal shot must be consulted), field khaki,
diffusion mauve to light tan. `tools/cdp2_cls.py` paints these classes; its metal mask
is patchy where poly edges cut the metal, so it is reliable only inside the white
outlines. Registration of the clean shot against the metal shot was checked on five
contacts of this cell (`tools/cdp2_cmont.py`): within 2 px.

Established (each from a 3-4x view plus a colour profile):

- **`hl1`: a diffusion line along the whole row, y 6948-6966** (tan under every rail,
  no contact to any rail in the cell). The same arrangement as cdp1's row B.
- **Two transistors in series from `hl1` to VSS**, both about 130 wide (x 9292-9425):
  gate bar 1 (poly, y 6972-6995), a diffusion strip y 6998-7012, gate bar 2 (poly,
  y 7014-7040), then a diffusion strip y 7044-7070 that runs on to the right under the
  metal m4 and joins the tail (9485-9535 x 7052-7072) of the VSS land of the next slice
  (contacts at 9537,7030 and 9570,7030 = 9147,7030 and 9180,7030 in this slice).
  Column profile at x 9333 (under the track-b metal): tan 6952-6968, bright poly
  6976-6990, tan 7000-7012, bright poly 7020-7032, tan 7044-7066.
  So `hl1` is pulled low in a slice when bar 1 AND bar 2 are high.
- **Bar 1** joins, at its left end, the poly P1 that runs down under the row A bus line
  (x 9240-9262, y 6972-7160; orange = over field all the way), turns right along
  y 7142-7162, passes under track b (y 7158-7172) and the VCC rail (y 7160-7170, up at
  x 9400-9412, right along y 7128-7140) and becomes the lower gate of the pair below.
  The join of bar 1 and P1 goes through a small heavy-outlined box (9266-9290 x
  6972-6997): `?`, see Ambiguities.
- **Bar 2** ends on a pad (9443-9490 x 6995-7045) with a contact (9463,7015) to the
  metal **m4** (x 9455-9472), which runs down to a contact (9465,7272) on a diffusion
  land (9450-9495 x 7250-7300, tan under the metal). Profile along m4: metal present
  throughout; under it diffusion at y 7058-7066 (the VSS strip), poly at 7082-7100 and
  7130-7142, a channel at 7193-7212, poly over field 7224-7240, the land from 7262.
- **A two-input NAND with its load** at x 9440-9550, y 7050-7265: from the VSS tail
  (y 7052-7072) down through gate "top bar" (poly, y 7080-7097, x 9483-9533) and gate
  "bottom bar" (y 7125-7142) to the node X (diffusion 9485-9535 x 7145-7185), which
  continues into a buried-contact box (9508-9547 x 7188-7226, a dark-outlined box with
  no metal in both metal shots). The load: VCC land (9345-9435 x 7185-7260, contact about
  9395,7235) -> strip y 7190-7215 under a poly block (9443-9500 x 7176-7222) -> the box;
  the block continues as the textured blob 9480-9540 x 7222-7265 and is tied to X at the
  box. Top bar = the poly line y 7082-7100 that comes from the contact pad
  (9278-9312 x 7078-7118) of the metal **m3** (x 9280-9298, contact 9288,7095); bottom
  bar = P1. So **X = NAND(m3, P1)**.
- m3 runs down from (9288,7095) to a second contact (9289,7341) on a large poly pad
  (9255-9305 x 7320-7365) and on to a third near (9287,7430).
- A second long poly block (9283-9345 x 7200-7248) lies over a horizontal strip
  y 7214-7245 that leaves the VCC land to the left: a second load. Its output end
  (x 9253-9282, y 7170-7265) is not resolved.
- The row A bus line (metal x 9240-9255) **ends at y 7178** over field, no contact
  (pink, s.d. 4-6 in five slices). Below it, x 9240-9248, both metal shots show an 8 px
  bright streak over a smooth salmon poly box (9228-9248 x 7195-7235): not resolved
  (narrow metal neck, or the channel of a narrow load as in the latch's n2 load).
- From row C: the n2 poly (x 9453-9474) runs up to y 7325 and the q poly (x 9502-9520)
  to y 7380, both textured (over a channel or in the open) across the region
  9432-9545 x 7400-7470. VSS contacts: (9186,7205), (9185,7430), and on a tab of the
  next slice's rail (9507,7340) with its land 9482-9535 x 7320-7365.

Not resolved: everything in y 7160-7500 left of x 9440 and the bottom right
(y 7300-7500). Do not build on the list above beyond what it says.

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
| `cdp2_c_sK_bus` (K=3..7) | metal | x 9246 + dx at y 7425 and (all seven) at y 7821 (down, not followed) | into the row | data for row C's latches |
| `cdp2_a_c_sK_q` (K=3..7) | poly | x 9511 + dx, y 7425, going up | out, to row B2 | row C latch output |
| `cdp2_a_c_sK_n2` (K=3..7) | metal and poly | metal x 9336 + dx and poly x 9463 + dx, both at y 7425 going up | out, to row B2 | inverted output |
| `cdp2_a_c_s2_q` | poly | line L1, x 7990, y 7472, going left | out | output of row C's s2 |
| `cdp2_a_c_s1_q` | poly | line L2, x 7990, y 7513, going left | out | output of row C's s1 |
| `cdp2_a_c_s1_q` | metal | x 8338, y 7395, going up | out | same net in metal |
| `cdp2_a_c_s1_n2` | metal | x 8165, y 7395, going up | out | inverted output of s1 |
| `cdp2_c_s1_bus`, `cdp2_c_s2_bus` | metal | x 8118 and x 8535 at y 7395, going up | in | bus lines of s1, s2 after their jog |
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
3. **Metal below the end of track b** (x 9326-9348, from y 6252 down): a separate piece
   from track b (between y 6190 and 6252 neither metal shot of chip 1 shows metal, and
   the n2 load lies there). Over the left part of the VCC land (y 6258-6294) the clean
   shot is speckled like a contact under it in all five slices (mean 170,150,100,
   s.d. 17-30, against flat tan s.d. 2 at x 9360 between the two metals), and both
   metal shots show metal. Read: a second metal contacted to the VCC land, i.e. **the
   line at x 9329-9340 that runs down through channel 2 in s4..s7 is a VCC branch**
   (in s3 it stops at y 6340). Drawn `?M`/`?C` inside the cell only. Whoever traces
   row B1 should check where that line lands.
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
- **Channel 2 (y 6350-6900)**: 13 poly lines, their ends and contacts (none in s3..s7). `cdp2_lines.py`
  gives a first pass but breaks at every metal edge; check ends by eye. The far left
  (x 7600-8700) has contacts at about y 6690 (x 8120, 8300, 8700) and y 6800-6850.
- **L1 and L2 left of x 7990** (y 7472, 7513): the two left-going outputs of row C.
- **Ends of `cdp2_c_ld`** (y 7800): left about x 7650, right past x 10850.
- **Rows B1, B2** (y 6930-7480, s3..s7), channel 3 (y 7830-7960), row D (y 7980-8450):
  not started. Rows B get q and n2 of row C's s3..s7 from below (ports) and, from
  above, only the bus lines of row A and the VCC branch (Ambiguities 3). They are
  not the latch cell (findcell finds no copy). Composites: `--comp cdp2_b` (rows B,
  master frame 9150,6890:9590,7500), `--comp cdp2_a` (row A, 9150,5940:9590,6350),
  `--comp cdp2_ctop` (top of row C, 9150,7420:9590,7610).
- Row D was only seen at 0.4x: findcell gives five copies (s3..s7) and a weaker
  sixth at dx -781; check whether it is yet another row of the latch turned over
  (findcell with the latch core, all eight orientations, y 6350-8600, found only row C).
- Logic left of the rows (x 7600-8750).
- Rails are drawn only over row A (y 5960-6350) and row C (y 7425-7830); x of the VSS
  rails 8013, 8403, 8793, 9184, 9574, 9965, 10355, 10745, of the VCC rails 8229 ... 10571.
