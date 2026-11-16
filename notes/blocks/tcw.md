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

## Read, not drawn (2026-11-24)

**Class map check.** `tools/wl_px.py` at known spots of the traced gate gives, for the sum
of red minus green over the two chip-2 shots: load gate (poly) 79, diffusion arm 45,
field 11-36; at the spots south of it that looked unreadable: 94 and 77 on the blocks
(poly), 47-49 on two areas (diffusion), 11 on the large area (field). So the `--open`
thresholds hold here; the map of y 3940-4210 east of the rail (`t2cm.png`) is right as
far as it goes, it just does not show which poly ties to which node.

**Tile y 3420-3700** (`t3cm.png`):

- An inverter: rail contact (6527,3490), one gate at y 3515-3535 whose poly comes from
  the west along y 3525 (seen to x 6430), output node y 3540-3560 with an arm east along
  y 3555 to a poly block (6625-6680, 3540-3570) and the diffusion under the supply rail.
  This is the place of one of `findcell`'s inverter matches ((6572,3535)).
- **`tcw_b` passes through**: its thin metal x 6465 ends on a pad (6460,3650); from the
  pad a poly crosses under the ground rail along y 3640-3655 over field (no transistor)
  and goes on east from (6580,3647). So `tcw_b` comes from east of the rail, between
  the column and the island.
- Under the rail at y 3575-3635 a small island that the map gives as diffusion with a
  poly outline, inside field: not understood.

**East of the supply rail** (`tb1.png`, x 6560-7120, y 3590-3720): the logic does not
end at the rail x 6690-6740. A second gate column stands at x 6750-6960 (boxes with
contact pits at (6885,3640), a wide metal at x 6860-6890, gates and loads between), and
`tcw_b`'s poly heads into it. So the untraced logic between this column and the island's
channel W1 (x 7174) is two columns wide, not one; the queue entry is widened.

## The whole ground rail as text (2026-11-25)

`tools/railprof.py 6514 6546 Y0 Y1` (new): classifies the strip of the clean shot under
a rail and prints the runs along it. Under a rail the clean shot's colours are the
"protected" ones, so a gate (bright salmon: poly over a channel), diffusion (tan) and
field (pink) separate cleanly; checked on the six gates already traced (all six found,
within 6 px). It does **not** find contacts (pits are too small and edge lines look the
same; two attempts with blob detection in the clean shot and in the metal shots found
only some of the known ones), and it calls dull edge regions "poly over field" (one such
at y 3910-3934, checked by colour: not a gate).

Seventeen gates under the rail x 6505-6560, in five stretches of diffusion:

| Stretch | Runs (y) | Reading |
|---|---|---|
| A, y 2699-3215 | D 2699-2739, **G 2740-2765**, D, **G 2791-2812**, D 2813-2912, **G 2913-2934**, D, **G 2957-2978**, D 2979-3085, **G 3086-3109**, D, **G 3140-3164**, D 3165-3215 | six gates in three pairs; not looked at |
| B, y 3237-3616 | D 3237-3250, **G 3251-3274**, D, **G 3295-3317**, D 3318-3337, **G 3338-3361**, D 3362-3408 (rail contact, two pits), **G 3409-3433**, D 3434-3447; then D 3470-3512 (rail contact), **G 3519-3542**, D 3543-3560 | class map `t4cm.png`: the nodes at y 3240, 3326 and 3437 each have an arm east. Readings: an AND-OR-invert at 3237-3408 if the top node is on ground through its arm (not seen), output at y 3326; a single pull-down at 3409 (output y 3437); the inverter at 3519 (output y 3550). The four upper gates take four horizontal polys from the west (y 3260, 3305, 3347, 3392) |
| C, y 3695-3925 | traced: `tcw_o3820` | |
| D, y 3956-4195 | traced (pull-downs): `fld_a_in`, `fld_y_b` | |
| E, y 4200-4344 | D, **G 4257-4281**, D | one gate; not looked at (a `findcell` inverter match at (6572,4273)) |

West of the column a bus of thin vertical metals (x 6232, 6276, 6319, 6360, 6403, 6465)
brings the inputs: each gate's poly runs west to a pad on one of them. A net can have
pads at several rows (`tcw_a`, `tcw_c` do), so the bus metals have to be followed pad by
pad; a metal at one x is several nets along its length.

## Not done

Everything else in the column (y 2500-3690 and y 4200-4450); the loads of the group at
y 3940-4200; `tcw_b`'s metal (x 6465) north of y 3990; `tcw_x3855`; the pad (6640,3985);
the polys of `tcw_a` and `tcw_c` going west along y 4000 and y 4130.

Suggested order: calibrate `tools/classmap.py --open` on the load of the traced gate
(known poly over channel at (6628-6668, 3808-3836), known diffusion arm, known field),
then take the column in 300 px tiles from y 3690 upwards.
