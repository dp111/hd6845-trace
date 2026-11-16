# tla: top-left logic, the gate cluster x 2450-3100, y 4600-5320 and its bus

Serial work, started 2026-11-16. Trace: `trace/tla.txt`. Views: `cache/scratch/tla/`.

## Names

In this note `in1`, `in2`, `in3`, `e3`, `e4`, `w2`, `c1`, `a2`, `b1`, `x1` are the signals
`rcs_in1` ... `rcs_x1` (`rcs_` = row counter step logic), `m2` is `rcs_cond_n`, and the
step signal is `rc_stepreq_n`. Bus line letters (A-G) and unit names are places, not signals.

## Status

Eighteen gates and one latch traced and extracted (52 transistors, no errors) in the first and middle
clusters; the rest is surveyed only. The first cluster runs from y 2940 to y 5330.

```
rc_stepreq_n = NOR(in1, in2, in3)        the row counter's step request (active low)   (2975,5035)
in2        = NOR(w2, e4)                 west column                                   (2571,5197)
in3        = NOR(e3, e4)                 east column                                   (3046,5197)
w2         = NOT c1                      pull-down under rail R1 itself                (2625,5066)
c1         = NOR(a2, b1)                 east column, top of the cluster               (3046,3115)
b1         = NOR(x1, a2, rcs_u3425)      east column; third pull-down west of the rail (3046,3590), (2920,3628)
rcs_u3425  = NOT rcs_bc3460              inverter; its output goes by a strap to b1's third gate
rcs_bc3460 = NOR(e3, e4)                 a second copy of in3's function               (3046,3892)
rcs_cond_n = NOR(in2, in3)               "m2": the step condition inverted              (3046,4765)
rcs_cond   = NOT rcs_cond_n              inverter on the column above; on bus piece A3   (3046,4636)
rcs_cond_lat <- rcs_cond while clk_tl  pass transistor latch (AMB-009)                (3046,4546)
rcs_u3288  = NOR(rcs_g3245, rcs_bd3330)                                                (3046,3288)
rcs_n4200  = NOT(rcs_cond AND clk_tl OR rcs_g4240)   AND-OR-INVERT under the rail (3008,4200)
in1        = NOR(rcs_mu, rcs_mv)         middle cluster                                (4081,4072)
rcs_mu     = NOT rcs_bq3335              middle cluster, inverter                      (4050,3374)
rcs_mn3852 = NOR(?, in1)                 middle cluster; second gate not read
```

Put together (b1 = NOT x1 AND NOT a2 AND NOT e3 AND NOT e4, so c1 = NOT a2 AND (x1 OR e3 OR e4)):

**step = in1 OR ( NOT e4 AND NOT (e3 AND a2) )**

and `m2` = e4 OR (e3 AND a2) is the complement of the bracket. `x1` cancels out of the step
(it still matters for `c1`, which also leaves the cluster westwards on the poly y 2985).
So: while `e4` is high only `in1` can step the row counter; while `e4` is low the counter
steps unless `e3` and `a2` are both high.

(Before the third pull-down of `b1` was found, on 2026-11-16, the formula read
`in1 OR (NOT e4 AND ((x1 AND NOT a2) OR NOT e3))`. That is superseded.)

What the inputs **are** is not known. None has reached a named signal yet:

