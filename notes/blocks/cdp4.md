# cdp4: central datapath, bottom part (x 7600-10850, y 11200-14000)

## Status

Traced and shipped (extracts clean, 96 transistors): channel 1 bus lines, rows A and B
(4-way pass-transistor selector per slice), row C (reset transistor on the selector
node, then an 8-bit latch row with a buffered output back into the selector), supply
rails for y 11790-13300.
Not traced: row R1 (y 11100-11800), channel 2 (y 13280-13620), row D (y 13640-14050,
six cells), the wiring right of x 10600. Found but not placed: row D and the lower half
of R1 are built from a latch cell of the same family (see Not done).

## Conventions

- Eight slices, pitch 390.3. Master slice for all cells is **s2** (third from the left).
  Offsets from findcell: s0 -782, s1 -391, s2 0, s3 391, s4 781, s5 1170, s6 1560, s7 1951.
- Slices are tagged by position (s0 leftmost). Bit order not established.
- Each slice has two wide vertical metal rails: x 8385-8425 and x 8597-8641 in s2
  (which is VSS and which VCC: not yet established; they pass rows A/B without contacts).
- In this part of the die the clean shot shows poly over field as salmon even in the
  open, and poly over a channel (thin oxide) in the open as dark red-brown. The long
  horizontal lines are poly (orange in `metal` and `acid`, metal lines cross over them).

## Inventory (rows, top to bottom)

| y | What | Slices | State |
|---|---|---|---|
| ~11100-11800 | row R1: tall complex cell (maybe 30 transistors), two rails per slice | 8 | not traced |
| 11820-11845 | one more horizontal poly line (y 11832), runs under all slices | - | not traced |
| 11860-12190 | channel 1: eight horizontal poly bus lines, 43.3 px apart, entering from the left edge; line of slice k ends at a contact on a vertical metal (x 8555 in s2) that goes up into R1 | 8 | traced |
| 12200-12470 | row A: two pass transistors onto node n | 8 | traced |
| 12470-12545 | two select poly lines (sel2, sel3) | - | traced |
| 12545-12800 | row B: two pass transistors onto node n (near mirror of row A) | 8 | traced |
| 12800-13270 | row C: complex cell | 8 | not traced |
| 13280-13620 | channel 2: about ten horizontal poly lines with stair-step contacts in pairs | 8 | not traced |
| 13640-14050 | row D: complex cell, only six copies, x 8000-10330 | 6 | not traced |
| 14050-14700 | fan-out wiring from row D down into the random logic (outside the region) | - | not traced |

## Logic

### Rows A and B: 4-way selector (traced)

Per slice, four pass transistors (W about 195, L 23-28) share one node `cdp4_n_sK`
(metal x 8548-8564 in s2, contacts at y 12352 and 12653, continues down into row C):

```
n <-> a   when sel1     a: metal from row R1 (x 8509 at y 11800, jogs to x 8467 at y 12178)
n <-> b   when sel2     b: metal from row R1 (x 8729)
n <-> d   when sel3     d: metal going down into row C (x 8729)
n <-> c   when sel4     c: metal going down into row C (x 8467)
```

sel1..sel4 are horizontal poly lines (y 12223, 12481, 12530, 12786) that enter across
the left edge (x 7600) and end at x 10590, just right of s7. The four gates are
branches of these lines. The transistors gated by sel2 and sel3 lie under the wide rail
at x 8597-8641; the rail has no contact there.

All eight slices are identical (mosaic in both layers).

Believed, not traced: a selector that puts one of four per-slice sources (two in R1
above, two in row C/D below) on n. Direction of each pass transistor is unknown until
R1 and row C are traced.

### Channel 1 (traced)

Eight poly lines `cdp4_bus_s0..s7`, one per slice, at y 12180 (s0), 12137, 12093,
12052, 12008, 11964, 11922, 11877 (s7). Each comes from the left edge and ends on a
metal contact at x 8555 + offset; the metal runs up into row R1 (not into rows A/B).

## Ports

| Name | Layer | Where it crosses | Direction | What |
|---|---|---|---|---|
| `cdp4_sel1` | poly | x 7600, y 12223 | from outside (left) | select: n <-> a |
| `cdp4_sel2` | poly | x 7600, y 12481 | from outside (left) | select: n <-> b |
| `cdp4_sel3` | poly | x 7600, y 12530 | from outside (left) | select: n <-> d |
| `cdp4_sel4` | poly | x 7600, y 12786 | from outside (left) | select: n <-> c |
| `cdp4_bus_s0`..`s7` | poly | x 7600, y 12180, 12137, 12093, 12052, 12008, 11964, 11922, 11877 | unknown | 8-bit bus between row R1 and whatever lies left of the array |

Internal for now (will join when R1 / row C are traced): `cdp4_a_sK`, `cdp4_b_sK`
(metal, drawn up to y 11790), `cdp4_c_sK`, `cdp4_d_sK`, `cdp4_n_sK` (metal, drawn down
to y 12810).

## Ambiguities

None yet in the traced part.

## Not done

- Row R1 (y 11100-11800), row C, channel 2, row D: see Inventory.
- Line at y 11832 (poly, under all slices).
- Rails: identify VSS / VCC and draw at full length.
- Right of x 10600 (y 11800-13600): a wide vertical rail at about x 10740 and several
  thin vertical metal lines at x 10790-10880; not looked at.
