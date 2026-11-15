# tla: top-left logic, the gate cluster x 2450-3100, y 4600-5320 and its bus

Serial work, started 2026-11-16. Trace: `trace/tla.txt`. Views: `cache/scratch/tla/`.

## Status

Two gates traced and extracted (7 transistors); the rest of the cluster is surveyed only.

```
wl_b    = NOR(in1, in2, in3)     the row counter's step signal (active low); load 29/30
tla_m2  = NOR(in2, in3)          no load found yet; feeds gate E0 further up the same column
```

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
| `in1` | y 4929-4947, pad contact (3360,4937) | line G, upper piece, x 3352-3375, comes from the north (seen to y 4380) | not followed |
| `in2` | y 4970-4992 then south at x 3000-3012 into the band y 5001-5020; pad contact (3148,4976) | line B, y 4705-5428 | (3150,4719): gate E1 of `m2`; (3150,5412): poly west along y 5400-5422, not followed |
| `in3` | y 5055-5075, pad contact (3108,5068) | line A, y 4790-5212 | (3108,4805): gate E2 of `m2`; (3108,5197): poly west along y 5188-5208 across R3, not followed |

So `in2` and `in3` are driven from further south-west (the two polys not yet followed), and
`in1` from the north.

## The small NOR `m2` (traced)

Column x 3030-3063 east of R3, between the east arms of two VSS boxes (y 4690-4707 and
y 4820-4842). Gates E1 (`in2`, y 4709-4734) and E2 (`in3`, y 4796-4817); the node between
them has a buried contact (box x 3045-3068, y 4750-4780) to a poly that runs east along
y 4753-4772, north under bus line C (x 3186-3206) and back west along y 4626-4645, where it
is gate E0 on the upper part of the same column (VSS below it; what is above: next piece).
No load has been found on `m2`.

## Not done

Everything else in the cluster (R1's columns, the loads L1-L3 and L_b, L_c between R2 and
R3, the thin metal x 2903-2923 and its taps, the column above E0), the bus pieces' other
ends, and the clusters above and below.
