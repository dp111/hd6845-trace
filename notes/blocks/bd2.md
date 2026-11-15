# bd2: bus control logic right of the register select gates

Region x 15850-17000, y 14700-17100. Trace: `trace/bd2.txt` (`@requires sel`, `areg`).
Extracts with 0 errors, 0 warnings. Two runs; this file was rewritten by the second.

## Status

- **Traced and extracted**
  - G1, the driver of `sel_stb_r`, and G2, the driver of `areg_load` (first run).
  - The **strobe latch** behind G1: rows 1-3 of the left gate column and the inverter
    G4 west of the rail (second run). A D latch, open while `e_b` is high.
  - The wiring of `e_b`, `bd2_n1`, `bd2_al_n`, `bd2_a`, `bd2_c` in the bundle down to
    y 15900.
- **Pull-downs traced, loads not**: the two gates of the gate group right of the bundle
  (`bd2_nu`, `bd2_al_n`).
- **Two results of the first run are corrected**: `areg_load` is not `NOT e_b` (G2's
  gate is a separate net, `bd2_al_n`), and row 1 has a third pull-down and a load.
- **Not traced**: where `bd2_c`, `bd2_x` and `bd2_m210` come from (east of x 16376, the
  right-hand column), the left column below y 15990 (where `rw_d`, `cs_d` and `rs_d`
  end: located, not traced), the right-hand column. See Not done.
- Images used: about 44 (first run) + 40 (second). What worked in the second run was
  **numbers instead of pictures**: character maps of small areas by colour class
  (`tools/bd2_umap.py` for what lies under metal in the clean shot, `tools/bd2_cmap.py`
  for poly against plain areas in the open, `tools/bd2_patch.py` / `bd2_prof.py` for
  single patches and profiles). At 5-6x the pictures of this area are too blurred to
  decide a junction; the maps decided them.

## Verdict on the disagreement with bd3: the input of the `sel_stb_r` driver is NOT `e_b`

bd3 reads the metal at x 16169 as one line from G1's gate down to `e_b`; the first run
here read a break at y 15443-15470. **The break is real: `trace/bd3.txt`'s `bd3_stb`
section is wrong in its last two `M` lines and its `N M 16167,15500 e_b` label** (the
inverter itself, its load, output route and the gap to the pad at 16255,15085 are
right and duplicate G1 here). Evidence, all from numbers (`tools/bd2_prof.py`):

1. Colour and grain of both metal shots down x 16162-16177 (`bd2_prof.py col 16169
   15405 15500 7 3`): metal (R about 180-200, G/R 0.8-0.9, grain 21-39) down to y 15411;
   the ring of contact 16167,15432 (dark 15414-15426, bright centre 15429-15438, dark
   15441-15453); then y 15455-15464 is **orange and smooth in both chips**: chip 2
   165/114/58, G/R 0.69, grain 11.5; chip 1 150/97/51, G/R 0.65, grain 6.7. Bare poly
   beside it measures G/R 0.58-0.75; twelve other 8 px pieces of the same trunk between
   dark crossings (y 16080-17325) measure R 158-212, G/R 0.78-0.90 (one shot at most
   down to 0.68, never both), grain 13-30. Then a dark line y 15465-15471, then metal.
2. That dark line at y 15465-15471 runs straight across from x 16136 to 16184
   (`bd2_prof.py map 16100 15396 16235 15504`): it is the top edge of the metal that
   arrives from contact 16122,15388 and turns down. Nothing underneath has an edge there:
   in the clean shot the poly under the line is uniform (221-231/158-179/118-133) from
   y 15442 to 15500.
3. Chip 2's stripped shot has a very dark bar across that poly at y 15451-15467
   (R 51-74; everywhere else from y 15380 to 15720 along x 16169 it is 96 or more,
   including under the three tap contacts further down): the uncovered piece of poly.
4. The thin dark line at x 16154-16160 between the horizontal metal y 15470-15490 and
   the lower trunk (`bd2_prof.py row 15479 16104 16192 4 2`) is 6 px wide and sits on
   the left edge of the poly underneath (red outline at x 16158-16163 in the clean
   shot): an edge printing through, not a gap. So the metal from 16122,15388 does join
   the lower trunk.
