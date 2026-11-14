# bd2: bus control logic right of the register select gates

Region x 15850-17000, y 14700-17100. Trace: `trace/bd2.txt` (`@requires sel`, `areg`).
Extracts with 0 errors, 0 warnings.

## Status

- Images used: about 40. Sharpened views (`tools/rdp3_sharp.py`) at 3-4x were the most
  useful for this area; plain views above 4x added nothing.
- **Traced and extracted**: the two strobe drivers (two big inverters at the top of the
  left gate column), their output routes to `sel` and `areg`, and their input wiring.
  - `areg_load = NOT e_b`. No other input, no latch, no clock.
  - `sel_stb_r = NOT bd2_n1`.
- **Partly traced**: the gate that drives `bd2_n1` ("row 1", x 15900-16140,
  y 15500-15670). Established: its output strip is pulled to ground through two
  transistors in series, gates `bd2_r1_a` and `e_b`. Not established: its load and what
  the L-shaped poly at its left end does (Ambiguity 1). So the full equation of
  `sel_stb_r` is still open: it is `e_b AND bd2_r1_a` possibly OR-ed with one more term.
- **Not traced**: the rest of the left gate column (y 15650-17100), the gate group right
  of the bundle (x 16240-16470, y 15400-15900), the whole right-hand column
  (x 16480-17000). Observations and coordinates for all three are under Not done.

## Inventory

