# ras: the row address selector (x 7100-7800, y 4880-6680)

Serial work, 2026-11-18. Trace: `trace/ras.txt`. Views: `cache/scratch/slbus/col5.png`,
`unit_*.png`, `mL1.png`, `mL2.png`, `mR1.png`, `mR4.png`, `top_m.png`, `top_a.png`;
overlay check `cache/scratch/ras/chk1.png`.

## Status

The column and its inputs are drawn and extracted: 11 pass transistors, no load, no supply
rail. The outputs are drawn to x 7960, where each enters a unit of an untraced column; the
five lines from those units to the central datapath's comparator are drawn in full (below);
the two gate lines and the three extra lines of bit 0 only as far as followed. **That the five outputs are the lines to the RA pins is expected, not shown.**

## What it is

The scan line counter's five lines (`sl0`-`sl4`, the metal stretch of `trace/slbus.txt`
at y 6498-6673) are tapped at x 7120-7337: a pad under each metal line, poly north to a
second pad at y 6023/6065, metal north into the column. There each line ends on a
contact box of diffusion. Between the boxes lie horizontal poly strips, about 25 px long
and 140 px wide, each a pass transistor from the box above it to the box below it:

```
            ras_o0_alt2 --[ras_o0_sel2]--+
            ras_o0_alt1 --[ras_o0_sel1]--+-- ras_o0
                    sl0 --[straight]-----+
                    sl0 --[shift]----------- ras_o1 ---[straight]-- sl1
                    sl1 --[shift]----------- ras_o2 ---[straight]-- sl2
                    sl2 --[shift]----------- ras_o3 ---[straight]-- sl3
                    sl3 --[shift]----------- ras_o4 ---[straight]-- sl4
```

- The strips at y 5160, 5340, 5515, 5695, 5870 are joined at their left ends to one
  vertical poly band (x 7151-7171): `ras_straight`. With it high, output k = `sl` k.
- The strips at y 5250, 5425, 5605, 5780 are joined at their right ends to a vertical poly
  band at x 7418-7432: `ras_shift`. With it high, output k+1 = `sl` k: the count shifted
  up one bit.
- Output 0 then has no counter bit. It has two more pass transistors at the top of the
  column: S2 (y 5078-5100; gate `ras_o0_sel1`, a metal from the north) from
  `ras_o0_alt1` (a metal from the west), and S1 (y 4945-4970; gate `ras_o0_sel2`, a poly
  from the north) from `ras_o0_alt2` (a metal from the north-west).

A shift by one with a separate bit 0 is what interlace sync and video needs on the RA
pins (row address = line count times two, plus the field). That is the reading, and the
names carry it; nothing traced yet says which mode drives which gate line.

## Contacts (centres)

| Node | Contact | Metal |
|---|---|---|
| `sl0` | 7235,5215 | from x 7120, east along y 5218 |
| `sl1` | 7235,5390 | from x 7164, east along y 5390 |
| `sl2` | 7248,5567 | from x 7208, east along y 5564 |
| `sl3` | 7264,5738 | from the south along x 7270 |
| `sl4` | 7337,5915 | from the south along x 7337 |
| `ras_o0` | 7337,5130 and 7337,4908 (strapped by a metal x 7381) | east along y 5132, north x 7576, east y 4847, north x 7712, east y 4765 to x 7793 (follower) |
| `ras_o1` | 7325,5300 | north, east along y 5258 over the strip, north x 7490, then north-east on a diagonal |
| `ras_o2` | 7335,5475 | y 5439 east, x 7402 north, y 5305 east, x 7532 north, y 5220 east, x 7662 north |
| `ras_o3` | 7332,5652 | east, x 7402 north to y 5502, jog east, x 7448 north, y 5350 east, x 7582 north to a pad (7577,5262); on east along y 5262 |
| `ras_o4` | 7335,5828 | east, x 7452 north, y 5546 east, x 7490 north, y 5393 east to a pad (7577,5392); poly on east |
| `ras_o0_alt1` | 7290,5045 | west along y 5066, south x 7072 to y 5311 (follower) |
| `ras_o0_alt2` | 7205,5000 | north x 7207, west along y 4788 to x 6922 (follower) |
| `ras_o0_sel1` | pad 7425,5090 at the strip's end | x 7467 north, y 4746 east, x 7657 north, y 4673 east to x 7860 (follower) |

## How sure

- The chain of boxes and strips: read in three shots at 4.4x for one unit
  (`unit_acid1b.png`, `unit_acid.png`, `unit_metal.png`) and at 2.5-3x for the rest. Each
  box has two diffusion fingers, one along the strip above and one along the strip below,
  with a field island between them; the trace draws one rectangle through each strip
  instead. The overlay sits on every strip, box and metal.
- Left band and its joins to the strips at y 5160, 5340, 5515: plain in the chip-2
  stripped shot (`mL1.png`). Below y 5390 the band lies under `sl1`'s metal and the two
  lower joins are placed by the strips' ends: marked `?`.
