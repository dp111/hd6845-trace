# Left vertical array (`larr`)

Region x 2400-4780, y 6450-18550. Trace file `trace/larr.txt`.

## Status

The lower section is a 14-bit counter, one row per bit, in three carry groups of 7, 3
and 4 rows. Traced, placed on all 14 rows and extracted clean (350 transistors, 0
errors, 0 warnings): x 2860-3480, the incrementer and the static pair that holds the
bit (cell `larr_bit`, first run), and x 3480-3900, the latch part (cell `larr_lat`,
second run). Rail E is settled: VSS. Not traced: the rest of the row (x 3900-4720),
the left column, the upper section, the logic in the two gaps. See Not done.

Whether this counter is the MA counter is NOT established (it was the first run's
working name). Evidence against taking it for granted is under Logic, "What the
counter is".

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
| 3290-3480 | rail E (VSS) with T1 / R2; inverters N3 (L3) and N4 (L4); gate Pv6 of the stored bit; hold device Pq | traced |
| 3480-3900 | latch part: pass gates Pv2 (Vm2) and Pv3 (Vm3) into X1; load L5 / Pv7 / Pv8 round the rail D boxes (N5); inverter X2 (Pv5, load on the VCC rail 3823-3873); pass gate under Vm5 (Y); clear device (Vm1); the band y 11950-11977 (stored bit) and its write gate (Vm6) | traced, cell `larr_lat` |
| 3900-4250 | Y ends in a buried contact (U-shaped box 3901-3939 x 11772-11800) onto a poly that goes up to 3951-3974 x 11660-11697; Z turns down at x 3950-3972 towards the next row; poly pad with a metal contact at 3958,11847 (a metal segment that runs down into the next row, to about y 11765 there); rail F x 3999-4045 with four contacts (y 11709, 11746, 11784, 11826) = a wide device; strap x 4101-4134; rail G x 4172-4218 | read only |
| 4250-4720 | separate cell per row (contacts on a line at x 4010-4050, loads) | - |

Vertical metal lines through the lower rows (x in master coordinates): rail A 2955-3003
(VSS), L0 2880-2900 (per group), carry 3063-3085 (row to row), rail B 3105-3178 (VCC),
rail E 3300-3400 (VSS), Vm1 3428-3448, rail C 3478-3528 (VCC), Vm2 3552-3575, Vm3
3599-3621, rail D 3648-3697 (VSS), Vm4 3727-3750 (tied to VSS), Vm5 3771-3795, VCC
rail 3823-3873, Vm6 3903-3922; further right (not traced) a segmented line 3949-3966,
rail F 3999-4045, rail G 4172-4218, rail H 4259-4301, a line 4336-4357. Vm1-Vm6 start
at the top of s0 (y 11045), run straight through both gaps (checked on the metal
shot) and end in the routing channel below the array (y 18100-18480), see Ports.

