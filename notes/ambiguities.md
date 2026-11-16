# Ambiguity register

Each entry: where, what is unclear, the candidate readings, the working assumption (if
any) and what would settle it. Status is open, assumed or resolved.

## AMB-001  Structure of the RES/LPSTB input buffers  (resolved)

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

Resolved: the large two-finger transistor with its load is the same cell as the
second stage of the CLK and E buffers, flipped top to bottom (found by template
matching, confirmed by overlay). That fixes the upper rail as ground and the lower
as supply. The first stage is a small inverter whose gate wraps round a pocket of
diffusion. Each cell is a non-inverting two-stage buffer. Traced in
trace/pads_in_top.txt; left cell is LPSTB, right cell is RES.

## AMB-002  Depletion implant visibility  (open)

Loads are identified by topology (gate tied to source through a buried contact, other
end on the supply). Whether the implant outline is visible in either shot is not yet
known. Matters for transistors that are depletion-mode without being wired as loads
(for example always-on pass devices), which topology alone would miss.

To settle: compare known loads against known pull-downs at 4-5x in both shots for any
consistent outline or tint.

2026-11-15: this now matters in a concrete place. The static register cell of the
central datapath (`cdp1_reg`, notes/blocks/cdp1.md) holds its value through a long
transistor whose gate is grounded; the cell only works if that device is
depletion-mode. So there are depletion devices that are not wired as loads, and
topology alone will not find them all. Any transistor whose gate is tied to VSS or to
its own source should be listed as a probable depletion device.

## AMB-003  Data pad cell  (open, narrowed)

Where: D0 master, 17780-18760 x 7150-7560 (and the same place in D1-D7).

The output fingers and their two gate nets are understood. The logic that makes
those gate nets from the two lines that arrive from the bus interface is not. The
clean shot of chip 1 settled which shapes under the VCC band are poly, and showed
that the cell contains more than two inverters: at least one transistor gated by the
second line sits in series with the pull-up gate net, the first line is tied to a
diffusion row deep in the cell, and two large closed shapes under the band are of
unknown kind. Everything established, with coordinates, is in
notes/blocks/pads.md.

To settle: trace the bus-interface logic that drives the two lines (M2), so that
their meaning and polarity are known; then finish the cell from 4x views of the
clean shot, starting with the buried contact at 17835-17858 x 7440-7460 and the left
end of row H's metal. A tri-state pair needs both output gates low when disabled,
which is a strong check on any reading.

## AMB-004  L-shaped poly on the input inverters  (assumed)

Where: 14626-14689 x 18286-18375 on the R/W group, and the same place in the RS and
CS groups (+628, +1256).

The input gate poly of the first inverter of each group continues past its diffusion
into an L that runs up beside the load and ends. It crosses no diffusion that I can
see, so it does nothing electrically as traced. It abuts the gate with no gap, so it
is drawn as part of the input net.

To settle: nothing needed unless a diffusion turns up under it. Worth a second look
if the input stage ever fails to simulate as a plain inverter.

## AMB-005  Input protection cells: gate of the clamp, and the comb  (assumed)

Where: master 14667-15131 x 18943-19219 (R/W); also CLK, E, RS, CS cells.

The clamp is a 424/40 transistor from the input node to the rail at y 18950-18998.
Its gate poly forms a ring round the node and no contact or buried contact to it is
visible, so what it is tied to is unknown (ground is usual for such a clamp). The
rail itself is taken to be VSS but has not been followed to the ring. Under the VCC
band, below the node, there is a comb of ten small U-shaped features whose layer and
purpose are not worked out.

None of this affects logic: with any normal tie the clamp is off in operation.

Update, from 4x composite views of the comb and the right-hand end: the pad's strip
is poly and joins the frame at 15015-15035 x 19215-19262; the frame's right arm
feeds a thin spine at y 19128-19140, and the ten U shapes hang from that spine over
the lower edge of the node diffusion. Working assumption: the U shapes are buried
contacts, so pad poly, frame, gate band and node are one net, and the band over
y 19029-19070 is a thick-oxide clamp to the rail (gate on its own drain). This is
the textbook arrangement and it gives the pad net a junction to the substrate, which
a poly-only path would lack. Still to do: follow the rail to a supply.

Checked against the clean shot of chip 1: the frame is a poly plate
(14670-15130 x 19125-19215) with ten finger-shaped slots; ten fingers of the node
diffusion reach down into the slots. The band above the node is poly with no metal
over it. Nothing contradicts the working assumption; the trace still draws the comb
as a single strip.

