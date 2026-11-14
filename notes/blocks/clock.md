# Clock block (9450-13100 x 18550-19950)

Status: gate row, wiring region and output stage traced (trace/clock.txt). Driver
logic surveyed, not traced.

## Summary so far

- The main internal clock is `ck_out` = NOT CLK. The CLK pin node runs along the
  bottom of the block as a metal line (y 19892-19912) and, through one contact at
  10985,19901, drives a three-stage buffer made of the two big arrays. Nothing but
  the pin feeds that buffer: the clock is not gated or divided.
- A second, unrelated-looking part of the block (gate row plus driver logic) takes
  a global signal `ck_src`, makes both polarities of it (lines A and B) and combines
  them with CLK in two mirrored, apparently bootstrapped, driver circuits. What
  those produce is not yet known.
- CLK therefore reaches the core by at least three routes: `ck_out` (heavy, inverted),
  `clk_b` from the input row (light, same sense as the pin), and the pin node itself.

## Gate row (11150-12150 x 18600-19000): traced

Six inverters. Loads on the VCC band along the top, pull-downs under the VSS rail at
y 18795-18848. Two metal lines cross the loads: line A (y 18700-18722) and line B
(y 18745-18768).

| Gate | Input | Output | Notes |
|---|---|---|---|
| g5 | `ck_src`: poly from a bus line at y 18455-18480 above the VCC band, which leaves left (not followed) | line B (`ck_b`) | tall weak load; output also tapped to a plain diffusion rectangle at 11728-11897 x 18975-19150 (added capacitance) |
| g6 | line B | line A (`ck_a`) | strong load (W/L about 68/26); output also goes up in poly at x 12098-12125 to a bus line at y 18455-18480 that leaves right (not followed) |
| g1, g2 | line B | `ck_g1`, `ck_g2` | so `ck_g2` = line B re-buffered |
| g3, g4 | line A | `ck_g3`, `ck_g4` | so `ck_g4` = line A re-buffered |

So `ck_b` = NOT `ck_src`, `ck_a` = `ck_src`. Lines A and B also continue right along
the row to x 13010 / 13090, where they turn up into the core (not followed).

## Wiring region (11950-12900 x 18850-19950): traced

Seven nets go down on vertical metals and enter the driver logic in metal at
x about 12000, each crossing the VCC metal at x 12088-12140 on a poly bar:

| Enters at y | Net | Via |
|---|---|---|
| 19254 | line B | V1 (x 12165-12190) |
| 19294 | line A | V2 (x 12208-12232) |
| 19490 | `clk_b` (CLK, buffered, same sense as the pin) | V5 (x 12557-12583) |
| 19532 | `ck_g4` (line A re-buffered) | V4 (x 12302-12318) |
| 19573 | `ck_g2` (line B re-buffered) | V3 (x 12255-12277) |
| 19900 | `clk_p` (the CLK pin node) | V6 (x 12600-12630), then along the bottom |

Six island devices to VCC hang on these nets (AMB-006, taken to be clamps). A plain
VCC diffusion block with nine contacts lies under the gate row's lines at
12385-12790 x 18600-18850.

## Driver logic (10900-12000 x 19140-19890): surveyed

Rails: VCC along the top (y 19160-19212, with an eight-contact diffusion at
11260-11600), VSS across the middle (y 19370-19452, entering from the left at
y 19340-19385). VCC also comes down the right side on the metal at x 12088-12140.

The two halves are roughly mirror images about x = 11437, but not near the centre.

What has been read so far (left half; mirror positions in brackets):
- Under the VSS rail there is a band of diffusion crossed by vertical poly gates,
  with VSS contact pairs at x 11070, 11213, 11355 (y 19390 and 19430). Above the rail,
  at y 19325-19365, three wide poly blocks: A 11020-11140, B 11160-11275,
  C 11300-11410. Vertical poly legs hang from them and run down below the rail.
- Below the rail the diffusion continues as a tall rectangle R1, 11050-11250 down to
  y 19850 (mirror 11625-11825). Two legs run down it lengthwise: 11100-11125, which
  carries on past the bottom edge, and 11155-11185, which stops just past it. With
  W of 400 or more these are the big devices of the block, either wide transistors
  or bootstrap capacitors.
- A second outline, R2, overlaps R1: 11135-11388 with its bottom edge at y 19885
  (mirror about 11550-11740). R1's own edges remain visible inside R2, so the two
  are different layers. One is diffusion; the other may be the depletion implant.
  If so this is the first place the implant outline has been seen (AMB-002).
- A smaller tall diffusion at 10920-11030 down to y 19760 (mirror 11840-11950) holds
  the lower end of the long vertical poly at x 10975-11003 (which starts near the
  VCC rail at y 19200). The poly jogs, passes a small box at 10940-10995 x 19632-19665
  and widens to 10950-10992 down to y 19775. Probably a bootstrap capacitor.
- Leg 11250-11290 ends at y 19545 on a contact at 11275,19580 fed by the `ck_g2`
  metal line. Its mirror, at 11592,19570, is fed by the `ck_g4` line (the `ck_g2`
  line jogs round it). So the left half is driven from line B and the right half
  from line A.
