# Central datapath, rows y 8450-11200 (`cdp3`)

Region x 7600-10850, y 8450-11200. Trace: `trace/cdp3.txt`. Helper: `tools/cdp3_prof.py`
(runs of metal-looking or poly-looking pixels along a scan line; good for positions of
lines, not reliable for continuity).

## Status

- Traced, extracted (0 errors, no open nets) and overlay-checked in all eight slices:
  rows E and F (two pass transistors per slice), their two gate lines, the eight
  per-slice tracks of channel G, the six per-slice tracks of channel D, and the vertical
  metal that joins them (lines b, c, h and the two lines into each row H cell).
- NOT traced: the three rows of large cells (A, C, H), channel B, the row at the bottom
  edge, the through lines at y 9493, 9537 and 10708, the rails (only two short pieces
  are drawn), the three per-slice vertical lines e, f, g.

## Inventory

Slices: eight, `s0` (left) to `s7`, pitch 390.3. Slice k = master (s4, x 9340-9730) moved
by dx = -1561, -1171, -781, -390, 0, 390, 781, 1171 (findcell offsets, used everywhere).
Tags are positions; the bit order is not established (see Logic for a hint).

Rows (y), top to bottom:

| Row | y | What | Slices |
|---|---|---|---|
| A | 8484-8784 (starts above 8450?) | large cell, a variant of the row C cell (findcell 0.36 against C, offset 0,-716) | 6: s2..s7; s0, s1 hold other logic (x 7600-8300, not looked at) |
| B | 8790-9200 | channel: horizontal poly lines (about y 8800, 8895-8985, 9110-9150) under vertical metal, and large plain rectangles (9450-9510 x 8800-8870, x 9000-9080). Not looked at closely |  |
| C | 9200-9500 | large cell | 6: s2..s7 (findcell 0.88-0.92). s1 position holds something else (score 0.41); x 7780-8300 other logic |
| D | 9500-9810 | channel: horizontal poly tracks under vertical metal | |
| E | 9828-10060 | one pass transistor per slice | 8 (s0, s1, s2 differ in detail) |
| F | 10088-10320 | one pass transistor per slice | 8, identical |
| G | 10300-10720 | channel: horizontal poly tracks under vertical metal | |
| H | 10738-11038 | large cell, another variant of the row C cell (findcell 0.40, offset 0,1538) | 8: s0..s7 |
| I | 11040-11200+ | next row, continues below the region; not looked at | |

Vertical metal in one slice (master s4, x centres; widths 18 unless stated). Seen
continuous through channels D-G in every slice at 0.8x, in s4 at 1.6x:

| Line | x | What |
|---|---|---|
| rail a | 9335-9379 | believed VCC (in the row C cell it has one small contact at 9357,9250 feeding a load-like strip under a poly block). In s0 only a thin line is at this position in rows D-E: not understood |
| b | 9424 | from a contact in the row C cell (9427,9338) down to the slice's tap on its channel D track |
| c | 9466 | from the row C cell down, diagonal jog, to the left contact of the row E transistor |
| h | 9509 | row E right contact, row F right contact, then down to the slice's contact on its channel G track (east piece). This is node N of the slice |
| rail d | 9552-9597 | believed VSS (in the row C cell it lies on a wide diffusion with three contacts, 9560,9330 / 9570,9380 / 9558,9435, bounded by gate strips) |
| e, f, g | 9639, 9684, 9732 | three lines that pass through rows D-G without contact (s4, 1.6x). Not followed |
| (row F left) | 9422 then 9466 | row F left contact down, diagonal jog just above the slice's track, into the row H cell at x 9466 |
| (west piece) | 9422 | from the slice's west contact on its channel G track down into the row H cell |

Horizontal poly lines (y centres measured in the chip-2 stripped shot):

| y | Line |
|---|---|
| 9493 | runs along the bottom of the row C cells (wide). Not traced |
| 9537 | through line, seen from x 7780 to beyond x 10850. Not traced |
| 9581, 9624, 9668, 9711, 9754, 9797 | channel D tracks of s7, s6, s5, s4, s3, s2: each from the west edge to its slice's tap contact at x 9421+dx, where it ends |
| 10057 | gate line of row E, from the west edge to s7 (ends about x 10690) |
| 10317 | gate line of row F, from the west edge to s7 |
| 10361, 10404, 10447, 10490, 10535, 10577, 10621, 10664 | channel G tracks of s7 ... s0. Each track is two pieces: west edge to a contact at x 9421+dx; a contact at x 9509+dx to the east edge. The gap between the two contacts was checked in all eight slices |
| 10708 | another line, present from about x 8200 east; absent at the west edge. Not traced |

## Logic

Traced (extracted):

    row E, s2..s7:  pass transistor, gate cdp3_gate_e, between cdp3_cq_sK (line c, from the row C cell) and cdp3_n_sK
    row E, s0, s1:  pass transistor, gate cdp3_gate_e, between rail d (vss) and cdp3_n_sK
    row F, s0..s7:  pass transistor, gate cdp3_gate_f, between cdp3_hq_sK (to the row H cell) and cdp3_n_sK

