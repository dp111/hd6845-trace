# tc1: top-centre logic, upper half (x 6400-8250, y 2500-4450)

Trace: `trace/tc1.txt`. Coordinates are metal-shot pixels. Local names start `tc1_`.

## Status

Run 1 (2026-11-15). Surveyed the whole region; traced and overlay-checked the **right
half of the "island"** (x 7600-7900, y 3100-4000: five gates R1-R5, 15 transistors) and
the wiring that joins them to each other and to the first contacts outside the island.
Not traced: the left half of the island (described under Inventory), the gate columns
at x 6400-7000, and all the bus fields. See Not done.

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
| Routing channel, about 14 vertical metal lines | x 7000-7330, y 2950-4450 |
| **Island**: three vertical rails and about 12 gates | x 7330-7900, y 3050-4050 |
| Island left rail, VSS | x 7420-7470, y 2975 to beyond 4300 |
| Island centre rail, VCC | x 7597-7647, top end y 3105, down to a wide bus at y 4190-4255 |
| Island right rail, VSS | x 7770-7820, from above y 2500 to its end at y 4000 |
| Wiring between island and datapath: verticals V1 x 7914-7931, V2 x 7957-7977, V3 x 8002-8022, then x 8043-8063 | x 7900-8080 |
| Six vertical metal lines, 44 px pitch (x 8100, 8143, 8187, 8231, 8272, 8317), from the top bus field down past y 3440 | x 8090-8330 |
| Bus field below the island (horizontals, a diagonal, the wide VCC bus y 4193-4257) | y 4040-4450 |

VSS/VCC are assigned from the loads (all hang from the centre rail) and the pull-down
sources (all contact the outer rails); the rails have not been followed to the pads. A
metal strap at y 3012-3036 seems to join the two outer rails across the top (seen at
1.25x only, not drawn).

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

Island, left half (**not traced**, read from the 2.2x views; coordinates are good to
about 5 px, the logic is a reading, not an extraction):

| Gate | Where | Reading |
|---|---|---|
| L1 | load 7510-7590 x 3165-3215 (weak), strip y 3186-3206 to the left rail; pull-down = poly band y 3215-3235 under the left rail, source contact (7435,3260) | inverter; input band comes from the west at y 3215-3235; output leaves west through buried contact 7355-7395 x 3165-3200 as poly at y 3173-3193. Mirror image of R1 |
| L2 | drain = middle of the rail column, y 3408-3474, plus the green region 7484-7547 x 3331-3500; gates = poly bands y 3388-3406 and y 3474-3492 from the west, each continuing as an L round the green region; strong load 7552-7588 x 3372-3458 from VCC pad 7602-7650 x 3383-3449, gate tie box 7550-7579 x 3467-3495 | 2-input NOR with wide transistors (a driver); output leaves west through buried contact 7365-7393 x 3422-3449 as poly at y 3428-3452 |
| L3 | same again 260 px lower: gates y 3647-3665 and y 3735-3751, drain y 3667-3735 plus green region 7484-7547 x 3600-3754, load 7552-7588 x 3631-3722, output box 7365-7393 x 3681-3708 | 2-input NOR driver |
| L4 | y 3840-4000: poly bands y 3845-3860 and y 3922-3945, box 7365-7393 x 3876-3917, load 7510-7590 x 3880-3950 with VCC pads at 7600-7650 x 3880-3935 | not read |

The left rail's diffusion column is x 7363-7482 (wider than the rail: the strip
x 7363-7410 is in the open and green), y 3188-3840, with VSS contacts at y 3260,
3305-3360 (five), 3500-3640, 3760-3830 and a small pad at 7411-7465 x 3954-4000.

## Logic (traced; extraction: 15 transistors, no errors)

```
tc1_r1_out = NOT tc1_a
tc1_r2_out = NOR(tc1_a, tc1_b)
tc1_r5_out = NOT(tc1_g.tc1_h + tc1_i.tc1_j)
tc1_r4_out = NOT tc1_r5_out
tc1_f      = NOR(tc1_r2_out, tc1_r4_out)
           = (tc1_a + tc1_b) . NOT(tc1_g.tc1_h + tc1_i.tc1_j)
```

