# cdp2: central datapath, rows y 5700-8450 (x 7600-10850)

Trace: `trace/cdp2.txt`. Scratch: `cache/scratch/cdp2/`. Tools: `tools/cdp2_pt.py`
(colour at points, both chips; used to test for contacts), `tools/cdp2_map.py` (text map
of colour classes), `tools/cdp2_lines.py` (follow a horizontal poly line by colour),
`tools/cdp2_mo.py` (stripped shot with the metal outline). `tools/rdp3_sharp.py` (unsharp
mask) at 3.3-5x on a median composite (`--comp cdp2_a`) is what made the junctions readable.

## Status

- Row A (y 6020-6345, five latch cells, slices s3..s7): cell traced, placed five times,
  overlaid on both layers, extracts as 5 x 6 transistors, no errors. Shipped.
- Everything else in the range is surveyed only (Inventory, Not done).

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
| 5700-6060 | channel 1: horizontal poly lines (at least y 5980, 6000, 6040; more above), crossed by the per-slice metal lines; contacts on some crossings | - | not traced |
| 6020-6345 | **row A: five static latch bits** `cdp2_lat` | s3..s7 (x 8790-10745) | traced |
| 6000-6310, x 7700-8300 | random logic left of row A | - | not traced |
| 6314-6334 | row A's load strobe `cdp2_a_ld` (poly, loops through every cell) | - | traced inside the row; ends not followed |
| 6350-6900 | channel 2: 13 horizontal poly lines, pitch 43.3, at y 6366, 6410, 6456, 6498, 6542, 6584, 6626, 6672, 6714, 6756, 6802, 6844, 6888. Per-slice metal lines and rails cross over them | - | not traced |
| 6930-7200 | row B1: cell, 5 copies (findcell 0.88-0.90) | s3..s7 | not traced |
| 7200-7480 | row B2: cell, 5 copies | s3..s7 | not traced |
| 6900-7480, x 7900-8750 | irregular logic left of rows B | - | not traced |
| 7530-7820 | row C: cell, 7 copies (dx -1172, -781, -390, 0, 390, 780, 1170) | s1..s7 | not traced |
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
- **Track b** (metal x 9325-9347): comes from above and ends at y 6187 over the n2 land.
  **No contact there** (flat tan, s.d. 4-5, all five slices). So in this row the track
  is not connected to the cell. A separate metal piece at the same x starts lower down
  (present on both chips from about y 6258, clear at y 6348) and continues into channel 2;
  where exactly it starts is not settled (Ambiguities 3).
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

Believed: a 5-bit register written from five bus lines when its strobe is high. Which
register is not established (5-bit candidates: R5, R9, R11, R10's low five bits).

All five instances compared (cellcheck, both layers): s5, s6, s7 identical (0-3 % bad
blocks). **s3 differs above the cell** (y 5985-6105): its track b has a contact at
(8943,6045) to a pad at the end of a channel-1 poly line (y 6034-6048, coming from the
left), and there is an extra vertical metal line at x 8893-8908 between the bus line and
track b that seems to bend right at y 6070. Not traced; the cell itself (below y 6105)
matches.

## Ports

| Name | Layer | Where it crosses | Direction | What |
|---|---|---|---|---|
| `cdp2_a_sK_bus` (K=3..7) | metal | x 8856, 9246, 9636, 10026, 10416 at y 5985 (up into channel 1) and y 6345 (down into channel 2) | into the row | data for the latch; not followed either way |
| `cdp2_a_sK_q` | metal | x 9509 + 390(K-4) at y 5985, going up | out | latch output, same sense as the bus |
| `cdp2_a_sK_trkb` | metal | x 9336 + 390(K-4) at y 5985, going up | - | track that ends over the n2 land without a contact |
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
3. **Track b, lower piece**: metal at x 9326-9348 is certain above y 6187 and at y 6348
   and below. Between, over the n2 load and the left part of the VCC land, the metal
   shots disagree (chip 2 bright, chip 1 not). Drawn: nothing below y 6187. Needs a
   look at y 6250-6400 on both metal shots; it decides whether the track from above is
   the same wire as the line at x 9333-9340 in channel 2.
4. Small dark boxes in the open beside the strobe gate (9270-9297 x 6244-6260 and
   9277-9298 x 6288-6313): read as bulges of the strobe poly over field. No diffusion
   there, so no device.

## Not done

- **Channel 1 (y 5700-6060)**: which poly line each bus line, q line and track b meets.
  This is what will name the register. Start at s3's contact (8943,6045).
- **Ends of `cdp2_a_ld`**: right of x 10850 at y 6324; left end near x 8520, y 6324.
- **Channel 2 (y 6350-6900)**: 13 poly lines, their ends and contacts. `cdp2_lines.py`
  gives a first pass but breaks at every metal edge; check ends by eye. The far left
  (x 7600-8700) has contacts at about y 6690 (x 8120, 8300, 8700) and y 6800-6850.
- Rows B1, B2 (y 6930-7480), row C (y 7530-7820), channel 3 (y 7830-7960), row D
  (y 7980-8450): not started. Composite of row A: `--comp cdp2_a` (master frame
  9150,5940:9590,6350, five instances).
- Logic left of the rows (x 7600-8750).
- Rails are drawn only over row A (y 5960-6350).
