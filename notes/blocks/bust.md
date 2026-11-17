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
| `cdp1_a0_bl` | 5045 / 5068 | 15280 | `amr` c1's inner output; east end a pad onto a metal x 15277 that runs down to y 6826 (part of it drawn in `rdp1` as an unnamed net): believed `ubus_b5`, not drawn |
| `cdp1_lw1` | 5088 / 5110 | 15584 | a poly south at x 15580 (not drawn) |
| `cdp1_lw2` | 5131 / 5153 | 16146 | `amr` c2's inner output; east end not drawn further |
| `cdp1_a2_bl` | 5175 / 5196 | 16926 | `amr` c3's inner output; east end not drawn further |

## What this establishes

- **The data bus bit order of the central datapath**: `cdp1`'s slice bit lines are the
  right datapath's data lines, slice 4 = `ubus_b1`, slice 3 = `ubus_b2`, slice 2 =
  `ubus_b3`, slice 1 = `ubus_b4` (firm geometry, `tools/unsure.py` does not list them).
  and slice 5 = `ubus_b0`. That is slice = 5 - bit, the order the glossary already gives
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
2. `ubus_b5`/`ubus_b6`: which bus lines feed them (`cdp1_a0_bl` is believed `ubus_b5`: its
   metal x 15277 ends at y 6826, `ubus_b5` is at x 15406; the link is not found).
3. Renaming the bus as data bus bits once the coordinator agrees on names (aliases are
   used for now).

## A problem found in `rdp1`'s trace (fix proposed as its own commit)

`rdp1` drew the VCC rail x 13600 from y 5560; the metal shots show no metal there above
y 5650 (`rail.png`, `c5b.png`): it starts at about y 5655. The overhang shorted VCC to the
metal from `cdp1_c5_bl`'s pad to `ubus_b0` (y 5632), and the extraction reported it. The
one-line fix to `trace/rdp1.txt` is a separate commit so it can be reviewed on its own.
