# tc1: top-centre logic, upper half (x 6400-8250, y 2500-4450)

Trace: `trace/tc1.txt`. Coordinates are metal-shot pixels. Local names start `tc1_`.

## Status

Runs 1 and 2 (2026-11-15). Traced, overlay-checked and extracting (26 transistors, no
errors, no open nets): the **island** (x 7330-7900, y 3050-4050: nine static gates), all
of its wiring, the **bus field below it** (y 4130-4450), the **six north-south metals**
east of it (x 8089-8321, each end to end) and the two top bus lines that feed them from
the west. **Every input of the island is now followed to the edge of the region; none is
driven inside this block**: `a` and `w1` come from the east (datapath side), `b`, `g`
and `i` from the south (tc2). See "Where the island's inputs come from".
Not traced: the gate columns at x 6400-7000 (about 40 loads; one structure in them, a
big driver gated by `g`, is described under Not done but not drawn), the channel
x 7000-7170 except the lines that concern the island, and most of the top bus field.

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
| Top bus field: seven horizontal metal lines at y 2554, 2598, 2641, 2684, 2727, 2771, 2814 (each 14 px wide), crossing the island's right VSS rail in poly | y 2500-2950, whole width; two lines traced |
| Gate columns, continuing the top-left logic | x 6400-7000, y 2650-4450; vertical rails at x 6507-6557, 6682-6757, 6857-6932 (widths near y 4000); not traced, rails not identified. Large devices under the rails, not island-style gates |
| Routing channel: verticals at x 7002-7022, 7048-7068, 7091-7110, 7133-7152 (west part, see Not done) and W1-W4 at x 7174-7325 (traced). South of y 4050 the west part is empty field except the polys of `g` | x 7000-7330, y 2950-4450 |
| **Island**: three vertical rails and nine gates | x 7330-7900, y 3050-4050 |
| Island left rail, VSS | x 7420-7470, y 2975-4335, where it becomes the VSS bus y 4288-4335 going east to x 7995 and then south (x 7943-7990) |
| Island centre rail, VCC | x 7597-7647, top end y 3105, down to the VCC bus y 4198-4250, which runs east to x 8166 and then south (x 8116-8165) |
| Island right rail, VSS | x 7770-7820, from above y 2500 (0.7x view) to its end at y 4000 |
| VSS strap joining the two outer rails | x 7420-7820, y 2975-3040 |
| Wiring between island and datapath: verticals V1 x 7914-7931, V2 x 7957-7977, V3 x 8002-8022, then x 8043-8063 | x 7900-8080 |
| Six north-south metal lines ns1..ns6, 44 px pitch (centres x 8096, 8140, 8184, 8227, 8270, 8314), traced end to end (table under Logic) | x 8089-8321, y 2720-4450 |
| Bus field below the island: tracks T1-T3, the `g` line, VCC and VSS buses, lines to tc2 and to the datapath; traced | y 4010-4450 |

VSS/VCC are assigned from the loads (all hang from the centre rail) and the pull-down
sources (all contact the outer rails); the rails have not been followed to the pads.
Both supplies leave this block southwards (ports).

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
| W1 | 7174-7194 | 2976-3952 (ends on its lower contact; bare field below, measured) | `tc1_w1` |
| W2 upper | 7223-7240 | 2987-3128 (then east along y 2978-2995 to x 7350) | `tc1_b` |
| W2 lower | 7220-7240 | 3170 to beyond 4450 | `tc1_l1_out` |
| W3 upper | 7265-7284 | 3032-3386 (from the east along y 3022-3042) | `tc1_a` |
| W3 lower | 7265-7284 | 3427-4070, then east along y 4060-4081 to contact (7336,4070) | `tc1_l2_out` |
| W4 upper | 7307-7325 | 3062-3648 | `tc1_r1_out` |
| W4 lower | 7307-7325 | 3690-4026, then east along y 4014-4037 to a contact at (7379,4026) | `tc1_l3_out` |

**Three of these verticals are cut where a gate is inserted in them**: W2 between
y 3130 and 3168, W3 between 3404 and 3422, W4 between 3664 and 3680. At 1x each looks
like one continuous line with two contacts. Each break was measured (`tc1_px.py col`:
bare field in the metal shot, unprotected colours in `acid1b`).