| What | Where | State |
|---|---|---|
| VCC rail | x 15795-15890, whole height (shared with `sel`'s right-hand column); band y 14745-14805 to areg's inverter rail x 16142-16194 | drawn |
| Ground rail of the left column | x 16008-16058, y 14908 to about 17050 (at y 17100 only a thin line x 16016-16026 is left); joined by the band y 14908-14960 to `areg_rail_r` | drawn; lower end not looked at |
| `areg_rail_r` | x 16401-16450 above y 14908; jogs to x 16355-16405 (y 14908-15330), then to x 16312-16362 (y 15400 to about 16330, the ground rail of the gate group right of the bundle) | drawn to y 15330 |
| G1, driver of `sel_stb_r` | 15900-16272 x 15030-15160 | traced |
| G2, driver of `areg_load` | 15895-16272 x 15225-15360 | traced |
| Bundle | x 16100-16400, vertical metals at x 16122, 16169, 16210, 16255, 16280, 16299, 16342, 16385 (segments: see Bundle below) | upper part traced |
| Row 1 | 15900-16150 x 15500-15670 | pull-down pair and output traced, rest open |
| Left column, rows below | x 15890-16150, y 15650-17100 | not traced |
| Gate group right of the bundle | x 16240-16470, y 15400-15900 | not traced (structure noted) |
| Right-hand column | x 16480-16800, y 14700-16450; routing to the east and south of it | not looked at |

## Logic

### G1: `sel_stb_r` driver (traced)

One inverter, `sel_stb_r = NOT bd2_n1`.

- Load: VCC land under the rail (contacts 15862,15048 and 15862,15108), strip
  y 15075-15145 east under the poly block 15903-15942 x 15030-15160 (W/L about 70/39).
  The block's top end is tied to the output by a buried contact at 15912-15948 x 15028-15062.
- Pull-down: poly band y 15078-15100 from x 15978 to the contact 16255,15086, with a leg
  down at x 15978-16000 to y 15160. Output above the band and left of the leg, ground
  below the band and right of the leg (contact 16032,15122 on the rail). W about 280.
- Output: strip y 15050-15078, buried contact 16185-16218 x 15030-15058 at its east
  end, poly north at x 16256 under the ground band to contact 16255,14868, metal west along
  y 14868 to contact 15928,14868, poly west along y 14825 into `sel` (15850,14825).
- **The poly from the north ends on that buried contact; it does not reach the contact
  at 16255,15086** (5x view: 10 px of bare field between them at y 15058-15068 in the metal
  shot, two separate rims in the clean shot). areg.md's by-eye note has the poly running
  on to that contact, which would tie the gate's input to its output.
- Input: contact 16255,15086, metal down x 16255 to y 15222, west, down x 16158-16178
  (the "upper trunk") to its **end** at contact 16167,15432.

### G2: `areg_load` driver (traced)

One inverter, `areg_load = NOT e_b`.

- Load: VCC land (contact 15863,15300), strip y 15258-15332 under the block
  15898-15940 x 15232-15335 (W/L about 75/42); the block has an arm along y 15228-15250 to
  a buried contact at 15963-15995 x 15243-15272 on the output.
- Pull-down: band y 15290-15312, x 15978-16195, ending in the pad of contact 16210,15300.
  Output above (y 15262-15290), ground below (contact 16040,15338). W about 128.
- Output: buried contact 16098-16132 x 15243-15277, poly east along y 15257 to contact
  16255,15258, metal east and up x 16297 to contact 16296,15003, poly under the ground
  band, contact 16296,14822, metal x 16299 up into `areg`.
- Input, all one net (`bd2_n2` = `e_b`):
  - the pad of contact 16210,15300;
  - metal x 16200-16222 from that contact down to its end at contact 16205,15690 (the
    poly from there goes east towards the gate group right of the bundle: not traced);
  - a poly under that metal ("strip 2") from the pad down to y 15488, diagonal to
    (16240,15515), then east as the band y 15503-15527 into the gate group right of
    the bundle, where it is the gate band `G_b` (not traced further);
  - a poly branch from strip 2 west along y 15358-15378, under the upper trunk without
    contact, to the pad of contact 16122,15388;
  - metal from that contact down x 16112-16135 to y 15480, east, and down as the
    "lower trunk" x 16158-16180.
- **The lower trunk is `e_b`.** `tools/sel_tracks.py v 16168` finds metal from y 15470 to
  17702 in both metal shots (gaps only where a contact or a crossing darkens it, the
  longest at 17006-17031 / 17057, where trunks.md has a tap); trunks.txt has `e_b`
  turning up at (16170,17691). Not looked at by eye below y 15850.
- **The upper trunk and the lower trunk are in line but are two wires.** Both metal shots
  show bare poly at x 16160-16180, y 15450-15468, between the contact 16167,15432 and
  the corner where the metal from 16122,15388 arrives; the track scan has the same gap
  (15443-15470).

So the address register's load strobe is simply NOT E: the register cells are
transparent while E is low. Whatever restricts loading to a write of the address
register (CS, RS, R/W) is not on this strobe; it would have to be on the cells' data
lines (`areg_din*`, which come down from the datapath above areg's cell row).

### Row 1: the gate that drives `bd2_n1` (partly traced)

Established (in the trace):

- Ground land 16028-16075 x 15505-15545 with contact 16047,15522 on the rail; diffusion
  column x 16018-16100 below it.
- Upper band y 15555-15578: gate, ends east in the pad of contact 16114,15560, whose
  metal (`bd2_r1_a`, x 16100-16120) goes down to a pad at 16098-16140 x 15768-15797.
- Lower band y 15603-15625: gate, runs on east (y 15600-15620) to the pad of contact
  16167,15605 on the lower trunk: `e_b`.
- Output strip y 15625-15650 below the lower band; at its east end a buried contact
  (16106-16144 x 15628-15670, a hook-shaped poly end with a heavy outline) to a poly band
  y 15646-15668 that runs east under both trunks to x 16228, into the poly block
  16226-16248 x 15598-15662, which joins strip 1 (the poly from contact 16167,15432 on
  the upper trunk: down x 16157-16180, diagonal, down x 16198-16222 to y 15612).
- Hence `bd2_n1` is this strip, and it is pulled low when `e_b` AND `bd2_r1_a`.

Believed: `bd2_n1 = NOT(e_b AND bd2_r1_a [OR bd2_r1_l])`, hence
`sel_stb_r = (e_b AND bd2_r1_a) [OR bd2_r1_l]` and
`sel_wN = rselN AND NOT sel_stb_r`. Which of the two forms holds depends on
Ambiguity 1. Either way the only clock-like input is E itself; no latch is on the path
from `bd2_n1` to the select gates.

Where the other inputs come from (seen in sharpened 3x views, not traced as gates):

- `bd2_r1_a`: the thin metal x 16100-16120 from the gate pad 16114,15560 ends on a poly
  pad with a heavy outline at 16098-16148 x 15765-15797, which sits at the east end of
  row 2's output strip (y 15745-15790, below the band y 15723-15745, ground contact
  16045,15700). By the layout style of this column (G1, G2, row 1: output strip, buried
  contact at its east end, poly onwards) that pad is row 2's output. Believed:
  `bd2_r1_a = NOT(row 2's gate)`; row 2's gate poly runs west to at least x 15905.
- `bd2_r1_l`: see Ambiguity 1; believed to be row 3's output. Row 3's upper band
  (y 15812-15832) is on `e_b` (tap 16166,15822).

The extraction lists the two series transistors under "not part of a static gate"
because no load is drawn.

## Bundle x 16100-16400: what is on each track

From `tools/sel_tracks.py` on both metal shots (y ranges; approximate, ends are where to
look for contacts) and the views of y 15330-15750. Only the part above y 15750 was
checked by eye.

| x | Segment | Net |
|---|---|---|
| 16122 | 15384-15490 | `e_b`: contact 16122,15388 down to the corner into the lower trunk |
| 16169 | 15211-15443 | `bd2_n1` (upper trunk), contact 16167,15432 at its lower end |
| 16169 | 15470-17702 | `e_b` (lower trunk); contacts seen at 16167,15605 (row 1), 16167,15735, 16165,15818; scan gaps at about 16127, 16389, 17018-17044 are probably contacts |
| 16210 | 15296-15690 | `e_b`: contact 16210,15300 to contact 16205,15690 |
| 16210 | 15771-16051 (16094 in chip 1) | not identified; starts at a contact at about 16207,15775 |
| 16210 | 16424-16568, 16754-17745 | not identified |
| 16255 | 15947-15983, 16144-17300+ | not identified |
| 16280 | 15470-15870 | not identified: thin metal from contact 16260,15470 (gate pad of `G_a`) down to a contact at about 16262,15870 |
| 16299 | 16033-17569 | `rw_d` per trunks.md; **top end at about y 16033-16059** |
| 16342 | 15326-16330 | the ground rail of the gate group (x 16312-16362) and its continuation, not `rs_d` |
| 16342 | 16596-17515 | `rs_d` per trunks.md; **top end at about y 16596-16624** (both shots; no metal at x 16342 at y 16500) |
| 16385 | 16138-17569 | `cs_d` per trunks.md; top end about y 16140-16190 |

## Ports

| Name | Layer | Crosses at | Direction | What |
|---|---|---|---|---|
| `sel_stb_r` | poly | x 15850, y 14825 (west) | driven here | write strobe gate of `sel` (G1 output) |
| `areg_load` | metal | x 16299, y 14700 (top) | driven here | address register load strobe (G2 output) = NOT E |
| `vcc` | metal | x 15795-15890, y 14700 and y 17100 | supply | rail shared with `sel` |
| `vcc` | metal | x 16142-16194, y 14700 (top) | supply | areg's inverter rail, joined here to the rail above by the band y 14745-14805 |
| `vss` (`areg_rail_r`) | metal | x 16401-16450, y 14700 (top) | supply | ground: every pull-down of the left column has its source on a branch of it |
| `areg_w6` | metal | x 16341, y 14700 (top) | unknown | contact 16337,14866, poly down x 16330-16345 under the ground band and on down (areg.md: to y 15255, then diagonally to about 16490,15390, i.e. to the right-hand column). Not drawn below the top edge |
| `areg_w7` | poly | x 16364, y 14700 (top) | unknown | turns at y 14805 and runs diagonally down-right under the rail to about (16470,14900), i.e. to the right-hand column. Not drawn |
| `e_b` | metal | x 16169, y 17100 (bottom) | from outside | E buffered; lower trunk |
| ? | metal | x 16212, y 17100 | ? | track 16210, segment 16754-17745 |
| ? | metal | x 16257, y 17100 | ? | track 16255, runs up to about y 16144 |
| `rw_d` | metal | x 16298, y 17100 | from outside | per trunks.md; top end about y 16040 |
| `rs_d` | metal | x 16342, y 17100 | from outside | per trunks.md; top end about y 16600 |
| `cs_d` | metal | x 16385, y 17100 | from outside | per trunks.md; top end about y 16160 |
| ? | metal | x 16016-16026, y 17100 | ? | thin line where the ground rail was; not looked at |
| ? | metal, 49 wide | x 16492-16540, y 17100; x 16505-16540 at y 14700 | supply? | wide vertical of the right-hand column, whole height |
| ? x 6 | metal | x 16580, 16624, 16668, 16711, 16755, 16799 at y 17100 | ? | six lines on a 43.5 px pitch leaving south; they are the nested corners at x 16560-16820, y 16480-16900 |
| ? | metal | x 16837 (faint), 17001 at y 17100 | ? | |
| ? | metal | x 16586, 16621, 16732, 16816, 16950, 16992 at y 14720 (top) | ? | lines of the right-hand column continuing into areg's untraced part |
| ? | metal | x 17000 (east), y about 14694, 14728, 14761, 14798, 14834, 14916, 14992, 15022, 15096, 15175, 15199, 15323, 15532, 15674, 15741, 15796, 15844, 15936, 16106, 16215, 16508, 16580, 16632, 16685, 16759, 16984, 17010, 17048, 17085 | ? | raw output of `sel_cut.py v 16995`: bright runs on a cut just inside the east edge. Not checked by eye; some are lines running along the edge, not crossing it |

The lists marked ? at the south, east and top edges come from `tools/sel_cut.py` only.

## Ambiguities

1. **Row 1, everything left of x 16018** (15900-16018 x 15530-15650). What is seen, in
   all four shots and in sharpened views (`tools/rdp3_sharp.py`):
   - An L-shaped poly: bar 15908-15992 x 15558-15587, neck down x 15908-15937 to the pad
     of contact 15925,15625; metal x 15912-15935 from there down to a contact at
     15925,15825 (`bd2_r1_l`; what is under that contact is not traced). The bar's east
     end (15973-15993) looks like a separate box with a heavy outline.
   - A VCC land directly west of it (15842-15892 x 15540-15608, contact 15865,15575).
     No diffusion edge is seen crossing the 12 px between the land and the L.
   - An outline above the bar: left edge x 15937 (y 15533-15558), top edge y 15535 from
     x 15937 east to the shoulder of the ground land at about x 16030.
   - A pocket below the bar's east end: 15978-15998 x 15590-15635, plain, closed on the
     left and bottom.
   - A strip x 15998-16012, y 15550-15630, salmon in the clean shot (poly, or diffusion
     under the rail's margin), between the pocket and the column's left edge (dark line
     x 16012-16018).
   - Inside the bar, in the clean shot and chip 1's metal shot, horizontal stripes
     (edges at about y 15564 and 15579).

   Readings:
   - (A) the bar is the gate's depletion load (strip from the VCC land east under the
     bar, gate tied to the output by a buried contact at the box, output down the pocket
     into the strip y 15625-15650). Then `bd2_n1 = NAND(e_b, bd2_r1_a)` and the metal
     `bd2_r1_l` is the same net as `bd2_n1`. For: the land is where every other load of
     this column starts (G1, G2); the stripes; the box. Against: no strip seen between
     land and bar; the outline above the bar then has no explanation.
   - (E) the bar is a third pull-down: ground diffusion above it (the outline, joined to
     the ground land), output below it (a thin strip along the bar's lower edge into the
     pocket). Then `bd2_n1 = NOT(bd2_r1_l OR (e_b AND bd2_r1_a))` and the load is
     somewhere not yet found. For: the outline above the bar and its straight left edge
     at x 15937. Against: the bar's end (x 15993) stops short of the pocket's right side,
     and no load is in sight.
   - Seen later, in favour of (E): directly below the pocket there is a boxed structure
     (15975-16010 x 15655-15715, heavy outline, inner box) and, west of it under the thin
     metal `bd2_r1_l`, bars at y 15660-15675, 15680-15708 and 15712-15730 that reach the
     VCC land 15850-15885 x 15685-15790 (contact row at x 15865). That is where a load of
     row 1 would be if the L is a pull-down; it could equally be row 2's load. Not resolved
     in sharpened 4x views.
   - Working assumption: none; the trace draws only the series pair and the output
     route, and leaves `bd2_r1_l` as a separate net. My belief leans to (E):
     `sel_stb_r = bd2_r1_l OR (e_b AND bd2_r1_a)`.
   - To settle: trace 15890-16020 x 15640-15730 (the candidate load) and find what
     `bd2_r1_l` meets at 15925,15825: that contact sits on a land (pitted in chip 2's
     stripped shot, specks in the clean shot) with a boxed tie beside it
     (15955-16000 x 15800-15845), which looks like the output land of row 3 next to its
     load; if so `bd2_r1_l` is row 3's output and (E) holds.
2. **Strip 1 into the block** (16205-16232 x 15598-15614, marked `?`): in the clean shot
   the salmon strip under the metal and the textured block beside it touch with no rim
   between them; in chip 2's stripped shot a dark line runs down the block's left side,
   but that is also where the metal's edge was. Taken as joined: otherwise strip 1 (and
   with it G1's input) would have no driver and the block and band would lead nowhere.
3. **Loads of G1 and G2**: the VCC lands under the rail are shared with the loads of
   `sel`'s right-hand column on the other side of the rail (`sel.txt` draws those
   schematically, with one contact per load at y 15065, 15195, 15325; the photos show
   contacts at 15048 and 15108, 15195, 15300). The strips from the lands to my load
   blocks are drawn from edge lines seen in the metal shot, not from a clear view.
