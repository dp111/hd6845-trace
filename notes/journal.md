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
- A gate row of six inverters buffers a global signal `inh_ck` into both polarities
  (lines A and B). Those go right into the core, and down into a "driver logic" of
  two mirrored circuits together with CLK. `inh_ck` was followed 4000 px along the
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
- Carry AMB-007 and the source of `inh_ck` as open items to pick up from the core.

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
- Register strobes: `wr_rN` = (register N selected) AND NOT `wr_stb_n` for R0-R15;
  R12-R17 also have a buffered select (believed read enables); R16/R17 have no strobe.
- `wr_stb_n` is the output of a latch, open while E is high:
  `c = NOR(rw_d, m255, cs_d)` with m255 believed NOT rs_d, `n1 = NOT(qb OR (E AND NOT c))`,
  `qb = NOT(n1 OR (E AND c))`, `wr_stb_n = NOT n1`. Nothing traced closes the strobe
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
  first entries. The clock block's `inh_ck` is not `ck_a`: it is the inverse of a
  core signal X, whose driver is an inverter in the gate column left of the select
  logic; X also gates a latch there.

Corrections made during the round (each was a wrong statement at the time)
- `inh_ck` = `ck_a` (mine, from a 1.1x view): no such link.
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
  of the wiring channel into bd1's `wr_r6`.
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
   carry-ins of r10 and r18, `cnt_gab`, and it receives the R2 match (bus line F/G) and
   `ck_a` (bus line C). This is the end-of-line / end-of-frame control: M4.
2. The rest of the bit cell: node `m`'s pull-up and the unresolved branch (B3, B4, load
   1 in `mra_col2`). Until then "next = q XOR carry" is believed, not extracted, and how
   a counter is cleared is unknown (L3 is `ck_a` for the horizontal counter, verified by
   following its poly in the clean shot, so the clear is not there).
3. North of the array (y < 7130): the 4-bit counter's outputs, `wr_r3`, `wr_r5`, L3 of
   r0-r3 and the VSS/VCC rails all leave there (`amr`, `rdp1`).
4. The east ends of the wiring channel that rdp2 saw and did not draw (row counter bits
   r4-r6, bus lines A, B, F), and the stretch between rdp3 and bd1 (bits r13, r14, r17).
5. Then as before: remaining datapath rows, data bus and pad cell (AMB-003), bd1/bd2/bd3
   re-read in the clean shot, top-left / left-centre / bottom logic, pad ring.

## 2026-11-16 West of the counters: the row counter's clock generator

Serial. Blocks `wl` (new, complete) and `bw` (new, wiring part-way). Full extraction
1,669 nets, 2,768 transistors, 0 errors, 0 warnings.

**What was established**

- West of the counters there is almost no logic: x 10850-11700 below y 9450 is a bus field
  of about twenty vertical metals. The logic is one block beside the 4-bit counter
  (x 11080-11660, y 6950-9150), 23 transistors, all extracted (`notes/blocks/wl.md`).
- **The character-row counter's two clocks are made there from one step pulse `p`** by a
  non-overlapping generator: slave clock = NOR(buffered master clock, p), master clock =
  NOR(NOT p, buffered slave clock). The two NOR drivers are 350 px wide with strong loads.
  So the row counter's master latches take the next count while `p` is high and its slaves
  pass it on when `p` is low again: one step per pulse of `p`.
- **`p` = NOR(a, b).** `a` is `inh_rc`, the same core signal whose other copy (`inh_ck`)
  holds `ck_b` low in the clock block: one signal stops both the horizontal counter's
  master clock and the row counter's step. `b` comes from far away: followed west along the
  central datapath's channel 3, north in a nested bundle at x 7790-7930, west through the
  crossing field x 6330-7700 to a contact (5838,7470) and up a metal x 5841 that goes north
  into the top-left logic (`notes/blocks/bw.md`).
- `ck_a` and the R2 match (the horizontal sync position) are taken west on the same
  channel; `ck_a` then goes north at x 7421, the R2 match ends on a metal at x 8340.
- The VSS rail of the block feeds mra's "rail x 11828" (mra's open point A4, closed).

**Corrections**

- mra's line x 12285 (`cnt_la_a`), "one metal through all nineteen rows, no contact", is
  three pieces cut at two of the four routing channels. The top piece feeds an inverter in
  `wl` and nothing found drives it: a contact has been missed in the rows (re-read R8).
- cdp2's note that the channel-3 lines "turn down" at their west end: they turn north.

**The user's instruction about revisits (2026-11-16)**