5. Gate polys followed at 3x (view k3): G1's band y 15078-15100 -> pad/contact
   16255,15086 -> metal x 16255, y 15222 west, x 16168 down -> ends on contact
   16167,15432 (poly "strip 1" goes on south from the pad).

So `sel_stb_r = NOT bd2_n1`, and `bd2_n1` is the Q of the latch below.

## Equations (the answer in one place)

    sel_stb_r = NOT bd2_n1                                   G1          traced
    bd2_n1    = NOT( bd2_qb OR (e_b AND bd2_a) )             row 1       traced
    bd2_qb    = NOT( bd2_n1 OR (e_b AND bd2_c) )             rows 2-3    traced
    bd2_a     = NOT bd2_c                                    G4          traced (two junctions inferred, below)
    areg_load = NOT bd2_al_n                                 G2          traced
    bd2_al_n  = NOT( bd2_x OR (e_b AND bd2_m210) )           pull-downs traced, load and the tie to G2 uncertain
    bd2_nu    = NOT( bd2_c AND e_b )                         pull-downs traced, load and destination not traced

Read as logic: rows 1-3 with G4 are a transparent latch. While `e_b` is high
`bd2_n1 = bd2_c` (and `bd2_qb = NOT bd2_c`); while `e_b` is low both hold. Hence

    sel_stb_r = NOT bd2_c   while E is high;  held at its last value while E is low
    sel_wN    = rselN AND bd2_c(latched)      (the NOR in sel)

- **Set** (strobes on, `bd2_n1` high): `e_b AND bd2_c` pulls `bd2_qb` low.
- **Cleared** (strobes off): `e_b AND bd2_a`, i.e. `e_b AND NOT bd2_c`, pulls `bd2_n1` low.
- **Held**: the cross-coupling `bd2_n1` -> row 2's gate, `bd2_qb` -> row 1's third
  pull-down, whenever `e_b` is low.

`bd2_c` is not yet traced to its source (it is the gate band G_a of the gate group and
may run on east of x 16376): **uncertain what it is**. Nothing in the traced part gates
the strobe with E low, so as traced a selected register stays open after E falls until
E rises again with `bd2_c` low; whether `bd2_c` itself contains E has to come from its
source.

## Inventory

