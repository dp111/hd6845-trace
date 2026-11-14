# Clock block (9450-13100 x 18550-19950)

Status: gate row and wiring region traced (trace/clock.txt). Driver logic and the two
big arrays surveyed, not traced. Function of the block as a whole not yet established.

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

## Big arrays (9570-10650 x 19200-19800): not yet examined

Two large multi-finger arrays with a small one between them. A wide metal runs up
into the core from each (x about 10690 and x about 9480).

## Open questions

- What `ck_src` is, and therefore what the block produces. Candidates: a clock
  phase fed back from the arrays, or a separate timing signal. CLK enters the driver
  logic directly as well (`clk_b`, `clk_p`).
- Whether the block bootstraps (see AMB-006).
