# HD6845S die trace: plan

Goal: recover the complete internal logic of the Hitachi HD6845S CRTC (die marking
`HD46505S`) from the two die photographs, down to transistor level, and express it as

- an annotated polygon trace of the die (SVG),
- a transistor netlist and a gate-level netlist derived from it,
- schematics that show every latch, flip-flop, counter, comparator, PLA and glue gate,
- a floor-plan overlay on the die photo showing where each register, counter,
  comparator and PLA sits and what each patch of random logic does,
- a reference model that is checked against the netlist and reproduces the
  undocumented edge-case behaviour.

Status (2026-11-15, night): M0 done. M1 done except the data pad cell and pad-ring
wiring. M2 largely done (address register, decode, strobe logic; data bus interface
partly). M3 about half done, by a round of parallel agents: 2,593 transistors traced
in seventeen blocks. M4 (control logic) barely started. See `notes/journal.md` and
`notes/work-packages.md`. "Provisional" marks things that still need proper tracing.

## 1. What reconnaissance established

| Item | Finding |
|---|---|
| Images | Chip 2: `hd6845metal2ndchip.jpg` 19838 x 21025 (metal intact, the reference frame), `hd6845acid2ndchip.jpg` (metal stripped). Chip 1, added later: `hd6845metal.jpg`, `hd6845acid.jpg`, `hd6845acid2.jpg`; the last is a clean stripped shot and is the best single source for poly and diffusion |
| Registration | Already aligned. A feature at metal (x, y) is at acid (x + 12.70 - 0.000096x - 0.000167y, y + 7.80 + 0.000140x - 0.000107y), i.e. about (+10, +8) mid-die. Affine fit residual under 1 px RMS over 24 patches, so no stitching tears between the two |
| Scale | Bit-slice pitch about 390 px, signal metal 20-25 px wide, contacts 30-40 px. Wiring is readable at 0.5x, transistors at 1x-2x |
| Process | Silicon-gate NMOS, one metal layer |
| Layer appearance | Metal: bright speckled yellow (metal shot). Poly: orange granular bands (both shots). Diffusion: dark-outlined regions, same hue as field. Contacts: ringed squares (metal shot), white pitted squares (acid shot). Not yet determined: buried contacts, whether depletion implants are visible |
| Pads (provisional) | 40 pads. VSS = top-middle pad at about (9000, 1050), sitting in the peripheral metal plane. VCC = bottom-middle at about (9030, 19880). Pin numbers run counter-clockwise from VSS, which matches the pad count per side: 18 pads between VSS and VCC down the left (RES, LPSTB, MA0-13, DISPTMG, CUDISP) and 20 up the right (CLK, R/W, E, RS, CS, D7-D0, RA4-RA0, HSYNC, VSYNC) |
| Register decode (provisional) | NOR-array structure at about x 14200-15750, y 13500-14650: about 18 column lines by 5 row pairs, the right shape for a 5-bit address to R0-R17 decoder |
| Test structures | Top right, around (15000-17500, 2400-3600): process monitors, not part of the circuit |
| Datasheet | Scan, no text layer. p1 pinout, p7 block diagram, p9 register table, p15-19 timing charts, p40 reset sequences, p41 anomalies when rewriting registers, p42-43 HD6845R vs S differences |

All coordinates in this project are pixel coordinates of the **metal shot**
(`hd6845metal2ndchip.jpg`), origin top-left.

## 2. Ground rules

1. Trace independently. Lance Ewing's work, and any other 6845 reverse engineering, is
   not opened until my own trace of the relevant block is finished, and then only as
   confirmation (milestone M6).
2. The datasheet, the CPC "ACCC" document (CRTC type 0) and beebjit are evidence of
   behaviour, not ground truth. Where the silicon disagrees, the silicon wins and the
   disagreement is written up.
3. Ambiguities are logged, not guessed away: each gets an ID, coordinates, the
   candidate readings, the working assumption and what would settle it. Assumed
   geometry is flagged in the trace so it renders differently and can be found again.
4. Names come from pin names, register numbers and counter numbers: `c0_eq_r0`,
   `r9_b3`, `c4_q[6:0]`, `ma_q[13:0]`. Counters use the CPC document's numbering (C0
   horizontal, C4 row, C9 raster, C3l/C3h sync widths, C5 vertical adjust) where a
   counter matches one.