| What | Where | State |
|---|---|---|
| VCC rail | x 15795-15890, whole height (shared with `sel`'s right-hand column); band y 14745-14805 to areg's inverter rail x 16142-16194 | drawn |
| VCC land under that rail | x 15850-15898, y 15682-15912 continuous (and on down, not followed) | drawn to 15912 |
| Ground rail of the left column | x 16008-16058, y 14908 to about 17050; joined by the band y 14908-14960 to `areg_rail_r` | drawn; lower end not looked at |
| `areg_rail_r` | x 16401-16450 above y 14908; jogs to x 16355-16405 (y 14908-15330), then to x 16312-16362 (y 15400 to about 16330, the ground rail of the gate group) | drawn to y 15330 and y 15400-15850; the jog between is the first run's observation, not drawn |
| G1, driver of `sel_stb_r` | 15900-16272 x 15030-15160 | traced |
| G2, driver of `areg_load` | 15895-16272 x 15225-15360 | traced |
| Row 1 (latch, Q side) | 15900-16150 x 15500-15715 | traced |
| Rows 2-3 (latch, Q bar side) | 15900-16150 x 15655-15915 | traced |
| G4 (`bd2_a = NOT bd2_c`) | 15900-16125 x 15857-15985 | traced |
| Gate group right of the bundle | x 16240-16480, y 15400-15850 | pull-downs traced, loads not |
| Left column below y 15990 | x 15890-16150, y 15990-17100 | located only (see Not done) |
| Right-hand column | x 16480-16800, y 14700-16450; routing east and south of it | not looked at |

## Logic

### G1: `sel_stb_r` driver (traced, first run)

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
- The poly from the north ends on that buried contact; it does not reach the contact
  at 16255,15086 (10 px of bare field between them at y 15058-15068).
- Input: contact 16255,15086, metal down x 16255 to y 15222, west, down x 16158-16178
  (the "upper trunk") to its **end** at contact 16167,15432. From that pad the poly
  "strip 1" runs down x 16157-16180, diagonally, down x 16208-16218 to y 15612 and steps
  right into a block (16224-16248 x 15600-15660). From the block's foot a band goes
  west: y 15643-15657 under the `bd2_al_n` metal, slanting down under the `e_b` trunk to
  y 15664-15680, to the buried contact at the east end of row 1's output strip.
  Checked in the second run: salmon unbroken under both metals, the block orange in
  the open (`bd2_umap.py 16140 15580 16260 15700`, `bd2_cmap.py 16180 15590 16262 15700`).

### G2: `areg_load` driver (traced; its input corrected in the second run)

One inverter, `areg_load = NOT bd2_al_n`.

- Load: VCC land (contact 15863,15300), strip y 15258-15332 under the block
  15898-15940 x 15232-15335 (W/L about 75/42); the block has an arm along y 15228-15250 to
  a buried contact at 15963-15995 x 15243-15272 on the output.
- Pull-down: band y 15290-15312, x 15978-16195, ending in the pad of contact 16210,15300.
  Output above (y 15262-15290), ground below (contact 16040,15338). W about 128.
- Output: buried contact 16098-16132 x 15243-15277, poly east along y 15257 to contact
  16255,15258, metal east and up x 16297 to contact 16296,15003, poly under the ground
  band, contact 16296,14822, metal x 16299 up into `areg`.
- **Input.** From the pad of contact 16210,15300 only a metal leaves: x 16200-16222 down
  to its end at contact 16205,15690. The first run had a poly ("strip 2") under that
  metal all the way from the pad and so joined G2's gate to `e_b`. It is not there:
  - under the metal the clean shot is pink field from y 15313 to 15355, between the
    olive contact footprint (y 15298-15310) and the poly that starts at y 15358
    (`larr_px.py - col 16211 15286 15400 3`; `bd2_umap.py 16100 15286 16246 15500`);
  - that poly is the branch from the `e_b` pad 16122,15388, which arrives along
    y 15358-15378 and turns down as strip 2 (x 16208-16218) to the gate band G_b;
  - where the metal crosses it there is no contact: metal bright and unbroken from
    y 15364 to 15400 in both shots, salmon unbroken under it, no olive patch.
- From the pad of contact 16205,15690 a poly bar (x 16228-16250, y 15688-15702, over
  field: the plain areas above and below it measure as field) runs east to the boxed
  cell at the west end of `bd2_al_n`'s diffusion (16266-16296 x 15684-15704).

So the address register's load strobe is `x OR (E AND m210)` in terms of the two
untraced inputs, not simply NOT E. **This changes what areg.md should assume.**

### The strobe latch (traced, second run)

Left gate column, rows 1-3, plus G4. All three AND-OR-invert / inverter gates have the
same build: pull-downs in a diffusion column under the ground rail, the output running
west under the rail's edge to a load whose strip comes from the VCC land under a poly
block. The block, a thin bar above it and a bar or pad below it are **one poly** (the
6-9 px dark lines between them are the strip's two edges under the poly; two polys could
not be that close), and that poly is tied to the output at a boxed cell.

**Row 1: `bd2_n1 = NOT( bd2_qb OR (e_b AND bd2_a) )`**

- Ground land 16028-16075 x 15505-15545, contact 16047,15522. Column x 16018-16100.
- Upper band y 15555-15578, gate `bd2_a` (pad and contact 16114,15560). Lower band
  y 15603-15625, gate `e_b` (east to the tap 16167,15605). Output strip y 15628-15657.
- Third pull-down, gate `bd2_qb`: the ground land has an arm west along y 15537-15552
  (tan and unbroken under the rail from x 16010 to the land: no edge between), which
  turns down at x 15942-15978, passes under the bar of the L-shaped poly
  (15908-15992 x 15558-15587) and returns east along y 15638-15657 into the output
  strip (tan and unbroken under the rail from x 16011 to 16059 at y 15640-15652).
  Evidence that this loop is diffusion and the pocket inside it (15978-16020 x
  15590-15637) field: in chip 2's stripped shot R-G is +13 to +21 on the loop and -5 in
  the pocket (field reference +1); the same order in both metal shots
  (`bd2_patch.py`, patches T4-T8 in the second run). The loop's left edge (x 15937)
  crosses the bar, and the bar is brighter over the loop than over field in three shots.
  This is the first run's reading (E); reading (A), the bar as the load, is out.
- Load: the output diffusion continues south (x 15962-15981 to y 15708); the strip from
  the VCC land joins it along y 15682-15704 under the poly block 15902-15952. That poly
  (y 15664-15735) runs on east as the band y 15712-15747, the gate of row 2. A finger of
  the band (15986-16008 x 15658-15712) ends in a boxed cell with a light centre
  (15988-16006 x 15660-15680) on the output diffusion: the tie, and the cross-coupling
  of `bd2_n1` into row 2.
- Output to G1: buried contact at the strip's east end (box 16102-16118 x 15644-15654,
  bar x 16130-16134 down into the band): see G1.