"Make sure the need to revisit is noted somewhere where it will be done later, and please
learn from this for the future." Done as: a **Re-read list** in `notes/work-packages.md`
(nine entries now, each a task with region and reason, to be worked off before M5), a
Re-read rule in `CLAUDE.md`, and traps 10-12 in `notes/tracing-guide.md`. A doubt about
earlier work goes on that list in the same commit; a remark in a report does not count.

**Tools and method**

- `tools/classmap.py --open`: where neither chip has metal, the class comes from the two
  chip-2 shots, which show open diffusion redder than open field. In the clean shot alone a
  wide open diffusion is only slightly greener than field (it had been read as field) and
  appears as pink boxes with heavy outlines between metals. With this the big drivers
  could be read in one pass.
- A crossing of a poly line under a metal in the clean shot shows a dark ring at each metal
  edge. That is the metal's margin, not a contact: a contact has a widened pad and a green
  dot. All five channel-3 lines cross twenty metals this way with no contact.
- Trap 11 struck again within the hour (`cnt_la_a`). Any line longer than one row group gets
  looked at where it crosses each routing channel before it is used.

**Open, in the order I would take them**

1. The source of `b`: the metal x 5841 north of y 6300 (top-left logic, `tl`). That is
   where the row counter's step is decided (scan line count, end of line): M4.
