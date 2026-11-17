# amr: R3's high nibble and its 4-bit comparator (x 11400-13060, y 5540-6450)

## Status (2026-11-17 13:20 (UTC+1), contributor session; the slice, its exit and its inputs independently reviewed)

**The slice is traced** (`trace/amr.txt`, cell `amr_slice`, placed four times; 57 transistors;
the full extraction has 0 errors, 0 warnings). Each slice is

- one **register bit of R3** (bits 4-7: columns at x 11490, 11880, 12270, 12660), the circuit
  of `rdp3_lat` in another layout, written from the slice's inner line (a data bus bit) on
  `wr_r3`; and
- one **comparator bit**: stored bit XOR the slice's outer line (an input here), whose
  output drives a big pull-down on one diffusion line through all four slices,
  `amr_eq_r3` = NOR of the four XORs. The line's load stands in the column at x 11490.

`tools/bust_fanout.py` lists `wr_r3` on data bits 4, 5, 6 and 7: the datasheet's R3
high nibble (vertical sync width).

**Both ends of the comparator are now joined** (`notes/blocks/amrw.md`, `trace/amrw.txt`):

- the four outer lines are the outputs of the 4-bit counter in the left array's upper rows,
  bit for bit: `c4l0` with R3 bit 4, `c4l1` with bit 5, `c4l2` with bit 6, `c4l3` with bit 7
  (the extraction prints `r3c_b4_x = NOT((c4l0 & r3_b4_q) | r3c_b4_nor)` and so on);