**Rows 2-3: `bd2_qb = NOT( bd2_n1 OR (e_b AND bd2_c) )`**

- Ground land with contact 16047,15700; band y 15722-15747 (gate `bd2_n1`); output
  y 15750-15808; band y 15811-15831 (gate `e_b`, from the tap 16166,15822, rounded west
  end at x 16020); node y 15837-15853; band y 15857-15877 (gate `bd2_c`); ground land
  with contact 16047,15898. Read under the rail with `bd2_umap.py 15996 15660 16070 15912`.
- The output has an arm west under the rail (y 15778-15798) to the load: strip from the
  VCC land under the block 15902-15952 x 15778-15797; that poly (y 15757-15847) ends
  in the pad of contact 15925,15825, from which the metal x 15912-15935 goes up to the
  pad of the L-shaped poly of row 1 (contact 15925,15625). The pad's poly wraps a boxed
  cell (15956-15996 x 15800-15842) on the output's arm: the tie. Either way round (the
  cell as tie of the load, or the pad as part of the load gate) this metal is `bd2_qb`.

**G4: `bd2_a = NOT bd2_c`**

- The west end of the `bd2_c` band widens and turns down under the rail's edge
  (x 16004-16022, salmon from y 15858 to 15917 with one dark edge line at y 15882-15890)
  and crosses a strip that runs from row 3's ground land (x 16026 on) west to an output
  land 15958-15996 x 15890-15920.
- Load: block 15900-15956 x 15890-15909 over the strip from the VCC land, one poly with
  the bars above (y 15868-15884) and below (y 15918-15929); the lower bar turns down
  (x 15933-15952) to y 15975.
- The output diffusion goes south from the land (x 15966-15980) and ends in a boxed
  cell at 15966-15978 x 15956-15970, between the load gate's down-turn and the west end
  (x 15988) of a poly bar y 15955-15973. That bar runs east under the rail (field above
  and below it: a wire) to the pad of contact 16105,15962.
- `bd2_a`: thin metal from that contact up x 16093-16112 to the pad of row 1's upper
  band (contact 16114,15560). About 13 px wide where it crosses rows 1 and 3, 16 px
  between y 15668 and 15768 and below y 15900.
- **Inferred, not seen**: that the cell ties both the load gate and the bar to the
  output (drawn as one poly through a `?B`). The bar has no other driver and row 1's
  upper band no other source, and the alternative driver would short the latch
  (Ambiguity 2).

### Gate group right of the bundle (pull-downs traced, second run)

Diffusion column x 16312-16366 under the ground rail x 16312-16362
(`bd2_umap.py 16250 15404 16384 15850`).

- Upper gate, `bd2_nu = NOT( bd2_c AND e_b )`: ground land y 15422-15461 (contact
  16338,15432); band G_a y 15466-15488, gate `bd2_c` (pad and contact 16260,15473 at its
  west end); node; band G_b y 15509-15531, gate `e_b` (strip 2); `bd2_nu` y 15533-15565,
  widening east to x 16374. Boxed cell at its west end (16246-16296 x 15552-15572, three
  plain cells) with no poly leaving it. Load and destination not traced (east).
