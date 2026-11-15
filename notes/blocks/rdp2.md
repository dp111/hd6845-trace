# rdp2: right datapath, middle rows

Region: x 13350-16950, y 8100-10700. Trace: `trace/rdp2.txt` (`@requires rdp3`).
Scratch: `cache/scratch/rdp2/`. No own tools; `tools/rdp3_cmp.py` and
`tools/rdp3_strips.py` did the comparing and line following.

**Slice tags and array columns.** Tags are rdp3's: s0..s7 from the left, pitch 390. The
cells of slice sK lie between the VSS rail at x 13783 + 390 K (left edge; the slice's own
pull-downs use the land under this rail) and the one at x 14174 + 390 K. Taking a column's
rail to be the one at its left edge, **sK = column c(K-1)**: s1..s7 are c0..c6 (rails
x 14174..16516), **s0 lies one pitch left of c0** (rail x 13783), and c7 (rail x 16906,
the ninth rail) has no cells in the rows traced here.
Believed bit order (see Logic, comparator D): s1..s7 = bits 0..6, s0 = bit 7, i.e. column
cN = bit N and bit 7 sits left of c0.

## Status

- Traced, placed, every instance checked, extracts with no errors and no open nets
  (170 transistors of this block): register row RC (8 latches) = **R0**; comparator C
  above it (8 XORs, wired NOR) = "c = R0"; comparator D above that (7 XORs, wired NOR),
  which compares c of each slice with the R0 bit of the next slice = "c = R0 shifted by
  one bit"; the wiring between them; both equality lines out to bundle tracks at the
  left edge; R0 bit 7's line round the array.
- **Nothing in this block drives the `c` lines.** Each c track ends at its topmost
  comparator contact (s1..s7 at y 9723 in comparator D, s0 at y 10244 in comparator C).
  They are fed from rdp3's side (routing zone below row RA).
- Not traced: everything above y 9440 (routing zone y 9000-9560, the seven-slice array
  y 8048-9080), the other lines of the s0 column and of the left bundle.

## Inventory

Per slice sK (x for s2; add 390 per slice), as in rdp3: VSS rail 14565, bus 14626, T2
track 14673, c track 14712, VCC rail 14772, strap track 14886 (in s7 a through line,
x 16838).

| y | What |
|---|---|
| 8048-8318 | latch row, 7 cells, centres x 13620 + 390 k (k = 0..6): one pitch left of s0 up to s5. `findcell` only (score 0.7), not looked at |
| 8415-8806 | comparator cells (`rdp3_mpd` centres y 8480, `rdp3_xor` centres y 8675), x centres 13966..15918 (six, score 0.87-0.90) and a weak one at 13576. `findcell` only |
| 8807-9077 | latch row, 7 cells, same x as the first. `findcell` only |
| 9000-9560 | routing zone: many horizontal poly lines; seen only at 0.35x except the two lines traced (below) |
| 9563-9954 | **comparator D**, slices s1..s7: `rdp3_mpd1` (s1, with the load) / `rdp3_mpd` at y 9563-9692, `rdp2_xor` at y 9692-9954 |
| 9440-10084, x 13800-14180 | s0 has no comparator D cell: routing column (poly bars from the bundle to tracks going north), see Not done |
| 9954-10084 | gap: T2 top contacts (y 10010) and poly bars to the XORs of comparator D; exit line of comparator C (y 10000-10021, s0) |
| 10084-10475 | **comparator C**, slices s0..s7: `rdp3_mpd1` (s0, with the load) / `rdp3_mpd` at y 10084-10213, `rdp2_xor` at y 10213-10475 |
| 10475-10564 | gap: q of RC up into the XORs, bar and contact to the T2 track (y 10529) |
| 10564-10834 | **register row RC = R0**: `rdp3_lat` upside down, eight copies; strobe poly y 10801-10829 |