2. What `a` / `inh_ck` is: bd1's `inh_src`, which comes from the bottom bus field.
3. Re-read R8/R9 in the counters (the line x 12285 and node `z`), then the rest of the bit
   cell (node `m`'s pull-up, B3/B4): the counters' next-state and clear are still not
   extracted.
4. North of the counters (`amr`): the 4-bit counter's outputs, bands H0/H1/H4, `la_n`.
5. The bus field's own lines; the ends of the other channel-3 lines; then as before.

## 2026-11-16 (later) The row counter's step followed to its gate

Serial. Blocks `bw` (route completed), `tla` (new, three gates). Full extraction 1,676
nets, 2,778 transistors, 0 errors, 0 warnings.

**What was established**

- `rc_stepreq_n`, the row counter's step, was followed to its driver: up the metal x 5841 to
  (5838,5585), west as poly through a second crossing field to (3518,5587), by metal to
  (3283,5238) and by poly to a buried contact on the output node of a gate at (2975,5035)
  in the top-left logic. About 9,000 px of wire from the counters, all drawn.
- That gate: **`b = NOR(in1, in2, in3)`**. Beside it: `in3 = NOR(e3, e4)` and
  `m2 = NOR(in2, in3)`. All three extracted (`notes/blocks/tla.md`). So the row counter
  steps when `in1` or `in2` is high, or when `e3` and `e4` are both low.
- `in1`, `in2`, `e3`, `e4` each lead on into bus fields: `in1` up a 2,200 px bus line and
  east along the top of the logic to another field at x 4140-4420; `in2` to a poly going
  west at y 5411; `e3` and `e4` onto two more bus lines. None reached a gate yet.

**What it means for the plan**

The top-left "logic" (2100-6400 x 2500-6350) is gate clusters joined by bus fields whose
lines are in pieces. Chasing one signal at a time does not converge there. It has to be
traced whole: every cluster, and every bus piece with its contacts. That is the bulk of M4
and it is large (my estimate: 300-500 transistors and several hundred wire pieces). It
would divide well among parallel agents (one cluster or one bus field each), which by the
standing rule needs the user's word.

**Method notes**

- Under a wide rail the clean shot shows field as pink with an olive stripe down the
  middle, and the class map paints the stripe as diffusion. It is not: diffusion under a
  rail is the tan boxes only. (Read as a continuous column at first; it would have made a
  transistor with VSS on both sides.)
- A load plate in the open shows the edges of the diffusion strip under it as two dark
  lines across the plate, so one plate over a 28 px strip looks like two or three plates.
  The chip-2 shots show it as one piece of poly.
- A bus line piece and the next piece at the same x can be 40 px apart end to end. Every
  bus line is followed in both shots; a 1x metal view shows one line.

**Open, in the order I would take them**

1. The cluster x 2440-3090, y 4590-5330 in full (R1's columns, the remaining loads, the
   column above gate E0, the thin metal's taps), then the vertical bus x 3090-3380 piece by
   piece, then the clusters above and below it.
2. The rest as listed in the previous entry (what `a` is; re-read R8/R9; `amr`; the bus
   field between datapath and counters).

## 2026-11-16 (night) The step logic, three levels deep

Serial, block `tla`. Full extraction after this entry: see the ship line. User: "carry on
serially for now please. The NOR gates are intriguing and I would love to know what they
are doing."

**What was established** (all extracted, `notes/blocks/tla.md`)

- step = in1 OR (NOT e4 AND ((x1 AND NOT a2) OR NOT e3)), from seven gates:
  b = NOR(in1, in2, in3); in2 = NOR(w2, e4); in3 = NOR(e3, e4); w2 = NOT c1;
  c1 = NOR(a2, b1); b1 = NOR(x1, a2); and m2 = NOR(in2, in3), the complement of the
  bracket, which feeds further logic in the same column.
- The cluster is two mirrored columns of small NORs either side of a VCC rail, each NOR on
  a diffusion column beside a VSS rail with its load between the rails. It runs from
  y 2940 to 5330.
- `e4` is a global: 7,000 px followed, from the cluster to the left bus field at x 6559,
  still going south. Every contact on it so far is a gate.
- `e3`, `a2`, `x1` all come from the east (y 2728, 3761, 3547); `in1` from the bus field
  at x 4279.

**Not established**: what any of the five inputs is. The reading "end-of-line strobe and
scan-line comparisons" is a guess from the formula's shape.

**Corrections**

- The round blob at each load's lower corner is the load gate's buried-contact tie, not a
  metal contact to the thin metal (I had drawn in3's node onto the thin metal).
- Bus line A's pieces A1 and A2 are 35 px apart end to end, with the gate poly visible
  between their pads: settled at 6.5x in both chips. Had they been one piece, c1's output
  would have been tied to its own input.

**Tools**

- `tools/tla_tracks.py`: where a track has metal; `tools/tla_contacts.py`: contact
  candidates on a track from the clean shot's colour. Both only say where to look.
  The contact finder missed A2's third contact (3103,3762) on the first pass because the
  line's x drifts 8 px along its length: profile at the measured x of each stretch.
- `strips.py --layer class`: 3,000 px of a bus in one image, pieces, crossings and contacts
  all visible.
- A net with gates on it and no driver means a contact is still missing: it found A2's.

**Open, in the order I would take them**

1. `e4`'s source: on south down the left bus field (x 6559 from y 8850); and from the
   other side the R0 match line on bd1's k7/k8 (re-read item R1 covers that channel).
2. The rest of this cluster: y 3400-4590 east, the west side above y 4940, b1's load.
3. `in1` (bus field x 4140-4420, then the middle or right gate column), `e3`, `a2`, `x1`
   to the east.
4. As before: what `a` (`inh_rc`) is; re-read R8/R9; `amr`; the bus fields.

## 2026-11-17 The chase of e4

Serial, blocks `tla`, `trunks`. Full extraction 1,683 nets, 2,789 transistors, 0 errors,
0 warnings. User: "shall we carry on then?"

**Aim**: name `e4`, the input that gates the whole step logic. **Not achieved.**

**What was established**

- `e4`'s net is drawn end to end: 17,000 px from the top-left cluster to a gate in bc1's
  left column at (7317,15435). It has five loads, all gates; its driver was not found.
- It is not RES and not `m2` (both looked possible; both refuted at high zoom).
- `res_b` and `lpstb_b` are traced to their ends: lines 3 and 4 of a five-line poly bus at
  x 5100-5290, where `e4` is line 5. From there all five go east together.
- bc1's 13-line bus line y 14526 is two nets split at x 7012/7100.

**Tools**

- `tools/follow.py`: follows one metal line through corners and diagonals using both
  chips' metal shots. Tested on four hand-traced lines. Two faults found and fixed in use:
  it bridged a gap before looking for a corner (stepping onto the next line of a
  staircase), and its corner test did not bridge the 4-8 px step line where metal comes
  off a poly edge. One fault remains: it can miss a corner right at a contact-rich end
  (it ended `res_b` 20 px short of its last turn). Ends are looked at by eye.
- `tools/xfield.py`: contact colours over a crossing field. Not usable where there are no
  pads (the colour drifts by the row); kept for fields with pads.

**What went wrong and what I changed**

- I followed the wrong net for 2,500 px (the eastern half of bus line y 14526) because a
  1.9x strip showed one continuous line; it is two pads 90 px apart. Caught when the
  metal shot at 5x showed the pads' metals going different ways.
- I nearly reported "e4 is RES" on the strength of a 217 px overlap and a tool's end
  point. Traps 13-15 in the tracing guide are from this.

**Assessment**

Chasing one signal from its loads does not find its driver in this part of the die: the
nets are long, cross three bus fields and have no landmarks. Two days of serial work have
given the step formula and five well-drawn but unnamed inputs. Naming them needs the
regions they come from traced as wholes: the top-left clusters (where the scan line
counter probably is), bc1/bc2 and the gate column of bd1. That is the same conclusion as
on 2026-11-16, now with tools that make the bus fields cheap.

**Open, in the order I would take them**

1. Finish the `tla` cluster as a block (about twenty gates), using the unit structure and
   `follow.py` for its bus pieces; then the cluster's twin columns at x 3450-3900 and
   x 4650-5050.
2. bd1's gate column (re-read R1): it holds what the R0 match feeds and what makes X.
3. The poly bus's other four lines east of the pads, and the diagonal fan.

## 2026-11-17 Signal names

The user asked whether signals were being renamed as they were understood (they were
not: only joined by alias), and then: "one of the aims here should be to ensure that all
labels are meaningful, or at very least are described in a table if it's hard to name
them. Make sure that all the documents reference the correct names."

Done, at the source:

- 672 net names renamed in the trace files (labels, templates, tags, aliases): counter
  bits (`hc0`-`hc7`, `rc0`-`rc6`, `hsw0`-`hsw3` and their nodes), registers and comparators
  by register number and bit (`r1_b3_q`, `r0c_b5_x`), match lines (`h_eq_r0`...), write
  strobes (`wr_r6`), the row counter's clocks and step (`rc_ck_m`, `rc_step`,
  `rc_stepreq_n`), the inhibit signal and its copies (`inh_n`, `inh_ck`, `inh_rc`,
  `inh_lat`), bus control (`wr_data_sel`...). Extraction unchanged: 1,683 nets, 2,789
  transistors, 0 errors, 0 warnings.
- The same table applied to every note, the plan, the instructions and the floor-plan
  descriptions (771 replacements). **This journal was rewritten too**: entries above use
  the new names. The old names are in "Former names" at the end of `notes/signals.md`.
- `notes/signals.md`: the glossary. Every one of the 1,526 named nets is covered by a row
  (name or pattern) saying what it is or, for a placeholder, what is known. `tools/build.py`
  checks it and reports names it does not cover (now 0).
- Convention `NAME_u` for a wire believed to be NAME whose join is not drawn. The rename
  exposed 14 such open joins that had been hidden behind unrelated-looking names; they
  are listed in `notes/work-packages.md`.
- Overlays and the SVG now show the canonical name of a net at every label.
- `tools/rename.py OLD NEW` for every later identification; `tools/signals.py` for the
  check on one block.

Not renamed: the central datapath rows, the left array and the two small logic blocks,
whose registers have no numbers yet. Their names stay by place and are described in the
glossary.

## 2026-11-17 (unsupervised) Floor plan, names, and the step logic two more levels deep

Serial, no agents (user: "while unsupervised, just work serially"). The user asked for the
floor-plan labels to be tidied, for tracing to continue, and "let's see if later on new
discoveries reveal the nature of e4". Full extraction at the end: see the ship line
(2,810 transistors at the last build, 0 errors, 0 warnings).

**Housekeeping done**

- Floor plan: labels are placed inside their own block clear of smaller blocks and of each
  other; blocks too small for a name get a number and a legend panel; names made consistent;
  superseded coarse blocks dropped; `out/floorplan_legend.txt` lists every block as text.
- Signal names: see the entry above ("Signal names"). The glossary check is part of the
  build and stays at zero uncovered names.
- Two open joins closed by drawing them: `h_eq_r0` and `h_eq_r1` between the right
  datapath and the strobe channel. `h_eq_r1` and `inh_lat` followed on, through the bottom
  bus field, to poly lines entering the bottom-centre logic at (10940,17598).

**The step logic (block `tla`)**

- Corrected formula: **step = in1 OR (NOT e4 AND NOT (e3 AND a2))**. `b1` has a third
  pull-down that the first pass missed (a strap from an inverter of NOR(e3,e4) to a gate
  hidden under a thin metal), which removes `x1` from the step.
- `in1` = NOR(`rcs_mu`, `rcs_mv`) is made in the middle cluster (x 3450-4110), a twin of the
  first; `rcs_mu` is an inverter there.
- The step condition does not only go to the step gate. `rcs_cond` = NOT e4 AND NOT(e3 AND
  a2) is sampled by a pass transistor into a dynamic latch (`rcs_cond_lat`) and gated into
  an AND-OR-INVERT (`rcs_n4200`) by a strobe, `clk_tl` (one junction of this is
  AMB-009).
- That strobe was followed to its far end: 4,500 px, out of the cluster's foot and south
  down x 2457 to the **left column beside upper row 2 of the left array** (`larr`).
- So the vertical logic is: three gate clusters at x 2450-5050, y 2950-5450, plus the nine
  upper rows of the left array and their left column. About 34 of perhaps 75 gates of the
  clusters are not traced; the upper rows are not traced at all.

**e4**: still not identified. Nothing found today names it. Its driver is not in the
first cluster; every contact on its 17,000 px is a gate.

**Method notes**

- Where no metal lies over a structure, read it in the **chip-2 shots at 6-7x**: poly bands
  are crisp, and a diffusion edge shows as a dark line running across the bands. The clean
  shot is poor there (it is the shot for what was under metal).
- A poly that ends inside a diffusion without crossing it, inside a ring, is a buried
  contact; one that crosses with the diffusion's edge lines visible through it is a gate.
  Class runs down the diffusion (`classmap.classify` on a 7 px column) tell the two apart
  where a thin metal hides them.
- Check a newly extracted gate for sense. `rcs_cond` first came out as NOR(strobe, m2)
  feeding a gate with the term (strobe AND that NOR), which can never be true: that is
  what exposed the pass transistor reading.
- `tools/follow.py` now stops when it returns to a corner it has turned (it was started on
  a wide rail and looped).

**Open, in the order I would take them**

1. The left column beside the upper rows of the left array (x 2480-2860, y 6700-10900) and
   those nine rows: where `clk_tl` comes from. With them the scan-line side of the
   vertical logic should become nameable, and through it e3, a2 and e4.
2. The remaining units of the three clusters, unit by unit (first cluster: y 3690-3800,
   4320-4535, 4830-5330 east; the whole west column above y 4940).
3. The gate column of the strobe channel (y 15860-16125), where `h_eq_r0` is sampled on
   `ck_out`: observations are in `notes/blocks/bd1.md`.
4. The bottom-centre logic, which receives `h_eq_r1`, `inh_lat` and e4.

**Addendum, same session: the strobe has a driver.** The strobe (former name `rcs_bb3807`) is now `clk_tl`:
it is the output of an inverter at (2626,7908) in the left column beside upper row 2 of
the left array (traced, extracted: `clk_tl` = NOT `ck_out`). The left column there is
the downward continuation of the first cluster's west side (same VSS and VCC rails, same
"rail gate" inverter as `rcs_w2`). Its input `ck_out` comes down a metal at x 2370 from
a contact (2365,5847) at the foot of the first cluster and carries on south at x 2500.
A signal that is made in one place, run 2,000 px, inverted locally and run 2,200 px back
is being distributed like a clock; which signal it is, is the next thing to find, in the
small cluster at y 5650-6300.

**Second addendum: the strobe is the clock.** Following the inverter's input (not its
output) with `tools/follow.py` gave the answer in one call: the metal that leaves the
inverter's pad southwards runs 17,238 px down the left edge and along the bottom to the
clock block. It is the left-edge trunk of `ck_out`, which trunks had drawn only to
y 18300. So the inverter's input (former name `rcs_stb_n`) **is `ck_out`** and the strobe is `clk_tl` = NOT `ck_out` (CLK
polarity). Joined by geometry (the missing 10,300 px of trunk are drawn; the extraction
merged the two nets with no warning) and renamed everywhere.

