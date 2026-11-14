# Trunks: long-distance wiring of the global signals

Trace: `trace/trunks.txt` (requires clock, inrow, pads_in_top). Coordinates are
metal-shot pixels. "L" = left, "R" = right, "U" = up (smaller y), "D" = down.

## Status

Work in progress (2026-11-15). Followed so far: `ck_out`, `ck_a`, `ck_b` from the
clock block to the three vertical metals at x 13022 / 13066 / 13132 and up to
y 16600; `ck_b` and one branch of `ck_a` into the bottom row of the mid-right array.
The line the clock notes call `ck_src` is **not** `ck_a` (see Ambiguities A1): it is
the output of the left-hand inverter of the input row.

## How to use this file

- "Trunk segments by position" (next section) is the look-up table: find a wire by
  its x or y and read off the net.
- Per-signal sections give the route in order, every branch, and every entry point
  into a block.
- Everything listed was followed on the photos junction by junction unless marked
  "(not verified)" or "(seen at low zoom)".

## Trunk segments by position

Vertical segments, sorted by x:

| x | y range | Layer | Net | Notes |
|---|---|---|---|---|
| 10848-10867 | 19015-19306 | metal | `ck_out` | joins the clock trace; corner contact at (10853,19015) |
| 11000-11040 | 18322-19032 | poly (wide) | `ck_out` | passes under the VCC band and bus lines L4, L5, L6 without contact |
| 12523 | 16900-16996 | metal | `ck_b` | entry into the mid-right array, bottom row |
| 12603-12624 | 16800-16953 | metal | `ck_a` | from contact (12631,16954) up into the mid-right array, bottom row |
| 12733-12757 | 16950-18471 | poly | `ck_a` | long poly from contact (12740,18471) up under the whole bus field (continuity between y 17050 and 18220 seen at 0.9x only) |
| 13000-13035 | 18455-18772 | poly | `ck_b` | from the end of line B up through the VCC band |
| 13012-13033 | 16995-18469 | metal | `ck_b` | ends at contact (13023,16995) |
| 13013-13037 | 16600-16945 | metal | `ck_a` | continues up (being followed) |
| 13055-13077 | 16952-18471 | metal | `ck_a` | jogs left to x 13025 at y 16943-16960 |
| 13085-13120 | 18455-18724 | poly | `ck_a` | from the end of line A up through the VCC band |
| 13122-13143 | 16600-18337 | metal | `ck_out` | continues up (being followed) |
| 13192-13212 | 18385-18775 | poly | S (`t_g0_out`) | see `S` below |
| 13849 | 18537-18775 | metal | S (`t_g0_out`) | output of input-row gate 0 |

Horizontal segments, sorted by y:

| y | x range | Layer | Net | Notes |
|---|---|---|---|---|
| 16943-16960 | 13025-13066 | metal | `ck_a` | jog |
| 16945-16965 | 12631-12745 | poly | `ck_a` | to contact (12631,16954) |
| 16966-17001 | 12878-13040 | poly | `ck_b` | under the wide VCC vertical (x 12935-12980) |
| 16987-17004 | 12523-12892 | metal | `ck_b` | from contact (12892,16991) left |
| 18243-18262 (L1) | ...-12807 | metal | not identified | ends at contact (12807,18253); poly on to contact (13216,18251), metal on right |
| 18290-18305 (L2) | ...-12849 | metal | not identified | contact (12849,18296); poly on to contact (13176,18297), metal on right |
| 18335-18350 (L3) | 11027-12807 | metal | `ck_out` | contacts at both ends only |
| 18332-18348 | 12807-13132 | poly | `ck_out` | under the vertical metals |
| 18375-18395 (L4) | 10857-12849 | metal | S (`t_g0_out`) | contacts at both ends only |
| 18378-18393 | 12849-13212 | poly | S | then down at x 13200 |
| 18420-18437 (L5) | 10810-12807 | metal | not identified | turns up at x 10803-10820; right end contact (12807,18427), poly to contact (13156,18427), metal on right |
| 18460-18480 (L6, left piece) | 10900-11870 | metal | S | contacts (10900,18470), (11772,18467) to gate g5's poly, (11852,18468) to a poly that goes up to a buried contact on a plain diffusion rectangle (11500-11720 x 18275-18400, added capacitance) |
| 18460-18480 (L6, right piece) | 12095-12740 | metal | `ck_a` | from g6's output poly (x 12110) to contact (12740,18471) |
| 18700-18722 | ...-13090 | metal | `ck_a` | line A of the clock block; end contact (13085,18709) |
| 18745-18768 | ...-13010 | metal | `ck_b` | line B; end contact (13000,18756) |
| 18765-18785 | 13200-13522 | poly | S | |
| 18765-18785 | 13522-13852 | metal | S | from contact (13522,18774) to the drop from gate 0 |
| 18938-18957 | <10650-10858 | poly | `ck_out` | branch W, under the VSS and VCC verticals; not yet followed further left |
| 19005-19025 | 10853-11023 | metal | `ck_out` | between the corner contact and the wide poly's foot |

## ck_out

Source: clock block output stage (NOT CLK).

1. Vertical metal x 10848-10867 from the clock block (y 19306) up to a corner contact
   at (10853,19015).
2. From that contact, metal right along y 19005-19025 to a contact at (11023,19015),
   the foot of a wide poly line (x 11000-11040).
3. The wide poly runs up through the open area, under the VCC band (y 18518-18665)
   and under bus lines L6, L5, L4 (no contacts; checked at 3x) to a contact at
   (11027,18340).
4. Bus line L3 (metal, y 18335-18350) from there right to a contact at (12807,18339).
   It crosses two polys without contact: at x 11843-11865 (see A1) and at
   x 12733-12757 (`ck_a`).
