# Journal

## 2026-11-14  M0: groundwork and pilot

Done
- Both shots converted to raw arrays; acid shot resampled into the metal frame
  (`tools/align.py`: affine fit over 270 patches, 0.57 px RMS, residual after
  resampling under 1 px almost everywhere, 2.5 px worst case).
- `tools/view.py` (two-layer views with grid and trace overlay), `tools/tracelib.py`
  (trace format, cells and mirrored instances), `tools/netlist.py` (extraction, rule
  checks, static gate recovery), `tools/build.py` (SVG, netlist, report, floor plan).
- Layer legend worked out on real structures (`notes/layers.md`). The process has
  buried contacts; loads are recognised by their gate-to-output tie.
- Pilot: `trace/pilot.txt`, two gates at 14280-14640 x 14880-15300. Extracts with no
  errors as `a_out = NOT in_a`, `b_out = NOR(a_out, in_c)`. The first overlay fitted
  without correction. A mirrored instance fits the right-hand half of the column.
- Coarse floor plan from a 12-tile survey at 0.2x (`floorplan.txt`, 68 blocks, all
  provisional) and repeat pitches by autocorrelation.
- Provisional pad table (`notes/pads.md`).

Found
- Automatic segmentation is not usable for geometry (reason in `notes/layers.md`).
- The first circuit tried, the RES/LPSTB buffers by the top pads, is a poor teaching
  example because it lies under wide rails; left as AMB-001.
- The die has two kinds of array: horizontal bit-slices at 390.3 px (central and right
  datapaths) and rows at 477 px (left and mid-right arrays). The left array is about
  25 rows tall, more than the 14 bits of MA, so it is not simply one bit per row.
- Rough size: about 26,000 px2 per transistor in dense logic, which puts the chip
  near 5,000 transistors.

Tracing rate
- Not yet representative. Understanding the legend took about 25 views. Once
  understood, a 380 x 380 px region with five transistors took one pass of entry and
  one overlay check. Estimate to be revised after M1 and M2: 300-ish unique dense
  regions after allowing for repetition, a handful of views each.

Not done yet (planned for later milestones)
- Image-space check of cell instances against their master (start of M3).
- Coverage checks (metal or contacts in the photo with no trace over them).
- Rule checks beyond the basics: floating gates, undriven nets.

Next: M1, the pad ring. Start by following the metal plane from the VSS pad and the
rail from the VCC pad to confirm which is which, then each pad's buffer or driver.

## 2026-11-14 (later)  M1 in progress: pad ring

Done
- VSS/VCC confirmed. The top-middle pad sits in the peripheral plane (outer ring =
  VSS). The bottom-middle pad feeds the band inside the pad ring (inner band = VCC).
  With pin 1 fixed, the mix of plain inputs, outputs with drivers and bidirectional
  pads round the die matches the pinout in only one orientation, so the pad table in
  `notes/pads.md` is now firm.
- Output driver cell traced once (MA3) and instanced at all 23 output pads
  (`trace/pads_out.txt`); every instance extracts as two inverters plus a push-pull
  pair, pad = NOT(core signal). Details in `notes/blocks/pads.md`.
- Input side: five identical protection cells under the bottom-right pads, in pad
  order CLK, R/W, E, then RS and CS (which of the last two is which is not yet
  followed to the pads). Each is a wide long-channel clamp to the rail at y 18968.
- Buffer row above them (`trace/inrow.txt`), traced from the left so far:
  gate 0 inverter (input from the core in poly, output leaves left along y 18775),
  gate 2 three-finger inverter fed by CLK, gate 1 two-finger inverter fed by gate 2
  (so gate 1 output is buffered CLK, leaving left along y 19070 towards the block at
  9550-12300 x 19050-19950), gate 3 R/W inverter, gates 4 and 5 inverters in a
  chain, giving both polarities of R/W.

New tools
- `findcell.py`: finds copies of a rectangle anywhere on the die in all eight
  orientations. It can lock onto the wrong finger of a periodic structure (MA11);
  check every placement by overlay.
- `cellcheck.py`: side-by-side picture of each instance against the master. The
  bad-block percentage is only a rough guide; look at the pictures.
- `composite.py` + `view.py --comp`: per-pixel median over all instances of a cell.
  Removes etch residue, debris and metal grain. This is what made the logic under
  the VCC band readable. Use it for every repeated cell.
- `view.py --shift dx,dy`: look at another instance in the master's coordinates. Raw
  metal of a clean instance shows where metal really is (grain = metal).

Things learned about reading the die
- Two logic-cell styles. Small gates: load is a tall poly block (about 70 x 105) over
  a 27 px diffusion strip coming down from a VCC contact, W/L about 0.25; the block
  is tied to the output by a buried-contact box at its lower corner; outputs often
  leave through a second buried contact into a poly bar that becomes the next gate's
  input. Big buffers: load block beside a VCC diffusion strip with the channel
  running sideways under it (W/L about 1.8), and a two- or three-finger pull-down
  with a metal strap joining the outer diffusions.