- Lower gate, `bd2_al_n = NOT( bd2_x OR (e_b AND bd2_m210) )`: ground land y 15596-15635
  (contact 16327,15612); band y 15638-15656, gate `bd2_x`, arriving from the east; the
  node `bd2_al_n` y 15663-15720 (arm east at y 15687-15708 to x 16374, arm west to the
  boxed cell); band G_d y 15726-15744, gate `e_b` (tap 16167,15735); node; band G_e
  y 15770-15788, gate `bd2_m210` (contact 16207,15778; the band also runs on east of
  the column); ground land y 15795-15831 (contact 16330,15812). Load not traced.
- `bd2_c`: metal pad on contact 16260,15473 and thin metal x 16270-16284 down to contact
  16274,15872 on the east end of row 3's lower band. It crosses both boxed cells.
  No contact there: the cell centres are cream in the clean shot (193-201/170-183/126-138)
  like diffusion under metal, not olive green like the footprints of the known contacts
  of these metals (154-165/167-183/96-103), although in the metal shots the centres are
  as bright as contact centres.
- East of the rail (seen in one 3x view, not traced): a poly bar 16395-16483 x
  15475-15498 in line with G_a, turning down at x 16465-16483 to y 15558; contact
  16450,15539 with a thin metal x 16444-16459 going down to contact 16450,15740; the
  wide vertical metal x 16489-16547 with a long contact strip.

## Bundle x 16100-16400: what is on each track

