# Data bus interface column (`dbus`)

Region: x 17050-17700, y 5300-17000, and the D0-D7 pad cells to its right.
Trace: `trace/dbus.txt`. Scratch tools: `tools/dbus_mosaic.py` (the same rectangle at
several offsets side by side, for comparing repeats), `tools/dbus_autocorr.py`
(vertical pitch of a strip).

## Status

Traced, extracting, overlay-checked: the input buffer chain (four inverters) as cell
`dbus_in`, placed six times (D0-D5); the input line of D0 from where it enters the
column, and the whole input line of D1 from the pad cell's contact.

Surveyed, with coordinates below, but NOT traced: the gate group ("cluster") under
each of chains 0-3, all other logic in the column, the channel wiring to the pads.
The pad cell (AMB-003) was not attempted; what the column tells us about its two
lines is under "P_x and P_y" below.

## Inventory

The column is not one unit per pad at the pad pitch. Logic occupies y 8030-16600
only; between y 5900 and 8030 there are just the rails and three metal lines coming
down from the D0 pad cell. Gates sit on a 152 px vertical pitch between two rails:

- VSS rail, metal, x 17355-17400 (pull-down diffusions under it; further up it joins
  a wide trunk at y 6620-6720).
- VCC rail, metal, x 17527-17585, top end at y 8287, bottom end about y 17000 where
  it joins a wide horizontal metal (y 16960-17010).
- Loads between the rails at x 17420-17520; gate outputs leave to the left in poly.
- Which rail is which comes from the orientation of the loads (every load's far end
  contacts the right-hand rail); neither rail was followed to a pad.
- Left of the VSS rail (x 17050-17300) is a wiring field. From unit 1 downward it
  carries five vertical metal lines (x about 17075, 17120, 17165, 17207, 17252).

