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

## 2026-11-15 (later)  Second die, clock generator, register decode

Three shots of a second die were added and registered into the reference frame
(`tools/align.py`, layers `metal1`, `acid1`, `acid1b`). `acid1b` (hd6845acid2.jpg) is
clean and changes what is readable; its colour legend is in `notes/layers.md`.

Done, in the order agreed
1. Legend for the clean shot, calibrated on six known places. Two lessons: metal
   protects a margin beyond its edges (narrow gaps between lines leave only a thin
   dark bar), and the colours shift across the die (open diffusion is green near
   the edge, pink in the decode array), so the legend must be re-checked locally
   against structure.
2. Clock driver logic: it is a two-phase non-overlapping clock generator.
   `ck_a` = NOR(delayed `ck_b`, CLK), `ck_b` = NOR(delayed `ck_a`, NOT CLK). Traced.
   The earlier reading of this block from the chip-2 shots was wrong in several
   places; the note in `notes/blocks/clock.md` replaces it.
3. Data pad cell: re-read, much more established, still not traced. It has more
   logic than two inverters. Parked again with the facts listed (AMB-003).
4. Existing traces checked against the clean shot: gate groups, protection cell and
   output pre-driver agree; the two inferred joins in the clock output stage are
   confirmed.
5. Register decode array read (`notes/blocks/decode.md`): 18 columns, each a 5-input
   NOR, selecting R7 R6 R4 R0 R2 R1 R10 R5 R3 R8 R9 R11 R13 R12 R14 R15 R17 R16 from
   left to right. Read by measuring colour at every crossing, with four independent
   consistency checks.

Trace: 443 transistors, no rule errors.

Method notes
- Regular arrays should be measured, not eyeballed: at 2.7x my impression of
  which crossings had transistors was wrong in places where the colour measurement,
  backed by the consistency checks, was right.
- Phase correlation fails inside regular arrays, so `acid1b` registration there is
  interpolated. Calibrate row and column positions from profiles before sampling
  (`tools/pla_read.py` hard-codes the measured ones).
- A cell that resists two passes should be left until its inputs are known. The
  data pad cell cost about 25 views over two sessions without a consistent reading.

Next
- M2: row drivers of the decode array and the address register; the cells above the
  array; where the 18 select lines go; then the bus interface that produces the two
  lines into each data pad cell, and back to AMB-003.

## 2026-11-15 (night)  Parallel round

Twenty-six agent runs on seventeen blocks, each working from `notes/tracing-guide.md`
on its own files. The round ended when the usage limit was reached; the last eleven
runs were resumed after it reset and all reported. By the user's instruction, work
is serial again from here.

All blocks together: 2,593 transistors, no rule errors, no warnings (443 before the
round). Cross-block joins are in `trace/zz_joins.txt`.

Established by tracing
- Register decode rows come straight from a 5-bit address register (five transparent
  latches above the decode array); five inverters right of the array make the
  complement rows.
- Register strobes: `sel_wN` = (register N selected) AND NOT `sel_stb_r` for R0-R15;
  R12-R17 also have a buffered select (believed read enables); R16/R17 have no strobe.
- `sel_stb_r` is the output of a latch, open while E is high:
  `c = NOR(rw_d, m255, cs_d)` with m255 believed NOT rs_d, `n1 = NOT(qb OR (E AND NOT c))`,
  `qb = NOT(n1 OR (E AND c))`, `sel_stb_r = NOT n1`. Nothing traced closes the strobe
  when E falls. The address register's load strobe is
  NOT(NOT(x OR (E AND NOR(rw_d, rs_d, cs_d)))), x unknown.
- Horizontal registers in the right datapath, identified by following their strobes:
  R0, R1, R2 (8 bits each) and R4 (7 bits), each with an equality comparator
  (true XOR per bit, wired-NOR line) against per-slice `c` lines. R0 has a second
  comparator against R0 shifted one place (R0/2), 7 bits. No `c` line is driven in
  the right datapath: all leave at its lower left.
