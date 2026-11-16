# r9m: where R9's match goes (followed, not drawn)

Serial work, 2026-11-21. No trace file. Views in `cache/scratch/rax/`: `eq1.png` ...
`eq9.png`. Every metal stretch from `tools/follow.py`.

## Route of `cdp1_b_eq`, from the comparator west

| Stretch | Layer | Ends |
|---|---|---|
| from `cdp1`'s edge (8340,4459) west | poly | pad (7815,4460) |
| west along y 4462, south at x 7450, west along y 4527 (the top one of six bus metals that cross above the row address selector) | metal | pad (6920,4525) |
| west under three rails | poly | pad (6445,4520) |
| west over a field of eight vertical polys (x 6050-6400, no pads seen), north along x 5974 from y 4528 to y 2642, west along y 2640 | metal | pad (5358,2640) |
| west under the metals of `res_b` (x 5275) and `lpstb_b` (x 5335) | poly | pad at about (4912,2640) |
| west, shifting up 42 px on a diagonal at x 4580-4660, to x 4192 at y 2598, south along x 4192 | metal | y 3385, with a stub west to x 4168 |

It is the second of four parallel lines over the last 1,200 px. The other three, by
their west ends: the first (y 2598 at x 4760) shifts to y 2555, turns south at x 4148 and
ends on the contact (4148,3335) of `rcs_bq3335`; the third ends on a pad (4270,2640) with
a poly west; the fourth on a pad (4232,2683) with a poly west. `rcs_e3`'s pad (4270,2725)
is the next position down; its metal goes east to x 4496 and south to y 3813 (followed,
not drawn), so `rcs_e3` is not one of the four.

## Where it ends

In the middle cluster of the row counter's step logic (`trace/tla.txt`), beside the
contact of `rcs_bq3335`, the input of the inverter that makes `rcs_mu`:

    rcs_mu  = NOT rcs_bq3335
    rcs_in1 = NOR(rcs_mu, rcs_mv)     = rcs_bq3335 AND NOT rcs_mv
    row counter step = rcs_in1 OR (NOT rcs_e4 AND NOT (rcs_e3 AND rcs_a2))

Whether the match line is on `rcs_bq3335` is AMB-013. If it is, the first term of the
row counter's step is "scan line equals R9 (as compared at the pins), and not
`rcs_mv`", which is what one expects of it; but that is the reason to be careful, not
evidence.

## Not done

Draw the route. The other three lines of the bundle to their sources (the first decides
AMB-013); the pads (4270,2640) and (4232,2683) west into the cluster; `rcs_e3`'s metal
beyond (4494,3813).
