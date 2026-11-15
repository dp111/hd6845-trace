# bd1: logic and routing channel left of the register-select gates (x 13000-14100, y 14700-17100)

Trace: `trace/bd1.txt` (`@requires sel`, `@requires bd3`). Coordinates are metal-shot pixels.

## Status

- Traced, extracted (0 errors, 0 warnings, no open nets) and checked by overlay: the route
  of every write strobe that enters the region (those of R0 to R7 all leave north on the
  track bundle, R8's leaves west in poly); the two big inverters at the top of the gate
  column, both driven by trunks' line X; X's own driver (one inverter, y 16125-16280);
  the rails of the gate column; 13 of the 18 tracks from the top edge to where they end
  or as far as they run straight.
- **The region is mostly a routing channel**, not logic: 18 vertical metal tracks
  (x 13088-13826) with poly cross-unders. The gates are a single column at
  x 13700-14080, y 15100-16900, of which three inverters are traced.
- NOT traced: the rest of the gate column (y 15350-16125 and 16280-16900) and about half
  of the channel wiring. See Not done; scans of the untraced tracks are tabulated there.

Boundary with `mra`: the mid-right array's own lines end with the `ck_a` rail at
x 13013-13037 (trunks). Everything from the track at x 13088 eastwards belongs to this
channel. There is no separate "bus at x 13000-13320": the lines there are tracks k0-k5
of the channel (k0-k3 are write strobes going north). Poly lines cross the boundary
westward under the `ck_a` rail at several y (ports table).

Reading coordinates off a view: a grid line is at the left edge of its label, and in a
two-panel image the right panel has its own origin (subtract the panel's offset before
dividing by the scale). `tools/sel_cut.py h Y x0 x1 --brief` gives track centres to 2 px
and is the quickest check.

## Inventory

| What | Where | Notes |
|---|---|---|
| Track bundle | x 13088 + 43.4 k, k = 0..17 (k17 = 13826), entering at y 14700 from the north | 18 metal lines, 20 wide. South of y 14850 they end, jog one or more tracks sideways (nested corners) or duck under each other in poly |
| Strobe polys from sel | y 14867, 14909, 14957, 15001, 15043, from x 14100 west | each ends on a contact under the track that takes it north |
| Wide rail from the north | x 13910-13958, y < 15246 | `vss`; ends in an arm (y 15215-15246) to the column's ground rail |
| Ground rail of the gate column | x 13826-13870, y 15100 to about 16760 | between y 15833 and 15991 it is replaced by two narrow lines (not traced), so the lower part is named `vss` from its pull-downs only |
| Supply rail of the gate column | x 13997-14044, y < 16960 | `vcc`: every load of the column ends on it. By scan it is continuous from y 14600 to 16960, where bd3's wide rail (y 16907-16954) arrives |
| Inverter pair on X | x 13765-14050, y 15120-15350 | two inverters, one ground contact between them (13838,15237) |
| (not traced) | x 13700-14050, y 15350-15880 | gates; receives polys from the channel at y 15671, 15713, 15887 and a line ending at (13713,15760) |
| (not traced) dense group | x 13740-13960, y 15880-16125 | `ck_out`'s tap at (13716,15930) enters here; several gate bars 20 px apart under the rail; a metal from X's driver ends here at a contact near (13928,15916) |
| X's driver | x 13760-14050, y 16125-16280 | one inverter; input poly arrives along y 16231 |
| (not traced) | x 13700-14050, y 16280-16900 | gates; `ck_out` taps at (13716,16490), (13716,16565), (13715,16711) |
| ck_out rail | x 13703-13727, y 15930-16711 | drawn in trunks.txt, not here |
| Bottom bundle | y 16862-17128, x 13380-14100 | strobes from bd3 turning north or west; line X's corner |

## Logic

Traced (extracted by netlist.py) unless marked believed.

### Where the write strobes go

Every strobe that enters was followed to where it leaves. None of them feeds a gate
in this region.

| Strobe | Enters | Route | Leaves |
|---|---|---|---|
| sel_w6 | poly, (14100,14867) | west to contact (13088,14867) | north, track k0 (13088,14700) |
| sel_w1 | poly, (14100,14909) | contact (13785,14913) | north, k16 (13782,14700) |
| sel_w2 | poly, (14100,14957) | contact (13609,14956) | north, k12 (13608,14700) |
| sel_w0 | poly, (14100,15001) | contact (13652,15000) | north, k13 (13652,14700) |
| sel_w4 | poly, (14100,15043) | contact (13521,15042) | north, k10 (13521,14700) |
| sel_w7 | poly, (14100,16864) | contact (13958,16861); metal west along y 16862; contact (13480,16864); poly west, diagonally up-left, north to contact (13218,16642); metal north on x 13218; jog west at y 15390 to x 13174 | north, k2 (13174,14700) |
| sel_w5 | metal, (14100,17041) | north at x 13915, west along y 16954, north at x 13435 to contact (13435,16908); poly west along y 16905, north at x 13164 to contact (13174,16730); metal north on x 13174 to contact (13175,15562); poly link to contact (13085,15563); metal north on x 13088; jog east at y 14912 to x 13131 | north, k1 (13131,14700) |
| sel_w3 | metal, (14100,17084) | step up at x 13832 to y 17041, west, north at x 13522 to contact (13522,16995); poly north at x 13518 (under sel_w7's metal) to contact (13522,16820); metal north on x 13521 to contact (13521,16455); poly west along y 16453 to contact (13262,16456); metal north on x 13261; jog west at y 15346 to x 13218 | north, k3 (13218,14700) |
| sel_w8 | metal, (14100,17128) | contact (13392,17126); poly west along y 17125 under every vertical line | west, (12985,17125), poly, still running |
| sel_w9 | metal, y 17172 | below the region; by scan the metal runs west to x 13471 | not followed |
| sel_w11 | metal, y 17215 | by scan to x 13414 | not followed |
| sel_w10 | metal, y 17258 | by scan to x 13471 | not followed |

So the strobes of R0 to R7 all go north in the bundle (towards the right datapath;
believed). The order on the tracks is k0 w6, k1 w5, k2 w7, k3 w3, k10 w4, k12 w2,
k13 w0, k16 w1. R8's goes west in poly; R9, R10, R11's were not followed.

The poly at y 14912 **west** of x 13712 is not sel_w1: sel_w1's poly ends at its
contact (13785,14913); a second poly starts 56 px further west on a contact under
track k14 and runs west, south (x 13133) and west again along y 15020 into the
mid-right array (`bd1_k14`).

### Line X: its driver and the two inverters it feeds (traced)

X is the line of `notes/blocks/trunks.md` (input of input-row gate 0, whose output S
is distributed over the whole die). Here it is `bd1_x`.

```
bd1_x   = NOT bd1_g       X's driver, y 16125-16280
bd1_xn1 = NOT bd1_x       upper inverter, gate bar y 15183-15203
bd1_xn2 = NOT bd1_x       lower inverter, gate bar y 15271-15291
```

- **X's driver** is one inverter. Pull-down: gate poly `bd1_g` crossing the diffusion
  under the ground rail diagonally (x 13817-13888), ground contact at (13855,16250).
  Output diffusion above the gate; it reaches X three ways: a buried contact at
  (13762-13800, 16170-16210) to the tap poly that runs west to the contact (13672,16190)
  on X's metal; a metal contact at (13917,16155) to a line going north into the dense
  group (ends at a contact near (13928,15916), not traced); and a strip down the west
  side of the load. Load: poly block x 13953-13991, y 16140-16265, tied to the output by
  a buried contact at its top (13953-13985, 16142-16174), supply contact (14017,16228).
  W/L of the load 68/37; of the pull-down 90/24 as certain, up to 188/26 with the two
  uncertain pieces (Ambiguities).
- `bd1_g` is on a metal line at x 13630 with a contact at each end. Top end,
  (13629,15673): a poly goes east into the gate column along y 15671, crosses a 30 px
  wide diffusion strip (x 13772-13802, lying under the metal line on x 13782) and ends
  at x 13805 (5x view): so g is the **gate** of a small transistor there, not an output.
  Bottom end, (13629,16150): the line ducks under X's horizontal metal in poly to a pad
  with a second contact, (13629,16235), from which the gate poly of X's driver runs east
  and a metal goes on south (not followed). **What drives g was not found; it must be
  south along x 13630.**
- **X's metal** on track k11's position starts at the contact (13567,15193): that is
  its top end. A second contact 88 px lower, (13567,15281). Each goes to a poly bar
  running east, and each bar is the gate of one inverter: pull-down W/L 131/20, load
  70/38 (poly block next to the supply rail, tied to the output by a buried contact).
  The two share the ground contact (13838,15237) between the bars.
- `bd1_xn1` leaves west in poly (buried contact 13766-13798, 15144-15173; poly along
  y 15151) to a contact at (13347,15150) where **track k6 ends: it goes north**.
- `bd1_xn2` leaves west in poly (buried contact 13766-13797, 15303-15333) to a contact
  at (13695,15325); metal south to (13700,15452), where one arm goes to a contact at
  (13655,15453) (poly west along y 15455 to a contact at (13520,15455), then metal south
  on x 13521 to a contact at (13520,15931), not traced further) and the other runs south
  on x 13716 to a contact at (13713,15760) in the gate column (not traced).

Believed: X, S (= NOT X, made by input-row gate 0), `bd1_xn1` and `bd1_xn2` are four
separately buffered copies of one clock-like signal `NOT bd1_g` and its inverse; all
three inverters here are the same size.

### Tracks traced so far

| Track at y 14700 | Net | What happens to it |
|---|---|---|
| k0 13088 | sel_w6 | ends at contact (13088,14867) |
| k1 13131 | sel_w5 | jogs to x 13088 at y 14912, down to contact (13085,15563) |
| k2 13174 | sel_w7 | jogs to x 13218 at y 15390, down to contact (13218,16642) |
| k3 13218 | sel_w3 | jogs to x 13261 at y 15346, down to contact (13262,16456) |
| k4 13261 | bd1_k4 | jogs to x 13304 at y 15308; by scan runs on past y 16700 |
| k5 13304 | bd1_k5 | jogs to x 13348 at y 15262, down to contact (13348,16411); poly east along y 16410 towards the gate column (seen to x 13700 at 0.9x, not followed) |
| k6 13348 | bd1_xn1 | ends at contact (13347,15150) |
| k10 13521 | sel_w4 | ends at contact (13521,15042) |
| k12 13608 | sel_w2 | ends at contact (13609,14956) |
| k13 13652 | sel_w0 | ends at contact (13652,15000) |
| k14 13694 | bd1_k14 | ends at contact (13692,14913); poly west into the mid-right array at y 15020 |
| k16 13782 | sel_w1 | ends at contact (13785,14913) |
| k17 13826 | bd1_k17 | jogs to x 13782 at y 14975, down to y 15131, west to x 13696, contact (13697,15239); poly west along y 15238 to contact (13131,15235); metal south on x 13131 to contact (13131,16413); poly on into the mid-right array (trunks: along y 16440-16462) |

k7, k8, k9, k11, k15: Not done.

## Ports

| Name | Layer | Crossing | Direction | What |
|---|---|---|---|---|
| sel_w6, sel_w1, sel_w2, sel_w0, sel_w4 | poly | x 14100, y 14867 / 14909 / 14957 / 15001 / 15043 (east) | in | from sel |
| sel_w7 | poly | 14100,16864 (east) | in | from bd3 |
| sel_w5, sel_w3, sel_w8 | metal | x 14100, y 17041 / 17084 / 17128 (east) | in | from bd3 |
| sel_w6 | metal | 13088,14700 (north) | out | track k0 |
| sel_w5 | metal | 13131,14700 (north) | out | track k1 |
| sel_w7 | metal | 13174,14700 (north) | out | track k2 |
| sel_w3 | metal | 13218,14700 (north) | out | track k3 |
| bd1_k4 | metal | 13261,14700 (north) | ? | track k4 |
| bd1_k5 | metal | 13304,14700 (north) | ? | track k5 |
| bd1_xn1 | metal | 13348,14700 (north) | out | track k6: NOT X |
| (k7, k8, k9) | metal | 13391 / 13435 / 13478, 14700 (north) | ? | not traced |
| sel_w4 | metal | 13521,14700 (north) | out | track k10 |
| (k11) | metal | 13565,14700 (north) | ? | not traced; by 1.5x view it jogs to x 13608 at y 15005, ends at a contact at (13609,15608), poly west then diagonally down-left towards (13250,15750) |
| sel_w2 | metal | 13608,14700 (north) | out | track k12 |
| sel_w0 | metal | 13652,14700 (north) | out | track k13 |
| bd1_k14 | metal | 13694,14700 (north) | ? | track k14 |
| bd1_k14 | poly | 13000,15020 (west) | ? | into the mid-right array's routing channel, under the `ck_a` rail |
| (not traced) | poly | 13035,15497 (west) | ? | the poly that lies along y 15385 turns south at x 13108 and leaves west here |
| (k15) | metal | 13738,14700 (north) | ? | not traced; scan: metal to y 15141 |
| sel_w1 | metal | 13782,14700 (north) | out | track k16 |
| bd1_k17 | metal | 13826,14700 (north) | ? | track k17 |
| bd1_k17 | poly | 12970,16451 (west) | ? | into the mid-right array (this last poly is `?`: from trunks' notes, not checked here) |
| sel_w8 | poly | 12985,17125 (west) | out | goes on west below the array's bottom row |
| bd1_x | metal | 13672,16610 (drawn to there) | out | line X; trunks.txt draws it from y 16600 south. Not labelled in trunks.txt: it reaches inrow's `t_g0_in` |
| bd1_x | metal | 13922,15905 (`?`) | ? | from the driver's output north into the dense group |
| bd1_g | poly | 13806,15671 (`?`) | out | gate of a transistor in the untraced group |
| bd1_g | metal | 13630,16300 (`?`) | in (believed) | going south; g's driver must be that way |
| bd1_xn2 | metal | 13716,15772 | out | to a contact at (13713,15760) in the gate column |
| bd1_xn2 | metal | 13521,15944 | out | line on x 13521 ending at a contact at (13520,15931) |
| vss | metal | 13910-13958, 14700 (north) | - | wide rail; named from the pull-downs it feeds |
| vcc | metal | 13997-14044, 14700 (north) | - | supply rail; joins bd3's wide rail at the bottom (by scan) |
| ck_out | metal | rail x 13703-13727, y 15930-16711 | in | trunks; its taps are not traced here |

## Ambiguities

- **Width of the pull-down of X's driver.** Certain: the gate poly crosses the
  diffusion under the rail (x 13817-13888). Uncertain, both drawn `?D`: (a) the poly
  ends east of the rail in a block (x 13886-13926, y 16183-16258) lying between the
  ground diffusion and the output strip, which would be a second channel (58 wide,
  38 long); (b) west of the rail the output diffusion (below the buried contact) and a
  heavy-outlined box (x 13759-13805, y 16247-16277) lie either side of the poly, as the
  source and drain strips do in the two inverters at the top, which would add 56 to the
  width. Neither changes the logic. To settle: a sharper photo; at 4.3x-5.6x the
  outlines are there but the continuity under the poly cannot be seen.
- **Is the ground rail one piece?** At y 15833-15991 the rail x 13826-13870 becomes two
  narrow lines. The lower part is labelled `vss` because pull-downs sit on it and the
  loads go to the other rail.
- The wide rail x 13910-13958 is called `vss` and the rail x 13997-14044 `vcc` from the
  orientation of the gates. The second is supported by bd3 (its wide rail y 16907-16954
  is traced to the input row's VCC band and turns north at x 13970-14030).
- The poly along y 15385 lies exactly under the 60 px metal jog of sel_w7 (x 13166-13225).
  No contact: both metal shots at 4x show plain metal there, and in `acid1b` the band
  shows no pad. That poly (from a corner at x 13108, where it goes south and then west
  into the mid-right array at y 15497, east to a contact near (13505,15385)) is not traced.
- X has **two** contacts at the top of its metal, 88 px apart, one per inverter gate
  bar, although the two bars could have been one poly. Both rings are plain in `metal`
  (2.9x) and the metal runs unbroken between them, so the two inverters do have the
  same input. They are separate gates with separate loads and outputs, not one
  double-width inverter: the outputs leave by different buried contacts to different
  wires and no diffusion or poly joins them.
- Contact pads look two ways in `acid1b` here: pale with a green centre, or a dark red
  box with a heavy outline (for example (13567,15281), (13522,16995), (13629,16235)).
  Both kinds have a plain contact ring in `metal`; both are treated as metal-to-poly
  contacts.

## Not done

Gate column (x 13700-14080). The photos are at their limit there: use
`tools/rdp3_sharp.py` at 2.9x for a group and 4.3-5.6x for junctions (plain view.py
was not readable).

- y 15350-15880: untraced. One sharpened 2.9x view of y 15570-15800 shows a compound
  group: a ground contact under the rail at (13845,15657); gate bars under the rail at
  y 15600-15621 and y 15741-15761; `bd1_g`'s gate on the strip at x 13772-13802 (above);
  a metal on x 13952-13972 ending at a contact at (13957,15738); a large supply land
  x 14000-14048, y 15577-15687 with several contacts. Seen elsewhere: a contact at (13781,15403) on a diffusion with a metal
  going south on x 13782; poly from contact (13655,15391) (the line on x 13652 from
  y 15081) going east then south along x 13720 under the metal; polys entering from the
  channel at y 15671 (`bd1_g`), 15713 (from contact (13674,15715)), 15887 (from contact
  (13432,15887)); `bd1_xn2`'s contact (13713,15760).
- y 15880-16125 (dense group): `ck_out` tap (13716,15930), poly east along y 15930 to
  x 13830; under the rail several poly bars about 20 px apart (y 15975-16050); a load
  at x 13955-13990, y 16005-16045 with supply contact (14018,16025); a contact near
  (13928,15916) where the metal from X's driver ends. Two passes at 2.6x and 4x gave no
  consistent circuit; one sharpened view (2.9x) is much better and is the way in.
- y 16280-16900: untraced. `ck_out` taps at (13716,16490), (13716,16565), (13715,16711).

Channel:

- Tracks k7, k8, k9, k11, k15, the lower end of k4 and where k5's poly (y 16410) goes.
- Lines that start inside the channel. Scan (`sel_tracks.py v`, metal present, y ranges;
  gaps of 20-26 px are usually a poly passing under): x 13435: 15251-15934, 15972-16769;
  x 13478: 15124-16594; x 13521: 15080-15398, 15415-15899, 15990-16273, 16445-16805;
  x 13565 below X: X itself to 16188; x 13608: 14992-15617; x 13652: 15081-15374;
  x 13630: `bd1_g`; x 13674: 15715-15973 (contacts at both ends; poly east at y 15713,
  poly west along y 15997 to a contact at (13522,15994)).
- Contacts seen at 0.9x and not traced (x,y): (13432,15887) (13520,15931) (13432,15960)
  (13523,16000) (13505,15385).
- The diagonals at x 13150-13450, y 16680-16890: three metal lines step two tracks east
  there (seen at 1.5x), sel_w7's poly passes under them.
- Bottom edge: a separate metal along y 17082 from contact (13480,17083) (poly going
  south) to contact (13698,17080) (poly coming down x 13690 from y 16840); a long
  vertical poly at x 13870-13885 passing under all the horizontal lines.
- sel_w9, sel_w11, sel_w10 west of x 14100 (they lie below y 17100).
