# dbh: data bus bits 4-7 to the pins D4-D7 (drivers, latches, wiring)

Region: the column x 16480-16800, y 13080-15800 (south of the right datapath, between the
address bundle and the wiring field of the `dbus` column), and the wiring from it to
`rdp3`'s bus ends (north), to `areg`'s bundle (west) and to the `dbus` column (east).
Trace: `trace/dbh.txt`; the two metals that bring `d4_d` and `d5_d` out of the wiring
field are in `trace/dbus.txt`.

## Status (2026-11-17 14:40 (UTC+1), contributor session; the latches and drivers independently reviewed, `dlat_en`'s driver not yet)

Traced, extracting (0 errors, 0 warnings), overlay-checked: **the four bus drivers of data
lines 4-7** (cell `dbh_drv`, 2 transistors, four copies), **the four data input latches of
D4-D7** (cell `dbh_lat`, 10 transistors, four copies, one upside down), the data lines
from `rdp3`'s ends into the drivers, the four gate rows from the latches to the drivers,
the data inputs of the four latches back to `d4_d` ... `d7_d` (the outputs of input
buffers 4-7 of `dbus`; buffers 6 and 7 are traced from the pad cells' contacts), and
**`dlat_en` from where `dbus` left it to its driver, a two-input NOR gate at
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
| 4 | `cdp1_c1_bl` (`rbus_b4`, metal x 16818) | 13660-13860 | 13870-14345 (upside down) | `d4_d`: chain 4's G4, metal x 17250 up to a pad (17206,13999), poly row y 13997 west | chain 4 = D4 by position (`dbus`: chains 2-5 are not followed to their pads) |
| 5 | `cdp1_a0_bl` (`rbus_b5`, metal x 16862) | 13465-13660 | 14350-14810 | `d5_d`: chain 5's G4, metal x 17252 up and west to a pad (17161,14693), poly row y 14692 west | chain 5 = D5 by position |
| 6 | `cdp1_a3_bl` (`rbus_b6`, metal x 16908) | 13270-13465 | 14827-15287 | `d6_d`: poly row y 15173 east to the output box (17318,15190) of G4 of buffer 6 (`dbus_in` upside down) | buffer 6's input line is traced from the contact of the D6 pad cell (`notes/blocks/dbus.md`) |
| 7 | `cdp1_a2_bl` (`rbus_b7`, poly x 16791) | 13075-13270 | 15304-15764 | `d7_d`: poly row y 15650 east, south at x 17188, east along y 15818 to the output box of G4 of buffer 7 | buffer 7's input line is traced from the contact of the D7 pad cell |

Firm geometry (no `?` on the path): data line k - driver k - gate row - latch cell, for all
four; latch cell - row - metal - `dk_d` of chain k for k = 4, 5; and latch cell - row -
`dk_d` of chain k - `dk_in` - the pad cell's contact for k = 6, 7. What rests on
position: that chains 4 and 5 are D4's and D5's (as in `dbus`). The numbering is self-consistent: the bus bit order
(`bust`: register widths) and the pad order agree for all eight bits if the four latch
cells are D4-D7 from top to bottom.

Inside every latch cell one zone is not resolved and is drawn `?` (Ambiguities), so
`tools/unsure.py --equations` gives `dk_lat`, `dk_lat_n` as DEPENDS, exactly as for
D0-D3; `dk_d_n` and "data line k = NOT `dk_lat_n`" are FIRM.

## Inventory

| What | Where | State |
|---|---|---|
| Rails | VCC metal x 16488-16535, VSS metal x 16657-16702, y 13080-15800 | drawn. Which is which: from the loads (every load's far end is on the left rail); not followed to a pad |
| Bus drivers, bits 7, 6, 5, 4 (top to bottom) | 16470-16810 x 13075-13860, pitch 195 | cell `dbh_drv`, master = bit 6's; findcell 0.86-0.91, cellcheck median ncc 0.97-0.98 |
| Latch cells, D4 (upside down), D5, D6, D7 | 16470-16850 x 13870-15790; D5-D7 at a 477 px pitch, D4's mirrored about y 14350 | cell `dbh_lat`, master = D5's; findcell 0.82-0.86, cellcheck median ncc 0.94-0.96 |
| Gate rows | under both rails at y 13265, 13458, 13655, 13852; west of the column down to the latch cells | drawn (bit 7's and 6's are `areg`'s `areg_w6`, `areg_w7`) |
| `dlat_en` | metal x 16858 / 16816 / 16770, y 13645-16498, then west and south to the poly row y 16865 | drawn to its driver; one crossing `?M` |
| Logic below y 15800 in this column | 16480-16800 x 15800-16450 | surveyed, not traced: five inverters on a 135 px pitch (see "Lower part of the column") |
| `dlat_en`'s driver | 15890-16130 x 16770-16960 (in `bd2`'s untraced left column) | traced: NOR, 3 transistors; output box and load tie `?` |

## Logic

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
`d6_lat_n` (aliases in `trace/dbh.txt`).

### `dlat_en` and its driver

From `dbus`'s end (16862,13650): down x 16858 to y 13802, west to x 16816 (`j1.png`, both
metal shots), down past the four latch cells to y 15803, west to x 16772 (`j2.png`). Its
metal starts as a corner 90 px below the end of bit 5's metal on the same track (x 16862,
contact (16857,13521)): two nets. One net enables all eight latches.

