# wrs: the write strobes of R8, R9, R10 and R11 to their register rows

Serial work, 2026-11-20. Trace: `trace/wrs.txt`. Views: `cache/scratch/rax/wr1.png`,
`wr2.png`, `wr3.png` (the cross-under under the vertical trunks), `wr9top.png` (R9's top end).

## Result

The four strobe tracks T3-T6 of `trace/bd3.txt` (`wr_r8`, `wr_r9`, `wr_r11`, `wr_r10`,
drawn there west to x 14090) are drawn on to their ends, and the full extraction joins
each to the load strobe of one register row of the central datapath. The names were made
one:

| Strobe | Register row | Bits | The row's strobe before the join |
|---|---|---|---|
| `wr_r8` | `cdp1` row A (y 3040-3330) | 6 | former name `cdp1_a_wr` |
| `wr_r9` | `cdp1` row C (y 4232-4524) | 5 | former name `cdp1_c_wr` |
| `wr_r11` | `cdp2` row A (y 6020-6345) | 5 | former name `cdp2_a_ld` |
| `wr_r10` | `cdp2` row C (y 7500-7825) | 7 | former name `cdp2_c_ld` |

So, by their strobes: **R8 is the 6-bit row at the top, R9 the 5-bit row with the
equality comparator below it, R11 the 5-bit row of `cdp2`, R10 the 7-bit row whose five
low bits go to the equal-and-greater comparator.** The widths agree with the data sheet in
all four (R8: interlace, two display-skew bits, two cursor-skew bits; R10: five raster
bits and two cursor mode bits), which also supports the register numbers that
`notes/blocks/sel.md` gave the decoder's lines.

What the numbering rests on: the decode array's assignment of select lines to register
numbers (`sel`). Nothing in this block tests that independently except the four widths.

## Route (the same for all four, nested throughout)

| Stretch | Layer |
|---|---|
| from x 14090 west along y 17128 / 17170 / 17214 / 17258 to pads at x 13386 / 13430 | metal |
| under the vertical trunks to pads at x 12805 / 12850 | poly |
| west to x 11636 / 11588 / 11549 / 11506, north, a 88 px step west at y 14618-14748, north along x 11549 / 11505 / 11461 / 11418 | metal |
| a 45-degree diagonal, 435 px in each direction, up to x 11113 / 11070 / 11026 / 10982 at y 10167-10236 | metal |
| north along the central datapath's east edge, each line stepping 44 px west (a short diagonal) just above each place where the innermost line ends | metal |
| the innermost line ends on a pad at the east end of a row's strobe poly: (10894,7801) R10, (10896,6325) R11, (10893,4505) R9, (10891,3308) R8 | contact, poly |

## How sure

- Metal: `tools/follow.py` end to end for each line, from both ends for three of them.
  The follower does not report the 44 px diagonal steps or the long diagonal as corners;
  they were located by running it with `--max` in 50 px stages (positions in the trace
  are good to about 10 px along the line).
- Pads of the cross-under: one 3.2x view in both shots (`wr3.png`) for the west four;
  the east four from the follower's ends and a 1.3x view.
- The extraction: four joins, each of one strobe with one row's strobe poly, and no
  other net merged (2,025 to 2,021 nets). A wrong step somewhere would have merged two
  strobes or left a line open.
- `trace/cdp1.txt` drew the two write polys only to x 10785; the 108 px to the pads are
  from one 3.6x view (`wr9top.png`): they cross two thin metals without a contact.

## What this identifies besides

- **R9's comparator** is `cdp1`'s row B: five XORs and a NOR, `cdp1_b_eq` (traced earlier).
  Four bits compare the register with a line each. In the fifth slice the register bit
  is replaced by the output of the nine-gate island `tc1`:

      cdp1_b5_a = NOR(tc1_r2_out, tc1_r4_out)
      with b = ras_shift, q = R9's bit of that slice, g = tc1_g, i = ras_o0_alt1:
      b = 0:  cdp1_b5_a = q
      b = 1:  cdp1_b5_a = NOT( i if q else g )

  One bit of the R9 compare is switched by `ras_shift` between the register bit and a
  function of two other signals: the shape of "R9 is N-2 and the field decides" in
  interlace sync and video. `ras_shift`, `tc1_g`, `ras_o0_alt1` are not traced to their sources,
  and that the slice is bit 0 rests on the column it stands in.
- **The value R9 is compared with** is traced: `trace/r9c.txt`, `notes/blocks/r9c.md`. It
  is the row address as it goes to the pins (`ra#_cmp`, made from the pad drivers' input
  lines by five units near the right edge), not the lines R10's comparator uses.

## Not done

`ras_shift`, `tc1_g`, `ras_o0_alt1`. The
nets of the four rows still carry `cdp1_`/`cdp2_` names (queue).
