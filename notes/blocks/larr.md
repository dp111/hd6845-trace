# Left vertical array (`larr`)

Region x 2400-4780, y 6450-18550. Trace file `trace/larr.txt`.

## Status

Surveyed. The lower section is the 14-bit memory address counter, one row per bit, in
three carry groups of 7, 3 and 4 rows. Traced, placed on all 14 rows and extracted
clean (196 transistors, 0 errors, 0 warnings): the left 620 px of the row, x 2860-3480,
which is the incrementer (carry chain, half adder, group all-ones line) and the two
inverters round the bit's storage node. Not traced: the rest of the row (x 3480-4720:
clocked latches, row-start latch, whatever else), the left column, the upper section,
the logic in the two gaps. See Not done.

## Inventory

| Piece | x | y | Rows | Notes |
|---|---|---|---|---|
| Upper rows | 2950-4200 | 6543-10924 | 9, tops 6543, 7020, 7498, 7975, 8539, 9015, 9493, 9970, 10447 | one row type, different from the lower one; 87 px extra between the 4th and 5th. findcell master 2950,7020:4200,7497, offsets -477, 0, 478, 955, 1519, 1995, 2473, 2950, 3427. Not traced |
| Lower rows | 2860-4720 | 10992-18063 | 14, tops 10992, 11470, 11947, 12424, 12901, 13379, 13856 / 14549, 15027, 15504 / 16154, 16631, 17109, 17586 | cell `larr_bit`, master is the second row (y 11470-11947). Offsets -478, 0, 477, 954, 1431, 1909, 2386, 3079, 3557, 4034, 4684, 5161, 5639, 6116 (dx 0 for the first seven, 1 after). Tags s0..s13 top to bottom |
| Gap 1 | 2850-4720 | 14333-14549 | - | horizontal poly bands; the carry out of s6 ends here (contact 3094,14390) and the carry-in of s7 arrives. Not traced |
| Gap 2 | 2850-4720 | 15981-16154 | - | same pattern 1650 px lower; carry out of s9 at contact 3095,16040 |
| Left column | 2480-2860 | 6700-18500 | irregular pitch (about 600-800), about 14 cells | between rails at x 2600-2650 and 2790-2824. Not traced. Believed to hold the stages that feed the `maN_drv_in` lines and the carry logic between groups |
| Upper right block | 4450-4780 | 8250-10500 | - | separate logic right of the upper rows; not surveyed |

Columns of a lower row, left to right (master coordinates):

| x | What | State |
|---|---|---|
| 2860-3120 | carry-out NOR with its load; pull-down onto the group line L0 | traced |
| 3120-3300 | loads L1 (net a) and L2 (N2); pass-gate strip (the XOR) | traced |
| 3290-3480 | rail E with T1 / R2; inverters N3 (L3) and N4 (L4); gate Pv6 of the stored bit | traced |
| 3480-3760 | rail C (VCC) boxes; clocked pass gates under the vertical lines Vm2 (x 3555-3575) and Vm3 (x 3600-3622); load L5 at 3540-3592 x 11738-11792 with buried contact 3568-3603 x 11795-11828; pull-downs round the rail D boxes (3650-3700) | read only, see Not done |
| 3760-4250 | not looked at closely | - |
| 4250-4720 | separate cell per row (contacts on a line at x 4010-4050, loads) | - |

Vertical metal lines through the lower rows (x in master coordinates): rail A 2955-3003
(VSS), L0 2880-2900 (per group), carry 3063-3085 (row to row), rail B 3105-3178 (VCC),
rail E 3300-3400 (`larr_phe`), Vm1 3428-3448, rail C 3478-3528 (VCC), Vm2 3555-3575,
Vm3 3600-3622, rail D 3650-3700 (VSS by its pull-downs), Vm4 3727-3750, more to the
right not listed. Vm2, Vm3 and Vm4 each drop a contact onto a poly gate in every row
(3558,11567; 3610,11567; 3728,11725): clocks or strobes of the latches.

Tools made for this block: `tools/larr_px.py` (print colours of points or profiles of
a composite in all four layers: the way the doubtful junctions below were settled),
`tools/larr_cls.py` (false-colour map field / diffusion / poly from the colour ratio
of the chip-2 stripped composite, good in open areas), `tools/larr_mont.py` (several
crops in one picture, with `--trace`), `tools/larr_fuse.py` (metal outline on a
stripped layer; of little use). Composite: `tools/t.sh larr composite.py larr_row
2860,11380:4820,12040 --offsets "0,0 0,477 0,954 0,1431 0,1909 0,2386 1,3557 1,4034
1,5161 1,5639 1,6116"`. In the composite the chip-2 stripped layer (`acid`) shows poly
orange also where metal was.