All sixteen are W/L about 190/28. `cdp3_n_sK` (line h) has no other connection inside
the traced part: it leaves east on its channel G track. So N is an eight-line bus that is
joined to the row C cells (six lines, plus rail d on two) when `cdp3_gate_e` is high and
to the row H cells when `cdp3_gate_f` is high.

Each row C cell (s2..s7) also has a line of its own from the west edge (`cdp3_cw_sK`,
channel D track, line b, contact at 9427,9338 in the cell); each row H cell (s0..s7)
likewise (`cdp3_hw_sK`, channel G track west piece). Directions are not known until the
cells are traced.

Believed, not traced: N is a read bus. Row C is a 6-bit register and row H an 8-bit
one, read onto N by `cdp3_gate_e` and `cdp3_gate_f`; the two slices with no row C cell put
rail d (0 if it is VSS) on the bus, as the unused top bits of a 6-bit readable register
would. That would make s0, s1 the two most significant bits (or s0 = bit 7 with the
order reversed; nothing fixes the order within s2..s7 yet). The per-slice west lines
would then be the data inputs of the two registers (for the light pen register they
would be memory address bits, which do come from the west). The only readable
registers in the datasheet are R14/R15 (cursor) and R16/R17 (light pen). All of this is
inference from the wiring pattern.

## Ports

West edge, x 7600 (all poly, all continue west beyond x 7540):

| Name | y | Direction | What |
|---|---|---|---|
| cdp3_cw_s7 .. cdp3_cw_s2 | 9581, 9624, 9668, 9711, 9754, 9797 | ? | per-slice line of the row C cells |
| (not traced) | 9537 | ? | through line of channel D |
| cdp3_gate_e | 10057 | in | gate line of row E |
| cdp3_gate_f | 10317 | in | gate line of row F |
| cdp3_hw_s7 .. cdp3_hw_s0 | 10361, 10404, 10447, 10490, 10535, 10577, 10621, 10664 | ? | per-slice line of the row H cells |

East edge, x 10850 (poly):

| Name | y | What |
|---|---|---|
| cdp3_n_s7 .. cdp3_n_s0 | 10361, 10404, 10447, 10490, 10535, 10577, 10621, 10664 | bus N. s7's track ends at a metal contact at about 10855,10355 and s6's at about 10900,10400, each on a vertical metal line that comes down from the north with a diagonal jog at y 10250-10330 (seen at 0.85x); the other six run on east at least to x 10960, presumably to the next contacts of the same staircase |
| (not traced) | 9537 | through line of channel D; a contact is visible at about 10925,9520 |

Into rows not yet traced (inside the region; the labels sit on the stubs):

| Name | Layer | Where | To |
|---|---|---|---|
| cdp3_cq_sK (K 2..7) | metal | x 9466+dx, y 9500 | row C cell, line c |
| cdp3_cw_sK (K 2..7) | metal | x 9423+dx, y 9500 | row C cell, line b (contact at 9427+dx, 9338) |
| cdp3_hq_sK (K 0..7) | metal | x 9466+dx, y 10720 | row H cell |
| cdp3_hw_sK (K 0..7) | metal | x 9422+dx, y 10720 | row H cell |

Top (y 8450) and bottom (y 11200) edges: not yet recorded (rails a, d and lines e, f, g
of every slice cross both; exact x in the table above plus dx, to be confirmed there).

## Ambiguities

- Rail identity. Rail d is labelled `vss` in the trace on the strength of the row C cell
  structure (wide diffusion with three contacts under it); rail a is believed VCC.
  Neither was followed to a pad, and the row C cell is not traced yet. If rail d turns
  out to be VCC the row E transistors of s0 and s1 pull N high instead of low.
- The gate lines' east ends were seen at 0.85x only (row E's poly visible to about
  x 10690; row F's not visible east of s7's gate).
- In the clean shot the row E and F transistors show khaki areas with a dark outline
  beside the body (x 9395-9432 and 9505-9537, below the pads). Read as open field: the
  chip-2 metal shot shows the body outline at x 9433-9500 only.

## Not done

- Row C cell (9340-9730 x 9200-9500 in s4; composite `cdp3_c` exists in cache/comp). First
  observations: top-left load (VCC contact 9357,9250; poly block 9395-9455 x 9225-9265;
  small box at 9478-9497 x 9200-9222, probably the load's buried contact); line b's
  contact at 9427,9338; a contact at 9490,9470; wide poly areas at 9455-9530 x 9310-9400;
  rail d over the wide diffusion 9545-9615 x 9200-9480; vertical poly strip at
  x 9600-9612 beside it; a contact at about 9630,9525 below the cell.
- Row A and row H cells (variants of C), row I, channel B, s0/s1 logic of rows A-C
  (x 7600-8560), the through lines, rails over their full length, lines e, f, g, and the
  top/bottom port tables.