| Signal | Followed to |
|---|---|
| `e4` | **17,000 px, all drawn, driver not found.** Bus line C middle piece (x 3196, y 3944-5677), east along y 5677, south at x 3527, contact (3565,5848), poly east along y 5847 to x 5285, south as line 5 of the poly bus x 5100-5290 to y 6850, diagonally to (5560,7122), east to a contact (6140,7124), metal east along y 7084, south at x 6769, contact (6730,8275), poly under six horizontal metals, contact (6730,8580), metal diagonally to x 6558, south down the left bus field (two steps west: x 6471 from y 9848, x 6300 from y 11880, x 6236 from y 12772), east at y 14528 to a contact (6411,14526), poly east to a contact (7012,14522), metal south to a contact (7055,15345), poly to the gate of a pull-down under the rail x 7290-7345 at (7317,15435) in bc1's untraced left column. **Five loads, all gates** (four in this cluster, one in bc1). See "The chase of e4" below |
| `e3` | bus line E, one piece y 2710-5166 with three contacts: (3283,5152) gate of in3; (3283,3852) a second gate (below); top (3283,2725), from which a poly runs east along y 2715-2735 to a pad (4270,2725) and a metal runs on **east along y 2718-2738** (pieces seen to x 5366; the three metals at y 2640, 2683 and 2728 run east in pieces, with cross-unders at the rails, as far as x 11700-12050, but tc1's notes show that pieces on one y are different nets) |
| `a2` | bus line A piece A2 (y 3166-3778): contacts (3108,3180) gate of c1, (3100,3632) gate of b1, (3103,3762) a poly that leaves **east along y 3752-3770** |
| `x1` | poly y 3538-3556 from the **east**, across the whole bus without a contact |
| `in1` | bus line G (x 3369, y 2754-4952), top contact (3368,2768), poly east along y 2768 to a contact (4225,2765), metal east and **south at x 4268-4290** (profile: unbroken to about y 4072; contact candidates at y 3898 and y 4090): into the middle or right gate column |

More of the east column (added 2026-11-17, extracted):

```
rcs_bc3460 = NOR(e3, e4)          unit at y 3892: a second copy of in3's function; its output
                                  goes up bus line C's upper piece to the unit at y 3425
rcs_u3425  = NOT rcs_bc3460       = e3 OR e4. An inverter: one pull-down, nothing above the node.
                                  Its load and its destination are in the dense part west of the rail
rcs_u3288  = NOR(rcs_g3245, rcs_bd3330)   unit at y 3288. Output up bus line C's top piece and west
                                  along y 2728 to about x 2822 (not looked at). rcs_g3245 comes from
                                  the east; rcs_bd3330 is a piece of bus line D (y 3330-4380)
```

Bus pieces now drawn: A1, A2, B (two pieces), C (top, upper, middle), D (y 3330-4380),
E (one piece y 2722-5158, three contacts), G upper.

**Where `in1` comes from (2026-11-17, extracted).** `in1`'s metal (bus line G of the first
field, the poly y 2768, then down the second bus field at x 4268-4290) ends on the output
of a unit of the **middle cluster** (x 3450-4110, the same construction 1042 px east: VCC
rail x 3824-3868, thin metal x 3948-3962, VSS rail x 3992-4041, units on a column east of
the VSS rail):

```
in1        = NOR(rcs_mu, rcs_mv)      unit at (4081,4072), with its load
rcs_mu     = NOT rcs_bq3335           inverter at (4050,3374): one gate, under the rail and on the column
rcs_mn3852 = NOR(?, in1)              the unit above in1's: in1 is one of its gates; output up x 4233 to y 2852
```

`rcs_mv` is a bus piece (x 4192, y 4112-4748) whose far end is a poly that leaves east and
south at (4283,4745); `rcs_bq3335` is a bus piece (x 4148, y 3320-3596). `e3`'s metal goes
east along y 2728 to x 4496, south to a contact (4490,3805), and on east in poly along
y 3805: towards the **right cluster** (x 4650-5050).

**What the step condition feeds (2026-11-17, extracted; one junction is AMB-009).**

```
rcs_cond     = NOT rcs_cond_n           = NOT e4 AND NOT (e3 AND a2): the bracket of the step formula
rcs_cond_lat <- rcs_cond while clk_tl is high      pass transistor: a dynamic latch
rcs_n4200    = NOT( rcs_cond AND clk_tl  OR  rcs_g4240 )
```