What that settles: the step condition `rcs_cond` is latched while CLK is high. What it
does not settle: e3, e4, a2 and in1 are still unnamed.

Lesson: when a net has only gate loads, follow the *input* of whatever drives it before
giving up, and try the follower from the far end of any long line a trace left unfinished:
`ck_out`'s trunk "followed at 1x to y 18300" was 10,000 px short of its end.

## 2026-11-17 (continued) Two more counters, their clock generator, and the upper right datapath

Serial. New blocks `ur`, `urch`, `rdp1`, `slbus`. Full extraction 2,014 nets, 3,364
transistors, 0 errors, 0 warnings. User: "let's continue".

**What was established**

- **The nine upper rows of the left array are counter bits**: nine copies of the mid-right
  array's bit cell (`tools/findcell.py`, scores 0.88-0.92). A 4-bit counter (rows u0-u3)
  and a 5-bit one (u4-u8), plain ripple chains, sharing one master and one slave clock.
- **Their clock generator is a second copy of the row counter's**, in the left column
  beside rows u0-u2 (found the same way; the generator is now a shared cell). Both
  counters step once per pulse of `lc_step`, which comes from the left-centre logic.
- **The 5-bit counter is the scan line counter** (`sl0`-`sl4`). Its five output lines were
  followed and drawn 9,000 px east, through the central datapath's channel 2 (unused
  there), to the comparator of R5 in the upper right datapath.