Left of the array, x 13348-13782: the bundle L0..L8 (x 13348 + 43.4 k), continued from
rdp3. Top ends of its lines inside this region are under Not done.

## Logic

### Row RC = R0 (traced)

`@inst rdp3_lat` at dx -781, -391, 0, 390, 780, 1170, 1561, 1951, dy -2456 (rdp3's mirror
and rotation). Compared copy by copy with row RB (`rdp3_cmp`, offset 0,-757): identical
except the top edge, where q leaves. Per bit, as rdp3: `a <- bus` while the strobe is
high, `n2 = NOT a`, `q = NOT n2`, weak hold device q -> a. q is in the sense of the bus.

- Bus lines `rdp3_bus_s0..s7` (one contact per cell, y 10809). s0's bus line ends at the
  top of its RC cell (y 10567); the others run on north through both comparators with no
  contact.
- **Strobe: `rdp3_rc_ld` = `sel_w0`, so RC is R0.** The row poly runs west under the first
  VSS rail to a pad with a contact at (13690,10815) on bundle track L8 (x 13694), metal
  south. Followed outside the region: L8 straight to y 12400, there one step left onto
  x 13652 (both metal shots, `jog.png`: the three tracks L6, L7, L8 each step one place
  left at y 12310, 12355, 12400), straight on to the contact at (13652,15000)
  (`l8_a.png`, `l8_b.png`, `l8_c.png`), which sel and bd1 give as `sel_w0`. rdp3's run 3
  found the same independently and draws pad, contact and track (its file names the net).
  By the same staircase RB's strobe (contact 13648,11571 on x 13652) lands on x 13608 =
  `sel_w2`: rdp3's earlier "RB = R0" came from a track scan that bridged the 25 px
  between the two steps.

### XOR cell `rdp2_xor` (rdp3's cell, traced there)

Text copy of `rdp3_xor` less its metal piece on the T2 track, which is absent in
comparator D and in s1 of comparator C and is a real wire elsewhere in C. Master at
comparator C, slice s2.

```
nor = NOR(c, q)          x = NOT(nor + c.q) = c XOR q
```

c from the slice's c track (contacts at y 10244 and 10429 in C; 9723 and 9908 in D); q in
poly from below at x 14879-14901 (s2).

### Comparator C (traced): c = R0

```
rdp2_cc_sK_x = c_sK XOR R0_sK        K = 0..7
rdp2_cc_eq   = NOR(rdp2_cc_s0_x .. rdp2_cc_s7_x)      high when the eight c lines equal R0
```

- The cells are band A's moved by (dx,-1692/-1691); all eight XORs and the seven plain
  pull-downs compared with the median of bands A, C, D by `rdp3_cmp`: no difference
  except where a metal line is missing (s1 has no T2 track, s0 no bus line here).
- The load of the eq line (`rdp3_mpd1`) is in **s0** (rdp3's bands have it in s1).
- q of each RC cell comes up in poly through the 89 px gap (x 14879-14901, y 10500-10600)
  into the XOR.
- eq strip: diffusion y 10084-10106, x 13768-16925. **Exit** (`eqc_left.png`,
  `c_s0_top.png`, `eqc_tab.png`): a tab comes up at x 13924-13946, buried contact
  (13922-13948 x 10052-10074) onto poly that goes up to y 10000-10021 and west under the
  first VSS rail and the bundle to a pad with a contact at (13434,10012) on **track L2**;
  metal south. rdp3 draws L2 on from y 10700 as `rdp3_n2s1` (jog onto L1 at y 12486, bd1's
  k7 at y 13480).

### Comparator D (traced): c against R0 shifted one slice

```
rdp2_cd_sK_x = c_sK XOR R0_s(K+1)    K = 1..6
rdp2_cd_s7_x = c_s7 XOR R0_s0
rdp2_cd_eq   = NOR(rdp2_cd_s1_x .. rdp2_cd_s7_x)
```

- Seven slices, s1..s7; cells are band A's moved by (dx,-2213/-2212), compared as above:
  differences only on the T2 and c track columns, where the metal is absent.
- The load of the eq line is in s1. Right end as in rdp3's bands (VSS lands under the
  ninth rail; seen at 1.3x and 2x).
