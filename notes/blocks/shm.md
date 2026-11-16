# shm: what makes the row address selector's mode line (x 8250-10670, y 2800-4110)

Serial work, 2026-11-20. Trace: `trace/shm.txt`. Views in `cache/scratch/rax/`:
`shiftsrc.png`, `shiftgate.png`, `g1a.png`, `g1m.png`, `g0top.png` (the two gates);
`ns56.png`, `ns56e.png`, `ns56f.png`, `a5q.png` (their inputs).

## Result (from the extraction)

    ras_shift_n = NAND(cdp1_a4_q, cdp1_a5_q)       two pull-downs in series, a load
    ras_shift   = NOT ras_shift_n                  one pull-down, a load
    ras_straight = NOT ras_shift                   (in the island tc1)

`cdp1_a4_q` and `cdp1_a5_q` are the outputs of the two register bits of **R8** in the
columns c6 and c7. So the row address selector shifts the scan line count up one bit,
and the R9 compare changes (`notes/blocks/ras.md`), exactly when both of those bits of
R8 are set. Column c7 is bit 0 in the block below (`cdp2`: its slice s7 takes row address
bit 0), so these are taken to be R8's bits 0 and 1, the interlace mode bits, and the
mode is "interlace sync and video". That the column order of R8's row is the same as
`cdp2`'s is not traced (its bit lines are not followed to the data pads); the result
itself is the support for it.

## The two gates (x 8300-8650, y 3760-4110)

In the slice-0 position below R8's row, under that slice's VSS rail (x 8415-8465), loads
towards its VCC rail (x 8595-8650):

- NAND: VSS contact (8432,3800); two polys cross the diffusion below it in series
  (y 3821-3844 from the contact (8270,3833) of the metal that the island's notes called
  ns5, y 3861-3884 from the contact (8313,3870) of ns6); output band y 3888-3925, east to
  a load (poly block x 8535-8585) and a VCC contact (8618,3897); west to a buried
  contact on a C-shaped poly that goes down x 8312 and east as the next gate.
- Inverter: VSS contact (8432,4010); gate y 4038-4056; output band y 4060-4095 with the
  same load arrangement; west through a buried contact to the poly that ends on the
  contact (8313,4090) of the mode line's metal (`trace/tc1.txt`).

Ten transistors with the island's two that it already had on the net; five are new
here. The four buried contacts are marked `?` (placed from the heavy dark boxes at the
poly ends); everything else is plain in the clean shot at 2.7-2.9x.

## The two inputs

The metals ns5 (x 8270) and ns6 (x 8314) of `trace/tc1.txt` come from two of five
horizontal metals above R8's row (y 2768-2945). Each crosses under two slice rails in
poly. Followed with `tools/follow.py`, pads seen on 2.3-2.6x views, drawn:

- y 2813: from ns6's corner east to a pad (9095,2813), poly, pad (9290,2813), metal,
  pad (9878,2813), poly, pad (10062,2813), metal east and south to the pad (10653,2940)
  at the top of bit a5's output poly.
- y 2857: from the pad (8355,2857) at the end of ns5's poly east, pads (9055,2857) and
  (9255,2857), (9836,2857) and (10022,2857), metal east and south along x 10282 onto bit
  a4's output metal.

The extraction joined each to the bit's output net and nothing else; the island's
names for the two metals were dropped. Not drawn: the line y 2945 (bit a2's output, by
its end at (9508,3034)), y 2900 (bit a3's, by its end near the pad (9865,2940)) and
y 2768 (ends on a pad (10614,2768)); they feed the island's other metals ns2-ns4 and
whatever else lies west.

## Not done

The other three lines; R8's bit lines to the data pads (the bit order).