- Central datapath: static register rows (6, 5, 6, 8 bits, the last two readable onto
  an 8-line bus), two 5-bit comparators (one plain equality with one bit's register
  input replaced by a three-term function from the logic beside it; one with a ripple
  chain between slices), a 4-way selector with three latch rows. No counter found.
- Left array: the 14-bit memory address counter (incrementer with carry groups of
  7, 3, 4; dynamic node taking the incremented value or a load value; static stored
  bit; clear device). Reload path and bit numbering not yet traced.
- Mid-right array: 19 rows in groups of 4, 3, 4, 4, 4; an AND chain over a per-row
  node q with group look-ahead, toggle-like logic, a stage clocked by `ck_a` and
  `ck_b`; right-hand columns not traced.
- Global wiring: `ck_out`, `ck_a`, `ck_b`, E, R/W, RS, CS, RES, LPSTB mapped to their
  first entries. The clock block's `ck_src` is not `ck_a`: it is the inverse of a
  core signal X, whose driver is an inverter in the gate column left of the select
  logic; X also gates a latch there.

Corrections made during the round (each was a wrong statement at the time)
- `ck_src` = `ck_a` (mine, from a 1.1x view): no such link.
- "strobe = NOT E" (one agent): the line it followed is broken; settled by a second
  agent's measurement.
- "this row is R0" (one agent): a track-scanning tool bridged a jog; two later runs
  agree it is R2.
- Several briefs of mine guessed structure wrongly (address register position, data
  bus units per pad, "logic" that was a routing channel, eight slices everywhere).

What worked
- One file prefix per block, `TRACE=` isolation, a locked commit script, and a ports
  table per block. Joins show up as multi-name errors in the combined extraction and
  are resolved in one coordinator file.
- Independent re-derivation: both wrong identifications above were caught because a
  second agent reached the same wires from another side.
- Measurement over impression: colour profiles for junctions, grain for metal breaks.

What did not
- Yield per run: 60-80 images buys one or two cells in an array (100-250 transistors
  with repetition) or about 25 transistors of random logic.
- Track-scanning tools are not safe for connectivity (bridges at jogs, false breaks).
- The clean shot's colours are local; three blocks needed their own legend.

Next (serial, in this order)
1. Mid-right array, x 12770-13040 and its wiring channel: is q the stored bit of a
   counter, and do its 19 outputs become the `c` lines the horizontal and vertical
   comparators use? (Groups 4+3, 4+4, 4 would fit a 7-bit, an 8-bit and a 4-bit
   counter; that is a hypothesis.)
2. Where the R0, R1, R2, R4 match lines go (tracks k7, k8 of the strobe channel and
   onward): the horizontal control logic.
3. The lower half of the top-centre logic (source of the three signals that modify
   one comparator bit), and the cross-coupled group below the central datapath.
4. Memory address counter: reload path and bit numbering.
5. Remaining rows of both datapaths; data bus; pad ring; then simulation (M5).

## 2026-11-15/16  Serial again: the counters

After the parallel round, back to one block at a time (user instruction). Two requests
from the user during the session, both recorded in `PLAN.md` and `CLAUDE.md`: a "visual
6845" as a deliverable (so every transistor is to be traced, M7), and schematics that
show registers, comparators and counters as blocks plus one gate-level sheet per kind.

**Established**

- The mid-right array is three synchronous counters built from one bit cell: 8 bits
  (rows r11-r18), 7 bits (r4-r10), 4 bits (r0-r3). The cell is a master-slave pair:
  `na = NOR(L3, NOT m)`, master `a` takes `na` on the master clock, `p3 = NOT a`,
  `d = n1 = NOT p3`, slave `q` takes `d` on the slave clock; `m` is the next value, made
  from `q` and the carry. Extracted, 629 transistors, all 19 rows checked against the
  master in two shots.
- **The 8-bit counter is the horizontal character counter.** Its master outputs `n1`
  are the `c` lines of the R0, R1 and R2 comparators: six of the eight joins closed by
  geometry when the wiring channel was drawn (rdp3's and bd1's ports met mine), the
  other two are named in both blocks' notes. Bit 0 is the bottom row; in the right
  datapath slices s1..s7 are bits 0..6 and s0 is bit 7.
