# dbh: data bus bits 4-7 to the pins D4-D7 (drivers, latches, wiring)

Region: the column x 16480-16800, y 13080-15800 (south of the right datapath, between the
address bundle and the wiring field of the `dbus` column), and the wiring from it to
`rdp3`'s bus ends (north), to `areg`'s bundle (west) and to the `dbus` column (east).
Trace: `trace/dbh.txt`; the two metals that bring `d4_d` and `d5_d` out of the wiring
field are in `trace/dbus.txt`.

## Status (2026-11-17 14:00 (UTC+1), contributor session; independently reviewed)

Traced, extracting (0 errors, 0 warnings), overlay-checked: **the four bus drivers of data
lines 4-7** (cell `dbh_drv`, 2 transistors, four copies), **the four data input latches of
D4-D7** (cell `dbh_lat`, 10 transistors, four copies, one upside down), the data lines
from `rdp3`'s ends into the drivers, the four gate rows from the latches to the drivers,
`dlat_en` from where `dbus` left it to its south end with its eight contacts, and the
data inputs of the four latches back to: `d4_d` and `d5_d` (chains 4 and 5 of `dbus`),
and two gate outputs in the lower part of the `dbus` column for D6 and D7 (those gates are
not traced). 48 transistors.

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
| 6 | `cdp1_a3_bl` (`rbus_b6`, metal x 16908) | 13270-13465 | 14827-15287 | `dbh_d6_in`: poly row y 15173 east to the output box (17318,15190) of an untraced gate of the `dbus` column | position only (third of four latch cells; its buffer is the next thing south of chain 5) |
| 7 | `cdp1_a2_bl` (`rbus_b7`, poly x 16791) | 13075-13270 | 15304-15764 | `dbh_d7_in`: poly row y 15650 east, south at x 17188 (`?`), east along y 15818 to the output box of an untraced gate | position only; one stretch of its row is `?` |

Firm geometry (no `?` on the path): data line k - driver k - gate row - latch cell, for all
four; and latch cell - row - metal - `dk_d` of chain k for k = 4, 5. What rests on
position: that chains 4 and 5 are D4's and D5's (as in `dbus`), and everything about which
pin feeds the latches of bits 6 and 7. The numbering is self-consistent: the bus bit order
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
| `dlat_en` | metal x 16858 / 16816, y 13645-15792 | drawn to its end (16772,15792) |
| Logic below y 15800 in this column (to about y 16450) | 16480-16800 x 15800-16450 | not looked at: five similar gates on a 120 px pitch (0.6x survey) |

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

### `dlat_en`

From `dbus`'s end (16862,13650): down x 16858 to y 13802, west to x 16816 (`j1.png`, both
metal shots), down past the four latch cells to y 15792, west to its end (16772,15792)
(`tools/follow.py`: one piece, 2208 px; `j2.png`). Its metal starts as a corner 90 px
below the end of bit 5's metal on the same track (x 16862, contact (16857,13521)): two
nets. One net now enables all eight latches. What is at its south end is not traced.

## Ports

| Name | Layer | Where | Direction | What |
|---|---|---|---|---|
| data lines 4-7 | metal / poly | `rdp3`'s ends at y 12900: x 16818, 16862, 16908 (metal), 16791 (poly) | out | driven: line k = NOT `dk_lat_n` |
| `d4_d`, `d5_d` | poly | rows y 13997 and y 14692 from the pads (17206,13999), (17161,14693) | in | from chains 4 and 5 of `dbus` |
| `dbh_d6_in` | poly | ends at (17302,15192) on the box 17300-17335 x 15175-15205 | in | output of the top gate of the lower `dbus` column (that gate's own gate band is fed by a poly down x 17255-17275 from a box near (17318,15648)) |
| `dbh_d7_in` | poly | ends at (17300,15818) | in | output of the gate at about y 15790 of the lower `dbus` column |
| `dlat_en` | metal | end (16772,15792) | in | driver not traced |
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
- `dbh_d7_in`'s stretch x 17188, y 15650-15820 between two metals (x 17177-17195): drawn
  firm after the independent review saw it plainly in the chip-2 metal shot; whether it
  runs on south of y 15825 is not checked.
- `dlat_en`'s jog at y 13802 is drawn square; the photo's corner is slightly slanted.
- Rails: supply by load orientation only.
- As in `dbus`: all eight data lines are driven all the time by these latches. The read
  path is elsewhere.

## Review

Independently reviewed (2026-11-17), with template-guided reading as the main suspicion:
every transistor of `dbh_drv` and `dbh_lat` read from the photo alone, all four copies at
3x, the four data-line routes and gate rows (no swap, no step), the latch inputs and
`dlat_en` confirmed. Its corrections (the VSS extension's place, `dlat_en`'s end, D7's
poly firm, the `?` zone's true position, these notes) are in.

## Not done

- The gates that feed `dbh_d6_in` and `dbh_d7_in` (lower part of the `dbus` column,
  y 15150-16550: about nine single gates, not copies of `dbus_in`), and from there to the
  pads D6 and D7. Until then bits 6 and 7 are tied to their pins by position only.
- `dlat_en`'s driver at (16772,15792) and the logic of this column below y 15800.
- The capacitor taps of chains 4 and 5 (`d4_b`: poly west along y 14040 to a pad
  (17140,14040) with a dot of metal; `d4_c`: poly west, diagonal, to a contact
  (16935,14335); `d5_b`: poly west along y 14755 to a pad near (16905,14752); `d5_c`: a
  contact (17205,15018), metal up to (17180,14890)): seen, not drawn.
- The five metals of the wiring field x 16925-17115 (pad driver lines): not followed.
