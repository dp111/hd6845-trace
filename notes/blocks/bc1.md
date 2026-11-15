# bc1: bottom-centre random logic, upper left part (x 7000-9000, y 14050-16300)

Trace: `trace/bc1.txt`. Scratch: `cache/scratch/bc1/`. Coordinates are metal-shot pixels.

## Status

Traced and shipped (extracts clean, overlays checked on both shots): **column A of the
right gate group**, six gates between the rails at x 8360 and x 8534 (y 15070-15990):
two inverters, three 2-input NANDs that decode two bus lines (`bc1_s0`, `bc1_s1`) into
three of the four one-of-four lines (active low), and one more inverter with a weak
load. All their wiring in the channel x 7990-8250 is traced.

Not traced: everything else (see Inventory and Not done). In particular the dense
logic right of the VCC rail (x 8560-8900), the whole left gate group (x 7100-7850) and
the routing field above y 14900 are only surveyed.

## Inventory

Survey views: `cache/scratch/bc1/sv_metal.png`, `sv_acid.png` (whole block, 0.6x).

The block has three parts.

**1. Routing field, y 14050-14900 (whole width).** Not logic.
- Six horizontal poly lines at y 14085, 14128, 14172, 14215, 14258, 14300 (pitch 43),
  x 7000 to about 8050 and on to the right in a nested staircase (x 8050-8200,
  y 14045-14240). They carry the six data tracks of `cdp4` row D (`cdp4_in6_s1..s6`):
  `cdp4_in6_s1` (metal x 8073) ends on a contact at (8075,14085) on the first line;
  the other lines step up at x 8100-8190 and continue right under the VCC rail x 8228
  to the other tracks (seen at 2x, not traced). Each line has a contact to a vertical
  metal further left: (7180,14080), (7222,14128), (7268,14172), (7312,14215),
  (7355,14258), (7400,14300); those six verticals arrive from above (y < 14040) and
  appear to end on the contacts; the poly lines continue left past the contacts to
  x 7000 (seen at 1.6x, `topL.png`).
- The strobe `cdp4_ld6` (metal x 7947) comes down to y about 14295 and turns left into a
  horizontal metal at y 14270-14295 (seen at 2x to x 7760; not followed further).
- Supplies: the VSS rail x 8013 of `cdp4` ends in a wide horizontal metal band
  y 14250-14305 running right to x about 8300, where rail R1 goes down (seen at 0.6x and
  2x). The VCC rail x 8228 turns right at y 14170-14240 and feeds a wide vertical
  x 8405-8465 that comes down to y 14930 and widens right into rail R2 (seen at 0.6x and
  2x; the corner at y 14925-14985 is in `t1.png`).
- A bus of 13 horizontal metal lines, y 14354 to 14873 (pitch 43.5: 14354, 14397, 14439,
  14482, 14526, 14570, 14613, 14656, 14699, 14744, 14786, 14832, 14873), x 7780-8280.
  Left ends: contacts in two columns at x about 7790 and 7830 onto horizontal polys
  arriving from the left. Right ends: most lines end on contacts at x 8250-8290 and
  continue (in poly under the rails x 8300-8560, then metal again from x 8560) towards
  x 9000. **The two lowest lines turn down into the channel: y 14832 = `bc1_s0`
  (turns down at x 8186), y 14873 = `bc1_s1` (turns down at x 8143)** (traced, `t1.png`).
- Vertical metals x 7000-7760 crossing the field (bundle continuing from the left bus
  field), not examined.

**2. Right gate group, x 7850-8960, y 14900-16300.**
- Wiring channel x 7860-8250: vertical metal tracks at x 7882, 7924, 7969, 8012, 8056,
  8098, 8143, 8186, 8229 (measured), horizontal polys under them into the gates.
  Tracks 8012-8229 are traced as far as they serve column A. Not traced: track 7969
  (from a contact at (7880,14910) via a horizontal at y 14912, down the whole channel to
  a contact at (7968,16300)); track 8012 below y 15865 (starts at contact (8012,15865)
  on a poly going left along y 15865); tracks 7882 (from contact (7880,15510)) and 7924
  (from contact (7925,15700)).