- Right band: plain. The four joins of the shift strips to it lie under the outputs'
  metal (x 7402) and are read from the strip outline reaching x 7410 (`unit_metal.png`,
  `mR1.png`): marked `?`. The alternative for both bands (a strip tied to the wrong band)
  would give a selector that makes no sense, but that is not evidence.
- **AMB-010**: `ras_o0_alt2`'s metal x 7207 crosses the strip S1 at (7207,4955). A dark pit shows
  there in the chip-2 stripped shot; there is no ring in either metal shot. Read as no
  contact.
- `ras_o3`'s jog from x 7402 to x 7448 at y 5502 crosses the right band: both metal shots
  show bright metal across it, cut by the band's edge lines. There is no pad, so no
  contact to the band.
- The metal routes are from `tools/follow.py` and one 3x view (`mR4.png`); three of the
  ends were not looked at.

## Where the outputs go (corrected 2026-11-19)

Views `nestN.png`, `xu.png`, `pads7.png`, `t4.png`, `cache/scratch/rax/pad3.png`, `pe.png`;
overlay checks `chk2.png`, `chk3.png`.

**All five outputs leave east as poly lines**, each from a pad at the end of its metal,
into a column of five identical units at x 7860-8100 (`trace/rax`, not traced yet):

| Output | Pad | Poly east along |
|---|---|---|
| `ras_o0` | 7795,4765 | y 4765 |
| `ras_o1` | 7748,4893 | y 4893 |
| `ras_o2` | 7708,5133 | y 5133 |
| `ras_o3` | 7577,5262 | y 5262 |
| `ras_o4` | 7577,5392 | y 5392 |

Each poly crosses its unit under the rails and ends, rounded, at x 8035. Nothing else is
on an output: no output goes anywhere but into its unit.

**Each unit has a second pad** at x 7832-7836, 43 px below its output's poly, with a
short poly into the unit. From these five pads the **nest of metals** east of the
selector (x 7530-7840, y 4800-5940) runs to five pads at the west ends of poly lines
that go east and, in nested steps at x 8295-8462 (clean shot at 2.9x, `join_a.png`), come
down onto the long lines of the central datapath's channel 1 that `trace/cdp2.txt`
starts at x 8480. All of it is drawn, and the extraction joins each to a through track of
that block's 5-bit comparator:

| Unit of | Pad | Channel pad | Channel line | Net |
|---|---|---|---|---|
| `ras_o0` | 7836,4808 | 7707,5935 | 6000 | `cdp2_trk_s7` |
| `ras_o1` | 7836,4945 | 7660,5890 | 5956 | `cdp2_trk_s6` |
| `ras_o2` | 7836,5172 | 7705,5848 | 5913 | `cdp2_trk_s5` |
| `ras_o3` | 7836,5300 | 7660,5800 | 5870 | `cdp2_trk_s4` |
| `ras_o4` | 7832,5437 | 7705,5758 | 5826 | `ch1w_5758` (in `cdp2`, slice s3 is wired differently: its notes) |

So the comparator of the central datapath's rows B (against the register of row C) is
fed, bit for bit, from the five units that take the selector's outputs: slice s7 is bit
0, s3 is bit 4, which is the order `notes/blocks/cdp2.md` needs for its magnitude chain
(s3 most significant). **What a unit does to its input (invert, buffer, latch) is not
traced.** `cdp2`'s own reading needs the tracks to carry the complement of the value.

### The mistake in the first version of this section

The first version (commits a313716, d96baf3) said "`cdp2_trk_s7` is `ras_o3`". Wrong.
The line from the pad (7836,4808) comes down the staircase, runs **west along y 5264 on
top of `ras_o3`'s poly** and turns south at x 7620; that corner stops 19 px short of
`ras_o3`'s pad (7577,5262). I read the bright metal east of the pad's ring, on a 3x
view, as leaving the pad. Checks that show two nets: both metal shots at 6x
(`pad3.png`: dark between x 7590 and 7610, 24 px against 10 px of ring on the side
where the pad's own metal arrives; in chip 1 the poly's colour shows there); the
follower started on the pad's own metal stops at the pad; the corner's west edge is the
vertical's west edge. Trap 16 of the tracing guide; re-read item R11.

Also seen: a sixth pad at (7832,5522) with a poly east and a metal south along x 7832
(not drawn); two more pads at the channel's west end, (7748,5672) and (7790,5718), with
metals south to y 6070 and y 6158 (not drawn).

## Not done

1. The five units at x 7860-8100, y 4730-5460 (`rax`): what each does with its output
   bit, and what leaves them towards the RA pad drivers (the lines found at the pad end
   are listed in `notes/blocks/trunks.md`).
2. `ras_straight` and `ras_shift` to their drivers: the left band bends west at its top
   (y 5140); the right band goes on north-east from (7425,5235).
3. `ras_o0_alt1`, `ras_o0_alt2`, `ras_o0_sel1`, `ras_o0_sel2` to their sources.
4. What is under the pad (7577,5262).
