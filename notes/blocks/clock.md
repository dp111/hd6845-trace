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

## Driver logic (10900-12000 x 19140-19890): being traced from the clean shot

Read from `acid1b` with `metal1` for contacts (2026-11-15). The earlier survey of this
block from the chip-2 shots was wrong in several places and is superseded.

It is two big push-pull drivers, one per half, that drive lines A and B themselves:
the left half's output diffusion is contacted by line A at (11030,19298), the right
half's by line B at (11838,19250). So A and B each have two drivers, a small inverter
in the gate row and a large push-pull here. The halves mirror each other about
x = 11437 except for which line the output pad sits under.

Left half, as read so far:
- Pull-up: the long vertical poly at x 10980-11000 is its gate. Left of it
  (x 10922-10978) is diffusion on VCC (contact at 10937,19188 under the top rail);
  right of it (x 11003-11035, widening to a contact box 11008-11055 x 19275-19322) is
  the output. Net of the gate: N1.
- N1's load: a diffusion finger comes down from the VCC diffusion at x 11258-11318,
  crossed by a poly gate at y 19218-19270 (W/L about 60/50). The gate's left end
  turns up at x 11228-11250 to a poly bar under the top rail (y 19165-19191) that
  runs left to the top of the long vertical poly, and turns down to a buried-contact
  box at 11228-11258 x 19278-19312 on the finger below the gate. So the load's gate
  is tied to its own output, and that output is N1.
- Below the load, N1's diffusion narrows to a neck (x 11285-11300, y 19325-19365)
  between the two poly blocks and widens again under the VSS rail at x 11277-11303.
- Under the VSS rail (y 19370-19452), left to right: VSS contacts 11055-11085;
  gate strip a (11100-11125); a node (11127-11160); gate strip b1 (11160-11185);
  VSS contacts 11200-11235; gate strip b2 (11245-11275); N1 (11277-11303); gate
  strip c1 (11305-11330); VSS contacts 11340-11380; gate strip c2 (11385-11405).
  b1 and b2 are joined above the rail by poly block B (11163-11272 x 19329-19365),
  c1 and c2 by block C (11305-11410). Strip a ends in a rounded top at y 19340.
- So N1 = NOR(b, c), and the node between a and b1 is pulled down by a or b. A
  narrow diffusion appears to run from that node up at x 11150-11165 and left along
  y 19318-19332 to the output's contact box, which would make it the output.
  To be confirmed.
- The gate strips run on down below the rail for about 400 px over diffusion: these
  are the very wide pull-downs (and, for the long vertical poly, the pull-up and a
  capacitor to the output at its lower end).
- A second load (x 11402 onward) mirrors the first, with its buried-contact box at
  11366-11400 x 19275-19320.

What the clean shot's colours mean is in `notes/layers.md`; the one surprise was that
metal lines protect a margin around themselves, so a 25 px gap between two lines
shows only as a thin dark bar, not as "open" colours.

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
