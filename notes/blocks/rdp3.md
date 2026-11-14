# rdp3: right datapath, lower rows

Region: x 13350-16950, y 10700-12900, plus x 13350-15800, y 12900-13480.
Trace: `trace/rdp3.txt`. Scratch: `cache/scratch/rdp3/`. Tool: `tools/rdp3_sharp.py`
(view.py with an unsharp mask; the junctions below were judged with it at 3-6x on a
median composite of the cells, `--comp r0w`).

## Status

- Row AR (the row above the decode array, y 13010-13280): one cell traced, placed five
  times, checked against the photo, extracts as five latch bits. Shipped.
- Everything above y 13000 (routing zone, two bands of array cells): surveyed only.

## Inventory (survey)

| y | x | What |
|---|---|---|
| 10700-10940 | 13780-16900 | bottom edge of the cells above (rdp2) and a band of horizontal lines |
| 10950-11560 | 13780-16900 | array band B2: three sub-rows of cells (about y 10950-11150, 11170-11360, 11380-11560), 8 slices at 390 px, slice origins about x 13780, 14170, ..., 16510 |
| 11560-11780 | 13780-16900 | gap crossed by the per-slice vertical lines and rails |
| 11780-12380 | 13780-16900 | array band B1: looks like a copy of band B2 (same three sub-rows), 8 slices |
| 12380-13000 | 13350-16950 | routing: per-slice verticals come down from B1; a group of about 10 horizontal metal lines at y 12700-12960 runs to the left edge; at the right, wide diagonal metals (x 16000-16900) |
| 13010-13280 | 14140-16160 | row AR: 5 latch cells at 390 px pitch (traced) |
| 13280-13500 | 14450-16300 | the five outputs of row AR, nested L-shaped lines going right |
| 10700-13480 | 13350-13760 | bundle of about 14 vertical metal lines down the left edge, with horizontal taps into the array |

Wide vertical metal rails, two per slice, run through everything: VSS at x 14175 + 390k
(60 wide) and VCC at x 14382 + 390k (56 wide). The VCC rails continue down into the VCC
bus of the decode array (y 13518); the VSS rails end at the bottom of row AR (y 13277),
except the one at x 16125, which runs on downwards and bends left (areg region).
Identification: both depletion loads of every AR cell hang from a diffusion land
contacted by the x 14382 + 390k rail, and both pull-downs have their sources on the
lands contacted by the x 14175 + 390k rail.

## Logic

### Row AR: five transparent latch bits (traced)

Cell `rdp3_ar`, master at x 14597-14987 (slice s1), instances s0..s4 at dx = -390, 0,
390, 780, 1170. Per cell, 5 transistors:

```
a   <- bus      through pass transistor T1 when rdp3_ar_ld is high   (T1 34/28 at 14623,13074)
n2  = NOT a     pull-down T_b 51/22 at 14621,13178; load L2 30/52 at 14732,13126
q   = NOT n2    pull-down T_a 52/22 at 14911,13124; load L1 28/49 at 14822,13086
```

- `rdp3_ar_bus_sN`: a vertical metal line (28 wide) that comes down from the array above
  at x 14625 + 390(N-1) and ends at the cell bottom. Contact at the top of the cell
  (14622,13035) to a diffusion land; the strip from the land passes under the strobe
  poly (T1) and ends on a buried contact to the poly that is the gate of T_b (node a).
- `rdp3_ar_ld`: one poly line along the top of the whole row (y 13015-13043). In each
  cell it loops down round the bus contact, and the loop is T1's gate. Its right end
  (16285,13022) has a contact to a thin metal line that goes down into the areg region.
  So all five bits load together when that line is high.
- `q` is in the same sense as the bus. It leaves each cell downward on a poly strip
  (buried contact on the output land at 14886,13232), then by a contact at
  (14886 + dx, 13308) onto a metal line that runs down and to the right, ducking under
  each VCC rail in poly. s4 has no such contact: its poly strip turns right at y 13307.
  All five lines continue to the right in poly beyond x 15890 (areg region), where they
  turn down in a bundle at x 16240-16290.

Believed, not traced: this is the 5-bit address register. Evidence: 5 bits wide, sits
on the decode array, loaded from five lines of the bit-sliced array (which the data bus
is expected to run through), and the outputs head for the area right of the decode
array where its row drivers are. Which slice is which data bit is not established:
tags are by position, s0 leftmost.