5. N-bit comparators, registers and counters may be drawn as blocks once one bit is
   understood, but everything that defines behaviour is kept at gate level: carry and
   reset style, which clock phase samples each comparator output, every derived
   signal, latch and flip-flop.

## 3. Method

### 3.1 Trace representation

The source of truth is plain-text geometry in `trace/`, one file per region or cell,
kept in git. Layers: diffusion, poly, metal, contact, buried contact (if the process
has them), implant (if visible), labels. Wires are paths with a width, areas are
polygons, contacts are points. Everything else is generated from it:

- `out/hd6845s.svg`: all layers plus net labels, in metal-shot coordinates, with both
  die photos as linked background layers and Inkscape layers.
- `out/netlist.json`: poly over diffusion makes a channel, contacts join layers.
- `out/report.txt`: rule checks and recovered gates (section 3.3).
- `out/floorplan.jpg` and `out/floorplan.svg`: the functional blocks listed in
  `floorplan.txt`, outlined and labelled over the die photo. Coarse and provisional
  after M0; each block is renamed and tightened as it is traced.

`python3 tools/build.py` regenerates all of these.

### 3.2 How the tracing is done

1. **Hand entry.** I view each region at about 2.5x in both shots with a coordinate
   grid, write the geometry, render it back over the photos and correct it. Automatic
   segmentation was tried in M0 and dropped: edges of the layers underneath print
   through the metal and cut every wire into fragments (`notes/layers.md`).
2. **Repetition.** Most of the die is bit-slices. Each distinct cell is traced once
   (`@cell`), stamped at every instance (`@inst`, with mirroring), and each instance is
   checked against the photo. The pilot showed a mirrored gate pair landing within a
   few pixels. Cells should hold the repeated core only; wiring that differs between
   instances is traced separately.
3. **Image-space instance check** (to build at the start of M3): compare each
   instance's photo patch with the master's and inspect only the flagged differences.
4. **Random logic** has no shortcut and is traced polygon by polygon. This is where
   the interesting behaviour lives and where most of the effort goes.

### 3.3 Verification, in increasing strength

1. Overlay review of every traced region against both shots.
2. Coverage checks: metal, poly or contacts present in the image but absent from the
   trace, and trace edges with no image edge under them.
3. Cell-instance diffing (3.2 step 3).
4. Electrical rule checks on the netlist: floating gates, undriven nodes, VCC-VSS
   shorts, single-terminal nodes, gates that only partly cross diffusion, loads that
   are not wired as loads.
5. Logic recovery: every region must resolve into sane NMOS structures (load plus
   pull-down network, pass-gate latch, cross-coupled pair, PLA). A region that does
   not is suspect.
6. Switch-level simulation of the whole netlist against the datasheet timing charts,
   then the CPC type-0 cases and beebjit's behaviours. Each mismatch sends me back to
   the die at the relevant coordinates; the outcome is either a trace fix or a
   documented disagreement with the reference.
7. Optional: an independent second trace of the critical control logic by a fresh
   agent that has not seen my netlist, then a netlist diff.
8. Last: comparison with Lance Ewing's work, and tests on real hardware for anything
   the netlist predicts that nobody has documented.

### 3.4 Records

- `notes/journal.md`: what was done each session and what is next.
- `notes/ambiguities.md`: the ambiguity register (rule 3).
- `notes/layers.md`, `notes/pads.md`, `notes/blocks/*.md`: findings per topic.

## 4. Milestones

**M0. Groundwork and pilot.**
Acid shot resampled into the metal frame; crop, side-by-side and overlay tools; layer
legend with example coordinates; trace format, netlist extractor, rule checker and
SVG generator working end to end on one small circuit (the buffer beside the top pads
at about (7000-7800, 1600-2050)); segmentation experiments; coarse floor plan of the
die from repetition analysis.
Exit: one circuit goes photo to polygons to netlist to gates, and I have a measured
tracing rate.

**M1. Pad ring and I/O.**
All 40 pads identified from VSS/VCC and the pinout; power rails traced; every input
buffer, output driver and data-bus driver traced to a named internal signal; internal
clock phases derived from CLK.

**M2. Bus interface and register decode.**
E/CS/RS/R/W decode, the 5-bit address register, the decode PLA, write strobes and the
read path (which registers read back, and what the others return). Following each
select line locates every register on the die.

