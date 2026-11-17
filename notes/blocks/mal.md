# mal: the fourteen copies of the ral cell in front of the MA pad drivers

## Status (2026-11-17 05:11, contributor session)

Placed (`trace/mal.txt`, 42 transistors: three per copy, as far as `ral_cell` is
traced). Depends on `trace/ral.txt` (`@requires ral`). Inputs, outputs and the force
taps' wiring are not drawn.

## Placement

`tools/findcell.py 14020 4265 14450 4525 --min 0.7 --region 2300,7800:3200,19000
--layer acid1b --cell ral_cell`: fourteen hits at 0.78-0.82, all turned 90 degrees about
(14235,4395), the first eleven also mirrored (`mx=14235`), the last three not. Centres
at x 2659-2661, y 8155, 8761, 9368, 9976, 10627, 11234, 12036, 12730, 13382, 15506,
16201, 17275, 17925, 18576 (tags m0-m13). Copy m0 checked by overlay in metal and the
clean shot at 1.45x and 3x (`cache/scratch/ral/m0.png`, `m0b.png`): the cell's middle
(VSS) rail lands on the vertical metal x 2600-2650, the top (VCC) rail on x 2780-2830,
the contacts on rings.

## Logic (as far as the cell is traced)

    ral_a_m#  <- input     pass transistor 16/26, gate ck_out    (all fourteen)
    ral_a_m#  <-> output   hold device 16/90, gate VSS
    ral_tf_m# -> VSS       pull-down 66/20, gate mal_frc_m#

**Each copy's strobe pad lands on `ck_out`'s left-edge trunk** (`trunks`: metal x
2500-2504, with "contact candidates about every 608 px (y 8360, 8965, 9573, 10181,
10831, 11440 ...): its taps into the left column, not looked at"). The copies' strobe
contacts are at y 8349, 8955, 9562, 10170, 10821, 11428, 12230, 12924, 13576, 15700,
16395, 17081, 17731, 18382, i.e. those taps. So, if the cell is the latch it is believed
to be (`notes/blocks/ral.md`), **every MA output is latched, transparent while
`ck_out` is high (CLK low)**, where the RA outputs are latched on `ral_stb`.
Believed, not extracted: the cell's forward path is not traced.

## Ports

| Name | Layer | Where | Direction | What |
|---|---|---|---|---|
| `ck_out` | metal | the trunk x 2500, contacts as above | in | strobe |
| input end of each pass transistor | diffusion | x about 2567, below each strobe contact | in | unnamed: the MA counter's (or start address's) bit, not followed |
| output of each hold device | poly | x about 2567, above | out | unnamed: believed the `maN_drv_in` line, not followed |
| `mal_frc_m0` ... `mal_frc_m13` | metal | pads at x 2728-2730 | in | force pull-down gates; each a pad of its own here |

## Not done

1. Each copy's input and output: which counter row feeds it and which MA pad driver it
   feeds (that also fixes the bit order m# -> MA#).
2. Where the force taps `mal_frc_m#` go.
3. Everything `ral` has not traced inside the cell.
