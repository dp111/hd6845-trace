# rdp3: right datapath, lower rows

Region: x 13350-16950, y 10700-12900, plus x 13350-15800, y 12900-13480.
Trace: `trace/rdp3.txt`. Scratch: `cache/scratch/rdp3/`.
Own tools: `tools/rdp3_sharp.py` (view.py with an unsharp mask; every junction below was
judged with it at 3-6x on a median composite of the five cells, `--comp r0w`) and
`tools/rdp3_strips.py` (montage of vertical strips, for following per-slice lines).

## Status

- Row AR (above the decode array, y 13010-13280): one latch cell traced as `rdp3_lat`,
  placed five times, every instance checked (cellcheck plus overlays), outputs traced
  to the edge of the region. Extracts as five latch bits, 25 transistors, no errors.
- The same cell, upside down, makes two 8-bit register rows in the array (RA, RB below).
  Found and fitted by overlay, **not placed in the trace**: their strobe lines, outputs
  and the cell edges are not examined yet.
- Per-slice bus lines traced from the bottom of RA to row AR. Routing zone read at 1.15x
  and described below with coordinates, not drawn. The other array rows: surveyed only.

## Inventory

Slices: 8, pitch 390, numbered s0..s7 from the left. Slice sK has its bus line at
x 13845 + 390K and its second track ("M-track") at x 13932 + 390K.

| y | x | What |
|---|---|---|
| 10561-10831 | 13815-16940 | register row RC: third copy of the latch cell (findcell dy -2459). Centre y 10696, so it belongs to rdp2 |
| 10831-10950 | 13780-16900 | gap with horizontal lines |
| 10950-11320 | 13780-16900 | band B2, two sub-rows of other cells (about y 10950-11150 and 11170-11320): not traced |
| 11321-11591 | 13815-16940 | **register row RB**: 8 latch cells upside down |
| 11591-11780 | 13780-16900 | gap; per slice the rails, the bus line and (from y 11740 down) a second thin line at bus + 35 |
| 11780-12167 | 13780-16900 | band B1, two sub-rows of other cells: not traced |
| 12167-12437 | 13815-16940 | **register row RA**: 8 latch cells upside down |
| 12437-13000 | 13700-16950 | routing zone (described below) |
| 13010-13280 | 14140-16160 | **row AR**: 5 latch cells under slices s1..s5 (traced) |
| 13280-13500 | 14450-16300 | the five AR outputs, nested L-shaped lines going right (traced to x 15884) |
| 10700-13480 | 13350-13760 | bundle of about 14 vertical metal lines down the left edge: not traced |

Rails, two per slice, vertical, wide metal: VSS at x 14175 + 390k (60 wide), VCC at
x 14382 + 390k (56 wide). Drawn from y 12437 down. VCC rails run on into the VCC bus of
the decode array (y 13518); VSS rails end at the bottom of row AR (y 13277) except the
one at x 16125, which goes on down and bends left (areg region). Which is which: both
depletion loads of every latch cell hang from a land contacted by the x 14382 + 390k
rail, and both pull-downs have their sources on lands contacted by the other rail; the
x 14382 + 390k rails also join the decode array's VCC bus.

## Logic

### Latch cell `rdp3_lat` (traced), as used in row AR

Master at x 14597-14987, y 13010-13280 (slice s2 of row AR). 5 transistors per cell:

```
a   <- bus      through pass transistor T1 while the strobe is high   (34/28 at 14623,13074)
n2  = NOT a     pull-down T_b 51/22 at 14621,13178; load L2 30/52 at 14732,13126
q   = NOT n2    pull-down T_a 52/22 at 14911,13124; load L1 28/49 at 14822,13086
```

- Bus: vertical metal line, contact at the top of the cell (14622,13035) to a diffusion
  land; the strip from the land passes under the strobe poly (T1) and ends on a buried
  contact to the poly that is T_b's gate (node a).
- Strobe: a poly line along the top edge of the cell row (y 13015-13043). In each cell it
  loops down round the bus contact; the bottom of the loop is T1's gate.
- L2's gate block (14707-14752 x 13100-13152) is one piece of poly with the U-shaped
  line that runs to T_a's gate; it is tied to n2 at the buried contact 14660-14692 x
  13140-13168. L1's gate block (14797-14848 x 13058-13150) is tied to q at 14846-14874 x
  13066-13100; its lower half is a contact pad from which a metal strap goes down to
  the output land (14820-14900 x 13197-13243).
- q is in the same sense as the bus and leaves by a buried contact on the output land
  (14886,13232) onto a poly strip.
- T_a's source is the VSS land of the *next* slice to the right; the last cell of a row
  needs a rail on its right (for AR: x 16125).

As traced the latch is dynamic. A static hold path is expected and is probably the
structure of AMB-1.

### Row AR (traced): 5 bits, believed to be the address register

Instances `ar_s1`..`ar_s5` under array slices s1..s5 (dx -390, 0, 390, 780, 1170).

- Data: `rdp3_bus_s1`..`s5`.
- Strobe `rdp3_ar_ld`: its right end has a contact at (16285,13022) to a thin metal line
  that goes down into the areg region. All five bits load together.
