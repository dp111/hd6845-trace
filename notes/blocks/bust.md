# bust: the bus between the central datapath and the right datapath (queue: busT)

## Status (2026-11-17 05:32, contributor session)

Wiring drawn (`trace/bust.txt`): twelve of the fourteen lines of `cdp1`'s big channel
from its east edge (x 10845) through the cross-under at x 11230-11700 and east as metal
to their ends at x 12000-16926, and five of the east ends joined to what they feed. No
transistors. (The thirteenth, `cdp1_l4676` = `rcs_bq3335`, is drawn by `r9m` the same
way; the fourteenth, `cdp1_l4544`, does not drop: it goes on at y 4555 to the
top-right corner of the staircase, not followed.)

## Route and order

West of the staircase each line is poly; it drops about 65 px by a 45-degree diagonal
under the wide supply metal (lower lines further west, so no two cross) and comes up on a
pad at x 11655 or 11697 (alternating). **Since poly lines cannot cross, the order is the
mapping**; every line was also followed by eye at 1.35x and 2.5x in the clean shot
(`cache/scratch/bust/xu.png`, `dg1.png`, `dg2.png`), and the pads checked at 3x in both
metal shots (`pe.png`: they are separate from the wide metal, which the follower's
default gap bridges). East of the staircase: metal, `tools/follow.py` from each pad,
2,000-5,250 px; the lower eight step down one track at x 13200-13525 (`jog.png`).