4. **areg.md, "seen below the region"**: two of its by-eye statements are wrong.
   The poly from contact 16252,14862 does not reach the contact at 16255,15085 (see G1),
   and the metal below 16255,15085 does not continue as `e_b`: it ends at 16167,15432.
5. **trunks.md** has `rs_d` on the metal x 16333-16352 "above 15900, not followed" with
   a tap at y 16335. The track is empty between about y 16330 and 16600 in both metal
   shots: `rs_d`'s metal ends at about y 16600, and the metal above y 16330 is the
   lower end of the ground rail x 16312-16362 or another wire. Likewise `rw_d`'s metal
   ends at about y 16040. Not checked by eye.
6. **Ground rail x 16008-16058 below y 16600**: the scans show several short gaps
   (16655-16679, 16797-16815, 16921-16975, 17053-17112 in chip 2, none of them in chip 1
   above 17049). Drawn continuous to y 17050.

## Not done

Everything below is seen, not traced.

- **Row 1's left end**: Ambiguity 1.
- **Left column, y 15650-17100** (x 15890-16150). The same style continues: VCC lands
  under the rail at x 15862, load polys at x 15900-15990, gate bands under the ground
  rail x 16008-16058 with ground contacts on the rail, outputs leaving east in poly to
  the bundle or west under the VCC rail. Seen:
  - y 15675-15790: ground contact 16045,15700; band y 15723-15745 whose poly runs on
    west to x 15940 (and perhaps under the thin metals to x 15900); output strip below
    it going west along y 15752-15787 to x 15950.
  - y 15805-15880: band y 15812-15832 with a rounded west end at x 16015; band
    y 15857-15878; contact pad 15900-15945 x 15805-15850 (end of `bd2_r1_l`); a box
    15950-15995 x 15795-15845 beside it.
  - Pad 16098-16148 x 15765-15797 at the lower end of `bd2_r1_a` (drawn; its contact is
    marked `?`). A metal at x 16095-16118 is also seen below it (y 15800-15895), not
    followed.
  - Taps of the lower trunk (`e_b`), drawn as poly stubs: 16167,15735 east to band `G_d`
    of the gate group; 16166,15822 west to row 3's upper band.
  - Contact 16207,15778: poly east = band `G_e` of the gate group; metal `bd2_m210`
    x 16200-16222 down to about y 16050 (drawn from the track scan, lower end not seen).
  - Further taps per trunks.md: `rw_d` at y 16030 (its top end), 16290, 16680; `rs_d` at
    16590 (top end); `cs_d` at 16170 (top end), 16430, 16815, 17170.
