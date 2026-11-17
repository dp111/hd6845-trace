# rad: the RA pad drivers' input lines

## Status (2026-11-17 04:49, contributor session)

RA2's input line drawn from the pad cell to a pad at (15252,4183) above the band of
`ral` cells (`trace/rad.txt`, wiring only, no transistors). RA0's and RA1's lines are
in `trace/r9c.txt`. RA3's and RA4's not started.

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

## Ports

| Name | Layer | Where | Direction | What |
|---|---|---|---|---|
| `ra2_drv_in` | metal | contact (18308,2094) | out (to the pad cell) | joins `pads_out`'s `ra2_drv_in` |
| `ra2_drv_in` | poly | below the pad (15252,4183) | in | believed: on down into `ral` cell s2's output poly (the vertical at x 15240-15263, y 4300-4500, which is s0's at x 14372-14395 moved by 868). Not drawn |

## Not done

1. The last stretch from the pad (15252,4183) into `ral` s2. With it, RA2 is joined end
   to end, and `r9c`'s `ra2_drv_in_u` can be renamed (its unit line starts at s2's
   lower output pad, (15208,4805)).
2. RA3's and RA4's lines from their pad cells (`pads_out` instances ra3, ra4, right
   edge, about (18800,2750) and (18800,4650)) to the band.
