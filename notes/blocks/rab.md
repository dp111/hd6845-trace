# rab: the five row address lines east of the central datapath (x 10510-15430, y 4300-6020)

Serial work, 2026-11-16. Trace: `trace/rab.txt`. Views: `cache/scratch/rax/ch1e_a.png`,
`l6000.png`, `rae.png`, `ram1.png`, `ram2.png`, `ram3.png`; overlay checks `chkA.png`,
`chkB.png`.

## Status

Wiring only, drawn and extracted; no new nets (everything joins `rax_o0`-`rax_o4`, the
outputs of the five units east of the row address selector, `notes/blocks/ras.md`).

## Route (the same for all five)

| Stretch | Layer | Ends |
|---|---|---|
| the long lines of the central datapath's channel 1 (y 6000, 5956, 5913, 5870, 5826 for bits 0-4), east of x 10510 | poly | staircase of pads at (10975,6000), (11015,5955), (11060,5912), (11105,5865), (11150,5822) |
| north along x 10981, 11022, 11065, 11108, 11154 (1,300-1,700 px), the first three turning east at the top | metal | pads at (11157,4331), (11105,4374), (11160,4416), (11105,4457), (11160,4500) |
| east under the wide supply metal x 11280-11600 | poly | pads at (11650,4331), (11695,4374), (11650,4416), (11695,4457), (11650,4500) |
| east along y 4332-4501 for 2,000 px, nested corner south at x 13822, 13780, 13736, 13692, 13644, east along y 4505, 4592, 4636, 4678, 4722 | metal | see below |

Ends:

- **bit 0**: pad (13815,4500); poly east along y 4500 to x 14000, where it meets a small
  structure beside a vertical poly (x 14040, y 4420-4548). Not resolved, not drawn.
- **bit 1**: pad (14430,4590); poly north along x 14430 into the logic above y 4500.
- **bit 2**: followed to x 14870 on y 4636; end not looked at.
- **bit 3**: pad (15425,4675); poly north.
- **bit 4**: followed to x 15250 on y 4722; goes on east.

## What this says about the RA pins

None of the five lines reaches a pad driver directly. They end in a band of logic at
x 13990-15500, y 4300-4520, north of the R5/R3 comparators (queue: `ral`), and the pad
drivers' inputs come out of the same band: RA0's is a poly along x 14340 that comes down
from that logic to a pad (14340,4764), then metal east along y 4764 to the driver's poly
at (15305,4762); RA1's metal along y 4592 arrives at the driver's poly (15345,4590) from
x 14774, while `rax_o1` on the same y ends at the pad (14430,4590): **one track, two
nets, the logic between them** (`ram3.png`). So between the units and each RA pin there
is at least one more gate, not traced.

A sixth line of the same bundle: metal from a pad at about (11650,4245) east along
y 4245, south along x 13862, east along y 4548 to x 15906, with pads at (14040,4548)
(poly north to y 4420) and (14490,4548) (poly north). Not drawn.

## How sure

- Metal: `tools/follow.py` for every stretch; corners and pads seen on 1.8-2x views; the
  overlay sits on the nested corner and both end pads.
- The cross-under: one 1.8x view in both shots, ten pads and five polys plain.
- `trace/cdp2.txt` had line 6000 ending at x 10518 beside s7's track; it goes on east
  (clean shot at 2.9x). Corrected there.

## Not done

Everything east of the ends listed. The pad (15425,4675) and bit 4's line towards the
RA3 and RA4 drivers on the right edge.
