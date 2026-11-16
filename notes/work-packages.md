# Work packages

The queue for parallel tracing. Maintained by the coordinating session only. Each
package is one agent's job: a region, a file prefix, and what is expected. Regions are
metal-shot pixels, x0-x1 x y0-y1. A row or cell belongs to the package that contains
its centre.

Status: `queued`, `running`, `done` (traced and reported), `checked` (an independent
agent has verified it), `partial` (reported, with work left: see its notes).

**2026-11-15 18:00.** The usage limit stopped all eleven running agents at once; they
were resumed when it reset. By the user's instruction no further agents are started
after this round: once these eleven have reported, the remaining packages below are
worked serially by the coordinating session, in priority order.

All eleven reported by 2026-11-15 night; statuses below are final for the round. They were: `bd2` (run 2), `cdp1` (run 2), `bc1`, `rdp3` (run 3),
`mra` (run 3), `larr` (run 2), `cdp3` (run 2), `rdp2`, `cdp2` (run 2), `tc1` (run 2),
`bd1` (run 2).

## Wave 1

| Prefix | Region | What | Status |
|---|---|---|---|
| `areg` | 15800-16950 x 12900-14700 | row inverters right of the decode array, fifth address register cell, bundle at x 16200-16400 | partial: inverters done; register cell partly; right-hand column x 16480-16800 not started |
| `sel` | 14100-15850 x 14650-16550 | where the 18 register select lines go below the decode array (latch column, strobe gating) | done: write strobe gates for R0-R11, R14, R15; R16/R17 buffered only; R12/R13 pass through |
| `trunks` | whole die | routes of the global signals (clocks, E, R/W, RS, CS, RES, LPSTB) from where their traces end into the core | partial (run 1; serial additions 2026-11-17: `ck_out` left-edge trunk to its top at (2500,7907), `res_b`/`lpstb_b` to their ends, `h_eq_r0`/`h_eq_r1` joins, `h_eq_r1` and `inh_lat` into the bottom bus field): ck_out, ck_a, ck_b, e_b, rw_d, rs_d, cs_d, res_b, lpstb_b, clk to their first entries; left: source of X (input of input-row gate 0), end of S, clk_b, upper ends and taps |
| `rdp3` | 13350-16950 x 10700-12900, and 13350-15800 x 12900-13480 | right datapath, lower rows | done (runs 1-3; 256 transistors): address register (5 latches); row RA **is R1** and row RB **is R2** (run 2's R0 was wrong), each with an 8-bit true-XOR equality comparator against the c lines; all three equality lines (R0, R1, R2) followed out of the region ungated; every bundle line and the routing zone traced; no c line is driven here, all eight leave at the lower left. Left: bit order; one disagreement with cdp2 about a contact inside the shared latch cell |
| `cdp1` | 7600-10850 x 2950-5700 | central datapath, top rows | partial (runs 1, 2; 107 transistors): rows A and C static register bits (6 and 5 cells, columns c2-c7); row B a 5-bit equality comparator, per bit ne = A XOR B with neither input inverted. In one slice the comparator's register-side input is replaced by the output of tc1's island, which takes that register bit as an input. Compare-value lines, bit lines and write lines to the region's edges. Left: rows D and E, the write lines down to a strobe, slice-0 logic |
| `larr` | 2400-4780 x 6450-18550 | left vertical array: the MA counter (14 lower rows), 9 upper rows of another type, a left column of output stages | partial (runs 1, 2; 350 transistors): incrementer and latch part of the counter row traced on all 14 rows (x 2860-3900); stored bit is static; rail E is VSS. Left: x 3900-4720 of the row (two passes gave no consistent circuit: the reload path), left-column cells, bit numbering (MA8 and MA9 lines reach the left column, rows not fixed), the 9 upper rows. **Next for the vertical logic**: the left column beside the nine upper rows (x 2480-2860, y 6700-10900) and those rows: the strobe `clk_tl` of the step logic ends at (2552,7872) beside upper row 2 |
| `mra` | 11700-13040 x 7200-17050 | the counters: horizontal (8 bits, rows r11-r18), character row (7 bits, r4-r10), a 4-bit one (r0-r3) | mostly done (run 4, serial; 629 transistors): the bit is a master-slave pair (master on ck_b from `na`, slave on ck_a), outputs and clock lines traced; the three counters have separate clocks (the row counter's come from the west). Left: the toggle network on node `m` (its pull-up, the unresolved cin branch B3/B4, load 1), so the next-state function and the way a counter is cleared are not extracted; the chain link r4 -> r3 (A1); what the line x 12902 (`cnt_gab`) is; the array's top and bottom ends |
| `mrach` | 13040-13425 x 7130-14700 | wiring channel right of the counters | done (wiring only): tracks, the poly hidden under them, counter outputs to the right datapath. Left: the east ends that rdp2 saw but did not draw, the stretch to bd1 east of x 13425, everything north of y 7130 |
| `wl` | 11040-11700 x 6930-9450 | logic west of the 4-bit counter | done (serial; 23 transistors): the character-row counter's clock generator (two cross-coupled NOR drivers making non-overlapping master and slave clocks from one step pulse p), p = NOR(`inh_rc`, b), two inverters, the bands over the counters' top and the metals that cross the block. Left: nothing inside; its ports' far ends (see `bw`) |
| `bw` | 10640-11480 x 6900-17200, and the lines that cross it west to x 5800 | bus field between the central datapath and the counters | partial (serial; wiring only): the five poly lines from `wl` followed west along cdp2's channel 3 and north into the crossing field x 6330-7700; the step signal b ends on a metal x 5841 going north into the top-left logic. Left: the bus field's own twenty lines (surveyed), the far ends of the five lines |
| `tla` | 2440-5060 x 2940-5640 | the three gate clusters of the vertical control and their bus fields | partial (serial; 52 transistors, eighteen gates and a latch): step = in1 OR (NOT e4 AND NOT (e3 AND a2)); in1 = NOR(mu, mv) in the middle cluster; the step condition is also latched while CLK is high (`clk_tl` = NOT `ck_out`, AMB-009; the inverter is in the left column of `larr`'s upper rows, at the top of the clock's left-edge trunk). `e4` drawn end to end, driver not found. Left: about 34 units of the first cluster, nearly all of the middle and right clusters, the bus pieces |
| `ur` | 2918-4240 x 6543-10924 | upper rows of the left array | mostly done (serial; 252 transistors by instancing): nine copies of the mid-right array's counter bit: a 4-bit and a 5-bit counter sharing one master and one slave clock; their clock generator (a second copy of the row counter's, 16 transistors) with its step input `lc_step` followed to the left-centre logic. Left: the two carry-ins, where the nine outputs go, the L3 and gab lines' sources, the line x 3478 |
| `urch` | 4240-4720 x 6140-10520 | wiring channel east of the left array's counters | partial (serial; wiring only): the nine counter outputs to the poly lines that take them east. Left: those lines beyond x 4720 (the 5-bit counter's were followed by eye through cdp2's channel 2 to the upper right datapath), the channel's other tracks, the logic block at x 4450-4780, y 8200-10500 |
| `dbus` | 17050-17700 x 5300-17000, and the D0-D7 pad cells | data bus interface column; then finish the data pad cell (AMB-003) | partial: input buffers D0-D5 traced; gate groups, bus lines, pad cell left (continue as the same block) |

| `cdp2` | 7600-10850 x 5700-8450 | central datapath | partial (runs 1, 2; 142 transistors): row A five latch bits, row C seven latch bits; rows B1/B2 a 5-bit comparator with a ripple chain between slices (per bit: NOR, XOR, a NAND with the chain input) and a row-long line pulled low per bit, i.e. it yields more than equality; it compares row C's bits with a 5-bit value on per-slice through tracks. What drives the chain input and what the chain output drives meet at one hidden corner (9300,7168) and are not drawn. Left: row D (six large cells continuing into cdp3's row A), channels 2 and 3, the strobes beyond x 10895 |
| `cdp3` | 7600-10850 x 8450-11200 | central datapath | partial (runs 1, 2; 159 transistors): row C (6 bits, columns c2-c7) and row H (8 bits) are static register bits, same circuit as cdp1's, each readable onto bus N through rows E/F and driving a line west; write lines traced to the region's east edge. Left: row A (a different, larger cell), row I, the logic beside row A, and one unexplained NAND onto a bit line |
| `cdp4` | 7600-10850 x 11200-14000 | central datapath, bottom rows | done except the upper half of its top latch row (y 11100-11490): a 4-way selector per slice with three latch rows (8, 8 and 6 bits); no counters or comparators |
| `rdp2` | 13350-16950 x 8100-10700 | right datapath, middle rows | partial (run 1; 311 transistors): row RC **is R0** (strobe followed to wr_r0); above it comparator C (c against R0, 8 bits) and comparator D (7 slices: c of each slice against the R0 bit one place up, i.e. against R0/2, top bit of c not compared); upper array: row RE **is R4** with comparator E against seven other c lines, and an unidentified latch row RF. Nothing here drives the c lines: they come from rdp3's routing zone. Left: routing zone y 9080-9560, upper bit order, x 16160-16950 above y 9440 |
| `bc1` | 7000-9000 x 14050-16300 | bottom-centre logic, upper left part | partial (run 1; 22 transistors): the strobe driver of cdp4's 6-bit latch row (a 2-input NAND and two strong inverters, with a twin output going back up), a 2-bit decoder with gates for 00, 10 and 01 only, and the six data lines into that latch row (two joined, four drawn part way). Left: the group at x 7190-7860, y 15570-16300 that makes the NAND's two inputs (looks like cross-coupled gates), column B right of x 8560, column A below y 16000, the 13-line bus |
| `bd3` | 14100-15900 x 16550-17100 and onward | where the strobe and select tracks from `sel` go; source of the write strobe | done: strobe = NOT e_b (so each write strobe = select AND E); R12/R13 gated and buffered like R14/R15; all 16 tracks to the region's edge |
| `bd1` | 13000-14100 x 14700-17100 | strobe channel of 18 vertical tracks plus one gate column at x 13700-14080 | partial (runs 1, 2; about 36 transistors of its own): strobes R0-R7 to the north edge; driver of line X and two big inverters of it; in the gate column y 15385-15850 an inverter and a latch gated by NOT X (upper half complete, lower half's load and the feedback link not traced). Left: gate column y 15850-16125 and 16280-16900 (everything ck_out feeds), tracks k7 and k8 (which carry the R0 and R1 match lines from rdp3) beyond their first jog; expect about 5 images per gate at 4-6x |
| `bd2` | 15850-17000 x 14700-17100 | bus control logic right of the select gates | partial (runs 1, 2): the common strobe is the output of a D latch open while E is high, set by NOR(rw_d, NOT rs_d (believed), cs_d); the address register load strobe is gated by E AND NOR(rw_d, rs_d, cs_d) OR an unknown x. bd3's 'NOT e_b' reading refuted by measurement. Left: source of x, three loads, the column below y 16680, the right-hand column |

Measured on the first report: one agent run lasts about 20 minutes and about 60-80
image views, and yields one or two traced cells plus survey notes. Blocks are
therefore done by a chain of runs on the same prefix, each resuming from the block's
notes. Order of priority for free slots: central datapath and the control logic
around it, select/address logic, the two 14-bit arrays, right datapath, trunks, data
bus and pads.

## Re-read list

Work already marked `done` or `partial` whose method later turned out to be unreliable.
**Every entry here is a task**: it is worked through before M5 (simulation) starts and
struck out, with the date and what was found, when done. Whoever finds that a method used
on earlier blocks can miss things adds the affected blocks here in the same commit
(`CLAUDE.md`, "Re-read rule").

Why the first four are here (found 2026-11-15/16 in `mrach`): in a wiring channel poly
runs *under* the metal tracks, on other nets, for hundreds of pixels (a track ends on a
contact, the net carries on in poly beneath its neighbour, comes back up three tracks
away). The metal shots show none of it. A channel read from the metal shot alone can
have wrong connections between tracks and missing taps. The clean shot (`acid1b`) shows
the poly as salmon under where the metal was; `tools/strips.py --layer acid1b` and
`tools/classmap.py` are the tools.

| # | Block | Region | What to re-read | Why suspect | Status |
|---|---|---|---|---|---|
| R1 | `bd1` | 13000-13700 x 14700-17100 | all 18 vertical tracks, end to end, in `acid1b`: every track end, every place a track is interrupted, poly under tracks; tracks k7/k8 beyond their first jog | channel read mostly from the metal shots; `mrach` already corrected one of its leads (bd1.txt line 191) | open |
| R2 | `bd3` | 14100-15900 x 16550-17100 | the 16 tracks, same check | notes cite the metal shot for the track checks (3 mentions of the clean shot in 247 lines) | open |
| R3 | `sel` | 14100-15850 x 14650-16550 | the track field T0-T17 between and below the gates, same check; rsel12/rsel13 "carried through with no contact" in particular | notes never mention the clean shot | open |
| R4 | `trunks` | whole die | every long run: taps and cross-unders along bus lines L3-L6 (y 18335-18470), the left bus field (x 6790-6870), the bottom trunk (y 18947), each "followed at 1x" stretch | read at 1x in the metal shot only; a tap in poly under a neighbouring line would not have been seen | open |
| R5 | `rdp2` | 13350-16950 x 8100-10700 | bundle lines and the zone y 9080-9560 in `acid1b` when its routing zone is traced | notes never mention the clean shot; the channel's east ends at y 9406, 9447, 9707, 9748, 9884, 9963 arrive there undrawn | open |
| R6 | every array block (`larr`, `cdp1`-`cdp4`, `rdp2`, `rdp3`, `areg`) | - | each line drawn once at full length across many rows (rails, clock lines, bit lines): look at it where it crosses each routing channel or row boundary | in `mra` three of the agents' full-length lines were really two or three pieces on different nets (ck_a rail, L1, L3) | open |
| R8 | `mra` | x 12240-12340, all 19 rows | the metal x 12276-12294 (`cnt_la_a`): find its contacts. Look at each row at 3-4x in both shots, and at the neighbouring metals (M1 at x 12226, line B at x 12325) for bridges | it was drawn as one line through all rows with no contact; it is three pieces (cut at y 12885-13030 and y 14965-15010) and the top piece feeds the gate of inverter I1 in `wl` with nothing found driving it. A wire with one end is a missed contact | open |
| R9 | `mra` | the hold device's far side `z` in each row | where `z` is tied: as traced it ends as a free stub in every row | a depletion "hold" device to a floating node does nothing; `z` and the line of R8 are both loose ends in the same columns | open |
| R10 | `bc1` | the 13-line bus y 14354-14873, x 6400-9300 | each line end to end: where it changes between poly and metal and where one y holds two nets | line y 14526 is two nets split at the pads (7012,14522) and (7100,14522); bc1's notes treat each y as one line | open |
| R7 | any junction or contact accepted by eye in the clean shot between tan, pink and salmon areas | - | when a block is next opened: class map plus a profile across each junction that decides a connection | twice in `mra` the eye joined two diffusions that a profile showed 20 px apart | standing |

## Open joins

Wires labelled `NAME_u` are believed to be net NAME but are not joined to it by drawn
geometry. `tools/build.py` prints the current list (12 on 2026-11-17, after the R0 and R1 match lines were joined). Each is closed by
tracing the stretch between the two pieces and renaming the label.

| Names | Where the gap is |
|---|---|
| `hc0_u` ... `hc5_u` | the horizontal counter lines between the strobe channel / wiring channel and the comparators' c lines (right datapath, y 13480-14700 and east of x 13425) |
| `h_eq_r2_u` | bus line G west of the counters: the R2 match line through the upper right datapath's undrawn bars (enters at (13425,9707)) |
| `wr_r0_u`, `wr_r1_u`, `wr_r2_u`, `wr_r4_u` | the load strobes at the register rows: between the strobe channel's tracks and the latch rows |
| `ck_a_u` | the horizontal counter's L3 line: poly from (12631,16954) to the `ck_a` bus line at (12740,18471), followed but not drawn |

## Queue

| Prefix | Region | What |
|---|---|---|
| `tc1` | 6400-8250 x 2500-4450 | top-centre random logic, upper half | partial (runs 1, 2; 26 transistors): the nine-gate island and all its wiring; its five inputs followed to the region's edges: a from the datapath (cdp1's register bit), w1 leaves east at (8350,3700), b, g, i arrive from tc2 at (7512,4450), (7143,4450), (7187,4450). Left: the gate columns at x 6400-7000 (large devices under wide rails, need 3-4x views and profiles), an undrawn structure at x 6750-6940, y 3930-4200, the channel at x 7000-7170 |
| `dbus` (continue) | as above | gate groups under the buffer chains, internal bus lines, P_x driver, D6/D7 buffers, then the pad cell |
| `areg` (continue) | as above | finish the fifth register cell (with `rdp3`'s four), the right-hand column x 16480-16800 |
| `rdp1` | 13350-16950 x 5450-8100 | right datapath, top rows |
| `tl1`-`tl6` | 2100-6400 x 2500-6350, in six parts | top-left random logic |
| `tc2` | 6400-8250 x 4450-6400 | top-centre random logic, lower half |
| `trunks` (continue) | whole die | source of X, end of S, clk_b, taps and upper ends |
| `lc1`-`lc3` | 4400-6450 x 6900-10400, in three parts | left-centre random logic |
| `bc2`, `bc3`, `bc4` | 9000-11000 x 14050-16300; 7000-9000 x 16300-18550; 9000-11000 x 16300-18550 | rest of the bottom-centre random logic |
| `cdp4` (continue) | 7600-10850 x 11100-11490 | upper half of the top latch row: source of selector input a, bus taps, latch data |
| `bl1`, `bl2` | 4800-6500 x 15800-18650 | bottom-left random logic |
| `bd1`-`bd3` | 13000-14100 x 14700-17100; 15850-17000 x 14700-17100; 14100-15850 x 16550-17100 | rest of the logic below the decode array; **start with re-read items R1, R2** |
| `tr1`, `tr2` | 11900-16400 x 3400-4500 | top-right logic rows |
| `amr` | 11400-13050 x 5250-6450 | logic above the mid-right array |
| `busL`, `busB`, `busT` | 4850-7550 x 10400-15000; 6500-13300 x 17000-18600; 11000-17000 x 3000-5300 | bus fields: follow the wiring between blocks and join their ports |
| `padring` | periphery | pad squares, supply rings, strips from pads to protection cells, the two comb cells by LPSTB/RES |
| verification | each finished package | an independent agent re-checks sampled gates and every port against the photos |
