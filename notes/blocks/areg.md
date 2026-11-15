# areg: address lines into the decode array, and the logic right of the array

> **Correction (coordinator, 2026-11-15).** The load strobe `areg_load` is not simply
> NOT `e_b`. The bd2 block traced its driver: `areg_load = NOT bd2_al_n`, with
> `bd2_al_n = NOT(bd2_x OR (e_b AND bd2_m210))` and `bd2_m210 = NOR(rw_d, rs_d, cs_d)`
> (see `notes/blocks/bd2.md`). The same block found this file's reading of the poly
> from (16252,14862) wrong: it ends on a buried contact.

Region x 15800-16950, y 12900-14700. Trace: `trace/areg.txt` (`@requires decode`).
Extracts with 0 errors, 0 warnings, no unnamed open nets.

## Status

- **The five cells at x 15930-16200 are not the address register. They are plain
  inverters**: upper row of each decode pair in, lower row out. Traced, placed five
  times, each instance checked, joined to the decode rows.
- **The address register is the row of five cells above the decode array**
  (x 14180-16150, y 13000-13290, one every 390 px, the datapath pitch). Four are in
  rdp3's area. The fifth (x 15745-16150) is in this region and is **partly** traced: its
  write path, its output inverter and its output line are in the trace; the first
  inverter's load and two internal links are described below but not drawn.
