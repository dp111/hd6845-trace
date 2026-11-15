# wl: logic west of the 4-bit counter (x 11080-11700, y 6950-9450)

Serial work, started 2026-11-16. Trace: `trace/wl.txt`. Views: `cache/scratch/wl/`.

## Status

Traced and extracted (16 transistors): **the clock generator of the character-row
counter**, y 7890-8900. Not yet traced: everything north of y 7890 in this block (where
signal `p` comes from), the vertical metals x 11060-11210 that pass over the drivers, and
the other lines that enter from the bus channel y 9182-9435 (bus lines B, C, G).

## What is west of the counters

- x 10850-11700 from y 9450 down to 17000 is not logic: it is a field of about twenty
  vertical metal lines between the central datapath and the counters, with fans of poly
  taps into the central datapath's rows (y 7800-8000, 10300-10700, 13300-13600).
- The logic is one block, x 11080-11660, y 6950-9150, beside rows r0-r3 (the 4-bit counter).
  Two wide vertical rails run through it: **VSS x 11437-11487** and **VCC x 11605-11655**
  (a metal with a contact every 40 px onto a diffusion strip). At its bottom the VSS rail
  turns east along y 9100-9150 and runs into the mid-right array's rail x 11800-11850:
  that is the feed of mra's "vss rail x 11828" (mra A4, now closed).

## The row counter's clock generator (traced)

The two clock lines of the 7-bit counter come up out of the bus channel into this block:

| Line | mra name | Route from the channel |
|---|---|---|
| D, slave clock | `mra_s7` | contact (11655,9315), metal west, contact (11519,9315), poly north under the VSS bus, contact (11519,9010), metal x 11512-11533 north to the contact (11517,8150) |
| E, master clock | `mra_m7` | poly y 9351-9369 west to x 11565, north, contact (11564,9057), metal x 11553-11578 north to the contact (11567,8622) |

Extracted logic (names `wl_*`):

```
pb     = NOT p                     pull-down 62/22, load 35/40
D      = NOR(e_buf, p)             pull-downs 374/25 and 322/25, depletion load 100/40
E      = NOR(pb, d_buf)            pull-downs 340/20 and 382/23, depletion load 99/40
e_n    = NOT E      (62/22, load 25/87)        e_buf = NOT e_n   (64/27, load 41/35)
d_n    = NOT D      (65/23, load 28/92)        d_buf = NOT d_n   (64/21, load 40/35)
```

So with `p` low, D (slave clock) is high and E (master clock) low; a high `p` pulls D low
at once, and E rises only after `d_buf` has fallen; when `p` falls, E falls (through `pb`)
and D rises only after `e_buf` has fallen. It is a **non-overlapping two-phase generator
driven by the single signal `p`**: E follows `p`, D follows `NOT p`, each delayed past the
other's fall by two inverters. The counter's master latches take the next count while `p`
is high, the slaves pass it on when `p` is low again: the row counter steps once per pulse
of `p`.

`p` arrives on the vertical metal x 11277-11297 from the north (contact (11285,8362) on
the gate band). Not yet followed.

### How it is built (for reading the rest of the block)

- Pull-downs are horizontal poly bands across diffusion; the VSS rail runs over a column of
  that diffusion and contacts it between the bands. The two big NORs use one diffusion
  area x 11140-11497 each, crossed by two bands, so each pull-down is 320-380 px wide.
  The bands are fed at one end and run in loops round the area's edge to reach the far
  columns (one crosses a column diagonally).
- Loads are in the right-hand column, under the two clock metals: a strong load is a
  vertical poly x 11557-11597 over a strip between the node (left) and the VCC strip
  (right); a weak load is a poly plate 90 px long over a 25 px strip. Each load gate is
  tied to its node by a buried contact on a short neck of the node's diffusion.
- The signal metals pass over the big diffusion areas without contact. Between the metals
  the diffusion is open and looks pink (boxes with a heavy outline) or greenish in the
  clean shot; under the metals it is tan. The dark lines between are the margins of the
  metal (tracing guide, trap 2), not layout. Open diffusion was told from open field by the
  chip-2 shots: `tools/classmap.py --open`.

## Ports (so far)

| Name | Layer | Where | Dir | What |
|---|---|---|---|---|
| `mra_s7` | M | (11655,9315) | out | slave clock of the row counter |
| `mra_m7` | P | (11640,9360) | out | master clock of the row counter |
| `wl_p` | M | x 11277-11297 at y 7960, continues north | in | the row counter's step pulse |
| vss | M | y 9100-9150 at x 11832 | - | joins mra's rail |
| vcc | M | x 11605-11655 at y 7890, continues north | - | |

## Not done

Listed under Status. Tools: `tools/wl_net.py` (extraction report restricted to a box),
`tools/wl_px.py` (patch colours in three shots).
