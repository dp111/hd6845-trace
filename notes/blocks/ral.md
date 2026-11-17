# ral: the stage in front of the RA pad drivers (x 13990-16330, y 4250-4560)

## Status (2026-11-17 05:00, contributor session)

**Partly traced** (`trace/ral.txt`, cell `ral_cell`, five copies s0-s4 west to east; s0 is
RA bit 0's cell, at x 13990-14460). Drawn: the two supply rails per cell, the line
`cnt_gab` (y 4350) with its tap and the pull-down it gates, the strobe line `ral_stb`
(y 4548) with its pad and the input pass transistor, the input strip, the hold device
(gate on VSS) from node a to the output, the buried contact onto the output poly, s0's
input join to `rax_o0`, and the output stub to `ra0_drv_in`; and **every copy's input and
output joined**: `rax_o0`-`rax_o4` in, the RA0-RA4 pad drivers' input lines out. **Not drawn**: the two
inverters and their loads (the forward path from node a to the output), and the upper
part of the output poly. 15 transistors (three per cell).

### Logic (traced)

```
ral_a_s#  <- rax_o#    pass transistor 16/26 at (14041,4487) + 434 per cell, gate ral_stb
ral_a_s#  <-> out_s#   hold device 16/90 at (14245,4487) + 434, gate VSS (out_s0 = ra0_drv_in)
ral_tf_s# -> VSS       pull-down 66/20 at (14160,4413) + 434 per cell, gate cnt_gab
```

The hold device is the same structure as `cdp2_lat`'s (long weak device, gate on VSS,
believed depletion-mode): it feeds the output back onto node a, overpowered by the
input while `ral_stb` is high. With a non-inverting path a -> output (two inverters,
not yet drawn), that is the static latch of the register rows: **each RA output would be
latched, transparent while `ral_stb` is high**. Believed, not extracted: the forward
path is the missing piece.

How the hold device was read: the poly block 14200-14290 x 4448-4500 lies over field in
its upper half (row profile y 4462: field at x 14185-14195 and 14300-14360, poly only at
14205-14285) and over the input strip in its lower half; the dark line at y 4470-4476
runs the block's full width in every column profiled (x 14204, 14208, 14250, 14282,
14286), which is the strip's edge under the poly, not a gap between two polys. So it is
one block, and its only neighbour is the VSS-contacted poly pad above (dark line at
y 4447 between them = the VSS rail's edge; join drawn `?P`). The strip's east end meets
the output poly's bend under a heavy-outlined patch (14315-14347 x 4470-4500, clean
shot): drawn `?B`.

### Ports

