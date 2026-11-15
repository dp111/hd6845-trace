# tc1: top-centre logic, upper half (x 6400-8250, y 2500-4450)

Trace: `trace/tc1.txt`. Coordinates are metal-shot pixels. Local names start `tc1_`.

## Status

Run 1 (2026-11-15). Surveyed the whole region; traced and overlay-checked the whole
**island** (x 7330-7900, y 3050-4050: nine gates, 26 transistors, no latch) together
with the wiring that joins its gates to each other: the four metal verticals in the
channel west of it (x 7174-7325) and the verticals east of it (x 7914-8064).
Not traced: the gate columns at x 6400-7000, the rest of the channel x 7000-7170, and
the bus fields above (y < 2975) and below (y > 4060), where every signal that enters or
leaves the island still has its far end. See Ports and Not done.

## How this area reads in the photos (cost me a third of the run; read this first)

- A **diffusion wire in the open is a strip about 22 px wide between two dark edge
  lines**. Its interior is only slightly redder than the field (acid1b raw RGB about
  165/120/100 against field 150/158/96; in `acid` R>G inside, G>R outside). It is not
  green. Only *large* open diffusions (the drains of the big drivers) are green. At
  2x the two edge lines look like "thin dark wires"; they are the two sides of one
  strip. `tools/tc1_px.py col X Y0 Y1 2 acid1b,acid,metal` across a strip settles it.
- A weak load is a poly block about 60 x 65-90 px with the strip passing under it (two
  dark lines across the block, 22-28 px apart). The gate tie is a tab of diffusion
  ("bump") hanging from the strip beside the block, ending under a buried-contact box
  that the block's stem enters.
- In the stripped shots a dark line runs parallel to every rail edge 10-25 px outside
  it (the etch boundary of the metal's protection). It crosses poly bands and
  diffusion alike and is not layout. The metal shot does not have it: a line seen
  there is real.
- Under the rails, tan (raw 190/172/128) is diffusion, salmon (235/160/115) poly,
  and the field is 150/133/105 (shown pink by the viewer).
- Pull-downs sit *under the VSS rails*: a poly band crossing the rail's diffusion
  column. Outputs leave the column sideways into a buried-contact box.

## Inventory

Rails and channels (from two 0.7x views of the whole region):

| What | Where |
|---|---|
| Horizontal bus field (metal lines, poly cross-unders) | y 2500-2950, whole width |
| Gate columns, continuing the top-left logic | x 6400-7000, y 2650-4450; vertical rails at x 6507-6557, 6686-6736, 6857-6900; not traced, rails not identified |
| Routing channel, about 14 vertical metal lines; the four nearest the island (W1-W4, x 7174-7325) are traced | x 7000-7330, y 2950-4450 |
| **Island**: three vertical rails and nine gates | x 7330-7900, y 3050-4050 |
| Island left rail, VSS | x 7420-7470, y 2975 to beyond 4300 (0.7x view) |
| Island centre rail, VCC | x 7597-7647, top end y 3105, down to a wide bus at y 4190-4255 |
| Island right rail, VSS | x 7770-7820, from above y 2500 (0.7x view) to its end at y 4000 |
| VSS strap joining the two outer rails | x 7420-7820, y 2975-3040 |
| Wiring between island and datapath: verticals V1 x 7914-7931, V2 x 7957-7977, V3 x 8002-8022, then x 8043-8063 | x 7900-8080 |
| Six vertical metal lines, 44 px pitch (x 8100, 8143, 8187, 8231, 8272, 8317), from the top bus field down past y 3440 | x 8090-8330 |
| Bus field below the island (horizontals, a diagonal, the wide VCC bus y 4193-4257) | y 4040-4450 |

VSS/VCC are assigned from the loads (all hang from the centre rail) and the pull-down
sources (all contact the outer rails); the rails have not been followed to the pads.

**The datapath's regular slices start at x 8340** (cdp1's slice 0 rail is at x 8403),
not at 7600-7650. x 8090-8330 is a bundle of six north-south metal lines.

Island, right half (traced):

| Gate | Where | Kind |
|---|---|---|
| R1 | load 7655-7715 x 3138-3203; pull-down under right rail y 3193-3213 | inverter |
| R2 | load 7655-7715 x 3307-3397; pull-downs in the column 7826-7881 x 3256-3410 | 2-input NOR |
| R3 | load 7685-7730 x 3470-3544 (strong); pull-downs under/right of the rail y 3452-3556 | 2-input NOR |
| R4 | load 7653-7713 x 3615-3682; pull-down under the rail y 3667-3689 | inverter |
| R5 | load 7656-7698 x 3832-3884 (strong); ladder 7740-7873 x 3740-3972 | AND-OR-invert, 2+2 |