A wide metal strap, y 2975-3040, joins the two VSS rails (x 7420-7820; drawn). The
poly lines of `tc1_b` (y 2977-2994) and `tc1_a` (y 3020-3038) run west under it; their
edges print through the metal as dark lines and make the strap look like three metal
lines. The metal that brings each of them is separate from the strap: a 20 px gap at
x 7822-7842 (`tc1_b`, measured) and at x 7397-7420 (`tc1_a`, seen at 2x).

## Logic (traced; extraction: 26 transistors, 25 nets, no errors)

```
tc1_r1_out = NOT tc1_a
tc1_l1_out = NOT tc1_b
tc1_l2_out = NOR(tc1_a, tc1_l1_out)        = NOT a . b        (driver)
tc1_l3_out = NOR(tc1_r1_out, tc1_l1_out)   = a . b            (driver)
tc1_l4_out = NOR(tc1_l2_out, tc1_w1)
tc1_r2_out = NOR(tc1_a, tc1_b)
tc1_r5_out = NOT(tc1_g.tc1_l2_out + tc1_i.tc1_l3_out)
tc1_r4_out = NOT tc1_r5_out                = b . (g.NOT a + i.a)
tc1_f      = NOR(tc1_r2_out, tc1_r4_out)   = (a + b) . NOT(b.(g.NOT a + i.a))   (driver)
           = a.NOT b  +  b.NOT a.NOT g  +  a.b.NOT i
```

In words: `f` is high when (a,b) = (1,0); when (a,b) = (0,1) unless `g`; when (a,b) =
(1,1) unless `i`; never when a = b = 0.

**No latch, no flip-flop, no clocked device and no pass transistor in the island or in
anything else traced in this block**: nine static gates and wiring. No named line
(`res_b`, `lpstb_b`, a clock) reaches anything traced here; `notes/blocks/trunks.md`
puts `res_b` and `lpstb_b` at x 5265-5330, west of this region.

### Where the island's inputs come from (all traced to the region edge)

| Input | Used by | Route back from the island | Leaves the region at |
|---|---|---|---|
| `tc1_a` | R1, R2, L2 | metal V3, poly east | east: poly y 3387-3402 at x 8250, in the datapath channel between cdp1's rows A and B (cdp1's notes: that line runs the full width, contact at 10615,3385) |
| `tc1_b` | L1, R2 | metal V2/V3-lower, corner (8100,3725), metal south x 8088-8105, contact (8139,4090), poly east y 4079-4101, contact (8313,4090), metal south x 8307-8321 and west along y 4411-4426, contact (8247,4417), poly west y 4408-4427, contact (7859,4417), metal west y 4411-4426, contact (7511,4417), poly south | south: poly x 7503-7522 at y 4450 |
| `tc1_g` | R5 | metal x 8045-8063 south, west along y 4151-4167, contact (7685,4158), poly west y 4144-4167; contact (7317,4158) on the way, metal south to contact (7315,4395), poly west y 4385-4403, south at x 7134-7153 | south: poly x 7134-7153 at y 4450. The other end of the y 4144-4167 poly (north at x 7177-7202, west along y 3995-4014, under the channel metals without contact) is the **gate** of transistors in a big structure at x 6750-6940, y 3930-4200 (Not done), so `g` is not driven there |
| `tc1_i` | R5 | track T3, metal south x 7265-7284, contact (7270,4437), poly west y 4424-4443, south at x 7179-7196 | south: poly x 7179-7196 at y 4450 |
| `tc1_w1` | L4 | metal W1 up to contact (7186,2986), poly east and north (x 7290-7308) to contact (7362,2770), bus line y 2764-2778 east, cross-under at the right VSS rail (contacts 7663,2769 and 7858,2769), on east and south as **ns1** (x 8089-8104), jog east at y 3651-3667, contact (8139,3704), poly east | east: poly y 3691-3712 at x 8250 (seen to x 8350), into the random logic at the datapath's slice-0 position |

So `w1` and ns1 are one net (`@alias tc1_w1 tc1_ns1`): the line has exactly two ends, L4's
gate and the poly at (8350,3700). The bus line carries no other contact (its metal run
is unbroken in `sel_tracks.py h 2771` between the contacts named).

### Outputs and internal nets

- `tc1_r1_out` (NOT a): buried contact, poly, contact (7924,3159), metal V1 up to
  y 3071 and west to contact (7862,3072), poly west along y 3065-3079 across the top of
  the island (under both VSS rails, over field) to contact (7317,3072), metal W4 upper
  down to contact (7316,3638) = L3's band c. Goes nowhere else.