5. Poly along y 18332-18348 under the wide VCC vertical and the `ck_b`, `ck_a`
   verticals to a contact at (13132,18337).
6. Vertical metal x 13122-13143 upwards: followed to y 16600, continues.

Branch W: at the corner contact (10853,19015) a poly leaves upwards (x 10838-10858),
turns left at y 18938-18957 and passes under the VSS (x 10763-10817) and VCC
(x 10677-10730) verticals. Followed to x 10650 only.

Branch at y 19240-19262 (from the clock block towards (9340,19240)): not yet followed.

## ck_b

1. Line B (metal, y 18745-18768) ends at a contact at (13000,18756).
2. Poly x 13000-13035 up through the VCC band to a contact at (13022,18469).
3. Vertical metal x 13012-13033 up through the bus crossing field to a contact at
   (13023,16995). **The metal ends here.**
4. Poly left along y 16966-17001 under the wide VCC vertical to a contact at
   (12892,16991).
5. Metal left along y 16987-17004 to x 12523, then up.
   **Entry: mid-right array, bottom row, metal going up at x 12513-12533, y 16900.**

## ck_a

1. Line A (metal, y 18700-18722) ends at a contact at (13085,18709).
2. Poly x 13085-13120 up through the VCC band to a contact at (13108,18471).
3. Metal: left to x 13066, up at x 13055-13077 to y 16952, jog left along
   y 16943-16960, up at x 13013-13037. Followed to y 16600, continues.

Second route (from gate g6 of the clock block, whose output is on line A according
to the clock trace): poly x 12098-12125 up to contact (12108,18467); bus line L6
right piece (metal, y 18460-18480) right to contact (12740,18471); poly x 12733-12757
up under bus lines L5..L1 (no contacts; checked at 2.25x) and on up to y 16950; left
along y 16945-16965 to a contact at (12631,16954); metal up at x 12603-12624.
**Entry: mid-right array, bottom row, metal going up from (12631,16954).**

## S: output of input-row gate 0 (`t_g0_out`; the clock notes' `ck_src`)

Source: the single inverter at the left end of the input row (gate 0, x 13730-13925).
Its input X arrives from the logic below the decode array (see below); S = NOT X.

Route of S:
1. Gate 0's output contact (13850,18537), metal down at x 13849 to y 18775, left along
   y 18765-18785 to a contact at (13522,18774).
2. Poly left along y 18765-18785 to x 13200, up at x 13192-13212 (under the VCC
   band) to y 18385, left along y 18378-18393 under the vertical metals to a contact
   at (12849,18384).
3. Bus line L4 (metal, y 18375-18395) left to a contact at (10857,18383).
4. Poly down from there (under L5) to a poly link between contacts (10810,18470) and
   (10900,18470).
5. From (10900,18470): bus line L6 left piece right to x 11870: gate g5's input
   (contact 11772,18467) and a capacitor rectangle (contact 11852,18468).
6. From (10810,18470): the long run to the left of the die described in
   `notes/blocks/clock.md` ("Route of `ck_a` to the left of the die"; that route
   carries S, not `ck_a`). Not yet re-followed here.

Route of X (gate 0's input), followed backwards: poly from gate 0 up at x 13765-13795
to a contact at (13782,18080); metal right along y 18075-18090 to x 14543; up at
x 14535-14552 to y 16992; left along y 16985-17000 to x 13952; up to y 16907; left
along y 16900-16915 to a contact at (13655,16908); poly up to a contact at
(13655,16822); from there a vertical metal at x 13664-13684 going up (y < 16600) into
the routing channel at the left edge of the logic below the decode array. Not
followed further.

## Ambiguities

### A1. `ck_src` is not `ck_a`: trace/clock.txt has a wrong link

`trace/clock.txt` ends with eight uncertain shapes ("seen at 1.1x; drawn roughly") and
`@alias ck_a ck_src`. They say that the bus piece feeding gate g5 (L6 left piece) is
joined to gate g6's output through a line at y 18335-18358 with contacts at
(12741,18347) and (11852,18347). Checked at 2.25x-6x in all four shots:

- The line at y 18335-18350 (L3) starts at the contact (11027,18340) on the wide poly
  that comes up from `ck_out`, and ends at the contact (12807,18339). It is `ck_out`.
- At (12741,18347) L3 passes over the poly x 12733-12757 with no contact; that poly
  carries on up beyond y 18220 (to the mid-right array).
- At (11852,18347) the poly from contact (11852,18468) ends in a buried contact on a
  small diffusion pad (11834-11880 x 18340-18385) that is joined by a narrow strip
  (y 18355-18368) to the plain diffusion rectangle 11500-11720 x 18275-18400. L3
  passes over the top of the pad; it does not widen and shows no contact ring.

So L6's left piece is not connected to L6's right piece. What is on it was followed
the other way: L4, the poly at x 13200, and the metal at y 18775 lead to the output
of input-row gate 0.

Consequence for the extraction: with `clock.txt` as it stands, `ck_out`, `ck_a` and
`ck_src` are shorted (reported as one error by `netlist.py`). Fix in `clock.txt`:
delete the eight `?` shapes after "line A is also the line first labelled ck_src"
and the `@alias ck_a ck_src`.

Consequence for the clock block's logic (not re-traced here): gate g5's input is S,
not `ck_a`. The clock notes have g5's output on line B and g6 (input line B) driving
line A; at 5x the two contacts (line B to g6's gate poly at 11985,18757; the long
contact from line A to g6's output at 11965-12030 x 18705-18720) do look real. If so,
g5 pulls `ck_b` low whenever S is high, which only makes sense if X is a `ck_b`-like
signal. X must be traced to its source to settle this.

## Not done

See Status; this section is rewritten as work proceeds.