| cdp1 line (x 10845) | metal y | east end | joined to |
|---|---|---|---|
| `cdp1_l4588` | 4655 | 12000 | `amr` c1's outer output (alias of `amr_ob_c1`); drop seen end to end at 3x (`c0a.png`) |
| `cdp1_l4632` | 4697 | 12390 | `amr` c2's outer output (`amr_ob_c2`) |
| `cdp1_l4676` (`rcs_bq3335`) | 4740 | 12782 | `amr` c3's outer output (drawn by `r9m`) |
| `cdp1_l4719` | 4787 | pad (13540,4787) | **R5's match**: poly south to `rdp1`'s poly x 13533-13556 from y 5450 (alias of `sl_eq_r5`) |
| `cdp1_c5_bl` | 4830 / 4850 | pad (13715,4850) | **`ubus_b0`**: poly south at x 13706 to a pad (13705,5628) (it ends there, above `rdp1`'s eq-line load), metal west along y 5632 and down as `ubus_b0` (2.7x in four shots, `c5.png`; follower) |
| `cdp1_c4_bl` | 4873 / 4894 | 13848 | **`ubus_b1`** (poly x 13845 to the data line's top, 5635) |
| `cdp1_c3_bl` | 4916 / 4937 | 14238 | **`ubus_b2`** |
| `cdp1_c2_bl` | 4959 / 4981 | 14630 | **`ubus_b3`** |
| `cdp1_c1_bl` | 5002 / 5024 | 15020 | **`ubus_b4`** |
| `cdp1_a0_bl` | 5045 / 5068 | 15280 | `amr` c1's inner output; **`ubus_b5`**: poly to a pad (15275,5628), metal down x 15277 to a pad (15277,6826), poly east under the VCC rail to a pad (15405,6826), `ubus_b5`'s metal south (3x, `b5.png`) |
| `cdp1_lw1` | 5088 / 5110 | 15584 | a poly south at x 15580 (not drawn) |
| `cdp1_lw2` | 5131 / 5153 | 16146 | `amr` c2's inner output; **`ubus_b6`**: poly to a pad (16146,5625), metal down x 16144 and west to a pad (16005,6825), poly west under the VCC rail to a pad (15870,6825), metal to `ubus_b6` (2.5x, `b6.png`) |
| `cdp1_a2_bl` | 5175 / 5196 | 16926 | `amr` c3's inner output; **`rbus_b7`**: poly to a pad (16922,5625), metal down x 16926, west to x 16839 and south: the through line on slice s7's strap track that `rdp2`/`rdp3` already identified as `rbus_b7`'s branch "to the upper array" (drawn from y 9440) |

## What this establishes

- **The data bus bit order of the central datapath**: `cdp1`'s slice bit lines are the
  right datapath's data lines, slice 4 = `ubus_b1`, slice 3 = `ubus_b2`, slice 2 =
  `ubus_b3`, slice 1 = `ubus_b4` (firm geometry, `tools/unsure.py` does not list them).
  slice 5 = `ubus_b0` and slice 0 = `ubus_b5`. That is slice = 5 - bit, the order the glossary already gives
  for R9's comparator
  (`cdp1_b#_b`, "# = 5 minus the bit"). So R8's and R9's bits can be named.
- **R5's match** (vertical total adjust: scan line = R5) leaves the right datapath north
  and runs west on `cdp1_l4719`, through the central datapath's channel unbroken
  (`cdp1` found no contact on it), towards the west logic. Where it is used: not
  followed west of x 8340.
- **`amr`'s outputs drive the bus**: its three outer outputs drive the three through-lines
  `cdp1_l4588`, `cdp1_l4632`, `cdp1_l4676` (the last is `rcs_bq3335`, the input of the
  row counter step logic's `rcs_mu` inverter); its three inner outputs drive
  `cdp1_a0_bl`, `cdp1_lw2` and `cdp1_a2_bl`. What `amr` computes is not traced.

## Not done

1. The east ends left as ports (table), and `cdp1_l4544`.
2. `cdp1_lw1` (east end 15584, a poly south at x 15580) and `cdp1_l4544`: not followed.
   Bit 7 of the upper array, and R3's own data lines, not identified.
3. Renaming the bus as data bus bits once the coordinator agrees on names (aliases are
   used for now).

## A problem found in `rdp1`'s trace (fix proposed as its own commit)

`rdp1` drew the VCC rail x 13600 from y 5560; the metal shots show no metal there above
y 5650 (`rail.png`, `c5b.png`): it starts at about y 5655. The overhang shorted VCC to the
metal from `cdp1_c5_bl`'s pad to `ubus_b0` (y 5632), and the extraction reported it. The
one-line fix to `trace/rdp1.txt` is a separate commit so it can be reviewed on its own.

With `ubus_b5` joined, the extraction shows one net writing R8's slice-0 bit (`wr_r8`)
and bit 5 of R7, R6 and R4 (`wr_r7`, `wr_r6`, `wr_r4_u`): one data bus line across the
chip, as expected.

With `ubus_b6` and `rbus_b7` joined: `cdp1_lw2` writes bit 6 of R7, R6, R4 and `cdp1_a2_bl`
writes bit 7 of R0, R1, R2 and R8's row-A slice 2 (which is therefore R8 bit 7, a cursor
skew bit). The six data lines now joined across the chip:

| Data bit | central datapath line | right datapath |
|---|---|---|
| 0 | `cdp1_c5_bl` (slice 5) | `ubus_b0` |
| 1 | `cdp1_c4_bl` (slice 4) | `ubus_b1` |
| 2 | `cdp1_c3_bl` (slice 3) | `ubus_b2` |
| 3 | `cdp1_c2_bl` (slice 2, row C) | `ubus_b3` |
| 4 | `cdp1_c1_bl` (slice 1) | `ubus_b4` |
| 5 | `cdp1_a0_bl` (slice 0, row A) | `ubus_b5` |
| 6 | `cdp1_a3_bl` (slice 3, row A) = `cdp1_lw2` (enters from the west) | `ubus_b6` |
| 7 | `cdp1_a2_bl` (slice 2, row A) | `rbus_b7` |

`amr`'s inner outputs drive bits 5, 6 and 7 (c1, c2, c3).

## West of the central datapath

The through-lines leave `cdp1`'s west edge (x 8340) as poly and end on a staircase of
pads at x 7795-7860, from which metals run west as the bus metals above the row address
selector (the same route as `r9m`'s line 1). Drawn: `cdp1_l4544` to (7535,4619),
`cdp1_l4588` (amr c1 outer) to (6913,4658), `cdp1_l4632` (amr c2 outer) to (6921,4699).
Not drawn: `cdp1_l4719` (R5's match), whose metal leaves a pad near (7782,4766) but whose
poly's drop from y 4719 is not seen (a straight guess crossed `ras` geometry).

Beyond x 6913-6921 the lines enter the crossing field under three rails (x 6440-6930,
`hop3.png`): six pads on its west side (y 4525, 4570, 4614, 4657, 4702, 4738) and poly
rows across, but the pads on its east side are not one per row, so the mapping across is
open. `r9m`'s notes say the bundle that runs with R9's match ends in the step logic's
middle cluster on pads (4270,2640) and (4232,2683): if `cdp1_l4588` and `cdp1_l4632` are
those two lines, all three of `amr`'s outer outputs feed the row counter's step logic.
Not established.

## `amr`'s partial slice c0: its two outputs drawn

c0's top contacts are at (11523,5585) and (11607,5585), each with a metal down the slice
to y 6302-6312 as in c1-c3 (follower; 3x, `cache/scratch/bust/c0t.png`). Its polys run
north, 45 degrees north-east under the supply metal, and north beside the staircase
(overlay at 1x on the clean shot, `c0ov.png`):

- **inner output** -> along x 11740 to a contact (11738,5000) on the bus metal y 5002,
  i.e. **`cdp1_c1_bl` = `ubus_b4`, data bit 4** (4x in four shots, `c0e.png`);
- **outer output** -> along x 11786, 45 degrees north-west to (11640,4544), and west as
  **`cdp1_l4544`**, the top through-line. It passes `rab`'s bit-0 pad with a dark edge
  between them (5x, `c0c.png`): `rax_o0` has no second driver.

So all four of `amr`'s slices put an outer output on a through-line into the west logic
(c0 `cdp1_l4544`, c1 `cdp1_l4588`, c2 `cdp1_l4632`, c3 `cdp1_l4676` = `rcs_bq3335`), and an
inner output on a data bus bit (c0 bit 4, c1 bit 5, c2 bit 6, c3 bit 7). Four slices,
data bits 4-7, and one result each to the west: the shape of a read-back or comparison
unit on the upper nibble. That's a guess from the wiring; the slice is not traced.

## Check: the register widths the data bus now gives

`tools/bust_fanout.py` lists, from the extraction, the write strobes of the register bits
on each data line (merged tree, 2026-11-17):

| Data line | Written into |
|---|---|
| bit 0, bit 1, bit 4 | R4, R5, R6, R7, R8, R9 |
| bit 2, bit 3 | R4, R5, R6, R7, R9 |
| bit 5 | R4, R6, R7, R8 |
| bit 6 | R4, R6, R7 |
| bit 7 | R0, R1, R2, R8 |
| `cdp1_a3_bl` (not yet joined to a data line) | R8 |

(R0-R2 bits 0-6 are on `rbus`, which `rdp2`/`rdp3` traced; R10-R15 are not yet on these
lines.) This is exactly the datasheet's layout, and nothing in the trace assumed it:
R5 and R9 are 5 bits (0-4), R4, R6 and R7 are 7 bits (0-6), and R8 has bits 0, 1, 4, 5, 7
plus `cdp1_a3_bl`, so **`cdp1_a3_bl` is R8 bit 6** (the datasheet's R8 is bits 0-1, 4-5,
6-7). **Prediction**: `cdp1_a3_bl` joins `cdp1_lw2` (bit 6) somewhere west of the central
datapath (it leaves `cdp1` towards `tc1`, as `tc1_x2`).

**Confirmed** (same session): `tc1_x2`'s metal runs on south along x 8075 and has a contact
(8078,5020) on the poly y 5024 that enters `cdp1` from the west as `cdp1_lw2` (3x,
`lw2w.png`; ring in the metal shot; the poly band continuous to x 8340 in the chip-2
stripped shot, column profiles at x 8110, 8240, 8310). Drawn; firm (`tools/unsure.py`
does not list it). Bit 6 now writes R4, R6, R7 and R8. The bit-6 group's canonical
name is `cdp1_a3_bl`, because `zz_joins.txt` already makes it canonical for `tc1_x2`.

Hence the central datapath rows: **R8 = row A**, slice 5 bit 0, slice 4 bit 1, slice 1
bit 4, slice 0 bit 5, slice 3 bit 6 (by the above), slice 2 bit 7; **R9 = row C**,
slice 5 bit 0 ... slice 1 bit 4. That settles the bit order the "rename" package was
waiting for.

## Next: the right datapath's routing zone (y 9080-9560), where `ubus` meets `rbus`

The fan-out check shows the other half of the gap: R0-R2's bits 0-6 are on `rbus_b0`..`b6`
(lower right array, `rdp2`/`rdp3`), and none of those is joined to `ubus_b0`..`b6`
(upper array). `rbus_bk` sits at the x of `ubus_b(k+2)`: the lines shift two slices
(781 px) east across `rdp2`'s untraced routing zone. Measured ends (tools/follow.py):

| Bit | `ubus` x, end going south | `rbus` x, end going north |
|---|---|---|
| 0 | 13455, 9168 | 14235, 9444 |
| 1 | 13845, 9104 | 14625, 9400 |
| 2 | 14235, 9104 | 15016, 9356 |
| 3 | 14625, 9320 | 15406, 9764 (follower stopped early) |
| 4 | 15016, 9276 | 15796, 9764 (stopped early) |
| 5 | 15406, 9234 | 16187, 9268 |
| 6 | 15796, 9104 | 16577, 9096 |

The zone is a channel of about 14 horizontal poly rows (25 px pitch, y 9080-9450) under
thin vertical metals that change rows at contacts (trap 10), and it also carries the
row counter's `uc` lines (`rdp1`: "fed in the routing zone of rdp2"). One pair seen at
1.4x (`b6z.png`): `ubus_b6` ends on a ring at (15790,9085), a poly row at y about 9085
runs east, and a ring at about (16580,9088) sits on `rbus_b6`'s top. Consistent with
"each data line crosses on one poly row", but the stripped shot's colour contrast here is
too weak to measure a row's continuity (column profile at x 16000), so **nothing is
drawn**. Method for whoever takes it: list every ring (contact) in the zone from both
metal shots, assign each to its poly row by y, check each row's continuity in the clean
shot at 3x between consecutive rings, then build the joins; `tools/bust_fanout.py` must
then show bit k writing R0, R1 and R2 as well.