- `amr_eq_r3` leaves the line through a buried contact under the foot of c0's outer metal
  ("Where `amr_eq_r3` leaves", below) and runs 12,000 px west and north to a gate in the
  top-left logic (`tla`'s first cluster, west side, at (2625,3461)).

Several joins are marked `?` (Ambiguities).

## Inventory

Four copies of one slice at the datapath pitch (offsets 0, -390, -781, -1171 from the
master, column c3). **The column at x 11490 (c0) is a full copy**, not a partial one:
`cellcheck.py amr_slice` gives 3-5 % bad blocks for c1, c2 and 15 % for c0, all of c0's at
the slice's edges and at the east end of the big pull-down (below). What made it look
partial is only that its two lines arrive in poly at the top (`notes/blocks/bust.md`). It also
differs under its outer line's foot, where the line `amr_eq_r3` has its exit ("Where `amr_eq_r3` leaves", below).

| y | What |
|---|---|
| 5545-6440 | VSS rail x 12603-12653 (hangs from the wide supply metal above), VCC rail x 12816-12870 (from y 5627; goes on south with a jog west at y 6340, not drawn) |
| 5620-5880 | the register bit |
| 5885-6130 | the comparator bit (two gates) |
| 6140-6275 | big pull-down and the line `amr_eq_r3` (diffusion, y 6246-6272) |
| 6312 | the three thin metals (data line x 12693, a metal on `n2` x 12735, outer line x 12782) end, rounded, on field: no contact (4x median, `z5.png`), in c1..c3. In c0 the outer line's metal ends 10 px shorter, over the buried contact of `amr_eq_r3` (below) |
| 6330-6400 | the q line's arm to a pad (12957,6348) and a poly south: q leaves the slice |

A fifth rail (VSS, x 12998-13044) stands east of the last slice with the two lands that the
slice's east-side pull-downs end on (`east.png`).

The slices interlock: the pull-down of inverter 2 (T3), the q pull-down of the NOR (Tq1) and
the series pair use the VSS lands of the **next** slice east, across an open gap (x 12925-12995
in c3) in which two polys run north-south (PE = q, PF = the outer line).

## Logic of the slice (c3's coordinates; names of bit 7)

Traced (every device seen on a 3-6x sub-pixel median of the copies, `tools/cdp1_sr.py`, and
the overlay checked on each column; W/L as extracted):

```
T1    73/22   pass     gate wr_r3        data line (inner metal, contact (12692,5640)) <-> r3_b7_a
T2    58/22            gate r3_b7_a      vss <-> r3_b7_n2
L1    25/59   load                       r3_b7_n2     (gate tie: box at the end of the n2 band)
T3    58/22            gate r3_b7_n2     r3_b7_q <-> vss (land of the next slice)
L2    26/56   load                       r3_b7_q      (gate tie: box (12927-12951,5721-5751))
hold  24/77   gate vss (poly band on the VSS rail, contact (12631,5858))   r3_b7_a <-> r3_b7_q

To1   40/26            gate c (outer line, pad (12782,5928))    r3c_b7_nor <-> vss
Tq1   38/23            gate r3_b7_q (PE)                        r3c_b7_nor <-> vss (next slice)
L3    22/54   load                       r3c_b7_nor
Tx    38/25            gate r3c_b7_nor   r3c_b7_x <-> vss
Tc2   70/21            gate c (PF, from the outer line's pad (12784,6112))   r3c_b7_x <-> mid
Tq2   70/21            gate r3_b7_q (PE)                        mid <-> vss (next slice)
L4    30/32   load                       r3c_b7_x     (gate tie: box (12661-12695,6054-6088))
big  241/25            gate r3c_b7_x     amr_eq_r3 <-> vss     (132/26 in c0: its gate's east side is 42 px further west)
load  69/36   (c0 only)                  amr_eq_r3
```

```
r3_b7_a    = data bit 7 while wr_r3 is high; held by the weak q -> a device otherwise
r3_b7_n2   = NOT r3_b7_a
r3_b7_q    = NOT r3_b7_n2
r3c_b7_nor = NOR(c7, r3_b7_q)
r3c_b7_x   = NOT(r3c_b7_nor + c7 . r3_b7_q)  =  c7 XOR r3_b7_q
amr_eq_r3  = NOR(r3c_b4_x, r3c_b5_x, r3c_b6_x, r3c_b7_x)     high when c = R3 bits 4-7
```

c4..c7 are the outer lines (`cdp1`'s through lines y 4544, 4588, 4632, 4676), which are the
counter bits `c4l0` ... `c4l3` (`notes/blocks/amrw.md`). In every column each has exactly two
contacts in the slice, both to poly (green patch in the clean shot, no specks), and none to
diffusion: **inputs here**, not outputs as the first survey assumed.

**Where `amr_eq_r3` leaves (2026-11-17 13:20; drawn).** The review found that c0's outer metal
(x 11601-11621) ends on an outlined box and that a poly leaves the box. The box
(11601-11628, 6286-6307) is a **buried contact on the line `amr_eq_r3`**, and the outer
line has no connection there:

- under that metal the clean shot is flat tan (protected diffusion) from y 6243, the top of
  the line, to y 6305, the bottom of the box, crossed by two dark lines only (y 6276, where
  the line's south edge is in the other columns, and y 6287, the box's north side, which
  runs on east as the south edge of the line where it is stepped down, x 11640-11800): the
  box stands on the line's diffusion (`b5a.png`, `b5b.png` at 5x in four shots; `z1.png` at 8x);
- inside the box: tan, no specks and no green patch. Beside known contacts at the same zoom
  (`cmp1.png`): a metal contact to diffusion has specks ((11521,5640)), a metal contact to
  poly a green patch ((11611,5928), (11613,6112), (11786,6348)); the box has neither;
- the metal is not widened over the box, and the dark stretch across it (12 px, y 6278-6289,
  the same in both metal shots) is what a buried contact's outline prints through a metal:
  10-12 px at the tie boxes (y 6106-6135) under the four data lines. So the metal goes on
  over the box and ends at y ~6305, 10 px short of where it ends on field in c1..c3;
- a poly leaves the box south (salmon bar y 6312-6320 in the metal's margin, then orange in
  both chip-2 shots), turns west at y 6338-6356, passes under c0's VSS rail and under the thin
  metal of `cnt_gab` (x 11396: no pad, no patch, metal unbroken, `z2.png` at 6x) and ends on
  a pad with a contact (11350,6347). From there: `notes/blocks/amrw.md`.

The other reading, a metal contact from the outer line to the line's diffusion, would make
c0's compared bit the comparator's own output; nothing in the four shots supports a contact.
The piece of diffusion between the line and the box is `?D` (the two dark lines across it
are not explained in full); the buried contact is drawn firm.

`tools/unsure.py --equations`: the latch equations (`n2`, `q`) are FIRM for c1..c3 (c0's
`r3_b4_n2` DEPENDS on its `?P` gate run, which the review saw plainly at 3.4x); `nor`, `x` and
`amr_eq_r3` DEPEND on `?` items (Ambiguities 1-5).

Traced: the outer lines are the 4-bit counter `c4l` (`notes/blocks/amrw.md`). Believed: that
this counter is the datasheet's vertical sync width counter, which makes `amr_eq_r3` "sync
width reached". Two metals look like
leftovers of a through-track layout: the metal x 12735 has one contact (to `n2`,
(12742,5759)) and the metal x 12957 one (Ambiguity 3); neither takes its net anywhere.

## The column at x 11490: the line's load

East of that column's VCC rail the rail has a pad with a contact (11690,6186) (ring in both
metal shots, `mb.png`, `c0b.png`) on a diffusion land (11677-11718, 6150-6221). A band runs
east from it under a poly block (11746-11782, 6136-6252; orange in both chip-2 shots) to a
region that turns down into the line: a depletion load, W/L 69/36. The block's foot stands on
the line in an outlined box (11760-11790, 6249-6280): the gate tie. One copy only, read at 3-4x
in four shots (`c0c.png`, `c0d.png`, overlay `c0o.png`).

## Method (for the next reader)

The four-copy plain median was too blurred; `tools/cdp1_sr.py x y w h --offsets "0,0 -390,0
-781,0" --layers acid1b,metal --up 4..6` (sub-pixel aligned median) at 125-160 px windows made
every junction under metal readable. `tools/classmap.py` and `tools/railprof.py` (text) gave
the diffusion / gate / field runs under each metal: good under metal, **wrong in the open gaps**
(they call open poly "dark" and open field "diffusion") and unreliable for channel against
poly-over-field (the comparator's `nor` poly reads "poly over field" where it is a gate). In
the open gaps the chip-2 shots decide: poly is orange in both. Views: `cache/scratch/amrc/`.

## Ambiguities

1. **Three joins lie under the 17-28 px gap between two metals**, where the clean shot shows
   only a dark bar: To1's source to the VSS arm ((12710-12726, 5938-5958): by elimination, that
   diffusion has no other exit); the `x` arm to the strip of the series pair ((12754-12770,
   6072-6110): the bar spans exactly the two pieces' heights, and below it the gap is green
   field, `j12.png`); the big pull-down's VSS diffusion to its land beside the rail
   ((12656-12684, 6176-6208): outline seen). All `?D`. What would settle them: the same
   spots in a shot of a die with the metal stripped and no residue, or the simulation.
2. **L3's gate tie.** The load block's poly goes north in the open gap into a green box with a
   ring at (12882,5927) on the edge of the `nor` arm, and beside it, under the q line, is a box
   with a heavy outline (12900-12925, 5932-5962). One of them is the buried contact: `?B` on
   the first, `?P` for the second. The q line shows a bright block between dark bars over the
   second box in both metal shots, but the clean shot has neither the green patch of a poly
   contact nor the specks of a diffusion contact there (`k34.png`): read as no contact. If it
   were one, the load's gate would be q, which gives no sensible gate.
3. **How q reaches PE.** PE's head lies on the east arm of the q land in an outlined box
   (4x median, `z8.png`): `?B`; the short metal x 12957 has a bright block over the same box
   (`mo1.png`, `mo34.png`): `?C` (butting). Either alone makes PE = q. A second bright block
   on that metal at y 5857-5877 has no contact patch in the clean shot: not drawn.
4. **East of the big pull-down's east side** (x 12881-12906, y 6176-6250, open gap): an
   outline that runs down into the line; its colour is not readable. `?D`; without it the
   pull-down is 203/25 instead of 241/25.
5. **In c0, is PF separate from the load block below it?** Both are at x 11757-11782; PF's
   foot (y 6124) and the block's head (y 6136) are 12 px apart, with PF's green end-rim between
   (`c0d.png`). Drawn separate. If they were one poly, c0's outer line would be `amr_eq_r3`
   itself, and the comparator would have three bits and a feedback, which fits nothing.
6. c0's bottom run of `wr_r3` (T1's gate there) and its west corner are seen only at 1.4x: `?P`.
7. The VCC rail is drawn as one straight path x 12816-12870; between y 5705 and 5770 its east
   edge is cut back diagonally to x 12852 (`mt.png`). No contact is affected.