South of (16772,15803) (images in `cache/scratch/dbl67/`):

| Stretch | Where | Seen |
|---|---|---|
| metal south | x 16762-16780, y 15803-16498 | `L1m.png` 1.65x, `de1.png` 4x in four shots, `o3.png`. It runs over the output boxes of the five inverters below the latch cells (y 15826, 15962, 16095, 16225, 16350). Over each box both metal shots show a 50 px stretch with dark rings and a dimmer centre (150 against 200), the same at all five; the boxes are cream in the clean shot (poly on diffusion; a metal contact is dark olive: calibrated on (16815,14437)). Read as **no contact** at any of them: five gate outputs cannot share one metal. The first crossing (y 15796-15880) is drawn `?M` because the earlier review read (16772,15803) as the line's end |
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

## Ports

| Name | Layer | Where | Direction | What |
|---|---|---|---|---|
| data lines 4-7 | metal / poly | `rdp3`'s ends at y 12900: x 16818, 16862, 16908 (metal), 16791 (poly) | out | driven: line k = NOT `dk_lat_n` |
| `d4_d`, `d5_d` | poly | rows y 13997 and y 14692 from the pads (17206,13999), (17161,14693) | in | from chains 4 and 5 of `dbus` |
| `d6_d` | poly | ends at (17302,15192) on the box 17300-17335 x 15175-15205 | in | output of G4 of input buffer 6 (`dbus`) |
| `d7_d` | poly | ends at (17300,15818) | in | output of G4 of input buffer 7 (`dbus`) |
| `cs_d` | metal | contact (16380,16818) on `bd2`'s line | in | first input of `dlat_en`'s NOR |
| `dbh_dlat_in_b` | poly | x 16231, drawn to y 17135 | in | second input of `dlat_en`'s NOR; source not traced |
| `vcc`, `vss` | metal | rails, y 13080-15800 | - | by load orientation |

- `lat`'s third pull-down: its gate is the rounded end of the `lat_n` stub (overhang past
  the strip 3 px or less), and both of the strip's joins (to VSS above, to `lat` below) are
  hidden under the rail's edge in all four cells: confirmed as a device by the review,
  but those two joins are not seen directly.

## Ambiguities

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
  tiles in four). Next: a 6-8x median of all eight latch cells (four here, four in
  `dbus`, turned), which should resolve it for both blocks at once.
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
- As in `dbus`: all eight data lines are driven all the time by these latches. The read
  path is elsewhere.

- **`dlat_en`'s metal over the five inverter output boxes** (x 16770, y 15810-16360): read
  as passing over them without contact (see the table above). If instead it ended on the
  first box (16770,15826), `dlat_en` would be the output of the first inverter and the
  metal further south a different net; the metal between the boxes is plain in both metal
  shots, and all five crossings look alike. The first crossing is `?M`. Settled by tracing
  the five inverters.
- **The output box of `dlat_en`'s NOR** (16090-16127 x 16850-16885, `?D`, `?B`) and **its
  load's tie** (15960-15990 x 16880-16925, `?`): seen as heavy outlines in four shots,
  insides not resolved. With them `tools/unsure.py --equations` gives `dlat_en` as
  DEPENDS. The gate's two pull-downs, its VSS contacts and the load strip are firm.

## Review

Independently reviewed (2026-11-17), with template-guided reading as the main suspicion:
every transistor of `dbh_drv` and `dbh_lat` read from the photo alone, all four copies at
3x, the four data-line routes and gate rows (no swap, no step), the latch inputs and
`dlat_en` confirmed. Its corrections (the VSS extension's place, `dlat_en`'s end, D7's
poly firm, the `?` zone's true position, these notes) are in.

## Not done

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