- **Where q comes from** (`gap1_s2.png`, `gap2_s2.png`, `bar1_*.png`, `bar2_*.png`,
  `ov_mid.png`): in the gap under comparator C a poly bar (y 10520-10538) takes q of RC
  left to a pad with a contact (y 10529) on the slice's T2 track. The track runs up
  through comparator C and ends on a contact at y 10010; from that pad a poly bar
  (y 10001-10019) runs left, under the VSS rail, and turns up into the q input of the
  XOR of the slice to the **left**. Slices s2..s7 have this; s1 has no T2 track and no
  bar (R0_s1 goes only to comparator C).
- **s0's bit goes round the array** (`s0_d.png`, `t2s0_top.png`, `q0_strips_*.png`,
  `hq_0..2.png`, `east2a/b.png`, `ov_right.png`): s0's T2 track runs on up to a pad at
  (13910,9708); poly north (x 13911-13924) to y 9480, east along y 9480-9494 under every
  rail and track of the array, south at x 16946-16964 (right of the ninth rail) to
  y 10020, west along y 10000-10020 under the ninth rail into the q input of s7's XOR.
- eq strip: diffusion y 9563-9585, x 14158-16925. **Exit** (`eqd_exit.png`,
  `eqd_tab.png`, `ov_s0s1.png`, `pads_l0l2.png`): in s1 a tab of the strip comes up into a
  buried-contact box (14308-14347 x 9518-9560) on the east end of a poly line: west along
  y 9523-9541 to x 13950, south (x 13950-13963) to y 9845, west along y 9828-9845 to a
  pad with a contact at (13346,9837) on **track L0**; metal south. rdp3 draws L0 on from
  y 10700 as `rdp3_n0` (straight to y 12789, steps left to x 13307, leaves at 13307,12850).

Believed: the pairing is a one-bit shift, so the bits ascend s1, s2, .., s7, s0, and
`rdp2_cd_eq` is "c[6:0] = R0[7:1]", i.e. c = R0/2 with **bit 7 of c (slice s0) not
compared**. This fits the CPC document's "VSYNC on C0 = R0/2" for interlace and rdp3's
guess that the address register (slices s1..s5) takes D0..D4. If c is the horizontal
counter, `rdp2_cc_eq` is end of line. Not traced: which slice is which data bit.

## Ports

| Name | Layer | Where | Direction | What |
|---|---|---|---|---|
| `rdp3_bus_s1`..`s7` | metal | x 14236, 14626, 15016, 15407, 15797, 16187, 16577 at y 9540, going north | through | data lines; drawn to y 9540, they go on north (track scan: to about y 9480 and beyond in places) |
| `rdp3_bus_s0` | metal | ends at (13845,10567) | - | top end of s0's data line |
| `rdp3_c_s0`..`s7` | metal | joined to rdp3's at y 10700 (x 13931, 14321, 14712, 15102, 15492, 15882, 16272, 16663) | in | compared with R0; not driven here; top ends y 10220 (s0), 9705 (others) |
| `rdp3_rc_ld` | poly | (13750,10815) going west to rdp3's pad | in | R0 load strobe = `sel_w0` |
| `rdp2_cc_eq` (= `rdp3_n2s1`) | metal | 13434,10700 going south (track L2) | out | high when c = R0 |
| `rdp2_cd_eq` (= `rdp3_n0`) | metal | 13348,10700 going south (track L0) | out | high when c_s1..s7 = R0_s2..s7,s0 |
| `rdp3_t16837` | metal | 16838,9440 going north | through | thin line on s7's strap track, no contact seen in comparators C, D or row RC |
| `vss` | metal | x 13783 + 390k (9) at y 9540 | - | rails, go on north |
| `vcc` | metal | x 13990 + 390k (8) at y 9540 | - | rails, go on north |

