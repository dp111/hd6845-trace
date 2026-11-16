# Tracing guide

For anyone (human or agent) tracing a block of the HD6845S die. Read all of it before
starting. It is the distilled experience of the first sessions; most of the traps in
it cost real time to find.

## 1. The job

We are recovering the exact transistor-level circuit of the chip from die photos, as
polygons in plain-text trace files. A tool extracts a transistor netlist from the
polygons and recognises gates. The end product is a schematic exact enough to emulate
undocumented behaviour, so **a wrong connection is worse than a missing one**.

Rules that override everything else:

- Trace what the photos show. Never fill a gap with what a circuit "should" be. If
  you cannot see how something connects, mark it uncertain (`?`) and write it down.
- Do not consult any other reverse-engineering of the 6845 (Lance Ewing's or anyone
  else's), and do not use the web at all. The datasheet (`cache/ds/p-NN.png`, block
  diagram on p-07, register table p-09) and the CPC document (`cache/accc.txt`, large:
  grep it, do not read it whole) describe behaviour; treat them as evidence, not truth.
- Several agents share this working tree. Touch only your own files (section 10).

## 2. Coordinates, photos, tools

All coordinates are pixels of the chip-2 metal photo, origin top-left, x right, y down
(19838 x 21025). Every photo has been resampled into that frame.

| Layer name | What it is | Use it for |
|---|---|---|
| `metal` | chip 2, metal intact | metal wires and their contacts |
| `metal1` | chip 1, metal intact | second opinion on metal; often shows outlines under wide metal better |
| `acid1b` | chip 1, metal stripped, **clean** | the main source for poly and diffusion, also under where metal was |
| `acid` | chip 2, metal stripped | poly in open areas (orange, unmistakable); has interference fringes under wide metal |
| `acid1` | chip 1, metal stripped, some fringes | rarely needed |

Run every tool through the wrapper, which selects your trace file and your scratch
folder (`cache/scratch/BLOCK/`):

```
tools/t.sh BLOCK quad.py X Y W H --scale S [--grid N] [--layers a,b,c,d] [--notrace] --out NAME.png
tools/t.sh BLOCK view.py X Y W H --scale S --layers acid1b [--grid N] [--trace --nofill] [--stack v] --out NAME.png
tools/t.sh BLOCK netlist.py
```

- `quad.py` shows layers of one region side by side: by default `metal` and `acid1b`
  with your trace outlined on the second. `--layers metal,acid,acid1b,acid1b` gives
  four panels when you need the other shots; `--traceall` outlines the trace on every
  panel (useful to check metal). `view.py` shows one layer, or several
  with `--layers a,b --stack v`. `--layers edges` shows only outlines present in
  both chip-2 shots. Three layers go in one row (keep W x S under 430).
- `mosaic.py X Y W H --offsets "0,0 dx,dy ..." --scale S --layer acid1b --out NAME.png`
  shows the same rectangle at several offsets side by side, to compare repeats.
