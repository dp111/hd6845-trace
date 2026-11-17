# Data bus interface column (`dbus`)

Region: x 17050-17700, y 5300-17000, and the D0-D7 pad cells to its right.
Trace: `trace/dbus.txt`. Scratch tools: `tools/dbus_mosaic.py` (the same rectangle at
several offsets side by side, for comparing repeats), `tools/dbus_autocorr.py`
(vertical pitch of a strip).

## Status (2026-11-17 14:00 (UTC+1), contributor session; clusters independently reviewed, the chain 4/5 outputs not yet)

Traced, extracting, overlay-checked: the input buffer chain (four inverters) as cell
`dbus_in`, placed six times (D0-D5); the input line of D0 from where it enters the
column, and the whole input line of D1 from the pad cell's contact; **the gate group
("cluster") under each of chains 0-3: a transparent data input latch and the driver of
the internal data line**, cells `dbus_lat` and `dbus_drv`, 12 transistors per bit, placed
four times (48 transistors). Data lines 0-3 (`cdp1_c5_bl` ... `cdp1_c2_bl`, drawn into the
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
the latches and bus drivers of bits 4-7 are (`notes/blocks/dbh.md`). The latches of D6 and
D7 there take their inputs from two gates in the lower part of this column (output boxes
near (17318,15190) and (17315,15815)), which are not traced.

Surveyed, with coordinates below, but NOT traced: all other logic in the column, the
channel wiring to the pads, where `dlat_en` is driven. The pad cell (AMB-003) was not
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
| Input chain, D1-D5 | same cell at (1,1365) (1,2732) (2,4098) (2,5465) (2,6223) | placed; findcell on the clean shot scores 0.81-0.83, each overlay checked at 1.25x. The four-gate core is the same in all six; the wiring left of x 17290 differs per copy and is drawn only for D0 (and D1's input) |
| Capacitor rectangles of chain 0 | 16960-17040 x 8445-8580 and x 8745-8880 | drawn |
| Cluster 0 (D0) | 17150-17590 x 8885-9520 | traced: `dbus_lat` upside down (mirror line y 9826.5) and `dbus_drv` at (0,-1368) |
| Clusters 1-3 (D1-D3) | 17150-17590 x 10250-10890, and the same at (1,1365), (1,2733) | traced: `dbus_lat` + `dbus_drv`, master = D1's. Clusters 1-3 are copies of each other (findcell 0.88, 0.85; cellcheck median ncc 0.96-0.97); cluster 0 is **not** a copy of them (findcell finds nothing above 0.4): its inverter-and-latch part is the same cell turned upside down (cellcheck ncc 0.94 on the clean shot, 0.91 on metal), its driver the same cell the right way up, and the wiring between the two differs |
| Cross-unders between units 0 and 1 | poly "line 1" y 9545-9566, "line 2" y 9590-9610, both under both rails | line 1 drawn (D1 input); line 2 is D1's P_y, not drawn |
| Logic below chain 5 | 17150-17590 x 15100-16600 | about nine single gates on the 152 pitch, not copies of `dbus_in` and not traced. The top one (y 15150-15260) drives the D6 latch's input row from its output box (17300-17335 x 15175-15205), and its own gate band is fed by a poly down x 17255-17275 from a box near (17318,15648); the gate at about y 15790 drives the D7 latch's input row (`notes/blocks/dbh.md`). No cluster follows chains 4 and 5 (chain 5 starts 758 px below chain 4): their latches are in `dbh`'s column |
| Logic above D0 | 17200-17700 x 5250-5900 | several gates, not looked at |

findcell (metal and clean shot, threshold 0.4) finds no seventh or eighth copy of
the chain. The input buffers of D6 and D7 are in the lower part of the column
(y 15100-16600), laid out differently: the inputs of the D6 and D7 latches come from
two gate outputs there (table above). Not traced.

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
  D1's. Chains 2-5 are tagged by position and *assumed* to follow the pad order.
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
  draws it to y 13650 and `trace/dbh.txt` from there: down past the latch cells of D4-D7
  (two contacts in each) to its end at (16772,15792), beside untraced logic. Believed: the
  write strobe from the bus control (E, CS, R/W); not traced.

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
| `dN_d` | poly, then metal | G4 output, 17290-17345 x 8825-8847 + offset | out of the chain | pad level, buffered and delayed; into the cluster |
| P_y of D0 | metal x 17590-17610 from the pad cell (contact near 17580,7495), contact 17597,8097, poly cross-under y 8090-8105, contact 17510,8097, metal left to x 17448 and down as the thin metal | - | to the pad | not drawn |
| P_y of D1 | poly y 9225-9240 from the pad cell to x 17650, down x 17640-17655 (under the P_x metal) to line 2 (y 9590-9610), left to a contact at 17120,9620, metal x 17110-17130 downward | - | to the pad | not drawn |
| P_x | metal x 17633-17650, y 7380-18835 | contacts listed above | to the pads | common enable-type line, not drawn |
| `dlat_en` (the first pass's "M_b") | metal x 17243-17262, then poly and metal | top end (17252,8990); bottom: west at y 13613, contact (17166,13611), poly west, contact (16986,13608), metal west and down x 16860; drawn here to (16862,13650), from there by `dbh` | in | enable of the eight input latches: `dbh` follows it down past the latch cells of D4-D7 (two contacts in each) to its end (16772,15792). Driver not traced |
| data lines 0-3 (`cdp1_c5_bl` ... `cdp1_c2_bl`) | poly | `dbl`'s contacts (17207,9467), (17077,10832), (17165,12200), (17208,13563) | out | driven by the units: line k = NOT `dk_lat_n` |
| thin metal | metal x 17438-17458 | through every cluster between the rails | - | D0's `P_y` in unit 0; it is also there in units 1-3 (`segs.py` finds it at most heights from y 9300 to 11100). No contact in any cluster. Not drawn, not followed |
| lines from the core | metal | the metals that arrive from the left at y 9460-9480, 9520-9545 and 9565-9585 and turn down at x 17195-17215 and 17155-17175 | - | these are `dbl`'s data lines 0, 3 and 2 |

**Internal data bus:** lines 0-3 leave the units from the bus drivers, through the
wiring field (`dbl`). The two poly lines leaving each chain to the left (y 8532 and 8792
in chain 0) are the capacitor taps, not bus lines.

## Review

The clusters were independently reviewed (2026-11-17): all 12 devices of the master in
four shots, cluster 0's mirrored latch and shifted driver, cluster 3 at 3x, the d_d poly
in the 28 px gap, the driver output boxes and `dlat_en` confirmed; the two collinear
polys measured as two. It corrected the data-line load's width (now about 68/27) and
the notes; the `?` tie of `dn_lat`'s load stays open.

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
  of line 5 (`dbh`).
- The data lines 0-3 are driven all the time by these latches (static pull-down and
  load). If the chip reads registers back over the same lines, something has to
  overpower or disable these drivers; nothing in the units does. Not a conflict in the
  trace, but a question for whoever traces the read path.

## Not done

- Where `dlat_en` is driven: the logic at its south end (16772,15792) (`dbh` draws the
  metal to there).
- The thin metal x 17438-17458 through units 1-3: where it comes from and goes.
- Left-hand wiring of chains 1-5: capacitor taps (what was seen of chains 4 and 5's
  is listed in `notes/blocks/dbh.md`).
- Logic at y 15100-16600: the gates that feed the D6 and D7 latches, i.e. the D6 and D7
  input buffers, and their lines from the pads. Logic at y 5250-5900.
- Channel wiring x 17590-17830: P_x line, P_y lines, input lines of D2-D7.
- The driver of P_x.
- Pad cell (AMB-003): not attempted.
