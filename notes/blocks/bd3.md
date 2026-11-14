# Below the register-select gates (`bd3`, x 14100-15900, y 16550-17100 and along the wires)

## Status

- Traced and extracted (trace/bd3.txt, `@requires sel`, 0 errors, no open nets): the
  strobe's two lines and the link between them; the row at y 16740-16870 (a two-inverter
  buffer of rsel12); two more inverter + NOR pairs in the right-hand column (write
  strobes of R12 and R13); all 16 tracks down to where they leave the region, including
  the nested corners and supply-rail crossings of T0-T6.
- The strobe has **no driver inside this region**. It enters from the east in poly at
  (15850,14825) (sel's port).
- Not traced: anything south of y 17100 except T3-T6's corners; the loads of the two new
  right-hand pairs are the schematic (`?`) loads of sel's cell `sel_rwr`.

## Inventory

| What | Where | Notes |
|---|---|---|
| Gate column, last row | x 14290-14930, y 16740-16870 | two inverters in series (not the inverter + NOR of the rows above): right half first stage, left half second stage |
| Ground rails of the gate column | x 14434 and 14789 | both end at y 16876 |
| Supply rail of the gate column | x 14584-14634 | runs on south past y 17300; by scan (sel_tracks) it reaches the VCC band of the input row at y 18130 |
| Wide rail | y 16907-16954, x 14060-14634 | joins the supply rail at its east end (seen at 1.1x and 1.65x, no dark line between); so `vcc`. Runs on west of x 14060 and turns north near x 13970-14030 |
| Strobe link | poly, contact 14239,16865 - x 14242 south - y 16996 east - contact 14673,16997 | joins `sel_stb_l` to T0 (`sel_stb_r`) |
| Horizontal bundle | y 16998-17258 (and on to 17432), x < 14912 | T0-T6 after turning west, pitch 43.3. Each crosses the supply rail in poly between two contacts (x 14672/14713 east, 14456/14499 west, alternating) |
| Right-hand gate column | x 15540-15890, y 16540-17130 | cell `sel_rwr` (from sel.txt) twice more: dy 600 (R12) and dy 900 (R13) |
| Track shuffle | x 15214-15344, y 16860-17040 | T8, T9, T10 each step one track left where the track to their left has ended |

## Logic

Traced (extracted by netlist.py) unless marked believed.

### The strobe

`sel_stb_l` and `sel_stb_r` are one net (traced):
- `sel_stb_l` (metal x 14307) turns west at y 16739 below the R7 NOR's contact, runs to
  x 14239 and down to a contact at (14239,16865) on a poly pad.
- The poly runs south along x 14242 under the wide rail to y 16996, then east along
  y 16996 (y 16987-17005) under the supply rail to a contact at (14673,16997).
- T0 (`sel_stb_r`, x 14912) comes down, turns west at y 16998 and ends on that contact.

The trace declares `@alias sel_stb_r sel_stb_l`.

Loads of the strobe in sel + bd3: the 16 NOR gates (R0-R15 except none missing: R0-R11
in the gate column, R14, R15, R12, R13 in the right-hand column). Nothing else. T15
(x 15561) ends at the R13 NOR's contact (15560,17072). T0 has no tap between y 16700
and its end. **No gate in this region drives the strobe**: its only other end is the
poly that arrives from the east along y 14825 at x 15850 (sel's port), so the driver is
east of x 15850 (package bd2).

### R12 select buffer (row y 16740-16870)

    bd3_n12 = NOT rsel12        (right half; pull-down W/L 134/22, weak load 27/56)
    bd3_b12 = NOT bd3_n12       (left half;  pull-down W/L 135/22, load 64/31)

- Input: T8's upper part (rsel12) ends at a contact at (15258,16668). Poly from it goes
  west along y 16668, south along x 15196, then west along y 16778 under tracks T7..T0
  (no contacts; 3.6x view) and is the gate bar of the first inverter, under the right
  ground rail.
- First inverter's output: buried contact at (14860,16820), poly east, south along
  x 14912 (directly under T0's metal, no contact), west along y 16910 across the supply
  rail and under the top edge of the wide rail to a pad at (14305,16867); metal up to a
  contact at (14306,16778) on the gate bar of the second inverter.
- Second inverter's output: buried contact at (14365,16822), poly west along y 16822,
  then south along x 14199 under the wide rail and all the horizontal lines. Seen to
  y 17320, still going.
- Both loads hang from one supply contact at (14609,16790).
- Believed: this is the read enable of R12, as `sel_b14`..`sel_b17` are for R14-R17.
  It leaves southwards on its own instead of on a bundle track.

### Right-hand gate column, continued

    sel_n12 = NOT rsel12     sel_w12 = NOR(sel_n12, sel_stb_r)     gates at y 16556; 16682, 16772
    sel_n13 = NOT rsel13     sel_w13 = NOR(sel_n13, sel_stb_r)     gates at y 16856; 16982, 17072

- rsel12: contact (15258,16560) on T8, poly east (in sel.txt).
- rsel13: T7 ends at a contact at (15214,16864); poly east along y 16862 to the inverter.
  **The same poly also runs south** from the pad along x 15216, directly under the metal
  that occupies T7's line below y 16902 (which is sel_w12). Seen to y 17120, still going:
  a second use of rsel13, not followed (believed: its buffer, like R12's).
- Strobe gates: contacts on T15 at (15560,16772) and (15560,17072); T15 ends there.
- Outputs: poly west along y 16732 to a contact at (15258,16734) (T8's lower part starts
  there), and along y 17032 to a contact at (15344,17036) (a new line starts there on
  T10's x).

So R12 and R13 have ordinary write strobes, and rsel12 (traced) and rsel13 (believed)
each have a buffered copy as well.

### Where each track goes

| Track | x at y 16550 | Net | Below y 16550 |
|---|---|---|---|
| T0 | 14912 | sel_stb_r | down to y 16998, west to contact (14673,16997), poly on to sel_stb_l. Ends |
| T1 | 14954 | sel_w5 | corner at y 17041; contacts (14713,17040), (14499,17040); west along y 17041 |
| T2 | 14998 | sel_w3 | corner y 17084; contacts (14672,17084), (14456,17084); west along y 17084 |
| T3 | 15041 | sel_w8 | corner y 17128; contacts (14713,17127), (14499,17127); west |
| T4 | 15085 | sel_w9 | corner y 17172; contacts (14672,17171), (14456,17171); west |
| T5 | 15128 | sel_w11 | corner y 17215; contacts (14713,17214), (14499,17214); west |
| T6 | 15171 | sel_w10 | corner y 17258; contacts (14672,17257), (14456,17257); west |
| T7 | 15214 | rsel13 | ends at contact (15214,16864) |
| T8 | 15258 | rsel12 | ends at contact (15258,16668). From contact (15258,16734): sel_w12, down to y 16910, steps west to x 15214, south |
| T9 | 15301 | sel_w14 | down to y 16955, steps west to x 15258, south |
| T10 | 15344 | sel_w15 | down to y 16998, steps west to x 15301, south. From contact (15344,17036): sel_w13, south |
| T11 | 15388 | sel_b16 | straight south |
| T12 | 15431 | sel_b17 | straight south |
| T13 | 15474 | sel_b15 | straight south |
| T14 | 15517 | sel_b14 | straight south |
| T15 | 15561 | sel_stb_r | ends at contact (15560,17072) |

By scan only (sel_cut.py, not drawn): the lines on x 15214, 15258, 15301, 15344 also
turn west, at y 17302, 17346, 17388, 17432, and cross the supply rail the same way
(pads at x 14713/14499 for 17302 and 17388); at x 14110 there are lines at every
43.3 px from y 16998 to 17432. At the west end the bundle turns north in nested corners
(y 16998 line at x 13957, y 17042 line at x 13915; one 3x view).

## Ports

| Name | Layer | Crossing | Direction | What |
|---|---|---|---|---|
| sel_stb_l = sel_stb_r | metal | 14307,16550 and 14912,16550 and 15561,16550 (top) | in (from sel) | strobe; one net |
| rsel12, rsel13, sel_w*, sel_b* | metal | tracks at y 16550 (top) | in | see the track table |
| sel_w7 | poly | 14100,16875 (west) | out | turns west at y 16875 (from x 14135) |
| bd3_b12 | poly | 14199,17100 (bottom; drawn to 17300) | out | rsel12 buffered; seen to y 17320 |
| rsel13 | poly | 15216,17100 (bottom; drawn to 17300) | out | under the metal of sel_w12 |
| bd3_x14543 | metal | 14100,16998 (west) and 14543,17100 (bottom) | ? | a through line, not one of the tracks: see Ambiguities |
| sel_w5 | metal | 14100,17041 (west) | out | |
| sel_w3 | metal | 14100,17084 (west) | out | |
| sel_w8 | metal | 14100,17128 (west) | out | below the region's bottom edge |
| sel_w9 | metal | 14100,17172 (west) | out | |
| sel_w11 | metal | 14100,17215 (west) | out | |
| sel_w10 | metal | 14100,17258 (west) | out | |
| sel_w12 | metal | 15214,17100 (bottom) | out | |
| sel_w14 | metal | 15258,17100 (bottom) | out | |
| sel_w15 | metal | 15301,17100 (bottom) | out | |
| sel_w13 | metal | 15344,17100 (bottom) | out | |
| sel_b16 | metal | 15388,17100 (bottom) | out | |
| sel_b17 | metal | 15431,17100 (bottom) | out | |
| sel_b15 | metal | 15474,17100 (bottom) | out | |
| sel_b14 | metal | 15517,17100 (bottom) | out | |
| vcc | metal | 14584-14634, 17100 (bottom); 14060, 16907-16954 (west) | - | supply rail and the wide rail |
| vss | metal | 15663-15718, 17100 (bottom) | - | ground rail of the right-hand column runs on |
| vcc | metal | 15795-15890, 17100 (bottom) | - | supply rail of the right-hand column runs on |

## Ambiguities

- **`bd3_x14543` and the strobe.** A metal line comes up from the south at x 14543
  (by scan from y ~18093, just above the input row's VCC band), turns west at y 16998
  and runs to x 13957, where it turns north. For 300 px (x 14250-14553) it lies exactly
  on top of the strobe's poly. No contact ring is visible anywhere along it in `metal`
  or `metal1` (3.8x), and the trace has none, so the two are separate nets. Against:
  the line occupies the place T0 would have in the bundle west of the supply rail, and
  the poly under it looks darker in `acid1b` at x 14235-14390 than poly under metal
  usually does (but so does poly under the supply rail, where there is certainly no
  contact). For: rsel13's poly runs under sel_w12's metal and `bd3_n12`'s poly under
  T0's metal in the same way, so poly under foreign metal is this layout's habit.
  Settle by tracing the line's ends (south end near 14543,18093; north along x 13957).
- sel.txt draws `sel_stb_l`'s metal straight down to y 16760; it really turns west at
  y 16739. Harmless (the overshoot touches nothing).
- Loads of `sel_rwr` (R12, R13 pairs) are sel's schematic `?` loads; at 1.3x the real
  load blocks are where the cell puts them. Exact outlines not traced.
- Pull-down diffusion of the two buffer inverters: the gate bars extend 50-70 px
  beyond the ground rail on the outer side with only slivers of diffusion visible above
  and below them; drawn as full-width transistors (W about 135). W is uncertain by 30%.

## Not done

- The strobe's source, east of x 15850 along y 14825.
- Where `bd3_b12` (poly x 14199, south of y 17320) and rsel13's poly (x 15216, south of
  y 17120) go.
- The tracks south of y 17100 and the west-going bundle beyond x 14100.
- The right-hand column below y 17130.