## AMB-006  Island devices in the clock block wiring  (assumed: clamps)

Where: B1 12385-12447 x 18885-18975, B2 12563-12627 (same y), B3 12738-12802 (same y),
T1 12380-12456 x 19132-19202, T2 12380-12456 x 19302-19372, BI 12432-12497 x 19636-19726.

Each is a diffusion strip from VCC that passes under a poly gate and ends in a short
stub with one metal contact. A small metal pad, connected to nothing else, covers the
stub contact and the gate. The gate poly is on a signal net: B1 on `ck_n2`, B2 on
buffered CLK (`clk_b`), B3 on the CLK pin node (`clk_p`), T1 and T2 on line B, BI on
`ck_n1`. W/L is about 55/27 for T1/T2 and 52/22 for B1-B3.

Unclear:
1. How gate and stub are tied. An isolated pad is only useful if it joins them, but
   no separate poly contact is resolved; a buried contact at the poly edge would do
   the same job and then the pad would be redundant. Drawn as a buried contact,
   flagged.
2. What they are for. Gate tied to the stub with the far side on VCC is a pull-up if
   the device is depletion-mode, or a clamp to VCC + Vt if it is enhancement-mode.
   The implant is not visible (AMB-002). A pull-up on the CLK pin node would break
   the datasheet's input leakage figure, which argues for a clamp at least for B3.
   `ck_n1` and `ck_n2` so far have no other pull-up, which argues for pull-ups there.
3. Whether T2's gate line really joins line B's poly at 12288,19262. The strip is
   clearly poly from y 19285 down; its top end is not resolved. The alternative is a
   dead end, which makes no sense.

Effect on logic: none for `clk_p` and `clk_b` (both are driven anyway). For `ck_n1`,
`ck_n2` and line B it decides whether the nets have a static pull-up.

Update: `ck_n1` is the output of gate 2 and `ck_n2` the output of gate 4 in the gate
row, so every island sits on a net that already has an inverter's depletion load,
except B3, which sits on the CLK pin node (the pin, after its series resistor: see
AMB-005). A pull-up is therefore needed nowhere and is ruled out on the pin by the
leakage figure. Working assumption: all six are enhancement devices used as clamps
to VCC + Vt, on the nets that drive the bootstrapped driver logic. Marked
kind=clamp, which leaves them out of logic recovery.

Checked against the clean shot of chip 1: no buried contact at any of the six. Each
is a plain gate over the strip, with the stub's metal contact showing as a speck and
nothing visible on the gate. So if gate and stub are tied, it is by the metal pad
contacting both, and a contact onto poly leaves no speck to see. The tie is still
unproven. The nets involved are now known to be the clock phases, their delayed
copies and CLK, where overshoot above VCC from the wide drivers is plausible, which
suits a clamp.

## AMB-007  Clock driver logic  (mostly resolved)

Where: 10900-12000 x 19140-19890.

Resolved 2026-11-15 from the clean shot of chip 1: the block is the two-phase
non-overlapping clock generator (notes/blocks/clock.md). Its logic is traced and
extracts as two cross-coupled NORs.

Still open, neither affecting the logic:
1. A box at 10938-11003 x 19632-19668 on the left pull-up's gate, where the poly
   widens from x 10966-10992 to x 10950-10992 (mirror image at 11870-11936). It
   looks exactly like a buried-contact window in all five shots. A buried contact
   there would tie the gate to the diffusion on both sides, that is the VCC side and
   the output together, which cannot be. Candidate readings: (a) not a buried
   contact but some other mask feature; (b) a buried contact to the output side
   only, making the "pull-up" a large depletion load with its gate on its source
   and the whole half one ratioed NOR. Reading (b) gives the same logic. The trace
   leaves the box out and treats the gate as driven by the small NOR.
2. Whether the wide pull-ups are enhancement or depletion devices.

To settle: a delayered shot (poly removed), or measuring the phase lines' high level
on a real chip.

## AMB-008: the pull-down line L3 of counter rows r4-r10 seemed to have no feed (resolved 2026-11-15)

Where: mid-right array, thin metal line L3, piece y 9440-13018.

It looked cut at both ends with no contact. At 6.5x in all four shots its lower end widens
into a foot that turns west onto the contact (12567,13005), which had been given to the
neighbouring line L2. Feed: a metal line from the west along y 13005, contact
(11765,13005), poly east, that contact. Lesson: a line that ends in a widened foot ends on
something; look at the foot at 6x before calling it free.