`rdp3_rc_s0_q` (R0 bit of slice s0) leaves the region for 14 px at (16950-16964, 9480 to
10020) and comes back; nothing else is on it out there as far as seen (`east1.png`).

## Ambiguities

- **Correction to rdp3 run 2 (already made by its run 3):** RB is R2, not R0; R0 is RC.
  `trace/zz_joins.txt` still has `@alias sel_w0 rdp3_rb_ld`, which is wrong: `sel_w0`
  is `rdp3_rc_ld`, `sel_w2` is `rdp3_rb_ld`.
- **AMB-1, buried contact of comparator D's exit** (14308-14347 x 9518-9560). Larger than
  the ones in the other three bands (38 x 40 against 26 x 22) and the poly reaches it
  straight from the west instead of from above. No metal over it in either metal shot,
  heavy outline, lighter inside, directly on the tab above the strip: read as a buried
  contact. If it were not one, comparator D's line would have no exit.
- **AMB-2, right-end VSS lands** of both comparators (16886-16940 x 10398-10475 and
  x 9877-9954) and of RC (16878-16926 x 10659-10744): placed where rdp3's bands have
  them; seen as tan areas with contact specks at 1.3x and 2x, not at tracing zoom.
- **AMB-3, the through line x 16838** lies over the q input poly of s7's XORs for its
  whole length. No contact ring seen at 2x (`ov_right.png`); not looked at closer.
- Inherited from rdp3's cells: its AMB-1 (hold device), AMB-7 (T7's diffusion, `?D`),
  AMB-8.

## Not done

- **Routing zone y 9000-9560** (all slices) and the **seven-slice array y 8048-9080**
  (findcell hits in Inventory; its cells sit one pitch further left than rdp3's
  slices). Not surveyed beyond `sv_metal.png` (0.35x).
- **s0 routing column, x 13800-14180, y 9440-10084** (`s0_d.png`, `bundle1.png`,
  `ov_s0s1.png`). Poly bars come in from the west under the first VSS rail; seen, not
  drawn:
  - y 9612-9630: from a contact at (13563,9616) on L5's top end to a pad with a contact
    at (13850,9620); metal hooks right and goes north on the T2 track position
    (x 13890; track scan: metal y 9398-9629).
  - y 9872-9888 ("P3"): from west of x 13330 to a pad with a contact at (14065,9877);
    metal north on a track at x 14062.
  - y 9958-9975 ("P4"): from the south-west (diagonal at x 13330-13405) to a pad with a
    contact at (14105,9965); metal north on the strap track x 14105 (scan: y 9264-9952).
  - a bar at y 9573 from a contact at about (13455,9573) east through the column;
    a bar at y 9525 from L6's top contact (13607,9528) east to x 13786, then north.
- **Left bundle, x 13330-13782, y 9440-10700**: only L0 and L2 south of their pads are
  drawn. Seen at 1.28x (`bundle1.png`), coordinates approximate: L3 (`rdp3_cb_eq`) ends on
  a contact at (13475,9705), poly west along y 9705; L2's piece from the north ends at
  (13433,9922), poly bar y 9915-9932 east to a contact at (13649,9919), which is the top
  of L7 south (`rdp3_n7s9`); L7's piece y 9593-9733 ends on a contact at (13649,9747),
  poly west along y 9745; L8's top contact at (13691,9485); L0's upper piece
  (y 9396-9646) and L2's top end share a poly bar at y 9661 that goes west. Track scan of
  all twelve (gap 8) is in the run's log, not kept.
- The upper pad (13692,10748) on L8 is in rdp3's file (`rdp3_n8`).
- Which slice is which data bit (needs the data bus followed to the D pads).