Island, left half (traced):

| Gate | Where | Kind |
|---|---|---|
| L1 | load 7532-7591 x 3160-3214; pull-down under the left rail y 3215-3235 | inverter (mirror image of R1) |
| L2 | drain = column y 3407-3471 plus the green region 7518-7547 x 3332-3513; gates = poly bands y 3388-3407 and y 3471-3492, each wrapping the drain as an L; strong load 7552-7588 x 3370-3460 | 2-input NOR, wide transistors |
| L3 | the same 258 px lower (bands y 3642-3663 and y 3729-3750, load 7552-7588 x 3630-3720) | 2-input NOR, wide transistors |
| L4 | pull-downs in the column 7368-7410 x 3828-3972 west of the rail; load 7541-7588 x 3874-3950 | 2-input NOR (mirror image of R2) |

The left rail's diffusion is a column x 7366-7482 (wider than the rail: x 7366-7410 is
in the open and green) from y 3290 to 3832, widened on the right to x 7547, with VSS
contacts at y 3258, 3335, 3527, 3597, 3803 and a pad at 7405-7468 x 3951-3998.

Channel west of the island, the four lines that serve it (all metal, about 20 wide):

| Line | x | y range | Net |
|---|---|---|---|
| W1 | 7174-7194 | 2976 to beyond 3985 | `tc1_w1` |
| W2 upper | 7223-7240 | 2987-3128 (then east along y 2978-2995 to x 7350) | `tc1_b` |
| W2 lower | 7220-7240 | 3170 to beyond 3985 | `tc1_l1_out` |
| W3 upper | 7265-7284 | 3032-3386 (from the east along y 3022-3042) | `tc1_a` |
| W3 lower | 7265-7284 | 3427 to beyond 3985 | `tc1_l2_out` |
| W4 upper | 7307-7325 | 3062-3648 | `tc1_r1_out` |
| W4 lower | 7307-7325 | 3690 to beyond 3985 | `tc1_l3_out` |

**Three of these verticals are cut where a gate is inserted in them**: W2 between
y 3130 and 3168, W3 between 3404 and 3422, W4 between 3664 and 3680. At 1x each looks
like one continuous line with two contacts. Each break was measured (`tc1_px.py col`:
bare field in the metal shot, unprotected colours in `acid1b`).

A wide metal strap, y 2975-3040, joins the two VSS rails (x 7420-7820; drawn). The
poly lines of `tc1_b` (y 2977-2994) and `tc1_a` (y 3020-3038) run west under it; their
edges print through the metal as dark lines and make the strap look like three metal
lines. The metal that brings each of them is separate from the strap: a 20 px gap at
x 7822-7842 (`tc1_b`, measured) and at x 7397-7420 (`tc1_a`, seen at 2x).

## Logic (traced; extraction: 26 transistors, no errors)

```
tc1_r1_out = NOT tc1_a
tc1_l1_out = NOT tc1_b
tc1_l2_out = NOR(tc1_a, tc1_l1_out)        = NOT a . b        (driver)
tc1_l3_out = NOR(tc1_r1_out, tc1_l1_out)   = a . b            (driver)
tc1_l4_out = NOR(tc1_l2_out, tc1_w1)
tc1_r2_out = NOR(tc1_a, tc1_b)
tc1_r5_out = NOT(tc1_g.tc1_h + tc1_i.tc1_j)
tc1_r4_out = NOT tc1_r5_out
tc1_f      = NOR(tc1_r2_out, tc1_r4_out)   = (a + b) . NOT(g.h + i.j)   (driver)
```

**No latch, no flip-flop, no clocked device and no pass transistor in the island**: nine
static gates. What the signals are is **not known**; none is traced to a pad or to a
named line. What is traced about each:

- `tc1_a`. Metal V3 (x 8002-8022, y 3016-3297) with three contacts: (8010,3028) to a
  poly running west under the VSS strap to contact (7381,3030), then metal W3 upper to
  contact (7273,3375) = L2's band a; (8009,3204) = R1's input; (8009,3286) = R2's band
  a. From that last contact a poly runs down x 8004-8025 and east along y 3387-3402
  into the datapath. **That east end is the only way out of what is traced, so `a` is
  believed to come from the datapath** (not followed past x 8290).
