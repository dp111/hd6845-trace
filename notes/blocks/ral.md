# ral: the stage in front of the RA pad drivers (x 13990-16330, y 4250-4560)

Serial work, 2026-11-16. **Survey only; no trace file yet.** Views in
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