- `tc1_l1_out` (NOT b): buried contact 7354-7396 x 3164-3199, poly west to contact
  (7228,3181), metal W2 lower: contacts (7230,3482) = L2's band b and (7230,3740) =
  L3's band d, and south past y 4450. No contact on it between y 3760 and 4450: the
  polys of `g` (y 4144-4167, 4385-4403), `x1` (4344-4362) and `i` (4424-4443) cross
  under it (the last checked by profile along x 7230).
- `tc1_l2_out`: buried contact 7358-7396 x 3420-3452, poly west to contact (7279,3437),
  metal W3 lower: contact (7273,3852) = L4's band e, then to track T2. Tap at
  (7510,4069): metal south to contact (7511,4242), poly south under the VSS bus, west
  along y 4320-4337, south at x 7422-7438 past y 4450.
- `tc1_l3_out`: buried contact 7356-7396 x 3684-3717, poly west to contact (7316,3700),
  metal W4 lower to track T1. Tap at (7554,4028): metal south to contact (7556,4206),
  poly south under both buses, west along y 4363-4382, south at x 7465-7481 past
  y 4450. From the pad under contact (7922,4027) a second poly goes south, east along
  y 4080-4097, diagonally (x - y = 3903) under the corner of `g`'s metal and under the
  VCC bus, and east along y 4212-4228 into the datapath (seen at 3.5x from the pad to
  the diagonal; the diagonal measured by profile at y 4170 and 4195).
- `tc1_l4_out`: buried contact 7364-7400 x 3878-3910, poly west along y 3885-3905 under
  W4, W3, W2, W1 (no contacts) to contact (7099,3897); metal north x 7091-7110 to
  contact (7100,3395); poly west along y 3388-3403 into the gate columns (seen to
  x 6930; **not drawn west of x 7150**).
- `tc1_r2_out`, `tc1_r4_out`, `tc1_r5_out`: as traced in run 1, each goes to one gate
  only (R3, R3, R4).
- `tc1_f`: R3's output; buried contact, poly band f, contact (7966,3506), metal east
  along y 3501-3519 and up x 8045-8064 to contact (8054,3354), poly east along
  y 3348-3362 into the datapath under ns1..ns6 without contact.
- R5's inputs h and j are `tc1_l2_out` and `tc1_l3_out` by tracks T2 and T1 (each:
  contact, poly east under the left and centre rails, contact, metal east).

### The six north-south metals (traced end to end; none has a transistor in this block)

| Line | x | North end | South end | Contacts |
|---|---|---|---|---|
| ns1 = `tc1_w1` | 8089-8104 | from the west on bus line y 2764-2778 | jogs east at y 3651-3667 to x 8132-8148, ends on contact (8139,3704): poly east y 3691-3712 | see `w1` above |
| ns2 | 8132-8148 | from the west on bus line y 2720-2734: cross-under at the VSS rail (contacts 7707,2725 and 7901,2724), metal west to contact (7403,2727), poly west y 2717-2737, south at x 7247-7267, west along y 2867-2883 (seen to x 7180) | ends on contact (8139,3567): poly east y 3556-3578 to x 8332, where it turns south | |
| ns3 | 8176-8191 | from the east on y 2720-2734 | jogs east at y 4151-4169 to x 8197-8213, ends on contact (8206,4329): poly west y 4320-4342 under the VCC and VSS verticals, south to contact (7905,4370), metal south x 7894-7909 past y 4450 | |
| ns4 | 8219-8234 | from the east on y 2764-2778 | jogs east at y 4112-4135 to x 8241-8257, west along y 4369-4383, south at x 8198-8212 past y 4450 | none in this block |
| ns5 | 8262-8278 | starts on contact (8271,2857): poly east y 2846-2868 | ends on contact (8270,3833) | (8270,3739) and (8270,3833), each to a poly going east |
| ns6 | 8307-8321 | from the east on y 2807-2821 | ends on contact (8313,3870) | (8313,3527) and (8313,3870), each to a poly going east; the metal is continuous across the upper one (profile along x 8314) |

Below ns1's and ns2's ends the same two tracks are reused: x 8088-8105 from y 3716 down
is `tc1_b` (field between y 3670 and 3710 at x 8096, measured), and x 8307-8321 from
y 4078 down is `tc1_b` again (ns6 ends at y 3883; a C-shaped poly lies between).

### Other lines through the bus field (routing only)

- `tc1_x1`: poly from the east at y 4255-4275 (datapath), south at x 7807-7831 under the
  VSS bus to contact (7815,4372), metal west along y 4369-4383 to contact (7359,4352),
  poly west along y 4344-4362 to contact (7056,4352), metal south x 7049-7068 past
  y 4450.