## The two lines of each slice north to the bus (first survey; the outer line turned out to be an input)

Each full slice has two vertical metals (x 12693 and 12782 in c3, -390 per column) that
run from y 6312 up to a contact to poly at y 5585 (`follow.py` from each contact: metal
straight down, 750 px). Their contacts inside the slice: the inner line one, to the pass
transistor's land (y 5640); the outer line two, to poly pads (y 5928, 6112). From each top contact a poly runs north
under the wide supply metal (y 5200-5550) to a pad on one metal line of a 13-line bus
(y 4657-5177, 43 px apart):

| Column | Inner line (x 12693 - 390k) | Outer line (x 12782 - 390k) |
|---|---|---|
| c3 | `db_b7` -> bus y 5177 | bus y 4742 = `cdp1_l4676` (an earlier reading that this line ends on `ra_eq_r9` was wrong: `notes/blocks/r9m.md`, correction) |
| c2 | `db_b6` -> bus y 5135 | `amr_ob_c2` -> bus y 4696 |
| c1 | `db_b5` -> bus y 5047 | `amr_ob_c1` -> bus y 4657 |
| c0 | poly from about (11497,5590) diagonally north-east, then north along x about 11645 to a pad near (11645,5005) | poly from about (11580,5590) diagonally, north along x about 11725, then diagonally north-west towards the pad (11650,4500) of `rab`'s bit 0 (`wt.png`): **not drawn**, it needs a 5x look at that pad |

