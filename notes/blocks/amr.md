# amr: the logic above the mid-right array (x 11400-13050, y 5250-6450)

## Status (2026-11-17 05:05, contributor session)

Surveyed; only the slices' output lines drawn (`trace/amr.txt`, wiring). The slice
itself is **not traced**.

## Inventory

**Four copies of one slice, at the datapath pitch** (390), not a mirrored pair as it
looks at low zoom. `findcell.py` with the right-hand slice (x 12750-12960 x
5600-6450, clean shot) as master, all orientations: dx 0 (1.00), -391 (0.91), -781
(0.92), -1171 (0.75); with the middle part x 12570-12750: dx 0, -390, -781, -1170 (0.69)
and +391 (0.52). So the slice is about x 12570-12960 for column c3; columns (by left
edge) c0 11490, c1 11880, c2 12270, c3 12660. **c0 is a partial copy**: its two top
lines are not metal, and they leave diagonally (below).

A median composite of the four (`composite.py amr_c 12560,5450:12970,6560 --offsets
"0,0 -390,0 -781,0 -1170,0"`) helps against dirt but is too blurred for junctions at 3x.

Known cells tried: `rdp3_lat` matches at 0.66-0.71 (at (11689,5750) and
(12860,5750)) and `cdp1_reg` (mirrored, turned 180) at 0.71-0.72, but an overlay of
`rdp3_lat`'s trace (`lat1.png`) fits only in parts (the hold device region): a
different circuit with similar pieces. `mra`'s counter bit: no match.

## Outputs: each slice sends two lines north to the horizontal bus

Each full slice has two vertical metals (x 12693 and 12782 in c3, -390 per column) that
run from y 6312 up to a contact to poly at y 5585 (`follow.py` from each contact: metal
straight down, 750 px). Their contacts inside the slice are not identified (the
follower's candidates are every poly crossing). From each top contact a poly runs north
under the wide supply metal (y 5200-5550) to a pad on one metal line of a 13-line bus
(y 4657-5177, 43 px apart):

| Column | Inner line (x 12693 - 390k) | Outer line (x 12782 - 390k) |
|---|---|---|
| c3 | `amr_oa_c3` -> bus y 5177 | **bus y 4742: the line that ends on `rcs_bq3335`** (`notes/blocks/r9m.md`) |
| c2 | `amr_oa_c2` -> bus y 5135 | `amr_ob_c2` -> bus y 4696 |
| c1 | `amr_oa_c1` -> bus y 5047 | `amr_ob_c1` -> bus y 4657 |
| c0 | poly from about (11497,5590) diagonally north-east, then north along x about 11645 to a pad near (11645,5005) | poly from about (11580,5590) diagonally, north along x about 11725, then diagonally north-west towards the pad (11650,4500) of `rab`'s bit 0 (`wt.png`): **not drawn**, it needs a 5x look at that pad |

The bus lines run west to the staircase of pads at x 11650-11700 and on under the wide
supply metal x 11280-11600 (the same cross-under as `rab`'s and the strobe's), and
east for 1,400-4,750 px to a staircase of ends at x 13544, 13546, 13848, 14238, 14630,
15020, 15280, 15584, 16146, 16926 (y 4787-5196), i.e. into the right datapath at its
390 pitch. None of these lines is drawn yet (east of x 12100 nothing in the trace).

So R9's bundle line 1 (the input of `rcs_mu`'s inverter) is the **outer output of
amr's slice c3**. AMB-013's test (is the first line "a second comparator's match"?):
it is the output of a four-way repeated slice, one per column, with two outputs each;
the slice is not traced, so what it computes is open.

## R3's write strobe runs through the slices (2026-11-17)

`wr_r3` (R3's write strobe; `rdp1` drew it ending at (13310,6385)) goes on north along
x 13327 to y 5628, west to a contact (13125,5628), and a poly runs west from there along
y 5615-5630 across all four slices (`trace/amr.txt`, the crossing drawn `?P`: seen
continuous at 1.45x only). With `bust`'s result that the slices' inner outputs are data
bits 4-7 (c0..c3), **`amr` is very likely R3's high nibble**: the vertical sync width
register, written from D4-D7 on `wr_r3`. `rdp1` has only R3's low nibble (the horizontal
sync width, compared with `hsw`). The outer outputs (to the vertical control logic) would
then be the register's bits, or per-bit comparisons with a 4-bit counter, on their way to
a comparator. Believed, not traced: the slice. (The 4-bit counter in the left array,
`c4l`, does not enter `amr` from the west at y 6157-6280: open field there.)

## Ports

| Name | Layer | Where | Direction | What |
|---|---|---|---|---|
| `amr_oa_c1` ... `amr_oa_c3` | metal | x 11916, 12304, 12693, y 5585-6312 | out | inner outputs; to bus y 5047, 5135, 5177 |
| `amr_ob_c1`, `amr_ob_c2` | metal | x 12001, 12390, y 5585-6312 | out | outer outputs; to bus y 4657, 4696 |
| `rcs_bq3335` | metal | x 12782, y 5585-6312 | out | c3's outer output (r9m) |
| `wr_r3` | poly | y 5622, x 11460-13125 | in | R3's write strobe, from `rdp1`'s x 13327 line |

## Not done

1. The slice, device by device (start with c3, x 12570-12960, y 5600-6450; use single
   shots at 3-4x for junctions, the composite only for dirt).
2. c0's two lines (above).
3. The bus lines y 4657-5177, west to the staircase and east to the right datapath.
