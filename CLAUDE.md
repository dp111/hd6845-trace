# HD6845S die trace

Reverse engineering the Hitachi HD6845S CRTC from two die photographs. Read `PLAN.md`
first, then `notes/journal.md` (latest entry) and `notes/ambiguities.md` if they exist.

## Standing rules from the user

- Trace independently. Do not open Lance Ewing's HD6845 reverse-engineering work (on
  GitHub) or any other 6845 netlist/schematic effort until our own trace of the
  relevant block is complete. After that it may be used as confirmation only, never as
  a starting point.
- The datasheet (`datasheets/`), the CPC document (`docs/ACCC1.8-EN.pdf`, which calls
  this chip "CRTC type 0") and beebjit are sources of observed behaviour. None of them
  is assumed to be 100% accurate.
- When something is ambiguous, note it and keep tracing so it can be resolved from
  another direction. If one reading fits the documentation, adopt it cautiously and
  record it as an assumption so it can be rethought if later tracing conflicts.
- Refer to features by pixel coordinates of the metal shot
  (`dieshots/hd6845metal2ndchip.jpg`, 19838 x 21025, origin top-left).
- Name signals from pin names, register numbers and counter numbers.
- **Signal names** (user, 2026-11-17): every label must be meaningful, or be described
  in a table where it cannot be named yet, and every document must use the current
  names. The glossary is `notes/signals.md`: read its rules. A signal is named for what
  it is as soon as that is known, and until then for where it is; when it is identified,
  rename it everywhere with `tools/rename.py OLD NEW` and add it to the glossary's
  tables. `tools/build.py` reports any net name the glossary does not cover: that count
  stays at zero. Names ending in `_u` are open joins and are tasks.
- N-bit comparators and similar may be left as blocks. Derived signals, latches,
  flip-flops and glue gates are wanted in full, especially the end-of-frame state
  machine, the interlace odd/even logic, and whatever makes some registers hold N and
  others N-1.

- **All transistors are to be traced** (user, 2026-11-15): a "visual 6845" (the layout
  in a browser with a switch-level simulation of the extracted netlist running on it)
  is a deliverable once tracing is complete. Schematics may show a comparator as a
  block; the trace and netlist may not leave anything out. See `PLAN.md` M7.
- Schematics (user, 2026-11-15): higher-order structures (N-bit registers, comparators,
  counters) are drawn as blocks, **and** one instance of each kind gets its own
  gate-level sheet. So every block's notes must give the bit cell's gates in full.
- **Re-read rule** (user, 2026-11-16): when tracing shows that a method used on earlier
  blocks can miss or misread things, the affected blocks go on the "Re-read list" in
  `notes/work-packages.md` in the same commit, as tasks with a region and a reason, and
  the lesson goes into the traps of `notes/tracing-guide.md`. A mention in the journal
  or in a report does not count. The list is worked off before simulation (M5).
- The user also wants a floor-plan overlay (`floorplan.txt` -> `out/floorplan.jpg`)
  kept current: rename and tighten a block whenever tracing identifies it.

## Practical

- Use `.venv/bin/python` (shapely, opencv, scikit-image, networkx are installed there).
- `cache/` is derived data and is not in git. `tools/prepare.py` then `tools/align.py`
  rebuild it. Every shot is resampled into the frame of the chip-2 metal shot, so all
  tools take the same coordinates for every layer.
- Five shots, as `view.py --layers` names: `metal`, `acid` (chip 2: metal intact,
  metal stripped) and `metal1`, `acid1`, `acid1b` (chip 1, added 2026-11-14).
  **`acid1b` (hd6845acid2.jpg) is the clean one**: no interference fringes, readable
  under where the metal rails were. Use `metal`, `acid` and `acid1b` together. Poly is
  easiest in `acid`; diffusion, contacts and anything under metal in `acid1b`. Its
  colour legend is in `notes/layers.md`.
- Keep large arrays on disk under `cache/`, not in `/tmp`: `/tmp` is RAM-backed here
  and the machine has 12 GB. Scratch renders go in `cache/scratch/`.
- `tools/view.py x y w h --scale 2.5 --grid 50 [--layers metal,acid] [--stack v]
  [--trace] [--nofill] --out FILE` renders a view. Keep each output under about
  1400 px a side or it is downscaled when read. `--trace --nofill` is the clearest
  way to check a trace against the photo.
- `tools/netlist.py` prints the extraction report; `tools/build.py` regenerates `out/`.
- Trace file format: docstring of `tools/tracelib.py`. Layer legend and what each
  feature looks like: `notes/layers.md`. Read that before tracing anything.

## Parallel work (from 2026-11-15)

The user asked for parallel agents and for the session to work unsupervised until the
weekly usage limit is reached, committing and pushing each new traced piece and
keeping the floor plan up to date.

**Confirmed 2026-11-17 (user, before leaving a session to run unsupervised):** "while
unsupervised, just work serially, rather than trying to do things with multiple agents in
parallel".

**Update, 2026-11-15 evening (user instruction after the usage limit was hit):** the
eleven agents that were interrupted were resumed to finish their runs. When they
have all reported, **go back to serial work: do not start new agents** unless the
user asks again. Integrate their reports as below, then carry on tracing in this
session, one block at a time, in the priority order in `notes/work-packages.md`.

- Every agent works from `notes/tracing-guide.md`. Read it before tracing anything,
  whoever you are.
- One block = one agent = one file prefix. An agent owns `trace/PREFIX*.txt`,
  `notes/blocks/PREFIX.md`, `floorplan.d/PREFIX.txt`, `tools/PREFIX_*.py` and
  `cache/scratch/PREFIX/`, and nothing else.
- Agents commit only through `tools/ship.sh "message" files...` and run tools through
  `tools/t.sh PREFIX tool.py ...` (sets `TRACE=PREFIX` so other blocks' unfinished
  files are not loaded).
- The coordinating session alone edits `floorplan.txt`, `notes/work-packages.md` (the
  queue and its status), `notes/journal.md`, `notes/ambiguities.md`, `PLAN.md`, this
  file and the shared tools, and alone runs `tools/build.py`. When a package reports:
  read its notes, spot-check an overlay, run the full extraction (no `TRACE`), trim the
  coarse block in `floorplan.txt` that its `floorplan.d` fragment replaces, rebuild,
  ship, mark it in `notes/work-packages.md`, and start the next package from the queue.
- `trace/examples/` holds worked examples that are not part of the chip's trace.