- Under wide metal the acid shot is unreliable in any single instance (residue,
  fringes). Dark lines seen through metal are edges of poly or diffusion beneath.
- Keep rendered views under about 1400 px wide; wider ones are downscaled on read.

Open
- AMB-003: data pad cell, layers under the VCC band (parked until M2).
- AMB-001 can now be re-read: the RES/LPSTB buffers use the same big-buffer cell as
  gates 1 and 2 of the buffer row.
- Pad squares and the two supply rings are not drawn yet (only MA3's pad).

Next
- Finish the buffer row to x 17500 and the wiring below it (bus lines at
  y 18620-18750, four large rectangles at y 18575-18794, links to the protection
  cells and pads). Then RES and LPSTB, then the block left of the CLK pad.

## 2026-11-14 (end of session)  M1 status

Traced and extracting cleanly (290 transistors, no rule errors):
- 23 output drivers (cell `outdrv`).
- Bottom-right inputs: five protection cells (`inprot`), CLK and E two-stage buffers
  (`buf3f` + `buf2f`), R/W, RS and CS four-inverter groups (`ingrp`), R/W taps and
  their two diffusion rectangles, one unidentified inverter at the left end.
- Top inputs: LPSTB and RES two-stage buffers (`topin` + flipped `buf2f`).

Still to do for M1, in the order I would take them:
1. The block left of the CLK pad (9550-12300 x 19050-19950) and the wiring between
   it and the input row (12400-13700 x 18500-19600). `clk_b` arrives there on the
   metal at y 19056 (ends at a contact at 12570,19055); the CLK node itself also runs
   left on the metal at y 19103 and turns down at x 12615. A U-shaped poly joins the
   contacts at 12570,19055 and 12852,19103, which cannot be a plain link between
   those two metals, so there are transistors here that need 2.4x views. The block
   has two large multi-finger arrays (9570-10650) and tall rectangles that look like
   bootstrap capacitors (10920-11700 x 19350-19850). This is where the internal clock
   phases are made.
2. Wiring below the input row: strips from pads to protection cells and on to the
   buffers, RS and CS taps and rectangles, and the lines that leave to the right at
   y 18615-18750 (`rw_d`, RS node, `rs_d`, CS node).
3. The two comb protection cells by LPSTB and RES.
4. Pad squares and the two supply rings as drawn metal.
5. Data pad cell (AMB-003), after the bus-interface logic that drives it.

## 2026-11-15  Clock block

Result
- The main internal clock is NOT CLK. The CLK pin node runs along the bottom of the
  block and drives, through a single contact, a three-stage buffer built from the
  two big arrays: inverter (3 fingers of W 480), inverter (2 fingers), then a
  push-pull pair whose pull-up gate is the inverse of its pull-down gate. No gating,
  no division. Output `ck_out` goes up into the core at x 10845-10870 and away to
  the left at y 19240-19262.
- A gate row of six inverters buffers a global signal `ck_src` into both polarities
  (lines A and B). Those go right into the core, and down into a "driver logic" of
  two mirrored circuits together with CLK. `ck_src` was followed 4000 px along the
  bottom bus field to the foot of the left bus field; its source is not known.
- The driver logic is not traced (AMB-007).

Traced: 321 transistors in total, no rule errors. New in the tools: an `edges`
layer in view.py (outlines present in both photos), an annotation layer for
devices that are off in normal operation (`A ... kind=clamp|field`), and `@alias`.

Corrections to earlier work
- Input protection cells redrawn from 4x composites: the pad arrives in poly, a comb
  of buried contacts ties it to the node, and the wide band above is a thick-oxide
  clamp (AMB-005). The previous drawing had the pad strip as diffusion.
- The six "island" devices in the clock wiring are taken to be clamps to VCC
  (AMB-006).

Method notes
- Following one metal line across the die by eye is slow (about one view per
  1300 px at full scale). Lines in the bus fields should be traced as bundles when
  those fields are done, not one at a time.
- Big multi-finger devices are quick: columns of contacts and gate strips read
  directly at 0.9x, and a schematic rectangle per group is enough for the netlist.
- The decisive questions were all junctions: which poly reaches which contact.
  Each took one 5-6x view. Deciding early which junctions matter, and looking only
  at those, would have saved many of the survey views.

Next
- M2: bus interface and register decode. `rw`, `rs`, `cs` and `e` are ready at the
  input row; the decode array is at 14180-15780 x 13480-14680.
- Carry AMB-007 and the source of `ck_src` as open items to pick up from the core.
