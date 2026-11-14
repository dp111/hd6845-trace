# Pad cells

## Output driver (`outdrv`, trace/pads_out.txt): done

23 instances: MA0-13, RA0-4, HSYNC, VSYNC, DISPTMG, CUDISP. Master is MA3.

- Pre-driver: two inverters in series under the inner VCC band. Input is a poly line
  from the core (`<pin>_drv_in`), first inverter output `<pin>_pu`, second `<pin>_pd`.
- Output pair: three pull-up fingers from VCC gated by `_pu`, three pull-down fingers
  to VSS gated by `_pd`. So the pad is the inverse of `_drv_in`.
- The pre-driver's ground reaches it through a wide diffusion tunnel under the pad
  neck (752-1027 x 3428-3568 on the master), because the VSS ring is on the far side
  of the pad from the core.
- The bond pads themselves are not in the cell: each pad sits differently relative to
  its driver. Only MA3's pad is drawn so far.

## Input pads

Bottom right (trace/inprot.txt, trace/inrow.txt):

| Pin | Path | Core-side nets |
|---|---|---|
| CLK | protection cell 1, then three-finger inverter, then two-finger inverter | `clk_n` = NOT clk, `clk_b` = clk buffered; `clk_b` leaves left along y 19070 |
| R/W | protection cell 2, then four inverters in a chain | `rw_a` = NOT rw, `rw_b` = rw, `rw_c` = NOT rw, `rw_d` = rw |
| E | protection cell 3, then three-finger and two-finger inverters | `e_n`, `e_b`; `e_b` goes up to the core in a wide poly line at x 16660-16705 |
| RS | protection cell 4, then four inverters | `rs_a` .. `rs_d` |
| CS | protection cell 5, then four inverters | `cs_a` .. `cs_d` |

In each four-inverter group the b and c outputs also connect to a large plain
diffusion rectangle (about 130 x 220 px), which looks like added capacitance.
One further inverter at the left end of the row (input from the core in poly,
output leaving left along y 18775) is not yet identified.

Top (trace/pads_in_top.txt):

| Pin | Path | Core-side net |
|---|---|---|
| LPSTB | left comb cell at 6380-6650 x 833-1280, then small inverter and two-finger inverter | `lpstb_b` = pin level, on the wire at y 1686 |
| RES | strip from the contact at 7880,1315, right comb cell, then the same two stages | `res_b` = pin level, on the wire at y 1730 |

Not yet drawn: the strips from the pads to the protection cells and from those to
the buffers, the two top comb cells, and the wiring below the buffer row.

## Data pad (D0-D7): in progress

Eight instances at dy = 0, 1735, 3470, 5054, 6637, 8242, 9847, 11452 from D0 (D0 at
the top, D7 at the bottom). Master rectangle 17600,5950:19200,7600. A median composite
of the eight (`tools/composite.py dpad ...`, view with `--comp dpad`) removes the etch
residue that hides the logic under the VCC band; raw metal of a clean instance
(`--shift 1,5054` for D3) shows where metal really is.

Read so far (D0 coordinates), all still to be confirmed by trace and extraction:

- Main fingers, top to bottom: A VCC (y 6757), B pad (6833), C VSS (6908), D pad
  (6983), E VCC (7058), F pad (7135). Gates between them at 6798, 6870, 6947, 7020,
  7097. A and E run on under the VCC band (x 17900-18200); C leaves to the right to
  the VSS ring.
- Right group below F (x 18740-19050): rows G' VSS (7215), H' pad (7290), I' VSS
  (7365), enclosed by one poly frame (strips at 7180, 7250, 7325). More pull-down
  fingers. The frame is fed from a poly bar at x 18684-18740 through three contacts
  on a metal column that comes from row I of the left group.
- Left group below F (x 18230-18660): rows G (7200), H (7275), I (7350), J (7425) and
  a three-contact row K (7517), with gate strips between them (T1 7237, 7312, 7386)
  joined into one spiral, and a separate strip P_y (7478) between J and K. Row G and
  row K are joined by a vertical metal at x 18228-18246.
- Left of the VCC band two metal straps collect the gate ends: S1 (x 17862-17883)
  takes the gates at 6798, 7020, 7097 and 7170, and S2 (x 17804-17825) the gates at
  6870 and 6947. So S1 is the pull-up gate net and S2 the pull-down gate net.
- Under the VCC band: three VCC contacts at (17977-18057, 7292) with a load block
  above (U', y 7225-7266) and below (L', y 7316-7359). Two poly lines enter from the
  bus-interface side: P_x (y 7399-7422, turning up at x 18170) and P_y (y 7465-7492).

Established since:
- The metal over row K's three contacts is an extension of the VCC band (a strip at
  y 7465-7495 joins them), so row K and row G are VCC rows and the gate at 7170 is a
  fourth pull-up finger, consistent with it being on S1.
- Rows C and I' both leave to the right on bars that reach the outer ring
  (y 6882-6944 and y 7312-7388), so both are VSS and the frame gates are pull-downs.
- Row J's wide bar (x 18272-18812, y 7400-7448) most likely joins row I' (VSS).

Not resolved (AMB-003): which shapes under the VCC band are poly and which are
diffusion, hence what P_x and P_y gate, and how the left group (rows G-K) is wired.
Parked until the bus-interface logic that drives P_x and P_y is traced.
