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
- N-bit comparators and similar may be left as blocks. Derived signals, latches,
  flip-flops and glue gates are wanted in full, especially the end-of-frame state
  machine, the interlace odd/even logic, and whatever makes some registers hold N and
  others N-1.

- The user also wants a floor-plan overlay (`floorplan.txt` -> `out/floorplan.jpg`)
  kept current: rename and tighten a block whenever tracing identifies it.

## Practical

- Use `.venv/bin/python` (shapely, opencv, scikit-image, networkx are installed there).
- `cache/` is derived data and is not in git. `tools/prepare.py` then `tools/align.py`
  rebuild it. `cache/acid_aligned.npy` is the acid shot resampled into the metal frame,
  so every tool takes metal-shot coordinates for both layers.
- Keep large arrays on disk under `cache/`, not in `/tmp`: `/tmp` is RAM-backed here
  and the machine has 12 GB. Scratch renders go in `cache/scratch/`.
- `tools/view.py x y w h --scale 2.5 --grid 50 [--layers metal,acid] [--stack v]
  [--trace] [--nofill] --out FILE` renders a view. Keep each output under about
  1400 px a side or it is downscaled when read. `--trace --nofill` is the clearest
  way to check a trace against the photo.
- `tools/netlist.py` prints the extraction report; `tools/build.py` regenerates `out/`.
- Trace file format: docstring of `tools/tracelib.py`. Layer legend and what each
  feature looks like: `notes/layers.md`. Read that before tracing anything.
