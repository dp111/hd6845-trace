# fld: the logic west of the row address selector (x 6380-7120, y 4720-5780)

Serial work, 2026-11-21/22. Trace: `trace/fld.txt` (two inverters and two XOR cells; the upper group's west part not traced). Views in
`cache/scratch/rax/`: `fld_a.png`, `fld_m.png` (the upper group, clean and metal at 1.65x),
`fldR.png`, `fldM.png`, `fldL.png` (three tiles at 2.7x), `fldA1.png`, `fldA2.png` (chip-2
stripped shot at 3.4x: the clearest), `fldG.png`, `fldB.png`, `fldS.png`, `fldD.png`,
`fldE.png`.

## Why this block matters

The two signals that can become row address bit 0 in interlace sync and video
(`ras_o0_alt1`, `ras_o0_alt2`) and the two that switch the R9 comparator's bit 0
(`tc1_i`, `tc1_g`) all come from here. This is where the field (odd/even) logic is
expected. Most of it is not traced.

## Traced: two inverters at the east end (x 6700-7050, y 5020-5275)

    tc1_g = NOT fld_a_in        tc1_i = NOT fld_b_in

Each: VCC contact box under the rail x 6700-6750, a load (poly block x 6765-6825 over
the band, its tail tied back to the output through a buried contact, `?`), the output
band east as a thin diffusion to a buried contact at x 6975, and one pull-down under the
rail x 6880-6925 with a VSS contact box below the gate. 4 transistors. The rails' supply
assignment is by the layout rule, not followed.

- Upper (output `tc1_g`): the buried contact (6975,5048) is on the poly that goes north to
  the pad (6985,4958); from that pad a metal goes to the pad (7050,4830) and the poly on
  to the island (`trace/ras.txt`), and **a second poly goes west along y 4958 to a pad
  (6660,4958)**, whose metal runs south along x 6660, then on a diagonal, to a pad
  (6752,5428) in the lower gate group. Gate `fld_a_in`: poly from the north along
  x 7020-7048, which comes from a horizontal poly along y 4910 from the west.
- Lower (output `tc1_i`): the buried contact (6982,5178) is on the island's input poly,
  which arrives from the east along y 5178 (`trace/ras.txt`). Gate `fld_b_in`: poly from
  the pad (7030,5215); metal south to a pad (7032,5345); poly west along y 5345 past
  x 6560.

## Traced: two copies of the comparator's XOR cell (x 6580-7030, y 5410-6100)

`tools/findcell.py` on the lower gate group: scores 0.88-0.91 against the five slices of
`cdp1`'s row B (and the comparator slices of the right datapath). The group is a copy of
the cell `cdp1_xor`, and 347 px below it stands a second copy. Both instanced
(`@inst cdp1_xor -2581,1758 tag=fx` and `-2581,2105 tag=fy`); the overlay sits on every
contact, pad, load block and gate of both (`fx_chk_a.png`, `fx_chk_m.png`, `fy_chk_m.png`).
Rails: west VSS x 6575-6625, VCC x 6800-6840, east VSS x 6978-7028 with the contact that
the next slice provides in the comparator rows ((7005,5615) and (7005,5962), rings in the
metal shot). 14 transistors. From the extraction:

    fld_b_in    = fld_x_a XOR tc1_g         (first cell)      tc1_i = NOT fld_b_in
    ras_o0_alt1 = fld_y_a XOR fld_y_b       (second cell)

Ports:

| Cell | Input B (metal x 6754, two pads) | Input A (poly x 6919-6942) | Output "ne" |
|---|---|---|---|
| first | `tc1_g`: its metal from the pad (6660,4958) comes down x 6665, a diagonal, x 6753 onto the upper pad (6752,5428) | `fld_x_a`: pad (6925,5718), metal west and south along x 6885 to a pad (6880,6062), poly south along x 6882 | a poly comes down x 6665 from the line along y 5345 (`fld_b_in`, the lower inverter's gate line) onto the cell's output diffusion |
| second | `fld_y_b`: the metal goes on south to y 6085 and west to a pad (6660,6085), poly west | `fld_y_a`: the poly goes on south along x 6930 | a poly comes down from the pad (6662,5712) at the end of `ras_o0_alt1`'s metal |

**Assumption (trap 17), both cells**: the buried contact between the poly that arrives
from above and the output diffusion is not resolved in any shot (`?B`). It is placed
where the original cell has its buried contact to the comparator's NOR gate, and in both
copies a poly ends exactly there. `tools/unsure.py` cannot see these two joins (the
cell's output diffusion carries no label of its own).

So, as traced: the line that can become row address bit 0 when R9's bit 0 is set is
the XOR of two signals, and the comparator's bit-0 input for the same case is the XOR of
the upper inverter's output with a third signal. None of `fld_x_a`, `fld_y_a`,
`fld_y_b`, `fld_a_in`, `ras_o0_alt2` is traced to its source.

## Followed, not drawn

- `ras_o0_alt2`: from its pad (6922,4787) a poly west along y 4787 to a pad at about
  (6455,4787).
- The upper group's west part (x 6380-6700, y 5000-5290): two more VCC contact boxes
  (6540,5095), (6540,5255) with a poly foot beside each (from a pad (6447,5045) with a
  metal from the north, and from the south along x 6435), a buried contact box at
  (6495,5180) between them, polys under the thin metals x 6400 and x 6660.
- `fld_x_a` south of (6882,6220), `fld_y_a` south of (6930,6220), `fld_y_b` west of
  (6560,6085), `fld_b_in`'s line west of (6560,5345), `fld_a_in`'s line (y 4910) west.

## Not done

Everything under "Followed, not drawn"; the routing field y 4720-4990 (seven horizontal
polys with pads at both ends).
