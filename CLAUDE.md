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

## Practical

- `cache/` is derived data and is not in git. `python3 tools/prepare.py` rebuilds it.
- Keep large arrays on disk under `cache/`, not in `/tmp`: `/tmp` is RAM-backed here
  and the machine has 12 GB.
- The acid shot is offset from the metal shot by about (+10, +8) px; the exact affine
  is in `PLAN.md` section 1.
- `python3 tools/crop.py <acid|metal> x y w h out.png [scale] [--grid N]` cuts a crop
  with an optional coordinate grid.