- Line B's metal (y 19240-19265) runs the full width of the block. Line A's
  (y 19292-19312) runs from the right as far as x 11055; a separate piece continues
  from a contact at 11020,19292 to the left edge.
- Full-height vertical poly strips at 11390-11416 and 11523-11547 run down past
  y 19890 towards the lines along the bottom of the block.

## Output stage: the two big arrays (9500-10730 x 19180-19815): traced schematically

The two arrays are one circuit, a three-stage buffer ending in a push-pull pair:

```
ck_p --> [inverter: s3,s4,s5, W 3x480] --> ck_t --> [inverter: s1,s2, W 2x480] --> ck_n2
ck_n2 --> [F3, W 345] --> ck_ga   (pull-up gate of the output)
ck_out:  pull-up  = group A, W 2x483 + 145, gate ck_ga, from VCC
         pull-down = F1 + F2, W 2x345, gate ck_n2, to VSS
```

So `ck_out` = NOT `ck_n2` = NOT `ck_p`, delayed by three stages.

`ck_p` is the CLK pin node itself. The gates s3-s5 are joined along the bottom and
continue down in poly at x 10650-10695 to a wide poly bar (10650-11000 x
19892-19935) lying under the metal line at y 19892-19912; a contact at 10985,19901
joins the two (seen clearly at 2.9x). That metal line is the one that arrives from
the CLK protection cell via the vertical metal at x 12600-12630, and it carries on
to the left past x 9420 (not followed).

Supplies: VSS comes down from the core on the wide metal at x 10755-10815, branches
right at y 19335-19375 into the driver logic's middle rail, and turns left at
y 19765-19815 as the bus under both arrays. VCC arrives twice: on the wide metal at
x 10652-10722 from the core (it feeds only the load of `ck_t`), and on a wide metal
from the left at y 19095-19145 that spreads along the top of the left array
(y 19245-19300).

Loads: `ck_t` has a 154/27 load at x 10652-10680; `ck_n2` has a 174/34 load (group C,
x 10130-10165). Both are about 5.5 squares wide, which is what first suggested that
the wide metal over group C is VCC and not a signal.

`ck_out` leaves the block two ways. Up the left side on a metal at x 9515-9545 and
away to the left at y 19240-19262 (not followed; it seems to reach a contact at
9340,19240). And downward at x 9848-9870 from the bus along the bottom, right along
y 19848-19865 to x 10850, up at x 10840-10870 to a contact at 10852,19422, under the
VSS branch in poly to 10852,19292, and on up into the core in metal (seen at 0.85x;
not yet in the trace).

Established by close-up (6x): the gate bar of group A (9640-9830 x 19195-19240)
continues down its right-hand side at x 9797-9830 to the contact at 9810,19337 on
the `ck_ga` metal; the bar that joins F1-F3 (y 19357-19372) is a separate piece of
poly just below that contact. This fixes the polarity of the output.

Inferred, flagged `?` in the trace:
- s1 and s2 are driven by `ck_t` through the two-contact pad at 10285-10375 x
  19180-19215. Seen: the pad and its contacts under the top bus, and the two gates
  ending beside it. Not seen: the poly join itself.
- F1, F2 and F3 share one gate bar, fed by the poly that comes down at x 9985-10010
  from the `ck_n2` pad.
- The two load gates are tied to their output sides (boxes seen at the top end of
  each gate).

Not yet traced here: the load of `ck_ga` (the small device at 10030-10160 x
19430-19680 is the candidate), and whether `ck_ga` is bootstrapped.

## The gate row's input line (`ck_src`) is a global signal

Followed from g5's gate: bus line y 18458-18480 leftwards to a contact at
10897,18468; a short poly link joins it to a contact at 10808,18470 and, by a branch
up at x 10850-10870, to a contact at 10855,18385 on the bus line at y 18375-18400
(which runs right). From 10808,18470 a metal runs down to 10808,18600, crosses under
the wide metal at x 10720-10770 in poly to 10685,18600, runs left in metal along
y 18590-18612 to x 10255, up at x 10250-10290 to y 18425, and left along y 18410-18440.
From there it is one of the lines of the bottom bus field: poly links under vertical
metals at x 9740-9840 (contacts 9870,18420 and 9650,18420), at x 8440-8560 (contacts
8600,18425 and 8380,18425) and at x 7470-7510 (contacts 7600,18425 and 7425,18425),
ending at a contact at 6800,18420. A poly line runs up from there to a contact at
6800,17990 at the foot of the innermost vertical line (x about 6790) of the bundle
that climbs the left bus field.

So `ck_src` is not made locally by anything traced so far. Either it is the block's
own output coming back after distribution, or it is a signal from elsewhere that the
clock block needs. Lines A and B, its two buffered polarities, are themselves sent
on to the right-hand side of the core.

## Open questions

- What `ck_src` is, and therefore what the block produces. Candidates: a clock
  phase fed back from the arrays, or a separate timing signal. CLK enters the driver
  logic directly as well (`clk_b`, `clk_p`).
- Whether the block bootstraps (see AMB-006).
