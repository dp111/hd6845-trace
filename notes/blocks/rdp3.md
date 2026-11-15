# rdp3: right datapath, lower rows

Region: x 13350-16950, y 10700-12900, plus x 13350-15800, y 12900-13480.
Trace: `trace/rdp3.txt`. Scratch: `cache/scratch/rdp3/`.
Own tools:
- `tools/rdp3_sharp.py`: view.py with an unsharp mask.
- `tools/rdp3_strips.py`: montage of vertical strips, for following per-slice lines.
- `tools/rdp3_cmp.py`: compares copies of a rectangle with their median, block by block,
  as text (no image needed), and can save the median as a composite. Every instance
  below was checked with it. Composites: `rdp3_w16` (x 14490-15010, y 11690-12445, the
  whole period of a slice: comparator cells and latch, median of 12 inner slices of both
  bands), `rdp3_p16` (narrower, all 16), `r0w` (the AR cells).
- `tools/rdp3_boxstat.py`: mean colour of small boxes in all shots, by class, with R-G of
  the clean shot: tells a metal contact on poly (olive, R-G -22..+7, bright in `metal1`)
  from a buried contact or diffusion under metal (tan, R-G +30..+40).
- `tools/rdp3_jogs.py`: for a bundle of vertical tracks, where metal crosses the gaps
  between tracks (jogs) and where a track has no metal. `tools/sel_tracks.py` bridges
  gaps up to 14 px and so reads two nets that share a track across a jog as one line.

Slice tags and columns: s0..s7 from the left; sK has its VSS rail (left edge of the
slice) at x 13783 + 390 K, i.e. s(K) = right-datapath column c(K-1); s0 lies left of c0.

## Status

- Traced, placed and checked: the address register row AR (5 latches), the two 8-bit
  register rows RA and RB (16 latches), under each a full 8-bit equality comparator
  (per slice an XOR of the register bit with a per-slice line `c`, and a pull-down on a
  row-wide wired-NOR line with one load), the exits of both equality lines, and the
  left-edge bundle (every line to both ends inside the region). Extracts with no errors
  and no open nets.