- `tools/t.sh BLOCK follow.py X Y N|S|E|W [--trace]` follows ONE metal line from a point on
  it (2 px steps, both chips' metal shots, corners and diagonals) and prints corners,
  wide stretches, contact candidates and the end, or the piece as a trace-file `M` line.
  Use it for every long run; then look at its end, at each staircase it went through and
  at each "wide" stretch (traps 13-15). `tla_tracks.py` profiles a straight track for
  breaks; `tla_contacts.py` lists contact candidates on one; `strips.py --layer class`
  shows 3,000 px of a bus in one image.
- For following bundles of parallel wires, `tools/sel_tracks.py` and `tools/sel_cut.py`
  (written by the agent that traced the select logic; read their docstrings) report
  where metal is present along a track or a cut. **Do not trust them for
  connectivity.** `sel_tracks.py` bridges gaps of about 20 px, so where a bundle steps
  sideways it joins two different nets that share a track: that produced a wrong
  register identification. It also reports breaks at contacts, blemishes and poly
  crossings. `tools/rdp3_jogs.py` finds the jogs. Confirm every track by overlay.
- X Y is the top-left corner, W H the size, in die pixels. The tool prints the path of
  the PNG; open it with the Read tool.
- **Keep every image under about 1400 px a side or it is downscaled when read and the
  zoom is wasted.** quad.py puts two panels side by side: keep W x S under 640.
  view.py with one layer: W x S under 1300.
- Useful scales: 0.5-1 to survey and follow wires, 2.5-3 to trace, 4-6 to settle one
  junction. Beyond 2 there is no new detail, only bigger pixels, but junctions are
  easier to judge.
- To look at someone else's finished trace as a worked example, set TRACE yourself:
  `TRACE=examples/pilot tools/t.sh BLOCK quad.py 14268 14880 380 380 --scale 1.7 --out cal.png`

Before tracing anything, render and study these three calibration views (each shows a
verified trace over the clean shot). Compare the four panels until you can name every
feature:

```
TRACE=examples/pilot tools/t.sh BLOCK quad.py 14268 14880 380 380 --scale 1.7 --out cal1.png   # two gates, open area
TRACE=inrow tools/t.sh BLOCK quad.py 14640 18190 640 400 --scale 1.0 --out cal2.png           # gate chain, loads under a VCC band
TRACE=decode tools/t.sh BLOCK quad.py 14200 13500 470 480 --scale 1.35 --out cal3.png         # NOR array
```

The matching trace files (`trace/examples/pilot.txt`, `trace/inrow.txt`) show how the
geometry is written.

## 3. How the chip is built

Silicon-gate NMOS, one metal layer, depletion loads, buried contacts.

- **Transistor**: poly crossing diffusion. Gate length 20-28 px. Nothing else makes a
  transistor.
- **Static gate**: a VCC contact, a diffusion strip down from it, a *load*, the output
  node, then pull-down transistors to a VSS contact. The load is a poly block over the
  strip whose gate is tied to the *output* side by a buried contact (a small box,
  about 30 x 28 px, with a heavy outline at a corner or end of the load poly). That
  tie is how a load is recognised. Weak loads are long (poly block 70 wide x 100 tall
  over a 27 px strip); strong ones short and wide.
- **NOR** = pull-downs side by side between output and VSS. **NAND / AND-OR-invert** =
  pull-downs in series.
- **Buried contact**: poly joined directly to diffusion, no metal. Outputs often leave
  a gate this way and become the gate poly of the next stage.
- **Metal contact**: metal to diffusion or metal to poly, about 30 px square.
- **Pass transistor**: poly crossing a diffusion that is not on a supply; used for
  latches and multiplexers, usually clocked. Expect dynamic latches (pass transistor
  into an inverter gate) in the datapaths.
- One metal layer, so wires cross by ducking under: contact, a short run in poly or
  diffusion, contact.
- **Supplies**: loads go to VCC, pull-downs to VSS. If you cannot follow a rail to a
  known supply, the orientation of the loads tells you which rail is which. Label
  supply metal `vss` / `vcc`; all pieces with those names are joined automatically.
- Big drivers use multi-finger transistors: columns of contacts alternating with long
  gate strips. Draw each group as one diffusion rectangle and one contact rectangle
  per column; that is accurate enough.

## 4. Reading the photos

What a feature looks like depends on the shot and, in the clean shot, on whether metal
was above it. Full notes with coordinates of examples: `notes/layers.md`.

| Feature | `metal` / `metal1` | `acid` | `acid1b` where metal was above | `acid1b` in the open |
|---|---|---|---|---|
| Metal | bright yellow, grainy | gone | - | - |
| Poly | orange-brown, visible only where no metal covers it | orange, granular | salmon, sharp red outline | dark red-brown, textured |
| Diffusion | plain, dark outline | plain tan, dark outline | flat tan, dark outline | green near the die edge, **pink near the centre** |
| Field | plain | greenish | pink | khaki / olive |
| Metal contact | ring in the metal | pitted box | dark specks on diffusion; on poly a paler patch; measures greenish against its surroundings (a test that caught two false contacts) | - |
| Buried contact | small heavy-outlined box | same | same | same |

Traps, all of them real:

1. **The clean shot's colours drift across the die.** Open diffusion is green in the
   bottom rows, pink in the decode array and mauve in the mid-right array; at the top
   of the central datapath diffusion is light tan with or without metal above it and
   the olive pockets are open field. Calibrate locally: find an unmistakable
   structure near where you work (a VCC contact with its load, a row of contacts) and
   see what colour each layer has there.
2. **Metal protected a margin of about 10 px beyond its edges.** A 25 px gap between two
   metal lines shows in `acid1b` only as a thin dark bar across whatever is underneath,
   or as a narrow olive strip with a dark outline. Those bars and strips are not layout.
   Where such a gap crosses poly it can leave a dark ring that looks like a contact;
   a real contact also shows as a ring in the metal shot.
3. A dark line across a metal wire in the metal shots is the edge of something
   *underneath*, not a break in the metal. Likewise, bright green bands in `acid1b`
   inside the arrays are gaps of open field between metal lines, not features.
4. Tan (diffusion under metal) and khaki (field in the open) are close. Check where the
   metal is before calling a tan area diffusion. A narrow diffusion wire in the open
   may show no colour of its own at all, only a strip about 22 px wide between two
   dark edges. The stripped shots also show an etch-boundary line beside every wide
   rail, which is not a feature.
5. Under wide metal, `acid` shows only fringes. Use `acid1b`, and `metal1` for outlines.
6. Automatic alignment of `acid1b` is within about 1 px in random logic but only
   interpolated inside regular arrays; check it against `metal` at a contact before
   measuring anything.
   Under metal, poly over a channel is distinctly brighter (redder) in `acid1b` than
   poly over field: that is how the decode array was read, and it works elsewhere.
7. **Your eye is unreliable for repeated patterns.** In the decode array, impressions at
   2.7x of which crossings had transistors were wrong where a colour measurement was
   right. For arrays, measure (see `tools/pla_read.py`) and cross-check.
8. Poly often runs directly underneath the metal of a *different* net for hundreds of
   pixels. Metal over poly is a connection only where there is a contact.
   Where a poly line ends next to another feature, zoom to 4-6x before deciding whether
   they touch; and when the decision matters, **measure it**: a colour profile across
   the junction (`tools/larr_px.py`, read its docstring) settled junctions that one
   agent had judged wrongly by eye three times. Most wrong readings so far were junctions judged at too low a zoom.
9. If a region will not give a consistent circuit after two honest passes, stop, record
   exactly what is established (with coordinates) and what is not, and move on.
10. **A wiring channel cannot be read from the metal shot.** Between the metal tracks of a
   channel, and directly under them, poly lines of *other* nets run for hundreds of
   pixels: a track ends on a contact, its net carries on in poly beneath the neighbouring
   track and comes back up to metal three tracks away. The metal shots show none of this
   (trap 8 at full scale). Read every channel in `acid1b`, end to end
   (`strips.py --layer acid1b`, and `classmap.py` where the colours are close), and
   account for every track end: a track that stops has gone somewhere. First seen in
   `mrach` (x 13040-13425), where half the nets change track under the metal.
11. **"Drawn once, at full length" is a claim about every crossing.** A rail or clock line
   that looks continuous through an array at 1x may be cut at each routing channel and
   re-fed from somewhere else. In the mid-right array the `ck_a` rail, the master clock
   line and line L3 are each three pieces on three nets. Look at such a line at 3x at
   every channel and row-group boundary before drawing it through.
12. **A line that ends in a widened foot ends *on* something.** Look at 6x for the contact
   or the turn before leaving it as a free end.

13. **A metal that lies on a poly line is not joined to it, however long the overlap.**
   The RES line runs exactly on top of another net's poly for 217 px and stops there; its
   real end is a 90 px arm to a contact one bus line over. Before calling two coincident
   lines one net, find the contact: a pad, a ring in the metal shot, the green patch in
   the clean shot. If none of the three is there, they are two nets.
14. **Where a tool says a line ends, look at the end at 5x in the metal shot.** A line ends
   on a contact; if you see none, the line has turned and the tool missed the corner.
15. **Crossing fields without pads carry no taps.** In the fields where poly rows cross a
   metal bus, the clean shot's colour under the metal drifts between salmon and
   yellow-green by the row, so colour alone finds "contacts" at every crossing. A real tap
   there has a widened pad.

**When a trap turns out to affect work already done**, add the affected blocks to the
"Re-read list" in `notes/work-packages.md` in the same commit that records the finding.
A remark in a journal entry or a report is not enough: nobody re-reads those when
choosing the next task.

## 5. The trace file

One file per block: `trace/BLOCK.txt`. The format is documented at the top of
`tools/tracelib.py`; read that docstring. In short, one shape per line:

```
@block myblock
M 14434,14880 y15300 w=52              # metal path: points, then width. xN / yN move one axis
D 14406,14898:14460,15002              # rectangle on the diffusion layer
P [ 100,100 x150 y130 x100 ]           # polygon
C 14423,14920 14422,15050 s=30x34      # contacts, one per point
B 14520,14927:14550,14955              # buried contact
N P 14328,14890 in_a                   # name the net that owns the poly at this point
?P 100,100:120,160                     # uncertain shape (drawn in yellow)
A 100,100:150,150 kind=clamp           # mark a transistor here: clamp, field (both off in
                                       # normal operation) or hold (weak always-on feedback)
@requires inrow                        # load another file (for cells defined there)
```

- Layers: M metal, P poly, D diffusion, C metal contact, B buried contact.
- Poly over diffusion is a channel unless a `B` covers the overlap. Draw diffusion
  *through* under the gate; the extractor splits it.
- A contact joins the metal over it to the poly under it, or else to the diffusion.
- Comment generously: what each group of shapes is. Someone will have to check it.
- Edge positions are uncertain by about 3 px. Draw shapes that must connect with a
  clear overlap, and shapes that must not with a clear gap (5 px or more). Slivers
  where edges nearly coincide produce warnings.
- Repetition: `@cell NAME tag=T ... @end` defines a cell at its master position;
  `@inst NAME dx,dy [mx=X] [my=Y] [rot=DEG o=x,y] tag=T` places a copy. A label
  containing `{}` gets the tag. **Prefix cell names with your block name.**
- Draw lines that run across many instances (rails, buses, clock lines) once, at full
  length, *outside* the cell; keep in the cell only what belongs to one instance.

## 6. The loop

1. **Survey** your region at 0.5-1x in `metal` and `acid1b`. Find the rails, the rows of
   loads, the repeated units, where wires enter and leave. Write a short inventory in
   your notes file before tracing. In the arrays, first run `findcell.py` with the
   master rectangles of cells other blocks have already traced (restricted to your
   region with `--region`, orientations `0,m0,180,m180`): the latch `rdp3_lat`
   (14597 13010 14987 13280, in `trace/rdp3.txt`) and the static register bit
   `cdp1_reg` (8745 3040 9225 3330, in `trace/cdp1.txt`) recur, some upside down, in
   several rows of both datapaths. A row that matches can reuse the cell by
   `@requires`, after checking how its edges differ.
2. **Trace a piece** (one gate group or one cell): view at 2.5-3x with `quad.py`, write
   the shapes.
3. **Overlay**: `quad.py` again (its last panel outlines your trace on the clean shot)
   and `view.py --layers metal --trace --nofill` for the metal. Every outline should
   sit on a real feature. Inside the piece, anything visible that you have *not*
   traced should be something you can name.
4. **Extract**: `tools/t.sh BLOCK netlist.py`. Fix every error. Read the recovered
   gates: does each transistor belong to a sensible structure? A load with no
   pull-down, a gate output that goes nowhere, a transistor with both ends on the same
   net, are usually tracing mistakes. The list "unnamed open nets" must end up empty:
   each net is either driven and used inside your trace, or named as a port.
5. **Write it down** in your notes file while you still have it in view, and **ship it**
   (section 10). Then the next piece.

Finish pieces completely before starting new ones. A block half-covered by verified
pieces is useful; a block fully covered by unchecked geometry is not.

## 7. Repetition and arrays

Most of the die is repeated cells. Trace a cell once.

- `tools/t.sh BLOCK findcell.py x0 y0 x1 y1 --min 0.5 [--region x0,y0:x1,y1] [--orient 0,m0] [--layer metal|acid1b] --cell NAME`
  finds other copies of a rectangle in any of eight orientations and prints `@inst`
  lines. It can lock onto the wrong period of a periodic structure: check every
  placement by overlay.
- `tools/t.sh BLOCK composite.py NAME x0,y0:x1,y1 --offsets "0,0 dx,dy ..."` builds the
  per-pixel median over the copies, which removes dirt, residue and metal grain. View
  it with `--comp NAME` on view.py / quad.py (coordinates stay those of the master).
  Start NAME with your block name (composites share one folder). Above 4x the median
  is blurrier than a single clean shot; use it for dirt, not for fine junctions. In a
  composite the `acid` layer shows poly even under metal, because the fringes average
  out.
- `tools/rdp3_cmp.py` compares instances as text and costs no images.
- `tools/rdp3_sharp.py` (unsharp mask; three agents found it on a median composite at
  3-5x their most useful view), `tools/cdp2_pt.py` (a colour-and-speckle test for
  whether a contact is present, which reversed one by-eye reading) and `tools/cdp1_sr.py` (read the docstrings). The latter makes a
  sub-pixel-aligned median of the copies of a cell at 3-6x. The agent that wrote it says it is what made a register
  cell readable where the plain composite was too blurred.
- `--shift dx,dy` on view.py / quad.py shows another instance in the master's
  coordinates: use it to compare instances.
- `tools/t.sh BLOCK cellcheck.py CELL [--bbox x0,y0:x1,y1] [--layer acid1b]` compares each
  instance's photo with the master's and tints differences. With `--bbox` it compares
  any rectangle, traced or not, at the instance positions: a cheap way to see whether
  untraced neighbours of a cell also repeat. **Instances are not always identical**: the wiring around a
  repeated core often differs (one bit has an extra gate, the end slice differs). Look
  at every instance at least at low zoom before declaring it a copy.
- Datapath slices repeat every 390.3 px horizontally; two other arrays repeat every
  477 px vertically. Use the offsets findcell reports, not multiples of the pitch.
- Tag instances by position (`s0`, `s1`, ... left to right, or top to bottom) unless you
  have established which is bit 0 (for a counter, the carry direction shows it; say
  how you know).
- Agents working on different parts of one array numbered their slices differently.
  So that blocks can be joined, state at the top of your notes how your tags map to
  the array's **columns**, which are defined by the wide VSS rail in each slice:
  central datapath column cN has its VSS rail at x = 7605 + 390.3 N (N = 0..7); right
  datapath column cN has its VSS rail at x = 14175 + 390 N. A row with fewer than
  eight cells occupies only some columns: say which.
- A programmed array (ROM/PLA) is read by measurement: see `tools/pla_read.py` and
  `notes/blocks/decode.md` for the method and its cross-checks.

## 8. Names and ports

- Lower case, digits, underscore. Prefix your local nets and cells with your block
  name (`areg_q0`, `cdp5600_carry_{}`).
- Use a global name only when you have *traced* the connection to something already
  named, or the identity is certain from structure; say which in your notes.
  Global names so far:

| Name | What |
|---|---|
| `vss`, `vcc` | supplies |
| `clk` | the CLK pin node (after its protection resistor) |
| `clk_b` | CLK buffered, same sense as the pin |
| `ck_out` | main internal clock, NOT CLK, heavily buffered |
| `ck_a` | clock phase, high only while CLK is low |
| `ck_b` | clock phase, high only while CLK is high |
| `e_b`, `e_n` | E buffered, and its inverse |
| `rw_a`..`rw_d`, `rs_a`..`rs_d`, `cs_a`..`cs_d` | R/W, RS, CS through 1, 2, 3, 4 inverters (`_a` and `_c` inverted) |
| `res_b`, `lpstb_b` | RES and LPSTB pins, buffered, same sense as the pin |
| `ar0`..`ar4`, `ar0_n`..`ar4_n` | address lines into the decode array (rows) |
| `rsel0`..`rsel17` | register select lines out of the decode array (columns), high when selected |
| `<pin>_drv_in` | the core signal entering an output driver; the pad is its inverse (`ma0`..`ma13`, `ra0`..`ra4`, `hsync`, `vsync`, `disptmg`, `cudisp`) |

- You will meet clock and control lines whose identity you cannot know locally. Give
  them a local name (`BLOCK_phi1`), note where they enter your block, and move on.
- **Ports.** Every wire that crosses your block's boundary goes in a ports table in your
  notes: local name, layer, the coordinate where it crosses, direction if known
  (driven inside / driven from outside), and what you think it is. Draw each such wire
  right up to the boundary and label it. Blocks are joined later through these tables,
  so they matter as much as the gates.

## 9. What to deliver

1. `trace/BLOCK.txt`: extracts with no errors, no unnamed open nets, uncertain shapes
   marked `?`.
2. `notes/blocks/BLOCK.md`, kept current as you go, with these sections:
   - **Status**: what is traced, what is not, in two or three lines.
   - **Inventory**: the cells / gate groups in the region with coordinates.
   - **Logic**: for each cell or group, the recovered logic in plain equations, the
     latches and what clocks them, and what you believe the function is (keep
     "traced" and "believed" visibly apart).
   - **Ports**: the table from section 8.
   - **Ambiguities**: each with coordinates, the candidate readings, your working
     assumption, and what would settle it.
   - **Not done**: anything in your region you did not get to, with coordinates, so the
     next agent can pick it up without re-surveying.
3. `floorplan.d/BLOCK.txt`: one line per functional piece you have identified, format
   `x0,y0:x1,y1  kind  name | description` with kind one of
   `pad io array pla logic route test power unknown`, prefixed `?` if the function is a
   guess. Example: `7600,5480:10850,5910  array  R1 register (8 bit) | written from the data bus when rsel1; feeds the comparator below`.
   These are drawn over the die photo, so make the names say what the piece *does*.

## 10. Committing, and what not to touch

- Commit and push after every finished piece with
  `tools/ship.sh "Subject line" trace/BLOCK.txt notes/blocks/BLOCK.md floorplan.d/BLOCK.txt`
  It commits exactly the files you name and refuses a trace file that does not parse.
  Subject in the imperative, under 70 characters, saying what was traced
  ("Address register: latch cell traced and placed five times"); add a body with a
  second `-m`-style paragraph by putting a blank line and text inside the same quoted
  message if there is something a reader of the history should know.
- **Never run any other git command that changes anything** (no add, commit, checkout,
  stash, reset, pull, rebase). Others have unsaved work in this tree.
- Yours: `trace/BLOCK*.txt`, `notes/blocks/BLOCK.md`, `floorplan.d/BLOCK.txt`, new
  tools named `tools/BLOCK_*.py`, your scratch folder.
- Not yours: every other file. In particular do not edit `floorplan.txt`,
  `notes/journal.md`, `notes/ambiguities.md`, `PLAN.md`, `CLAUDE.md`, the shared tools,
  or another block's files; do not run `tools/build.py`, `align.py` or `prepare.py`. If
  a shared tool is wrong or missing something, say so in your final report (and copy
  it to `tools/BLOCK_x.py` if you need a variant now).
- If you find that an existing trace of a neighbouring block is wrong, do not fix it:
  record it under Ambiguities with the evidence.
- Do not start sub-agents.

## 11. What is known about the chip

Register and counter widths help recognise datapath rows (from the datasheet; not yet
confirmed in silicon):

| | Width | Function |
|---|---|---|
| R0 | 8 | horizontal total |
| R1 | 8 | horizontal displayed |
| R2 | 8 | horizontal sync position |
| R3 | 4 + 4 | sync widths (horizontal low nibble, vertical high nibble) |
| R4 | 7 | vertical total |
| R5 | 5 | vertical total adjust |
| R6 | 7 | vertical displayed |
| R7 | 7 | vertical sync position |
| R8 | 2 + 2 + 2 | interlace mode (bits 0-1), DISPTMG skew (4-5), cursor skew (6-7) |
| R9 | 5 | maximum raster address |
| R10 | 5 + 2 | cursor start raster, blink mode (bits 5-6) |
| R11 | 5 | cursor end raster |
| R12, R13 | 6, 8 | display start address |
| R14, R15 | 6, 8 | cursor address (readable) |
| R16, R17 | 6, 8 | light pen address (read only) |

Counters expected: horizontal character counter (8 bit), raster counter (5), row
counter (7), vertical adjust counter (5), sync width counters (4 + 4), memory address
counter (14) with a row-start latch (14). Each programmable limit has a comparator.

Already traced (see `notes/blocks/*.md`): the pad ring's output drivers and input
buffers, the clock block (`notes/blocks/clock.md`), the register decode array
(`notes/blocks/decode.md`, with the left-to-right order of the select columns). The
coarse floor plan is `floorplan.txt` (picture: `out/floorplan.jpg`); most of it is
still guesses from shape.

Pads, for orientation: MA0-13 down the left side and along the bottom left, RA0-4 top
right, HSYNC/VSYNC top, DISPTMG/CUDISP bottom, D0-D7 down the right side (D0 at the
top), CLK, R/W, E, RS, CS bottom right, RES and LPSTB top. Table: `notes/pads.md`.

## 12. Pace and context

- **Images are your budget.** You have room for roughly 60 to 80 of them before your
  context is full, and an image costs in proportion to its area: a 1300 x 650 view
  costs half of a 1300 x 1300 one. The first agent on a block spent most of its
  budget surveying and traced one eight-transistor cell. So: survey with a handful of
  large-area, low-zoom views, decide what to trace, then spend on tracing. Read text
  (trace files, netlist reports, notes) freely; it is cheap.
- Old images drop out of your context as new ones arrive. **Write coordinates and
  conclusions into your notes file as soon as you have them.** Do not rely on
  remembering an image.
- Expect one to two views per unique transistor. Decide which junctions matter and
  look at those, rather than paging through the region.
- **If `notes/blocks/BLOCK.md` already exists, you are continuing someone's work.** Read
  it and the existing trace first. Trust what is marked traced and shipped (it
  extracts); re-check what is marked uncertain when you need it; start from the "Not
  done" list. Do not survey again.
- What a brief says "is known" about a block's structure is the coordinator's belief
  from a low-zoom look and may be wrong (one brief's "one unit per bit" was). Check
  it with one view before building on it.
- Ship often. If you run out of room, everything shipped so far is safe, and your notes
  tell the next agent where to resume.
- Your final message should be short (under 300 words): what you traced, the main
  findings, what is uncertain, what is not done, and any problem with the tools. The
  detail belongs in the notes file.