- `tc1_x2`: poly from the east at y 4365-4383 to contact (8075,4372), metal south
  x 8067-8082 past y 4450.
- VCC bus y 4198-4250 from the foot of the centre rail east to x 8166, then south at
  x 8116-8165. A plain rectangle: the diagonal lines on its east end are the edges of
  the `tc1_l3_out` poly underneath. VSS bus y 4288-4335 from the foot of the left rail
  east to x 7995, then south at x 7943-7990.

Believed, not traced: L2, L3 and R3 have strong loads and wide pull-downs, so
`tc1_l2_out` (NOT a AND b), `tc1_l3_out` (a AND b) and `tc1_f` are lines with a heavy
load: strobes or enables. `a` and `b` together select which of them is active.

Sizes (W/L in px): weak loads 22/60 (R1, R2), 27/59 (L1), 28/59 (R4), 23/47 (L4);
strong loads 38/45 (R3), 40/42 (R5), about 65/36 (L2, L3; the strip's height under the
gate was not measured). Pull-downs 43/20 (R1, R4), 72/20 (L1), 55/18 (R2), 42/21 (L4),
67/18 (R3), 133/19 (R5, each of four), about 260/23 and 230/23 (L2, L3: each gate wraps
the drain region as an L). For L2 and L3 the W comes from rectangles drawn to the
visible edges; whether a source strip lies under the far end of each bottom arm
(x 7547-7591) was not settled, so their W is good to about 15 %.

## Ports

Region edges: x 8250 on the east (drawn to x 8350, where the datapath's first slice
starts), y 4450 on the south (tc2), y 2500 on the north, x 6400 on the west. "In/out"
is as seen from this block; where no driver has been found the direction is "?".

East side (into the datapath, or the random logic at its slice-0 position x 8290-8750):