- Outputs `rdp3_ar_sN_q`: poly strip down to a contact at (14886 + dx, 13308), then metal
  down and to the right at y 13481 (s1), 13437 (s2), 13392 (s3), 13352 (s4), with a poly
  cross-under beneath each VCC rail. From contacts at x 15884 / 15839 they continue to
  the right in poly. s5 has no contact: its strip turns right at y 13307 and runs on in
  poly under the x 16125 rail. All five turn down in a bundle at x 16240-16290 (areg).

Believed, not traced: address register (5 bits, on top of the decode array, fed from
the data lines, outputs towards the decode row drivers).

### Register rows RA and RB (found, fitted, not placed)

`findcell` on the latch core finds it mirrored top-to-bottom in three rows of eight.
Ready-made placements (cellcheck against the AR master: median ncc 0.85-0.89, core
identical, differences only along the cell edges; overlay on metal checked for RA s2,
`cache/scratch/rdp3/b1_ovm.png`):

```
# RA, y 12167-12437 (strobe poly y 12404-12432, bus contact y 12412, q leaves upward at y 12215)
@inst rdp3_lat -782,-853 mx=14790 rot=180 o=14790,13150 tag=ra_s0
@inst rdp3_lat -391,-853 mx=14790 rot=180 o=14790,13150 tag=ra_s1
@inst rdp3_lat 0,-853 mx=14790 rot=180 o=14790,13150 tag=ra_s2
@inst rdp3_lat 390,-853 mx=14790 rot=180 o=14790,13150 tag=ra_s3
@inst rdp3_lat 780,-854 mx=14790 rot=180 o=14790,13150 tag=ra_s4
@inst rdp3_lat 1170,-854 mx=14790 rot=180 o=14790,13150 tag=ra_s5
@inst rdp3_lat 1560,-854 mx=14790 rot=180 o=14790,13150 tag=ra_s6
@inst rdp3_lat 1951,-854 mx=14790 rot=180 o=14790,13150 tag=ra_s7
# RB, y 11321-11591: dy -1699 (s4, s6: -1700), same dx. RC (rdp2), y 10561-10831: dy -2459.
```

Before placing them, check: (1) the cell edge that faces up in the array (the AR cell's
bottom: the grounded poly band, the output strip, the ends of the three tracks), where
cellcheck shows differences and a horizontal metal line runs at y 12140-12160; (2) a
difference block near the VCC contact (master 14770-14790 x 13045-13060); (3) the end
slices s0 and s7; (4) where each row's strobe poly ends; (5) where q goes (up into the
sub-rows above, presumably comparators or counters).

Believed: RA, RB (and RC) are 8-bit registers written from the bus lines, each with the
cells it is compared against in the two sub-rows above it.

### Bus lines and bit order

`rdp3_bus_sK` is a thin metal line per slice at x 13845 + 390K. It passes straight
through band B1 (seen continuous on strips of s0, s2, s3, s7 from RB's bus contact at
y 11566 to y 12200) and, for s1..s5, on down to the AR cells (traced, y 12437-13014).

In the routing zone four of the eight leave towards the lower right (read at 1.15x,
not drawn):

| Bus | Path |
|---|---|
| s0 | contact (13843,12503), poly line at y 12503 right to contact (16047,12500), metal down to contact (16047,12822), poly right at y 12825 to x 16808, then down |
| s5 | contact (15797,12738) on the line that also feeds AR, poly right at y 12743 to contact (16817,12743), metal down at x 16817 |
| s6 | contact (16186,12698), poly right at y 12697 to contact (16860,12700), metal down at x 16860 |
| s7 | contact (16580,12568), poly down and right at y 12655 to contact (16908,12653), metal down at x 16908 |
| s1..s4 | no contact in the routing zone; end in the AR cells |

Inference (not traced): the four that leave bottom right go to the lower data pads and
the other four are fed from higher up, so s1..s4 would be D0..D3 in some order, s5 = D4
(the address register needs D0-D4 and uses s1..s5), and s0, s6, s7 = D5..D7 in some
order. To be settled by the dbus / areg traces.

### M-tracks (second per-slice line, x 13932 + 390K)

Thin metal, passes through the latch cells with no contact found. In the routing zone
each ends on a contact to a horizontal poly line that runs left (read at 1.15x, not
drawn):

| Slice | Contact | Poly line | Left end |
|---|---|---|---|
| s0 | (13930,12565) | not followed | |
| s1 | none: the track runs straight down through the AR cell at x 14322 and on below it (seen to y 13340) | | |
| s2 | (14703,12960) | y 12958 | beyond x 13700 |
| s3 | (15105,12915) | y 12915 | beyond x 13700 |
| s4 | (15497,12870) | y 12872 | beyond x 13700 |
| s5 | (15880,12828) | y 12828 | contact (14108,12828) and/or (13737,12828), metal going down |
| s6 | (16276,12785) | y 12783 | contact (13782,12783), metal going down |
| s7 | (16665,12458) | y 12455 left to contact (15668,12452), metal link down to (15668,12745), poly y 12743 left | contact (14065,12740), metal going down |

