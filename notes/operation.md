# How the HD6845S works: what the trace has established

This is the short version. The block notes (`notes/blocks/`) are the reference; the
glossary of names is `notes/signals.md`. Last checked against the extraction on
2026-11-16 (2,050 nets, 3,430 transistors).

## How to read this page

Every statement carries one of three marks.

| Mark | Meaning |
|---|---|
| **Firm** | The extracted netlist says it, and still says it when every item marked uncertain (`?`) is deleted from the trace. `tools/unsure.py --equations NAME` prints this for any equation: 683 of the 1,013 extracted equations are firm. |
| **Marked** | Extracted, but it depends on at least one uncertain item or on a join that is believed and not drawn. The assumption is named. |
| **Open** | Not traced. Nothing is claimed. |

"Firm" means the drawing says so without any flagged doubt. It does not mean the chip
has been simulated: nothing has been.

**The short answer to the three questions this page was asked to answer:**

- *What is each counter clocked on?* Known, and firm, for all five counters found so far.
- *How is each counter reset?* **Open for every counter.** The cell's next-value network
  is not fully extracted. One candidate mechanism is known (below).
- *What happens when each comparator fires?* **Open for every comparator.** Each
  comparator's output is traced some way; none is traced into the logic that uses it,
  except that the row counter's step logic is partly known.

## Clocks

