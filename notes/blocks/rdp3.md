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

## Status

- Traced, placed and checked: the address register row AR (5 latches), the two 8-bit
  register rows RA and RB (16 latches), and under each of them a full 8-bit equality
  comparator (per slice an XOR of the register bit with a per-slice line `c`, and a
  pull-down on a row-wide wired-NOR line with one load). 256 transistors, extracts
  with no errors and no open nets.
- Both load strobes traced to the edge of the region. RB's is `sel_w0` (followed to
  sel's port): **RB is R0**. RA's comes from a gate in the logic column west of the
  select gates (package bd1), not directly from `sel`: RA is not identified.
- Not traced: where the two `eq` lines leave (not found), the routing zone, the
  left-edge bundle, the gap zones between the bands.

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
| 10831-10925 | gap: RC's strobe poly at y 10800-10830, otherwise not looked at |
| 10925-11056 | band B match pull-downs (`rdp3_mpd`), `rdp3_cb_eq` strip at y 10930-10952 |
| 11056-11321 | band B XOR cells (`rdp3_xor`) |
| 11321-11591 | **register row RB = R0** (`rdp3_lat` upside down), strobe poly y 11558-11586 |
| 11591-11775 | gap: empty field except a poly line at y 11695-11712 from the west to slice s1 (the feed of `rdp3_c_s1`, see "c lines") and the rounded top ends of the T2 pieces at y 11738 |
| 11775-11905 | band A match pull-downs, `rdp3_ca_eq` strip at y 11776-11798 |
| 11905-12167 | band A XOR cells |
| 12167-12437 | **register row RA** (`rdp3_lat` upside down), strobe poly y 12404-12432 |
| 12437-13000 | routing zone (read at low zoom by the first run, table below; not drawn) |
| 13010-13280 | **row AR**: 5 latch cells under slices s1..s5 |
| 13280-13500 | the five AR outputs, nested L-shaped lines going right |

Left of the array, x 13348-13825: a bundle of 12 vertical metal tracks on a 43.4 px
pitch, L0..L11 at x 13348 + 43.4 k. What is known of them is under Ports.

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
  (13823,12700); thin metal on bundle track L11 (x 13825) goes down from there.
- Strobe `rdp3_rb_ld`: row poly; right end free; runs on west to a pad with a contact
  at (13648,11571); metal on track L7 (x 13652) goes down, straight.
- Which registers (followed outside the region by track scan `tools/sel_tracks.py` and
  two views, `cache/scratch/rdp3/sel_west.png`, `sel_west2.png`):
  - L7 is continuous metal from y 11566 to a contact at (13652,15000) on the poly bar
    y 15001, which is `sel_w0` at sel's west port (14100,15001). **RB = R0.**
  - L11 runs to y 14975, steps left to x 13784 and enters the gate column at
    x 13700-13990, y 15100-16400 (contact seen at about 13776,15155). That logic is
    untraced (bd1). So RA's strobe is made there. RA is compared with the same `c`
    lines as R0 and has 8 bits; not identified further.
  - For the record, the other west outputs of sel: `sel_w1` to L10 (contact 13782,14912;
    L10's metal from there up ends at y 13994, the piece above, y 12807-13877, is
    another net); `sel_w2` to L6 (contact 13608,14957), which runs up, steps onto L7's
    track above RB's contact (y 11500-11520) and continues north into rdp2; `sel_w4` to
    L4 (contact 13520,15040; metal up to y 12930); `sel_w6` (bar y 14867) passes under
    the whole bundle westward. The west part of bar y 14909 (west of x 13712) is not
    `sel_w1`: it starts on a contact at (13692,14912) on L8.

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

Believed: the `c` lines are the bits of the horizontal character counter (R0 is
compared with them) and `rdp3_cb_eq` is "counter = R0".

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
