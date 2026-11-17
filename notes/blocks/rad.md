# rad: the RA pad drivers' input lines

## Status (2026-11-17 04:52, contributor session)

RA2's, RA3's and RA4's input lines drawn from their pad cells towards the band of `ral`
cells (`trace/rad.txt`, wiring only, no transistors). RA0's and RA1's lines are in
`trace/r9c.txt`. Each of RA2-RA4 still has one stretch undrawn (below); with the `ral`
branch's output joins they close the path `ral` cell s# -> RA# pad driver for all five
bits.

## RA2 (`ra2_drv_in`)

| Stretch | Layer | Ends | How |
|---|---|---|---|
| from the contact (18308,2094) on the pad driver's input poly (`pads_out`, instance ra2) west along y 2097 | metal | pad (17727,2097) | follow.py (from x 18280; the contact by 4x view in metal and the clean shot, `ra2g.png`) |
| south under the wide rail x 17600-17880, y 2140-2440 | poly | pad (17727,2485) | 1.6x, metal and clean shot (`ra2b.png`) |
| south along x 17727 to y 3880, west along y 3878 | metal | pad (15422,3872) | follow.py (3,650 px; ends at x 15423) |
| west under RA0's and RA1's metals (x 15300, 15342) | poly | pad (15258,3872) | 3x in three shots (`ra2d.png`) |
| south along x 15255 (the "x 15258" RA metal in r9c's notes) | metal | pad (15252,4183) | follow.py from y 3935; 4x (`ra2f.png`) |

Views in `cache/scratch/ral/` (taken while working on `ral`) and
`cache/scratch/rad/ov.png` (the overlay of the hop and the x 15255 metal).

The first draft ran the metal y 3878 straight on to x 15255: the extraction reported a
short between `ra0_drv_in`, `ra1_drv_in` and `ra2_drv_in`, because RA0's and RA1's
metals come down at x 15300 and 15342. The follower had stopped at x 15423, on the pad
of the poly hop.

## RA3 (`ra3_drv_in`)

| Stretch | Layer | Ends | How |
|---|---|---|---|
| the pad driver's input poly (instance ra3, y 3220) | poly | pad (17768,3222) | 1.6x (`ra3a.png`) |
| south along x 17771 to y 3968, west along y 3962 | metal | pad (16290,3960) | follow.py (2,200 px) |
| south along x 16290 under r9c's five metals (y 4000-4180) and the band's top rail | poly | pad (16295,4478) | 2.2x and 1.9x in three shots (`ra3b.png`, `ra3c.png`) |
| south along x 16297 | metal | drawn to y 4600 | 1.9x |

The metal x 16297 is the one `ral` cell s3's output metal (y 4590) joins from the west
(drawn on the `ral` branch, which takes it on south to RA3's unit line at (16297,5108)).
So RA3's driver input is s3's output.

## RA4 (`ra4_drv_in`)

| Stretch | Layer | Ends | How |
|---|---|---|---|
| the pad driver's input poly (instance ra4, y 4975) | poly | pad (17768,4978) | 1.6x (`ra4a.png`) |
| south along x 17771 to y 5942, west along y 5938 | metal | pad (17530,5937) | follow.py sampled with `--max` (unsampled, it jumps onto the wide rail) |
| west under the wide rail x 17440-17490 | poly | pad (17398,5937) | 2.4x (`ra4b.png`) |
| west to x 17338, north | metal | contact (17335,5800) on `r9c`'s bit-4 unit input poly | follow.py; 4x in four shots (`ra4c.png`): ring in both metal shots, pale centre on a poly pad in both stripped shots |

So the RA4 pad driver's input is the gate line of `r9c`'s RA4 unit (`ra4_cmp` = NOT
`ra4_drv_in`): the pad `r9c` left open is this line's end. `r9c` labels the unit's input
metal `ra4_drv_in_u` and draws its run south (x 17142, y 5150-5805) as `?P`, so the two
names are joined here by `@alias ra4_drv_in ra4_drv_in_u`, **through uncertain geometry**
(`tools/unsure.py` lists `ra4_drv_in` as two pieces without it). Not renamed.

## Ports

| Name | Layer | Where | Direction | What |
|---|---|---|---|---|
| `ra2_drv_in` | metal | contact (18308,2094) | out (to the pad cell) | joins `pads_out`'s `ra2_drv_in` |
| `ra3_drv_in` | metal | x 16297 at y 4600 | in | `ral` s3's output joins this metal at y 4590 (on the `ral` branch) |
| `ra4_drv_in` | poly | contact (17335,5800) | in | `r9c`'s unit input line, alias of `ra4_drv_in_u` |
| `ra2_drv_in` | poly | below the pad (15252,4183) | in | believed: on down into `ral` cell s2's output poly (the vertical at x 15240-15263, y 4300-4500, which is s0's at x 14372-14395 moved by 868). Not drawn |

## Not done

1. The last stretch from the pad (15252,4183) into `ral` s2. With it, RA2 is joined end
   to end, and `r9c`'s `ra2_drv_in_u` can be renamed (its unit line starts at s2's
   lower output pad, (15208,4805)).
2. `r9c`'s `?P` from its bit-4 metal (17135,5150) south to y 5805: when it is seen end to
   end, rename `ra4_drv_in_u` to `ra4_drv_in` and drop the alias.
3. With the `ral` branch merged: `ra3_drv_in` (r9c) joins `ra3_drv_in` through
   x 16297; then rename it.