Whether the y 12743 line is broken under the VSS rail at x 15735 (between the link
contact at 15668 and the s5 bus contact at 15797) was not seen; it must be, or bus s5
and M-track s7 would be one net.

## Ports

| Name | Layer | Where | Direction | What |
|---|---|---|---|---|
| `rdp3_bus_s1`..`s5` | metal | x 14235, 14625, 15015, 15405, 15795 at y 12437 (drawn end; the lines continue up through the array) | into AR | data lines |
| `rdp3_ar_ld` | metal | 16285,13080 going down (areg region) | into the row (assumed) | load strobe of row AR |
| `rdp3_ar_s1_q` | metal, then poly | contact 15884,13482, poly on to the right | out | AR output, slice s1 |
| `rdp3_ar_s2_q` | metal, then poly | contact 15839,13437 | out | slice s2 |
| `rdp3_ar_s3_q` | metal, then poly | contact 15884,13392 | out | slice s3 |
| `rdp3_ar_s4_q` | metal, then poly | contact 15839,13352 | out | slice s4 |
| `rdp3_ar_s5_q` | poly | 16170,13307 going right | out | slice s5 |
| `rdp3_ar_s1_trk` | metal | 14322,13277 going down; same line comes from the array at 14322,13014 | through | M-track of slice s1 |
| `vcc` | metal | x 14382, 14772, 15162, 15552, 15942 at y 13520 (decode VCC bus) and at y 12437 upward | - | rails |
| `vss` | metal | x 14175 ... 16125 (390 apart) at y 12437 upward; 16125,13320 downward | - | rails |
| (not drawn) | metal | x 16808 (poly), 16817, 16860, 16908 going down at about y 12850 | ? | bus s0, s5, s6, s7 leaving bottom right |
| (not drawn) | metal | x 13737, 13782, 14065, 14108 going down at about y 12850; poly lines y 12872, 12915, 12958 leaving left at x 13700 | out (assumed) | M-tracks s5, s6, s7, s4, s3, s2 |

## Ambiguities

- **AMB-1, hold path of the latch (14700-14820 x 13205-13275).** Node a's gate poly runs
  on from T_b to a buried contact on a small land under the M-track (14680-14724 x
  13214-13244). From there towards the output land (14820-14868 x 13197-13243), under the
  VCC rail, lie three parallel stripes: S1 y 13208-13220, pale like diffusion; S2
  y 13226-13245, salmon like poly; S3 y 13251-13272, poly: the band along the cell
  edge, which has a contact to the VSS rail at (14562,13256) and ends at x 14809.
  Readings: (a) S2 gates a long weak (depletion) device between the two lands, a
  resistive q -> a feedback that the bus overpowers while the strobe is high; (b) S1
  is a plain diffusion link a = q; (c) S1/S2 form a capacitor on node a. In the gap
  between the VCC rail and the strap (x 14811-14820) the photo shows field beside S1
  and something continuous beside S2. Drawn: S1 as uncertain diffusion on node a, S2 as
  an unconnected poly (`rdp3_<tag>_x2`), no device. Working assumption: static by (a).
  Would settle it: a sharper photo of 14720-14825 x 13200-13250.
- **AMB-2, the grounded poly band S3.** The contact to the VSS rail is clear; nothing was
  seen crossing the band. Possibly the gate of the AMB-1 device.
- **AMB-3, track contacts inside the latch cell.** No contact pad or pit was seen where
  the M-track (x 14712) and the x 14886 track cross the strobe poly or end, so none is
  drawn; a contact to the strobe would short the five AR bits. The x 14886 track lies
  along q's drain (outline of a long contact at 14886,13130, drawn uncertain, harmless).
  The M-track may touch n2 at (14712,13172) (pale patch in the chip-2 stripped shot):
  not drawn, and unlikely given that the same track passes three register rows.
- **AMB-4, end of `rdp3_ar_ld`.** Contact (16285,13022) and the metal below it are drawn
  uncertain: seen at 1.5x only, and inside the areg region.
- **AMB-5, upper end of the AR track stubs.** For s2..s5 the M-track ends on its
  routing-zone contact (y 12828-12960) and the AR cell's piece of the track
  (`rdp3_ar_sN_trk`, from y 13014) looks separate (plain field between at 0.7x). For s1
  the track is continuous. Not checked at higher zoom.

## Not done

- Place and verify RA and RB (list above), their strobes and outputs.
- The four sub-rows of other cells: y 10950-11150, 11170-11320 (band B2) and
  y 11780-11980, 11980-12167 (band B1), 8 slices each.
- Routing zone y 12437-13000: horizontal poly lines at y 12455, 12503, 12655, 12697,
  12743, 12783, 12828, 12872, 12915, 12958 with the contacts listed above; the wide
  diagonal metals at x 16000-16900; the thin vertical at (16601,12755-12827).
- Left-edge bundle x 13350-13760 and everything left of x 14140 below y 12900.
- Bus lines s0, s6, s7 below RA, and all bus lines above y 12437 (seen, not drawn).