- **The upper right datapath's top rows** (`rdp1`) are built from the cells of the rows
  below: R6's comparator, R7 and its comparator, and a top row holding **R5** (5 bits) and
  **one nibble of R3** (4 bits), each with a comparator. 284 transistors by instancing.
  Strobes `wr_r7`, `wr_r5`, `wr_r3` followed in; `uc_eq_r6` joined to the strobe
  channel's track k4.
- **The mid-right 4-bit counter is the horizontal sync width counter** (`hsw0`-`hsw3`):
  its four outputs end under the counter tracks of R3's comparator.
- **Bit order of the upper right array**: slices left to right are bits 0-6. Names of R4,
  R6, R7, R5, their comparators and the lines `ubus`, `uc` now carry bit numbers.

So the registers found so far: R0, R1, R2 (lower right), R4, R6, R7, R5, R3-nibble (upper
right), all with equality comparators. Still to find: R9 and the cursor and start-address
registers (central datapath), R3's other nibble, R8.

**Mistakes caught**

- Instancing the clock generator put its input contact on the neighbouring metal
  (`clk_tl`); the first extraction said "the scan line counter is clocked by CLK". The
  overlay showed the real pad one track to the west. Per-copy differences of an instanced
  cell must be looked for at every port, on the overlay, before the extraction is read.