The bus lines run west to the staircase of pads at x 11650-11700 and on under the wide
supply metal x 11280-11600 (the same cross-under as `rab`'s and the strobe's), and
east for 1,400-4,750 px to a staircase of ends at x 13544, 13546, 13848, 14238, 14630,
15020, 15280, 15584, 16146, 16926 (y 4787-5196), i.e. into the right datapath at its
390 pitch. None of these lines is drawn yet (east of x 12100 nothing in the trace).

(Withdrawn: an earlier version said here that the input of `rcs_mu`'s inverter is c3's
outer output. An independent review showed two poly hops on that route step one track,
and that input is R9's match: `notes/blocks/r9m.md`, correction. c3's outer line is
`cdp1_l4676`; where it goes west of `cdp1` is in `notes/blocks/bust.md`.)

## R3's write strobe runs through the slices (2026-11-17)

`wr_r3` (R3's write strobe; `rdp1` drew it ending at (13310,6385)) goes on north along
x 13327 to y 5628, west to a contact (13125,5628), and a poly (22 wide, y 5625-5647) runs west
from there across all four slices. In each slice it detours south around the data line's
contact land: down the 28 px gap between the outer line and the metal x 12735 (x 12752-12772),
west along y 5667-5690 across the land's lower part (**the gate of T1**), and up again at
x 12642-12665 under the VSS rail's edge. The west corner is seen end to end on the 5x median
(`t_12575_5600.png`); the east leg is an orange band from y 5622 to 5695 in both chip-2
shots in all four columns (`wl.png`). Drawn firm for c1..c3 and c0's leg; c0's bottom run and
west corner `?P` (Ambiguity 6). `tools/unsure.py` no longer lists `wr_r3`.

(The 4-bit counter in the left array, `c4l`, does not enter `amr` from the west at
y 6157-6280: open field there. It arrives on the four outer lines, through `cdp1`'s through
lines: `notes/blocks/amrw.md`.)

## Ports

| Name | Layer | Where | Direction | What |
|---|---|---|---|---|
| `db_b5` ... `db_b7` (aliases of the data lines, `notes/blocks/bust.md`); c0's is `db_b4` | metal | x 11916, 12304, 12693 (c0: 11522), y 5585-6312 | in | data bus bits 5, 6, 7 (c0: bit 4): written into R3 bits 4-7 through T1 |
| `amr_ob_c1`, `amr_ob_c2` (= `cdp1_l4588`, `cdp1_l4632`), `cdp1_l4676`, c0's `cdp1_l4544` | metal | x 12001, 12390, 12782 (c0: 11611), y 5585-6312 | **in** | the four bits compared with R3 bits 4-7: `c4l1`, `c4l2`, `c4l3` and c0's `c4l0`, the 4-bit counter of the left array (`notes/blocks/amrw.md`) |
| `wr_r3` | poly | y 5636, x 11445-13125 | in | R3's write strobe, from `rdp1`'s x 13327 line |
| `r3_b4_q` ... `r3_b7_q` | poly | (12965 - 390k, 6400), going south from the pad (12957 - 390k, 6348) | out | the stored bits leave the slice south; in c3 the poly joins a band y 6405-6425 running west under the VCC rail (`b5.png`). Not followed |
| `amr_eq_r3` | diffusion; poly from the buried contact (11601-11628, 6286-6307) | y 6246-6272, x 11445-13047; pad (11350,6347) | out | to the top-left logic (`notes/blocks/amrw.md`) |
| `vss` | metal | x 12628 - 390k and x 13021, y 5545 (to the wide metal above) and y 6440 (goes on south; contact to a land at (12625,6435)) | | rails |
| `vcc` | metal | x 12843 - 390k, y 6335 | | goes on south with a jog west |

## Review

Independently reviewed (2026-11-17): all 14 transistors per slice confirmed on c3 at
3.4-6.5x (no missed or invented channel), the loads, the data inputs (bits 4..7) and
`wr_r3` as T1's gate; the three `?D` joins read as joined; PE = q in function. It found
the box and the poly under the foot of c0's outer line (read since as the exit of `amr_eq_r3`,
above) and corrected the overclaims.
Unsure: L3's gate tie (both candidates give gate = nor), the pull-down's east corner (W
only), c0's load (one copy).

## Not done

1. (Done: `amr_eq_r3` leaves by the buried contact under c0's outer metal; `notes/blocks/amrw.md`.
   The line's two closed ends, under c0's VSS rail and under the rail east of c3, stay as
   they were read: no contact seen on either.)
2. (Done: the four outer lines are `c4l0` ... `c4l3`; `notes/blocks/amrw.md`.)
3. Where the four q polys go south of y 6400.
4. The rails south of y 6440 and the VCC rail's jog.
5. The `?` items (Ambiguities): the three joins in metal gaps need a shot that shows them.
6. The bus lines y 4657-5177 are in `trace/bust.txt`; nothing more to do here.