`clk_tl` is **the clock**: NOT `ck_out`, i.e. CLK polarity (identified 2026-11-17 by
following it to its driver and the driver's input to the clock trunk; before that it was
the placeholder with the former name `rcs_bb3807`). Its route: bus line B (y 3807-4552; gate contacts at y 3810,
4160, 4410, 4548), a poly east onto a piece of bus line D down to (3240,5587), a poly west
along y 5587 under the cluster's foot to (2458,5587), a thin metal 2,240 px south at
x 2457 to (2456,7822), and a poly into the output node of an **inverter** at (2626,7908)
in the left column beside upper row 2 of the left array (traced: a "rail gate" like `w2`'s,
load to the VCC rail x 2780-2832). The inverter's input pad (2500,7907) is on the
left-edge trunk of `ck_out`: `tools/follow.py` from there south follows one metal 17,238 px
down the left edge and along the bottom to the clock block's branch contact (8567,18946).
The trunk also goes on from the pad, west and 2,050 px north at x 2370, to a contact
(2365,5847) and a poly that gates a unit of the small cluster below this one and ends on a
contact (2745,5842): more `ck_out` loads, not followed.

So:

- the step condition is sampled into `rcs_cond_lat` **while CLK is high**, and in that same
  phase it can pull `rcs_n4200` low;
- the row counter's step request itself (`rc_stepreq_n`) is combinational in `in1`, `e3`,
  `e4`, `a2`.

The column was read from the chip-2 shots at 7x: where no metal lies over it, they show
the poly bands and the diffusion edges (as lines across the bands) far more clearly than
the clean shot.

So the step logic is spread over all three clusters. They are one block of about 75 small
gates and three bus fields, and they are being traced unit by unit from here on (no more
chasing of single signals).

## How the row counter's step signal gets here

`rc_stepreq_n` (see `notes/blocks/wl.md`, `notes/blocks/bw.md`) was followed from the block west of
the counters: west along the central datapath's channel 3, north, west through the crossing
field x 6330-7700, up the metal x 5841 to a contact (5838,5585), west as poly along y 5585
through a second crossing field to a contact (3518,5587), by metal west and north to a
contact (3283,5238), by poly east, north (under a bus line) and west along y 5018 to a
buried contact at (3056,5030) on the output node of the gate below. About 9,000 px of wire.

## Layout of the cluster

Three vertical rails: R1 x 2590-2640, **R2 x 2775-2830 = VCC**, **R3 x 2950-3000 = VSS**
(R1 not yet read). Pull-downs sit on diffusion boxes under R3, each box tied to the rail by
a contact, with horizontal poly gates; a second column of pull-downs lies just east of R3
(x 3030-3063) between arms of those boxes. Loads lie between R2 and R3: a diffusion strip
from a VCC box under R2, under a poly plate in the open (bright orange-red, textured), to
the gate's node. East of the cluster a vertical bus of seven metal positions (x 3097-3375,
pitch 43) carries signals between this cluster, the ones above and below it, and the poly
lines that run east. **The bus lines are in pieces**: each piece joins two or three poly
lines by contacts and ends plainly; two pieces can share one x.

Under the wide rails the clean shot shows field as pink with an olive stripe down the
middle (the class map paints it olive): that stripe is not diffusion. Diffusion under a
rail is the tan boxes only.

## The step gate (traced)

- Output node: a U of diffusion round the VSS contact box of R3 at y 4950-4998: top part
  y 4903-4927, strip x 2888-2905 on the west, bottom part y 5022-5050. So the three
  pull-downs are: `in1` (gate y 4929-4947, above the box), `in2` (gate y 5001-5020, below
  the box), `in3` (gate y 5055-5075, onto the next box down, contact (2987,5108)).
- Load: strip y 5018-5047 from the VCC box under R2 (contact (2805,5030)), plate
  x 2845-2875. The plate's poly runs up to y 4962; its tie to the node (a dark box at
  (2885-2908, 4958-4996) on the strip) is drawn uncertain.