**M3. Datapath cells.**
Register, counter and comparator bit cells; the MA counter and row-start latch; cursor
compare; light-pen latch. Output: which bits of each register physically exist, and
the carry and reset style of each counter.

**M4. Control logic.**
- Horizontal: C0 wrap, display-enable latch, HSYNC set/reset and width counter, the
  R0/2 comparison used by interlace.
- Vertical: C9 and C4, vertical adjust, the end-of-frame sequence (including the
  three-cycle sequence at the start of the last scanline), VSYNC start and width.
- Interlace: field flip-flop, the odd/even half line, VSYNC half-line delay, RA
  generation in interlace sync-and-video mode.
- DISPTMG and CUDISP skew pipelines, cursor start/end/blink, blink divider, light-pen
  synchroniser, reset.
- For every comparator: what its output feeds and on which phase. This is what
  explains why some registers hold N and others N-1.

**M5. Integration and simulation.**
Whole-chip netlist passing the rule checks; simulator programs the registers through
the real bus timing and produces frames; validation against the three references.

**M6. Schematics, model, write-up, cross-check.**
Structural Verilog as the exact machine-checkable schematic; SVG schematic sheets per
block, in which N-bit registers, comparators, counters, selectors and similar repeated
structures are drawn as blocks, **plus one gate-level sheet for one instance of each
kind of such structure** (one register bit with its strobe gating, one comparator
slice with its match line, one counter bit with its carry chain, one pad driver, and so
on; user request 2026-11-15); a detailed block diagram; the annotated full-die SVG; a write-up of findings
and of every disagreement with the datasheet, the CPC document and beebjit; a
reference emulation model run in lock-step against the netlist simulation; comparison
with Lance Ewing's work.

**M7. Visual 6845 (added 2026-11-15, user request).**
A browser page in the manner of the transistor-level "visual" chip simulators: the
traced layout drawn from `out/`, every node clickable, a switch-level simulation of the
extracted netlist running in the page with the nodes coloured by state, the pins driven
by a small bus/clock script, and the registers, counters and outputs shown as they
change. It needs **every transistor traced**: nothing may stay a black box, including
the comparators, the pad drivers and the input protection (schematics may still draw a
comparator as a block; the trace and the netlist may not). It also needs every node as
polygons with a stable number, which the trace already is. The deep-zoom viewer
(decision 4) becomes the same page: photos underneath, layout and simulation on top.

Order within M3 and M4 will follow the signals outward from M1 and M2 rather than a
fixed list, so that every block is entered from nets that are already named.

## 5. Repository layout

```
dieshots/ datasheets/ docs/   inputs
cache/                        derived image data (not in git): tools/prepare.py, tools/align.py
tools/                        view, tracelib, netlist, build, align, prepare
trace/                        source-of-truth geometry, and align.json
floorplan.txt                 functional blocks for the floor-plan overlay
out/                          generated SVG, netlist, report, floor plan
sim/                          switch-level simulator and tests
model/                        Verilog and reference model
schematics/                   SVG sheets
notes/                        journal, ambiguities, findings
```

## 6. Risks

- **My error rate.** Reading thousands of features from crops will produce mistakes.
  The plan assumes this and leans on the checks in 3.3 rather than on care alone.
- **Depletion vs enhancement** may not be visible. If so it is inferred from topology
  (gate tied to source, drain on VCC) and every inference is listed.
- **Obscured spots**: bond debris on pads, dirt, and places where neither shot is
  clear. These go in the ambiguity register.
- **Dynamic logic.** If the chip stores state on gate capacitance, the simulator must
  model charge retention; the netlist alone will show whether it does.
- **Scale.** The transistor count is unknown until the floor plan is done. M0-M2 are
  the calibration; I will report the measured rate after M2.

## 7. Decisions

1. The die shots and the PDFs are committed. The repository is private.
2. Final reference model: structural Verilog for the exact netlist plus a C model for
   emulator use.
3. Tracing is serial for now. Parallel agents for M3-M4 to be reconsidered after M2.
4. A browsable deep-zoom viewer (tiled photos with the trace overlaid and clickable
   nets) is the final task.
5. A functional floor-plan overlay is a deliverable, kept up to date throughout.
6. A "visual 6845" is a deliverable once everything is traced (M7), so the trace must
   end with all transistors in it: complete coverage of the die, not only the logic
   needed to explain behaviour.