- The last comparator slice of a group came out as "x = NOT nor": its series pair ends on
  a VSS land of the next slice's rail, absent at a group's right end.
- A straight "c track" profile showed a gap in every latch row; it is a jog of the track,
  the same in every row, not a break.

**Method**

- **`findcell.py` first.** Three blocks today (252 + 16 + 284 transistors) came from
  cells already traced. Before tracing any regular-looking region by hand, try every known
  cell against it, in all orientations.
- `tools/rowstrips.py`: the same strip for every row of an array in one image.
- Poly lines that change line position in a knot: check the result against an independent
  expectation (here: bits must come out in order across the slices).

**Open, in the order I would take them**

1. Where `lc_step` is made (left-centre logic, at about (5030,7000-7150)): the scan line
   counter's step. And the scan line counter's other comparators (R9 at least): its lines
   pass channel 2 unused, so R9's comparator takes them elsewhere, or they are tapped
   further west (the pads at x 4925-6196, and the vertical poly bus they cross).
2. `rdp2`'s routing zone (y 9080-9560): joins the row counter to the `uc` lines, closing
   `uc_eq_r4/r6/r7` against `rc`.
3. Where the match lines go: `sl_eq_r5` (north), `hsw_eq_r3`, `uc_eq_r7` (west),
   `uc_eq_r6` and `h_eq_r0` (strobe channel gate column), `h_eq_r1` (bottom-centre).
4. The rest of the step-logic clusters; the 4-bit left counter's outputs; `e4`.

## 2026-11-18: the row address selector; `inh_src` is a bus line

Questions from the user: is the scan line counter put out directly as RA0-4; how do the
R5 and R9 compares work; what makes VSYNC width 0 special. And two sets of questions on
jsbeeb issue 1866 (write strobe and E, R8 skew path, compare phase, shortest CLK pulse,
what `inh` does).

**Found**

- **The scan line counter does not go straight to the pins.** Its five lines are tapped
  at x 7120-7337 and feed a column of eleven pass transistors (`trace/ras.txt`,
  `notes/blocks/ras.md`): one gate line passes `sl` k to output k, the other passes `sl`
  k to output k+1, and output 0 has two more gated sources. A shift by one bit with a
  separate bit 0: the shape of interlace sync and video. 3,375 transistors, 2,025 nets,
  no errors.
- `inh_src` followed 3,700 px west from the strobe channel and drawn: a bottom-bus line
  with four branches, three still open (`notes/blocks/trunks.md`). Not made locally.
- RA0's and RA1's pad driver inputs followed from the pads to x 15300, y 4140-4800,
  where they meet metals from the west (not drawn; `notes/blocks/trunks.md`).

**Not found**

- The selector's outputs are not joined to the pads (gap: x 7860 to 11650 along
  y 4450-4800) nor to the central datapath's channel 1, towards which a nest of metals
  east of the column turns. If channel 1's lines are the selector's outputs, R9, R10 and
  R11 are compared with what goes to the pins, not with the counter. Open.
- R9's comparator: still not identified. Candidates are the central datapath's rows A
  (five latches) and B (5-bit comparator on the through tracks).
- R3's high nibble and the 4-bit counter `c4l`: nothing new.

**Method**

- A structure with no supply rail over it is worth a second look before assuming gates:
  this column is pass transistors only.