No latch, no clocked device and no pass transistor among these five gates: purely
combinational. What the signals are is **not known**; nothing here is traced to a pad or
to a named line. What is traced about each:

- `tc1_a`: metal V3 (x 8002-8022, y 3016-3297). Three contacts: (8010,3028) to a poly
  running west along y 3020-3038; (8009,3204) to R1's input band; (8009,3286) to R2's
  band a. From the last contact a poly continues down x 8004-8025 and then east along
  y 3387-3402 into the datapath. So one of the two ends (the west poly or the east
  poly) is the source and the other a load; which is not known.
- `tc1_b`: poly from the west along y 2977-2994, contact (7859,2984), metal east along
  y 2978-2998 and down V2 (x 7957-7977) to contact (7968,3375) on R2's band b. The poly
  continues from that contact: down x 7959-7977, east along y 3452-3472, down
  x 8004-8024 to contact (8009,3549), then metal down x 8002-8022 to y 3725 and east
  along y 3716-3733 (seen to x 8100, where it meets a vertical at x 8085-8100 going
  down).
- `tc1_r1_out` (= NOT a): buried contact, poly, contact (7924,3159), metal V1 up to
  y 3071, west to contact (7862,3072), then poly west along y 3065-3079 across the top
  of the island (under both VSS rails, over field) to x 7338 and on.
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

Believed, not traced: with strong loads on R3 and R5 and a line into the datapath,
`tc1_f` looks like a gated strobe or enable for the datapath row at y 3330-3480; the
left half's L2 and L3 are two more drivers of the same kind facing west.

Sizes (W/L in px): weak loads 22/60 (R1, R2), 28/59 (R4); strong loads 38/45 (R3),
40/42 (R5); pull-downs 43/20 (R1, R4), 55/18 (R2), 67/18 (R3), 133/19 (R5, each of
four). The W of R5's load strip under its gate (drawn y 3838-3878) was not measured.

## Ports

| Name | Layer | Where it crosses | Dir | What |
|---|---|---|---|---|
| `tc1_f` | P | y 3348-3362 at x 8250, running east; seen to x 8290 under the six vertical metals without contact | out | R3 output. Enters the datapath in the channel between cdp1's row A (y 3040-3330) and row B (y 3480-3900) |
| `tc1_a` | P | y 3387-3402 at x 8250, running east; seen to x 8290 | ? | same channel, 40 px below `tc1_f` |
| `tc1_a` | P | 7800, y 3020-3038, running west (not followed) | ? | other end of the same net |
| `tc1_b` | P | 7800, y 2977-2994, running west (not followed) | in? | |
| `tc1_b` | M | 8100, y 3716-3733, running east to a vertical at x 8085-8100 (not followed) | ? | |
| `tc1_r1_out` | P | 7338, y 3065-3079, running west (not followed) | out | NOT `tc1_a` |
| `tc1_g` | M | 8053, 4060 going down | in | followed to y 4060 only; below is the bus field |
| `tc1_h` | M | 7968, 4060 going down; at about y 4070 it turns west (1.5x view) | in | |
| `tc1_i` | M | 8010, 4060 going down; at about y 4115 it turns west (1.5x view) | in | |
| `tc1_j` | M | 7922, 4027: contact to a poly pad, poly beyond not followed | in | |
| `vcc` | M | centre rail 7622, drawn y 3105-4060 | | continues down to the wide bus y 4193-4257 |
| `vss` | M | right rail 7795, drawn y 3000-4000 | | continues up |

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

## Not done

- **Island left half**, L1-L4 (table above). Start with a quad at 2.2x of x 7330-7600,
  y 3130-3560. Inputs and outputs all go west as poly bands at x 7335; follow them
  into the channel x 7000-7330.
- West ends of `tc1_a` (poly y 3020-3038), `tc1_b` (poly y 2977-2994), `tc1_r1_out`
  (poly y 3065-3079) beyond x 7800 / 7338.
- Lower ends of `tc1_g/h/i/j` and the east end of `tc1_b` in the bus field y 4040-4450.
- The six vertical metals at x 8090-8330 and where `cdp1_a1_q` ends.
- Gate columns x 6400-7000 (about 40 loads visible), channel x 7000-7330, top bus field
  y 2500-2950: nothing traced.
