# Central datapath, rows y 8450-11200 (`cdp3`)

Region x 7600-10850, y 8450-11200. Trace: `trace/cdp3.txt`. Helper: `tools/cdp3_prof.py`
(runs of metal-looking or poly-looking pixels along a scan line; good for positions of
lines, not reliable for continuity).

## Status

- Traced, extracted (0 errors, no open nets) and overlay-checked in all eight slices:
  rows E and F (two pass transistors per slice), their two gate lines, the eight
  per-slice tracks of channel G, the six per-slice tracks of channel D, and the vertical
  metal that joins them (lines b, c, h and the two lines into each row H cell).
- Traced the same way: channel B's six tracks onto line g and its six poly links from
  line f to the next slice (wiring only; contacts checked at 2x in the clean shot, lines
  by overlay at 0.8x).
- NOT traced: the three rows of large cells (A, C, H), the row at the bottom edge, the
  through lines at y 8819, 9493, 9537 and 10708, the rails (only two short pieces are
  drawn), lines e, f, g outside channel B, the s0/s1 logic at x 7600-8560.
- Surveyed with coordinates but not traced: the row C cell (own section below).

## Inventory

Slices: eight, `s0` (left) to `s7`, pitch 390.3. Slice k = master (s4, x 9340-9730) moved
by dx = -1561, -1171, -781, -390, 0, 390, 781, 1171 (findcell offsets, used everywhere).
Tags are positions; the bit order is not established (see Logic for a hint).

Rows (y), top to bottom:

| Row | y | What | Slices |
|---|---|---|---|
| A | about 8400-8790 (cut by the region's top edge; contacts on rail d at y 8437 and 8500) | large cell, a variant of the row C cell (findcell 0.36 against C, offset 0,-716) | 6: s2..s7; s0, s1 hold other logic (x 7600-8300, not looked at) |
| B | 8790-9200 | channel: horizontal poly tracks and short poly links under vertical metal; see "Channel B" |  |
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
| rail a | 9335-9379 in rows D-G; 9375-9425 in channel B, at the top of the row C cell and at both region edges (y 8450, y 11200) | believed VCC (in the row C cell it has a contact at 9357,9252 feeding a load: strip under a poly block with a buried-contact tie). In s0 only a thin line is at this position in rows D-E: not understood |
| b | 9424 | from a contact in the row C cell (9427,9338) down to the slice's tap on its channel D track |
| c | 9466 | from the row C cell down, diagonal jog, to the left contact of the row E transistor |
| h | 9509 | row E right contact, row F right contact, then down to the slice's contact on its channel G track (east piece). This is node N of the slice |
| rail d | 9552-9597 | believed VSS (in the row C cell it lies on a wide diffusion with three contacts, 9560,9330 / 9570,9380 / 9558,9435, bounded by gate strips) |
| e, f, g | 9639, 9684, 9732 | three lines that pass through rows D-G without contact (s4, 1.6x) and are present at both region edges. f and g have contacts in channel B (below). Not traced |
| (x 9500) | 9490-9510 | comes down from the row A cell and ends at a contact in channel B (s4: 9500,9140) |
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

Top edge (y 8450) and bottom edge (y 11200), per slice (master s4 x, add dx). Seen in
the metal shot at 1.6x for s4 and s5 at both edges; the other slices only at 0.4x. The
top edge cuts through the row A cells, the bottom edge through row I.

| Line | x at y 8450 | x at y 11200 | What |
|---|---|---|---|
| rail a | 9375-9420 | 9380-9425 | believed VCC |
| rail d | 9548-9596 (contacts at 9568,8437 and 9568,8500) | 9550-9598 (contact at 9570,11200) | believed VSS |
| e | 9625-9645 | 9630-9645 | not identified |
| f | 9665-9690 | 9670-9690 | `cdp3_f_sK` in s1..s6: tied to the row A cell of the next slice in channel B |
| g | 9715-9740 | 9715-9740 | `cdp3_g_sK` in s1..s6: fed from the west by a channel B track |

West edge, channel B (poly, x 7600):

| Name | y | What |
|---|---|---|
| cdp3_g_s6 .. cdp3_g_s1 | 8907, 8950, 8994, 9037, 9080, 9123 | per-cell vertical line g of the 6-bit rows (direction unknown) |
| (not traced) | 8864, 9167 | lines into the s0/s1 logic |

East edge, channel B: the y 8819 through line (not traced).

Stubs inside the region (channel B, labels on the metal): `cdp3_f_sK` (K 1..6) at
x 9684+dx, y 8790 and y 9200; line g at x 9731+dx, y 8790 and y 9200; the x 9500 line of
s2..s7 (same net as `cdp3_f` of the slice to the west) at x 9503+dx, y 8790.

## Ambiguities

- Rail identity. Rail d is labelled `vss` in the trace. Evidence: (1) in the row C cell
  it lies on a wide diffusion with three contacts and the load at the cell's top left
  hangs from rail a; (2) rail d of s1..s7 (x 8403, 8793, 9184, 9574, 9964, 10355, 10745)
  is at the x of the VSS rails that `cdp1` followed to the plane under the VSS pad (8403,
  8796, 9187, 9577, 9967, 10357, 10738 at y 4530), and rail a at the top of row C
  (x 9400+dx) at the x of cdp1's VCC rails (8620 ... 10570). The stretch between y 4530
  and y 8450 belongs to cdp2 and was not looked at here, so continuity is assumed. If
  rail d were VCC the row E transistors of s0 and s1 would pull N high instead of low.
- Slice numbering against the neighbours (from their notes, not traced): `cdp4`'s slice
  K has its rails at this block's slice K-1 (cdp4 s2 rails 8405 / 8619 = rail d of s1 and
  rail a of s2 here), and the vertical metal its channel-1 bus lines end on (x 8555 in
  its s2) is this block's line g (8561 in s1). So line g probably runs from channel B down
  through rows C-H into cdp4's row R1 and is fed from the west there too.