- **The comparators see the master, not the slave.** What leaves each bit is `n1`, the
  buffered master latch, which already holds the next count during `ck_b`.
- **The three counters have separate clocks.** The horizontal and the 4-bit counter run
  on `ck_b`/`ck_a` every cycle. The 7-bit counter's master and slave clocks are two bus
  lines from the west (E and D of the routing channel between r3 and r4), so it steps
  only when the logic there pulses them. Its outputs go to the upper right array (the R4
  and R6 comparators): the character-row counter.
- rdp2's unidentified 7-bit register "RF" is **R6**: its strobe line runs down track T0
  of the wiring channel into bd1's `sel_w6`.
- `ck_a` reaches the 4-bit counter by a diffusion cross-under, a tapless line through
  rows r10-r4 and a bus line; the same bus line carries `ck_a` on west.
- Fourteen cross-block joins closed by geometry (`trace/zz_joins.txt`); full extraction
  2,745 transistors, 0 errors, 0 warnings.

**Corrections to what was reported before**

- "`q` is a line from outside, so the array is probably not a counter" (third mra run,
  repeated in my last summary): wrong. The `q` poly ends in a buried contact on the slave
  pass gate. My own hypothesis in that summary (8 + 7 + 4 counters) is what the trace
  now shows.
- "The line x 12902 is `ck_b`" and "the rail x 13025 is `ck_a` for all 19 rows" (third
  run and trunks): both wrong. The first ends free above the `ck_b` contact and is fed
  from the top; the second is three pieces on three nets.
- My first drawing of L3 for rows r4-r10 had no feed (AMB-008). It has one: its widened
  lower end turns onto a contact I had given to the neighbouring line.
- Twice in this session the eye joined two diffusions in the clean shot that a colour
  profile showed to be 20 px of field apart.

**Tools and method**

- `tools/classmap.py` and `view.py --layers class`: false-colour class map of the clean
  shot (poly / channel / diffusion / field). It made the fourth column readable in an
  afternoon. Limits are in its docstring and in `notes/blocks/mra.md`.
- `tools/strips.py`: a long channel as strips side by side, any layer, with the trace.
- **Wiring channels must be read in the clean shot.** Poly runs hidden under the metal
  tracks for hundreds of pixels; the metal shot shows none of it. bd1's and bd3's
  channels were read mostly from the metal shot and should be looked at again.
- Where no metal lies above, the chip-2 metal shot shows diffusion directly.
- A through-line drawn "once, full length" by an agent is a claim about every routing
  channel it crosses. Three of those claims were wrong here. Check each crossing.

**Open, in the order I would take them**

1. The logic west of the counters (x 10400-11700 and the bands above row r0): it makes
   the row counter's two clocks (bus lines D, E), its L3 line (metal along y 13005), the
   carry-ins of r10 and r18, `mra_gab`, and it receives the R2 match (bus line F/G) and
   `ck_a` (bus line C). This is the end-of-line / end-of-frame control: M4.
2. The rest of the bit cell: node `m`'s pull-up and the unresolved branch (B3, B4, load
   1 in `mra_col2`). Until then "next = q XOR carry" is believed, not extracted, and how
   a counter is cleared is unknown (L3 is `ck_a` for the horizontal counter, verified by
   following its poly in the clean shot, so the clear is not there).
3. North of the array (y < 7130): the 4-bit counter's outputs, `sel_w3`, `sel_w5`, L3 of
   r0-r3 and the VSS/VCC rails all leave there (`amr`, `rdp1`).
4. The east ends of the wiring channel that rdp2 saw and did not draw (row counter bits
   r4-r6, bus lines A, B, F), and the stretch between rdp3 and bd1 (bits r13, r14, r17).
5. Then as before: remaining datapath rows, data bus and pad cell (AMB-003), bd1/bd2/bd3
   re-read in the clean shot, top-left / left-centre / bottom logic, pad ring.

