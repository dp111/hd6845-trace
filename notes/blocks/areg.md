# areg: address lines into the decode array, and the logic right of the array

Region x 15800-16950, y 12900-14700. Trace: `trace/areg.txt` (`@requires decode`).

## Status

- Traced and extracted: the five cells at x 15930-16200 (one per decode row pair) and the
  five lines that feed them.
- **The five cells are not the address register. They are plain inverters** that make the
  lower row of each pair from the upper row. The register itself is the row of five
  cells above the decode array (x 14180-16130, y 13000-13270, one every 390 px); four of
  them are in rdp3's area, the fifth (x 15760-16130) is in this region.
- In progress: the fifth register cell, the vertical bundle, the right-hand column.

## Inventory

| What | Where | State |
|---|---|---|
| Row inverters `areg_inv` x 5 | 15930-16200 x 13730-14570, pitch 173 | traced, extracted, checked on all five |
| Feed lines of the upper rows | metal from x 15800 at y 13350/13391/13433/13480, poly L shapes to the cells | traced |
| VSS rail over the inverters' left ends | x 15925-15975, y 13700-14625, comes down a diagonal from (16115,12900) | lower part traced |
| VCC rail over the inverters' right ends | x 16142-16194, comes down a diagonal from (16280,12900) | lower part traced |
| Fifth address register cell | 15760-16130 x 13000-13270 | not traced yet |
| Vertical bundle | x 16200-16450 | surveyed (list under Not done) |
| Right-hand column of cells | x 16480-16800 | not traced |

## Logic

### Row inverter (traced)

One per row pair, identical (cellcheck: 95-96 % median correlation, differences only where
the feed joins).

- The pair's ground diffusion rail from the decode array (y 13782-13832 for pair 0) runs on
  to the right, takes a contact from the VSS rail at (15950,13805), and continues as the
  source of the pull-down.
- Upper row poly: arrives from the array at y 13753-13777, steps up under the VSS rail to a
  band at y 13731-13751, runs across the cell and ends in a tab under the VCC rail
  (16150-16182 x 13731-13773). **There is no contact on the tab** (no ring in either metal
  shot, no mark in the clean shot; compare the real poly contact at 16232,14107). A bar
  hangs from the band at x 15993-16018 down to y 13843: the pull-down gate (W/L 71/25).
- Output node: diffusion x 16018-16087, y 13790-13832.
- Load: poly block 16087-16130 x 13768-13865 over the diffusion strip (W/L 42/43), other end
  of the strip contacted to the VCC rail at (16165,13805). The block is part of the lower
  row poly, which reaches the output node through a buried contact at
  16038-16068 x 13803-13843 (the "intricate shape": the concentric arches in the clean shot
  are the buried contact window).
- Lower row poly: block, bottom band y 13860-13882, then steps up under the VSS rail to the
  array's lower row at y 13838-13864.

So, traced: `ar<k>_n = NOT ar<k>` for k = 0..4, where `ar<k>` is the **upper** row of pair k
and `ar<k>_n` the lower. The upper row is the one that arrives from outside; the lower is
generated here.

### Is the upper row the true address bit?

Traced so far: the upper row of each pair is the wire that comes from the register (through
one metal-poly contact, no gate in between), and the lower row is its inverse. Whether the
wire from the register carries the latched data bit or its inverse depends on the register
cell: see "Fifth register cell" (to be filled in). decode.md's check 4 (only the upper-row-true
reading gives addresses 0-17) is independent evidence that it is the true bit.

### Feeds (traced)

| Pair | Enters | Route |
|---|---|---|
| 0 (`ar0`) | metal, x 15800, y 13480 | contact 15887,13480; poly right to x 15975, down under the VSS metal to the cell's left pad at y 13731 |
| 1 (`ar1`) | metal, x 15800, y 13433 | contact 15840,13433; poly right to x 16189, down, jog right at y 13565 to x 16210, down to cell 1's tab at y 13936 |
| 2 (`ar2`) | metal, x 15800, y 13391 | contact 15885,13392; poly right to x 16231, down to contact 16232,13522; metal x 16232 down to contact 16232,14107 on a poly pad joined to cell 2's tab |
| 3 (`ar3`) | metal, x 15800, y 13350 | contact 15840,13350; poly right to x 16280, down to y 14286, left into cell 3's tab |
| 4 (`ar4`) | poly from the fifth register cell, at 16066,13280 | right along y 13309 to x 16320, down to y 14459, left (under the metal line at x 16300) into cell 4's tab |

The four metal lines come from the left; in a wide view they collect one line from each of
the four register cells left of x 15800. Which cell drives which line is in rdp3's area.

## Ports

| Name | Layer | Crosses at | Direction | What |
|---|---|---|---|---|
| `ar0` | metal | x 15800, y 13480 | driven from outside (left) | address bit for row pair 0, from a register cell above the array |
| `ar1` | metal | x 15800, y 13433 | driven from outside | same, pair 1 |
| `ar2` | metal | x 15800, y 13391 | driven from outside | same, pair 2 |
| `ar3` | metal | x 15800, y 13350 | driven from outside | same, pair 3 |
| `ar0`..`ar4`, `ar0_n`..`ar4_n` | poly | x 15800, the ten decode rows | upper rows pass through, lower rows driven here | rows of the decode array (joined to `trace/decode.txt` by overlap) |
| ground rails | diffusion | x 15775, y 13782-13832 and every 173 below | - | the decode array's five ground rails, contacted to VSS here as well |

## Ambiguities

- The tab at the right end of each upper row (16150-16182 x 13731-13773 for pair 0) sits
  under the VCC rail and looks like a contact pad. For pairs 1-4 the tab is where the feed
  joins. For pair 0 the feed joins at the left instead and the tab is a dead end; I see no
  contact on it (a contact would short `ar0` to VCC). Working assumption: no contact.

## Not done

See Status. Bundle, as surveyed at y 13625 (chip-2 metal shot):
poly 16203-16222 (`ar1` feed), metal 16226-16242 (`ar2` feed), poly 16270-16290 (`ar3`
feed), metal 16295-16309, poly 16313-16330 (`ar4` feed), metal 16336-16350, poly
16353-16374, wide metal 16402-16451 with a poly under its left edge from y 13650 to 14440.
