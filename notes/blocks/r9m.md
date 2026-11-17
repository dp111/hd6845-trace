# r9m: where R9's match goes (drawn, except the last 12 px: AMB-013)

Serial work, 2026-11-16. No trace file. Views in `cache/scratch/rax/`: `eq1.png` ...
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

## Drawn (2026-11-17 04:33, contributor session)

`trace/r9m.txt`: the whole route above, from `cdp1`'s poly end (x 8340) to the stub at
the foot of x 4194, as one net `cdp1_b_eq`. Every metal stretch re-run through
`tools/follow.py` (both chips' metal shots); the diagonal at x 4626-4668 placed by
sampling the follower with `--max` (it is at (4670,2639) after 180 px, (4660,2633) after
190, (4620,2598) after 230). Checked by overlay in `metal` and the stripped shots at
1-1.25x along the whole route and at 4x at the corner (4194,2599)
(`cache/scratch/r9m/pv1.png`, `pv2.png`, `pv3.png`, `cor.png`).

The follower's two contact candidates on the route are not contacts (four shots at 4x,
`cc1.png`, `cc2.png`): (7379,4527) and (5973,3398) are dark specks in the clean shot only,
with no ring in either metal shot. So the line has no taps between the comparator and
the step logic.

Extraction: no new transistors (the three poly hops cross no diffusion), no name clash;
`cdp1_b_eq` is one net from the comparator's load to (4170,3376). The stub's last 12 px
to the metal x 4148 (`rcs_bq3335`) are **not drawn** (AMB-013 unchanged).

## Not done

The other three lines of the bundle to their sources (the first decides
AMB-013); the pads (4270,2640) and (4232,2683) west into the cluster; `rcs_e3`'s metal
beyond (4494,3813).
