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