- `tc1_b`. Poly y 2977-2994 under the VSS strap between contacts (7338,2987) and
  (7859,2984). West end: metal W2 upper down to contact (7228,3117), poly round to L1's
  input band. East end: metal V2 (x 7957-7977) to contact (7968,3375) = R2's band b;
  the poly goes on from there (down x 7959-7977, east y 3452-3472, down x 8004-8024) to
  contact (8009,3549), metal down x 8002-8022 to y 3725 and east along y 3716-3733
  (seen to x 8100, where it meets a vertical at x 8085-8100 going down). **That is the
  only way out, so `b` is believed to arrive there.**
- `tc1_r1_out` (NOT a): buried contact, poly, contact (7924,3159), metal V1 up to
  y 3071 and west to contact (7862,3072), poly west along y 3065-3079 across the top of
  the island (under both VSS rails, over field) to contact (7317,3072), metal W4 upper
  down to contact (7316,3638) = L3's band c. Goes nowhere else.
- `tc1_l1_out` (NOT b): buried contact 7354-7396 x 3164-3199, poly west to contact
  (7228,3181), metal W2 lower: contacts (7230,3482) = L2's band b and (7230,3740) =
  L3's band d, and continues down past y 3985.
- `tc1_l2_out`: buried contact 7358-7396 x 3420-3452, poly west to contact (7279,3437),
  metal W3 lower: contact (7273,3852) = L4's band e, continues down past y 3985.
- `tc1_l3_out`: buried contact 7356-7396 x 3684-3717, poly west to contact (7316,3700),
  metal W4 lower, continues down past y 3985.
- `tc1_l4_out`: buried contact 7364-7400 x 3878-3910, poly west along y 3885-3905 under
  W4, W3, W2, W1 (no contacts) and on past x 7150.
