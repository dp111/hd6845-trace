# HD6845S die trace: plan

Goal: recover the complete internal logic of the Hitachi HD6845S CRTC (die marking
`HD46505S`) from the two die photographs, down to transistor level, and express it as

- an annotated polygon trace of the die (SVG),
- a transistor netlist and a gate-level netlist derived from it,
- schematics that show every latch, flip-flop, counter, comparator, PLA and glue gate,
- a reference model that is checked against the netlist and reproduces the
  undocumented edge-case behaviour.

Status: plan only. Nothing below is traced yet; "provisional" marks things seen during
reconnaissance that still need proper tracing.

## 1. What reconnaissance established

| Item | Finding |
|---|---|
| Images | `hd6845metal2ndchip.jpg` 19838 x 21025 (metal intact), `hd6845acid2ndchip.jpg` 19857 x 21029 (metal stripped) |
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

- `out/hd6845s.svg`: all layers plus net labels, in metal-shot coordinates, with the
  die photo as a linked background and Inkscape layers.
- Transistor netlist: poly over diffusion makes a channel, contacts join layers.
- Check reports (section 3.3).

### 3.2 How the tracing is done

1. **Proposal.** Try automatic segmentation for the layers where it looks reliable:
   metal from the metal shot, poly from the acid shot, contact candidates by template.
   The pilot decides which of these are good enough to use as a starting point.
   Anything unreliable is drawn by hand.
2. **Correction.** I view each region at 1x-2x in both shots with a coordinate grid
   and the current trace overlaid, fix the proposal, add diffusion and contacts, and
   label nets.
3. **Repetition.** Most of the die is bit-slices. Each distinct cell is traced once,
   stamped at every instance, and each instance is compared with the master in image
   space. Only the flagged differences are inspected by eye.
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
block; a detailed block diagram; the annotated full-die SVG; a write-up of findings
and of every disagreement with the datasheet, the CPC document and beebjit; a
reference emulation model run in lock-step against the netlist simulation; comparison
with Lance Ewing's work.

Order within M3 and M4 will follow the signals outward from M1 and M2 rather than a
fixed list, so that every block is entered from nets that are already named.

## 5. Repository layout

```
dieshots/ datasheets/ docs/   inputs (not in git yet, see section 7)
cache/                        derived image data, regenerated by tools/prepare.py
tools/                        cropping, overlay, build, extraction, checks
trace/                        source-of-truth geometry
out/                          generated SVG, netlists, reports
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

## 7. Open decisions

1. Whether the die shots (190 MB) and the third-party PDFs go into the repository,
   and whether the repository stays private.
2. Language of the final reference model. Default: structural Verilog for the exact
   netlist plus a C model for emulator use.
3. Whether to run M3-M4 regions in parallel with multiple agents once the conventions
   are fixed. Faster, costs more tokens. Default: serial.
4. Whether a browsable deep-zoom viewer (tiled photos with the trace overlaid and
   clickable nets) is wanted alongside the SVG. Default: yes, as a late addition,
   because a 400-megapixel overlay is hard to review any other way.