| Name | Layer | Where (s0; +434, +868, +1431, +1865 for s1-s4) | Direction | What |
|---|---|---|---|---|
| `vcc` | metal | top rail y 4220-4268 | supply | by device orientation, not followed to a labelled rail |
| `vss` | metal | middle rail y 4397-4446 | supply | same |
| `cnt_gab` | metal | y 4346-4362, x 13895-16330 | in | the counters' `_m`/`_mb` gate line: drawn back to `wl`'s band H4 (glossary); first called `ral_frc` here |
| `ral_stb` | metal | y 4540-4556, x 13990-15910 (ends on s4's pad) | in | the sixth line of rab's bundle; drawn back 9,000 px to x 8350, where it is `tc1`'s ns4 (formerly `tc1_ns4`, renamed) |
| `rax_o0` | poly | (14000,4500), from rab | in | s0's input, onto the strip by a buried contact (`?B`: round ring in both stripped shots) |
| `rax_o1` ... `rax_o4` | poly | up x 13995 + dx from pads at (14430,4590), (14863,4635), (15425,4675), (15860,4632) to the buried contact on each strip | in | s1-s4's inputs; s2's and s4's pads at the ends of rab's metals (s4's goes on east along y 4722 to x 15862 and north) |
| `ra0_drv_in` | poly | x 14331-14349 at y 4480-4525, joins r9c's poly from the pad (14340,4764) | out | s0's output |
| `ra1_drv_in` | poly | s1's output poly down to a pad (14774,4592) on RA1's line y 4592 | out | |
| `ra2_drv_in_u` | poly | s2's output poly down to a pad (15208,4805), where r9c's RA2 unit line starts | out | |
| `ra3_drv_in_u` | poly, metal, poly | s3's output poly to a pad (15771,4593), metal east along y 4590 and south along x 16297, poly to a pad (16297,5108), where r9c's RA3 unit line starts | out | |
| `ra4_drv_in_u` | poly, metal, poly | s4's output poly to a pad (16205,4640), metal south along x 16207, poly to a pad (16205,5153), where r9c's RA4 unit line starts | out | |
| `ral_a_s#`, `ral_tf_s#` | diffusion | inside the cell | internal | node a (between the pass and hold devices) and Tf's drain; both continue into the untraced part |

### How sure

- Rails, line taps, contacts: metal composite and single shots at 2.6-4x; overlay
  `cache/scratch/ral/ov1.png`.
- The input strip: colour profile along y 4486 in both stripped shots
  (`tools/ral_prof.py row 4486 13985 14460 5`): not field from x 14015 to 14315, field
  at 14320-14340, again not field 14345-14390 (the output poly's horizontal piece).
  Down x 14120: diffusion at y 4479-4491, field at 4458-4467 (so the box of the
  pull-down Tf ends at the middle rail's edge, y about 4450; the dark line there is
  that edge).
- Copies: `cellcheck.py ral_cell --layer acid`: s1 0.6 %, s2 4.2 %, s3 1.2 % bad blocks;
  s4 15 %, all of it the strobe line ending at s4's pad and a wide rail at the band's
  east edge, outside the drawn devices.

### Not done (next)

1. **The forward path from node a to the output**: no buried contact from the strip
   (x 14055-14200) to any poly was seen; Tf's poly ends at y 4462, 17 px above the
   strip. Candidates: the L-shaped poly 14245-14345 x 4325-4370 / 14325-14345 x
   4370-4448 (a pull-down gate in the box 14252-14365 x 4378-4448, VSS contact at about
   (14265,4415), drain x 14348-14370, which seems to run up to a load under the top rail:
   poly block 14285-14365 x 4277-4310); and a vertical diffusion strip x 14200-14225,
   y 4300-4395, above the VSS pad. Two passes did not give a consistent circuit.
   Third look, with `metal1` (2026-11-17, `cache/scratch/ral/a2.png`, four shots of
   14000-14150 x 4370-4530 at 4x): east of the strobe gate the strip seems to have an
   arm going **north**, x 14055-14085, from the strip up to y about 4380 under the VSS
   rail (outlines in `metal1` and `acid`: a vertical edge at x 14083-14090 from y 4380 to
   4495; row profiles at y 4468, 4473, 4500 show colour at x 14058-14078 that the strip
   east of it does not have). Both metal shots show a ring at about (14045,4425), over
   the strobe poly's rounded top end (14010-14060 x 4405-4432). Neither is resolved: if
   the ring is a contact onto the arm, node a would sit on VSS, which makes no sense, so
   one of these readings is wrong. This corner is the next thing to settle (contact test
   `tools/cdp2_pt.py` on the ring; colour profile across x 14050-14095 at y 4420).
2. Whether Tf's drain `ral_tf_s#` (strip x 14172-14196) is the first inverter's output,
   i.e. n2 = NOR(a, cnt_gab), which would make `cnt_gab` a force/clear of the latch.
3. The output poly from y 4300 to 4480 (x 14375-14395): believed to be the second
   inverter's output node (its load's gate tie at about 14365-14395 x 4280-4310).
4. The copies' input and output polys (s1-s4), and the fifteen copies in the left array.

## First survey

Serial work, 2026-11-16. Survey only. Views in
`cache/scratch/rax/`: `ral1.png`, `ral2.png` (the band at 1.55x), `ralA.png`, `ralM.png`,
`ralC.png` (the master cell at 2.8x in the clean, metal and chip-2 stripped shots),
`ralq1.png` ... `ralq4.png` (its four quadrants at 3.6x), `ram1.png` ... `ram3.png`.

## What it is

A band of five copies of one cell, about 430 x 260 px. `tools/findcell.py` with the cell
at x 14020-14450, y 4265-4525 as master (clean shot):

| Copy | dx | Score |
|---|---|---|
| master | 0 | 1 |
| 2 | 434 | 0.93 |
| 3 | 868 | 0.89 |
| 4 | 1431 | 0.94 |
| 5 | 1865 | 0.84 |

and **fifteen more hits elsewhere, turned 90 degrees** (scores 0.78-0.82): fourteen in
the left array's untraced left column at x 2660 (y 8155, 8761, 9368, 9976, 10627, 11234,
12036, 12730, 13382, 15506, 16201, 17275, 17925, 18576; some mirrored), which is where
the `maN_drv_in` lines start, and one at (8449,5562), in the untraced corner below the
central datapath's top block. So this cell is the common stage in front of every memory
address and row address output: nineteen or twenty copies. Trace it once, check each
copy's ports.

## Ports of the master, as far as read

- **Rails**: a wide metal along the top (y up to 4270), a wide metal y 4395-4442 with
  contacts to two diffusion boxes (pits at (14117,4423) and (14262,4422)) and to a poly
  pad (14210,4420). Pull-down gates cross the diffusion beside both boxes, so the
  middle rail is taken to be VSS and the top one VCC (not followed to a labelled rail).
- **A thin metal along y 4350** through all five cells, with a tap up to a poly pad at
  (14156,4318) in each. Its poly (x 14148-14170) comes down across the diffusion under
  the middle rail, between the contact box at x 14100-14145 and a node at
  x 14172-14192: a pull-down gated by this line. Where the line comes from: not followed.
- **The sixth line of the row address bundle** (`notes/blocks/rab.md`): metal along
  y 4548 under the band, with a pad per cell ((14040,4548) for the master) and a poly up
  x 14035-14055 to y 4420. On the way it crosses a horizontal diffusion band
  (y 4478-4500): read as a pass transistor. So this line is the cell's strobe; the same
  cell in the left column sits beside the `ck_out` trunk, whose taps come every 608 px.
- **The poly pad on the middle rail** (14210,4420) goes down to two wide poly bars
  (x 14200-14292, y 4452-4472 and 4478-4502) over the diffusion bands there: the shape of
  the long weak device with its gate on VSS that the register latches use (`hold`).
- **Output**: an S-shaped poly, vertical at x 14372-14395 from y 4320 through the middle
  rail to y 4500, west to x 14345, south along x 14340-14362 to the pad (14340,4764),
  whence metal to the RA0 driver's poly at (15305,4762).
- **Input**: not placed. `rax_o0`'s poly arrives along y 4500 at x 14000 and `rax_o1`'s
  comes up x 14430 from the pad (14430,4590), i.e. at the left edge of the next cell.

A pass transistor on a strobe, two inverters and a weak feedback device is the static
latch of the register rows (`cdp2_lat`), so the working guess is: **each RA and MA
output is latched, transparent on the line y 4548 (RA) or `ck_out`'s trunk (MA)**, and
can be forced by the line y 4350. A guess until the cell is traced.

## Not done

The cell itself, device by device (start from the chip-2 stripped shot: most of the cell
has no metal over it); the two rails and the lines y 4350 and y 4548 to their sources;
the other four copies' inputs and outputs; the fifteen copies elsewhere.

## 2026-11-16 23:07  Second look (contributor session): readings before drawing

Median composite of the five RA copies: `composite.py ral_c 13990,4240:14460,4600
--offsets "0,0 434,0 868,0 1431,0 1865,0"`. In this band the chip-2 stripped shot (`acid`)
of the composite is the clearest view of poly; `classmap.py --comp ral_c --open` helps
with open diffusion. At 4x the composite is too blurred for junctions: use single shots
there.

Read (one or two views each; to be confirmed by overlay before drawing):

| Feature | Where | Reading |
|---|---|---|
| Top rail | metal y 4220-4270, whole band | joins a wide vertical metal at x 14950-15100 going north (survey at 0.4x). Load-shaped poly blocks hang below it (e.g. 14300-14360 x 4275-4305 over a diffusion strip): taken as VCC |
| Middle rail | metal y 4395-4447, whole band | contacts to diffusion at (14117,4423) and (14265,4415), and a contact to the poly pad 14200-14246 x 4398-4446 (green centre in the clean shot) at about (14222,4422): taken as VSS |
| Line y 4350 | metal y 4343-4359 | metal tab up to the poly pad 14142-14176 x 4303-4346, contact (14157,4318) |
| Pull-down Tf | poly x 14150-14170, y 4346-4466, over diffusion 14102-14196 x 4378-4448 | source on the VSS contact (14117,4423); drain the strip x 14172-14196. Gate = line y 4350. The poly runs on 20 px below the diffusion box (to y 4466) over a strip y 4450-4470: possibly a second device, not settled |
| L-shaped poly | 14245-14345 x 4325-4370, then down x 14325-14345 to y 4448 | crosses the diffusion box 14252-14365 x 4378-4448 (contact at about (14265,4415)) as a pull-down gate; drain x 14348-14365 |
| Output poly | vertical x 14375-14395, y 4300-4500 | as in the first survey |
| Two poly bars | 14200-14290 x 4455-4473 and 4480-4500, inside an outlined box 14195-14300 x 4450-4505 | joined to the VSS pad above? Not settled (the dark line at y 4447-4452 is not resolved at any zoom tried) |
| Strobe pass device | poly x 14028-14053, y 4440-4535, contact pad 14025-14058 x 4530-4562 on the metal y 4548 | crosses a horizontal strip y 4478-4500 (seen in both stripped shots) |

Open: whether the drain of Tf joins the VSS-poly pad side (x 14196/14200), how node a
reaches the gates, and where the diffusion strips y 4450-4470 and y 4478-4500 end on the
right (one turns up at x 14390-14420).
