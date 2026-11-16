# Register decode array (14140-15800 x 13500-14670)

Status: read and in the trace (trace/decode.txt, generated). The row drivers and the
logic that uses the column outputs are not traced yet.

## Result

The array decodes the 5-bit address into 18 select lines, one per register R0-R17.
Each column is a 5-input NOR with a depletion load, high for exactly one address.
Left to right the columns select:

| Column | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| x | 14260 | 14347 | 14434 | 14520 | 14607 | 14694 | 14780 | 14867 | 14954 | 15040 | 15127 | 15214 | 15300 | 15387 | 15474 | 15560 | 15647 | 15734 |
| Register | 7 | 6 | 4 | 0 | 2 | 1 | 10 | 5 | 3 | 8 | 9 | 11 | 13 | 12 | 14 | 15 | 17 | 16 |

There is no column for addresses 18-31, and no column decodes fewer than five bits:
nothing in this array responds to an address above 17, and there are no "don't care"
bits that would make registers alias.

## Structure

- 18 metal columns at 86.66 px pitch. Each has a depletion load at the top (VCC
  contact at y 13553, gate y 13590-13645 tied to the column by a buried contact at
  its right, output contact at y 13676) and leaves the array at the bottom
  (contact at y 14640).
- 10 poly rows at y 13766, 13851, 13940, 14024, 14112, 14196, 14284, 14369, 14456,
  14543, in five pairs. Pair k (from the top) is address bit k; the upper row of a
  pair is the true line, the lower the complement. The rows end at the left
  (x 14225) and are driven from the right.
- A ground diffusion rail between the two rows of each pair, contacted at its left
  end to the VSS metal at x 14140-14200.
- Contact pads on the columns in six bands: above row 1, between the pairs, below
  row 10. A pad's diffusion can run under the row above it, the row below it, or
  both, to reach a rail; that is where a transistor is.

## How it was read

`tools/pla_read.py` samples the clean shot of chip 1 under the column metal:
- pad present or not at each of 18 x 6 places (tan against pink; the two groups are
  separated by more than 25 units of red-minus-green);
- transistor or not at each of 18 x 10 crossings (poly over diffusion is redder
  than poly over field; per-row gaps of 4 to 18 units between the two groups).

Checks, none of which were used to make the decisions:
1. Every transistor has a pad beside it, except two borderline colour values
   (row 1 column 13, row 3 column 2) that sit just above their row's threshold with
   no pad beside them; both are taken as no transistor.
2. Every pad has at least one transistor.
3. Every column has exactly one transistor in each of the five pairs.
4. With the upper row of each pair as the true line, the 18 columns decode exactly
   the addresses 0-17, each once. Any other choice of polarity for any pair gives
   addresses above 17.

The matrix is saved in trace/decode_matrix.json. `tools/gen_decode.py` turns it into
trace/decode.txt, whose extraction gives the 18 NORs back.

Caveats
- Which row is "true" rests on check 4, that is, on the chip having registers 0-17
  as documented. It is not yet confirmed by tracing the row drivers.
- The rows are named `ar0`..`ar4` / `ar0_n`..`ar4_n` on the assumption that they
  come straight from the address register. If the drivers gate them (for example
  with chip select), the columns are qualified selects and the names should change.
- The geometry in trace/decode.txt is rectangles at measured positions with
  typical sizes, not outlines of each feature.
- Read from chip 1 only (the clean shot). Chip 2's metal shot shows the same pads
  where I looked (top-left corner), but the full matrix was not re-read there.

## Row drivers (traced by the `areg` block)

The address register is the row of five cells **above** the array (x 14180-16150,
y 13000-13290, one per 390 px), not the five cells to its right as first thought.
Each register cell's output runs to the upper row of its pair with no gate in
between; the five cells right of the array (x 15930-16200) are plain inverters that
make the lower row from the upper one (`arK_n = NOT arK`). So the rows are driven
straight from the address register, as the names assume.

Whether the register's output is the true or the inverted data bit is supported but
not proven by tracing (it rests on one link inside the register cell that is still
uncertain, see `notes/blocks/areg.md`); the 0-17 argument above remains the main
evidence for the polarity. The register's load strobe (`ar_load`) comes up a
vertical line at x 16299 from a gate at about x 15880-16150, y 15230-15330.

## Next

- Finish the register cell (four of the five are in the `rdp3` block's region).
- The row of cells above the array (14150-15820 x 13030-13260) and the structures at
  y 13260-13500 between it and the array.
- Where each column goes below the array (contacts at y 14640, then the latch
  column and logic at y 14700-17100).