## Logic

### Lower row, x 2860-3480: the incrementer (traced, extracted)

Net names carry the row tag. All of this is extracted from the trace except where
marked believed.

- `larr_a` = NOT carry-in. Load L1 on rail B; pull-down gate P2 (the carry-in) to T1,
  which is on rail E.
- `larr_n4` = NOT `larr_g6`. Load L4 on rail C; pull-down gate Pv6 to R2, on rail E.
  `larr_g6` is the poly gate at 3358-3385 x 11752-11862: believed the stored counter
  bit Q (see Ambiguities for the node it sits on). N4's poly goes a
  long way: Ph4, buried contact to the pass-gate strip, arm, P4, metal strap, along
  the bottom, up under rail A.
- `larr_n2` = NOT `larr_n4` (so = Q). Load L2 on rail B; pull-down gate P4 to R2.
- `larr_cout` = NOR(`larr_a`, `larr_n4`) = carry-in AND Q. Pull-downs to rail A (VSS),
  W 66 and 138; depletion load under rail B with its gate tied to the output by metal.
  `larr_cout` of a row is the carry-in of the row below, by metal x 3063-3085.
- `larr_mid` = carry-in ? `larr_n4` : `larr_n2`, two pass transistors on one strip
  (y 11655-11705), gates P2 and `larr_a`. So mid = carry-in XOR Q.
- `larr_n3` = NOT `larr_mid` = NOT (carry-in XOR Q): the inverted sum. Load L3 on rail
  C, pull-down to T1. N3 leaves right along a diffusion strip (y 11640-11660) to the
  clocked pass gates under Vm2 and Vm3.
- `larr_l0_gN`: one vertical metal per group, pulled to VSS by every row whose
  `larr_n4` is high (Q low). So it is high only when all Q of the group are 1, if
  something pulls it up (the pull-up is not in the rows: left column, not traced).

Four of these gates have their sources on rail E (`larr_phe`) instead of VSS; while
that line is high they cannot pull down. See Ambiguities.

### Groups and carry (traced)

- Carry runs from the top row of a group downward, so within a group the top row is
  the least significant.
- Group 0 = s0-s6. Carry-in of s0 (`larr_cin_s0`): P2's top is a poly pad
  (3258-3295 x 11000-11040) with a contact to a wide metal line that comes down from
  the upper section at x 3250-3295 and ends there; a poly line from 2897,10945 joins
  the same pad. Carry out of s6 (`larr_cout_g0`): contact 3094,14390 in gap 1 onto a
  poly band that runs right along y 14389 (followed to x 3300).
  `larr_l0_g0` is the metal x 2880-2900 from s0's tap (11332) to s6's (14114); its
  connection to anything else was not found, see Not done.
- Group 1 = s7-s9. Carry-in of s7 (`larr_cin_s7`) arrives as poly from the left column
  along y 14566. `larr_l0_g1` starts at a contact at 2892,14523 whose diffusion leaves
  to the left (2850-2880 x 14508-14540), runs down past s7-s9 and through gap 2 and
  ends on the poly line that is the carry-in of s10 (contact 2893,16171). So the
  carry-in of group 2 is the all-ones line of group 1; whatever conditions it on the
  carry into group 1 must hang on that line in the left column.
- Group 2 = s10-s13. No L0 line: the pull-downs are there but their necks end blind
  at x 2905 (`larr_l0nc_s10`..`s13`). Carry out of s13 continues down to a contact at
  about 3070,18122 on a horizontal poly at y 18105-18125 (not drawn).

### Bit order (believed)