- **Gate group right of the bundle** (x 16240-16470, y 15400-15900). Ground rail
  x 16312-16362 (the jogged `areg_rail_r`) with a diffusion column x 16290-16365 under
  it and these features from top to bottom:
  land y 15412-15465 (dark dot at 16332,15432: contact?);
  band `G_a` y 15465-15490, its west end is the pad of contact 16260,15470 (thin metal
  x 16268-16290 from there down to about 16262,15870);
  band `G_b` y 15510-15535 = strip 2 = `e_b`;
  node y 15535-15585 with a poly box at its west end (16243-16318 x 15548-15578, rounded
  west end, perhaps a contact to the thin metal at 16277,15562);
  ground contact 16325,15612;
  band y 15635-15660, which comes from the east (x 16434+);
  node y 15660-15725 with a second poly box at its west end (16225-16318 x 15683-15715,
  reaching west towards the pad of contact 16205,15690 on the `e_b` metal);
  band `G_d` y 15725-15750 = `e_b` (tap 16167,15735, traced to x 16262);
  band `G_e` y 15770-15795 = `bd2_m210` (contact 16207,15778, traced to x 16262);
  ground contact 16330,15815.
  Loads and more gates on its east side (x 16370-16470): a load block at
  16405-16450 x 15468-15495, contacts at 16450,15540 and 16450,15738 joined by a thin metal
  x 16440-16460. East of that the wide vertical x 16490-16545 with long contact rows
  (a supply rail of the right-hand column).
  This group takes `e_b` on at least two gates and is the likely source of
  `bd2_r1_a`; it could not be resolved at 3-6x in the time available: the two poly boxes
  are the obstacle.
- **Right-hand column** (x 16480-16800, y 14700-16450) and the routing east and south of
  it: not looked at beyond the survey. `areg_w6` and `areg_w7` go there.