- The strip pattern was plain in the chip-2 stripped shot at 2.5x and unreadable in the
  clean shot at 4.4x (narrow diffusion fingers between two edge lines print black
  there). Try the other stripped shot before zooming further.

**Open, in the order I would take them**

1. The selector's five outputs to their ends, and the nest of metals at x 7530-7715 into
   channel 1; then the two gate lines and bit 0's extra sources (interlace logic).
2. Where `lc_step` is made; where `sl_eq_r5` goes.
3. `inh_src`'s three open ends.
4. As before: `rdp2`'s routing zone; the other match lines; the step-logic clusters;
   `c4l`'s outputs and R3's high nibble; `e4`.

**Later the same day.** All five selector outputs leave east as poly lines (y 4765, 4893,
5133, 5262, 5392) into a column at x 7860-8100 that is not traced. `ras_o3` also runs,
through the nest of metals east of the selector, onto a line of the central datapath's
channel 1; with the five channel lines drawn to `cdp2`'s, the extraction makes
`cdp2_trk_s7` and `ras_o3` one net. So the central datapath's 5-bit comparator (rows B,
against row C's register) sees the selector's output on at least that bit. Lesson for
the method: a named net of one block turning out to be a named net of another is
reported by the extraction as "carries several names"; that message is the join being
confirmed, and the fix is one name (`tools/rename.py`, or `@alias` where the name comes
from a cell template).

## 2026-11-19: correction: `cdp2_trk_s7` is not `ras_o3`

Yesterday's last commit joined `ras_o3`'s pad (7577,5262) to a metal that only passes it
(trap 16, R11). Corrected in the trace and in `notes/blocks/ras.md`. What stands:

- No selector output goes anywhere but into its own unit of a column of five identical
  units at x 7860-8100 (`rax`, not traced).
- Each unit has a second pad; the five lines from those pads are now all drawn and the
  extraction joins them to `cdp2`'s comparator tracks, bit 0 on slice s7 up to bit 4 on
  s3. That order is the one `cdp2`'s magnitude chain needs.

What made me look again: the result did not fit (output 3 on the slice that should be
bit 0), and the unit's second pad looked like an output. A result that breaks a regular
pattern is a reason to re-test the join that produced it before writing it up.

**Same day, later: the row address lines to the RA logic.** The five lines that feed the
central datapath's comparator (`rax_o0`-`rax_o4`) do not stop there: each goes on east of
the comparator, north 1,500 px, under a supply metal, east 2,000 px along the top of the
right-hand arrays and into a band of logic at x 13990-15500, y 4300-4520, out of which
the RA pad drivers' inputs come (`trace/rab.txt`, `notes/blocks/rab.md`). So the path of
a row address bit is: scan line counter, selector (`ras`), unit (`rax`), then both the
cursor-style comparator and, through one more band of logic (`ral`), the pin. Two blocks
on that path are untraced (`rax`, `ral`).

Mistakes of earlier blocks found on the way and corrected: `cdp2`'s line 6000 does not
end at x 10518. Method note: `tools/follow.py --gap 50` bridges real gaps (it joined a
pad at (7900,4372) to a rail 40 px away); keep the default 24 and look at every reported
corner near a rail.

**Same day: the units and the stage in front of the pads.** `rax`: the pull-down of each
unit drawn (five transistors); taken to be inverters (AMB-011), load not traced. `ral`:
the band in front of the RA pad drivers is five copies of one cell, and
`tools/findcell.py` finds the same cell fourteen times in the left array's untraced left
column, in front of the MA drivers. Ports read, cell not traced; it looks like the
register rows' static latch on a strobe line (`notes/blocks/ral.md`). `bd2`: looked for
where `wr_data_e_n` goes (the write-strobe question of jsbeeb issue 1866): it leaves on a
strap between two poly pads, destination not read.

**Open, in the order I would take them**

1. The `ral` cell (twenty copies: RA and MA outputs), then its strobe and force lines to
   their sources.
2. `bd2`'s gate group east of the rail: `wr_data_e_n`'s destination.
3. `rax`: the load and the east half of the unit.
4. The selector's two gate lines and bit 0's extra sources (interlace logic).
5. As before: `lc_step`; `sl_eq_r5`; `inh_src`'s three ends; `rdp2`'s routing zone; R3's
   high nibble and `c4l`; `e4`.

## 2026-11-20: R8, R9, R10, R11 identified by their write strobes

The user doubted that the 7-bit row with the comparator is R10. Settled by tracing
instead of by elimination: the four strobe tracks T3-T6 followed 11,000-14,000 px each
to the central datapath (`trace/wrs.txt`, `notes/blocks/wrs.md`). The extraction joins
`wr_r8` to `cdp1` row A (6 bits), `wr_r9` to `cdp1` row C (5), `wr_r11` to `cdp2` row A
(5), `wr_r10` to `cdp2` row C (7). 2,021 nets, 3,380 transistors, no errors.

