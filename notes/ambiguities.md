# Ambiguity register

Each entry: where, what is unclear, the candidate readings, the working assumption (if
any) and what would settle it. Status is open, assumed or resolved.

## AMB-001  Structure of the RES/LPSTB input buffers  (open)

Where: 6950-8000 x 1640-2060, two identical cells.

Each cell has a small inverter (driver gate fed from a pad through the vertical metal
at x 7380, load block at 7304-7370 x 1942-1996) followed by a large two-finger
transistor (diffusion 7080-7234 x 1790-1986) and a second wide poly block at
7025-7060 x 1897-1965. Both stages sit between two wide rails (y 1834-1886 and
y 2004-2052) and much of the detail is under the upper rail.

Unclear: how the second block and the two-finger transistor connect near
7025-7110 x 1830-2000, and therefore which rail is VCC and which VSS here. One reading
has the box at 7040-7070 x 1837-1867 as a buried contact tying the output diffusion to
the poly that leaves through the contact at 7076,1684; the other has it as a metal
contact to the upper rail.

To settle: trace both rails back to the VSS and VCC pads (M1), then re-read the cell
knowing which is which. Not needed for anything else yet.

## AMB-002  Depletion implant visibility  (open)

Loads are identified by topology (gate tied to source through a buried contact, other
end on the supply). Whether the implant outline is visible in either shot is not yet
known. Matters for transistors that are depletion-mode without being wired as loads
(for example always-on pass devices), which topology alone would miss.

To settle: compare known loads against known pull-downs at 4-5x in both shots for any
consistent outline or tint.

## AMB-003  Data pad cell: layers under the VCC band  (open)

Where: D0 master, 17900-18380 x 7150-7560 (and the same place in D1-D7).

The pre-driver logic lies under the VCC band. Etch residue hides it in every single
instance; the median composite shows all the edges but not which layer each belongs
to. Two poly lines come in from the bus-interface side (P_x at y 7399-7422, P_y at
y 7465-7492), there are two load blocks either side of three VCC contacts at
y 7292, and a five-row multi-finger structure (rows G-K, x 18230-18660) to the right.
Details and what is established: notes/blocks/pads.md.

Candidate readings differ on whether the strips between rows G-J are one spiral gate
fed from P_y, and on what the three-contact row K is for.

To settle: trace the logic that drives P_x and P_y (M2). Knowing whether they are
data and enable, and their polarity, should leave one consistent reading. A tri-state
pair needs both output gates low when disabled, which is a strong constraint.

## AMB-004  L-shaped poly on the input inverters  (assumed)

Where: 14626-14689 x 18286-18375 on the R/W group, and the same place in the RS and
CS groups (+628, +1256).

The input gate poly of the first inverter of each group continues past its diffusion
into an L that runs up beside the load and ends. It crosses no diffusion that I can
see, so it does nothing electrically as traced. It abuts the gate with no gap, so it
is drawn as part of the input net.

To settle: nothing needed unless a diffusion turns up under it. Worth a second look
if the input stage ever fails to simulate as a plain inverter.

## AMB-005  Input protection cells: gate of the clamp, and the comb  (open)

Where: master 14667-15131 x 18943-19219 (R/W); also CLK, E, RS, CS cells.

The clamp is a 424/40 transistor from the input node to the rail at y 18950-18998.
Its gate poly forms a ring round the node and no contact or buried contact to it is
visible, so what it is tied to is unknown (ground is usual for such a clamp). The
rail itself is taken to be VSS but has not been followed to the ring. Under the VCC
band, below the node, there is a comb of ten small U-shaped features whose layer and
purpose are not worked out.

None of this affects logic: with any normal tie the clamp is off in operation. To
settle: follow the rail to a supply, and look for the gate tie in the composite at
14660-14710 x 19020-19080.
