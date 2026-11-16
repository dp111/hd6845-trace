# tcw: the gate column west of the island (x 6380-6760, y 2500-4450)

Serial work, 2026-11-24. Trace: `trace/tcw.txt` (**one gate**); the three pull-downs at
y 3940-4200 are in `trace/fld.txt`. Views in `cache/scratch/rax/`: `tcw_s.png` (survey of
the whole column at 1.03x), `t1a.png`, `t1m.png`, `t1cm.png` (class map), `t1load.png`
(the gate at y 3690-3905), `t2cm.png`, `w3a.png`, `w3c.png`, `w3m.png`, `w4.png`,
`w5cm.png` (the group at y 3940-4200).

## What the block is

One column of random logic, about twenty gates by the survey, built like the step-logic
clusters of the top-left block: pull-down stacks under a ground rail (x 6505-6560), each
with a load towards the supply rail x 6690-6740, inputs arriving from the west on pads
with thin vertical metals (x 6276, 6319, 6403, 6465, 6645 ...) and on horizontal polys.
`tools/findcell.py` with the cells traced so far finds no copy of any of them here
except three weak matches of the small inverter of `fld` (scores 0.68-0.74 at
(6572,3535), (6572,4143), (6572,4273)). So it has to be traced gate by gate.

Why it matters: the two sources of row address bit 0 in interlace sync and video, and
the R9 comparator's bit-0 inputs, come out of this column (`notes/blocks/fld.md`), and
the bundle that carries R9's match passes it (`notes/blocks/r9m.md`). The field
(odd/even) flip-flop is expected here.

## Traced

### AND-OR-invert at y 3690-3905 (extracted)

    tcw_o3820 = NOT( tcw_x3855 OR (tcw_a AND tcw_c) )

Under the rail one diffusion column: rail contact (6512,3708) | gate `tcw_c` (y 3732-3750)
| node | gate `tcw_a` (y 3777-3795) | output | gate `tcw_x3855` (y 3845-3863) | rail contact
(6535,3905). The output node has an arm east (y 3808-3836) to a load whose gate poly is
one piece with a pad (6648,3785) above it; the pad's tail goes west and down onto the arm
(buried contact, `?`). From the pad a thin metal runs south along x 6645 to a pad
(6640,3985): the output's way out. What that pad feeds is not traced.

- `tcw_c` and `tcw_a` are the same nets as two of the three inputs of the group below:
  their thin metals (x 6319, x 6403) end on pads at (6318,3740) and (6400,3788), and from
  each pad the poly goes east as a gate of this stack. So neither net is driven here;
  their drivers are further on (each also has a poly going west from its lower pad, along
  y 4130 and y 4000).
- `tcw_x3855`: a short gate poly that widens south-east of the rail at
  (6570-6625, 3850-3900). Not followed.

How sure: class map (poly over channel at the three gates, diffusion between, both
contacts), one 2.8x view in two shots, the load and its pad at 5.6x in both stripped
shots. The supply assignment of the two rails is the layout rule (AMB-014).

### The group at y 3940-4200 (in `trace/fld.txt`; pull-downs only)

`fld_a_in` low through `tcw_a` AND `tcw_b`; `fld_y_b` low through `tcw_c`. Their loads are
not found: the class map of the area east of the rail there (`t2cm.png`) does not give a
readable picture (the open-area thresholds are not calibrated for this spot).

## Not done

Everything else in the column (y 2500-3690 and y 4200-4450); the loads of the group at
y 3940-4200; `tcw_b`'s metal (x 6465) north of y 3990; `tcw_x3855`; the pad (6640,3985);
the polys of `tcw_a` and `tcw_c` going west along y 4000 and y 4130.

Suggested order: calibrate `tools/classmap.py --open` on the load of the traced gate
(known poly over channel at (6628-6668, 3808-3836), known diffusion arm, known field),
then take the column in 300 px tiles from y 3690 upwards.
