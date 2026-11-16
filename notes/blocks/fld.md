# fld: the logic west of the row address selector (x 6380-7120, y 4720-5780)

Serial work, 2026-11-21. Trace: `trace/fld.txt` (**two inverters only**). Views in
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

## Followed, not drawn

- `ras_o0_alt1`: poly west along y 5303 to a pad (6615,5303); metal on a diagonal and
  south along x 6664 to a pad (6662,5712) in the lower gate group.
- `ras_o0_alt2`: from its pad (6922,4787) a poly west along y 4787 to a pad at about
  (6455,4787).
- The upper group's west part (x 6380-6700, y 5000-5290): two more VCC contact boxes
  (6540,5095), (6540,5255) with a poly foot beside each (from a pad (6447,5045) with a
  metal from the north, and from the south along x 6435), a buried contact box at
  (6495,5180) between them, polys under the thin metals x 6400 and x 6660.
- The lower gate group (x 6540-6920, y 5400-5780): rails x 6575-6620 and x 6790-6830,
  about ten gates. Both `ras_o0_alt1` and `tc1_g` have a pad in it.

## Not done

Everything under "Followed, not drawn"; the routing field y 4720-4990 (seven horizontal
polys with pads at both ends).
