# amrw: the wiring of R3's upper comparator (`amr`): its result west, its counter in

## Status (2026-11-17 13:20 (UTC+1), contributor session; independently reviewed)

Wiring drawn (`trace/amrw.txt`; the first 60 px of the result's route are in `trace/amr.txt`),
no transistors; the full extraction has 0 errors, 0 warnings and the same transistor count.

- **The four compared lines of `amr` are the 4-bit counter of the left array**, bit for bit:
  `c4l0` = `cdp1_l4544` (R3 bit 4), `c4l1` = `cdp1_l4588` (bit 5), `c4l2` = `cdp1_l4632` (bit 6),
  `c4l3` = `cdp1_l4676` (bit 7). The extraction now gives `r3c_b4_x = c4l0 XOR r3_b4_q` ...
  `r3c_b7_x = c4l3 XOR r3_b7_q` and `amr_eq_r3` = NOR of the four: **high when the 4-bit
  counter equals R3 bits 4-7**. That the counter is the datasheet's vertical sync width
  counter is what this says in the datasheet's words; nothing was assumed from it.
- **`amr_eq_r3` is followed to `tla`**: 12,000 px of wire to a poly crossing of the west
  column of `tla`'s first cluster, read as the gate of one transistor of a series pair under rail R1 at
  (2625,3461). The gate is seen, not drawn (it is in `tla`'s untraced part).

## Route of `amr_eq_r3` (east to west)

| Stretch | Layer | Ends | Seen |
|---|---|---|---|
| buried contact on the line under c0's outer metal (11601-11628, 6286-6307); south, then west along y 6347 under c0's VSS rail and under `cnt_gab`'s metal | poly | pad (11350,6347) | `notes/blocks/amr.md`; `f1.png` 4x, `z2.png` 6x, overlay `ov1.png` |
| west along y 6349, south at x 11068 | metal | pad (11027,6407) | follower; `w1.png` 3.5x |
| west along y 6408: the **second line of the central datapath's channel 2**, 3,580 px, no pad | poly | pad (7445,6410) | `st2.png`, `st3.png` 1.6x; `k1.png` 3x at x 7800-8220; `p1.png` 3.5x four shots |
| west along y 6413 over the crossing fields x 6330-7400 | metal | pad (6145,6410) | follower (1,284 px, no candidate); `w3.png`. The follower makes two false jumps on this
route (trap 16): from x 5888 past the pad (6495,4568) onto the wide metal x 6530-6580, and
from the pad (7445,6410) east to the thin metal x 7532; both are bare poly in both chips
(independent review) |
| west | poly | pad (5629,6412) | `st4.png`; `pads1.png` 3.8x |
| west over the vertical poly bus x 5000-5450 | metal | pad (4931,6412) | follower; `pads1.png` |
| west | poly | pad (4631,6411) | `w4.png` 2.7x: the pad is separate from the row y 6452's bend beside it |
| north along x 4628 to y 5982, west | metal | pad (3998,5979) | follower both ways; `n1.png`, `w5.png` |
| west | poly | pad (3740,5978) | `w6.png` |
| north along x 3738 | metal | pad (3739,5630) | follower; `n2.png` |
| west along y 5630 through `tla`'s second crossing field and under the foot of the step logic cluster, 1,500 px | poly | pad (2242,5632) | `st5.png` 1.65x, `w7.png` |
| north along x 2240, 2,170 px straight (the poly rows y 4540, 4980, 5500 pass under it with no pad) | metal | pad (2244,3463) | follower sampled every 400 px; `v1m.png`, `v1b.png` |
| east along y 3461 across the first bus field (six vertical metals, no pad) | poly | the diffusion column under rail R1, x 2596 | `t1.png` 3x, `d1.png` 4.5x |

Every pad has a ring in both metal shots and a green patch on a poly pad in the clean shot.
Every poly row was also profiled in the clean shot against its two flanks
(`tools/amrw_row.py`): no stretch on any of them where the row is missing.
`fld` found that the lower lines of channel 2 step down one position at x 7860-7960; the
three top rows (y 6365, 6409, 6452) do not: they are straight from x 7500 to 11000.

### Where it ends (seen at 2.75x and 4.5x, `d2.png`, `d1.png`; NOT drawn)

Under `tla`'s rail R1 (metal x 2603-2655) lies a diffusion column x 2596-2690 from y 3260 to
y 3570, with contacts to the rail near its top (specks at (2620,3280)) and near its bottom
((2612,3548)). Four horizontal polys cross it (brighter where they are over it):
y 3320-3340, y 3362-3385, y 3450-3472 (**`amr_eq_r3`**) and y 3493-3515 (from the pad
(2283,3505) of a metal that runs north along x 2283 to y 3198, not followed). Between the
second and the third the column is one node (y 3390-3445), with a box with a ring of poly
round it west of it at (2556-2590, 3395-3435). Read as: two series pairs from the rail to
one node, i.e. node = NOT(a.b + `amr_eq_r3`.d), if R1 is VSS here as `tla` found it at
y 5100-5300. Not drawn: the node's load, its exit and the other three gates are not read.

## The counter's four lines (west to east)

`trace/urch.txt` draws the four rows from the counter's tracks as far as x 4720.

| Stretch | `c4l0` | `c4l1` | `c4l2` | `c4l3` | Seen |
|---|---|---|---|---|---|
| poly east to a pad | y 6157, (5016,6153) | y 6197, (4977,6196) | y 6239, (5015,6240) | y 6281, (4977,6283) | `c4a.png` 1.85x; `pads2.png` |
| metal east over the poly bus, north by nested corners at | x 5450 | x 5495 | x 5540 | x 5582 | follower; `c4b.png`; overlay `ov2.png` |
| to a pad | (5537,5803) | (5580,5849) | (5537,5893) | (5582,5935) | `c4c.png` 2.7x |
| poly east to a pad | (5880,5805) | (5927,5850) | (5885,5893): `bust`'s | (5922,5935): `bust`'s | `c4c.png`: four straight rows, pad to pad |
| metal north, east at | x 5888, y 4572 | x 5933, y 4613 | (`bust`: x 5972, y 4660) | (`bust`: x 6016, y 4702) | follower; `vv.png`: four nested metals |
| west pad of the crossing field | (6495,4568) | (6454,4612) | `bust`'s | `bust`'s | `cf1.png`, `cf2.png`, `pads2.png` |
| poly east across the field | y 4568 | y 4612 | y 4657 | y 4700 | `cf2.png` 2.25x, both stripped shots: four straight rows |
| east pad | (6968,4570) | (6925,4612) | `bust`'s | `bust`'s | |
| metal east, north, east | y 4572, x 7492, y 4506 | y 4613, x 7536 (`bust`'s corner), y 4547 | `bust` | `bust` | follower; `cn1.png`, `z3.png` 4x |
| pad on the row into `cdp1` | (7860,4502) | (7810,4547) | (7848,4592) | (7830,4635) | `cn1.png` |
| `cdp1`'s line (after the stair at x 8215-8345, `notes/blocks/bust.md`) | `cdp1_l4544` | `cdp1_l4588` | `cdp1_l4632` | `cdp1_l4676` | |
| `amr` column, R3 bit | c0, bit 4 | c1, bit 5 | c2, bit 6 | c3, bit 7 | |

The four lines stay nested in the same order from the counter to `cdp1`; none crosses
another. That the counter's bits arrive in order on R3 bits 4-7 is consistent with the corrected
stair at `cdp1`'s west edge (`notes/blocks/bust.md`); it is not an independent check of it,
since the order is kept under any uniform shift.

`tools/unsure.py`: `c4l0` and `c4l1` are joined through firm geometry. `c4l2` and `c4l3`
pass over `bust`'s two `?P` rows across the crossing field (y 4657, 4700); here both rows
were seen end to end in both stripped shots (`cf2.png`), so those two can be made firm.
`amr_eq_r3` depends on one `?D` (`notes/blocks/amr.md`).

## Names

The nets keep the counter's names (`c4l0` ... `c4l3`); `cdp1_l4544` ... `cdp1_l4676` and
`amr_ob_c1`, `amr_ob_c2` are aliases of them (`trace/amrw.txt`; the two alias lines in
`trace/bust.txt` now point at `c4l1`, `c4l2`). Renaming the counter for what it is (the
vertical sync width counter) and `amr_eq_r3` after it is left to the coordinator.

## Ports

| Name | Layer | Where | Direction | What |
|---|---|---|---|---|
| `amr_eq_r3` | poly | (2596,3461), going east under `tla`'s rail R1 | out | gate of a transistor in `tla`'s west column (above) |
| `c4l0` ... `c4l3` | poly | x 4715, y 6157, 6197, 6239, 6281 | in | from `urch` |

## Ambiguities

1. The buried contact that starts the route (`notes/blocks/amr.md`, "Where `amr_eq_r3`
   leaves"): read as a buried contact, not a metal contact, from four shots; the diffusion
   under it is `?D`.
2. `bust`'s west pads of the crossing field for `c4l2` and `c4l3` are drawn about 30 px from
   where the pads are ((6492,4655) and (6452,4700) in `cf2.png`, drawn at (6460,4657) and
   (6470,4702)); the connections are the same.

## Review

Independently reviewed (2026-11-17): the box at (11601-11628, 6286-6307) measured as a
buried contact (colour against known buried and metal contacts; no ring, no widening, no
pit), so c4l0's line is not joined to `amr_eq_r3`; the four counter rows have no swap at
any corner; the 12,000 px route's every pad and the channel-2 row at 3x confirmed. Its
wording fixes are in.

## Not done

1. The gate at (2625,3461) and the rest of `tla`'s west column y 3260-3570 (above): the
   column, its four gates, the node's load and exit; and the source of the gate in series
   with `amr_eq_r3` (metal x 2283 north from (2283,3505), to y 3198).
2. An independent review of this route.
