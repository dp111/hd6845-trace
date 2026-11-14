# Left vertical array (`larr`)

Region x 2400-4780, y 6450-18550. Trace file `trace/larr.txt`.

## Status

Survey done. Tracing of the lower-section row cell in progress (see Inventory).

## Inventory (survey, 2026-11-15)

The region is not one array but three stacked/abutted things:

| Piece | x | y | Rows | Notes |
|---|---|---|---|---|
| Upper rows | 2950-4200 | 6543-10924 | 9 at tops 6543, 7020, 7498, 7975, 8539, 9015, 9493, 9970, 10447 | one row type; 87 px extra gap between row 4 and row 5 (7975 -> 8539). findcell master 2950,7020:4200,7497, offsets -477, 0, 478, 955, 1519, 1995, 2473, 2950, 3427 |
| Lower rows | 2900-4720 | 10992-18063 | 14 at tops 10992, 11470, 11947, 12424, 12901, 13379, 13856, 14549, 15027, 15504, 16154, 16631, 17109, 17586 | one row type (14 = the memory address width). Two routing gaps: 14333-14549 and 15981-16154, so the rows group 7 + 3 + 4. findcell master 2950,11470:4250,11947, offsets -478, 0, 477, 954, 1431, 1909, 2386, 3079, 3557, 4034, 4684, 5161, 5639, 6116 (dx 0 for the first seven, 1 after) |
| Left column | 2480-2860 | 6700-18500 | irregular pitch (about 600-800), not 477 | its own cells between the rails at x 2600-2650 and 2790-2824; believed to be the stages that feed the `maN_drv_in` lines. Not traced |
| Upper right block | 4450-4780 | 8250-10500 | - | separate logic right of the upper rows; not surveyed |

Supplies in the lower rows (from the load at 3200-3245 x 11550-11600, which hangs on
the rail at x 3103-3178): rail B x 3103-3178 is VCC; rail A x 2955-3003 is taken as VSS
(pull-downs hang on it). Rail B runs down into the wide band at y 18520-18730.

Composite of the lower row (median of 11 rows): `tools/t.sh larr composite.py larr_row
2860,11380:4820,12040 --offsets "0,0 0,477 0,954 0,1431 0,1909 0,2386 1,3557 1,4034
1,5161 1,5639 1,6116"`, view with `--comp larr_row`. In the composite the chip-2
stripped layer (`acid`) shows poly orange everywhere, also where metal was: it is the
best layer for poly here.

## Logic

### Lower row cell `larr_bit` (master row y 11470-11947; coordinates of the master)

Traced so far: x 2860-3340 (the control chain), extraction clean.

Rails through the row (vertical metal): A x 2955-3003 = VSS (pull-down sources);
B x 3105-3178 = VCC (three depletion loads hang on it; runs into the band at y 18520);
E x 3300-3400, irregular outline (3300-3350 at the top of the row, 3360-3425 beside
the H2 contact box at y 11640-11700, back to 3300-3350 below) = taken as VSS, see
Ambiguities; C x 3478-3528 = VCC (loads L3/L4, runs into the band at y 18520);
D x 3650-3700 not yet settled.

Traced gates (names as in the trace file, `{}` = row tag):

- `larr_a_{}` = NOT `larr_cin_{}`. Load L1 (VCC box 3130-3187 x 11553-11600, gate
  block 3200-3245 x 11550-11610, buried contact 3215-3250 x 11608-11640); pull-down is
  the gate P2 at 3263-3292 x 11560-11632 between L1's strip and the diffusion box T1
  (3292-3355 x 11553-11640, contact 3322,11587 to rail E). [T1 and this channel are not
  drawn yet; the channel is certain from the two edge lines across P2 at y 11557 and
  11635.]
- `larr_cout_{}` = NOT `larr_a_{}`: one very wide pull-down (W about 300) wrapped round
  the drain at 2962-3112 x 11553-11757, source on rail A; depletion load is the strip
  3122-3142 x 11650-11770 under rail B with gate P3 tied to the output by metal.
  `larr_cout` of one row is `larr_cin` of the row below (metal x 3063-3085).
- `larr_l0` (vertical metal x 2880-2900, all rows): each row pulls it to VSS when
  `larr_a` is high (W 70). So it is a wired NOR of all `larr_a`.
- `larr_n2_{}` = NOT `larr_a_{}`: load L2 (block 3190-3245 x 11775-11840), pull-down
  gate P4 at 3278-3297 x 11777-11822 to the box at 3298-3340 x 11770-11830 on rail E.
  N2 leaves in diffusion round the P4 pad and off to the right along y 11925-11943.
- Pass-gate strip y 11655-11705: N2 -[gate a]- mid -[gate cin]- R. The mid node goes by
  metal H2 (y 11668-11698) to poly Pv1 (contact 3333,11660); R ties by buried contact
  (3318-3345 x 11705-11735) to poly Ph4, which is believed to be the node of load L4.
  So mid = (cin ? R : 0).

Believed (not yet fully traced): Pv1 is the pull-down of N3 (load L3 on rail C), i.e.
N3 = NOT mid = NAND(cin, R).

Consequence that needs explaining: with only the one pull-down found, `larr_cout` =
`larr_cin`, i.e. the "carry" chain down the rows passes its input on unchanged through
two inverters per row. Either it is a re-buffered control line rather than a carry, or
a pull-down on `larr_a` has been missed.

## Ports

(to do)

## Ambiguities

- **Rail E (x 3300-3400): VSS or a signal?** It is the source of the pull-downs of
  `larr_a`, `larr_n2` and N3, all of which have depletion loads to VCC, which says VSS.
  But it also has two metal-to-poly contacts per row: at 3337,11522 onto a small poly
  pad (3328-3350 x 11512-11532) at the place where the poly line H1 (y 11486-11506,
  from the left column) jogs down to become H3 (y 11508-11530, to the right), and at
  3330,11890 onto a tab of a horizontal poly at y 11900-11920. And at the bottom of the
  array (3320,18225) it ends in a contact and a thin metal line to 3745,18235 instead
  of joining the VCC band or anything wide. Working assumption: VSS, the poly lines
  being tied low. What would settle it: following the rail up through the upper
  section to a supply, or finding what the tied poly lines gate.
- **Hook of the `larr_a` gate at 2985-3045 x 11631-11652**: read as plain poly (the gate
  jogging round the VSS contact), one net with the piece below it. It is not a buried
  contact: it is 20 px wide like any poly line, the real buried contacts here are
  33 px boxes, and a contact would short the gate to its own drain.
- **Bridge 3100-3122 x 11645-11685** between the carry-out drain and the load strip is
  open diffusion by its colour in both chip-2 shots (R/G 1.18, field is 1.03); the
  clean shot only shows it as a small outlined box.


## Not done

Everything except the survey.