- The gate lines' east ends were seen at 0.85x only (row E's poly visible to about
  x 10690; row F's not visible east of s7's gate).
- In the clean shot the row E and F transistors show khaki areas with a dark outline
  beside the body (x 9395-9432 and 9505-9537, below the pads). Read as open field: the
  chip-2 metal shot shows the body outline at x 9433-9500 only.

## Channel B (y 8790-9200): tracks and links traced

From a 1.6x view of s4 (both shots), a 0.8x metal view of the full width, a 2x mosaic of
all eighteen contacts in the clean shot, and the overlay.

Traced:
- Six poly tracks from the west edge, y 8907, 8950, 8994, 9037, 9080, 9123. Each ends at
  a contact on line g of one slice (x 9729+dx): s6, s5, s4, s3, s2, s1 in that order. East
  of its contact the track is gone. Nets `cdp3_g_s1`..`cdp3_g_s6`.
  Line g of slice k lies on the boundary with slice k+1 (x 9732 = the left edge of the
  next cell), so these six lines sit at the left edge of the six cells s2..s7 of rows A
  and C: a 6-bit bus from the west onto a vertical line per cell.
- Six poly links, a metal contact at each end, joining line f of slice k (contact at
  x 9681+dx) to the x 9500 line of slice k+1 (contact at x 9507+dx'), which comes down
  from the row A cell and ends there. Links at y 8862 for s1-s2, s2-s3, s4-s5, s5-s6 and
  at y 9144 for s3-s4, s6-s7. Nets `cdp3_f_s1`..`cdp3_f_s6`. So each row A cell (s2..s7)
  is tied to line f of the slice to its west; line f also has contacts inside the row
  C cell (not traced).
- Lines f, g and the x 9500 lines are drawn across the channel only (y 8790-9200).

Seen, not traced:
- y 8819: through line, from about x 8420 east past x 10870.
- No track was seen for s7's line g (x 10903, outside the region) or for s0's.
- A poly line at y 9167 from the west edge to a contact at about (8290,9169), with a
  contact at about (7834,9169) on the way, and a poly at y 8864 from the west edge to a
  contact at about (7834,8861) on the same vertical metal: s0/s1 logic, not understood.
- In the clean shot the channel also shows plain rectangles (9435-9490 x 8830-8880 and
  x 9000-9110 in s4). They are open field between the metal lines, not devices.

## Row C cell: what is established so far (not traced)

Master s4, x 9340-9730, y 9200-9500. Read from 3x and 4x views of the median composite
`cdp3_c` (cache/comp; six instances) in `metal`, `acid` and `acid1b`. None of this is in
the trace file. Colours of the clean shot here: poly salmon under metal and orange-red
textured in the open; diffusion flat tan under metal and flat pink with a dark outline
in the open; field khaki in the open, pink under metal; narrow open gaps bright green.

Metal:
- Rail a enters at the top at x 9375-9425, is x 9335-9425 wide over y 9230-9265 (contact
  to diffusion at 9357,9252), then runs down the left edge at x 9335-9375 (second,
  elongated contact at 9350,9475 on a diffusion 9333-9375 x 9375-9510).
- Line b: its top end is a contact at 9427,9343 on a POLY pad (9405-9450 x 9327-9365,
  green-speckled paler patch, no dark specks). So the per-slice west line `cdp3_cw_sK`
  is on poly here: a gate input, or an output that arrives in poly.
- Line c: a contact to DIFFUSION at 9490,9470 (tan region 9477-9520 x 9452-9495, dark
  specks). Line c itself is at x 9458-9475 below y 9500; how the contact pad joins it
  was not examined.
- Rail d x 9552-9592 over a wide diffusion (9547-9595 x 9210-9500, wider in places) with
  contacts at 9565,9327 / 9575,9380 / 9562,9437. At the top right the rail has a bulge
  with a contact at 9592,9220 that lands on POLY (salmon pad 9582-9657 x 9201-9240).
- Lines e (9627-9647), f (9675-9692), g (9725-9745) run through; f shows contact-like
  blobs (9684,9213 and lower). Not examined.

Poly and diffusion, left half:
- Load at the top left: VCC contact box 9340-9395 x 9229-9275; diffusion strip y 9229-9259
  east under a poly block 9399-9455 x 9200-9269; output diffusion 9459-9515 x 9234-9255;
  buried-contact box 9475-9498 x 9200-9223 at the top right of the block.
- The load's poly continues WEST along y 9201-9222 out of the cell (seen to x 9325), and
  at the cell's top right a heavy-outlined box (9680-9712 x 9197-9230) sends a poly line
  east at y 9204-9214 into the next slice. So there is a chain along the top of the row:
  a node per slice boundary, loaded in the slice to the east. This is what a comparator's
  combining line or a carry chain would look like; which, and its direction, is open.
- Band U: poly from the cell's left edge (stair, about y 9340-9370 at x 9325) up to
  y 9292-9302 over x 9390-9475, then y 9280-9297 east to the column.
- Column: vertical poly x 9525-9545 over the whole cell height (y 9202-9502) between the
  left half and the wide diffusion under rail d. Band U joins it (same poly; band U ends
  just east of it at x 9553), so column = band U = a signal from the slice to the west.
  A 4.4x view in `acid` and `metal1` (x 9462-9572) shows dark bars across the column at
  y 9264-9270, 9301-9305, 9387-9391, 9408-9413 and 9489-9496, lining up with the top and
  bottom edges of the regions to its left, and field (greenish in `acid`, khaki in the
  clean shot) in the stair-shaped gap y 9391-9408 between them. Read: the column is a
  gate, and the diffusions 9477-9518 x 9305-9387 ("R1") and 9462-9518 x 9413-9495 (the
  line c contact region) each pass under it to the rail d diffusion, i.e. two pull-downs
  gated by band U, one of them on the line c node. The same may hold for the load output
  9459-9515 x 9234-9264. Believed from one view; not yet overlaid or extracted.
- Vertical poly strips at x 9391-9407 (y 9352-9400 and y 9442-9500) crossing strips that
  run east from the diffusion under rail a: probably two more loads or pull-ups, one of
  them into the line c node.
- Horizontal poly along the bottom of the row at y 9483-9503 (the "9493 line").

Right half (x 9600-9740): dense, with a vertical poly strip at x 9612-9622 (y 9290-9500)
beside the rail d diffusion and several horizontal diffusion fingers. Not decoded.

Working guess (not traced): a static register bit with a comparator bit against the
per-slice west line and a read path to bus N, i.e. row C = a 6-bit readable register
with an equality comparator (the cursor register R14 against MA8-13 would fit, and row
H = R15 against MA0-7).

## Not done

- Row C cell (9340-9730 x 9200-9500 in s4): see the section above for what is known. It
  needs 4-5x views junction by junction; start with the column question, then the right
  half. Budget about twenty views. A contact at about 9630,9525 sits just below the cell.
- Channel B: the y 8819 through line and the s0/s1 lines (y 8864, 9167; contacts near
  x 7834 and 8290).
- Row A and row H cells (variants of C), row I, the s0/s1 logic of rows A-C
  (x 7600-8560), the through lines (y 8819, 9493, 9537, 10708), rails over their full
  length, lines e, f, g.

## Tools and method notes

- `tools/cdp3_prof.py`: positions of metal lines (`--mode metal`) and of horizontal poly
  lines (`--mode poly`, chip-2 stripped shot). The poly mode fails under metal ghosts and
  the metal mode breaks lines at every edge underneath, so use it for coordinates, never
  for continuity.
- `composite.py` over the six row C instances gives a much cleaner picture than any single
  instance; views above 4x add nothing.
- In this part of the die the bright green bands of the clean shot are narrow strips of
  open field between features (or between metal lines), not features.
