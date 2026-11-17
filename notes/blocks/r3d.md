# r3d: R3's low-nibble data lines, from the data bus

## Status (2026-11-17 08:41, contributor session)

Wiring only (`trace/r3d.txt`), no transistors. The four data lines of R3's 4-bit register
row in the right datapath's top array (`rdp1`'s `r3_b0_d`..`r3_b3_d`, which `rdp1` drew
down to y 6400) are followed to the data bus: **`r3_bK_d` is data bit K for K = 0-3**
(joins by `@alias` to `cdp1_c5_bl`, `cdp1_c4_bl`, `cdp1_c3_bl`, `cdp1_c2_bl`). Stacked
on `bust`, which drew the data bus lines and their routing-zone rows.

## Route

The routing-zone rows of data bits 0-3 (`bust`: from the `ubus` ends to the `rbus` top
contacts) do not end at the `rbus` contacts. They run on east, straight and parallel
(chip-2 shot at 2x over x 14230-16700, `cache/scratch/r3d/strips.png`: no step, only
contact pads), each to a contact under a thin metal of the vertical bundle right of the
upper array. The four thin metals run straight north between the rails x 16340, 16512 and
16730 (metal test in both metal shots at y 7000, 8000, 8800, 9050) to R3's data lines
below their latch row:

| Bit | Row (y), contact | Thin metal | Top | R3 line |
|---|---|---|---|---|
| 0 | 9445, (16273,9443) | x 16274 | contact (16273,6772); poly west along y 6775 (3x) to a contact (15490,6775) | `r3_b0_d` (metal x 15492 from y 6400) |
| 1 | 9400, (16400,9400) | x 16404 | contact (16400,6820), clear of the VCC metal box above it (15 px gap, 5x); poly north to y 6735, west (3x) to a contact (15880,6735) | `r3_b1_d` (metal x 15884 from y 6400, 2.6x) |
| 2 | 9355, (16615,9355) | x 16620 | contact (16615,6760); poly north to y 6688 and west to a contact (16362,6688) | `r3_b2_d`: its metal x 16274 from y 6400 turns east along y 6688 to that contact (2.4x) |
| 3 | 9310, (16660,9312) | x 16664 | straight on north as `r3_b3_d` (follower 9280 to 5670) | `r3_b3_d` |

Bit 0's thin metal x 16274 has one tap on the way, a contact at (16272,9205) with a poly
leaving east along y 9205 (both metal shots and acid1b at 4.5-6x): the data line's branch
to the D-pin units, followed in `dbl`. The other three metals have no contact between their
ends (follower started on each line; independent review surveyed the bundle).

The x 16274 line is two pieces: `r3_b2_d` above (to y 6700, then east) and bit 0 below
(from its contact at y 6772); both metal shots show no metal between (`j1.png`).

Images: `cache/scratch/r3d/` (`ov_top.png`, `ov_bot.png` are the overlays) and
`cache/scratch/bust/e_end.png`, `e_b01.png`, `e_b23.png` (the row ends at 2-4.5x).

## What this establishes

- With `tools/bust_fanout.py`: data bits 0-3 now also write R3 (`wr_r3`); bits 4-7 do not.
  So the 4-bit row in `rdp1` is R3's **low** nibble, the horizontal sync width, compared
  with the `hsw` counter (`hsw_eq_r3`), as the datasheet says. That was taken from the
  datasheet before; it now follows from the trace (the bit numbers themselves rest on the
  register-width match in `bust`).
- R3's high nibble (vertical sync width) should be the four slices of `amr` on data bits
  4-7; `wr_r3` already runs through them. Not traced.

## A fix in `rdp1` (its own commit)

`rdp1` drew `hsw2`'s counter track ending on a contact at (16270,6470), with its metal
hooked west to x 16258 and its poly line y 6472 ending at x 16260. Both metal shots and the
clean shot (2.4x, `b2top.png`) put the ring and the pad at about (16315,6477): the metal
hooks west only from x 16358 to the ring, and `r3_b2_d`'s thin metal x 16274 passes west
of it with a clear gap. As drawn, extending `r3_b2_d` down shorted it to `hsw2`. The fix
moves the contact, the metal's end and the poly's end; the extraction is otherwise
unchanged (same transistor count; `hsw2` still reaches its comparator slice).

## Review

Independently reviewed (2026-11-17): every row, contact, corner and the `rdp1` fix
confirmed; it found the tap at (16272,9205), now described above.

## Not done

- Rows y 9400, 9355 and 9310 (bits 1-3) also run on east past their contacts, to contacts
  near x 16950-17030; row y 9355 may be interrupted at x 16635-16695 (an oval of field
  on the row in the clean shot; continuous in the chip-2 shot). Followed in `dbl`.
