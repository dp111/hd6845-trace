# cdp1: central datapath, top rows (x 7600-10850, y 2950-5700)

## Status

Rows A and C (two rows of the same static register cell, 6 and 5 bits) are traced,
instanced, checked instance by instance and extract cleanly. Row B (between them),
rows D and E, the wiring channels and the per-slice bit lines are surveyed only
(see Inventory and Not done). The area left of x 8340 was not touched: it is random
logic and overlaps the queued packages `tc1`/`tc2`.

## Inventory

The array is **not eight slices wide here**. In this region it has six slice positions
at a pitch of 390 px, `s0`..`s5`, left edges at x 8380, 8770, 9160, 9550, 9940, 10330
(the wide VSS rail of each slice). Only row A uses s0; every other row uses s1..s5.
Slices are numbered by position; no bit order is established yet (see Not done).

| Row | y | Slices | What it looks like | State |
|---|---|---|---|---|
| top wiring | 2950-3040 | - | VSS band and feeds, the q outputs of row A leaving upward | traced (to y 2950) |
| A | 3040-3330 | s0-s5 (6) | register cell `cdp1_reg` | traced |
| below A | 3330-3420 | all | two horizontal poly lines y 3340-3360 and 3385-3405 running the full width, contacts at 10655,3345 and 10615,3385 | not traced |
| B | 3440-3990 | s1-s5 (5) | comparator slice (believed): pull-down on a row-long NOR line plus about eight transistors; input pad at its foot (9113,3958) fed by row C's q | surveyed, see Logic |
| channel B/C | 3990-4230 | all | five horizontal poly lines (y about 4003, 4047, 4090, 4133, 4177) crossed by thin vertical metal lines with contacts (9310,4130; 9617,4085; 9703,4085; 10093,4040; 10483,4000) | not traced |
| C | 4232-4524 | s1-s5 (5) | `cdp1_reg` again (dy = 1194) | traced |
| channel | 4530-5150 | all | about 15 horizontal metal lines, the rails crossing over/under | not traced |
| D | 5150-5370 | s1-s5 (5) | small cells under a horizontal poly line | not traced |
| E | 5380-5700 | s1-s5 (5) | larger cells; may run past y 5700 | not traced |

Per slice, vertical metal: VSS rail (52 px wide, left edge of the slice), bit line
(20 px, 62 px right of the rail centre), VCC rail (50 px, 214 px right of the VSS
rail centre). Slice s5 has one more VSS rail on its right at x 10711-10765, and a thin
vertical metal line runs at x 10795-10820 right of that (seen at y 4224-4544, not
followed).

Left of x 8750 between y 3440 and 5700 (slice-0 position below row A) and everything
left of x 8340 is random logic, not part of the array.

## Logic

### `cdp1_reg`: static register bit (traced; rows A and C)

Master: row A, slice 1, x 8745-9225, y 3040-3330. Six transistors:

| | Gate | Between | W/L | What |
|---|---|---|---|---|
| pass | row write line `wr` | bit line `bl` and `x` | 36/23 | write (and the only access to the cell) |
| pull-down 1 | `x` | `q1` and VSS | 55/27 | |
| load 1 | `q1` | VCC and `q1` | 27/58 | depletion load |
| pull-down 2 | `q1` | `q` and VSS | 61/23 | shares the next slice's VSS diffusion |
| load 2 | `q` | VCC and `q` | 30/70 | depletion load |
| feedback | **VSS** | `q` and `x` | 25/82 | long, narrow, gate grounded |

    q1 = NOT x          q = NOT q1 = x
    x  = bl while wr is high; otherwise held from q through the feedback transistor

The feedback device has its gate tied to VSS through a poly line that does nothing
else, so it must be a depletion transistor used as a resistor (an enhancement device
there would never conduct and the poly line would be pointless). *Believed, not
visible*: the implant cannot be seen. With it the cell is a static latch that the bit
line overpowers when `wr` is high.

`q` (true data, same sense as the bit line when written) is the only output: it leaves
the top of the cell in poly (`pt`). `q1` is used only inside the cell.

