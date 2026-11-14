# Data bus interface column (`dbus`)

Region: x 17050-17700, y 5300-17000, and the D0-D7 pad cells to its right.
Trace: `trace/dbus.txt`. Scratch tools: `tools/dbus_mosaic.py` (same rectangle at
several offsets side by side), `tools/dbus_autocorr.py` (vertical pitch of a strip).

## Status

Traced and extracting: the input buffer chain (four inverters) of D0, as a cell.
Located, not yet instanced: the same chain for D1-D5. Surveyed only: everything else.
The pad cell (AMB-003) has not been touched yet.

## Inventory

The column is NOT one unit per pad at the pad pitch. Logic occupies y 8030-16600 only
(between y 5900 and 8030 there is nothing but three metal lines from the D0 pad cell
and the rails). Gates sit on a 152 px vertical pitch between two rails:

- VSS rail, metal, x 17355-17400 (pull-down diffusions under it; joins a wide trunk at
  y 6620-6720 further up).
- VCC rail, metal, x 17527-17585, top end at y 8287 (load contacts on it).
- Loads between them at x 17420-17520; gate outputs leave to the left in poly.

| What | Where | Notes |
|---|---|---|
| Input chain, D0 | 17255-17590 x 8280-8880 | cell `dbus_in`, traced |
| Input chain, D1-D5 | same cell at dy 1365, 2732, 4098, 5465, 6223 (dx 1, 1, 2, 2, 2) | findcell on acid1b, scores 0.81-0.83; the four-gate core is identical in all six (compared side by side at 0.9x); the wiring left of x 17290 differs per copy |
| Gate group below each of chains 0-3 ("cluster") | 17150-17590 x 8890-9520, repeats at +1366 three more times | about four gate pitches of denser logic with five vertical metal lines; NOT traced. Chains 4 and 5 have no such group directly below them (chain 5 starts 758 px below chain 4) |
| Two poly cross-unders between units | y 9545-9565 and 9590-9612 (unit 0/1 boundary) | upper one: D1 pad input on its way to chain 1 (contact 17293,9555, metal jumper to 17293,9640). Lower one: D1's P_y, from a contact at 17120,9620 on a metal line that comes up from below |
| Other logic | 17150-17590 x 15100-16600 | single gates on the 152 pitch, not surveyed in detail |
| Logic above D0 | 17200-17700 x 5250-5900 | several gates, not looked at |
| Capacitor rectangles | 16960-17040 x 8445-8580 and x 8745-8880 (chain 0) | plain diffusion, one metal contact each |

No copy of the chain was found for D6 and D7 inside the column (findcell, both the
metal and the clean shot). Where their input buffers are is not known.

## Logic

### Input chain `dbus_in` (traced)

Four inverters in series, exactly the arrangement of the R/W, RS and CS input buffers
in the bottom row (`rw_a`..`rw_d`):

    d0_a = NOT d0_in      (G1, y 8287-8425)
    d0_b = NOT d0_a       (G2, y 8436-8568)
    d0_c = NOT d0_b       (G3, y 8588-8720)
    d0_d = NOT d0_c       (G4, y 8742-8870)

`d0_in` is the line from the D0 pad cell (see Ports). `d0_b` and `d0_c` each run left
in poly to a metal contact next to a plain diffusion rectangle (the same "added
capacitance" rectangles as in the bottom row). For chain 0 the strap from `d0_c`'s
contact (17078,8795) to its rectangle's contact (16990,8787) is there; the strap for
`d0_b` (contacts at 17078,8490 and 16988,8468) is absent in both metal shots, each
contact carrying only a dot of metal. So only `d0_d`, the pad level delayed by four
inverters, feeds logic: it leaves G4 in poly to a contact at 17205,8837 and goes down
in metal (x 17198-17218, "M_a") into the gate group below, ending at a contact at
17207,9255.

G1's gate poly continues into an L (17413-17503 x 8292-8318) that crosses no
diffusion and ends beside the load, as on the bottom-row input inverters (AMB-004).

Believed, not traced: the gate group below each chain gates `dN_d` onto the internal
bus (write) and makes the pad driver's data line (read).

## Ports

| Name | Layer | Where | Direction | What |
|---|---|---|---|---|
| `d0_in` | metal, x 17548-17566 | comes down from the D0 pad cell (contact near 17546,6755), turns left at y 8188 | in | D0 pad through its protection structure |
| D0 `P_y` | metal, x 17590-17610, then poly y 8090-8105, then metal x 17438-17458 ("thin metal") down through unit 0 | contact 17597,8097; contact 17510,8097 | out (believed) | per-bit line to the D0 pad cell; where it is driven is not traced |
| `P_x` | metal, x 17633-17650 | contact 17625,7380 (D0 cell) and contact 17640,9115 (D1 cell) on the same vertical line | out (believed) | **common to the pad cells** (seen for D0 and D1): an enable, not a per-bit line |
| D1 pad input | poly | from contact 17822,8400 left along y 8400 to x 17600, down in poly x 17597-17612 to the cross-under at y 9555 | in | to chain 1 |
| D1 `P_y` | poly | y 9225-9240 from the pad cell to x 17650, down x 17642-17660 to the cross-under at y 9600, to contact 17120,9620 | out (believed) | |

Internal data bus lines towards the core: not yet identified. The two poly lines
leaving chain 0 to the left at y 8532 and y 8792 are NOT bus lines; they end at the
capacitor contacts.

## Ambiguities

- `d0_b` capacitor: contacts cut, strap absent. Looks like a metal-mask option. Does
  not affect logic.

## Not done

- Chains 1-5: instance the cell and trace each copy's left-hand wiring (it differs).
- The gate groups ("clusters") at y 8890-9520 + n x 1366, n = 0..3.
- Logic at y 15100-16600 and at y 5250-5900.
- All channel wiring between the column and the pad cells (x 17590-17830).
- Pad cell (AMB-003).