- The node goes east in the open to a buried contact (box x 3045-3068, y 5015-5047) with the
  poly that carries `rc_stepreq_n` away.

Inputs (pieces of the vertical bus):

| Input | Gate poly | Bus piece | Other contacts on the piece |
|---|---|---|---|
| `in1` | y 4929-4947, pad contact (3360,4937) | line G, upper piece, x 3352-3378, y 2754-4952 | top contact (3368,2768): poly east along y 2758-2778 to a contact (4225,2765) on a vertical metal of the next bus field (x 4140-4420). Not followed further |
| `in2` | y 4970-4992 then south at x 3000-3012 into the band y 5001-5020; pad contact (3148,4976) | line B, y 4705-5428 | (3150,4719): gate E1 of `m2`; (3150,5412): poly west along y 5400-5422, not followed: its driver |
| `in3` | y 5055-5075, pad contact (3108,5068) | line A, y 4790-5212 | (3108,4805): gate E2 of `m2`; (3108,5197): the output of the gate `in3 = NOR(e3, e4)` |
| `e3` | y 5147-5167, pad contact (3283,5152) | line E, upper piece, ends here; comes from the north (seen from y 5060) | not followed |
| `e4` | y 5230-5250, pad contact (3192,5237) | line C; another contact on it at (3192,5325), and it turns east at y 5665-5690 | extent not read |



## The small NOR `m2` (traced)

Column x 3030-3063 east of R3, between the east arms of two VSS boxes (y 4690-4707 and
y 4820-4842). Gates E1 (`in2`, y 4709-4734) and E2 (`in3`, y 4796-4817); the node between
them has a buried contact (box x 3045-3068, y 4750-4780) to a poly that runs east along
y 4753-4772, north under bus line C (x 3186-3206) and back west along y 4626-4645, where it
is gate E0 on the upper part of the same column (VSS below it; what is above: next piece).
No load has been found on `m2`.

## The gate that makes `in3` (traced)

