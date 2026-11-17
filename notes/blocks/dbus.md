# Data bus interface column (`dbus`)

Region: x 17050-17700, y 5300-17000, and the D0-D7 pad cells to its right.
Trace: `trace/dbus.txt` (the column beside the pads) and `trace/dbus_h.txt` (bits 4-7 and
`dlat_en`'s driver). Scratch tools: `tools/dbus_mosaic.py` (the same rectangle at
several offsets side by side, for comparing repeats), `tools/dbus_autocorr.py`
(vertical pitch of a strip).

## Status (2026-11-17 14:13 +0000, contributor session; independently reviewed: the clusters in Round 1, buffers 6 and 7 with their input lines and the inverter below them in Round 2, the rest (cluster 2, latch copies D5/D6, the eight data-line joins) in Round 3; see Review)

Traced, extracting, overlay-checked: the input buffer chain (four inverters) as cell
`dbus_in`, placed **eight times** (D0-D5 upright; **D6 and D7 upside down in the lower
part of the column**, y 15157-15757 and 15786-16386); the input line of D0 from where it
enters the column, and the whole input lines of D1, **D6 and D7** from the pad cells'
contacts; **the gate group ("cluster") under each of chains 0-3: a transparent data input
latch and the driver of the internal data line**, cells `dbus_lat` and `dbus_drv`, 12
transistors per bit, placed four times (48 transistors); and **the inverter below chain 7**
(`dbus_n9`, 2 transistors), whose output is on the thin metal between the rails.
Data lines 0-3 (`db_b0` ... `db_b3`, drawn into the
units by `dbl`) are thereby joined to the pins D0-D3 (D0 and D1 by traced input lines from their pads;
D2 and D3 by the chains' position, see Ambiguities): line k = `dk_lat` = the level of
pin Dk while `dlat_en` is high, held while it is low. One buried contact per bit (the tie
of `dk_lat`'s load gate) is drawn `?`: see Ambiguities.

The clusters hold **no output path**: nothing in them has a data line as an input, and
the thin metal through them (a pad driver line, `P_y`) has no contact there.

Chains 4 and 5 have no cluster below them: their outputs `d4_d` and `d5_d` leave the
wiring field to the west on a metal each (x 17250 from (17249,14304) up to a pad
(17206,13999); x 17252 from (17250,15060) up and west to a pad (17161,14693)), drawn here,
and go on as poly rows to the latch cells of D4 and D5 in the column x 16480-16800, where
the latches and bus drivers of bits 4-7 are (the section Bits 4-7 below). Chains 6 and 7 have
none either: `d6_d` and `d7_d` leave their top gates (G4) in poly to the west, as the
input rows of the latch cells of D6 and D7 there.

Surveyed, with coordinates below, but NOT traced: the logic above D0, the capacitor taps
of chains 1-7, the channel wiring of the pad driver lines. `dlat_en`'s driver is traced: see
the section Bits 4-7 below. The pad cell (AMB-003) was not
attempted; what the column tells us about its two lines is under "P_x and P_y" below.

## Inventory

The column is not one unit per pad at the pad pitch. Logic occupies y 8030-16600
only; between y 5900 and 8030 there are just the rails and three metal lines coming
down from the D0 pad cell. Gates sit on a 152 px vertical pitch between two rails:

- VSS rail, metal, x 17355-17400 (pull-down diffusions under it; further up it joins
  a wide trunk at y 6620-6720).
- VCC rail, metal, x 17527-17585, top end at y 8287, bottom end about y 17000 where
  it joins a wide horizontal metal (y 16960-17010).
- Loads between the rails at x 17420-17520; gate outputs leave to the left in poly.
- Which rail is which comes from the orientation of the loads (every load's far end
  contacts the right-hand rail); neither rail was followed to a pad.
- Left of the VSS rail (x 17050-17300) is a wiring field. From unit 1 downward it
  carries five vertical metal lines (x about 17075, 17120, 17165, 17207, 17252).

| What | Where | State |
|---|---|---|
| Input chain, D0 | 17255-17590 x 8280-8880 | cell `dbus_in`, traced |
| Input chain, D1-D5 | same cell at (1,1365) (1,2732) (2,4098) (2,5465) (2,6223) | placed; findcell on the clean shot scores 0.81-0.83, each overlay checked at 1.25x. The four-gate core is the same in all six; the wiring left of x 17290 differs per copy: drawn for D0-D3 (their `d_d`/`lat_n` polys into the clusters) and for D4, D5 (the `d4_d`/`d5_d` metals to the latches of bits 4-7) |
| Capacitor rectangles of chain 0 | 16960-17040 x 8445-8580 and x 8745-8880 | drawn |
| Cluster 0 (D0) | 17150-17590 x 8885-9520 | traced: `dbus_lat` upside down (mirror line y 9826.5) and `dbus_drv` at (0,-1368) |
| Clusters 1-3 (D1-D3) | 17150-17590 x 10250-10890, and the same at (1,1365), (1,2733) | traced: `dbus_lat` + `dbus_drv`, master = D1's. Clusters 1-3 are copies of each other (findcell 0.88, 0.85; cellcheck median ncc 0.96-0.97); cluster 0 is **not** a copy of them (findcell finds nothing above 0.4): its inverter-and-latch part is the same cell turned upside down (cellcheck ncc 0.94 on the clean shot, 0.91 on metal), its driver the same cell the right way up, and the wiring between the two differs |
| Cross-unders between units 0 and 1 | poly "line 1" y 9545-9566, "line 2" y 9590-9610, both under both rails | line 1 drawn (D1 input); line 2 is D1's P_y, not drawn |
| Input chain, D6 | 17255-17590 x 15157-15757 | cell `dbus_in` mirrored about a horizontal line (`my=8580`, offset (3,6877)): G4 at the top, G1 at the bottom. findcell on the clean shot 0.87; overlay `cache/scratch/dbl67/c6.png` at 2x in two shots, every item within about 5 px |
| Input chain, D7 | 17255-17590 x 15786-16386 | the same, offset (3,7506); findcell 0.81; overlay `c7.png` |
| Inverter `dbus_n9` | 17250-17590 x 16400-16600 | traced, 2 transistors; its load's tie `?` |
| Below y 16600 | - | no more gates: the VSS rail ends at y 16550, the VCC rail at y 17020; the two input lines of D6 and D7 cross here (y 16669 and 16711) |
| Logic above D0 | 17200-17700 x 5250-5900 | several gates, not looked at |

The lower part of the column (y 15100-16600) is therefore nine gates: the four
inverters of chain 6, the four of chain 7, and `dbus_n9`. (findcell in the upright
orientation finds no seventh or eighth copy; with the orientations `m0,180,m180` it finds
both.)

## Logic

### Input chain `dbus_in` (traced)

Four inverters in series, the same arrangement as the R/W, RS and CS input buffers
in the bottom row (`rw_a`..`rw_d`). For chain n:

    dN_a = NOT dN_in      (G1, y 8287-8425 in chain 0)
    dN_b = NOT dN_a       (G2, y 8436-8568)
    dN_c = NOT dN_b       (G3, y 8588-8720)
    dN_d = NOT dN_c       (G4, y 8742-8870)

- `d0_in` is the line from the D0 pad cell (Ports). Traced into G1.
- `d1_in` is traced from the D1 pad cell's contact into chain 1's G1, so chain 1 is
  D1's; `d6_in` and `d7_in` likewise (below). Chains 2-5 are tagged by position and
  *assumed* to follow the pad order.
- `d0_b` and `d0_c` each run left in poly to a metal contact next to a plain
  diffusion rectangle (the "added capacitance" rectangles of the bottom row). The
  strap from `d0_c`'s contact (17078,8795) to its rectangle (contact 16990,8787) is
  there. The strap for `d0_b` (contacts 17078,8490 and 16988,8468) is absent in both
  metal shots: each contact carries only a dot of metal. They are NOT bus lines.
- Only `dN_d`, the pad level delayed by four inverters, feeds logic. `d0_d` leaves G4
  in poly to a contact at 17205,8837 and goes down in metal (x 17198-17218, "M_a")
  into cluster 0, ending at a contact at 17207,9255.
- G1's gate poly continues into an L (17413-17503 x 8292-8318) that crosses no
  diffusion and ends beside the load, as on the bottom-row input inverters (AMB-004).

In chains 1-5 the b and c lines also run left (for chain 1: `d1_b` up at x 17225-17245
to y 9750 and left along y 9740-9760; `d1_c` left to x 17165 and down), presumably
to their capacitors; not followed.

### Input lines of D6 and D7 (traced; images in `cache/scratch/dbl67/`)

Both chains stand upside down, so their inputs are at the bottom and the lines come up
from below the column.

| Line | Route | Seen |
|---|---|---|
| `d6_in` | contact (17838,16515) at the foot of the metal that comes down from the contact column of the D6 pad cell's protection structure (the same arrangement as D1's contact at (17835,8405), `p16.png`); poly west along y 16505-16525 under a wide metal, south x 17655-17675, west along y 16658-16680 under the `P_x` metal and the VCC rail (no contact) to a pad (17290,16668); metal north x 17290-17306 beside chain 7, crossing chain 7's poly lines (uniform width, no pad), west at y 15890, north x 17246-17262 to the pad (17253,15693) of G1's gate band | `e6.png` 2.1x, `x67.png` 2x three shots, `e67.png` 2.4x, `m7b.png` 2.9x and `m7.png` 5x three shots, `i67.png` 3.8x; `tools/follow.py` stops at the box (17300-17322 x 16478-16500) from both sides (S from 16390 ends at 16476, N from 16600 at 16516): that stretch is `?M` |
| `d7_in` | contact (17830,17490) at the head of the metal that goes down into the contact column of the D7 pad cell's protection structure (`d7c.png`); poly west along y 17480-17500 to a contact (17555,17487); metal north x 17548-17565 to a pad (17560,17122); poly north x 17528-17550 under a thin horizontal metal (y 17068-17090, no contact) and under the VCC rail to y 16711; west along y 16700-16722 to a pad (17255,16715); metal north x 17246-17262 to the pad (17253,16322) of G1's gate band | `d7b.png` 1.9x, `d7a.png` 2.7x three shots, `x67.png`, `e67.png`, `i67.png`; follow.py from (17255,16370) south: one piece to (17254,16716); overlay `o4.png` |

So D6's protection column is entered from its lower end and D7's from its upper end. As
for D1, "the pad cell's contact" is where tracing stops: the pad cell itself is AMB-003.

### Inverter `dbus_n9` (traced; `g9.png`, `g9w.png`, `g9e.png`, overlay `o2.png`)

    dbus_n9 = NOT dbus_n9_in

- Pull-down under the VSS rail: diffusion x 17352-17400, VSS contact (17375,16417), gate
  = a poly row y 16441-16463 that arrives from the west (at 0.8x it starts at a pad near
  (16990,16450); not followed) and ends rounded at x 17419.
- Node: under the rail y 16466-16497, east along y 16474-16497 to a vertical strip
  x 17445-17468 (y 16425-16590) whose south end is a pad with **the end contact of the
  thin metal** (17447,16565). Depletion load: gate block 17475-17525 x 16452-16518 over
  the strip y 16474-16499 to the VCC land (contact (17555,16475)); its tie is a
  heavy-outlined box 17470-17500 x 16420-16447 at the head of the vertical strip (`?`).
- The node also has a stub west (y 16480-16500) to a heavy-outlined box
  17300-17322 x 16478-16500 beside `d6_in`'s metal: see Ambiguities.
- Believed: this inverter drives a pad driver line. The thin metal looks continuous in a
  1x strip of the whole column (`thin.png`) up to its corner at y 8097, where the first pass of
  this block found it to be D0's `P_y`; it was not followed at a zoom that would show a break or a tap, so
  "`dbus_n9` = D0's `P_y`" is not claimed. The five inverters in the lower part of the
  column of bits 4-7 (x 16480-16800) have their pads on the metals of the wiring field that carry the other
  pad driver lines; together these may be the output stage of the read path.

### Data input latch and bus driver (`dbus_lat`, `dbus_drv`; traced)

Twelve transistors per bit. For bit n (extracted equations):

    dn_d_n  = NOT dn_d
    dn_lat_n = NOT( dn_d   . dlat_en + dn_lat   )
    dn_lat   = NOT( dn_d_n . dlat_en + dn_lat_n )
    data line n = NOT dn_lat_n

- A transparent latch: while `dlat_en` is high `dn_lat` = `dn_d` (the pad level through
  the four inverters) and the data line follows the pin; while `dlat_en` is low the two
  cross-coupled AND-OR-invert gates hold. The data line is driven all the time, by a wide
  pull-down (W/L 85/20, gate `dn_lat_n`) against a strong load (about 68/27; its width was corrected by the independent review):
  **data flows from the pin to the data line only**. The clusters contain no gate with a
  data line as input and no connection to the pad driver lines, so the lines 0-3 that
  `bust` calls the data bus are a write bus as far as these units go; a read path, if
  the chip has one for these bits, is elsewhere (the pad driver lines `P_y` come up the
  column from below).
- `dlat_en` (the first pass's "M_b") is the only control line: one metal, x 17243-17262,
  from its top contact in cluster 0 (17252,8990) down to y 13613, with two contacts per
  cluster (the two series gates). There it turns west to a contact (17166,13611), goes
  on in poly to a contact (16986,13608) and in metal west and down x 16860; this file
  draws it to y 13650 and `trace/dbus_h.txt` from there: down past the latch cells of D4-D7
  (two contacts in each) and on to its driver, a NOR gate with `cs_d` as one input
  (the section Bits 4-7 below): `dlat_en = NOR(cs_d, dbh_dlat_in_b)`.

Layout, in the master's coordinates (cluster 1; clean shot unless said):

| What | Where | Notes |
|---|---|---|
| Diffusion column under the VSS rail | x 17347-17395 (17325-17395 at y 10372-10500) | VSS 10338-10385 (C 17368,10362) / `d_d` band 10390-10410 / `dlat_en` band 10433-10455 / `lat_n` 10457-10515 / `lat` band 10522-10545 / VSS 10548-10595 (C 17368,10565) / field / `lat` 10608-10645 / `dlat_en` band 10648-10670 / `d_d_n` band 10693-10715 / VSS 10720-10770 (C 17368,10745) / `lat_n` band 10780-10800 / data line node 10803-10840 |
| Inverter `d_d_n` | 17347-17590 x 10290-10420 | the `d_d` band turns up at x 17402-17420 as a vertical gate between the top VSS land and the output (17420-17460); output neck up x 17442-17460 to a buried contact (17440-17462 x 10290-10318) on the top band (y 10296-10315), which runs west to the contact of metal M_c (17307,10306) and east into the load gate (L, then block 17468-17520 x 10345-10393); VCC contact (17555,10385) |
| M_c | metal x 17301-17321, (17307,10306) to (17303,10705) | `d_d_n` down to its gate band. Passes over the two buried-contact boxes at x 17300-17327 without a contact (no ring; both are poly-to-diffusion boxes) |
| `lat_n` | column 10457-10515, strip east y 10467-10497 to the load | west: buried contact 17298-17327 x 10474-10501, poly west into the wiring field, down, and back east as the driver's gate band (per copy, below). East: load gate = pad 17432-17523 x 10425-10462 plus block to y 10508, tied to the node by the buried-contact box 17437-17462 x 10438-10467 under the thin metal; contact of metal M_d (17490,10440) on the pad |
| M_d | metal x 17485-17505, (17490,10440) to (17490,10640) | `lat_n` to a poly pad, then poly down x 17497-17520 and west along y 10688-10712 to x 17440: the gate of `lat`'s third pull-down, over a diffusion strip under the thin metal (x 17447-17470) between `lat` (above) and an east extension of the VSS land (y 10717-10742) |
| `lat` | column 10608-10645, east along y 10612-10638, up x 17437-17470 to the strip y 10562-10592 under its load gate | load gate = block 17477-17523 x 10528-10605, continuous with the `lat` band (y 10522-10545) that crosses the column as `lat_n`'s pull-down. West: buried contact 17298-17329 x 10605-10635 to a poly pad 17283-17327 that goes nowhere (closed outline on its west side in the clean shot; nothing under M_c above or below it) |
| VCC land of the two latch loads | 17528-17590 x 10465-10592 | one long contact |
| Bus driver (`dbus_drv`) | 17200-17590 x 10728-10872 | pull-down: `lat_n` band y 10780-10800 over the column, here 85 px wide (x 17347-17432), between the VSS land and the data line node. Node west: buried contact 17298-17342 x 10808-10847 onto the data line's poly (y 10823-10845, from its contact in the wiring field). Node east along y 10820-10838 to the load: gate block 17495-17523 x 10757-10856, tied to the node by the band y 10850-10872 and the buried-contact box 17438-17464 x 10848-10862; VCC contact (17555,10800) |

Per copy (outside the cells):

| Unit | `d_d` into the latch | `lat_n` to the driver's gate | data line |
|---|---|---|---|
| D0 | metal M_a (x 17198-17218) from (17205,8837) to a contact (17206,9254) on the band | poly west along y 9154-9176, down x 17158-17178 in the open (brown C in the metal shot), east along y 9412-9433 | bit 0: `dbl`'s contact (17207,9467) lies on the driver's poly |
| D1 | poly west from G4 along y 10190-10212, down the 28 px gap between the metals x 17215 and x 17243 (x 17222-17240) to the band | poly west along y 10476-10497, down x 17203-17217 **under the metal of data bit 3** (no contact), east along y 10780-10800 | bit 1: poly east from (17077,10832) |
| D2 | as D1, +1365 | vertical at x 17181-17195 | bit 2: poly east from (17165,12200) |
| D3 | as D1, +2733 | vertical at x 17181-17195 (in the open) | bit 3: contact (17208,13563) on the driver's poly |

The gap poly of D1-D3 cannot be seen as a colour of its own in the clean shot (the slit
between the two protected margins is 8 px). It was measured: red minus green along the
slit x 17227-17235 is +46..+59 in both metal shots over y 10230-10380 and +17..+23 just
below the band (y 10415-10465) and +21..+29 above the chain's output, in all three
copies; the chip-2 stripped shot gives +30..+34 against +5..+18.

How it was read. The area between the rails could not be read from single views (first
pass of this block). What worked: `tools/cdp1_sr.py` (sub-pixel median of the three
copies under chains 1-3, 4-6x, `cache/scratch/dbc/sr0.png` ... `sr6r.png`) in four
shots, single-copy 3x views for the wiring field, and colour profiles along the two
metal gaps. Then the cell was laid over every copy (`o1a.png`, `o1b.png` 3.1x; `o23.png`;
`p0a.png`, `p0b.png` 2.75x for cluster 0; `pm0.png` metal) and `cellcheck.py` run.

Two readings that the first look got wrong and the profiles corrected:
- The `d_d_n` band (from M_c) and the `lat_n` gate band (from M_d) lie on one line
  (y 10686-10712) and end facing each other in the gap between the VSS rail and the thin
  metal. They are **two polys**: both metal shots show two rounded ends with field
  between (5x mosaic of three copies, `mc_all.png`; profile along the row, all four units:
  poly to x 17420, 8-10 px of field colour at x 17424-17432, poly again from x 17436).
  Joined, they would short `d_d_n` to `lat_n`.
- A strip in the gap between M_c and the VSS rail (x 17325-17347, y 10548-10600) looks
  like a poly joining `lat`'s west box to the `lat` band. It is field (profile: +20
  against +45..+60 on the band's own end at y 10524-10540).

### P_x and P_y (established about the two lines of AMB-003)

- **P_x is one line common to all eight pad cells**, not a per-bit line. A single
  vertical metal at x 17633-17650 starts at D0's contact (17625,7380), has a contact
  to each cell's P_x poly at that cell's P_x height (17640,9115 for D1; 10860,
  12440, 14030, 15630, 17235 for D2-D6) and ends on D7's contact (17625,18835).
  Continuity was seen at 1.3x from D0 to D1 and at the bottom end, and at 0.5x in
  between. Where it is driven was not found: no branch was seen at the top or bottom
  end, so the driver must tap it somewhere along the column.
- **P_y is per bit.** D0's comes up the column on the thin metal of unit 0; D1's
  comes from a metal line at x 17110-17130 that rises from below to a contact at
  17120,9620, then crosses in poly (line 2); D7's arrives in poly down x 17590-17605
  and along y 18905-18935.
- Consequence for the pad cell, using the facts in pads.md: rows G (VCC) and H with
  strip 1 (gate P_x, row H tied to P_x by the buried contact) form a depletion load
  *on P_x*, and row K (VCC) with P_y's buried contact a depletion load *on P_y*. So
  both lines are open-drain as far as the column is concerned, with a pull-up in
  every pad cell (eight in parallel on P_x). That would make P_x an enable shared by
  the cells and P_y the data, with the cell containing the gating (rows I, J and the
  S1/S2 nets). This is inference from the earlier notes, not a new reading of the
  pad cell.

## Ports

| Name | Layer | Where | Direction | What |
|---|---|---|---|---|
| `d0_in` | metal x 17548-17566 | comes down from the D0 pad cell: poly from a contact near 17818,6578 left along y 6578, down to a contact near 17546,6755, then metal down; turns left at y 8188 (cross-under 17300-17500) | in | D0 pad after its protection structure. Drawn from y 8050 down |
| `d1_in` | poly | from the D1 pad cell's contact at 17822,8400 (drawn up to x 17835) | in | D1 pad after its protection structure |
| `d2_in`..`d5_in` | poly | G1 gate band of each chain, at 17291,8340 + offset | in | not followed to the pads |
| `d6_in`, `d7_in` | poly, metal | contacts (17838,16515) and (17830,17490); metal stubs drawn towards the pad cells' contact columns | in | D6 and D7 pads after their protection structures |
| `dbus_n9_in` | poly | row y 16452, drawn from x 17250 | in | input of the inverter below chain 7; from the west |
| `dbus_n9` | metal | thin metal x 17440-17456, drawn y 16400-16577 | out | up the column between the rails |
| `dN_d` | poly, then metal | G4 output, 17290-17345 x 8825-8847 + offset | out of the chain | pad level, buffered and delayed; into the cluster |
| P_y of D0 | metal x 17590-17610 from the pad cell (contact near 17580,7495), contact 17597,8097, poly cross-under y 8090-8105, contact 17510,8097, metal left to x 17448 and down as the thin metal | - | to the pad | not drawn |
| P_y of D1 | poly y 9225-9240 from the pad cell to x 17650, down x 17640-17655 (under the P_x metal) to line 2 (y 9590-9610), left to a contact at 17120,9620, metal x 17110-17130 downward | - | to the pad | not drawn |
| P_x | metal x 17633-17650, y 7380-18835 | contacts listed above | to the pads | common enable-type line, not drawn |
| `dlat_en` (the first pass's "M_b") | metal x 17243-17262, then poly and metal | top end (17252,8990); bottom: west at y 13613, contact (17166,13611), poly west, contact (16986,13608), metal west and down x 16860; drawn in `trace/dbus.txt` to (16862,13650), from there in `trace/dbus_h.txt` | in | enable of the eight input latches: it goes on down past the latch cells of D4-D7 (two contacts in each) to its driver (`dlat_en = NOR(cs_d, dbh_dlat_in_b)`, the section Bits 4-7 below) |
| data lines 0-3 (`db_b0` ... `db_b3`) | poly | `dbl`'s contacts (17207,9467), (17077,10832), (17165,12200), (17208,13563) | out | driven by the units: line k = NOT `dk_lat_n` |
| thin metal | metal x 17438-17458 | through every cluster between the rails | - | D0's `P_y` in unit 0; it is also there in units 1-3 (`segs.py` finds it at most heights from y 9300 to 11100) and through chains 4-7. No contact in any cluster. Its south end is the contact (17447,16565) on `dbus_n9`. Drawn only there |
| lines from the core | metal | the metals that arrive from the left at y 9460-9480, 9520-9545 and 9565-9585 and turn down at x 17195-17215 and 17155-17175 | - | these are `dbl`'s data lines 0, 3 and 2 |

**Internal data bus:** lines 0-3 leave the units from the bus drivers, through the
wiring field (`dbl`). The two poly lines leaving each chain to the left (y 8532 and 8792
in chain 0) are the capacitor taps, not bus lines.

## Review

Round 1 (2026-11-17, an independent agent; the clusters): all 12 devices of the master in
four shots, cluster 0's mirrored latch and shifted driver, cluster 3 at 3x, the d_d poly
in the 28 px gap, the driver output boxes and `dlat_en` confirmed; the two collinear
polys measured as two. It corrected the data-line load's width (now about 68/27) and
the notes; the `?` tie of `dn_lat`'s load stays open.

Round 1 (2026-11-17, an independent agent; bits 4-7: `dbh_drv`, `dbh_lat`, the four copies,
the data-line routes and gate rows, the latch inputs, `dlat_en`'s middle part), with
template-guided reading as the main suspicion: no wrong device or join; it corrected the
VSS extension's place, `dlat_en`'s end, D7's poly (made firm), the `?` zone's position in
the notes, and the notes (details in the section "Bits 4-7").

Round 2 (2026-11-17, an independent agent; the D6/D7 input buffers at 3.6-4x on each copy,
`d6_in` and `d7_in` from their pad cells, `dlat_en`'s route south and its NOR driver,
`dbus_n9`): no wrong transistor or connection. Fixed: the stretch of `d6_in`'s metal over
the box (17300-17322 x 16478-16500) is now `?M` (no metal pixel in either shot, the
follower stops on both sides; read as passing over, not a contact); `dlat_en`'s metal over
all five inverter output boxes is `?M` (the same evidence at all five); the notes'
firm-path claim for D6.

Round 3 (2026-11-17, an independent agent): the two `?M` fixes of Round 2 in four shots
(`d6_in` over the box, `dlat_en` over the five inverter output boxes); cluster 2 at 3x;
the `dbh_lat` copies of D5 and D6 at 4x; the eight joins of the data lines to their
drivers at 3.4-4x; the tools (extraction, `tools/unsure.py`, `tools/signals.py`). Its
findings were in the notes and the trace comments only, not in the geometry: status lines
that still said "not yet reviewed", the box under `d6_in` described as undrawn, `dlat_en`
described with one `?M` crossing instead of five, wording left from when bits 4-7 and the
D6/D7 buffers were separate pieces, and three stale comments in `trace/dbus_h.txt`. All
fixed (2026-11-17 14:13 +0000); the extraction is unchanged.

Round 4 (2026-11-17, an independent agent: the Round 3 fixes, this file end to end against
both trace files and `tools/unsure.py --equations`, the gate): no error in the trace; five
document items, fixed: the `?M` stretch's length (50 px), `dlat_en`'s two contacts per
cluster (glossary, trace comment), the Status line's Round 3 credit, the inventory row of
chains D1-D5 and three latch-cell y ranges in `trace/dbus_h.txt`'s comments; and
`notes/operation.md`'s data-bus row now has the input latches and `dlat_en` (marked).

## Ambiguities

- **The tie of `dn_lat`'s load gate** (`?P`, `?D`, `?B` in `dbus_lat`, master 17410-17443 x
  10540-10588; four copies). The `lat` band is the gate of `lat_n`'s pull-down and of the
  load on `lat`, and it touches nothing else, so it has to be tied to `lat`; the tie is
  not where the other three are. What is seen: in the gap between the VSS rail and the
  thin metal, directly below the band, a small box with a heavy outline (metal shots,
  4-copy median `cache/scratch/dbc/tie4.png`: 17418-17437 x 10565-10582; clean shot: a
  D-shaped outline 17425-17447 x 10555-10600), beside the north-west corner of `lat`'s
  diffusion. Red minus green in the slit x 17420-17430 (chip-2 metal shot, three copies;
  calibration in the same slit: field +14..+20, diffusion +30..+37, poly +44..+46): the
  band +44..+46 (y 10524-10552), one dark line of 8 px, the box +26..+48 (y 10566-10580),
  then field +14..+17 (y 10588-10604), then `lat`'s diffusion +36..+42 (y 10618-10630).
  So the box is poly or diffusion, not field, and it is cut off from the diffusion below
  it in the slit: read as a west tab of `lat`'s diffusion (from x 17437) with a tab of the
  band over it and a buried contact, like the box that ties `lat_n`'s load 110 px above.
  Drawn `?` because the inside of the box could not be resolved in any shot. Without it
  the extraction has no gate for `dn_lat`, and `tools/unsure.py --equations` lists
  `dn_lat` and `dn_lat_n` as DEPENDS. Settled by any view that resolves 10 px in that gap.
- `lat`'s west box (17298-17329 x 10605-10635): a buried contact onto a poly pad that
  ends 20 px further west and connects to nothing. Same in all four units. Purpose not
  established (added capacitance on the storage node?). No effect on the equations.
- The data line's load: the gate block is 28 px wide in the chip-2 shots (17495-17523) and
  looks 42 px wide in the clean shot (17480-17522). Drawn 28. Affects only W/L.
- `d0_b` capacitor: contacts cut, strap absent in both metal shots. Looks like a
  metal-mask option. No effect on logic.
- Chains 2-5 are assigned to D2-D5 by position only. The data lines agree for 2 and 3:
  the line `bust` numbers bit 2 ends in chain 2's unit and bit 3 in chain 3's. For 4 and 5
  likewise: chain 4's output feeds the latch that drives data line 4, chain 5's the one
  of line 5 (the section Bits 4-7 below).
- The data lines 0-3 are driven all the time by these latches (static pull-down and
  load). If the chip reads registers back over the same lines, something has to
  overpower or disable these drivers; nothing in the units does. Not a conflict in the
  trace, but a question for whoever traces the read path.

- **The box 17300-17322 x 16478-16500 at the west end of `dbus_n9`'s stub**, under the
  east edge of `d6_in`'s metal (x 17290-17306). Two readings: (a) a metal contact, which
  would put the inverter's output on D6's input line; (b) a closed box that the metal
  passes, like the closed poly pads on the latch nodes. Seen: both metal shots have no
  bright metal for 36 px there (y 16476-16512), with dark lines across the metal at the
  box's top and bottom edges and a dim centre (90-120 against 200 on the line); the clean
  shot shows the box's inside cream (185,169,126) at x 17306-17322, east of the metal's
  axis, and the metal's own pink margin running on unbroken along x 17286-17292. Calibration:
  the known mid-line contact (16815,14437) is dark olive in the clean shot (121,102,64)
  with a bright centre in the metal; the poly-on-diffusion boxes that `dlat_en`'s metal
  crosses at x 16770 are cream (178,167,125) with a dim centre (150), and those cannot be
  contacts. The box here matches the second kind. **Working assumption: (b), no contact**,
  and no contact is drawn at the box: the 50 px of `d6_in`'s metal over it (y 16470-16520)
  are drawn `?M`, since neither metal shot shows metal there (Review, Round 2), and the stub
  is drawn up to it. Reading (a) also makes no electrical sense (an inverter output and the
  thin metal on a pad's input). Two passes (6x in four shots, 8x sharpened, pixel grids).
  Settled by a sharper shot, or by finding in the D6 pad cell that nothing else drives
  the input line.
- The tie of `dbus_n9`'s load gate (`?P`, `?D`, `?B`, 17462-17500 x 16418-16455): a box
  with a heavy outline in all four shots, inside not resolved.
- Chains 6 and 7 are placed as copies. Checked on the overlays: every item of both.
  Not looked at above 2x: the cells' insides (they are the master's by correlation and
  overlay, not by an independent reading).

## Not done

- The thin metal x 17438-17458: followed at 1x only between its two ends ((17510,8097)
  and (17447,16565)); whether it is one piece.
- `dbus_n9_in`: the row y 16452 west of x 17250 (a pad near (16990,16450)).
- Left-hand wiring of chains 1-7: capacitor taps (what was seen of chains 4 and 5's
  is listed under "Not done" of the section Bits 4-7 below; chains 6 and 7: the `b` and `c` lines leave west
  from x 17258 like the others, not looked at).
- Logic at y 5250-5900.
- Channel wiring x 17590-17830: P_x line, P_y lines, input lines of D2-D5.
- The driver of P_x.
- Pad cell (AMB-003): not attempted.

## Bits 4-7: drivers and input latches south of the right datapath (`trace/dbus_h.txt`)

Region: the column x 16480-16800, y 13080-15800 (south of the right datapath, between the
address bundle and the wiring field of the data pin column), and the wiring from it to
`rdp3`'s bus ends (north), to `areg`'s bundle (west) and to the data pin column (east).
Trace: `trace/dbus_h.txt`; the two metals that bring `d4_d` and `d5_d` out of the wiring
field are in `trace/dbus.txt`.

### Status (2026-11-17 14:13 +0000, contributor session; independently reviewed: the latches and drivers in Round 1, `dlat_en`'s route south and its driver in Round 2; see Review above)

Traced, extracting (0 errors, 0 warnings), overlay-checked: **the four bus drivers of data
lines 4-7** (cell `dbh_drv`, 2 transistors, four copies), **the four data input latches of
D4-D7** (cell `dbh_lat`, 10 transistors, four copies, one upside down), the data lines
from `rdp3`'s ends into the drivers, the four gate rows from the latches to the drivers,
the data inputs of the four latches back to `d4_d` ... `d7_d` (the outputs of input
buffers 4-7 in the data pin column; buffers 6 and 7 are traced from the pad cells' contacts), and
**`dlat_en` from (16862,13650), where `trace/dbus.txt` ends it, to its driver, a two-input NOR gate at
15890-16130 x 16770-16960** (3 transistors): `dlat_en = NOR(cs_d, dbh_dlat_in_b)`. The
second input is followed 240 px and not to its source. 51 transistors.

Result (extracted equations, the same as bits 0-3):

    dk_d_n   = NOT dk_d
    dk_lat_n = NOT( dk_d   . dlat_en + dk_lat   )
    dk_lat   = NOT( dk_d_n . dlat_en + dk_lat_n )
    data line k = NOT dk_lat_n           (k = 4..7)

so **each of the data lines 4-7 follows its pin while `dlat_en` is high** and holds while
it is low, driven all the time by a static pull-down and load, like lines 0-3. Nothing in
this column has a data line as an input: no read path here either.

How firm:

| Bit | Data line | Driver (y) | Latch cell (y) | Latch input | Tied to the pin by |
|---|---|---|---|---|---|
| 4 | `db_b4` (metal x 16818) | 13660-13860 | 13870-14345 (upside down) | `d4_d`: chain 4's G4, metal x 17250 up to a pad (17206,13999), poly row y 13997 west | chain 4 = D4 by position (chains 2-5 are not followed to their pads: Ambiguities above) |
| 5 | `db_b5` (metal x 16862) | 13465-13660 | 14350-14810 | `d5_d`: chain 5's G4, metal x 17252 up and west to a pad (17161,14693), poly row y 14692 west | chain 5 = D5 by position |
| 6 | `db_b6` (metal x 16908) | 13270-13465 | 14827-15287 | `d6_d`: poly row y 15173 east to the output box (17318,15190) of G4 of buffer 6 (`dbus_in` upside down) | buffer 6's input line is traced from the contact of the D6 pad cell (the `d6_in` row of the input-line table above) |
| 7 | `db_b7` (poly x 16791) | 13075-13270 | 15304-15764 | `d7_d`: poly row y 15650 east, south at x 17188, east along y 15818 to the output box of G4 of buffer 7 | buffer 7's input line is traced from the contact of the D7 pad cell |

Firm geometry (no `?` on the path): data line k - driver k - gate row - latch cell, for all
four; latch cell - row - metal - `dk_d` of chain k for k = 4, 5; and latch cell - row -
`dk_d` of chain k - `dk_in` - the pad cell's contact for k = 7, and for k = 6 except one
50 px stretch of `d6_in`'s metal (y 16470-16520, over a box) drawn `?M`: neither metal shot
shows metal there and the follower stops at it from both sides (review). What rests on
position: that chains 4 and 5 are D4's and D5's (as for chains 2 and 3: Ambiguities above). The numbering is self-consistent: the bus bit order
(`bust`: register widths) and the pad order agree for all eight bits if the four latch
cells are D4-D7 from top to bottom.

Inside every latch cell one zone is not resolved and is drawn `?` (Ambiguities), so
`tools/unsure.py --equations` gives `dk_lat`, `dk_lat_n` as DEPENDS, exactly as for
D0-D3; `dk_d_n` and "data line k = NOT `dk_lat_n`" are FIRM.

### Inventory

| What | Where | State |
|---|---|---|
| Rails | VCC metal x 16488-16535, VSS metal x 16657-16702, y 13080-15800 | drawn. Which is which: from the loads (every load's far end is on the left rail); not followed to a pad |
| Bus drivers, bits 7, 6, 5, 4 (top to bottom) | 16470-16810 x 13075-13860, pitch 195 | cell `dbh_drv`, master = bit 6's; findcell 0.86-0.91, cellcheck median ncc 0.97-0.98 |
| Latch cells, D4 (upside down), D5, D6, D7 | 16470-16850 x 13870-15790; D5-D7 at a 477 px pitch, D4's mirrored about y 14350 | cell `dbh_lat`, master = D5's; findcell 0.82-0.86, cellcheck median ncc 0.94-0.96 |
| Gate rows | under both rails at y 13265, 13458, 13655, 13852; west of the column down to the latch cells | drawn (bit 7's and 6's are `areg`'s `areg_w6`, `areg_w7`) |
| `dlat_en` | metal x 16858 / 16816 / 16770, y 13645-16498, then west and south to the poly row y 16865 | drawn to its driver; its metal over the five inverter output boxes (x 16772, y 15796-16370) is `?M` |
| Logic below y 15800 in this column | 16480-16800 x 15800-16450 | surveyed, not traced: five inverters on a 135 px pitch (see "Lower part of the column") |
| `dlat_en`'s driver | 15890-16130 x 16770-16960 (in `bd2`'s untraced left column) | traced: NOR, 3 transistors; output box and load tie `?` |

### Logic

### Bus driver `dbh_drv` (traced)

The same circuit as `dbus_drv`: the data line's node (diffusion) with a depletion load
(gate block 16543-16585 x 13300-13405 over the strip from the VCC land, arm east along
y 13300-13322, tied to the node by the buried contact 16616-16647 x 13322-13344) and one
pull-down under the VSS rail (gate band y 13358-13388, channel x 16648-16774: W about 125,
L 30; VSS contact (16693,13410)). Load about 73/42. The node's east end
(16745-16774 x 13313-13350) carries a buried contact onto the data line's poly.
The gate band turns south at x 16780-16797 to the gate row (y 13447-13470 in the master).
Read on the 4-copy median at 4x in three shots (`cache/scratch/dbh/sr_acid1b.png`,
`sr_acid.png`, `sr_metal.png`); overlay `o1.png`.

Data lines in (they are `rdp3`'s four lines "going south" at y 12900):

- bit 7: poly down x 16783-16800 to y 13128 and west onto the node box (2.4x in two
  stripped shots, `b7.png`).
- bit 6: metal x 16908 ends on a contact (16904,13326); poly west under the metals of bits
  5 and 4 (no contact there) (2.4x, `z1.png`).
- bit 5: metal x 16862 ends on a contact (16857,13521); poly west under bit 4's metal.
- bit 4: metal x 16818 ends on a contact (16813,13716).

### Data input latch `dbh_lat` (traced, one zone `?`)

Circuit and arrangement are those of `dbus_lat` turned by 180 degrees (findcell scores
0.63-0.67 against it; that is how it was recognised), but the layout is not a copy: the
x positions differ by up to 30 px from part to part, so it is a cell of its own, and every
item was placed on the photos (3-copy median at 4-5x in four shots, `La_*.png`,
`Lb_*.png`, `T1.png`-`T7.png`, `U1.png`; overlays `q1.png`, `q2.png` at 2.6x on the
master, `k134.png` on the other three). Master coordinates (D5's cell):

| What | Where | Notes |
|---|---|---|
| Upper column under the VSS rail | x 16672-16730 | VSS land y 14352-14385 (one long contact shared with the cell above; each cell draws its half) / `d_d_n` band 14386-14410 / node / `dlat_en` band 14428-14450 / `lat` 14455-14492 |
| `lat`'s third pull-down | diffusion strip x 16628-16646, y 14352-14465, beside the rail, from the top VSS land down to `lat` | gate = the end of the `lat_n` poly (stub y 14388-14412, rounded end at x 16648; the strip's edges print through it at x 16625 and 16645). The stub is **not** the `d_d_n` band: that one starts at x 16658 under the rail |
| `lat_n` poly at the top | stub, up-leg x 16553-16578, pad 16553-16603 x 14435-14472 with the contact (16572,14452) | the driver's gate row arrives on it from the west (y 14432) |
| M_d | metal x 16561-16581, (16572,14452) to (16575,14655) | `lat_n`: from its load gate pad up to the row's pad |
| `lat`'s load | gate block 16543-16608 x 14487-14574, one poly with the `lat` band (y 14550-14574, east to x 16748); strip y 14508-14537 from the VCC land | the strip's two edges print through the block as dark lines, nothing else does (`U1.png`, chip-1 metal shot) |
| Middle VSS land | 16688-16735 x 14505-14553, contact (16702,14527) | `lat` band below it, then `lat_n` |
| Lower column | x 16680-16730 | `lat_n` y 14576-14640 (wider to the west: its load strip y 14602-14632) / `dlat_en` band 14640-14662 / node / `d_d` band 14686-14707 / VSS land 14708-14752, contact (16705,14729) |
| `lat_n`'s load | gate 16543-16603 x 14587-14672 (the lower part is the pad of M_d), pad east to x 16648, tied to the strip by the box 16610-16647 x 14635-14659 | |
| Closed poly pads on `lat` and `lat_n` | boxes 16766-16795 x 14458-14497 and x 14592-14630, east of the thin metal | buried contacts onto pads that go nowhere (closed outline on three sides), as on `dbus_lat`'s `lat` |
| Inverter `d_d_n` | VSS land / vertical gate x 16655-16676 (the `d_d` band turned down) / output 16608-16655 x 14716-14752 / load block 16545-16602 x 14704-14752 / VCC land 16480-16538 x 14688-14745 | output neck down to the buried contact 16606-16634 x 14772-14799 on the band y 14778-14800, which goes west into the load gate (L) and east under the rail (field above and below it) to the contact (16756,14790) |
| M_c | metal x 16741-16761, (16756,14790) up to (16761,14389) | `d_d_n` to its gate band |
| `dlat_en` contacts | (16815,14437) and (16813,14652) on the metal x 16816 | the two series gates |

Per copy: the gate row joins the top pad (D5: y 14432 from under `areg`'s rail; D4: y 14258,
mirrored; D6: y 14907 = `areg_w7`; D7: y 15386 = `areg_w6`), and the `d_d` band runs on
east as the input row.

### Gate rows (traced)

| Bit | Row under the rails | Route to the latch |
|---|---|---|
| 7 | y 13265 = `areg_w6`'s poly | `areg`'s metal x 16341 down to a contact (16338,14865), poly x 16342 to y 15262, diagonal to (16466,15386), east |
| 6 | y 13458 = `areg_w7`'s poly | poly x 16364 to y 14798, diagonal to (16460,14907), east |
| 5 | y 13655 | west to x 16410, south **under** `areg`'s rail (salmon line in the clean shot, 800 px) to y 14432, east |
| 4 | y 13852 | west to x 16465, south in the open to y 14258, east |

1.45-1.6x in three shots (`d1m.png`, `g1.png`, `g2.png`), 3.3x at the contact and the
diagonal (`g3.png`), overlays `o23.png`. So `areg_w6` = `d7_lat_n` and `areg_w7` =
`d6_lat_n` (aliases in `trace/dbus_h.txt`).

### `dlat_en` and its driver

From the end of the part drawn in `trace/dbus.txt` (16862,13650): down x 16858 to y 13802, west to x 16816 (`j1.png`, both
metal shots), down past the four latch cells to y 15803, west to x 16772 (`j2.png`). Its
metal starts as a corner 90 px below the end of bit 5's metal on the same track (x 16862,
contact (16857,13521)): two nets. One net enables all eight latches.

South of (16772,15803) (images in `cache/scratch/dbl67/`):

| Stretch | Where | Seen |
|---|---|---|
| metal south | x 16762-16780, y 15803-16498 | `L1m.png` 1.65x, `de1.png` 4x in four shots, `o3.png`. It runs over the output boxes of the five inverters below the latch cells (y 15826, 15962, 16095, 16225, 16350). Over each box both metal shots show a 50 px stretch with dark rings and a dimmer centre (150 against 200), the same at all five; the boxes are cream in the clean shot (poly on diffusion; a metal contact is dark olive: calibrated on (16815,14437)). Read as **no contact** at any of them: five gate outputs cannot share one metal. All five crossings are drawn `?M` (one item, x 16772, y 15796-16370): the first review read (16772,15803) as the line's end, and the second found the metal alike over all five (dark runs of 26-29 px), so all five are marked or none |
| west | y 16491-16505 to a contact (16577,16495) | `de2.png` 2.6x three shots |
| poly under the VCC rail | y 16487-16513, x 16435-16590 | same; contact (16443,16495) at its west end |
| metal west and south | x 16427, y 16493-16872; contact (16424,16860) | `tools/follow.py` (332 px, one piece), `de3.png`, `n3.png` 3.3x |
| poly row west | y 16853-16877, x 16110-16430, under `cs_d`, `rs_d`, `rw_d`, `bd2_rs_n`, the metal x 16205 and `e_b` | `n3.png`, `de4.png`. No pad at any crossing, and the clean shot is salmon (215,160,110), not olive, under each metal: no tap |
| output box | 16090-16127 x 16850-16885, on the east edge of the gate's node | `n1.png`, `n2.png` 3.2x four shots: heavy outline in all four, the row's poly reaches it; green centre in the clean shot. Inside not resolved: `?B` |

**The driver** (traced; `n1.png`, `n2.png`, `de6.png`, `n7.png`, overlay `o1.png`), in the
part of `bd2`'s left column that `bd2` lists as not traced:

    dlat_en = NOR( cs_d, dbh_dlat_in_b )

- Diffusion column x 16025-16095, y 16770-16960, under and east of the VSS rail
  (x 16003-16053); VSS contacts (16042,16790) and (16042,16940), rings in both metal shots.
  The rail is wider over the node but shows no ring there.
- Band 1, y 16808-16832: gate `cs_d`. The band runs east under the bundle to a pad with a
  contact (16380,16818) on the `cs_d` metal (x 16372-16390): ring with a bright centre in
  the metal shot, olive in the clean shot (173,146,93).
- Band 2, y 16895-16917: gate `dbh_dlat_in_b`. It runs east under `e_b` and the metal
  x 16205 (no tap: salmon under both) to x 16240 and turns south in the 28 px gap between
  the metals x 16205 and x 16250 (x 16222-16240; orange strip in both chip-2 shots,
  `n5.png` 3x), followed to y 17135. At y 17158-17178 it meets a poly row; whether it
  joins it or crosses was not resolved (`n6.png`).
- Node between the bands (y 16835-16890): west as a strip y 16847-16885 under the load's
  gate block (15925-15968 x 16830-16925, W/L about 38/43) to a VCC land
  (15845-15895 x 16838-16903, contact near (15862,16868)) under the wide VCC metal; east to
  the output box.
- The load gate's tie: a loop at the block's south-east corner (15960-15990 x 16880-16925)
  with a small box inside in the metal shots. Drawn `?`.

Believed (datasheet: a register is written when CS is low, R/W low, on E): `cs_d` is CS
buffered in the pin's sense, so the latches can only be transparent while CS is low; the
second input should then carry R/W and E. Not traced.

### Lower part of the column (y 15800-16450; surveyed, not traced)

Five inverters between the same two rails, on a 135 px pitch (`L1m.png`, `L1a.png` 1.65x;
gate 2 at 2.9x in four shots, `G2.png`). Gate 2: VCC land 16495-16545 x 15950-16015, load
block 16548-16600 x 15935-16000 with its tie below (16575-16615 x 16000-16030); output
strip y 15955-15970 east under the VSS rail to a box 16745-16780 x 15950-15975 and on east
in poly to a pad (16900,15958); pull-down under the VSS rail: gate band y 15985-16008 from
a pad (16855,15995), VSS contact (16690,16030). The other four look the same. Input pads
at (16810,15865), (16855,15995), (16895,16122), (16945,16255) and a fifth band (y 16385)
that ends near x 16800; output pads at (16855,15815), (16900,15958), (16950,16085) and
further east for gates 4 and 5. The pads sit on the vertical metals of the wiring field
(x 16815, 16860, 16905, 16950): from the pad positions each gate's output appears to land
on the metal that carries the next gate's input, i.e. a chain, but no pad was looked at
above 1.65x. Not traced; `dlat_en`'s metal passes over the five output boxes.

### Ports

| Name | Layer | Where | Direction | What |
|---|---|---|---|---|
| data lines 4-7 | metal / poly | `rdp3`'s ends at y 12900: x 16818, 16862, 16908 (metal), 16791 (poly) | out | driven: line k = NOT `dk_lat_n` |
| `d4_d`, `d5_d` | poly | rows y 13997 and y 14692 from the pads (17206,13999), (17161,14693) | in | from chains 4 and 5 of the data pin column |
| `d6_d` | poly | ends at (17302,15192) on the box 17300-17335 x 15175-15205 | in | output of G4 of input buffer 6 (`dbus_in`, upside down) |
| `d7_d` | poly | ends at (17300,15818) | in | output of G4 of input buffer 7 (`dbus_in`, upside down) |
| `cs_d` | metal | contact (16380,16818) on `bd2`'s line | in | first input of `dlat_en`'s NOR |
| `dbh_dlat_in_b` | poly | x 16231, drawn to y 17135 | in | second input of `dlat_en`'s NOR; source not traced |
| `vcc`, `vss` | metal | rails, y 13080-15800 | - | by load orientation |

- `lat`'s third pull-down: its gate is the rounded end of the `lat_n` stub (overhang past
  the strip 3 px or less), and both of the strip's joins (to VSS above, to `lat` below) are
  hidden under the rail's edge in all four cells: confirmed as a device by the review,
  but those two joins are not seen directly.

### Ambiguities

- **The zone x 16605-16658, y 14460-14545 of every latch cell** (`?D`, `?P`, `?B`): how
  `lat` reaches its load strip and where the load's gate (the `lat` band) is tied to it.
  Seen: heavy outlines 16612-16650 x 14490-14545 with three horizontal lines at y 14500,
  14515, 14530 (chip-1 metal shot, `U1.png`), a heavy blob in the clean shot. `lat`'s band
  and load block touch nothing else, so the tie has to be there. The `?` items are drawn as
  `dbus_lat` has it, which the independent review found to be about 25 px off the feature:
  in all four copies the feature is a vertical bar x 16637-16662, y 14488-14545, from the
  SW corner of the `lat` land down onto the `lat` band (cross-lines at y 14500, 14512,
  14530), and x 16612-16640, y 14467-14492 is plain field. Same topology (`lat` = strip
  end = load gate); poly or diffusion not resolved. The drawn items should move there when
  this is settled. Two passes (4x median in three shots; 5x
  tiles in four). Next: a 6-8x median of all eight latch cells (four here, the four
  `dbus_lat` copies turned), which should resolve it for all eight at once.
- The pad (17206,13999) of `d4_d`'s row: the metal from chain 4 bends onto it from the
  south-east. Metal test along y 14002 in both metal shots: only 3-6 px dips at the pad's
  edge between the pad's centre and the line, and the clean shot shows no poly between the
  pad and chain 4's `d4_b` band 35 px east of it. Read as joined (the metal has no other
  end). If it were not, `d4_d` would go nowhere.
- `d7_d`'s stretch x 17188, y 15650-15820 between two metals (x 17177-17195): drawn
  firm after the independent review saw it plainly in the chip-2 metal shot; whether it
  runs on south of y 15825 is not checked.
- `dlat_en`'s jog at y 13802 is drawn square; the photo's corner is slightly slanted.
- Rails: supply by load orientation only.
- As for lines 0-3 (Ambiguities above): all eight data lines are driven all the time by
  their latches. The read path is elsewhere.

- **`dlat_en`'s metal over the five inverter output boxes** (x 16770, y 15810-16360): read
  as passing over them without contact (see the table above). If instead it ended on the
  first box (16770,15826), `dlat_en` would be the output of the first inverter and the
  metal further south a different net; the metal between the boxes is plain in both metal
  shots, and all five crossings look alike. All five crossings are `?M` (x 16772,
  y 15796-16370). Settled by tracing
  the five inverters.
- **The output box of `dlat_en`'s NOR** (16090-16127 x 16850-16885, `?D`, `?B`) and **its
  load's tie** (15960-15990 x 16880-16925, `?`): seen as heavy outlines in four shots,
  insides not resolved. With them `tools/unsure.py --equations` gives `dlat_en` as
  DEPENDS. The gate's two pull-downs, its VSS contacts and the load strip are firm.

#### Review of the bits 4-7 part

Independently reviewed (2026-11-17), with template-guided reading as the main suspicion:
every transistor of `dbh_drv` and `dbh_lat` read from the photo alone, all four copies at
3x, the four data-line routes and gate rows (no swap, no step), the latch inputs and
`dlat_en` confirmed. Its corrections (the VSS extension's place, `dlat_en`'s end, D7's
poly firm, the `?` zone's true position, these notes) are in.

### Not done

- The source of `dbh_dlat_in_b`: from (16231,17135) south; it meets a poly row at
  y 17158-17178 (x 16165-16300) just above a pad with a contact on the metal x 16205
  (16205,17210). Next step: a 4-5x view of 16190-16260 x 17130-17230 in the two chip-2
  shots, then follow whichever it joins.
- The five inverters of the column's lower part (y 15800-16450) and where their pads'
  metals go.
- The rest of `bd2`'s left column around the NOR (x 15890-16150, y 16680-17100).
- The capacitor taps of chains 4 and 5 (`d4_b`: poly west along y 14040 to a pad
  (17140,14040) with a dot of metal; `d4_c`: poly west, diagonal, to a contact
  (16935,14335); `d5_b`: poly west along y 14755 to a pad near (16905,14752); `d5_c`: a
  contact (17205,15018), metal up to (17180,14890)): seen, not drawn.
- The five metals of the wiring field x 16925-17115 (pad driver lines): not followed.
