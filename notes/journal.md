# Journal

## 2026-11-14  M0: groundwork and pilot

Done
- Both shots converted to raw arrays; acid shot resampled into the metal frame
  (`tools/align.py`: affine fit over 270 patches, 0.57 px RMS, residual after
  resampling under 1 px almost everywhere, 2.5 px worst case).
- `tools/view.py` (two-layer views with grid and trace overlay), `tools/tracelib.py`
  (trace format, cells and mirrored instances), `tools/netlist.py` (extraction, rule
  checks, static gate recovery), `tools/build.py` (SVG, netlist, report, floor plan).
- Layer legend worked out on real structures (`notes/layers.md`). The process has
  buried contacts; loads are recognised by their gate-to-output tie.
- Pilot: `trace/pilot.txt`, two gates at 14280-14640 x 14880-15300. Extracts with no
  errors as `a_out = NOT in_a`, `b_out = NOR(a_out, in_c)`. The first overlay fitted
  without correction. A mirrored instance fits the right-hand half of the column.
- Coarse floor plan from a 12-tile survey at 0.2x (`floorplan.txt`, 68 blocks, all
  provisional) and repeat pitches by autocorrelation.
- Provisional pad table (`notes/pads.md`).

Found
- Automatic segmentation is not usable for geometry (reason in `notes/layers.md`).
- The first circuit tried, the RES/LPSTB buffers by the top pads, is a poor teaching
  example because it lies under wide rails; left as AMB-001.
- The die has two kinds of array: horizontal bit-slices at 390.3 px (central and right
  datapaths) and rows at 477 px (left and mid-right arrays). The left array is about
  25 rows tall, more than the 14 bits of MA, so it is not simply one bit per row.
- Rough size: about 26,000 px2 per transistor in dense logic, which puts the chip
  near 5,000 transistors.

Tracing rate
- Not yet representative. Understanding the legend took about 25 views. Once
  understood, a 380 x 380 px region with five transistors took one pass of entry and
  one overlay check. Estimate to be revised after M1 and M2: 300-ish unique dense
  regions after allowing for repetition, a handful of views each.

Not done yet (planned for later milestones)
- Image-space check of cell instances against their master (start of M3).
- Coverage checks (metal or contacts in the photo with no trace over them).
- Rule checks beyond the basics: floating gates, undriven nets.

Next: M1, the pad ring. Start by following the metal plane from the VSS pad and the
rail from the VCC pad to confirm which is which, then each pad's buffer or driver.