| Name | Layer | Where it crosses | Dir | What |
|---|---|---|---|---|
| `tc1_ns5` | P | x 8350, y 2846-2868 | ? | north end of ns5, from contact (8271,2857) |
| `tc1_ns3` | M | x 8350, y 2720-2734 | ? | ns3 arrives from the east over the top of the datapath |
| `tc1_ns4` | M | x 8350, y 2764-2778 | ? | ns4, the same |
| `tc1_ns6` | M | x 8350, y 2807-2821 | ? | ns6, the same |
| `tc1_f` | P | x 8250, y 3348-3362 | out | R3 output; runs on under ns1..ns6 without contact, in the channel between cdp1's rows A and B |
| `tc1_a` | P | x 8250, y 3387-3402 | in (believed) | same channel, 40 px below `tc1_f` |
| `tc1_ns6` | P | x 8350, y 3516-3539 | ? | from contact (8313,3527) |
| `tc1_ns2` | P | x 8250, y 3556-3578; reaches x 8332 and turns south there | ? | from contact (8139,3567) |
| `tc1_w1` (= ns1) | P | x 8250, y 3691-3712 (seen to x 8350) | **in** (its only other end is L4's gate) | from contact (8139,3704) |
| `tc1_ns5` | P | x 8350, y 3728-3751 | ? | from contact (8270,3739) |
| `tc1_ns5` | P | x 8350, y 3822-3844 | ? | from contact (8270,3833) |
| `tc1_ns6` | P | x 8350, y 3859-3881 | ? | from contact (8313,3870), the south end of ns6 |
| `tc1_l3_out` | P | x 8250, y 4212-4228 (drawn to x 8350) | out | a AND b, to the datapath just above cdp1's row C |
| `tc1_x1` | P | x 8250, y 4255-4275 (drawn to x 8350) | ? | passes through: see the west side, y 4344-4362 |
| `tc1_x2` | P | x 8250, y 4365-4383 (drawn to x 8350) | ? | passes through: see the south side, x 8075 |

South side (tc2), west to east:

| Name | Layer | Where it crosses | Dir | What |
|---|---|---|---|---|
| `tc1_l1_out` | M | 7230, 4450 (W2 lower, x 7220-7240) | out | NOT b |
| `tc1_l2_out` | P | x 7422-7438, y 4450 | out | NOT a AND b; from the tap on track T2 |
| `tc1_l3_out` | P | x 7465-7481, y 4450 | out | a AND b; from the tap on track T1 |
| `tc1_b` | P | x 7503-7522, y 4450 | in (believed: its only other end) | from contact (7511,4417) |
| `tc1_ns3` | M | x 7894-7909, y 4450 | ? | from contact (7905,4370) |
| `vss` | M | x 7943-7990, y 4450 | | the VSS bus (y 4288-4335, from the foot of the left rail) turns south |
| `tc1_x2` | M | x 8067-8082, y 4450 | ? | to contact (8075,4372) |
| `vcc` | M | x 8116-8165, y 4450 | | the VCC bus (y 4198-4250, from the foot of the centre rail) turns south |
| `tc1_ns4` | M | x 8198-8212, y 4450 | ? | ns4 has no contact in this block |

West side (drawn to x 6960, the east edge of the gate columns, which are not traced):

| Name | Layer | Where it crosses | Dir | What |
|---|---|---|---|---|
| `tc1_l4_out` | P | x 6960, y 3388-3403, going west; ends at x 6931 | out | NOR(l2_out, w1); arrives by contact (7099,3897), metal x 7091-7110, contact (7100,3395). West of x 6968 the band has diffusion-coloured (tan) areas above (y 3360-3386) and below (y 3405-3423) it: believed the gate of one transistor at x 6931-6968 (one 4x view, not drawn) |
| `tc1_g` | P | x 6960, y 3995-4014, going west | out of this wire (it is a gate there) | to the big structure at x 6750-6940, y 3930-4200, see Not done |
| `tc1_ns2` | P | x 7180, y 2867-2883, going west | ? | far end of ns2 (1.5x view) |

South side, in the channel (tc2), west to east:

| Name | Layer | Where it crosses | Dir | What |
|---|---|---|---|---|
| `tc1_x1` | M | x 7049-7068, y 4450 | ? | from contact (7056,4352) |
| `tc1_g` | P | x 7134-7153, y 4450 | **in** (believed: every other end of `g` is a gate) | from contact (7315,4395) |
| `tc1_i` | P | x 7179-7196, y 4450 | **in** (its only other end) | from contact (7270,4437) |

North side:

| Name | Layer | Where it crosses | Dir | What |
|---|---|---|---|---|
| `vss` | M | right rail x 7771-7819, drawn y 3000-4000; it continues north through the top bus field (the bus lines cross it in poly) | | |

Seen while following these, **not mine and not drawn**: `cdp1_a0_q` (poly from the
datapath at y 3017-3040) turns north at x 8047-8072 and west again along y 2930-2950; it
passes 15 px from the `tc1_a` contact pad at (8010,3028) **without touching it** (field
gap at x 8030-8046, measured with `tc1_px.py row 3029`). `cdp1_a1_q` (poly, y 2978-2993)
turns north at x 8094-8112 up to y 2893 and west along y 2893-2907; two more polys of
the same kind (y 2850-2864 down x 8134-8152 to y 2935-2950; y 2805-2821 down
x 8181-8202 to y 2893-2908) nest round it: they are the row A outputs fanning out west
into the top bus field, all under ns1..ns6 without contact (1.4x view only).
A large C-shaped **poly** at x 8307-8360, y 3907-4062 (orange in the metal shot; at 1x
it looks like metal) lies between ns6's south end and `tc1_b`'s contact (8313,4090)
and touches neither (field at y 3896-3908 and 4056-4070, measured).

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

8. **Bump on `g`'s poly** at x 7007-7031, y 3976-4000, directly under the channel metal
   x 7001-7023. It looks like half a contact pad. Profiles along x 7012 show unbroken
   bright metal in both metal shots and plain salmon poly in `acid1b`, where a real
   contact 90 px away (7099,3897) shows a 12 px bright dot inside a thick dark ring and a
   green-tan patch. Working assumption: no contact.
9. **Direction of `b`, `g`, `i`.** "In" for these rests on every other end being a gate
   or (for `g`) a gate in the untraced structure at x 6750-6940. If tc2 finds no driver
   on the polys at (7512,4450), (7143,4450), (7187,4450), look again at that structure.
10. **ns lines' polys east of x 8250** were drawn from 1.4-1.9x views only as far as
   x 8350; what they meet there is outside this block.
11. The supplies of the gate columns (rails x 6682-6757 and x 6857-6932 near y 4000) are
   **not identified**: nothing traced ties them to the island's rails.

## Not done

- **Gate columns x 6400-7000, y 2650-4450**: nothing drawn. Dense random logic with large
  devices under wide rails (x 6510-6560, 6682-6757, 6857-6932 near y 4000) and thin
  verticals between (x 6745-6762, 6766-6785, 6808-6828, 6913-6932, 6938-6955, 6959-6977).
  It is not built like the island: budget for 3x views and profiles, not 2x.
- **The structure that `g` gates, x 6750-6940, y 3930-4200** (surveyed at 2.4-4.2x, not
  drawn because the circuit is not settled). Established, with the evidence:
  - `g`'s poly arrives along y 3990-4009, runs up x 6850-6860 and back west along
    y 3943-3961 to about x 6772: an L round a diffusion (region A, x 6863-6938,
    y 3924-3987) that has a large metal contact at (6897,3964) to the wide rail
    x 6861-6932.
  - Below the L's bottom arm is diffusion again (region B, y 4014-4030, x 6851-6938;
    tan under the rail on both sides of the salmon band in profiles along x 6875 and
    x 6905): so the arm is a **gate**, W about 75.
  - The west arm (y 3943-3961) crosses a diffusion column under the thin metal
    x 6808-6828 (tan at x 6806-6830 both at y 3928-3936 and at y 3968 onward, profile
    along x 6818): a second gate of `g`, W about 28.
  - Below B a much larger U-shaped poly (top bar y 4034-4053, legs x 6863-6887 and
    x 6923-6938, down to about y 4100) surrounds a diffusion island (x 6888-6923,
    y 4056-4133) with contact pits at (6902,4090) and (6913,4117). The rail metal is
    continuous from region A over `g`'s arm, B and the U to the island (`acid1b` shows
    protected colours all the way along x 6875 and x 6905; a slit narrower than about
    20 px would not show, but an island of metal inside the rail would have nowhere to
    go), so **A and the island are believed to be on the same rail** and the L and the U
    two transistors in parallel from that rail to node B. The U's poly has a pad at about (6829,4091) under the thin metal
    x 6808-6828 (dark ring in both metal shots): its gate signal comes on that metal.
  - West of the column: a poly block x 6752-6792, y 4032-4100 (textured in the open,
    its west 10 px salmon under the edge of the rail x 6682-6757), with a stem up
    x 6752-6763 to y 3992 and a heavy-outlined box with an inner square (x 6765-6799,
    y 3987-4020: looks like a buried contact) above it; a diffusion (tan, x 6710-6749,
    y 4033-4110) lies under the rail to its west. Read as the **load** of node B (strip
    from the rail's diffusion under the block to the column, gate tied at the box), but
    what the box joins was **not** settled. The column probably joins B: in the 14 px
    strip between them (x 6836-6850, in the gap between the two metals) a profile along
    y 4021 gives `acid1b` 112-144/59-77/56-77 (red, not the khaki of open field) and the
    metal shot 155/145/95 (not the orange of poly), i.e. a narrow open diffusion.
  - The ns-line checks of this run are worth repeating here: `sel_tracks.py` reported
    breaks on ns3 at y 3341-3367 and 2953-2975 and on ns5 at y 3365-3387; profiles show
    metal with plain poly or field under it at all three (chip 2 has blemishes there,
    chip 1 does not). They are not contacts.
  - Candidate reading: node B = NOR(`g`, signal on the metal x 6808-6828), a strong
    driver, rail x 6861-6932 = VSS, rail x 6682-6757 = VCC. Not adopted.
- **Channel x 7000-7170**: verticals at x 7002-7022 (from contact 7010,3092 down), x 7048-7068
  (from contact 7056,3138 down), x 7091-7110 (upper piece from the north to contact
  7098,3180; lower piece is `tc1_l4_out`), x 7133-7152 (from the north down to y 4050,
  west to contact 7099,4047, poly west y 4035-4055). Each contact's poly goes west into
  the gate columns. Two C-shaped polys lie under them (y 3345-3360 / x 7135-7154 /
  y 3476-3491, and y 3518-3534 / x 7050-7069 / y 3845-3865). None drawn.
- **Top bus field y 2500-2975**: seven bus lines (y 2554, 2598, 2641, 2684, 2727, 2771,
  2814), each crossing the right VSS rail in poly between contacts at x 7663 or 7707 and
  x 7858 or 7902 (alternating). Only the y 2727 (ns2) and y 2771 (`w1`) lines are drawn.
  The y 2814 line's poly runs on east from contact (7707,2811) without a second contact
  in view. The row A outputs of cdp1 fan out west into it (see Ports).
- Far ends of ns3..ns6 and of ns2's west poly; `tc1_x1`, `tc1_x2` (all in the Ports table).