Carry direction makes s0 the least significant bit of group 0, and the chaining of
the groups (group 2 takes group 1's all-ones line) makes the order s0 = bit 0 ... s13
= bit 13. Not yet confirmed by following the `maN_drv_in` lines (they reach the array
through the left column, which is not traced).

## Ports

Lower section, x 2860-3480 only. Coordinates are where the wire crosses out of what
is traced.

| Name | Layer | Where | Direction | What |
|---|---|---|---|---|
| `vss` rail A | metal x 2955-3003 | top 2979,10900 (goes on up); ends 18135 | in | ground of the carry gates |
| `vcc` rail B | metal x 3105-3178 | top 3130,10900 (goes on up); bottom into band y 18520 | in | |
| `vcc` rail C | metal x 3478-3528 | top 3503,10900; bottom into band y 18520 | in | |
| `larr_phe` rail E | metal x 3300-3350 | top 3325,10985 (goes on up beside the line of `larr_cin_s0`); bottom ends at contact 3320,18225 with a thin metal to 3745,18235 | in | source line of four gates per row and two poly taps per row; clock or enable, see Ambiguities |
| `larr_cin_s0` | metal x 3250-3295 | 3273,10940, from the upper section | in | carry into bit 0 |
| (same net) | poly | 2897,10945 going up | ? | second leg of the same net |
| `larr_cin_s7` | poly y 14566 | 2850,14566 | in, from the left column | carry into group 1 |
| `larr_l0_g1` = `larr_cin_s10` | diffusion | 2850,14524 going left | pulled low in the rows; pull-up elsewhere | all-ones of group 1 and carry into group 2 |
| `larr_l0_g0` | metal x 2880-2900 | no exit found between y 11318 and 14130 | pulled low in the rows | all-ones of group 0 |
| `larr_cout_g0` (= `larr_cout_s6`) | poly y 14389 | 3300,14389 going right | out | carry out of group 0 |
| `larr_cout_g1` (= `larr_cout_s9`) | contact 3095,16040 | poly under it not traced | out | carry out of group 1 |
| `larr_cout_s13` | metal x 3063-3085 | leaves the last row at 3074,18070, contact about 3070,18122 | out | carry out of the counter |
| H1 (on `larr_phe`), 11 rows | poly y top+31..51 | 2860,11511 in the master; rows s1-s6, s8, s9, s11-s13 | to the left column | believed a tap of rail E |
| H3 (on `larr_phe`), same 11 rows | poly y top+38..60 | drawn to x 3780, goes on right | - | along the top of the row |
| `larr_n3_sN` | diffusion strip y 11640-11660 | 3490,11650 (master) | out | NOT sum, to the clocked latches |
| `larr_g6_sN` | diffusion strip x 3400-3422 | 3411,11978 (master), into the band along the top of the next row | in | the stored bit |
| `larr_n2_sN` | diffusion strip y 11925-11943 | 3292,11934 (master) | out | Q, to the right along the bottom of the row |
| Pq1 (on `larr_phe`), every row | poly y 11900-11921 | ends at 3388,11910 (master) | - | gate strip at the bottom of the row |

## Ambiguities

- **What rail E is.** It is the source of the pull-downs of `larr_a`, `larr_n2`,
  `larr_n3`, `larr_n4` (loads to VCC on all four), which would make it VSS. But it has
  two metal-to-poly contacts per row (3337,11522 onto the pad where H1 meets H3;
  3330,11890 onto the tab of Pq1), Pq1 crosses diffusion further right (3490-3540 x
  11900-11920) as a gate, and at the bottom of the array the rail ends in a contact
  and a thin metal line instead of a supply. A grounded gate would be a permanently
  off transistor, so the working reading is a clock or enable that is low while the
  incrementer evaluates and high to force `a`, N2, N3, N4 high. It is traced as the
  signal `larr_phe`. Settle it by following the rail up through the upper section
  (it runs on at x 3300-3350 beside the line that feeds `larr_cin_s0`).
- **H1 to pad.** H1 (poly from the left column, y 11486-11506) ends under rail E in a
  T shape (3290-3325 x 11485-11500, stem 3305-3322 down to 11537) beside the pad
  (3328-3350 x 11512-11532) that rail E contacts and from which H3 starts. Whether the
  T is poly joined to the pad could not be seen (stem drawn `?P`). It is taken as
  joined because H1 crosses no diffusion and has no other end.
- **Three junctions that decide the adder**, all first misread by eye at 3-6x and
  then settled with colour profiles (`larr_px.py`):
  1. 2985-3045 x 11605-11652. There is no poly joining the bar of net a to the upright
     gate below it: x 2985-3001 between the left strip and the drain is field
     (profile along y 11620), and the "hook" is only the end cap of the upright gate
     (poly from x 3012 to 3033 along y 11642). So the carry pull-down is a NOR of two
     gates, not one gate.
  2. P4 and the pad under the strap (3238-3280 x 11863-11907): the pad measures as
     ordinary poly under metal and P4 starts 6 px from it with one edge line between:
     taken as one poly.
  3. Arm, buried contact 3318-3347 x 11703-11737, Ph4: both the arm (from below) and
     Ph4 (from the right) end at the outline of the contact box, each about 10 px of
     dark outline from the poly inside it. Taken as all joined (the arm has no other
     end). If the arm were not joined, N4 would not reach the carry gate and the cell
     would make no sense.
- **The storage node `larr_g6`.** Traced: the gate poly ends in a buried contact
  (3362-3398 x 11858-11897) onto a diffusion strip that runs down the open space
  between rail E and Vm1 (3400-3422 x 11872-11975; diffusion by colour, class map
  `larr_cls.py`) into the wide diffusion band along the top of the next row (y
  11950-11975 here, 11463-11497 in the next row's frame; lower part drawn `?D`, not
  checked on s6, s9, s13 which have no row below). So the stored bit of row n lives on
  the band along the top of row n+1, which runs right to at least x 3750. Read but not
  drawn: Vm1 (metal x 3428-3448) contacts a poly pad at 3425-3455 x 11895-11930
  (contact 3440,11912) whose poly runs right along y 11900-11922 and crosses between
  the VSS region 3490-3700 x 11862-11897 and that band: a clear device, bit to VSS when
  Vm1 is high. Not resolved: a second poly Pq2 (y 11928-11948) runs from the end of the
  N2 strip (3290) to a tab of the g6 strip at 3385-3403 x 11920-11937, parallel to
  Pq1. If it is tied at both ends by buried contacts then g6 = N2 and the bit is a
  static cross-coupled pair N2/N4 (and rail E would have to be VSS for it to hold);
  if it only gates something, g6 is dynamic. This is the next thing to settle; it also
  decides the rail E question. Profile along y 11937 (`larr_px.py larr_row row 11937
  3236 3428 4`): x 3236-3278 (the horizontal part of the N2 strip) and x 3384-3398
  (the tab) have the same colour as each other in every layer, and it is neither the
  open diffusion of the g6 strip beside it nor the open poly of Pq2 (chip-2 stripped
  R/G 1.28, like poly on thin oxide; clean shot dull green). Between them Pq2 is plain
  poly (3290-3376), meeting each end-to-end across one edge line. That looks like one
  continuous link N2 - Pq2 - g6 with a buried contact at each end, i.e. the static
  reading, but it is not proven and is not drawn.
- **Carry channel under P2** (3263-3292 x 11560-11632, pull-down of net a): no
  outline is visible in the views; it is certain from the two edge lines across P2 at
  y 11557 and 11635 and the different colour of the poly between them.
- **Bridge 3100-3122 x 11645-11685** from the carry-out drain to its load strip: open
  diffusion by colour in both chip-2 shots (R/G 1.18; field 1.03).

## Not done

- **Rest of the lower row, x 3480-4720.** Partial readings, master coordinates, none
  drawn: N3's strip reaches a pass gate Pv2 (poly 3513-3537 x 11630-11700, fed from
  Vm2's pad 3538-3578 x 11552-11590), then a node at 3540-3580, then pass gate Pv3
  (3580-3597 x 11600-11695, fed from Vm3's pad at 3597-3625 x 11552-11600), then a
  node that runs right as a diffusion strip y 11650-11672. Below: diffusion
  3550-3650 x 11700-11735 with a buried contact at 3612-3648 x 11703-11737 to gate Pv7
  (3625-3648 x 11740-11795), which pulls the node of load L5 (3592-3625 x 11750-11830)
  to the rail D box 3655-3700 x 11750-11795; Pv8 (3703-3722 x 11745-11795, fed from
  Vm4 by contact 3728,11725) on the other side of that box; Pv5 (3703-3722 x
  11553-11640) on the upper rail D box (contact 3672,11603); a second diffusion strip
  y 11828-11850 that turns down at x 3757-3775; VSS box 3650-3705 x 11862-11920
  (contact 3672,11885) joined to a wide region 3490-3700 x 11862-11895 which Pq1
  separates from the next row's top band. The 2-panel views `v_3450_*`, `v_3610_*`
  (view.py ... --scale 3.9 --layers metal,acid1b --comp larr_row) are the way in.
- **Gaps 1 and 2** (y 14333-14549, 15981-16154): two poly bands per gap along the
  whole width, plus thin lines; they carry the group carries to logic further right.
- **Left column** x 2480-2860 and the route from it to the `maN_drv_in` lines. One
  observation to start from: `ma8_drv_in` (poly along y 11852 from the driver) ends at
  about x 2255 on a pad with a metal contact (2237,11880); a short metal joins it to
  a contact at 2197,11923 on a poly that runs right along y 11905-11928 into the
  left-column cell at 2550-2720 x 11880-12010. So MA8's stage is the left-column cell
  level with rows s1/s2, not with s8: the stages are placed near their pads and the
  bits must reach them through the bundle of vertical metal lines at x 2150-2520
  (eight lines counted at y 11600-12000). Bit numbers are therefore still unconfirmed.
  A second poly along y 11823-11847 runs from a contact at 2283,11833 (on a bundle
  line at x 2270-2290) to x 2850, where it turns down beside s1's L0 tap without
  touching it.
- **L0 of group 0**: find its pull-up and where it is read (look along x 2860-2905,
  y 11300-14140, and at the poly that crosses under it).
- **Upper section** (9 rows) and the block at 4450-4780 x 8250-10500.
- Full-length drawing of rail E, Vm1-Vm4, rail D and the lines further right.