- **Run 3 corrects run 2: RB is R2 and RA is R1; R0 is row RC (rdp2's), the row above.**
  The bundle steps one track to the left at y 12300-12540, which the track scan could
  not see. So `rdp3_cb_eq` is "c = R2" (horizontal sync position) and `rdp3_ca_eq` is
  "c = R1" (horizontal displayed). The R0 comparator is rdp2's band C.
- Both equality lines leave through a buried contact in slice s1 onto a poly line going
  west to bundle track L3: `rdp3_cb_eq` then goes **north** (out of the region at
  13478,10700), `rdp3_ca_eq` **south** (out at 13434,13480, bd1's track k8). Neither is
  gated or latched inside the region.

## Inventory

Slices: 8, pitch 390, numbered s0..s7 from the left. In slice sK:

| x (s2; add 390 per slice) | What |
|---|---|
| 14565 | VSS rail (60 wide); a ninth one at x 16906 right of s7 |
| 14626 | bus line (data), `rdp3_bus_sK` |
| 14673 | metal piece y 11738-12200 in each band, no contact found ("T2") |
| 14712 | `rdp3_c_sK`: the line the register bits are compared with |
| 14772 | VCC rail (56 wide) |
| 14886 | strap inside each latch cell, no contact; in s7 a through line (x 16838) |

Rows (band B = band A moved up by 846; the two bands are identical from the top of the
comparator down, measured: block correlation 0.93-0.98):

| y | What |
|---|---|
| 10561-10831 | register row RC (rdp2's; the region's top edge y 10700 cuts through it) |
| 10831-10925 | gap: the poly line of `rdp3_cb_eq` at y 10846-10867 (from slice s1 west to the bundle); RC's strobe poly is at y 10800-10830 |
| 10925-11056 | band B match pull-downs (`rdp3_mpd`), `rdp3_cb_eq` strip at y 10930-10952 |
| 11056-11321 | band B XOR cells (`rdp3_xor`) |
| 11321-11591 | **register row RB = R2** (`rdp3_lat` upside down), strobe poly y 11558-11586 |
| 11591-11775 | gap: empty field except the poly line of `rdp3_ca_eq` at y 11693-11713 (from slice s1 west to the bundle) and the rounded top ends of the T2 pieces at y 11738 |
| 11775-11905 | band A match pull-downs, `rdp3_ca_eq` strip at y 11776-11798 |
| 11905-12167 | band A XOR cells |
| 12167-12437 | **register row RA = R1** (`rdp3_lat` upside down), strobe poly y 12404-12432 |
| 12437-13000 | routing zone (read at low zoom by the first run, table below; not drawn) |
| 13010-13280 | **row AR**: 5 latch cells under slices s1..s5 |
| 13280-13500 | the five AR outputs, nested L-shaped lines going right |

Left of the array, x 13348-13825: a bundle of 12 vertical metal tracks on a 43.4 px
pitch, L0..L11 at x 13348 + 43.4 k (bd1 calls the same tracks k6..k17 at y 14700).
L10 and L11 exist only below the array (L10's place is the first VSS rail higher up).
See "Left-edge bundle" under Logic.

Rails: which is which was settled by the first run (both loads of every latch hang from
the x 14772 + 390k rail, which also runs into the decode array's VCC bus). All new
cells agree: every load strip starts on a land contacted by that rail.

## Logic

### Latch cell `rdp3_lat` (traced)

Master at x 14597-14987, y 13010-13280 (slice s2 of row AR). 6 transistors:

```
a   <- bus      pass transistor T1 while the strobe is high        34/28
n2  = NOT a     pull-down 51/22, load 30/52
q   = NOT n2    pull-down 52/22, load 28/49
a  <-> q        hold device, gate tied to VSS, 22/82 (see below)
```

- Bus contact at the strobe edge of the cell; strip under the strobe poly's loop (T1);
  buried contact to the poly that is the first inverter's gate (node a).
- q is in the same sense as the bus. It leaves by a buried contact on the output land
  onto a poly strip (down in AR, up into the comparator in RA/RB).
- T_a's source is the VSS land of the next slice to the right; the last cell of a row
  has a land under the rail to its right (AR: x 16125; RA/RB: ninth rail, x 16906).
- **Hold device (was AMB-1/AMB-2, read on the composites at 6-7x in three shots).** The
  poly band along the cell edge is contacted to the VSS rail (AR 14562,13256) and
  widens under the VCC rail into a block, AR 14727-14809 x 13206-13272. Two thin dark
  lines cross the block at y 13223 and 13246: what the first run saw as three stripes
  S1/S2/S3 is one piece of poly with the edges of a diffusion strip showing through
  (the gaps between the "stripes" are 3-5 px, far below any spacing rule; in the slot
  between the c track and the VCC rail, where the poly shows in open colours, S3 and S2
  look joined, which agrees but is not decisive on its own). The strip runs from the feedback land (node a, buried contact) to the
  output land (q). So: a transistor a <-> q, W/L about 22/82, gate at VSS. An
  enhancement device would never conduct, so it is believed to be depletion mode: a weak
  feedback that holds the latch and that the bus overpowers during a write. The strip is
  drawn uncertain (`?D`), the transistor is tagged `kind=hold`. Not visible: the
  implant, and the strip's ends where they meet the two lands (each is hidden by a
  metal-gap line).

### Rows RA, RB (traced): 8 bits each

`@inst rdp3_lat ... rot=180` at dx -782, -391, 0, 390, 780, 1170, 1560, 1951 and
dy -853/-854 (RA), -1699/-1700 (RB). The cell is the AR cell unchanged: the first run's
doubts about the cell's upper edge were the hold device's stripes and poly seen between
metal lines. Differences are outside the cell: the bus line and the c track run through;
q goes up in poly.

- Strobe `rdp3_ra_ld`: row poly; right end free (ends at x 16925); at the left end it
  turns down at x 13782 under the first VSS rail to a pad with a contact at
  (13823,12700); thin metal on bundle track L11 (x 13825) goes down from there and
  leaves the region at y 13480.
- Strobe `rdp3_rb_ld`: row poly; right end free; runs on west to a pad with a contact
  at (13648,11571); metal goes down on track L7 (x 13651), **jogs left at y 12357 onto
  track L6 (x 13608)** and leaves the region on L6.
- Which registers (run 3; the lower ends are bd1's table of tracks at y 14700, the
  stretch y 13480-14700 between the two regions was checked with `tools/rdp3_jogs.py`
  in both metal shots: no jog, and no break longer than a poly line passing under):
  - `rdp3_rb_ld` arrives on L6 = bd1's k12 = `sel_w2` (contact 13609,14956).
    **RB = R2** (horizontal sync position).
  - `rdp3_ra_ld` goes down L11 to y 14000, **jogs left onto L10** (x 13782; seen,
    `cache/scratch/rdp3/l11_jog.png`) = bd1's k16 = `sel_w1` (contact 13785,14913).
    **RA = R1** (horizontal displayed). The metal on L11 below y 14050 is another net
    (bd1's k17, which comes from a track at x 13868 by a jog at y 14050); the piece of
    L10 above y 13893 is a third net (ends there on a contact to a poly line going west).
  - `sel_w0` (bd1's k13, x 13652) comes up L7, **jogs right onto L8 at y 12400** and
    ends on the contact (13690,10815) on the west end of the strobe poly of row RC, the
    register row above RB, which is rdp2's. **RC = R0.** Drawn here as `rdp3_rc_ld`.
  - The three rows from the top are therefore R0, R2, R1: the order of those three
    select columns in the decode array.
  - Run 2 had RB = R0 from a track scan of L7 "continuous from y 11566 to 15000". It is
    not one line: at the jog two nets share the track 22 px apart, and
    `tools/sel_tracks.py` bridges gaps up to 14 px on either side of a dark line.
  - On chip 2 the `sel_w0` line has a 10 px dark gap at (13652,12708). Chip 1's metal is
    unbroken there and nothing lies under it: dirt or a scratch on that die, not layout.

### Comparator (traced): `rdp3_xor`, `rdp3_mpd`, `rdp3_mpd1`

Per slice, master s2 of band A (x 14545-14952, y 11776-12167):

```
nor = NOR(c, q)              load 31/58;  T6 gate c 41/24;  T7 gate q 36/22
x   = NOT(nor + c.q)         load 27/50;  T5 gate nor 40/23; series pair c 72/25, q 72/24
eq  = NOR(x of 8 slices)     per slice 269/23 (s1: shorter); one load 67/42, in slice s1
```

so x = c XOR q and `eq` is high when the register equals the eight `c` lines.

- `c` reaches the cell on the x 14712 track through two contacts onto poly pads:
  (14720,11936), poly east under the VCC rail to gate G1 (x 14853-14878), and
  (14715,12121), poly west = gate of T6.
- q comes up from the latch in poly at x 14879-14901, jogs right at y 12095 and is gate
  G2 (x 14901-14925); on the way it crosses the nor node (T7).
- x is a diffusion node (band under the bus at y 11937-11961, strip down the left to
  T5, strip east at y 11963-11978 to the series pair). A tab (14624-14644 x
  11913-11942) carries it up to a buried contact on the pull-down's gate.
- Match pull-down `rdp3_mpd`: C-shaped gate round a VSS diffusion (land and contact at
  14562,11870); outside the C the diffusion is the `eq` line, a strip y 11776-11798
  that runs through all eight slices (under the VSS rails) and ends dead under the
  first rail (x 13768) and under the ninth (x 16925).
- **Exit of the `eq` line (run 3).** In slice s1 a tab of the strip comes up under the c
  track (x 14314-14336) to a buried contact (box 14312-14338 x 11744-11766 in band A,
  y 10898-10920 in band B) on the end of a poly line. The line runs up 50 px, then west
  through the gap above the band (band A y 11693-11713, band B y 10846-10867), under
  slice s0's lines and rails and under bundle tracks L4..L9 without contact, to a pad
  with a metal contact on track L3: (13479,11703) and (13477,10857).
  - The box is a buried contact and not a contact to the c track that passes over it
    (run 2's reading, "feed of c_s1"). Measured with `tools/rdp3_boxstat.py`: inside the
    box the clean shot is tan, R-G = +37 (band A) and +34 (band B), the same as the eq
    strip under the same track (+38, +32); the 24 known metal contacts from the c tracks
    to poly pads give -22..+7 (one +29) and are bright in the chip-1 metal shot
    (180-212), the box is not (125-140, as the strip: 136-160). A column profile down
    x 14322 shows poly (R-G +63..+99) down to the box and diffusion colour, not field,
    from the box to the strip. Both bands show the same structure
    (`cache/scratch/rdp3/eq_tab_c.png`, 6x, both bands side by side).
  - A contact to the track would also tie c of slice s1 to both eq lines.
  - `rdp3_cb_eq` goes **north** from (13477,10857) on L3 and leaves the region at
    (13478,10700); by scan the metal runs on to about y 9960. `rdp3_ca_eq` goes **south**
    from (13479,11703) on L3, jogs left at y 12530 onto L2 (x 13434) and leaves the
    region at (13434,13480); that track is bd1's k8, which bd1 has not traced.
  - Nothing gates or latches either line inside the region: wired NOR, one load, poly,
    metal.
- Slice s1 (`rdp3_mpd1`): the C is shorter (right arm at x 14352-14372) and the room is
  taken by the load of `eq`: VCC land with contact (14403,11862), strip east under a
  gate block (14455-14497 x 11812-11915), up at x 14502-14524 to the `eq` strip; the
  block's neck ends on a buried contact on the strip (14473-14499 x 11774-11803).
- T7's diffusion (14808-14945 x 12128-12164, `?D`): the part left of the q poly is in
  the open and has the colour of field in the clean shot; read as diffusion because the
  nor node's tie box and neck (14838-14873 x 12086-12140) lead into it, the strip right
  of the q poly (tan under the rail's margin) needs a partner, and the chip-2 stripped
  shot shows it warmer than the field above it. If it were field, nor = NOT c and
  x = c AND NOT q.

Believed: the `c` lines are the bits of the horizontal character counter (R0, R2 and
R1 are all compared with them, R0 in rdp2's band C). Then `rdp3_cb_eq` is "counter =
R2", the start of horizontal sync, and `rdp3_ca_eq` is "counter = R1", the end of the
displayed part of the line.

### Row AR (first run): 5 bits, the address register

Instances `ar_s1`..`ar_s5`. Data `rdp3_bus_s1`..`s5`; strobe `rdp3_ar_ld` (joined to
`areg_load` in zz_joins); outputs `rdp3_ar_sN_q` go right at y 13352-13481 with a poly
cross-under beneath each VCC rail (joined to `ar0`..`ar4`).

### Bus lines and bit order

`rdp3_bus_sK`: thin metal at x 13845, 14236, 14626, 15016, 15407, 15797, 16187, 16577
(K = 0..7) at the top edge y 10700, straight down. One contact per latch cell and
nothing else on them inside the array. s1..s5 end in the AR cells.

Nothing in the region shows which slice is which data bit: there is no carry chain, and
the comparator treats all slices alike. Inference only: the address register takes
D0-D4 and uses s1..s5.

Routing zone, read at 1.15x by the first run, not drawn and not re-checked:

| Bus | Path |
|---|---|
| s0 | contact (13843,12503), poly at y 12503 right to contact (16047,12500), metal down to (16047,12822), poly right at y 12825 to x 16808, then down |
| s5 | contact (15797,12738), poly right at y 12743 to contact (16817,12743), metal down at x 16817 |
| s6 | contact (16186,12698), poly right at y 12697 to contact (16860,12700), metal down at x 16860 |
| s7 | contact (16580,12568), poly down and right at y 12655 to contact (16908,12653), metal down at x 16908 |

### Left-edge bundle (traced, run 3)

Thin metal, 18 wide, tracks L0..L11 at x 13348 + 43.4 k. Between y 12300 and 12540
most lines step one track to the left going down, so a track number names a place, not
a net. Each net, from north to south (all drawn; overlay `ov_bun1.png`):

| Net | North end | Path | South end |
|---|---|---|---|
| `rdp3_n0` | L0 at y 10700 | straight down L0 to y 12789, steps left to x 13307 | leaves the region west/south at (13307,12850); the track at x 13307 above y 12745 is another line, which turns west there |
| `rdp3_s0` | poly pad from the west, contact (13346,12829) | L0 | L0 at y 13480 (bd1's k6 = `bd1_xn1`) |
| `rdp3_n1s4` | L1 at y 10700 | L1 to contact (13390,12438); poly link east y 12426-12454 under L2, L3; contact (13522,12440); L4 | L4 at y 13480 = bd1's k10 = **`sel_w4`** (so R4's write strobe goes north on L1) |
| `rdp3_n2s1` | L2 at y 10700 | L2, jog left at y 12486, L1 | L1 at y 13480 (bd1's k7, untraced there) |
| `rdp3_cb_eq` | L3 at y 10700 | L3 down to contact (13477,10857) | (poly east to comparator B) |
| `rdp3_ca_eq` | (poly from comparator A) contact (13479,11703) | L3, jog left at y 12530, L2 | L2 at y 13480 (bd1's k8, untraced there) |
| `rdp3_n4` | L4 at y 10700 | L4 to contact (13522,12375); poly west y 12387-12407 under L3..L0 | leaves west at (13330,12397) |
| `rdp3_n5` | L5 at y 10700 | L5 to contact (13565,11920); poly west y 11910-11931 | leaves west at (13330,11920) |
| `rdp3_n6` | L6 at y 10700 | L6 to contact (13608,11438); poly west y 11429-11452 | leaves west at (13330,11440) |
| `rdp3_n7s9` | L7 at y 10700 | L7, jog left at y 11507, L6, jog left at y 12313, L5 to contact (13565,12826); poly link east y 12815-12837 under L6, L7, L8; contact (13736,12826); L9 | L9 at y 13480 (bd1's k15, untraced there) |
| `rdp3_n8` | L8 at y 10700 | L8 to contact (13692,10745); poly west y 10737-10758, down between L1 and L2 (x 13413), west y 10954-10976 | leaves west at (13330,10965) |
| `rdp3_rc_ld` | contact (13690,10815) on RC's strobe poly | L8, jog left at y 12400, L7 | L7 at y 13480 = bd1's k13 = **`sel_w0`** |
| `rdp3_rb_ld` | contact (13648,11571) on RB's strobe poly | L7, jog left at y 12357, L6 | L6 at y 13480 = bd1's k12 = **`sel_w2`** |
| `rdp3_ra_ld` | contact (13823,12700) on RA's strobe poly | L11 | L11 at y 13480; at y 14000 it jogs onto L10 = bd1's k16 = **`sel_w1`** |

Lines that start in the routing zone and go south (their upper ends are in the next
section): L3 from contact (13478,12916), L5 from (13565,12957), L8 from (13692,12870),
L10 from (13780,12785).

Four lines from the north turn west one after another (`rdp3_n8` at y 10965, `rdp3_n6`
at 11440, `rdp3_n5` at 11920, `rdp3_n4` at 12397), towards the mid-right array. What
they are is rdp2's to say.

A poly line crosses the whole bundle along y 13406-13429 without a contact (not drawn
yet: its east end is not followed).

### `c` lines: where they come from

Slice s1 (traced, contact uncertain): a poly line comes from the west along y 11695-11712
in the gap under RB, passes under slice s0's lines and rails (no contact seen at 2.7x), turns down
under s1's c track at x 14310-14333 and ends on a contact to the track at (14322,11750)
(ring in the chip-1 metal shot, pale pad in the clean shot, one view at 4x:
`cache/scratch/rdp3/line_end_ov.png`; `rdp3_cmp` flags exactly this spot as differing
from the other slices). West of x 13760 it is not followed.

The other slices, below the array (first run's "M-tracks", read at 1.15x, not drawn):

| Slice | Contact | Poly line | Left end |
|---|---|---|---|
| s0 | (13930,12565) | not followed | |
| s1 | none in the routing zone (fed from the gap under RB, above); the track also runs straight down through the AR cell at x 14322 and on below it | | |
| s2 | (14703,12960) | y 12958 | beyond x 13700 |
| s3 | (15105,12915) | y 12915 | beyond x 13700 |
| s4 | (15497,12870) | y 12872 | beyond x 13700 |
| s5 | (15880,12828) | y 12828 | contact (14108,12828) and/or (13737,12828), metal going down |
| s6 | (16276,12785) | y 12783 | contact (13782,12783), metal going down |
| s7 | (16665,12458) | y 12455 left to contact (15668,12452), metal link down to (15668,12745), poly y 12743 left | contact (14065,12740), metal going down |

Track scan of the bundle (metal present, y): L3 12936-15101, L4 12930-14901, L8
12908-14880, L9 12866-14944, L10 12807-13877, L11 from 12700. These starts match the
poly lines of the table, so the `c` lines probably come up the bundle; L4's lower end
is on `sel_w4`, which does not fit a counter bit, so some of this is wrong. To be
traced.

## Ports

| Name | Layer | Where | Direction | What |
|---|---|---|---|---|
| `rdp3_bus_s0`..`s7` | metal | x 13845, 14236, 14626, 15016, 15407, 15797, 16187, 16577 at y 10700 | through | data lines, continue north into rdp2 |
| `rdp3_c_s0`..`s7` | metal | x 13931, 14321, 14712, 15102, 15492, 15882, 16272, 16663 at y 10700; drawn down to y 12445 | in (assumed) | compared with RA and RB; continue north, and south into the routing zone |
| `rdp3_rb_ld` | metal | 13652,13480 (track L7) going south | in | load strobe of RB; is `sel_w0` (contact 13652,15000) |
| `rdp3_ra_ld` | metal | 13825,13480 (track L11) going south | in | load strobe of RA; from the gate column at 13776,15155 (bd1) |
| `rdp3_ca_eq` | diffusion | strip y 11776-11798, x 13768-16925 | out | RA = c. Exit not found |
| `rdp3_cb_eq` | diffusion | strip y 10930-10952, x 13768-16925 | out | R0 = c. Exit not found |
| `rdp3_t16837` | metal | 16838,10745 north end not looked at; 16838,12550 going south | through | uses the strap track of slice s7; no contact found in the region |
| `rdp3_ar_ld` | metal | 16285,13080 going down | in | load strobe of row AR (= `areg_load`) |
| `rdp3_ar_s1_q`..`s4_q` | metal, then poly | contacts 15884,13482; 15839,13437; 15884,13392; 15839,13352 | out | `ar0`..`ar3` |
| `rdp3_ar_s5_q` | poly | 16170,13307 going right | out | `ar4` |
| `rdp3_ar_s1_trk` | metal | 14322,13277 going down | through | the s1 `c` line below the AR cell (not joined to `rdp3_c_s1` in the trace: the piece between y 12445 and 13014 is not drawn) |
| `vcc` | metal | x 13990 + 390k (8) at y 10700; x 14382..15942 at y 13520 | - | rails |
| `vss` | metal | x 13783 + 390k (9) at y 10700; 16125,13320 downward | - | rails |
| (not drawn) | metal | x 16808 (poly), 16817, 16860, 16908 going down at about y 12850 | ? | bus s0, s5, s6, s7 leaving bottom right |
| `rdp3_c_s1` | poly | 13760,11704 going west | in (assumed) | feed of slice s1's c line |

## Ambiguities

- **AMB-1 (narrowed, see the hold device above).** Left open: depletion or enhancement
  (not visible), and the strip's two ends.
- **AMB-3, the strap at x 14886 and the piece at x 14673 ("T2").** Each is a piece of
  metal as long as one cell (strap y 12174-12430 in RA; T2 y 11738-12200) with no
  contact found at either end or along it. The first run drew a long contact from the
  strap to q's drain from an outline in the clean shot; removed, because in slice s7 the
  same track carries a through line across band A (seen in metal from RB's cell to RA's,
  `cache/scratch/rdp3/s7_right.png`), which would tie RB's and RA's bit 7 together. Both
  metal shots show the strap dimmer and narrower over y 12290-12345, as they do the c
  track inside the latch cell (y 12285-12400): there the clean shot shows the area was
  protected and a metal-gap line beside it, so the metal is taken as continuous.
  T2 lies over the gate of T6 at y 12121-12145 and over the VSS-tied band at its lower
  end; a contact to either was looked for at 5x and not seen.
- **AMB-4, end of `rdp3_ar_ld`** (first run): contact (16285,13022) seen at 1.5x only.
- **AMB-5, AR track stubs** (first run): whether the c lines of s2..s5 reach the AR
  cells' track pieces. With the c lines now known to be comparator inputs this matters
  only for s1, whose line runs on south.
- **AMB-6, the `c` track inside the latch cell.** Track scan and both metal shots show no
  bright metal on it over y 12281-12408 (RA), and its upper piece seems to end with a
  round bright patch on the latch's n2 land at (14712,12270). Read as continuous with
  no contact (clean shot: protected colours along the whole stretch; a contact to n2
  would tie the n2 nodes of three registers together through the track). The other
  reading (track broken, n2 brought up to the comparator) would change the XOR's
  inputs; a sharper metal photo of 14690-14730 x 12260-12420 would settle it.
- **AMB-7, T7's diffusion** (see Comparator).
- **AMB-8, node x to the series pair.** The strip y 11963-11978 meets the band's right
  end at x 14694-14700 exactly under a metal-gap line (dark bar, as over diffusion;
  over field it would be an olive strip). Taken as joined.

## Not done

- Exit of the two `eq` lines. Checked: both ends of the band-A strip (dead ends, no
  contact, `ma_left.png`, `ma_right.png`, `m_leftend.png`), the gap above the load
  (empty), the foot of the L-shaped part in s2 and s7. Not checked: under each VSS rail
  between slices at more than 3x; where the through line x 16838 crosses the strip
  (16838,11787); the bottom end of the load's gate block (14455-14497 x 11915); band B.
- RA's strobe beyond (13776,15155), i.e. which register RA is.
- Routing zone y 12437-13000 (tables above), the bus lines s0, s6, s7 and all c lines
  below y 12445.
- Left-edge bundle x 13348-13825: only the two strobe tracks are drawn.
- Gap zone y 10831-10925 (under RC): not looked at beyond one 1.2x view. The poly line of
  `rdp3_c_s1` west of x 13760.
- The through line x 16838: both ends.