So the 7-bit row is R10 (five raster bits and two cursor mode bits), and **R9's
comparator is found**: `cdp1`'s row B, traced weeks ago without a name. One of its five
bits does not take the register bit but the output of the island `tc1`, switched by
`ras_shift`: the place where interlace changes the R9 compare. Its compare value comes from
the RA pad drivers' input lines (followed, not drawn), not from the lines R10 uses.

**Method**

- An identification "by elimination" is a guess. Where a register row's strobe can be
  followed to a decoder line, do that first: here it took four follower runs.
- `tools/follow.py` does not report diagonals (tracing guide, tools).

**Open, in the order I would take them**

1. R9's five compare-value lines to their sources; `ras_shift`, `tc1_g`, `ras_o0_alt1`.
2. The `ral` cell (twenty copies) and its strobe.
3. `bd2`: `wr_data_e_n`'s destination.
4. The selector's gate lines; `rax`'s load; then as before.

**Same day: what R9 is compared with.** The five compare-value lines of R9's comparator
drawn end to end (`trace/r9c.txt`): they are the outputs of five units near the right
edge, below the RA4 pad driver, whose gates are the pad drivers' input lines. The
extraction joins each to one comparator input (bit 0 at slice 5 ... bit 4 at slice 1)
and, for RA0 and RA1, the unit's gate to the pad cell's own input net. So R9 is compared
with the row address at the pins, one stage later than R10. 2,024 nets, 3,385
transistors, no errors; three new open joins (RA2-RA4's lines to the pad cells).

Method: the same five-line bundle had been taken for "data bus interface" in the floor
plan because it ends beside the data pads' column. A coarse floor-plan label that
nobody traced is not evidence of anything.

**Open, in the order I would take them**

1. `ras_shift`, `tc1_g`, `ras_o0_alt1`: the three inputs that switch bit 0 of the R9 compare.
2. The `ral` cell (twenty copies) and its strobe: it sits between R10's and R9's view of
   the row address.
3. `bd2`: `wr_data_e_n`'s destination. Then the selector's gate lines, the loads of `rax`
   and of the R9 units, RA2-RA4's lines.

**Same day: the selector's controls are the island's outputs.** The five polys that leave
the nine-gate island `tc1` southwards are the selector's two gate lines, the gates of bit
0's two extra pass transistors and one of bit 0's alternative sources (`trace/ras.txt`,
last section; five joins in the extraction, 2,019 nets). The island's letters got the
selector's names. Result: `ras_straight` = NOT `ras_shift`; in shift mode R9's bit 0
selects which of two signals is put on row address bit 0 (`ras_o0_sel1` = shift AND bit,
`ras_o0_sel2` = shift AND NOT bit), and the R9 comparator's bit 0 is switched to the
inverse of the same signal. `notes/blocks/ras.md`.

Mistake found on the way: `ras_o0_sel1`'s metal had been drawn along a bus line the
follower jumped to (24 px gap). Tracing guide and R11 extended.

**Open, in the order I would take them**

1. The driver of `ras_shift`, and `ras_o0_alt1`, `ras_o0_alt2`, `tc1_g` to their sources:
   the interlace mode and the field signal.
2. The `ral` cell (twenty copies) and its strobe; the loads of `rax` and of the R9 units
   (they fix the polarity of the bit-0 compare).
3. `bd2`: `wr_data_e_n`'s destination.

**Same day: the mode line is the AND of two bits of R8.** `trace/shm.txt`: a NAND and an
inverter in the slice-0 position below R8's row; their inputs are the outputs of R8's
bits in columns c6 and c7, which reach the island's metals ns5 and ns6 along two of five
lines above the row (two poly cross-unders each). 2,019 nets, 3,390 transistors. The
chain is now extracted end to end: R8's two bits, the mode line, the selector's shift,
the choice of bit 0's source by R9's bit 0, and the switch of the R9 comparator's bit 0.

**Open, in the order I would take them**

1. `ras_o0_alt1`, `ras_o0_alt2`, `tc1_g`: the two signals that can become row address
   bit 0 (the field), followed only to pads at (7078,5303)'s metal, (6922,4787) and
   (6985,4958).
2. Where `cdp1_b_eq` (R9's match) goes: leaves west along y 4459.
3. The `ral` cell and its strobe; the loads of `rax` and of the R9 units.
4. `bd2`: `wr_data_e_n`'s destination.