- `tc1_w1`: metal W1. Top end contact (7186,2986) to a poly that runs east along
  y 2977-2997 (under W2's horizontal) and turns north at x 7290-7308 into the top bus
  field. Contact (7190,3938) = L4's band f. Continues down past y 3985.
- `tc1_r2_out`: buried contact, poly, contact (7924,3332), V1 segment down to contact
  (7924,3464), poly band c west to R3. Goes nowhere else.
- `tc1_r4_out`: diffusion under the right rail to a buried contact (7856-7892 x
  3621-3654) on the foot of an L-shaped poly (down x 7898-7918, y 3539-3647; west along
  y 3539-3556) = R3's band d. Goes nowhere else. Checked at 6x in the metal shot: the
  poly's outline widens round the box.
- `tc1_r5_out`: buried contact, poly, contact (7922,3854), V1 segment up to contact
  (7922,3679), poly band e west to R4. Goes nowhere else.
- `tc1_f`: R3's output; buried contact, poly band f, contact (7966,3506), metal east
  along y 3501-3519 and up x 8045-8064 to contact (8054,3354), poly east along
  y 3348-3362 into the datapath.
- `tc1_g`, `tc1_h`, `tc1_i`, `tc1_j`: each arrives on a metal vertical from below:
  g contact (8052,3768), metal x 8043-8063; h contact (7968,3808), metal x 7957-7978;
  i contact (8010,3894), metal x 8000-8020; j contact (7922,3939), metal x 7914-7931
  down to another contact at about (7922,4027) (poly beyond, not followed).

Believed, not traced: L2, L3 and R3 have strong loads and wide pull-downs, so
`tc1_l2_out` (NOT a AND b), `tc1_l3_out` (a AND b) and `tc1_f` are lines with a heavy
load: strobes or enables. `a` and `b` together select which of them is active; `f` is
additionally blocked by `g.h + i.j`.

Sizes (W/L in px): weak loads 22/60 (R1, R2), 27/59 (L1), 28/59 (R4), 23/47 (L4);
strong loads 38/45 (R3), 40/42 (R5), about 65/36 (L2, L3; the strip's height under the
gate was not measured). Pull-downs 43/20 (R1, R4), 72/20 (L1), 55/18 (R2), 42/21 (L4),
67/18 (R3), 133/19 (R5, each of four), about 260/23 and 230/23 (L2, L3: each gate wraps
the drain region as an L). For L2 and L3 the W comes from rectangles drawn to the
visible edges; whether a source strip lies under the far end of each bottom arm
(x 7547-7591) was not settled, so their W is good to about 15 %.

## Ports

Nothing below has been followed to its far end; "going" is the direction away from the
island.

| Name | Layer | Where it crosses | Dir | What |
|---|---|---|---|---|
| `tc1_f` | P | y 3348-3362 at x 8250, going east; seen to x 8290 under the six vertical metals without contact | out | R3 output. Enters the datapath in the channel between cdp1's row A (y 3040-3330) and row B (y 3480-3900) |
| `tc1_a` | P | y 3387-3402 at x 8250, going east; seen to x 8290 | in (believed) | same channel, 40 px below `tc1_f` |
| `tc1_b` | M | 8100, y 3716-3733, going east to a vertical at x 8085-8100 that goes down | in (believed) | |
| `tc1_l1_out` | M | 7230, 3985 going down (W2 lower) | out | NOT b |
| `tc1_l2_out` | M | 7274, 3985 going down (W3 lower) | out | NOT a AND b |
| `tc1_l3_out` | M | 7316, 3985 going down (W4 lower) | out | a AND b |
| `tc1_l4_out` | P | 7150, y 3885-3905, going west | out | NOR(l2_out, w1) |
| `tc1_w1` | M | 7185, 3985 going down (W1) | ? | |
| `tc1_w1` | P | 7299, 2950 going north (x 7290-7308) | ? | other end of W1 |
| `tc1_g` | M | 8053, 4060 going down | in | below is the bus field |
| `tc1_h` | M | 7968, 4060 going down; at about y 4070 it turns west (1.5x view) | in | |
| `tc1_i` | M | 8010, 4060 going down; at about y 4115 it turns west (1.5x view) | in | |
| `tc1_j` | M | 7922, 4027: contact to a poly pad, poly beyond not followed | in | |
| `vcc` | M | centre rail 7622, drawn y 3105-4060 | | continues down to the wide bus y 4193-4257 |
| `vss` | M | right rail 7795 drawn y 3000-4000 (it continues up); left rail 7445 drawn y 2975-4060 (continues down); strap y 2975-3040 | | |

Seen while following these, **not mine and not drawn**: `cdp1_a0_q` (poly from the
datapath at y 3017-3040) turns north at x 8047-8072 and west again along y 2930-2950; it
passes 15 px from the `tc1_a` contact pad at (8010,3028) **without touching it** (field
gap at x 8030-8046, measured with `tc1_px.py row 3029`). `cdp1_a1_q` (poly, y 2972-2992)
ends at about x 8108 by the vertical metal x 8087-8110 (junction not looked at).

## Ambiguities

1. **Rails.** VSS/VCC of the island assigned from load orientation only (see
   Inventory). Would be settled by following the centre rail's bus (y 4193-4257) east.
2. **Diffusion column right of the right rail joins the pads under it** (R1's source
   pad to R2's column at 7826-7832 x 3256-3280; R2's lower source at 7826-7832 x
   3390-3410). The joins lie under the rail's edge line, so they cannot be seen
   directly; no gap shows in `tc1_px.py row 3270` / `row 3400` and the circuit needs
   them. Working assumption: joined.
3. **R5's gate tie.** The load's stem goes up to a buried-contact box (7673-7702 x
   3767-3802); a 10 px light strip between two dark lines runs from the box down
   x 7705-7719 to the output region. Read as a narrow diffusion wire (its colour in
   `acid` is diffusion-like). If it were field the load gate would float, so the
   reading is safe, but the strip is at the limit of the photos.
4. **Strips between the series gates of R5** (y 3779-3794 and y 3907-3921): in the open
   they look like thin outlined bands, which could be taken for two more poly lines.
   Under the rail the same y is plain diffusion (tan), so they are the series nodes.

5. **L2/L3 diffusion right of the left rail** is drawn as one rectangle 7478-7547 x
   3290-3830 that the L-shaped gates cut into drains and source strips. The strips
   between one gate's arm and the next (y 3290-3306, 3539-3562, 3801-3830) are 16-29 px
   tall and were seen at 2x only. They are all VSS either way; only W is affected.
6. **Poly under metal W1** (x 7183-7200, y 3104-3235, part of `tc1_b`) runs lengthwise
   under W1 for 130 px. No contact ring is visible on W1 there at 2.4x; assumed none.
7. Crossings of the west-going poly bands under W1-W4 were judged at 2.25-2.4x: a
   contact shows there as a 30 px dark ring and a pad with a green dot in `acid1b`;
   every band has exactly one, at its end.

## Not done

- Far ends of everything in the Ports table. Cheapest next steps: (a) the channel
  x 7150-7350 below y 3985 for W1, W2, W3, W4; (b) the bus field y 4040-4450 east of
  x 7900 for `tc1_g/h/i/j` and `tc1_b`; (c) `tc1_a` and `tc1_f` east of x 8290 belong
  with cdp1.
- The six vertical metals at x 8090-8330 and where `cdp1_a1_q` ends.
- Gate columns x 6400-7000 (about 40 loads visible; three vertical rails at x 6507-6557,
  6686-6736, 6857-6900), the channel x 7000-7170, the top bus field y 2500-2975:
  nothing traced.