- The load strobe (`areg_load`) is traced from the register cells to where it leaves the
  region: metal at x 16299, y 14700, going down. Followed by eye below the region: it is
  the output of a gate at about x 15880-16150, y 15230-15330 (bd2's area), see Logic.
- Vertical bundle x 16200-16450: traced as labelled wires with ports.
- Right-hand column of cells (x 16480-16800) and everything right of x 16460: not started.

## Inventory

| What | Where | State |
|---|---|---|
| Row inverters `areg_inv` x 5 | 15930-16200 x 13730-14570, pitch 173 | traced, extracted, all five checked |
| Feeds of the upper rows | metal from x 15800 at y 13350/13391/13433/13480, poly L shapes | traced |
| VSS rail | enters at (16122,12900), diagonals, x 15925-15975 over the inverters, ends y 14625 | traced |
| VCC rail of the inverters | enters at (16282,12900), x 16142-16194, leaves at y 14700 | traced |
| VCC rail of the register row | x 15925-15975 from y 12900 to 13578, then the wide rail x 15795-15890 down to y 14700; joins the decode array's VCC bus | traced |
| Fifth register cell | 15745-16150 x 13000-13290 | partial (see Logic) |
| Bundle: `areg_load`, `areg_w6`, `areg_w7`, `areg_rail_r` | x 16291-16451 | traced as wires |
| Right-hand column | x 16480-16800 | not traced |

## Logic

### Row inverter (traced)

One per row pair, identical (cellcheck: 95-96 % median correlation, differences only where
the feed joins).

- The pair's ground diffusion rail from the decode array (y 13782-13832 for pair 0) runs on
  to the right, takes a contact from the VSS rail at (15950,13805), and is the source of
  the pull-down.
- Upper row poly: arrives from the array at y 13753-13777, steps up under the VSS rail to a
  band at y 13731-13751, crosses the cell and ends in a tab under the VCC rail
  (16150-16182 x 13731-13773). A bar hangs from the band at x 15993-16018 down to y 13843:
  the pull-down gate (W/L 71/25).
- Output node: diffusion x 16018-16087, y 13790-13832.
- Load: poly block 16087-16130 x 13768-13865 over the diffusion strip (W/L 42/43), far end
  of the strip contacted to the VCC rail at (16165,13805). The block is part of the lower
  row poly, which is tied to the output node by a buried contact at
  16038-16068 x 13803-13843 (the "intricate shape": concentric arches in the clean shot).
- Lower row poly: block, bottom band y 13860-13882, steps up under the VSS rail to the
  array's lower row at y 13838-13864.

Traced: `ar<k>_n = NOT ar<k>`, k = 0..4. `ar<k>` is the **upper** row of pair k and is the
wire that arrives from the register; `ar<k>_n`, the lower row, is generated here.

### Feeds of the upper rows (traced)

| Pair | Enters | Route |
|---|---|---|
| 0 | metal, x 15800, y 13480 | contact 15887,13480; poly right to x 15975, down under the VSS metal into the cell's left pad at y 13731 |
| 1 | metal, x 15800, y 13433 | contact 15840,13433; poly right to x 16189, down, jog right at y 13565 to x 16210, down to cell 1's tab at y 13936 |
| 2 | metal, x 15800, y 13391 | contact 15885,13392; poly right to x 16231, down to contact 16232,13522; metal x 16232 down to contact 16232,14107 on a poly pad joined to cell 2's tab |
| 3 | metal, x 15800, y 13350 | contact 15840,13350; poly right to x 16280, down to y 14286, left into cell 3's tab |
| 4 | poly, from the fifth register cell at 16066,13280 | right along y 13309 to x 16320, down to y 14459, left (under `areg_load`) into cell 4's tab |

No gate anywhere on these routes: each upper row is the register cell's output node itself.
The four metal lines collect, in a wide view, one line from each of the four register
cells left of x 15800 (each cell's output poly goes down to a contact at about y 13308,
seen on cell 4 at 15668,13308). Which cell drives which line is in rdp3's area; the
natural guess (leftmost cell = pair 0) is not traced.

### Fifth register cell (partly traced)

Five copies, found by correlation at dx 0, -390, -781, -1171, -1562 (scores 0.83-0.93).
A 5-instance median picture is `cache/comp/areg_bit_*` (`--comp areg_bit`, master frame =
this cell, 15740,12980:16150,13300); rebuild with
`tools/t.sh areg composite.py areg_bit 15740,12980:16150,13300 --offsets "0,0 -390,0 -781,0 -1171,1 -1562,0"`.

Traced (in the trace file, extracted):

- **Strobe poly.** One poly line snakes through all five cells: a band along the top of
  the cell (y 13015-13033), at its left end a strip down (x 15852-15872) to a band at
  y 13061-13081 that crosses the write strip. In this cell the top band runs on right to
  a contact at (16297,13022) and from there in metal down the bundle (`areg_load`). To the
  left the band at y 13061-13081 meets a leg (x 15745-15766, y 13015-13085) that is the
  right end of cell 4's top band.
- **Write path.** Thin vertical metal at x 15787-15807 comes from above the region and
  ends at y 13275 (`areg_din4`). Contact at (15797,13037) to a diffusion strip
  (x 15778-15848). The strobe band crosses the strip: pass transistor, W/L 70/20. Below
  the band the strip ends in a buried contact (15818-15850 x 13088-13106) to a poly
  (`areg_s4`, the storage node) that runs down under the data line and is the gate of a
  pull-down at 15781-15801 x 13150-13200 (W/L 50/20).
  Extracted: `areg_s4 <- areg_din4` through the pass transistor when `areg_load` is high.
- **First inverter (pull-down only).** Source side runs left under the next cell's VSS
  rail to its contact at (15728,13165) (outside this region, labelled `areg_c5_src`);
  drain side is `areg_s4_n`.
- **Output inverter.** VCC land 15885-15962 x 13050-13099 (contact 15930,13069 to the VCC
  rail), strip to the right under the load gate (15966-16022 x 13062-13100, W/L 25/56),
  turning down into the output node (16026-16070 x 13100-13150). Pull-down gate
  16071-16090 x 13092-13182 (W/L 50/19), source contacted to the VSS rail at (16118,13152).
  The load gate continues down as a pad (to y 13145) and right onto the output node
  through a buried contact (16030-16052 x 13112-13148). Extracted: `ar4 = NOT areg_g1`.
- **Output route.** Contact on the pad (15995,13127), metal strap (x 15988-16028) down to a
  contact at (16008,13215) on a diffusion that extends right to x 16076; the output poly
  (x 16055-16075) starts on that extension and goes down to become the `ar4` feed.
- `areg_g1`, the output pull-down's gate, is the end of a poly band (y 13160-13182) that
  comes from a vertical piece at x 15919-15944 under the VCC rail.

Seen but not drawn (believed):

- The first inverter's load: a poly block under strap M2 at 15885-15904 x 13105-13157 over
  a strip coming down from the VCC land.
- `areg_s4_n` reaches `areg_g1`: the drain of the first pull-down seems to run right along
  y 13160-13187 under M2 to a heavy edge at x 15905-15912 (a buried contact onto the
  vertical piece of `areg_g1`). There is also a poly blob with a buried-contact box at
  15828-15866 x 13127-13172 that belongs to this node.
- Static feedback: something runs right from the foot of the storage poly (15783-15815 x
  13203-13228) along y 13205-13245 (poly pieces in the open at x 15815-15848, 15855-15873,
  15900-15920; two bands under the VCC rail, y 13207-13218 and y 13225-13245) to the left
  edge of the diffusion under the strap's lower contact (x 15985). If that is a
  connection, the storage node and the output node are the same net and the cell is a
  cross-coupled ("jam") latch that the data line overpowers while the strobe is high.
- A horizontal poly band at y 13250-13268, x 15748-15985, along the bottom of the cell.
- Two metal straps that run from the top band to the bottom of the cell with no contact
  found: M2 (x 15877-15897, y 13015-13275) and M5 (x 16050-16068, y 13015-13272), named
  `areg_m2`, `areg_m5`. The clean shot shows no contact mark on the top band under either.

What the cell is, as far as established:

- Kind of latch: a level-sensitive latch written through a single pass transistor.
  Transparent while `areg_load` is high. The address register must hold indefinitely, so
  it has to be static; two inverters are present, which fits a cross-coupled pair, but
  the closing link is not traced.
- Data input: the thin vertical metal at x 15797, entering the region at y 12900 from
  the datapath above (a data bus bit line by its position; which bit is not established).
- Load strobe: `areg_load` (see Ports). No clock is involved in the cell.

### Is the upper row of each pair the true address bit?

- Traced: the upper row is the register cell's output node (no gate in between), the
  lower row is its inverse. So decode.md's naming (upper = `ar<k>`, lower = `ar<k>_n`) is
  right in the sense "upper = what the register puts out".
- Traced: the output node is the output of an inverter whose input is `areg_g1`, and the
  storage node (same sense as the data line) drives a first inverter.
- Not traced: that `areg_g1` is the first inverter's output. If it is (believed), the
  register output has the **same sense as the data line**, and the upper row is the true
  address bit provided the data line carries the data bit uninverted.
- So: **confirmed that the upper row is the register's direct output; "upper = true bit"
  is supported (two inversions between storage node and output, as far as seen) but
  rests on one link that is believed, not traced, and on the polarity of the data line.**
  Nothing found contradicts decode.md.

### Where the load strobe comes from (seen below the region, not traced: bd2's area)

Followed `areg_load` past the boundary at 1-3x, without tracing:

- Metal x 16291-16307 goes down from y 14700 to a contact at (16298,14822), ducks under a
  horizontal metal band (y 14905-14960, a branch of `areg_rail_r`) in poly, and comes back
  to metal at a contact at (16298,15000).
- That metal runs down to y 15265, turns left and **ends** at a contact at (16255,15258).
  Nothing continues down at x 16299 below y 15270.
- From the contact a poly runs left along y 15245-15268 to a buried contact at about
  16105-16130 x 15250-15275 on a diffusion strip (y 15258-15288) that runs on to the left
  under a wide vertical rail (x 16005-16050) to beyond x 15985.
- Directly below that strip a long poly band (y 15290-15312, x 15990-16195) with
  diffusion on its far side (y 15315-15350, contacted to the wide rail at about
  16035,15335): a pull-down on the strobe node. The band comes from a contact at
  (16210,15300) whose metal goes down at x 16200-16220.
- So **`areg_load` is the output node of a gate at about x 15880-16150, y 15230-15330**,
  not a pin signal wired straight through. The rest of that gate (its load and other
  pull-downs, to the left of x 15985) was not looked at.
- Warning for whoever joins the ports: `notes/blocks/trunks.md` has `rw_d` on a metal at
  x 16290-16308 from y 17558 up to "above 15900, not followed", and `rs_d` at
  x 16333-16352. These are in line with `areg_load` (x 16299) and `areg_w6` (x 16341) but
  **`areg_load` is not that metal continued**: its metal ends at (16255,15258). `areg_w6`
  likewise leaves metal at a contact at (16337,14862) and continues as a poly that runs
  down x 16340 to y 15255 and then diagonally down-right to about (16490,15390). Whether
  either trunk line reaches these by another route is open.
- Also seen: a third contact at (16252,14862) beside the two cross-unders takes a
  horizontal metal from the left (y 14855-14875) into a poly going down x 16247-16265 to
  a contact at (16255,15085); from there a metal goes down to y 15213, left to x 16170 and
  down at x 16160-16180 (trunks has `e_b` on a metal at x 16160-16180 further down).

## Ports

| Name | Layer | Crosses at | Direction | What |
|---|---|---|---|---|
| `ar0` | metal | x 15800, y 13480 | from outside (left) | output of a register cell, for row pair 0 |
| `ar1` | metal | x 15800, y 13433 | from outside | same, pair 1 |
| `ar2` | metal | x 15800, y 13391 | from outside | same, pair 2 |
| `ar3` | metal | x 15800, y 13350 | from outside | same, pair 3 |
| `ar0`..`ar4`, `ar0_n`..`ar4_n` | poly | x 15800, the ten decode rows | upper rows pass through to the array, lower rows driven here | joined to `trace/decode.txt` by overlap |
| decode ground rails | diffusion | x 15775, y 13782-13832 and every 173 below | - | also contacted to VSS here |
| `areg_load` | metal | x 16299, y 14700 | from outside (below) | load strobe of the address register; no tap in this region other than the register |
| `areg_load` | poly | x 15800, y 13061-13081 | passes on to the left | the same strobe continuing to the other four register cells |
| `areg_din4` | metal | x 15797, y 12900 | from outside (above) | data line of the fifth register cell |
| `areg_c5_src` | diffusion | x 15745, y 13150-13200 | - | source of the first pull-down; joins cell 4's VSS rail contact at (15728,13165) |
| `areg_w6` | metal | x 16341, y 14700 | unknown | up the bundle to contact 16337,13264, then poly right along y 13263; drawn to x 16480, goes on to the right-hand column |
| `areg_w7` | poly | x 16364, y 14700 | unknown | up the bundle to y 13453, then right; drawn to x 16480, goes on to the right-hand column |
| `areg_rail_r` | metal | x 16426, y 12900 and y 14700 | supply? | 49 px wide rail through the whole region; which supply is not established |
| `vss` | metal | x 16122, y 12900 | supply | VSS rail entering from above |
| `vcc` | metal | x 16282, y 12900 and x 16168, y 14700 | supply | VCC rail of the inverters |
| `vcc` | metal | x 15950, y 12900 and x 15795-15890, y 14700 | supply | VCC rail of the register row / wide rail; also joins the decode VCC bus at x 15775, y 13518-13632 |

No taps on `areg_load`, `areg_w6`, `areg_w7` between their ends: looked at in the clean and
metal shots over the full height.

## Ambiguities

1. Tab at the right end of each upper row (16150-16182 x 13731-13773 for pair 0), under the
   VCC rail. For pairs 1-4 it is where the feed joins; for pair 0 the feed joins at the
   left and the tab is a dead end. No contact seen on it in either metal shot or the clean
   shot (a contact would short `ar0` to VCC). Working assumption: no contact.
2. Register cell, join between the strobe band's left end (x 15772) and cell 4's leg
   (x 15745-15766): a dark line at x 15768-15775 lies between them, under the edge of
   cell 4's VSS rail. Read as the metal-margin artefact, i.e. one poly. Two separate polys
   6 px apart would break the design rules. Not drawn left of x 15772.
3. Register cell, output poly start (16050-16080 x 13222-13249): drawn as a buried contact
   to the diffusion extension. No contact mark there in the clean shot. Strap M5 passes
   over it, so a metal contact joining M5, diffusion and poly cannot be excluded from the
   metal shots alone; that would make `areg_m5` the output node as well.
4. Register cell, straps M2 and M5: both run exactly from the top band to the bottom of
   the cell, which suggests contacts at their ends, but none is visible. If M5 contacted
   the top band and the output poly the strobe would be shorted to the output, so at most
   one of those can be real. Needs the other four cells compared one by one.
5. Register cell, storage poly between the buried contact and y 13140 (marked `?`): the
   route (down the right edge of the data line, then widening under it) is read from heavy
   outlines only.
6. Which supply `areg_rail_r` is. The loads of the right-hand column cells will tell.
7. Under `areg_rail_r` a poly runs along its left edge (x 16402-16420) from y 13650 to
   y 14440, with an arm to the right at each end (y 13650-13665 and y 14422-14440). Seen
   in the clean shot, not drawn.

## Not done

- Fifth register cell: everything listed under "seen but not drawn". Best next step:
  trace the cell on the median picture at 6x in three strips (x 15800-15925 is the hard
  one), then check the result on each of the five instances; the cell differs between
  instances only below y 13270 (output contact at y 13308 in cells 1-4, none in cell 5).
- The gate that drives `areg_load` (about x 15880-16150, y 15230-15330, outside the
  region): trace it and its inputs. This is the question that matters most.
- Right-hand column, x 16480-16800: four identical cells at about y 13060-13250,
  13270-13450, 13470-13640, 13660-13840 (pitch about 190, each with a contact near
  x 16540), then larger, different cells from y 13900 to 14700. Wide vertical metals at
  x 16490-16540 and x 16650-16700, thin ones at x 16790-16830. Horizontal poly lines
  arrive from the bundle at y 13263 (`areg_w6`), y 13453 (`areg_w7`), y 13657 and y 14431
  (the two arms of the poly under `areg_rail_r`).
- Region right of x 16800 (a block at 16860-16950 x 13820-13930, lines to the right edge).
- The neighbouring items left of x 15800 that belong to this cell row are rdp3's.