For the 8-bit counter L3 is `ck_a` (poly followed in the clean shot to clock.txt's bus
line), so there it is a clock phase, not a clear. What the L3 lines of the row counter
(from the west along y 13005) and of the 4-bit counter (north) carry is open until their
sources are traced.

## AMB-009: the top of the column at (3045,4515) in the step logic cluster: buried contact or VSS? (2026-11-17)

**Where.** `trace/tla.txt`, the column x 3028-3063 above gate E0. A poly band (gate
`clk_tl`, y 4535-4558) crosses the column between the node `rcs_cond` and the column's
top end (y 4512-4532). Directly above that end sits the poly pad (3024-3066, 4455-4522) at
the bottom of the metal `rcs_cond_lat`.

**Reading adopted (drawn `?B`).** The pad overlaps the column top and is tied to it by a
buried contact: the band is a pass transistor, and `rcs_cond_lat` is a dynamic latch that
takes `rcs_cond` while `clk_tl` is high. Evidence: the pad's lower edge is a much
heavier dark band than its other edges (clean shot, 5.8x); the pad has no other poly
leaving it, so without the tie the metal would end on nothing; and the circuit makes
sense.

**Other reading.** The column top joins the VSS box under the rail to its west (the class
map shows diffusion on both sides of the rail's edge at y 4515-4530, with two dark lines at
x 2998 and x 3018 between them that could be the rail's etch boundary rather than edges),
and a 5 px strip between pad and column measures as field (green; it lies in the margin
of the metal's end, so it may be an artefact). Then the band would be a second pull-down:
`rcs_cond` = NOR(`clk_tl`, `rcs_cond_n`), and the unit above,
NOT(`rcs_cond` AND `clk_tl` OR `rcs_g4240`), would reduce to NOT `rcs_g4240`: a gate
with a term that can never be true. That is why this reading was not adopted.

**To settle it.** Simulation will not distinguish them easily; find where `rcs_cond_lat`'s
other end goes (poly west along y 4010-4030 from the pad at (3040,4028)): a latch node must
end on a gate.

## AMB-010: is the strip S1 of the row address selector tied to the metal that crosses it at (7207,4955)? (2026-11-18)

`notes/blocks/ras.md`. The metal of `ras_o0_alt2` comes down x 7207 over the left end of
the poly strip S1 (gate `ras_o0_sel2`, y 4945-4970) and ends 45 px further on the contact
(7205,5000) of the diffusion below the strip.

- For a contact: a dark pit at (7207,4955) in the chip-2 stripped shot, and the strip's
  left end is wide enough for one.
- Against: no ring in either metal shot (the contact 45 px below has a plain one); the
  bright spots on the metal there are the stretches between the edge lines of the strip
  and of the diffusion finger above it.

**Adopted: no contact** (assumption). Then S1 is a third pass transistor into `ras_o0`,
gated by a poly that arrives from the north along x 7427. With a contact, gate and source
of S1 would be one net and the device a diode from `ras_o0_alt2` to `ras_o0`. Settle by
tracing `ras_o0_sel2` north and `ras_o0_alt2` north-west: if they turn out to be one net
anyway, the question is moot.

## AMB-011: the units east of the row address selector are taken to be inverters (2026-11-19)

`notes/blocks/rax.md`, "Assumptions". Drawn: one pull-down per unit, gate = selector
output, from VSS to the node that leaves on the unit's second pad (`rax_o#`). Not
traced: the load. Four readings carry the conclusion `rax_o#` = NOT `ras_o#`: one
diffusion under two metals with an unreadable gap between; no contact where the thin
metal x 7902 crosses the output's box; a buried contact at the pad poly's end; a load
somewhere east. **Adopted** because the result is the complement that the central
datapath's comparator needs, found independently. Settle by tracing the unit's east
half and the thin metal's two end pads.

## AMB-012: the units that make R9's compare value are taken to be inverters under a VSS rail (2026-11-20)

`notes/blocks/r9c.md`, "Assumptions". Drawn: one pull-down per unit from the output to
the rail x 17440-17495, gate = an RA pad driver's input line. Not established: that the
rail is VSS (not followed to a labelled rail) and that the unit has a load. If the rail
were VCC the device would be a pull-up and `ra#_cmp` would follow `ra#_drv_in` instead of
inverting it. **Adopted: VSS and a load**, by the layout rule (gates under the ground
rail, load towards the other rail). Settle by tracing a unit's east half and following
either rail to a labelled one.

## AMB-013: does R9's match line end on the step logic's input `rcs_bq3335`? (2026-11-21)

`notes/blocks/r9m.md`. R9's match (`cdp1_b_eq`) was followed 9,000 px from the comparator
to the middle cluster of the row counter's step logic. Its last metal comes down x 4192
from y 2598 and ends at y 3385 with a 25 px stub west (y 3368-3385, to x 4168). Twelve
pixels further west is the metal x 4148 that ends on the contact (4148,3335) of
`rcs_bq3335` (`trace/tla.txt`), and that metal is itself the end of **another** line of
the same four-line bundle (the one that is at y 2598 at x 4760).

- Reading A: the stub joins the metal x 4148 (the 12 px dark line between them is the
  edge of the poly pad underneath printing through). Then two lines of the bundle are one
  net, `rcs_bq3335`, which makes sense only if their two drivers are meant to be tied
  (a wired AND of two gate outputs), and `rcs_in1` = that AND, gated by `rcs_mv`.
- Reading B: the stub ends on a contact of its own that neither metal shot shows, and
  R9's match goes somewhere not found.

Both metal shots at 5x (`cache/scratch/rax/eq9.png`) and a profile (`--half 1`: metal at
x 4149-4157 and 4169-4196 on y 3376) do not decide it. **Not adopted either way; nothing
drawn.** Settle by tracing the other line (poly y 2595 at x 5400) to its driver: if that
is a second comparator's match, reading A is the design.

## AMB-014: the gate group that makes `fld_a_in` and `fld_y_b` (2026-11-23)

`notes/blocks/fld.md`, last traced section. Three pull-downs under the rail x 6505-6560 are
drawn from a class map and 3.6-4.6x views in both stripped shots. Not established: that
the rail is VSS; the loads; the two buried contacts (`?B`) that put the two output lines
on their nodes; that the node above the series pair is separate from the rail contact
at y 3905; that the dark spot (6548,4188) is not a contact (if it were, `fld_y_b`'s node
would sit on the rail). **Adopted** as drawn: `fld_a_in` = NAND(`tcw_a`, `tcw_b`),
`fld_y_b` = NOT `tcw_c`. Settle when the region west of the island is traced as a block.

## AMB-015: three joins on the east side of the gate column's middle stretch (2026-11-26)

`notes/blocks/tcw.md`, "Stretch B, east side". All three are in the trace as `?` items:

1. **The two output nodes at y 3326 and y 3437 are one** (`tcw_o3326`, alias
   `tcw_o3437`): a 24 px strip x 6588-6612 between their arms. Evidence: an outlined band
   there in both metal shots; in the chip-2 stripped shot it is plain tan (that shot's
   diffusion colour) while the two gate-poly ends beside it are orange; in the chip-1
   fringed shot khaki. Against: the clean shot's class map gives the neighbouring strip
   (x 6582-6598) as field with a line of poly on its west side, which would instead join
   the two gates' east ends (and with them two bus metals); the two readings differ by
   one strip's width, at the resolution limit.
2. **The inverter at y 3519 has a load** whose gate (block (6625-6680, 3540-3570)) is tied
   to the output at its west end. The block and the arm under it are plain; the tie is
   placed by analogy with the gate above.
3. **Its output leaves on the bus metal `tcw_m6362b`**: the node's west end meets the end
   of the poly from the pad (6385,3567). Both ends are seen (class map); the buried
   contact is not.

**Adopted as drawn.** With them: `tcw_o3550` = NOT `tcw_m6232`, and it is the middle gate
of the first stack. Settle 1 with a profile across the strip in the chip-2 shots at
several y, and by finding the load of `tcw_o3326` (one load or two decides it).

Profile done the same day (sum of red minus green over the two chip-2 shots, 4 px
steps, x 6556-6626, at y 3345, 3365, 3380, 3395, 3415, 3440): the strip x 6594-6602 reads
as diffusion at every height; the space between the two gates' east ends (x 6572-6576,
y 3365-3395) reads as **field**, so the gates are not joined to each other (the
alternative reading is out). Still open: at y 3440 a dark line (x 6580-6588) lies between
the lower arm and the strip, and a dark line cannot show whether two regions meet. So
item 1 stands as "a diffusion strip runs between the two arms; that it joins them is
assumed".

