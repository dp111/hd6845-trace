# tla: top-left logic, the gate cluster x 2450-3100, y 4600-5320 and its bus

Serial work, started 2026-11-16. Trace: `trace/tla.txt`. Views: `cache/scratch/tla/`.

## Status

Four gates traced and extracted (13 transistors); the rest of the cluster is surveyed only.

```
wl_b    = NOR(in1, in2, in3)     the row counter's step signal (active low); load 29/30
in2     = NOR(w2, e4)            west column; load 17/53
in3     = NOR(e3, e4)            east column; load 29/54
tla_m2  = NOR(in2, in3)          east column; load 29/53; feeds gate E0 further up the column
```

Put together: **step = in1 OR (NOT e4 AND NOT (w2 AND e3))**, and
`m2 = e4 OR (w2 AND e3)` is its complement apart from `in1`. So `e4` is a gate on the
whole thing: while it is high, only `in1` can step the row counter; while it is low the
counter steps unless `w2` and `e3` are both high.

What the four inputs are is **not known yet**. Where each has been followed to:

| Signal | Followed to |
|---|---|
| `e4` | 7,000 px: bus line C (x 3196, y 3944-5677), east along y 5677, south at x 3527, contact (3565,5848), poly east along y 5847 to x 5285, south to y 6850, diagonally to (5560,7122), east to a contact (6140,7124), metal east along y 7084, south at x 6769, contact (6730,8275), poly under six horizontal metals, contact (6730,8580), metal diagonally south-west and **south down the left bus field at x 6548-6570** (seen to y 13000; that field's crossings at y 9560-9780, 10340-10660 and 11860-12080 not read). All drawn to y 8680 |
| `in1` | bus line G (x 3369, y 2754-4952), top contact (3368,2768), poly east along y 2768 to a contact (4225,2765) on a vertical metal of the bus field x 4140-4420 |
| `e3` | bus line E, upper piece, bottom contact (3283,5152); comes from the north |
| `w2` | poly y 5142-5164 from the west bus (x 2420 and beyond) |

## How the row counter's step signal gets here

`wl_b` (see `notes/blocks/wl.md`, `notes/blocks/bw.md`) was followed from the block west of
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
  poly that carries `wl_b` away.

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

The cluster sits directly above the left array (`larr`: the MA counter and nine upper
rows of another type). My guess, not shown by anything yet: those nine rows hold the
scan line counter and this cluster is the vertical control. If so the step gate's inputs
would be scan-line matches and an end-of-line strobe.

## Not done

Everything else in the cluster (R1's columns, the loads L1-L3 and L_b, L_c between R2 and
R3, the thin metal x 2903-2923 and its taps, the column above E0), the bus pieces' other
ends, and the clusters above and below.