| x | Segment | Net |
|---|---|---|
| 16104 | 15560-15962 | `bd2_a`: contact 16114,15560 (row 1 upper band) to contact 16105,15962 (G4's bar) |
| 16122 | 15384-15490 | `e_b`: contact 16122,15388 down to the corner into the lower trunk |
| 16169 | 15211-15443 | `bd2_n1` (upper trunk), contact 16167,15432 at its lower end |
| 16169 | 15470-17702 | `e_b` (lower trunk); taps 16167,15605 (row 1), 16167,15735 (G_d), 16166,15822 (row 3); scan gaps at about 16127, 16389, 17018-17044 are probably contacts |
| 16210 | 15296-15690 | `bd2_al_n`: contact 16210,15300 (G2's gate) to contact 16205,15690 |
| 16210 | 15771-16051 (16094 in chip 1) | `bd2_m210`: starts at contact 16207,15778 (band G_e); contacts seen at about 16210,15992 and 16210,16083 in a 1.2x survey |
| 16210 | 16424-16568, 16754-17745 | not identified |
| 16255 | 15947-15983, 16144-17300+ | not identified; contact at about 16255,16127 on a poly band going west |
| 16277 | 15466-15872 | `bd2_c`: contact 16260,15473 (G_a) to contact 16274,15872 (row 3's lower band) |
| 16299 | 16033-17569 | `rw_d` per trunks.md; **top end at contact about 16297,16040**, tap about 16298,16300 |
| 16342 | 15400-16330 | ground rail of the gate group (x 16312-16362) and its continuation; ends at a contact about 16343,16342 |
| 16342 | 16596-17515 | `rs_d` per trunks.md; **top end at contact about 16342,16605** |
| 16385 | 16138-17569 | `cs_d` per trunks.md; **top end at contact about 16386,16171**, tap about 16386,16430 |

## Ports

| Name | Layer | Crosses at | Direction | What |
|---|---|---|---|---|
| `sel_stb_r` | poly | x 15850, y 14825 (west) | driven here | write strobe gate of `sel` (G1 output) |
| `areg_load` | metal | x 16299, y 14700 (top) | driven here | address register load strobe (G2 output) = NOT `bd2_al_n` |
| `vcc` | metal | x 15795-15890, y 14700 and y 17100 | supply | rail shared with `sel` |
| `vcc` | metal | x 16142-16194, y 14700 (top) | supply | areg's inverter rail |
| `vss` (`areg_rail_r`) | metal | x 16401-16450, y 14700 (top) | supply | ground |
| `areg_w6` | metal | x 16341, y 14700 (top) | unknown | contact 16337,14866, poly down x 16330-16345 and on to the right-hand column (areg.md). Not drawn |
| `areg_w7` | poly | x 16364, y 14700 (top) | unknown | to the right-hand column. Not drawn |
| `e_b` | metal | x 16169, y 17100 (bottom) | from outside | E buffered; lower trunk |
| `bd2_c` | poly | x 16378, y 15477 (band G_a's east end, inside the region) | from outside the traced part | data input of the strobe latch; source not found |
| `bd2_x` | poly | x 16376, y 15647 | from outside the traced part | band arriving from the east |
| `bd2_m210` | metal / poly | metal x 16210 down to about y 16050; poly band G_e east of x 16376, y 15779 | unknown | |
| `bd2_nu` | diffusion | x 16374, y 15555 | driven here | goes east, not followed |
| ? | metal | x 16212, y 17100 | ? | track 16210, segment 16754-17745 |
| ? | metal | x 16257, y 17100 | ? | track 16255, runs up to about y 16144 |
| `rw_d` | metal | x 16298, y 17100 | from outside | per trunks.md |
| `rs_d` | metal | x 16342, y 17100 | from outside | per trunks.md |
| `cs_d` | metal | x 16385, y 17100 | from outside | per trunks.md |
| ? | metal | x 16016-16026, y 17100 | ? | thin line where the ground rail was; not looked at |
| ? | metal, 49 wide | x 16492-16540, y 17100; x 16505-16540 at y 14700 | supply? | wide vertical of the right-hand column, whole height |
| ? x 6 | metal | x 16580, 16624, 16668, 16711, 16755, 16799 at y 17100 | ? | six lines on a 43.5 px pitch leaving south |
| ? | metal | x 16837 (faint), 17001 at y 17100 | ? | |
| ? | metal | x 16586, 16621, 16732, 16816, 16950, 16992 at y 14720 (top) | ? | lines of the right-hand column continuing into areg's untraced part |
| ? | metal | x 17000 (east), y about 14694, 14728, 14761, 14798, 14834, 14916, 14992, 15022, 15096, 15175, 15199, 15323, 15532, 15674, 15741, 15796, 15844, 15936, 16106, 16215, 16508, 16580, 16632, 16685, 16759, 16984, 17010, 17048, 17085 | ? | raw output of `sel_cut.py v 16995`; not checked by eye |

The lists marked ? at the south, east and top edges come from `tools/sel_cut.py` only.

## Ambiguities

1. **The boxed cells.** Every tie of an output to poly in this block is a "boxed cell":
   one to three small plain patches inside a heavy outline, at the end of a diffusion,
   with a poly ending at or wrapping it. At 6x the buried-contact window itself cannot
   be told from its outlines, so each is a `?B` in the trace: row 1's output to the band
   for G1 (16100-16132 x 15636-15662), row 1's tie (15984-16010 x 15656-15684), rows
   2-3's tie (15956-15994 x 15806-15846), G4's (15962-15984 x 15952-15976), `bd2_al_n`'s
   (16262-16292 x 15682-15706). Each is taken as a poly-to-diffusion contact because the
   poly that ends there has no other driver (G1's gate, G2's gate, row 1's upper band)
   or is a load gate. G1's and G2's own output contacts look the same and are certain.
2. **Two boxed cells with no poly leaving them**: at the east end of `bd2_qb`
   (16088-16142 x 15764-15798, three plain cells; the mirror image of row 1's output
   contact about y 15716) and at the west end of `bd2_nu` (16246-16296 x 15552-15572).
   Not drawn. The thin metals `bd2_a` and `bd2_c` pass over them. If `bd2_a` had a
   contact on the first, `bd2_a` would be `bd2_qb` and row 1 would reduce to
   `NOT bd2_qb`: the latch could then be set and never cleared, and G4's output would
   be shorted to it. If `bd2_c` had a contact on the second, `bd2_c = NOT(bd2_c AND e_b)`.
   Neither makes a circuit, and the clean shot shows no contact footprint on either
   (and none under `bd2_a` where it widens at y 15753-15762: tan, not olive; but that
   patch is small). Working assumption: unused cells, no contact. What would settle it:
   a sharper photo, or tracing `bd2_nu`'s and `bd2_c`'s other ends.
3. **`bd2_a` across rows 1 and 3** is only a 3-6 px bright core in the metal shots
   between y 15566-15668 and 15800-15898 (R 140-200), dark where it crosses the two
   boxed cells. Taken as one metal from 16114,15560 to 16105,15962 because the clean shot
   has a protected (pink) strip under it all the way and the core is metal-yellow over
   the orange band at y 15606 in both chips. No contact on rows 1 or 3's bands (salmon
   unbroken under it).
4. **Loads of G1 and G2**: the VCC lands under the rail are shared with the loads of
   `sel`'s right-hand column on the other side of the rail (`sel.txt` draws those
   schematically). The strips from the lands to the load blocks are drawn from edge
   lines seen in the metal shot.
5. **areg.md, "seen below the region"**: the poly from contact 16252,14862 does not
   reach the contact at 16255,15085 (see G1), and the metal below 16255,15085 does not
   continue as `e_b`: it ends at 16167,15432. And `areg_load` is not NOT E (G2).
6. **trunks.md** has `rs_d` on the metal x 16333-16352 "above 15900, not followed" with
   a tap at y 16335. The track is empty between about y 16345 and 16596: `rs_d`'s metal
   ends at the contact about 16342,16605, and the metal above y 16342 is the lower end
   of the gate group's ground rail, ending on a contact about 16343,16342 (1.2x survey).
7. **Ground rail x 16008-16058 below y 16600**: the scans show several short gaps
   (16655-16679, 16797-16815, 16921-16975, 17053-17112 in chip 2, none of them in chip 1
   above 17049). Drawn continuous to y 17050.

## Not done

- **Source of `bd2_c`** (the latch's data input). Its net: band G_a (16250-16378 x
  15466-15488), pad/contact 16260,15473, thin metal x 16270-16284, contact 16274,15872,
  row 3's lower band, G4's gate. No driver found on it. Look first at G_a's east end
  (x 16364-16395): a poly bar 16395-16483 x 15475-15498 lies in line with it.
- **Loads of `bd2_nu` and `bd2_al_n`**, where `bd2_nu` goes, the sources of `bd2_x`
  (band y 15638-15656 from x 16376 east) and `bd2_m210` (band G_e east of x 16376;
  metal x 16200-16222 from 16207,15778 down to about y 16050).
- **Left column below y 15990: where R/W, CS and RS act** (located in a 1.2x survey,
  view `sv4.png`; nothing traced). The column repeats about every 260 px:
  - ground land y 15990-16026 with a contact about 16044,16004; gate band y 16032-16047
    whose poly runs east to the contact about 16297,16040 = **top end of `rw_d`**;
    diffusion below it from y 16056;
  - poly band at y about 16127 from the column east to a contact about 16255,16127
    (metal x 16255 from there down);
  - poly band at y about 16171 from x 15973 east across the column and the bundle to the
    contact about 16386,16171 = **top end of `cs_d`**;
  - the same three again 260 px lower: band to `rw_d`'s tap 16298,16300; band at
    y about 16342 to the contact 16343,16342 (end of the gate group's ground metal);
    band at y about 16385 to a contact about 16211,16386; band at y about 16430 to
    `cs_d`'s tap 16386,16430;
  - a third group from y about 16480: contacts at about 16255,16558, 16210,16602 and
    **16342,16605 = top end of `rs_d`**.
  - Loads of these rows are west of the rail at x 15900-15990 as in rows 1-4 (the VCC
    land continues); `tools/bd2_umap.py 15996 15876 16072 16070` already shows the first
    row under the rail.
- **Right-hand column** (x 16480-16800, y 14700-16450) and the routing east and south of
  it: not looked at. `areg_w6`, `areg_w7`, and probably `bd2_c`, `bd2_x`, `bd2_m210` go there.