- Rail R1 = VSS, x 8336-8384. Rail R2 = VCC, x 8510-8558. Rail R3 = VSS, x 8686-8731.
- **Column A** (between R1 and R2), top to bottom: gates 1-6, y 15070-15990 (traced).
  Below, y 16000-16300 and on below the block: a different, wider gate structure under
  R1 (diffusion x 8300-8395, polys at y 16032, 16107, 16125, 16170, 16215) with loads at
  x 8430-8500 (not traced; it continues below y 16300).
- **Column B** (right of R2, x 8560-8900): dense. Loads hang on the right side of R2
  (poly blocks at x 8570-8620: y 14975-15050, 15105-15140, 15450-15520, ...), pull-downs
  under and right of R3, horizontal polys going right to contacts on vertical metals
  x 8790, 8837, 8881, 8925. A thin vertical metal x 8642 runs down the whole column
  between R2 and R3 (it is `bc1_dec00_n`). Only its first gate is understood (see Logic,
  "inverter A, seen not traced").
- Right of x 8900: vertical tracks at x 8925, 8967, ... (boundary with `bc2`), not
  examined.

**3. Left gate group, x 7100-7850, y 14950-16300.** Not examined beyond the survey.
Wide vertical metals at x about 7310, 7490 and 7665 (rails; which is which not
established). Loads (textured poly blocks) seen at x 7250-7290 and x 7400-7460; two
large devices at 7330-7480 x 15020-15100 and 15240-15330 (wide poly rings: drivers?).
Horizontal polys enter from the left field (x 7000-7150) with contacts on verticals at
x 7060 and 7110.

## Logic

### Column A (traced)

Structure of every gate: VSS contact on R1, the diffusion column under the rail crossed
by one or two horizontal gate polys that arrive from the channel, the output node
below them; from the node a diffusion strip runs right through a depletion load (poly
block 8448-8500, strip under it) to a land contacted by R2; the load gate is tied to
the strip by a buried contact on a hook-shaped bump (above the block; below it in
gate 6). The node also runs left to a buried contact (x 8271-8308) into a poly line
that goes to a contact on a channel track.

| Gate | y | Function | Inputs (track) | Output (track) |
|---|---|---|---|---|
| 1 | 15072-15196 | `bc1_s0_n` = NOT `bc1_s0` | s0: x 8186 above y 15089, x 8229 below; contact (8229,15128) | x 8186, y 15160-15617, contact (8186,15172) |
| 2 | 15203-15327 | `bc1_s1_n` = NOT `bc1_s1` | s1: x 8143, contact (8143,15262) | x 8098, y 15291-15739, contact (8098,15303) |
| 3 | 15335-15507 | `bc1_dec00_n` = NAND(`s1_n`, `s0_n`) | contacts (8098,15390), (8186,15433) | x 8056 up to contact (8056,14960) |
| 4 | 15507-15677 | `bc1_dec10_n` = NAND(`s1`, `s0_n`) | contacts (8143,15563), (8186,15605) | contact (8056,15652), metal left to x 8012, up to y 14913, right to contact (8100,14913) |
| 5 | 15676-15855 | `bc1_dec01_n` = NAND(`s1_n`, `s0`) | contacts (8186,15738), (8229,15780) | contact (8186,15823), metal to x 8143, down to y 16170, left to x 8056, down out of the block |
| 6 | 15853-15990 | `bc1_g6_out` = NOT `bc1_g6_in` | x 8143 from below the block, jog at y 16260 to x 8186, contact (8186,15910) | contact (8229,15956), x 8229 down to contact (8229,16107), poly right into the untraced gates below y 16000 |

- In each NAND the input nearer VSS is the first one listed.
- Low when: `dec00_n` s1=0,s0=0; `dec10_n` s1=1,s0=0; `dec01_n` s1=0,s0=1. There is no
  gate for s1=1,s0=1 in this column.
- Loads: gates 1-5 W/L about 26/52; gate 6 about 33/78 (weaker).
- Where the outputs go (traced): `bc1_dec00_n`: poly from (8056,14960) right along
  y 14960, up at x 8255, right along y 14913 under R1 and the R2 feeder to a contact at
  (8642,14910) on the thin vertical metal x 8642 that runs down column B (seen to
  y 16000; its taps not traced). `bc1_dec10_n`: poly from (8100,14913) right, up at
  x 8210, right along y 14870 under R1 to about x 8500, where it continues right
  under or into a horizontal metal line (not resolved, not followed).

