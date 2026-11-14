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

## Big arrays (9570-10650 x 19200-19800): partly read, not traced

Supplies here:
- VSS comes down from the core on the wide metal at x 10755-10815. It branches right
  at y 19335-19375 into the driver logic's middle rail, carries on down, and turns
  left at y 19765-19815 to run under both arrays as their bottom bus.
- The wide metal at x 10652-10722 (from the core, ends at y 19410) is taken to be VCC:
  the only thing under it is a small device whose gate is tied back to its other
  side, i.e. a load.

Right-hand array (10235-10725 x 19180-19790), columns left to right:

| x | What |
|---|---|
| 10237-10278 | col 1, diffusion with contacts, joins the bottom bus (VSS) |
| 10280-10300 | gate s1 |
| 10300-10353 | col 2, joins a metal that leaves left at y 19235-19262 |
| 10355-10378 | gate s2 |
| 10380-10423 | col 3, joins the bottom bus (VSS) |
| 10425-10447 | gate s3 |
| 10449-10495 | col 4, joins the top bus (y 19183-19212) |
| 10497-10520 | gate s4 |
| 10522-10565 | col 5, joins the bottom bus (VSS) |
| 10567-10590 | gate s5 |
| 10592-10628 | col 6, joins the top bus; diffusion probably extends to x 10652 |
| 10652-10680 | gate of the load, box at its top end 10645-10682 x 19237-19262 |
| 10683-10725 | load's supply side, three contacts to the metal at x 10652-10722 |

So there are two large inverters here. Gates s3-s5 (W about 3 x 480) pull the top bus
low against the load. Gates s1-s2 pull col 2 low. s3-s5 have separate rounded top
ends and are joined at the bottom by a poly bar (y 19752-19775) that runs right and
then down in poly at x 10655-10690 to a poly bar along the bottom of the block
(y 19905-19930), heading for the driver logic. s1 and s2 end at the top at y 19222
next to a horizontal band (y 19215-19232, x 10240-10440) and the top bus has a pad
with two contacts at 10285-10375 x 19180-19215; the likely reading is that the top
bus drives s1 and s2 through that pad, making the two inverters a chain. Not
confirmed. s1 and s2 also have long feet under the bottom bus (to y 19790).

Left-hand array (9500-10220 x 19190-19790), partly read:

- The wide metal that enters at the top left (x 9575-9625 from y 19100, where it
  comes in from the left at y 19095-19145) spreads along y 19245-19300 from x 9580
  to 10120. Columns A1 (x 9600-9632) and A3 (9738-9770) and column C1 (10085-10115)
  contact it. Reading this metal as a signal makes the device between C1 and C2
  nonsensical, and reading it as VCC makes everything a pull-up, so it is taken to
  be a second VCC feed. Not confirmed.
- Group A, gate GA: a poly bar at 9640-9815 x 19195-19240 with two fingers down at
  x 9640-9665 and 9712-9735 (to y 19750), joined at the bottom by a bar
  (y 19742-19762) to a third, short, wide finger at 9555-9595 x 19580-19740.
  Fingers 1 and 2 lie between A1/A3 and column A2 (9672-9705, contacts from
  y 19320). The short finger lies between A1 and a column at 9510-9535 that joins
  a bus along the bottom (y 19745-19790, x 9510-9880). If A2 is on that bus too,
  group A is one big pull-up from VCC to that bus.
- Group B (9800-10030): columns at 9805-9835, 9870-9905, 9940-9970, 9995-10030
  with three gate fingers between them; a metal at y 19325-19360 (x 9800-10010)
  crosses their tops. Not yet read.
- Group C: gate 10130-10165 (y 19225-19420) between C1 and column C2
  (10180-10210). C2's metal runs up to a top strap (y 19195-19228, x 9990-10215),
  which joins the metal leaving the right-hand array's column 2 at y 19235-19262
  and, at its left end, a two-contact pad at 9985-10030 x 19195-19235.
- A small device below group C: poly block 10060-10090 x 19500-19660 beside a
  three-contact column at 10110-10150.

The two arrays are therefore one circuit, not two independent drivers.

A metal at x 10840-10865 comes down from the core to a contact at 10852,19292,
crosses under the VSS branch in poly to 10852,19422 and continues down. The bus
line carrying `ck_src` (y 18455-18480) runs left to a contact at 10895,18467 and
links to a vertical metal near x 10810 that heads down this way, so `ck_src` very
probably comes from this part of the block: the gate row re-buffers something made
here, and the driver logic's two halves take that signal and its complement back.

## Open questions

- What `ck_src` is, and therefore what the block produces. Candidates: a clock
  phase fed back from the arrays, or a separate timing signal. CLK enters the driver
  logic directly as well (`clk_b`, `clk_p`).
- Whether the block bootstraps (see AMB-006).
