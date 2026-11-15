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

Running in this last round: `bd2` (run 2), `cdp1` (run 2), `bc1`, `rdp3` (run 3),
`mra` (run 3), `larr` (run 2), `cdp3` (run 2), `rdp2`, `cdp2` (run 2), `tc1` (run 2),
`bd1` (run 2).

## Wave 1

| Prefix | Region | What | Status |
|---|---|---|---|
| `areg` | 15800-16950 x 12900-14700 | row inverters right of the decode array, fifth address register cell, bundle at x 16200-16400 | partial: inverters done; register cell partly; right-hand column x 16480-16800 not started |
| `sel` | 14100-15850 x 14650-16550 | where the 18 register select lines go below the decode array (latch column, strobe gating) | done: write strobe gates for R0-R11, R14, R15; R16/R17 buffered only; R12/R13 pass through |
| `trunks` | whole die | routes of the global signals (clocks, E, R/W, RS, CS, RES, LPSTB) from where their traces end into the core | partial (run 1): ck_out, ck_a, ck_b, e_b, rw_d, rs_d, cs_d, res_b, lpstb_b, clk to their first entries; left: source of X (input of input-row gate 0), end of S, clk_b, upper ends and taps |
| `rdp3` | 13350-16950 x 10700-12900, and 13350-15800 x 12900-13480 | right datapath, lower rows | runs 1, 2 reported; **run 2's 'row RB is R0' was wrong** (RB is R2, per run 3 and rdp2 independently); run 3 still running |
| `cdp1` | 7600-10850 x 2950-5700 | central datapath, top rows | partial (runs 1, 2; 107 transistors): rows A and C static register bits (6 and 5 cells, columns c2-c7); row B a 5-bit equality comparator, per bit ne = A XOR B with neither input inverted. In one slice the comparator's register-side input is replaced by the output of tc1's island, which takes that register bit as an input. Compare-value lines, bit lines and write lines to the region's edges. Left: rows D and E, the write lines down to a strobe, slice-0 logic |
| `larr` | 2400-4780 x 6450-18550 | left vertical array: the MA counter (14 lower rows), 9 upper rows of another type, a left column of output stages | partial (runs 1, 2; 350 transistors): incrementer and latch part of the counter row traced on all 14 rows (x 2860-3900); stored bit is static; rail E is VSS. Left: x 3900-4720 of the row (two passes gave no consistent circuit: the reload path), left-column cells, bit numbering (MA8 and MA9 lines reach the left column, rows not fixed), the 9 upper rows |
| `mra` | 11700-13320 x 7200-17050 | mid-right vertical array (rows every 477 px) | partial (runs 1, 2): columns x 11730-12470 in all 19 rows: an AND chain over a per-row node q (x(N) = x(N+1) AND q(N)) with what looks like toggle logic; x 12470-13000 (storage, source of q) untouched; run 3 running |
| `dbus` | 17050-17700 x 5300-17000, and the D0-D7 pad cells | data bus interface column; then finish the data pad cell (AMB-003) | partial: input buffers D0-D5 traced; gate groups, bus lines, pad cell left (continue as the same block) |

| `cdp2` | 7600-10850 x 5700-8450 | central datapath | partial (run 1): row A = five latch bits, row C = seven latch bits (same cell as the address register latch); rows B1/B2, D, channels 2, 3 left; run 2 running |
| `cdp3` | 7600-10850 x 8450-11200 | central datapath | partial (runs 1, 2; 159 transistors): row C (6 bits, columns c2-c7) and row H (8 bits) are static register bits, same circuit as cdp1's, each readable onto bus N through rows E/F and driving a line west; write lines traced to the region's east edge. Left: row A (a different, larger cell), row I, the logic beside row A, and one unexplained NAND onto a bit line |
| `cdp4` | 7600-10850 x 11200-14000 | central datapath, bottom rows | done except the upper half of its top latch row (y 11100-11490): a 4-way selector per slice with three latch rows (8, 8 and 6 bits); no counters or comparators |
| `rdp2` | 13350-16950 x 8100-10700 | right datapath, middle rows | partial (run 1; 311 transistors): row RC **is R0** (strobe followed to sel_w0); above it comparator C (c against R0, 8 bits) and comparator D (7 slices: c of each slice against the R0 bit one place up, i.e. against R0/2, top bit of c not compared); upper array: row RE **is R4** with comparator E against seven other c lines, and an unidentified latch row RF. Nothing here drives the c lines: they come from rdp3's routing zone. Left: routing zone y 9080-9560, upper bit order, x 16160-16950 above y 9440 |
| `bc1` | 7000-9000 x 14050-16300 | bottom-centre logic, upper left part | partial (run 1; 22 transistors): the strobe driver of cdp4's 6-bit latch row (a 2-input NAND and two strong inverters, with a twin output going back up), a 2-bit decoder with gates for 00, 10 and 01 only, and the six data lines into that latch row (two joined, four drawn part way). Left: the group at x 7190-7860, y 15570-16300 that makes the NAND's two inputs (looks like cross-coupled gates), column B right of x 8560, column A below y 16000, the 13-line bus |
| `bd3` | 14100-15900 x 16550-17100 and onward | where the strobe and select tracks from `sel` go; source of the write strobe | done: strobe = NOT e_b (so each write strobe = select AND E); R12/R13 gated and buffered like R14/R15; all 16 tracks to the region's edge |
| `bd1` | 13000-14100 x 14700-17100 | mostly a routing channel of 18 vertical tracks, plus one gate column at x 13700-14080 | partial (run 1): strobes R0-R7 followed to the north edge on named tracks (R8 leaves west); the driver of line X and two big inverters of it traced; gate column y 15350-16125 and 16280-16900 (what ck_out feeds) and several tracks left; run 2 running |
| `bd2` | 15850-17000 x 14700-17100 | bus control logic right of the select gates | partial (run 1): areg_load = NOT e_b (one inverter). **Disagrees with bd3 about the common strobe**: bd2 reads its driver's input as the output of a further gate (e_b in series with another signal, possibly a latch), bd3 as e_b itself. Run 2 running to settle it and go on to CS, RS, R/W |

Measured on the first report: one agent run lasts about 20 minutes and about 60-80
image views, and yields one or two traced cells plus survey notes. Blocks are
therefore done by a chain of runs on the same prefix, each resuming from the block's
notes. Order of priority for free slots: central datapath and the control logic
around it, select/address logic, the two 14-bit arrays, right datapath, trunks, data
bus and pads.

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
| `bd1`-`bd3` | 13000-14100 x 14700-17100; 15850-17000 x 14700-17100; 14100-15850 x 16550-17100 | rest of the logic below the decode array |
| `tr1`, `tr2` | 11900-16400 x 3400-4500 | top-right logic rows |
| `amr` | 11400-13050 x 5250-6450 | logic above the mid-right array |
| `busL`, `busB`, `busT` | 4850-7550 x 10400-15000; 6500-13300 x 17000-18600; 11000-17000 x 3000-5300 | bus fields: follow the wiring between blocks and join their ports |
| `padring` | periphery | pad squares, supply rings, strips from pads to protection cells, the two comb cells by LPSTB/RES |
| verification | each finished package | an independent agent re-checks sampled gates and every port against the photos |
