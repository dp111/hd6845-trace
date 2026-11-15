# Work packages

The queue for parallel tracing. Maintained by the coordinating session only. Each
package is one agent's job: a region, a file prefix, and what is expected. Regions are
metal-shot pixels, x0-x1 x y0-y1. A row or cell belongs to the package that contains
its centre.

Status: `queued`, `running`, `done` (traced and reported), `checked` (an independent
agent has verified it), `partial` (reported, with work left: see its notes).

## Wave 1

| Prefix | Region | What | Status |
|---|---|---|---|
| `areg` | 15800-16950 x 12900-14700 | row inverters right of the decode array, fifth address register cell, bundle at x 16200-16400 | partial: inverters done; register cell partly; right-hand column x 16480-16800 not started |
| `sel` | 14100-15850 x 14650-16550 | where the 18 register select lines go below the decode array (latch column, strobe gating) | done: write strobe gates for R0-R11, R14, R15; R16/R17 buffered only; R12/R13 pass through |
| `trunks` | whole die | routes of the global signals (clocks, E, R/W, RS, CS, RES, LPSTB) from where their traces end into the core | partial (run 1): ck_out, ck_a, ck_b, e_b, rw_d, rs_d, cs_d, res_b, lpstb_b, clk to their first entries; left: source of X (input of input-row gate 0), end of S, clk_b, upper ends and taps |
| `rdp3` | 13350-16950 x 10700-12900, and 13350-15800 x 12900-13480 | right datapath, lower rows, including the row of cells above the decode array | partial (run 1): address register latch row traced (5 bits); two 8-bit register rows found, not placed; run 2 running |
| `cdp1` | 7600-10850 x 2950-5700 | central datapath, top rows | partial (run 1): rows A and C are static register bits (6 and 5 cells), row B upper half is a 5-input equality NOR; row B per-bit logic, bit lines, channels, rows D, E left; run 2 running |
| `larr` | 2400-4780 x 6450-18550 | left vertical array (rows every 477 px), by the MA pads | partial (run 1): it is the MA counter: incrementer (carry groups of 7, 3, 4) traced on the 14 lower rows; rest of the row, left column, 9 upper rows of another type, bit numbering left; run 2 running |
| `mra` | 11700-13320 x 7200-17050 | mid-right vertical array (rows every 477 px) | partial (run 1): chain column x 11730-12200 in all 19 rows; run 2 running on x 12200-13320 |
| `dbus` | 17050-17700 x 5300-17000, and the D0-D7 pad cells | data bus interface column; then finish the data pad cell (AMB-003) | partial: input buffers D0-D5 traced; gate groups, bus lines, pad cell left (continue as the same block) |

| `cdp2` | 7600-10850 x 5700-8450 | central datapath | partial (run 1): row A = five latch bits, row C = seven latch bits (same cell as the address register latch); rows B1/B2, D, channels 2, 3 left; run 2 running |
| `cdp3` | 7600-10850 x 8450-11200 | central datapath | partial (run 1): wiring rows E, F and channels B, D, G traced (two rows of cells gated onto an 8-line bus); cell rows A, C, H, I not traced; run 2 running |
| `cdp4` | 7600-10850 x 11200-14000 | central datapath, bottom rows | done except the upper half of its top latch row (y 11100-11490): a 4-way selector per slice with three latch rows (8, 8 and 6 bits); no counters or comparators |
| `bc1` | 7000-9000 x 14050-16300 | bottom-centre logic, upper left part; receives the six data tracks and strobe leaving the bottom of `cdp4` | running |
| `bd3` | 14100-15900 x 16550-17100 and onward | where the strobe and select tracks from `sel` go; source of the write strobe | done: strobe = NOT e_b (so each write strobe = select AND E); R12/R13 gated and buffered like R14/R15; all 16 tracks to the region's edge |
| `bd1` | 13000-14100 x 14700-17100 | logic left of the select gates; the write strobes pass through it heading west | running |
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
| `tc1` | 6400-8250 x 2500-4450 | top-centre random logic, upper half | running |
| `dbus` (continue) | as above | gate groups under the buffer chains, internal bus lines, P_x driver, D6/D7 buffers, then the pad cell |
| `areg` (continue) | as above | finish the fifth register cell (with `rdp3`'s four), the right-hand column x 16480-16800 |
| `rdp1` | 13350-16950 x 5450-8100 | right datapath, top rows |
| `rdp2` | 13350-16950 x 8100-10700 | right datapath, middle rows |
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