The latch as traced is dynamic (nothing returns q to a). A static hold path is expected
and is probably the structure of AMB-1, which could not be read.

Two loads: L2's gate block (14707-14752 x 13100-13152) is one piece of poly with the
U-shaped line that runs to T_a's gate, and is tied to n2 by the buried contact at
14660-14692 x 13140-13168. L1's gate block (14797-14848 x 13058-13150) is tied to q at
14846-14874 x 13066-13100; its lower half is a contact pad from which a metal strap
goes down to the output land.

## Ports

| Name | Layer | Where it crosses | Direction | What |
|---|---|---|---|---|
| `rdp3_ar_bus_s0`..`s4` | metal | x 14235, 14625, 15015, 15405, 15795 at y 12990 (top of row AR; not yet followed upward) | into the row | data for the five latch bits |
| `rdp3_ar_ld` | metal | 16285,13060 going down (areg region) | into the row (assumed) | load strobe of row AR |
| `rdp3_ar_q_s0` | metal, then poly | contact 15884,13482; poly on to the right | out | latch output, slice s0 |
| `rdp3_ar_q_s1` | metal, then poly | contact 15839,13437 | out | slice s1 |
| `rdp3_ar_q_s2` | metal, then poly | contact 15884,13392 | out | slice s2 |
| `rdp3_ar_q_s3` | metal, then poly | contact 15839,13352 | out | slice s3 |
| `rdp3_ar_q_s4` | poly | 16170,13307 going right | out | slice s4 |
| `vcc` | metal | x 14382, 14772, 15162, 15552, 15942 at y 13520 (into the decode VCC bus) and at y 12900 upward | - | rails |
| `vss` | metal | x 14175 ... 16125 (390 apart) at y 12900 upward; 16125,13320 downward | - | rails |

## Ambiguities

- **AMB-1, hold path of the AR latch (14700-14820 x 13205-13275).** Node a's gate poly
  runs on from T_b to a buried contact on a small diffusion land under the metal track
  at x 14712 (14680-14724 x 13214-13244). From that land towards the output land
  (14820-14868 x 13197-13243) there are, under the VCC rail, three parallel stripes:
  S1 y 13208-13220, pale like diffusion; S2 y 13226-13245, salmon like poly; S3
  y 13251-13272, poly, which is the band along the cell bottom that has a contact to
  the VSS rail at (14562,13256) and ends at x 14809. Readings: (a) S2 is the gate of a
  long weak (depletion) device between the two lands, i.e. a resistive q -> a feedback
  that the bus overpowers when rdp3_ar_ld is high; (b) S1 is a plain diffusion link
  a = q; (c) S1/S2 are a capacitor on node a. In the gap between the VCC rail and the
  strap (x 14811-14820) the photo shows field beside S1 and something continuous
  beside S2. Drawn: S1 as uncertain diffusion on node a, S2 as an unconnected poly
  (`rdp3_ar_s2_sN`), no device. Working assumption: the latch is static by (a). What
  would settle it: a sharper photo of 14720-14825 x 13200-13250, or the same structure
  in an array cell where no rail covers it.
- **AMB-2, the grounded poly band S3.** Its contact to the VSS rail is clear; no use
  for it was found (nothing seen crossing it). Possibly the gate of the AMB-1 device.
- **AMB-3, the two spare tracks.** The metal at x 14712 (`rdp3_ar_trk_sN`) and at
  x 14886 run the full height of the cell and stop at its edges (y 13014 / 13277),
  over the strobe poly at the top and over poly at the bottom. No contact pad or pit
  was seen at any of those ends, and a contact from either to the strobe line would
  short all five bits, so none is drawn. The x 14886 track lies along q's drain
  diffusion (outline of a long contact at 14886,13130, drawn uncertain); the x 14712
  track may touch n2 at (14712,13172) (pale patch in the chip-2 stripped shot), not
  drawn.
- **AMB-4, end of rdp3_ar_ld.** Contact at (16285,13022) and the metal below it are
  drawn uncertain: seen at 1.5x only, and it is in the areg region.

## Not done

- Follow the five bus lines and the rails upward from y 12990 through the routing zone
  (y 12380-13000) to band B1.
- The horizontal lines at y 12700-12960 and the left-edge bundle x 13350-13760.
- Array bands B1 (y 11780-12380) and B2 (y 10950-11560): cells not traced.