| What | Where | State |
|---|---|---|
| Input chain, D0 | 17255-17590 x 8280-8880 | cell `dbus_in`, traced |
| Input chain, D1-D5 | same cell at (1,1365) (1,2732) (2,4098) (2,5465) (2,6223) | placed; findcell on the clean shot scores 0.81-0.83, each overlay checked at 1.25x. The four-gate core is the same in all six; the wiring left of x 17290 differs per copy and is drawn only for D0 (and D1's input) |
| Capacitor rectangles of chain 0 | 16960-17040 x 8445-8580 and x 8745-8880 | drawn |
| Cluster 0 | 17150-17590 x 8885-9520 | not traced, see below |
| Clusters 1-3 | cluster 0 + 1366, 2732, 4098 (by eye at 0.5x; not checked) | not traced |
| Cross-unders between units 0 and 1 | poly "line 1" y 9545-9566, "line 2" y 9590-9610, both under both rails | line 1 drawn (D1 input); line 2 is D1's P_y, not drawn |
| Logic below chain 5 | 17150-17590 x 15100-16600 | single gates on the 152 pitch, not surveyed in detail. No cluster follows chains 4 and 5 (chain 5 starts 758 px below chain 4) |
| Logic above D0 | 17200-17700 x 5250-5900 | several gates, not looked at |

findcell (metal and clean shot, threshold 0.4) finds no seventh or eighth copy of
the chain. Where the input buffers of D6 and D7 are is not known; the lower part of
the column (y 15100-16600) is the first place to look, then the corner by the
bottom-right input pads.

## Logic

### Input chain `dbus_in` (traced)

Four inverters in series, the same arrangement as the R/W, RS and CS input buffers
in the bottom row (`rw_a`..`rw_d`). For chain n:

    dN_a = NOT dN_in      (G1, y 8287-8425 in chain 0)
    dN_b = NOT dN_a       (G2, y 8436-8568)
    dN_c = NOT dN_b       (G3, y 8588-8720)
    dN_d = NOT dN_c       (G4, y 8742-8870)

- `d0_in` is the line from the D0 pad cell (Ports). Traced into G1.
- `d1_in` is traced from the D1 pad cell's contact into chain 1's G1, so chain 1 is
  D1's. Chains 2-5 are tagged by position and *assumed* to follow the pad order.
- `d0_b` and `d0_c` each run left in poly to a metal contact next to a plain
  diffusion rectangle (the "added capacitance" rectangles of the bottom row). The
  strap from `d0_c`'s contact (17078,8795) to its rectangle (contact 16990,8787) is
  there. The strap for `d0_b` (contacts 17078,8490 and 16988,8468) is absent in both
  metal shots: each contact carries only a dot of metal. They are NOT bus lines.
- Only `dN_d`, the pad level delayed by four inverters, feeds logic. `d0_d` leaves G4
  in poly to a contact at 17205,8837 and goes down in metal (x 17198-17218, "M_a")
  into cluster 0, ending at a contact at 17207,9255.
- G1's gate poly continues into an L (17413-17503 x 8292-8318) that crosses no
  diffusion and ends beside the load, as on the bottom-row input inverters (AMB-004).

In chains 1-5 the b and c lines also run left (for chain 1: `d1_b` up at x 17225-17245
to y 9750 and left along y 9740-9760; `d1_c` left to x 17165 and down), presumably
to their capacitors; not followed.

### Cluster 0 (observed, NOT traced; none of this is in the trace file)

Seen in 2.6x-4x views. Reliable: the diffusion column under the VSS rail and the
poly bands crossing it. Not resolved: everything between the rails at x 17400-17525.

Vertical metal lines through the cluster:
- M_a x 17198-17218: `d0_d`, from 17205,8837 to a contact at 17207,9255.
- M_b x 17243-17262: starts at a contact at 17252,8990 (to poly band B) and runs on
  down through unit 1 and beyond: a line shared by several units.
- M_c x 17305-17325: from a contact at 17303,8942 (poly band A) to a contact at
  17313,9345.
- thin metal x 17438-17458: D0's `P_y` (see Ports), through the whole of unit 0.
- M_d x 17488-17508: from a contact at 17492,9010 to a contact at 17492,9210.
- VCC rail carries one long contact at 17555, y 9080-9165 and ordinary ones at
  17555,9270 and 17555,9430.

Diffusion column under the VSS rail, x 17325-17405, top to bottom:

| y | What |
|---|---|
| 8890-8935 | VSS land, contact 17362,8910 |
| 8937-8962 | poly band A (left end on the contact at 17303,8942, metal M_c) |
| 8962-8985 | diffusion |
| 8985-9012 | poly band B (runs left to the contact at 17252,8990, metal M_b) |
| 9012-9058 | node N0. A heavy-outlined box at 17295-17345 x 9022-9052 on its left looks like a buried contact (N0 leaving in poly); where that poly goes is not resolved |
| 9058-9110 | VSS land, contact 17363,9090 |
| 9112-9133 | poly band C |
| 9133-9195 | node N1 |
| 9195-9218 | poly band D |
| 9220-9240 | diffusion |
| 9243-9263 | poly band E |
| 9265-9310 | VSS land, contact 17368,9285 |
| 9360-9400 | VSS land, contact 17362,9380 |
| 9410-9432 | poly band F |
| 9432-9470 | node N2 |

Read as gates this gives N0 = NOT(A.B), N1 = NOT(C + D.E), N2 = NOT(F) (or more
inputs). Loads and outputs were not resolved, so these equations are a reading of the
pull-downs only. Other features, unexplained:
- Two nested L-shaped poly lines right of the column at 17400-17520 x 8915-9020; the
  inner one (y 8943-8965, then down x 17495-17520) ends on M_d's top contact
  (17492,9010). Band A (y 8948-8968 at its right end) lines up with it and may be
  the same line.
- A closed outline 17403-17447 x 8935-9022 in the gap between the VSS rail and the
  thin metal: gap artefact or a diffusion strip, undecided.
- A ring-shaped outline 17425-17535 x 9095-9160 beside the long VCC contact, with
  poly under M_d at x 17478-17520 from y 9060 to 9200. Probably the driver of
  `P_y` (whose load is in the pad cell, see below).
- A load with VCC contact 17555,9270 (poly block 17470-17520 x 9255-9300) and one
  with VCC contact 17555,9430 (vertical poly block 17487-17520 x 9395-9480).

### P_x and P_y (established about the two lines of AMB-003)

- **P_x is one line common to all eight pad cells**, not a per-bit line. A single
  vertical metal at x 17633-17650 starts at D0's contact (17625,7380), has a contact
  to each cell's P_x poly at that cell's P_x height (17640,9115 for D1; 10860,
  12440, 14030, 15630, 17235 for D2-D6) and ends on D7's contact (17625,18835).
  Continuity was seen at 1.3x from D0 to D1 and at the bottom end, and at 0.5x in
  between. Where it is driven was not found: no branch was seen at the top or bottom
  end, so the driver must tap it somewhere along the column.
- **P_y is per bit.** D0's comes up the column on the thin metal of unit 0; D1's
  comes from a metal line at x 17110-17130 that rises from below to a contact at
  17120,9620, then crosses in poly (line 2); D7's arrives in poly down x 17590-17605
  and along y 18905-18935.
- Consequence for the pad cell, using the facts in pads.md: rows G (VCC) and H with
  strip 1 (gate P_x, row H tied to P_x by the buried contact) form a depletion load
  *on P_x*, and row K (VCC) with P_y's buried contact a depletion load *on P_y*. So
  both lines are open-drain as far as the column is concerned, with a pull-up in
  every pad cell (eight in parallel on P_x). That would make P_x an enable shared by
  the cells and P_y the data, with the cell containing the gating (rows I, J and the
  S1/S2 nets). This is inference from the earlier notes, not a new reading of the
  pad cell.

## Ports

| Name | Layer | Where | Direction | What |
|---|---|---|---|---|
| `d0_in` | metal x 17548-17566 | comes down from the D0 pad cell: poly from a contact near 17818,6578 left along y 6578, down to a contact near 17546,6755, then metal down; turns left at y 8188 (cross-under 17300-17500) | in | D0 pad after its protection structure. Drawn from y 8050 down |
| `d1_in` | poly | from the D1 pad cell's contact at 17822,8400 (drawn up to x 17835) | in | D1 pad after its protection structure |
| `d2_in`..`d5_in` | poly | G1 gate band of each chain, at 17291,8340 + offset | in | not followed to the pads |
| `dN_d` | poly, then metal | G4 output, 17290-17345 x 8825-8847 + offset | out of the chain | pad level, buffered and delayed; into the cluster |
| P_y of D0 | metal x 17590-17610 from the pad cell (contact near 17580,7495), contact 17597,8097, poly cross-under y 8090-8105, contact 17510,8097, metal left to x 17448 and down as the thin metal | - | to the pad | not drawn |
| P_y of D1 | poly y 9225-9240 from the pad cell to x 17650, down x 17640-17655 (under the P_x metal) to line 2 (y 9590-9610), left to a contact at 17120,9620, metal x 17110-17130 downward | - | to the pad | not drawn |
| P_x | metal x 17633-17650, y 7380-18835 | contacts listed above | to the pads | common enable-type line, not drawn |
| M_b | metal x 17243-17262 | from 17252,8990 down through unit 1 | unknown | shared control line of the clusters, not drawn |
| lines from the core | metal | two wide metals arrive from the left at y 9520-9545 and 9565-9585 and turn down at x 17195-17215 and 17155-17175; another arrives at y 9460-9480 to a contact at 17207,9470 | unknown | not followed |

**Internal data bus: not identified.** The two poly lines leaving each chain to the
left (y 8532 and 8792 in chain 0) are the capacitor taps, not bus lines. The bus
lines must leave from the clusters or run in the left-hand wiring field.

## Ambiguities

- `d0_b` capacitor: contacts cut, strap absent in both metal shots. Looks like a
  metal-mask option. No effect on logic.
- Chains 2-5 are assigned to D2-D5 by position only.
- Whether clusters 1-3 are exact copies of cluster 0 has not been checked.

## Not done

- Clusters 0-3 (start with the diffusion-column table above; the open questions are
  the loads and the structures at x 17400-17525).
- Left-hand wiring of chains 1-5: capacitor taps, and where each `dN_d` goes
  (for chains 4 and 5 there is no cluster below).
- Logic at y 15100-16600 (and the D6, D7 input buffers), logic at y 5250-5900.
- Channel wiring x 17590-17830: P_x line, P_y lines, input lines of D2-D7.
- The driver of P_x.
- Pad cell (AMB-003): not attempted.
