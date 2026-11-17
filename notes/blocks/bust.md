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
| `cdp1_l4588` | 4655 | 12000 | `amr` c1's outer output (alias of `amr_ob_c1`); its drop seen only to (11616,4608): `?P` |
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
| 6 | `cdp1_lw2` (from cdp1's west edge) | `ubus_b6` |
| 7 | `cdp1_a2_bl` (slice 2, row A) | `rbus_b7` |

`amr`'s inner outputs drive bits 5, 6 and 7 (c1, c2, c3).