Same construction as `m2`, one rail box further down (column x 3030-3063, y 5122-5266,
between the east arms of the VSS boxes at y 5080-5140 and y 5258-5297). Gates E3 (`e3`,
y 5147-5167) and E4 (`e4`, y 5230-5250). The node between them goes three ways: a buried
contact (box x 3042-3068, y 5181-5214) to the poly that runs east to bus line A's bottom
contact; a diffusion strip **west under the VSS rail** (y 5186-5208, tan between two thin
dark lines in the clean shot) to a box under the thin metal; and from that box, by a contact
(2915,5250), up the thin metal x 2903-2923. The load is on the far side of that box: a strip
y 5188-5216 under a poly plate x 2842-2897 to the VCC box under R2 (contact (2805,5212)).
The plate is one piece of poly from y 5168 to y 5265 (it looks like two plates in the clean
shot because the strip's edges show through it); its tie to the node is drawn uncertain.

## The gate that makes `in2` (traced)

The west side of the cluster is the mirror image of the east side: R1 (x 2600-2650) is a
second VSS rail, the small NORs sit on a column just **west** of it (x 2550-2592), and
their loads lie between R1 and the VCC rail R2 under a second thin metal (x 2688-2708).
`in2`'s gate: column y 5120-5282 between the rail boxes at y 5080-5142 and y 5258-5297;
gates `w2` (y 5142-5164) and `e4` (y 5230-5250, from a pad with a contact (2497,5238)
under a metal that comes round from bus line C by the poly y 5312-5332 and a contact
(2565,5321)); output by a buried contact (box x 2548-2578, y 5182-5214) and a poly west to
a contact (2412,5196), metal south and east along y 5411, contact (2565,5410), poly east
along y 5400-5422 under the whole cluster to bus line B's bottom contact (3150,5412).
Load: strip east under R1, box under thin metal W, plate x 2722-2775, VCC box under R2.

## The chase of `e4` (2026-11-16/17)

`e4` gates the whole step logic, so naming it was the first aim. Result: its route is
drawn end to end and it is **not identified**. What was learnt on the way:

- **It is not RES**, though it looked like it for an hour. The RES line (`res_b`, metal
  x 5266-5290 from the pad buffers at the top) comes down the whole top-left logic without
  a tap and from y 5857 to y 6075 lies exactly on top of `e4`'s poly (bus line 5). Five
  shots at 5-9x and a colour profile every 6 px show no contact; the metal's last 20 px
  turn **west** along y 6055-6080 to a contact (5190,6065) on the pad of bus line 3. The
  overlap is routing (tracing guide, trap 8). `lpstb_b` ends the same way one line over:
  contact (5232,6105), bus line 4. Both are now drawn in `trace/trunks.txt`.
- So the poly bus x 5100-5290 (y 6060-6850) carries, west to east: two unidentified
  lines, `res_b`, `lpstb_b`, `e4`. All five fan out diagonally at y 6850-7350 to
  horizontal metals going east (pads at x 6130-6165). `e4` travels with the two input
  pins' signals from the top-left to the centre, which suggests (no more) that it is a
  signal of the same standing: a chip-wide control line.
- It is not the neighbouring gate's output either: `m2`'s poly runs under bus line C for
  120 px (y 4636-4762) with no contact (6.4x, three shots).
- The two crossing fields it passes in the left bus field (y 9560-9780 and
  y 10340-10660) give it no tap. In those fields the clean shot's colour under a metal
  varies from salmon to yellow-green from crossing to crossing, on whole rows at a time,
  so the contact-colour test (`tools/xfield.py`) is not usable there; a real tap has a pad.
- The 13-line bus of bc1 (y 14354-14873): its line y 14526 is **two nets**. The poly from
  the west ends on the pad (7012,14522) and goes south (`e4`); the line's continuation
  east starts on a separate pad (7100,14522) fed by a metal from the north. (I followed
  the eastern piece to a gate at (9480,15560) before noticing: not `e4`.)

Where its driver can still be: on one of the poly stretches as a branch I did not see
(the diagonal fan and y 7122, x 5560-6128, were only read at 1.1x), or at a contact with
a pad on the 4,000 px of metal in the left bus field that the profile tools did not flag.

## The thin metals and the dense part (open, 2026-11-17)

- **Thin metal E (x 2903-2923)** shows dark stretches of 40-60 px wherever it passes a
  load's tie (the buried contact between the load plate's tab and the tail of the node's
  box), at y 3164, 3337, 3530, 3620, 3820, 4202, 4313, 4640, 4813, 4935, 5011, 5246. Neither
  metal shot shows bright metal there. Read as: the metal is continuous and dips over the
  buried contacts (if those were metal contacts, the outputs of several different gates
  would be shorted together). So where thin E really makes contact is still not found;
  `tools/tla_contacts.py` is no help on it (it passes over tan diffusion boxes all the way).
- **The dense part west of the rail, x 2835-2975, y 3395-3665: resolved 2026-11-17.** It is
  two loads and a strap. The inverter `rcs_u3425`'s node strip runs west under the rail to a
  diffusion column under thin E (x 2900-2940, ending at y 3500); its load plate
  (x 2845-2895) continues downwards as a pad with a metal contact (2865,3488) and a
  buried-contact tie to that column. A **metal strap** (x 2850-2886) takes the node from
  that contact down, over `b1`'s load plate, to a second pad (contact (2865,3640)) whose
  poly arm crosses `b1`'s box under thin E at y 3617-3638 **as a gate** (9x: bright over a
  channel, diffusion on both sides, and the part below links east to the VSS box). So
  `b1` has three pull-downs. How the two crossings were told apart: class runs down
  x 2912-2928 show plain diffusion with a box at its edge at the top crossing (a tie) and
  a bright band right across the diffusion at the bottom one (a gate).