**Believed, not traced:** a 2-to-4 decode of a two-bit register field that arrives on
the bus from the left (the widths suggest one of the two-bit fields of R8 or R10, but
the two bus lines have not been followed to a register).

### Inverter A at the top of column B (seen, not traced)

y 14940-15060. VSS contact on R3 at (8715,14965); gate poly y 14988-15009 from a
contact at (8838,14998) on the vertical metal x 8837; output node under R3 (y
15009-15033) runs left to a load at x 8572-8603 against R2 (VCC land 8515-8565 x
15008-15058) and right to a buried contact at 8768-8795 x 15025-15054, from which a poly
leaves right along y 15042 (seen to x 8892). The load's gate tie is a box at 8616-8651
x 14977-15006 that lies under the thin metal x 8642: whether that box is a buried
contact or a metal contact from x 8642 was not settled, so the gate is not in the trace.
The vertical x 8837 has further contacts at about y 15127, 15300, 15455, 15520.

## Ports

| Name | Layer | Where it crosses | Direction | What |
|---|---|---|---|---|
| `bc1_s0` | metal | bus line y 14832, drawn from x 8040 (the line continues left to about x 7790) | from outside | decoder input, low bit |
| `bc1_s1` | metal | bus line y 14873, drawn from x 8040 (continues left to about x 7790) | from outside | decoder input, high bit |
| `bc1_dec01_n` | metal | x 8056, y 16300 (continues down) | driven inside | low when s1=0, s0=1 |
| `bc1_dec10_n` | poly | y 14870, drawn to x 8500 (continues right) | driven inside | low when s1=1, s0=0 |
| `bc1_dec00_n` | metal | x 8642, drawn y 14898-15060 (continues down column B) | driven inside | low when s1=0, s0=0 |
| `bc1_g6_in` | metal | x 8143, y 16300 (continues down) | from outside (below) | input of inverter 6 |
| `bc1_g6_out` | poly | y 16107, drawn to x 8300 | driven inside | into the untraced gates at y 16000-16300 |
| `vss` | metal | R1 x 8360, drawn y 14890-16300 (continues both ways) | - | rail |
| `vcc` | metal | R2 x 8534, drawn y 14990-16300 (continues both ways) | - | rail |

Not yet drawn, seen in the survey (for the next agent): the six data polys at x 7000
(y 14085..14300) and their six verticals at y 14040 (x 7180..7400); the strobe
`cdp4_ld6` heading left along y 14285; the 13 bus lines at their left ends (x 7790) and
right ends.

## Ambiguities

1. **Supply identity of R1 and R2.** Taken from the orientation of all six loads (tie
   on the R1 side, land on the R2 side) and from the low-zoom path of the rails up to
   the `cdp4` rails (R1 to the VSS rail x 8013 through the band y 14250-14305; R2 to the
   VCC rail x 8228 through the wide vertical x 8405-8465). The joints of those paths
   were seen at 0.6x and 2x only and are not drawn.
2. **Load hooks.** The hook between each load block and the strip is drawn as a
   diffusion bump with a buried contact at its end (as in the pilot example). It could
   equally be a poly stem with the buried contact on the strip; the connectivity (load
   gate tied to the output) is the same.
3. **Right end of `bc1_dec10_n`** (poly y 14870 at x about 8500): the poly appears to
   continue right underneath a horizontal metal line that starts at x 8510; a contact
   there was not looked for.

## Not done

- Column B, x 8560-8900, y 14940-16300 (dense; start with `d1a.png`, `e1.png`). Open
  questions there: the boxes under the thin metal x 8642 at 8616-8651 x 14977-15006 and
  8621-8648 x 15157-15193 (buried contacts or taps of `bc1_dec00_n`?); the island at
  8569-8619 x 15145-15190 with a metal contact at (8590,15170) to a short vertical metal
  x 8592 that ends on a second contact at (8590,15380).
- Column A below y 16000 (the gates fed by `bc1_g6_out`; contacts at (8290,16030),
  (8229,16171), (8143,16215)).
- Left gate group x 7100-7850.
- Routing field y 14050-14900: draw the data polys, the strobe, the bus.
- Channel tracks x 7882, 7924, 7969 and 8012 below y 15865.
