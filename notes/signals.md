# Signal names

Every named net in the trace is listed here, by name or by pattern. `tools/build.py`
checks this: a net name that no row of these tables covers is reported as
"not in notes/signals.md" in the build output and in `out/report.txt`.

In a pattern, `#` stands for a number and `*` for any run of letters, digits and
underscores. The first column of every table is read by the build, so keep each pattern
in backticks in the first column.

## Rules

1. **A signal is named for what it is** as soon as tracing shows what it is: pin names
   as on the datasheet (`e`, `rw`, `ma5`), register numbers (`r1_b3_q`, `wr_r6`), counter
   bits (`hc0`, `rc3_q`), results (`h_eq_r0`).
2. **A signal that is not identified is named for where it is**: a block prefix and a
   local name (`cdp3_h_c5_q`, `rcs_e4`). The table says what is known about it. When it
   is identified it is renamed everywhere with `tools/rename.py` (trace files, notes,
   floor plan) and its old name goes into "Former names" at the end of this file.
3. Suffixes: `_n` inverse (active low), `_q` output of a latch or register bit, `_b#` bit
   number (bit 0 = least significant), `_s#` slice number where the bit order is not
   established, `_dly` a delayed copy, `_buf` a buffered copy.
4. **`_u` marks an open join**: a piece of wire believed to be the same net as the name
   without the suffix, whose connection has not been drawn (`hc1_u`, `wr_r0_u`). Every
   `_u` name is a task; the build lists them.