- **Two kinds of non-standard unit** in this cluster, both now traced once: the strap
  (an output carried over a neighbouring load to a gate), and the AND-OR-INVERT unit
  whose diffusion is one wide area under the VSS rail and under a signal metal beside it
  (`rcs_n4200`, y 4045-4320), with series gates.

## Reading aids for this region

- **The loads' ties.** Each load plate has a tab at its lower corner that is tied by a
  buried contact to a tail of the node's box, right under the thin metal. In the metal
  shot the tie looks like a metal contact (a round blob). It is not one: all the loads of
  a column have it and the thin metal runs on past them. So the thin metals (x 2903-2923
  and x 2688-2708) do not join the loads' nodes; what they do connect is not read yet.
- **Under a wide rail** the clean shot shows field as pink with an olive stripe down the
  middle; the class map paints the stripe as open diffusion. Diffusion under a rail is the
  tan boxes only.
- **The bus as a class map** (`strips.py --layer class`): metal shows as white bands (field
  that was under metal), gaps between pieces as olive blocks, poly crossings as red bars,
  contacts as yellow-green blobs in a red pad. One image shows 3,000 px of the bus.
- `tools/follow.py` follows one metal line from a point through corners, jogs and
  diagonals, using both chips' metal shots, and prints it as a trace line. It turned a
  4,000 px bus-field run from an afternoon into a minute. Its ends and its staircases must
  still be looked at: see its docstring for the two mistakes it made here.
- `tools/tla_tracks.py` (where a track has metal; splits at gaps) and
  `tools/tla_contacts.py` (contact candidates on a track from the clean shot's colour).
  Both are for knowing where to look. A dark band across one chip's metal with nothing
  under it in the clean shot is dirt: check the other chip's metal shot (`metal1`).
- Not every part of the column is the simple NOR unit: y 4235-4620 on the east side has
  diffusion strips under the thin metal with gates across them (pass transistors or a
  latch). Not traced.

## What the chase showed about this part of the die

The top-left "logic" is gate clusters joined by bus fields: the vertical bus x 3090-3380
beside this cluster, seven horizontal poly lines along its top (y 2630-2900), another
vertical bus field at x 4140-4420, the poly bus x 5100-5300 / y 5840-6850 with its
diagonal fan, and the left bus field x 6300-6900 that runs the height of the die. Signals
such as `e4` are global: they have a dozen taps. Following one at a time costs a handful
of views per hop. The region has to be traced whole, cluster by cluster and bus by bus.

My guess, **not shown by anything yet**: this is the vertical control. In a 6845 the
character row counter steps at the end of a scan line when the scan line counter has
reached R9. The formula has that shape if `e4` is an end-of-line timing strobe (active
low), `e3` or `x1`/`a2` are scan-line comparisons, and `in1` is a separate cause. The way
to prove or refute it is to reach a named signal: the R0 match line from the right
datapath (bd1's tracks k7/k8, not followed past their first jog) is the best candidate
for `e4`, and it would arrive up the left bus field, which is where `e4` comes from.

## Not done

- The inputs' sources (table in Status). Next: `e4` south down the left bus field, and
  from the other side the R0 match line from bd1's k7/k8.
- The unit at y 3895 (seen), the unit at y 3420, the dense part west of the rail at
  y 3400-3660 (a strap x 2852-2890 between contacts (2868,3488) and (2868,3640), a vertical
  poly under the rail's west edge x 2947-2967, gates across a diffusion under thin metal E):
  b1's load is in there.
- y 3700-4590 on the east side and the whole west side above y 4940 (R1's columns).
- The thin metals' ends and contacts; how rail R2 (VCC, top end y 3018) is fed.
- Bus pieces not yet drawn: B2 (from (3150,3810) south), C upper, D, F, and everything
  north of y 2940.
