# Central datapath, rows y 8450-11200 (`cdp3`)

Region x 7600-10850, y 8450-11200. Trace: `trace/cdp3.txt`. Helpers: `tools/cdp3_prof.py`
(runs of metal-looking or poly-looking pixels along a scan line) and `tools/cdp3_px.py`
(classifies poly / diffusion / field along a scan line from colour, in the chip-2 shots
and in the clean shot; thresholds are local to this block).

## Columns and tags

Everything is tagged by the array's **column**: `cN` starts at its wide VSS rail,
x = 7605 + 390.3 N (left edge; the rail is about 45 wide), and ends at the next rail.
There is a ninth rail, "c8", at x 10720-10768, which only ends the array.

Inside a column, from the left (x for c5, add 390.3 per column):

| x (c5) | What |
|---|---|
| 9548-9592 | VSS rail ("rail d" in the first run's wording) |
| 9628-9648 | line e: the column's bit line (`cdp3_bl_cN`) |
| 9675-9692 | line f (`cdp3_f_cN`) |
| 9722-9740 | line g, only between the row A cell and channel B (`cdp3_g_cN`) |
| 9765-9815 at the top of row C and in channel B; 9725-9769 from y 9295 down through rows D-G | VCC rail ("rail a") |
| 9808-9826 | line b: west output of the row C cell (`cdp3_cw_cN`) |
| 9848-9865 | line c: read output of the row C cell (`cdp3_cq_cN`), jogging to 9812 above row E |
| 9890-9908 | line h: node N of the column (`cdp3_n_cN`) from row E down to its channel G track |

The first run numbered "slices" `s0..s7` by a 390-px window that started at the VCC rail.
Its slice sK is column cK for the VCC rail, lines b, c, h and the row E/F transistors,
but its "lines e, f, g of sK" lie right of the next VSS rail and are in column c(K+1).
All net names and tags in the trace are now column numbers; `sK` survives only in a few
comments of the trace file, with that meaning.

Which columns each row occupies:

| Row | Columns |
|---|---|
| A (large cell, cut by the top edge) | c2..c7 |
| C (register cell) | c2..c7 |
| E (pass transistor to bus N) | c0..c7 (c0, c1 pass VSS) |
| F (pass transistor to bus N) | c0..c7 |
| H (large cell) | c0..c7 |

## Status

- Traced, extracted (0 errors, no open nets) and overlay-checked:
  - row C: the register cell `cdp3_reg`, placed in c2..c7 (10 transistors each), with the
    VSS diffusion of each rail and the write line that loops through the cells;
  - rows E and F (two pass transistors per column), their two gate lines, the tracks of
    channels D and G and the vertical metal joining them;
  - channel B: six tracks onto line g, six poly links from line f to the "x 9893" line.
- NOT traced: rows A, H, I; the s0/s1 logic at x 7600-8560; the through lines at
  y 8819 and 10708; rails and lines e, f outside row C.

## Inventory

Rows (y), top to bottom:

| Row | y | What |
|---|---|---|
| A | about 8400-8790 (cut by the region's top edge) | large cell, six (c2..c7); x 7600-8300 holds other logic |
| B | 8790-9200 | channel: horizontal poly tracks and short poly links under vertical metal |
| C | 9195-9550 | register cell `cdp3_reg`, six (c2..c7); x 7780-8380 other logic |
| D | 9550-9810 | channel: six poly tracks, the west outputs of row C |
| E | 9828-10060 | one pass transistor per column, eight |
| F | 10088-10320 | one pass transistor per column, eight |
| G | 10300-10720 | channel: eight poly tracks in two pieces each |
| H | 10738-11038 | large cell, eight (c0..c7) |
| I | 11040-11200+ | next row, continues below the region |

Horizontal poly lines (y centres):

| y | Line |
|---|---|
| 8819 | through line in channel B, from about x 8420 east past x 10870. Not traced |
| 8907 ... 9123 | channel B tracks onto line g of c7 ... c2 |
| 9533 | `cdp3_c_wr`, write line of row C: runs along y 9520-9546 and in every cell loops up (x 9581-9603 in c5), east along y 9476-9498 over the write transistor, and down again (x 9697-9719). West of c2 and east of c7 it runs straight on (seen to x 8355 and x 10900). The first run listed its two levels as separate lines "9493" and "9537" |
| 9581, 9624, 9668, 9711, 9754, 9797 | channel D tracks of c7 ... c2: from the west edge to the tap contact under line b |
| 10057, 10317 | gate lines of rows E and F |
| 10361 ... 10664 | channel G tracks of c7 ... c0, each in a west piece (to the row H cell) and an east piece (node N, to the east edge) |
| 10708 | another line, present from about x 8200 east. Not traced |

## Logic

### Row C: `cdp3_reg`, a static register bit with two output buffers (traced)

Master in column c5, x 9545-9950, y 9195-9550; instances at dx -1171, -781, -390, 390,
781. Ten transistors (positions for c5):

| | Gate | Between | W/L | Where |
|---|---|---|---|---|
| write | `cdp3_c_wr` | bit line `cdp3_bl` and `x` | 72/22 | diffusion 9620-9692, write line across it at y 9476-9498; bit-line contact below at 9637,9527 |
| pull-down 1 | `x` | VSS and `q1` | 62/25 | x poly 9609-9634 over 9590-9657 x 9350-9412 |
| load 1 | `q1` | VCC and `q1` | 24/54 | strip y 9388-9412 under block C (9670-9724) |
| pull-down 2 | `q1` | `q` and next VSS | 50/19 | column 9914-9933, y 9216-9266 |
| load 2 | `q` | VCC and `q` | 33/54 | strip y 9229-9259 under block 9787-9845 |
| hold | **VSS** | `q` and `x` | 22/94 | L-shaped strip under the grounded block B (9664-9716 x 9241-9320) |
| pull-down W | `q1` | `cw` and next VSS | 79/19 | column, y 9308-9387 |
| load W | `cw` | VCC and `cw` | 26/16 | strip y 9378-9404 under poly 9782-9798 |
| pull-down R | `q1` | `cq` and next VSS | 79/19 | column, y 9415-9494 |
| load R | `cq` | VCC and `cq` | 26/16 | strip y 9448-9474 under poly 9782-9798 |

    x  = bl while cdp3_c_wr is high; otherwise held from q through the hold device
    q1 = NOT x        q = NOT q1 (= x)
    cw = NOT q1       west output, line b -> channel D track -> west edge
    cq = NOT q1       read output, line c -> row E pass transistor -> bus N

So the cell stores the bit line's value in true form and gives it out twice through
separate strong inverters (loads 26/16 against 24/54 and 33/54 inside the latch). The
hold device has its gate on VSS through a poly that does nothing else (pad under a bulge
of the VSS rail, contact at 9592,9218): as in `cdp1_reg` and `cdp2_lat`, only a depletion
device makes sense there. *Believed, not visible.*

The cell is the same circuit as cdp1's `cdp1_reg` (x, q1, q, grounded-gate hold, write
pass from a bit line 62 px right of the VSS rail centre) with the two output buffers
added; the layout is different (findcell with cdp1's master finds nothing here), and it
was traced from this block's photos only.

How the nodes are made, for checking:
- `x`: vertical poly 9609-9634 x 9292-9453. Its top lies on the west end of the hold strip
  (buried contact, drawn `?B`, see Ambiguities); its foot on a small box of diffusion
  (buried contact 9614-9644 x 9430-9458) that is the top-left corner of the write
  transistor's diffusion.
- `q1`: diffusion right of the x gate (9634-9657); an arm at y 9350-9367 to the tie box
  9666-9694 x 9348-9369; the poly over the tie widens east (to x 9752, y 9346-9371), has
  a strip down through block C (the load gate), and climbs in a Z under the VCC rail to
  "band U" (y 9285-9303, then 9275-9300) and the "column" 9914-9933 x 9202-9498 at the
  cell's right edge, where it gates the three pull-downs onto the next column's VSS
  diffusion.
- `q`: diffusion 9843-9908 x 9228-9262, tie box 9850-9892 x 9198-9226 to the load block,
  and the poly band along the top of the cell (y 9199-9222) west to a buried contact
  9676-9706 x 9197-9221 on the top of the hold strip. That band is what the first run
  took for a chain along the row: it stays inside one column cell (field at x 9664-9674).
- `cw`: diffusion "R1" 9862-9912 x 9322-9388 and the lobe west of it round the tie box
  9828-9856 x 9370-9396; the poly on the tie is the foot of the pad that line b lands on
  (contact 9817,9343), and the same poly's strip 9782-9798 x 9350-9414 is the load gate.
- `cq`: diffusion "R2" 9862-9912 x 9442-9495 with the contact of line c (9882,9470), and
  its extension west to the load; tie box 9828-9856 x 9453-9478 to the poly band
  9775-9856 x 9480-9498, whose strip 9782-9798 x 9432-9485 is the load gate. The two
  strips at x 9782-9798 are separate pieces: field at y 9418-9430 (measured).
- The pull-downs through the column are at y 9216-9266, 9308-9387, 9415-9494 (dark bars
  across the column at 9214, 9268, 9304, 9388, 9412, 9496); between them is field.

Instances: c3..c7 match the master (cellcheck 3-5 % of blocks, the differing ones in
channel D below). c2 differs only at its VSS rail: no cell to its left, so the diffusion
under the rail is one box (8386-8440 x 9350-9412, one contact) feeding pull-down 1.

*Believed:* a 6-bit register written from the data bus through the bit lines, readable
on bus N, whose outputs go west. R12 (display start, high) and R14 (cursor, high) are
the 6-bit readable registers of this chip type; which one this is depends on where the
`cdp3_cw` lines go west of x 7600, and on which select line drives `cdp3_c_wr`.

### Rows E and F (traced)

    row E, c2..c7:  pass transistor, gate cdp3_gate_e, between cdp3_cq_cN and cdp3_n_cN
    row E, c0, c1:  pass transistor, gate cdp3_gate_e, between VSS and cdp3_n_cN
    row F, c0..c7:  pass transistor, gate cdp3_gate_f, between cdp3_hq_cN (row H cell) and cdp3_n_cN

All sixteen are W/L about 190/28. `cdp3_n_cN` leaves east on its channel G track. So N is
an eight-line bus that gets the six row C bits (and 0 on c0, c1) when `cdp3_gate_e` is
high and the eight row H values when `cdp3_gate_f` is high: a read bus, with the two
unused top bits of the 6-bit register reading 0. That makes c0, c1 the two most
significant bits if the order is monotonic (not established).

### Channel B (traced, wiring only)

- Six poly tracks from the west edge (y 8907 ... 9123) each end at a contact on line g of
  one column (c7 ... c2). Line g comes down from the row A cell and **ends at that
  contact** (checked in all six: no metal below it; the first run had drawn it down to
  y 9200). So each row A cell gets one line from the west.
- Six poly links join line f of a column (contact at x 9681 in c5) to the "x 9893" line of
  the same column, which comes down from the row A cell and ends at the link (links at
  y 8862 for c2, c3, c5, c6 and at y 9144 for c4, c7). Line f then runs down through the
  row C cell without a contact and on to the bottom edge.

## Ports

West edge, x 7600 (all poly, all continue west beyond x 7540):

| Name | y | Direction | What |
|---|---|---|---|
| cdp3_g_c7 .. cdp3_g_c2 | 8907, 8950, 8994, 9037, 9080, 9123 | ? | one line into each row A cell |
| (not traced) | 8864, 9167 | ? | lines into the logic at x 7600-8560 |
| cdp3_c_wr | 9533 | in | write line of row C (seen at x 8355; not yet followed to x 7600) |
| cdp3_cw_c7 .. cdp3_cw_c2 | 9581, 9624, 9668, 9711, 9754, 9797 | out | row C register outputs (true), each from a 26/16 load |
| cdp3_gate_e | 10057 | in | read row C onto N |
| cdp3_gate_f | 10317 | in | read row H onto N |
| cdp3_hw_c7 .. cdp3_hw_c0 | 10361, 10404, 10447, 10490, 10535, 10577, 10621, 10664 | ? | per-column line of the row H cells |

East edge, x 10850 (poly):

| Name | y | What |
|---|---|---|
| cdp3_n_c7 .. cdp3_n_c0 | 10361, 10404, 10447, 10490, 10535, 10577, 10621, 10664 | bus N. c7's track ends at a metal contact at about 10855,10355 and c6's at about 10900,10400, each on a vertical metal line that comes down from the north with a diagonal jog at y 10250-10330 (seen at 0.85x); the other six run on east at least to x 10960 |
| cdp3_c_wr | 9533 | write line of row C, runs on east (seen to x 10900) under three thin vertical metal lines at x 10803, 10848, 10888 |
| (not traced) | 8819 | through line of channel B |

Top edge (y 8450) and bottom edge (y 11200), per column (x for c5):

| Line | x | What |
|---|---|---|
| VSS rail | 9548-9596 | contacts at 9568,8437 and 9568,8500 (row A), 9570,11200 |
| cdp3_bl_cN | 9628-9648 | bit line: drawn only in row C so far |
| cdp3_f_cN | 9675-9692 | from the row A cell (via the link in channel B); drawn y 8790-9560 |
| VCC rail | 9765-9815 at the top, 9770-9815 at the bottom | |

Into rows not yet traced (the labels sit on the stubs):

| Name | Layer | Where | To |
|---|---|---|---|
| cdp3_hq_cN (N 0..7) | metal | x 9466 + 390 (N-4), y 10720 | row H cell |
| cdp3_hw_cN (N 0..7) | metal | x 9422 + 390 (N-4), y 10720 | row H cell |
| cdp3_g_cN (N 2..7) | metal | x 9731 + 390 (N-5), y 8790 | row A cell |
| x 9893 line (same net as cdp3_f_cN) | metal | x 9893 + 390 (N-5), y 8790 | row A cell |

## Ambiguities

- **Top of the x poly** (9607-9637 x 9291-9319 in c5, drawn `?B`). The hold strip comes
  out of block B's left edge as a pale strip (9622-9664 x 9296-9314) and ends under the
  top of the x poly, where the clean shot shows only a dark blob in the gap between the
  VSS rail and line e. Read as a buried contact (strip to x), as in `cdp1_reg`. The
  alternative, the strip passing under the poly as a transistor, leads nowhere: nothing
  is west of the poly but the VSS rail's field.
- **Joint between the west buffer's tie and R1** (9855-9868 x 9374-9390, drawn `?D`). The
  tie box's right outline and R1's left outline merge into one dark line there in both
  stripped shots. Without the joint R1 would be a pull-down with nothing on it and the
  load would have no pull-down. The read buffer below, same layout, shows its joint
  plainly (continuous tan at y 9453-9462).
- **Line f over block B.** In the metal shots line f looks slightly wider at 9673-9691 x
  9287-9312 (between the two edges of the strip under it), in all six cells. Read as no
  contact: the line is no wider than elsewhere, and the clean shot shows unbroken poly
  below. A contact there would put line f on the grounded poly.
- Rail identity. The rails are labelled from structure (loads hang from "rail a", pull-
  downs end on "rail d") and from their x matching the VSS / VCC rails that `cdp1`
  followed to the VSS pad plane at y 4530. Not followed through cdp2 here.
- The gate lines' east ends were seen at 0.85x only (row E's poly visible to about
  x 10690; row F's not visible east of c7's gate).
- Neighbours: `cdp4` (below) tags the column whose VSS rail is at x 8405 as its s2, so its
  sK is column c(K) here; `cdp2` (above) uses the same numbering as cdp4.

## Not done

- Row A cell (c2..c7, y about 8400-8790, cut by the top edge) and row H cell (c0..c7,
  y 10738-11038): believed variants of `cdp3_reg`; not traced.
- Row I (y 11040-11200+).
- The logic at x 7600-8560 beside rows A-C; channel B lines at y 8864 and 9167 (contacts
  near x 7834 and 8290).
- Through lines y 8819 and 10708; `cdp3_c_wr` west of x 8355 and east of x 10900.
- Rails and lines e, f over their full length (drawn only in row C and channel B).

## Tools and method notes

- The clean shot here: poly salmon under metal and dark red textured in the open;
  diffusion flat tan under metal and mauve-pink in the open; field pink under metal and
  khaki in the open. In a gap between two metal lines only a strip a few px wide is
  "open", so poly shows there as a dark red bar and field as a green one with a dark
  centre (the "rings" at 9660,9333 and 9705,9333 are field).
- The median composite over the six cells (`composite.py`, name `cdp3_col`, frame of
  column c5) at 4x in the clean shot was the most useful single view. Above 4x nothing
  more is resolved.
- `tools/cdp3_px.py` (colour classes along a scan line) settled several things a view did
  not: that the strips at x 9782-9798 are two pieces, where the pull-downs cross the
  column, that the stair between R1 and R2 is field. Letters next to an edge are noise.
- `tools/cdp3_prof.py --mode metal` needs `--thr 150`; with a lower threshold plain field
  counts as metal.