5. Rows and slices are places and keep their numbers in the notes ("row r18", "slice
   s3"); the tables below say which bit each one is.

## Where the bits are

Counters (mid-right array, rows r0-r18 from the top, `notes/blocks/mra.md`):

| Rows | Counter | Bit of row |
|---|---|---|
| r18 ... r11 | horizontal character counter, `hc0` ... `hc7` | r18 = bit 0 (carry enters there), r11 = bit 7 |
| r10 ... r4 | character row counter, `rc0` ... `rc6` | r10 = bit 0, r4 = bit 6 |
| r3 ... r0 | 4-bit counter, `c4b0` ... `c4b3` (not identified; its outputs leave north) | r3 = bit 0 (taken from the carry chain's direction), r0 = bit 3 |

Counters in the left array's upper rows (rows u0-u8 from the top, `notes/blocks/ur.md`; the
same bit cell as the mid-right array's):

| Rows | Counter | Bit of row |
|---|---|---|
| u8 ... u4 | 5-bit counter, `c5l0` ... `c5l4` (not identified) | u8 = bit 0 (the carry enters there from the left column), u4 = bit 4 |
| u3 ... u0 | 4-bit counter, `c4l0` ... `c4l3` (not identified) | u3 = bit 0, u0 = bit 3 |

Right datapath, lower array (R0, R1, R2 and their comparators): slice s1 = bit 0, s2 =
bit 1, ... s7 = bit 6, **s0 = bit 7** (from the counter lines: `hc0` arrives at s1, `hc7`
at s0). Upper array (R4, R6): bit order not established, names keep the slice (`sm1`, `s0`
... `s5`, left to right).

## Supplies, pins and pad circuits

| Name | What it is |
|---|---|
| `vcc`, `vss` | supplies |
| `clk`, `e`, `rw`, `rs`, `cs`, `res`, `lpstb` | the pin itself (pad node) |
| `cs_p`, `e_p`, `rs_p`, `rw_p` | the pin's node behind its protection strip, at the input of its buffer |
| `clk_n`, `clk_b` | NOT CLK and CLK buffered (input row; `clk_b` feeds the phase generator) |
| `e_n`, `e_b` | NOT E and E buffered. `e_b` is the E that the bus control logic uses |
| `rw_a`, `rw_b`, `rw_c`, `rw_d`, `rs_a`, `rs_b`, `rs_c`, `rs_d`, `cs_a`, `cs_b`, `cs_c`, `cs_d` | the four inverters of each input chain: `_a` and `_c` inverted, `_b` and `_d` true. The core uses `_d` |
| `res_n`, `res_b` | NOT RES and RES buffered. `res_b` runs down the top-left logic to line 3 of the poly bus at x 5100-5290 |
| `lpstb_n`, `lpstb_b` | the same for LPSTB; `lpstb_b` ends on line 4 of that bus |
| `ma#`, `ra#`, `hsync`, `vsync`, `disptmg`, `cudisp` | output pins (pad node) |
| `*_drv_in` | the signal from the core that an output pad cell receives (the pad is its inverse) |
| `*_pu`, `*_pd` | inside an output pad cell: gate of the pull-up fingers (first inverter) and of the pull-down fingers (second inverter) |
| `d#_in` | data pin D# behind its protection, at its input buffer |
| `d#_a`, `d#_b`, `d#_c`, `d#_d` | the four inverters of data input buffer #: `_a`, `_c` inverted, `_b`, `_d` true |
| `dbus_cap#b` | plate of a capacitor beside the D0 input buffer (purpose not established) |

## Clocks

| Name | What it is |
|---|---|
| `ck_a` | phase high only while CLK is low (non-overlapping with `ck_b`). Slave clock of the horizontal and 4-bit counters |
| `ck_b` | phase high only while CLK is high. Master clock of the horizontal and 4-bit counters. Held low while `inh_ck` is high |
| `ck_a_u` | the line that gates the second pull-down of the horizontal counter's `_nx_g` nodes: followed in poly to the `ck_a` bus line of the clock block; join not drawn |
| `ck_out` | NOT CLK from the big three-stage buffer: the main internal clock, distributed along the bottom and left edges |
| `clk_tl` | NOT `ck_out`, i.e. CLK polarity, for the top-left logic: made by an inverter at (2626,7908) in the left column beside upper row 2 of the left array, where the left-edge trunk of `ck_out` arrives, and run back north (thin metal x 2457, poly y 5587, bus lines D and B). In the step logic it samples `rcs_cond` into `rcs_cond_lat`, enables the first term of `rcs_n4200`, and gates units at y 3765 and y 4410 |
| `ck_a_pu`, `ck_b_pu` | gates of the source-follower pull-ups of the two phase drivers |
| `ck_g#` | outputs of the clock gate row: `ck_g1`, `ck_g2` = `ck_b` delayed by one and two inverters, `ck_g3`, `ck_g4` = the same for `ck_a` |
| `ck_clkn` | NOT `clk_b` inside the phase generator |
| `ck_t`, `ck_n#`, `ck_ga` | internal nodes of the main clock buffer (first stage output, second stage output, gate of the output pull-up) |

## The inhibit signal

One core signal stops both the horizontal counter's master clock and the row counter's
step. Its source is not traced; it enters the strobe channel's gate column from the
bottom bus field. All five names below are copies of it.

| Name | What it is |
|---|---|
| `inh_src` | the signal as it arrives (gate of the driver of `inh_n`); source unknown |
| `inh_n` | NOT `inh_src`: "line X" of the notes. Input of the lone inverter in the input buffer row |
| `inh_ck` | NOT `inh_n` from that inverter: holds `ck_b` low in the clock block, and is distributed along the bottom bus field and up the left bus field ("S" in the notes) |
| `inh_rc` | NOT `inh_n` from the upper inverter in the strobe channel: runs up the wiring channel, over the top of the counters, to the row counter's step gate (`rc_step` = NOR(`inh_rc`, `rc_stepreq_n`)) |
| `inh_lat` | NOT `inh_n` from the lower inverter: gates the latch in the strobe channel's gate column |

## Counters

For `<bit>` read `hc#`, `rc#`, `c4b#`, `c5l#` or `c4l#`. Each bit is a master-slave pair
(`notes/blocks/mra.md`; the node letters used there are given in brackets).

| Name | What it is |
|---|---|
| `hc#`, `rc#`, `c4b#`, `c5l#`, `c4l#` | the bit as the rest of the chip sees it: the buffered **master** (node n1). The comparators compare this, not the slave |
| `hc#_q`, `rc#_q`, `c4b#_q`, `c5l#_q`, `c4l#_q` | slave latch (q): takes `_d` on the slave clock |
| `*_q_n` | NOT `_q` (g1) |
| `*_m` | master latch node (a): takes `_nx_g` on the master clock |
| `*_mb` | node b, joined to `_m` through a pass transistor gated by `cnt_gab`; gate of the feedback device from `_d` to `_m` |
| `*_m_n` | NOT `_m` (p3) |
| `*_d` | NOT `_m_n`: the copy of the master that the slave gate passes to `_q` (d) |
| `*_nx` | next-value node of the bit (m): pulled low through networks of the carry and `_q`; its pull-up and one branch are not resolved, so the next-state function is not extracted |
| `*_nx_n` | NOT `_nx` (nb) |
| `*_nx_g` | NOR(L3 line, `_nx_n`) (na): the next value, forced low while the counter's L3 line is high |
| `*_ci_n` | NOT carry-in of the bit (n2) |
| `*_co` | carry out of the bit = carry-in AND `_q` (x); carry-in of the next row up |
| `*_tab` | a diffusion tab pulled low by `_q_n` (spare finger); in rows r7-r10 and r15-r18 it is on the look-ahead line |
| `*_rb` | lower part of the diffusion R in the `_nx` network; its continuation is not resolved |
| `*_z` | far side of the weak always-on device from `_q`; ends as a free stub as traced (re-read item R9) |
| `*_md`, `*_mt` | metal straps between a row and its neighbour in the chain column (lower, upper); their joins are in `notes/blocks/mra.md` |
| `hc_ci`, `rc_ci`, `c4b_ci` | carry-in of each counter's bit 0. Sources not traced |
| `hc_lo4_set`, `rc_lo4_set` | look-ahead line: low while any of bits 0-3 is clear, i.e. high when `_q` of bits 0-3 are all 1 (group lines B and A) |
| `rc_ck_m`, `rc_ck_s` | master and slave clock of the row counter (bus lines E and D), made by the generator below |
| `rc_l3`, `c4b_l3` | the L3 line of the row counter (from the west along y 13005) and of the 4-bit counter (from the north). What they carry is not known; for the horizontal counter L3 is `ck_a` |
| `lc_ck_m`, `lc_ck_s` | master clock (line L1) and slave clock (rail x 4218) of both counters of the left array's upper rows: one line each through all nine rows, each fed at the top by a poly from the west (y 6500 and y 6455). Sources not traced |
| `c4l_l3`, `c5l_l3` | the L3 lines of those two counters: the 4-bit one's comes from the north; the 5-bit one's from a poly along y 6410 (from the west, and from a metal from the north at x 3968) |
| `c4l_gab`, `c5l_gab` | their pass-gate lines: the 4-bit one's comes from the north; the 5-bit one's from a poly from the east along y 6520, ending on a contact at (4087,11005) |
| `cnt_gab` | gate line of the `_m` to `_mb` pass transistors of all 19 bits (x 12902), fed from the top by band H4. Source not traced |
| `cnt_l2_a`, `cnt_l2_b`, `cnt_l2_c` | three pieces of the metal line L2 that passes through the rows without a contact |
| `cnt_la_a`, `cnt_la_b`, `cnt_la_c` | three pieces of the metal x 12285 through the rows; no contact found in the rows (re-read item R8). `cnt_la_a` feeds an inverter west of the counters |
| `cnt_la_a_n` | NOT `cnt_la_a`; leaves north |
| `cnt_bus_a`, `cnt_bus_b` | bus lines A and B of the channel between rows r3 and r4; not identified. B runs from the datapath channel 3 to the upper right datapath |

## Row counter clock generator and step

| Name | What it is |
|---|---|
| `rc_stepreq_n` | request to step the row counter, active low. Made by a three-input NOR in the top-left logic |
| `rc_step` | NOR(`inh_rc`, `rc_stepreq_n`): the step pulse. The row counter's masters load while it is high |
| `rc_step_n` | NOT `rc_step` |
| `rc_ck_m_n`, `rc_ck_m_dly` | NOT `rc_ck_m`, and `rc_ck_m` delayed by two inverters; `rc_ck_s` = NOR(`rc_ck_m_dly`, `rc_step`) |
| `rc_ck_s_n`, `rc_ck_s_dly` | the same for `rc_ck_s`; `rc_ck_m` = NOR(`rc_step_n`, `rc_ck_s_dly`) |
| `rcs_in1`, `rcs_in2`, `rcs_in3` | the three inputs of the NOR that makes `rc_stepreq_n`. `rcs_in2` = NOR(`rcs_w2`, `rcs_e4`), `rcs_in3` = NOR(`rcs_e3`, `rcs_e4`). `rcs_in1` not identified: from the bus field at x 4279 |
| `rcs_w2`, `rcs_c1`, `rcs_b1` | `rcs_w2` = NOT `rcs_c1`; `rcs_c1` = NOR(`rcs_a2`, `rcs_b1`); `rcs_b1` = NOR(`rcs_x1`, `rcs_a2`, `rcs_u3425`) |
| `rcs_cond_n` | NOR(`rcs_in2`, `rcs_in3`) = `rcs_e4` OR (`rcs_e3` AND `rcs_a2`): the step condition inverted (called m2 in the block notes) |
| `rcs_cond` | NOT `rcs_cond_n`: the row counter's step condition apart from `rcs_in1`. On bus line A's piece A3; first gate of the series pair in `rcs_n4200` |
| `rcs_cond_lat` | `rcs_cond` sampled through a pass transistor while `clk_tl` is high (a dynamic latch on a metal and two poly pads); its poly goes west under the rail at y 4010-4030, not followed |
| `rcs_e3`, `rcs_e4`, `rcs_a2`, `rcs_x1` | inputs of the step logic, **not identified**. `rcs_e4` gates everything except `rcs_in1`; it is a long control line (17,000 px, five gate loads, driver not found) that runs beside `res_b` and `lpstb_b` |
| `rcs_u#` | output of a unit of the step logic cluster that has no better name yet, by the y of its buried contact (`rcs_u3288` = NOR(`rcs_g3245`, `rcs_bd3330`); `rcs_u3425` = NOT `rcs_bc3460` = `rcs_e3` OR `rcs_e4`, third input of `rcs_b1`) |
| `rcs_n#` | output of an AND-OR-INVERT unit of the first cluster (`rcs_n4200` = NOT(`rcs_cond` AND `clk_tl` OR `rcs_g4240`)); leaves on a metal strap x 2845-2885 |
| `rcs_g#` | an input of the cluster that arrives on a poly line from outside, by the y of that line |
| `rcs_ba#`, `rcs_bb#`, `rcs_bc#`, `rcs_bd#`, `rcs_be#`, `rcs_bf#`, `rcs_bg#` | a piece of bus line A-G beside the first cluster (x 3090-3380) whose driver is not yet known, by the y of its top end |
| `rcs_bp#`, `rcs_bq#`, `rcs_br#`, `rcs_bs#`, `rcs_bt#`, `rcs_bu#`, `rcs_bv#` | the same for the second bus field (x 4140-4420; tracks P-V at x 4148, 4192, 4235, 4279, 4322, 4365, 4409) |
| `rcs_mu`, `rcs_mv` | the two inputs of the NOR that makes `rcs_in1` (middle cluster): bus pieces of the second bus field (x 4192). `rcs_mu` = NOT `rcs_bq3335` (an inverter at y 3413); `rcs_mv` comes from a poly that leaves the bus field east and south at (4283,4745) |
| `rcs_mn#` | output of a unit of the middle cluster, by the y of its output (`rcs_mn3852` = NOR(?, `rcs_in1`)) |
| `rcs_thin_e`, `rcs_thin_w` | two thin metals down the cluster, over the loads; what they join is not read |
| `wl_i#_in`, `wl_i#_out` | input and output of the unidentified inverter I2 west of the counters |
| `wl_h#` | horizontal poly bands H0 and H1 above the counters; not identified |

## Registers, comparators and their results

| Name | What it is |
|---|---|
| `rsel#` | select line of register # from the address decode (high when the address register holds #) |
| `rsel#_n` | NOT `rsel#` |
| `rsel#_bn`, `rsel#_buf`, `rsel#_bufn` | buffer of a select line: first inverter and output (`rsel12_bufn` is the first inverter of R12's separately built buffer) |
| `wr_stb_n` | common write strobe, active low |
| `wr_r#` | write strobe of register #: `rsel#` AND NOT `wr_stb_n` |
| `wr_r#_u` | the load strobe line at the register's latch row, where its join to `wr_r#` is not drawn |
| `r#_b#_a`, `r#_b#_n2`, `r#_b#_q` | register R#, bit #: storage node (loaded from the bus while the strobe is high), its inverse, and the output (= the stored bit) |
| `r#_s#_*`, `r#_sm#_*` | the same for R4 and R6, by slice |
| `r#c_b#_nor`, `r#c_b#_x` | comparator of R#, bit #: NOR(counter bit, register bit), and x = counter bit XOR register bit |
| `r#c_s#_*`, `r#c_sm#_*` | the same for the R4 comparator, by slice |
| `r#hc_s#_nor`, `r#hc_s#_x` | comparator of the horizontal counter against R0 shifted one place (R0/2), by slice |
| `h_eq_r#` | high when the horizontal counter equals R# (R0: end of line; R1: displayed width; R2: sync position) |
| `h_eq_r#half` | high when the horizontal counter equals R0/2 |
| `h_eq_r#_u` | a piece believed to be `h_eq_r#` whose join is not drawn (tracks k7, k8 of the strobe channel; bus line G west of the counters) |
| `uc_s#`, `uc_sm#` | the seven counter lines of the upper right array, by slice. Believed to be the row counter (four of seven joined by geometry) |
| `uc_eq_r#` | high when those lines equal R4 |
| `hc#_u` | the horizontal counter line at the comparators, where its join to `hc#` is not drawn |
| `rbus_b#` | data line of bit # through the lower right datapath (believed D#; its connection to the data pads is not traced) |
| `ubus_s#`, `ubus_sm#` | data lines of the upper right array, by slice |
| `ar#`, `ar#_n` | address register bit # and its inverse (rows of the decode array) |
| `ar#_a`, `ar#_n2`, `ar#_q`, `ar#_trk` | nodes of address register bit #: storage node, its inverse, output, and the track that takes it to the decode |
| `ar_load`, `ar_load_n` | load strobe of the address register and its inverse |
| `areg_w#` | lines 6 and 7 of the bundle beside the address row inverters; not identified |

## Bus control

| Name | What it is |
|---|---|
| `wr_data_sel` | NOR(`rw_d`, `bd2_rs_n`, `cs_d`): a write to the data register is addressed |
| `wr_data_sel_n` | NOT `wr_data_sel` |
| `wr_data_lat`, `wr_data_lat_n` | transparent latch of `wr_data_sel`, open while `e_b` is high |
| `wr_data_e_n` | NOT(`wr_data_sel` AND `e_b`) |
| `wr_addr_sel` | NOR(`rw_d`, `rs_d`, `cs_d`): a write to the address register is addressed |
| `bd2_rs_n` | believed NOT `rs_d` (its gate is not fully traced) |
| `bd2_x` | second term of the address register load, from the untraced right-hand column |

## Strobe channel gate column (`notes/blocks/bd1.md`)

| Name | What it is |
|---|---|
| `bd1_k#` | tracks of the channel not yet identified (`bd1_k4`, `bd1_k11`) |
| `bd1_a`, `bd1_an` | input and output of inverter A |
| `bd1_n#`, `bd1_q`, `bd1_k` | nodes of the latch gated by `inh_lat` (upper half node, lower half node, output, and the node pulled low by `inh_src`'s line) |

## Central datapath (`notes/blocks/cdp1.md` ... `cdp4.md`)

None of these rows has a register number yet, so all names are by place. Columns are
`c#`, slices `s#`, counted from the left.

| Name | What it is |
|---|---|
| `cdp1_a#_*`, `cdp1_c#_*` | cdp1 rows A and C, static register bit in column #: `_x` storage node (bit line while the write line is high), `_q1` its inverse, `_q` output, `_bl` bit line, `_m#` metal straps of the cell |
| `cdp1_a_wr`, `cdp1_c_wr` | write lines of rows A and C |
| `cdp1_b#_a`, `cdp1_b#_b` | cdp1 row B comparator, slice #: its two inputs |
| `cdp1_b#_n2`, `cdp1_b#_ne` | NOR(a, b) and a XOR b |
| `cdp1_b_eq` | NOR of the five `_ne`: high when the two 5-bit values are equal |
| `cdp1_l#`, `cdp1_lw#` | horizontal lines of the data bus channel, named by their y; and two write-line links |
| `cdp2_a_s#_*` | cdp2 row A (5-bit latch), slice #: `_a` storage node, `_n2` inverse, `_q` output, `_bus` bit line |
| `cdp2_a_c_s#_*` | cdp2 row C (7-bit latch), the same nodes |
| `cdp2_a_ld`, `cdp2_c_ld` | load strobes of rows A and C |
| `cdp2_a_s#`, `cdp2_c_s#`, `cdp2_c_s#_bus` | per-slice lines and bit lines of those rows |
| `cdp2_b_s#`, `cdp2_b_s#_*` | cdp2 row B comparator with a ripple chain, slice #: `_y` = NOR(q, t), `_ne` = q XOR t, `_x` chain output of the slice, `_o2` inverse of the previous slice's chain output, `_p1` internal node |
| `cdp2_b_cin`, `cdp2_b_hl` | chain input of that comparator; and a row-long line pulled low per bit |
| `cdp2_trk_s#` | the value that row B compares row C against, per slice (through track) |
| `cdp2_ch#_#` | a line of channel 1, named by its y |
| `cdp3_c_c#_*`, `cdp3_h_c#_*` | cdp3 rows C (6 bit) and H (8 bit), static register bit in column #: `_x`, `_q1`, `_q` as in cdp1 |
| `cdp3_c_wr`, `cdp3_h_wr` | write lines of rows C and H |
| `cdp3_cw_c#`, `cdp3_hw_c#` | west outputs of those bits |
| `cdp3_cq_c#`, `cdp3_hq_c#` | read outputs of those bits, to the pass transistors onto bus N |
| `cdp3_n_c#` | bus N, column # |
| `cdp3_gate_e`, `cdp3_gate_f` | gates of the read pass transistors of rows E (row C onto bus N) and F (row H onto bus N) |
| `cdp3_bl_c#`, `cdp3_f_c#`, `cdp3_g_c#` | column lines e (bit line), f and g |
| `cdp3_k_a`, `cdp3_k_b`, `cdp3_k_c` | lines of the NAND beside row C |
| `cdp3_l#` | a line of channel B, named by its y |
| `cdp4_lc_s#_*`, `cdp4_lr_s#_*`, `cdp4_ldr_s#_*` | cdp4 latch rows C (8 bit), R1-lower (8 bit, upside down) and D (6 bit), slice #: `_a` storage node, `_n2` inverse, `_q` output, `_x2` internal strap |
| `cdp4_ld`, `cdp4_ld#b`, `cdp4_ld#` | load strobes of those rows (C, R1-lower, D) |
| `cdp4_in_s#`, `cdp4_in#b_s#`, `cdp4_in#_s#` | data inputs of those rows |
| `cdp4_n_s#` | output node of the 4-way selector, slice # |
| `cdp4_a_s#`, `cdp4_b_s#`, `cdp4_c_s#`, `cdp4_d_s#` | the selector's four sources per slice |
| `cdp4_sel#` | the four select lines of the selector |
| `cdp4_rst` | gate of the pull-down on the selector node |
| `cdp4_bus_s#` | the eight poly lines of channel 1 |

## Left array (`notes/blocks/larr.md`): the 14-bit memory address counter

Row tags `s0` ... `s13` are rows from the top; which MA bit each is has not been fixed.

| Name | What it is |
|---|---|
| `larr_n#_s#` | inverters of the row: `_n2` = the stored bit Q, `_n3` = NOT(carry-in XOR Q), `_n4`, `_n5` = the value sampled into the latch part |
| `larr_g#_s#` | storage node of the bit (`g6`) |
| `larr_x#_s#` | `_x1` dynamic node that takes the incremented or the loaded value; `_x2` = NOT `larr_ld` |
| `larr_ld_s#` | value offered for loading, from the right |
| `larr_y_s#`, `larr_z_s#` | new value leaving to the right; value written back to the bit |
| `larr_a_s#`, `larr_mid_s#` | internal nodes of the incrementer |
| `larr_cin_s#`, `larr_cout_s#` | carry in and out of a row |
| `larr_h_s#` | line H along a row boundary |
| `larr_l#_g#`, `larr_l#nc_s#` | group carry lines and their pieces |
| `larr_vm#` | vertical control lines Vm1-Vm6 of the latch part (clear, count, load, tied off, transfer, write) |

## Top-centre island and bottom-centre block

| Name | What it is |
|---|---|
| `tc1_l#_out`, `tc1_r#_out` | outputs of the left and right gate columns of the nine-gate island |
| `tc1_b`, `tc1_g`, `tc1_i`, `tc1_w#`, `tc1_x#` | its inputs and channel lines |
| `tc1_ns#` | north-south lines ns1-ns6 east of the island |
| `bc1_s#`, `bc1_s#_n` | the two bus lines the 2-bit decoder decodes, and their inverses |
| `bc1_dec#_n` | decoder outputs, active low (00, 10, 01) |
| `bc1_ld_in#`, `bc1_ld_n`, `bc1_ld_a` | inputs, NAND output and twin output of the driver of cdp4's row D strobe |
| `bc1_d#` | data lines 3-6 into cdp4's row D |
| `bc1_g#_in`, `bc1_g#_out` | input and output of inverter 6 |

## Odd ones

| Name | What it is |
|---|---|
| `rdp#_n#s#`, `rdp#_t#` | two short pieces of bundle wiring in the right datapath, named by track and position |

## Former names

Names used before 2026-11-17, for reading older commits; `tools/rename.py` adds a line for
every later rename. Row tags of the counter cells changed with the names: r18...r11 became
hc0...hc7, r10...r4 became rc0...rc6, r3...r0 became c4b0...c4b3; slice tags of the lower right
datapath s1...s7, s0 became b0...b6, b7.

| Old | New | Example |
|---|---|---|
| areg_load | ar_load | |
| bd2_a | wr_data_sel_n | |
| bd2_al_n | ar_load_n | |
| bd3_b12 | rsel12_buf | |
| bd2_c | wr_data_sel | |
| bd1_g | inh_src | |
| bd1_k7 | h_eq_r0_u | |
| bd1_k8 | h_eq_r1_u | |
| bd1_k5 | h_eq_r0half | |
| bd1_k14 | hc3 | |
| bd1_k17 | hc0 | |
| bd1_k9 | hc2 | |
| bd2_m255 | bd2_rs_n | |
| bd2_m210 | wr_addr_sel | |
| bd3_n12 | rsel12_bufn | |
| bd2_n1 | wr_data_lat | |
| bd2_nu | wr_data_e_n | |
| bd2_qb | wr_data_lat_n | |
| bd1_x | inh_n | |
| bd1_xn2 | inh_lat | |
| bd1_xn1 | inh_rc | |
| ck_src | inh_ck | |
| mra_a_r# | c#b#_m | mra_a_r0 -> c4b3_m |
| mra_a_r# | hc#_m | mra_a_r11 -> hc7_m |
| mra_a_r# | rc#_m | mra_a_r10 -> rc0_m |
| mra_b_r# | c#b#_mb | mra_b_r0 -> c4b3_mb |
| mra_b_r# | hc#_mb | mra_b_r11 -> hc7_mb |
| mra_b_r# | rc#_mb | mra_b_r10 -> rc0_mb |
| mra_busa | cnt_bus_a | |
| mra_busb | cnt_bus_b | |
| mra_busg | h_eq_r2_u | |
| mra_cin_r3 | c4b_ci | |
| mra_cin_r18 | hc_ci | |
| mra_cin_r10 | rc_ci | |
| mra_cka2 | ck_a_u | |
| mra_ckb | ck_b | |
| mra_d_r# | c#b#_d | mra_d_r0 -> c4b3_d |
| mra_d_r# | hc#_d | mra_d_r11 -> hc7_d |
| mra_d_r# | rc#_d | mra_d_r10 -> rc0_d |
| mra_g#_r# | c#b#_q_n | mra_g1_r0 -> c4b3_q_n |
| mra_g#_r# | hc#_q_n | mra_g1_r11 -> hc7_q_n |
| mra_g#_r# | rc#_q_n | mra_g1_r10 -> rc0_q_n |
| mra_gab | cnt_gab | |
| mra_gla | rc_lo4_set | |
| mra_glb | hc_lo4_set | |
| mra_l2a | cnt_l2_a | |
| mra_l2b | cnt_l2_b | |
| mra_l2c | cnt_l2_c | |
| mra_l3m | rc_l3 | |
| mra_l3n | c4b_l3 | |
| mra_la | cnt_la_a | |
| mra_la2 | cnt_la_b | |
| mra_la3 | cnt_la_c | |
| mra_m7 | rc_ck_m | |
| mra_m_r# | c#b#_nx | mra_m_r0 -> c4b3_nx |
| mra_m_r# | hc#_nx | mra_m_r11 -> hc7_nx |
| mra_m_r# | rc#_nx | mra_m_r10 -> rc0_nx |
| mra_md_r# | c#b#_md | mra_md_r0 -> c4b3_md |
| mra_md_r# | hc#_md | mra_md_r11 -> hc7_md |
| mra_md_r# | rc#_md | mra_md_r10 -> rc0_md |
| mra_mt_r0 | c4b3_mt | |
| mra_mt_r# | hc#_mt | mra_mt_r11 -> hc7_mt |
| mra_n#_r# | c#b# | mra_n1_r0 -> c4b3 |
| mra_n#_r# | c#b#_ci_n | mra_n2_r0 -> c4b3_ci_n |
| mra_n#_r# | hc# | mra_n1_r11 -> hc7 |
| mra_n#_r# | hc#_ci_n | mra_n2_r11 -> hc7_ci_n |
| mra_n#_r# | rc# | mra_n1_r10 -> rc0 |
| mra_n#_r# | rc#_ci_n | mra_n2_r10 -> rc0_ci_n |
| mra_na_r# | c#b#_nx_g | mra_na_r0 -> c4b3_nx_g |
| mra_na_r# | hc#_nx_g | mra_na_r11 -> hc7_nx_g |
| mra_na_r# | rc#_nx_g | mra_na_r10 -> rc0_nx_g |
| mra_nb_r# | c#b#_nx_n | mra_nb_r0 -> c4b3_nx_n |
| mra_nb_r# | hc#_nx_n | mra_nb_r11 -> hc7_nx_n |
| mra_nb_r# | rc#_nx_n | mra_nb_r10 -> rc0_nx_n |
| mra_p#_r# | c#b#_m_n | mra_p3_r0 -> c4b3_m_n |
| mra_p#_r# | hc#_m_n | mra_p3_r11 -> hc7_m_n |
| mra_p#_r# | rc#_m_n | mra_p3_r10 -> rc0_m_n |
| mra_q_r# | c#b#_q | mra_q_r0 -> c4b3_q |
| mra_q_r# | hc#_q | mra_q_r11 -> hc7_q |
| mra_q_r# | rc#_q | mra_q_r10 -> rc0_q |
| mra_rb_r# | c#b#_rb | mra_rb_r0 -> c4b3_rb |
| mra_rb_r# | hc#_rb | mra_rb_r11 -> hc7_rb |
| mra_rb_r# | rc#_rb | mra_rb_r10 -> rc0_rb |
| mra_s7 | rc_ck_s | |
| mra_tab_r# | c#b#_tab | mra_tab_r0 -> c4b3_tab |
| mra_tab_r# | hc#_tab | mra_tab_r11 -> hc7_tab |
| mra_tab_r# | rc#_tab | mra_tab_r10 -> rc0_tab |
| mra_x_r# | c#b#_co | mra_x_r0 -> c4b3_co |
| mra_x_r# | hc#_co | mra_x_r11 -> hc7_co |
| mra_x_r# | rc#_co | mra_x_r10 -> rc0_co |
| mra_z_r# | c#b#_z | mra_z_r0 -> c4b3_z |
| mra_z_r# | hc#_z | mra_z_r11 -> hc7_z |
| mra_z_r# | rc#_z | mra_z_r10 -> rc0_z |
| rdp3_ar_ld | ar_load | |
| rdp#_ar_s#_a | ar#_a | rdp3_ar_s1_a -> ar0_a |
| rdp#_ar_s#_n# | ar#_n# | rdp3_ar_s1_n2 -> ar0_n2 |
| rdp#_ar_s#_q | ar#_q | rdp3_ar_s1_q -> ar0_q |
| rdp#_ar_s#_trk | ar#_trk | rdp3_ar_s1_trk -> ar0_trk |
| rdp#_bus_s# | rbus_b# | rdp3_bus_s0 -> rbus_b7 |
| rdp#_c_s# | hc# | rdp3_c_s0 -> hc7 |
| rdp#_c_s# | hc#_u | rdp3_c_s1 -> hc0_u |
| rdp3_ca_eq | h_eq_r1 | |
| rdp#_ca_s#_nor | r#c_b#_nor | rdp3_ca_s0_nor -> r1c_b7_nor |
| rdp#_ca_s#_x | r#c_b#_x | rdp3_ca_s0_x -> r1c_b7_x |
| rdp3_cb_eq | h_eq_r2 | |
| rdp#_cb_s#_nor | r#c_b#_nor | rdp3_cb_s0_nor -> r2c_b7_nor |
| rdp#_cb_s#_x | r#c_b#_x | rdp3_cb_s0_x -> r2c_b7_x |
| rdp2_cc_eq | h_eq_r0 | |
| rdp#_cc_s#_nor | r#c_b#_nor | rdp2_cc_s0_nor -> r0c_b7_nor |
| rdp#_cc_s#_x | r#c_b#_x | rdp2_cc_s0_x -> r0c_b7_x |
| rdp2_cd_eq | h_eq_r0half | |
| rdp#_cd_s#_nor | r#hc_s#_nor | rdp2_cd_s1_nor -> r0hc_s1_nor |
| rdp#_cd_s#_x | r#hc_s#_x | rdp2_cd_s1_x -> r0hc_s1_x |
| rdp2_ce_eq | uc_eq_r4 | |
| rdp#_ce_s#_nor | r#c_s#_nor | rdp2_ce_s0_nor -> r4c_s0_nor |
| rdp#_ce_s#_x | r#c_s#_x | rdp2_ce_s0_x -> r4c_s0_x |
| rdp2_ce_sm1_nor | r4c_sm1_nor | |
| rdp2_ce_sm1_x | r4c_sm1_x | |
| rdp3_n4 | rc0 | |
| rdp3_n5 | rc1 | |
| rdp3_n6 | rc2 | |
| rdp3_n8 | rc3 | |
| rdp3_ra_ld | wr_r1_u | |
| rdp#_ra_s#_a | r#_b#_a | rdp3_ra_s0_a -> r1_b7_a |
| rdp#_ra_s#_n# | r#_b#_n# | rdp3_ra_s0_n2 -> r1_b7_n2 |
| rdp#_ra_s#_q | r#_b#_q | rdp3_ra_s0_q -> r1_b7_q |
| rdp3_rb_ld | wr_r2_u | |
| rdp#_rb_s#_a | r#_b#_a | rdp3_rb_s0_a -> r2_b7_a |
| rdp#_rb_s#_n# | r#_b#_n# | rdp3_rb_s0_n2 -> r2_b7_n2 |
| rdp#_rb_s#_q | r#_b#_q | rdp3_rb_s0_q -> r2_b7_q |
| rdp3_rc_ld | wr_r0_u | |
| rdp#_rc_s#_a | r#_b#_a | rdp3_rc_s0_a -> r0_b7_a |
| rdp#_rc_s#_n# | r#_b#_n# | rdp3_rc_s0_n2 -> r0_b7_n2 |
| rdp#_rc_s#_q | r#_b#_q | rdp3_rc_s0_q -> r0_b7_q |
| rdp2_re_ld | wr_r4_u | |
| rdp#_re_s#_a | r#_s#_a | rdp3_re_s0_a -> r4_s0_a |
| rdp#_re_s#_n# | r#_s#_n# | rdp3_re_s0_n2 -> r4_s0_n2 |
| rdp#_re_s#_q | r#_s#_q | rdp3_re_s0_q -> r4_s0_q |
| rdp3_re_sm1_a | r4_sm1_a | |
| rdp3_re_sm1_n2 | r4_sm1_n2 | |
| rdp3_re_sm1_q | r4_sm1_q | |
| rdp2_rf_ld | wr_r6 | |
| rdp#_rf_s#_a | r#_s#_a | rdp3_rf_s0_a -> r6_s0_a |
| rdp#_rf_s#_n# | r#_s#_n# | rdp3_rf_s0_n2 -> r6_s0_n2 |
| rdp#_rf_s#_q | r#_s#_q | rdp3_rf_s0_q -> r6_s0_q |
| rdp3_rf_sm1_a | r6_sm1_a | |
| rdp3_rf_sm1_n2 | r6_sm1_n2 | |
| rdp3_rf_sm1_q | r6_sm1_q | |
| rdp3_s0 | inh_rc | |
| rdp#_ubus_s# | ubus_s# | rdp2_ubus_s0 -> ubus_s0 |
| rdp2_ubus_sm1 | ubus_sm1 | |
| rdp#_uc_s# | uc_s# | rdp2_uc_s0 -> uc_s0 |
| rdp2_uc_sm1 | uc_sm1 | |
| sel_b# | rsel#_buf | sel_b13 -> rsel13_buf |
| sel_bn# | rsel#_bn | sel_bn13 -> rsel13_bn |
| sel_n# | rsel#_n | sel_n0 -> rsel0_n |
| sel_stb_l | wr_stb_n | |
| sel_stb_r | wr_stb_n | |
| sel_w# | wr_r# | sel_w0 -> wr_r0 |
| t_g0_in | inh_n | |
| t_g0_out | inh_ck | |
| tla_a2 | rcs_a2 | |
| tla_b1 | rcs_b1 | |
| tla_c1 | rcs_c1 | |
| tla_e# | rcs_e# | tla_e3 -> rcs_e3 |
| tla_in# | rcs_in# | tla_in1 -> rcs_in1 |
| tla_m2 | rcs_m2 | |
| tla_thin | rcs_thin_e | |
| tla_thinw | rcs_thin_w | |
| tla_w2 | rcs_w2 | |
| tla_x1 | rcs_x1 | |
| wl_b | rc_stepreq_n | |
| wl_d_buf | rc_ck_s_dly | |
| wl_d_n | rc_ck_s_n | |
| wl_e_buf | rc_ck_m_dly | |
| wl_e_n | rc_ck_m_n | |
| wl_la_n | cnt_la_a_n | |
| wl_p | rc_step | |
| wl_pb | rc_step_n | |
| h_eq_r0_u | h_eq_r0 | |
| h_eq_r1_u | h_eq_r1 | |
| rcs_ba4100 | rcs_cond | |
| rcs_cm4028 | rcs_cond_lat | |
| rcs_m2 | rcs_cond_n | |
| rcs_bb3807 | rcs_stb | |
| rcs_stb_n | ck_out | |
| rcs_stb | clk_tl | |