Tools made for this block: `tools/larr_asc.py` (second run: ASCII class map from
measured colours; noisy, only worth it for one junction at a time), `tools/larr_px.py` (print colours of points or profiles of
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
  which is on rail E (VSS).
- `larr_n4` = NOT `larr_g6`. Load L4 on rail C; pull-down gate Pv6 to R2, on rail E.
  `larr_g6` is the poly gate at 3358-3385 x 11752-11862: the stored counter bit Q. N4's poly goes a
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

- **The bit is static.** `larr_g6` sits on a diffusion strip (3400-3422 x 11872-11975,
  measured continuous) that runs into the band along the bottom of the row. `larr_n2`
  (= Q, the output of the second inverter) is joined to that strip through a long
  channel (about 85 x 17) under a poly plate Pq that is tied to rail E (VSS) by the
  contact at 3330,11890: a hold device, `kind=hold`, believed depletion mode (a gate at
  VSS makes no sense otherwise), the same structure as in cdp2 and rdp3. So
  g6 -> N4 -> N2 -(weak)-> g6 is a static pair, overwritten through the pass gate of
  Vm6 or pulled low by the clear device.

### Lower row, x 3480-3900: the latch part (traced, extracted; cell `larr_lat`)

Per row (net names carry the row tag):

- `larr_x1` <- `larr_n3` through Pv2, gate Vm2 (`larr_vm2`). `larr_n3` is
  NOT (carry-in XOR Q), so this takes the incremented value.
- `larr_x1` <- `larr_x2` through Pv3, gate Vm3 (`larr_vm3`).
  `larr_x2` = NOT `larr_ld`: an inverter (pull-down Pv5 onto rail D, load on the VCC
  rail x 3823-3873) whose input `larr_ld` is a poly band (y 11553-11568) that arrives
  from the right. So this takes a value offered from the right (not yet followed).
- `larr_x1` is a dynamic node: the gate of Pv7 and two pass-gate drains, nothing else.
- `larr_n5` = NOR(`larr_x1`, Vm4). Load L5 on rail C, pull-downs Pv7 and Pv8 on the
  two sides of a rail D box. Vm4 is tied to VSS (below), so `larr_n5` = NOT `larr_x1`:
  the incremented value, or the value on `larr_ld`, in true sense.
- `larr_y` <- `larr_n5` through the gate under Vm5 (`larr_vm5`). Y leaves to the right
  along y 11805-11824 (see Not done for where it goes).
- `larr_g6` <- `larr_z` through the gate under Vm6 (`larr_vm6`): the write of the
  stored bit. Z arrives from the right along y 11913-11933.
- `larr_g6` -> VSS through the device under the poly from the Vm1 pad (`larr_vm1`): a
  clear of the bit.

Believed function: Vm2 = count, Vm3 = load, each samples into X1; Vm5 and Vm6 then
move the new value towards the stored bit. Y and Z are different nodes (Y ends on a
poly, i.e. it is the gate of something further right), so there is at least one more
stage between them that is not traced. Until it is, the polarity of what is written
back and the phase relation of Vm2/Vm3 against Vm5/Vm6 are open.

**Vm4 is tied off.** The line has a contact to the gate of Pv8 in every row, starts
at the top of s0 and ends at 3737,18229 on a diffusion strip (y 18201-18222, tan
under the metal lines, green in the open; nothing crosses it) whose other end is the
contact at the bottom end of rail E (3330,18212). Rail E is VSS, so Pv8 never
conducts: an unused clear of the X1 inverter.

### Groups and carry (traced)

- Carry runs from the top row of a group downward, so within a group the top row is
  the least significant.
- Group 0 = s0-s6. Carry-in of s0 (`larr_cin_s0`): P2's top bends left
  (3258-3295 x 11000-11040) into a poly line that runs to x 2897 and turns up
  (2885-2910 x 10945, not followed). The first run drew a contact from this bend to
  the wide metal above it; there is none (see Ambiguities, "s0 carry-in"), and that
  metal is the VSS trunk that becomes rail E. Carry out of s6 (`larr_cout_g0`): contact 3094,14390 in gap 1 onto a
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
the groups (group 2 takes group 1's all-ones line) makes s7 below s10. How group 0
connects to group 1 is not traced (it happens in the left column / gap 1).

### What the counter is (believed: MA; not confirmed by tracing)

7 + 3 + 4 rows read naturally as one 14-bit counter with its ripple carry broken
twice (group 1's all-ones line is the carry into group 2; the carry into group 1
comes from the left column, presumably from group 0's all-ones line `larr_l0_g0`).
That fits the memory address counter, and every row also takes a value from the right
(`larr_ld`, through Vm3), which fits a reload from a row-start latch. But the
identity is not traced: the `maN_drv_in` lines have not been followed into the rows
(the stage of MA8 is level with rows s1/s2, first run), and where `larr_ld` comes
from is not traced either.

## Ports

Lower section, x 2860-3900. Coordinates are where the wire crosses out of what is
traced.

| Name | Layer | Where | Direction | What |
|---|---|---|---|---|
| `vss` rail A | metal x 2955-3003 | top 2979,10900 (goes on up); ends 18135 | in | ground of the carry gates |
| `vcc` rail B | metal x 3105-3178 | top 3130,10900 (goes on up); bottom into band y 18520 | in | |
| `vcc` rail C | metal x 3478-3528 | top 3503,10900; bottom into band y 18520 | in | |
| `vss` rail E | metal x 3302-3356 | top: it is the lower end of the trunk x 3259-3310 that comes down through the upper section (step at y 10986-11000); bottom ends at contact 3330,18212 | in | ground of four gates per row, gate of the hold devices, and of the poly lines H1/H3 |
| `vss` rail D | metal x 3648-3697 | top joins a wide band y 10935-10985; ends y 18130 | in | ground of the latch part |
| `vcc` rail x 3823-3873 | metal | top end y 11041; bottom into the band y 18520 | in | loads of X2 |
| `larr_vm1` | metal x 3428-3448 | bottom contact 3438,18342, line to the right | in | clear of the stored bit |
| `larr_vm2` | metal x 3552-3575 | turns right at y 18430 | in | X1 <- incremented value |
| `larr_vm3` | metal x 3599-3621 | turns right at y 18405 | in | X1 <- NOT ld |
| `larr_vm5` | metal x 3771-3795 | bottom contact 3783,18166 | in | Y <- N5 |
| `larr_vm6` | metal x 3903-3922 | bottom contact 3913,18207 | in | g6 <- Z |
| `larr_ld_sN` | poly y 11553-11568 | 3965,11561 (master), goes on right | in | value to load |
| `larr_y_sN` | diffusion y 11805-11824 | 3895,11815 (master), goes on right | out | new value, after Vm5 |
| `larr_z_sN` | diffusion y 11913-11933 | 3940,11923 (master), goes on right and turns down at x 3950-3972 | in | value written to the bit |
| `larr_cin_s0` | poly | 2897,10945 going up | in | carry into bit 0 |
| `larr_cin_s7` | poly y 14566 | 2850,14566 | in, from the left column | carry into group 1 |
| `larr_l0_g1` = `larr_cin_s10` | diffusion | 2850,14524 going left | pulled low in the rows; pull-up elsewhere | all-ones of group 1 and carry into group 2 |
| `larr_l0_g0` | metal x 2880-2900 | no exit found between y 11318 and 14130 | pulled low in the rows | all-ones of group 0 |
| `larr_cout_g0` (= `larr_cout_s6`) | poly y 14389 | 3300,14389 going right | out | carry out of group 0 |
| `larr_cout_g1` (= `larr_cout_s9`) | contact 3095,16040 | poly under it not traced | out | carry out of group 1 |
| `larr_cout_s13` | metal x 3063-3085 | leaves the last row at 3074,18070, contact about 3070,18122 | out | carry out of the counter |
| H1 (on `vss`), 11 rows | poly y top+31..51 | 2860,11511 in the master; rows s1-s6, s8, s9, s11-s13 | to the left column | believed a tap of rail E |
| H3 (on `vss`), same 11 rows | poly y top+38..60 | drawn to x 4100, goes on right | - | along the top of the row; purpose not found yet |

## Ambiguities

- **Rail E: settled, VSS.** It is the lower end of the wide metal trunk x 3259-3310
  that comes down through the upper section: the trunk steps right at y 10986-11000
  and goes on as rail E (one piece of metal in both metal shots, one protected
  footprint in the clean shot). It is the source of four pull-downs per row, and the
  two poly taps are explained: one is the gate plate of the hold device (a grounded
  gate, as in cdp2/rdp3), the other the pad of H1/H3. Its bottom end is a contact and a
  diffusion strip to the end of Vm4 (a tie-off). The trunk itself has not been
  followed up to a pad; VSS rests on the orientation of the gates.
- **s0 carry-in: the first run's contact does not exist.** At 3258-3295 x 11000-11040
  the poly of P2 bends left under a lobe of the trunk. Clean shot: the bend is plain
  salmon everywhere (216-220/158-162/113-116); real metal-to-poly contacts in this
  block measure greenish there (154/168/91, 179/183/105, 181/188/107). The "ring" in
  the metal shot is the notch of field in the bend's inner corner, and the dark lines
  round the lobe are 8 px wide and sit exactly on the poly edges (profiles: row 11012,
  col 3280). So `larr_cin_s0` is only the poly line that leaves at 2897,10945. If
  there were a contact, bit 0's carry-in would be grounded and group 0 could not count.
- **What H1/H3 are for.** Both are tied to VSS at the pad 3337,11522 (11 rows). H3
  runs along the top of the row to at least x 4100 just below the previous row's
  stored-bit band; H1 goes to the left column. Not found: anything they gate.
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
- **The storage node `larr_g6`: settled, static** (Logic, "The bit is static"). What
  was measured: the plate's upper half (y 11908-11911) is 219/160/114, like poly on
  field; its lower half (y 11926-11935) 232-235/163-170/117-121, like poly on a channel
  (Pv2 under rail C: 236/167/119); diffusion under the same rail is 196/175/133. The
  4 px dark line between the halves is far below any spacing rule: one plate, with the
  edge of a diffusion strip showing through. Left of the plate the N2 strip is open
  diffusion (green), right of it the tab of the g6 strip likewise. Not visible: the
  strip under the plate (drawn `?D`) and the implant.
- **Y pass gate** (3774-3795 x 11752-11822): between N5's diffusion (to x 3758) and
  the gate there is a dark bar exactly in the gap between Vm4 and Vm5, and right of
  the gate a narrow light strip (x 3802-3813) with a heavy edge at 3813-3820. Read as
  diffusion on both sides (the same gap is olive over field further down; clean shot
  165/120/95 in the strip against 108/120/60 below it; chip-2 shot not orange). The
  strip joins the band y 11805-11824. If it were field there would be a poly stub
  under Vm5 and N5 would go nowhere.
- **X2 strip under the end of Pv5** (3705-3725 x 11648-11660): the gate's end cap and
  the top edge of the strip are within 5 px of each other and in the open gap the
  colours do not separate them. Taken as not crossing (a pass gate there would be
  driven by the inverter's own input).
- **Carry channel under P2** (3263-3292 x 11560-11632, pull-down of net a): no
  outline is visible in the views; it is certain from the two edge lines across P2 at
  y 11557 and 11635 and the different colour of the poly between them.
- **Bridge 3100-3122 x 11645-11685** from the carry-out drain to its load strip: open
  diffusion by colour in both chip-2 shots (R/G 1.18; field 1.03).

## Not done

- **Rest of the lower row, x 3900-4720.** Readings, master coordinates, none drawn:
  Y's diffusion (3899-3926 x 11775-11890) ends at the top in a buried contact
  (U-shaped box 3901-3939 x 11772-11800) onto a poly that runs up 3915-3933, right
  along y 11705-11737 and up again 3949-3974 to a block at y 11660-11697. Z's strip
  (y 11913-11933) turns down at x 3950-3972 and leaves the row at the bottom. A poly
  pad 3945-3985 x 11832-11870 has a metal contact (3958,11847); its metal is a segment
  x 3949-3966 that runs down across the row boundary to about y 11765 of the next row.
  A second load block 3882-3919 x 11600-11668 on the same VCC box as X2's, buried
  contact 3900-3934 x 11682-11700. Rail F (x 3999-4045) has four contacts on one wide
  diffusion (4002-4050 x 11690-11845) with wide gates on its right (x 4054-4090):
  a driver. Views: `u4.png`, `m4.png`, `z6.png` in the scratch folder.
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
- The lines right of Vm6 at full length; where Vm1, Vm2, Vm3, Vm5, Vm6 go in the
  routing channel below the array (y 18100-18480); the trunk of rail E up to a pad.