| Fact | Mark |
|---|---|
| Two phases are made from CLK. `ck_b` can be high only while CLK is high; `ck_a` only while CLK is low. Each waits for the other to fall (cross-coupled NORs with two-inverter delays), so they never overlap. | Firm |
| `ck_b` is also held low whenever `inh_ck` is high. | Firm (the gate); the inverter that makes `inh_ck` has one uncertain item |
| `inh_ck`, `inh_rc` and `inh_lat` are three copies of one signal, `inh_src`. | Firm |
| Where `inh_src` comes from, and so what it means. | Open |
| A separate large buffer makes `ck_out` = NOT CLK for the rest of the chip; `clk_tl` = NOT `ck_out` is used in the top-left logic. | Firm, except the join from the CLK pad to the buffer (one uncertain item in the pad's input network) |

## Counters

Five counters are identified. All use the same master-slave bit cell.

| Counter | Bits | Clocked by | Gets a clock when | Mark |
|---|---|---|---|---|
| Horizontal character counter `hc` | 8 | `ck_b` and `ck_a` directly | every CLK cycle in which `ck_b` is allowed to rise | Firm |
| Horizontal sync width counter `hsw` | 4 | `ck_b` and `ck_a` directly | as above | Firm |
| Character row counter `rc` | 7 | its own pair `rc_ck_m`, `rc_ck_s` | once per pulse of `rc_step` | Firm |
| Scan line counter `sl` | 5 | a second pair `lc_ck_m`, `lc_ck_s` | once per pulse of `lc_step` | Firm |
| A 4-bit counter `c4l` (not identified; possibly vertical sync width) | 4 | the same pair as `sl` | once per pulse of `lc_step` | Firm |

How the two private clock pairs are made (the same cell twice):

    X_ck_m = NOR(X_step_n, X_ck_s delayed)      master clock: high during the step pulse
    X_ck_s = NOR(X_step,   X_ck_m delayed)      slave clock: high between pulses

| Fact | Mark |
|---|---|
| The two equations above, for both copies. | Firm |
| `rc_step` = NOR(`inh_rc`, `rc_stepreq_n`): the row counter steps when the step logic asks and the inhibit signal is low. | Firm |
| `rc_stepreq_n` = NOR of three terms; the step happens when term 1 is high, or when NOT `rcs_e4` AND NOT (`rcs_e3` AND `rcs_a2`). | Marked (one term's gate has an uncertain item); and the inputs `rcs_e3`, `rcs_e4`, `rcs_a2` are **not identified** |
| What makes `lc_step`. | Open |
| The memory address counter (14 bits, left array) and what clocks it. | Open (cells traced, control lines not) |

Inside a counter:

| Fact | Mark |
|---|---|
| In `hc` and `hsw` the master latch loads on `ck_b` (CLK high) and the slave on `ck_a` (CLK low). | Marked (the cell contains uncertain items; that these two lines gate the pass devices of exactly these twelve bits is firm) |
| The value the rest of the chip sees (the comparators, the outputs) is the buffered master, not the slave. | Firm for the buffer; marked for the cell behind it |
| Carry ripples up the bits: carry out = carry in AND the bit's slave. `hc` and `rc` also have a look-ahead line over bits 0-3. | Firm per bit; the bit-to-bit link is marked |
| The carry into bit 0 of each counter (what makes it count at all). | Open |
| The next-value function (increment, hold, clear). | **Open**: one pull-up and one branch of the network are not resolved |

**Reset.** Not established for any counter. What is known: in every bit the value on
its way to the master passes a gate `NOR(L3, …)`, so while the counter's line "L3" is
high the master is loaded with 0 (marked). For `rc`, `hsw`, `sl` and `c4l` that line
arrives from outside the counter and its source is open; it is the candidate for a
synchronous clear. For `hc` the same line is believed to be `ck_a` (join not drawn),
which would make it part of the clocking there and not a clear. So even the mechanism
is not settled.

## Registers and writing

| Fact | Mark |
|---|---|
| Each register bit is a transparent latch: it follows the data line while its write strobe is high and holds when it falls. | Extracted; the cell has uncertain items |
| `wr_r#` = register # selected AND the common strobe (`wr_stb_n` low). | Firm for R0-R11; marked for R12-R15 |
| The common strobe is a latch of "write, chip selected, RS high" that is open while E is high. | Marked (four of its nets are joined only through uncertain items) |
| Whether anything ends the strobe when E falls, or re-times it to CLK. | **Open**. As drawn nothing does; that reading rests on the marked nets above |
| The register rows of R3 (one nibble), R5, R6, R7, R8, R9, R10, R11 are identified by their strobe lines, drawn end to end. | Firm for the joins; the register *numbers* rest on the address decoder's numbering of its lines |
| The rows of R0, R1, R2, R4. | Marked: their strobe joins are believed, not drawn |
| R12-R15 (start address, cursor), R16/R17 (light pen), the status register. | Open beyond their strobe gates |
| Which nibble of R3 the 4-bit row is. | Marked: taken from the data sheet |

## Comparators

All are bit-by-bit equality (XOR per bit, NOR over the bits) unless noted. For the first
seven rows of the table the NOR is firm and each XOR has one uncertain link inside its
cell, so the bit equations are marked. R9's and R10's comparators are marked
throughout.

| Output | Compares | Counter inputs | Where the output goes |
|---|---|---|---|
| `h_eq_r0` | `hc` with R0 (8 bits) | bits 6-7 drawn, bits 0-5 believed | to a gate column beside the strobe channel; ends on a buried contact there. **Use: open** |
| `h_eq_r0half` | `hc` bits 0-6 with R0 bits 1-7 (R0 / 2) | as above | towards the same gate column. **Use: open** |
| `h_eq_r1` | `hc` with R1 | as above | into the bottom-centre logic. **Use: open** |
| `h_eq_r2` | `hc` with R2 | as above | believed to run west of the counters on a bus line (join not drawn). **Use: open** |
| `hsw_eq_r3` | `hsw` with the R3 nibble (4 bits) | drawn | not followed. **Use: open** |
| `uc_eq_r4`, `uc_eq_r6`, `uc_eq_r7` | seven lines `uc` with R4, R6, R7 | `uc` is **believed** to be the row counter; the join is not drawn | R6's goes to the strobe channel, R7's leaves west; not followed. **Use: open** |
| `sl_eq_r5` | scan line counter with R5 (5 bits) | drawn | leaves north; not followed. **Use: open** |
| R9's (`cdp1_b_eq`) | **the row address as it goes to the RA pins** with R9 (5 bits) | marked (the five lines pass units whose loads are not traced) | followed to the row counter's step logic; the last 12 px are undecided (AMB-013). **Use: open** |
| R10's (central datapath) | the row address one stage earlier with R10 bits 0-4; gives "equal" and "greater" | marked | not followed. **Use: open** |

Not found at all: comparators for R11 (cursor end), R12-R15 against the address
counter, and whatever the 4-bit counter `c4l` is compared with.

## The row address (RA0-RA4)

| Fact | Mark |
|---|---|
| The RA pins are not the scan line counter directly. Between them: a selector, a row of five units, then a five-cell stage in front of the pad drivers. | Firm that the selector and the units are there; the stage is not traced |
| The selector passes scan line bit k to output k, or to output k+1 (a shift up by one bit). The two control lines are opposites: `ras_straight` = NOT `ras_shift`. | Firm for the control; six strip joins inside the selector are uncertain |
| `ras_shift` = AND of two bits of R8. | Marked (four buried contacts). That they are R8's interlace bits 0 and 1 is believed |
| In shift mode output 0 has no counter bit; one bit of R9 chooses which of two signals drives it (`ras_o0_sel1` = shift AND that bit, `ras_o0_sel2` = shift AND NOT that bit). | Firm. That the bit is R9's bit 0 is believed (from the column it stands in) |
| One of those two signals is NOT(row counter bit 0) XOR another signal. | Marked; the other signal is open |
| In shift mode the R9 comparator does not compare that bit of R9; the comparator's input is switched to another signal. | Firm that it is switched; what it is switched to is marked and its source open |
| Where the field (odd/even) signal is made. | **Open**: expected in the gate column west of the nine-gate island, which is being traced |

## Not established at all

So that silence is not read as knowledge:

- How HSYNC, VSYNC, DISPTMG and CUDISP are made from the comparator outputs.
- The end-of-frame sequence (R4, then R5 extra lines, then restart) and the interlace
  odd/even logic.
- Why some registers act as N and others as N-1: no comparator's timing relative to its
  counter is established.
- The R8 skew path, the light pen, the status register, reset from the RES pin (the
  buffered `res_b` line is followed across the chip; what it does at its taps is not).
- The memory address counter's control, and the cursor compare.

The list of what is assumed, with the evidence for and against each, is
`notes/ambiguities.md` (AMB-001 to AMB-016). Work still to re-check before anything is
simulated is the "Re-read list" in `notes/work-packages.md` (R1-R12).