How the nodes are made (so the next reader can check): `x` is one poly piece (gate of
pull-down 1, an arm to a buried contact at 8898-8928 x 3097-3130 on the feedback
diffusion, and a tail to a buried contact at 8836-8872 x 3202-3230 on a small diffusion
island that is the pass transistor's upper side). `q1` is the diffusion right of the
gate (8868-8894 x 3133-3188), a narrow band along y 3152-3170 to the top of the load
strip at 8958-8985, a buried contact at 8896-8932 x 3174-3204 to the load's gate, and
that gate's poly running right along y 3150-3176 to the gate of pull-down 2
(9130-9153). `q` is the diffusion under m5's upper contact, m5, the big poly block
9028-9098 x 3185-3285 (load 2's gate), its buried contact at 9082-9112 x 3190-3224 and
the diffusion under m6 at 9104-9130.

### Row A (traced): 6-bit register, **believed R8** (interlace 2 bits, DISPTMG skew 2 bits, cursor skew 2 bits)

- Six cells `a0`..`a5`. Each `q` leaves upward on its own wire to the logic above and
  left of the array, not to a comparator: that and the width of six are the reasons for
  the R8 guess. Which cell is which bit is not known (bit lines not followed).
- `cdp1_a_wr` (believed: write strobe of this register) is one poly line that meanders
  through the cells; it starts under the VSS rail of slice 0 (8395-8445 x 3250-3322,
  no connection found there) and leaves to the right past x 10786 at y 3300-3322.

### Row C (traced): 5-bit register, function not known

- Five cells `c1`..`c5`. Each `q` goes up in metal from a poly pad at the top of the
  cell (9113+k*390, 4222) to a poly pad at the foot of row B (9113+k*390, 3958), i.e. it
  drives a gate in row B. Slice 5 differs: its metal goes left and up at x 10632.
- `cdp1_c_wr`: the same kind of meander, y 4494-4516.

### Row B (surveyed at 3-4x, NOT traced; coordinates for slice 2, add 390 per slice)

Read from `cdp1_sr.py` composites of slices 2-4; slice 1 and slice 5 differ (findcell
scores 0.74 and 0.82 against slice 2). What is established, and what is only believed:

- **A diffusion line runs along the whole row** at y 3505-3540 (it passes under every VSS
  rail; between x 9430 and 9560 it narrows to y 3510-3528, with a stub down x 9430-9448
  to y 3610). In each slice one wide transistor pulls it to VSS: gate = a poly arm
  y 3545-3568, x 9205-9420; VSS = the diffusion band y 3575-3606 below the arm, fed by
  the rail contact at 9183,3608. In slice 1 only, at x 8990-9135 y 3505-3640, a depletion
  load from the VCC contact at 9012,3605 (gate bar x 9070-9100, tie box at 9085,3520)
  pulls the line up. So the line is a **5-input NOR, load in slice 1**: believed the
  comparator's "all bits equal" output (high when no slice's gate is high). Where it
  leaves the row (left end at x 8790, right end past slice 5) was not followed.
- The pull-down's gate poly goes right, down the VCC-rail side (x 9397-9420), back left
  along y 3612-3632 (over field), and down at x 9238-9262 to a buried contact at
  9240-9262 x 3655-3680 (under the bit-line metal, which does **not** contact it: no pad,
  no ring) onto the diffusion of the lower half. Call that node `g`.
- Lower half (y 3650-3900), about eight transistors, believed to make
  `g` = (row C bit) XOR (a second input):
  - input 1: row C's `q`, poly up from the pad at 9503,3958, a vertical gate
    x 9523-9545, y 3690-3830, between the diffusion on its left (x 9500-9520) and a
    VSS strip under the next slice's rail (x 9550-9568);
  - input 2: a vertical metal line x 9325-9347 with two poly contacts, 9337,3668 and
    9337,3860. It comes up from channel B/C, where it is contacted to one horizontal
    poly line (see below). From the upper pad a poly arm y 3662-3695 runs right to a
    vertical gate x 9475-9498, y 3695-3772; from the lower pad a gate blob
    x 9265-9318, y 3845-3885;
  - VCC contact 9398,3757 on a diffusion 9350-9428 x 3732-3790; under the rail below it
    a poly block 9350-9428 x 3790-3840 (load gate, part of the horizontal poly
    y 3797-3823 that runs left to x 9190 as the gate of a pull-down between the
    diffusion 9185-9232 x 3700-3795 and the VSS diffusion below it, contact 9185,3870);
    a second load gate x 9430-9452, y 3795-3845 with its tie box 9450-9480 x 3820-3862;
  - two horizontal gates y 3703-3728 and y 3738-3768 over a diffusion column x 9270-9322.
  The exact series/parallel structure was not resolved; two honest passes at 4x left the
  diffusion outlines between x 9260-9330 and around 9430-9460 unclear.

### Channel B/C (surveyed)

Five horizontal poly lines, y about 4003, 4047, 4090, 4133, 4177, in segments. The
vertical metal line of each slice at x 8947+390k (row B's input 2) ends on a contact to
a different one: slice 2 at 9337,4130; slice 3 at 9716,4088; slice 4 near 10106,4045;
slice 5 near 10497,4003 (slice 1 not looked at). So five separate signals reach the five
comparator slices from the side: believed the bits of a 5-bit counter that lives
elsewhere. The lines are broken into segments and some segments are joined by short
poly hooks (one at x 9240-9255, y 4085-4135 joins the y 4090 and y 4133 lines), so the
routing must be traced, not assumed.

The bit lines of row A do not all continue as the bit lines of row C: slice 2's
(x 9247) jogs right at y 4035-4065 and goes on down at x 9287; slice 3's (x 9628)
ends on a contact to the y 4090 poly line at 9628,4088. Row A's register therefore
taps different bus bits from row C's in the same slice.

## Ports

| Name | Layer | Where it crosses | Dir | What |
|---|---|---|---|---|
| `vss` | M | feeds at 9140-9197, 9900-9987, 10711-10765 x y 2950 (from the plane under the VSS pad); band continues left at 8340, y 2987-3037 | in | supply |
| `vss` | M | rails x 8403, 8796, 9187, 9577, 9967, 10357, 10738 at y 4530 (drawn to there; they continue down) | - | |
| `vcc` | M | rails x 8620, 9010, 9400, 9790, 10180, 10570 at y 4530 (drawn to there; they continue down; top end is in row A) | in | supply, from below |
| `cdp1_a0_q` | P | 8340,3024 going left | out | row A bit, slice 0 |
| `cdp1_a1_q` | P | 8340,2985 going left | out | row A bit, slice 1 |
| `cdp1_a2_q` | M | 9507,2950 (turns left at y 2940 just above) | out | row A bit, slice 2 |
| `cdp1_a3_q` | P | 9872,2950 (pad with metal contact at 9865,2940 just above) | out | row A bit, slice 3 |
| `cdp1_a4_q` | M | 10275,2950 going up | out | row A bit, slice 4 |
| `cdp1_a5_q` | P | 10665,2950 (pad with metal contact at 10655,2940 just above) | out | row A bit, slice 5 |
| `cdp1_a_wr` | P | 10786,3311 going right (not followed further) | in | row A write line |
| `cdp1_c_wr` | P | 10786,4505 going right; left end not looked at | in | row C write line |
| `cdp1_aN_bl` | M | 8857+k*390, 3330 going down (k = -1..4 for a0..a5) | in/out | bit lines of row A; continue down through row B, not followed |
| `cdp1_cN_bl` | M | 8857+k*390, 4524 going down (k = 0..4 for c1..c5) | in/out | bit lines of row C; continue down into the channel, not followed |
| `cdp1_c5_q` | M | 10632,3990 going up | out | row C slice 5 output, not followed into row B |

## Ambiguities

1. **m3 and m6 have no contact that I can see.** Each cell has two more vertical metal
   pieces that end inside it: m3 (8934-8956 x 3060-3168, a 10 px neck down to a pad at
   8936-8960 x 3288-3321) and m6 (9105-9127 x 3060-3322). Neither shows a contact ring
   or a widened pad, and `acid1b` shows no contact specks or patch under them, where
   every certain contact in the cell shows both. They are traced as floating metal
   (`cdp1_*_m3`, `cdp1_*_m6`). In row C, m6 is joined to `q` by the pad at the top of
   `pt`. Candidates if they do connect: m3 to the feedback diffusion under it at
   8930-8955 x 3098-3125 (that is `x`); m6 to the diffusion arm under it at 9098-9132 x
   3098-3122 or the diffusion at 9104-9130 x 3185-3240 (both `q`). None of these would
   change the logic. What would settle it: a sharper metal shot, or finding the same
   cell elsewhere with m3/m6 used. The dark rings on the poly write line at 9133-9148 x
   3300-3318 and 8962-8975 x 3295-3318 are *not* contacts: they sit in the gaps between
   two metal lines (trap 2 of the guide).
2. **`pt` to `q`** (buried contact at 9096-9134 x 3096-3126, drawn `?B`). `pt` ends on
   the arm of the q diffusion; a box with a heavy outline is there but lighter inside
   than the other buried contacts. Inferred: `pt` touches nothing else in the cell, and
   in row C it drives a gate of row B, so it must be an output.
3. **Feedback transistor.** Read as one diffusion 8905-9132 x 3099-3124 under a
   widening (8958-9040 x 3066-3128) of the grounded poly. The alternative reading, a
   separate poly strip 8958-9040 x 3100-3123 butted to diffusion at both ends, would
   make `x` = `q` by a plain wire and leave the grounded poly without any function, so
   it is rejected; the poly shows as one piece from y 3066 to 3120 in the 10 px sliver
   between m3 and the VCC rail (8960-8975).
4. **Load 1 geometry.** The load strip is taken as 8958-8985 under a poly block
   8933-9016 x 3176-3234; the block's left tie is the buried contact at 8896-8932.
   The strip's exact position under the block is not certain (it is hidden by m3's neck
   and the VCC rail); the connectivity (VCC - load - q1, gate = q1) does not depend on it.
5. Slice 0 of row A has no VSS diffusion tail to its left and no neighbour; the cell
   was drawn so that this needs no exception. The first cell's write-line leg is wider
   (8395-8445) than the others.

## Not done

- **Bit lines.** Each cell's bit line goes down from the contact at 8857+k*390, 3301
  (row A) / 4495 (row C). Row A's must pass row B and reach the poly lines of channel
  B/C or the big channel; row C's go straight into the big channel. Following them to
  the data bus gives the bit order and settles R8 / which 5-bit register row C is.
- **Row B** (y 3440-3990, five cells): what row C's q is compared or combined with.
- The two poly lines below row A (y 3340-3360, 3385-3405) and their contacts.
- Channel B/C, the big channel y 4530-5150, rows D and E.
- Where `cdp1_a_wr` and `cdp1_c_wr` come from (right of x 10786).
- Thin vertical metal line at x 10795-10820.
- Everything left of x 8340.

## Method notes for whoever continues

- Colours in `acid1b` here: diffusion is light tan with a heavy dark outline *whether or
  not metal was above*; poly is salmon under or near metal and dark orange-red, textured,
  in the open; field is pink under metal and olive in the open. Olive pockets with a
  thin outline and green rim are open field, not diffusion.
- `tools/cdp1_sr.py x y w h --offsets "..." --layers metal,acid1b,metal1,acid --up 5`
  aligns all instances of a cell to a fraction of a pixel and takes the median at 5x.
  It is much sharper than a single view or `composite.py` and is what resolved this
  cell. Offsets for `cdp1_reg`: `0,0 391,0 781,0 1171,0 1561,0 -391,0 0,1193 781,1192
  1172,1192 1562,1192` (acid1b offsets; the trace uses the metal-shot offsets).
- `tools/cdp1_tab.py` prints a brightness table of a strip; metal reads 60-75, bare
  field 45-55. It showed where a thin metal line really runs.
