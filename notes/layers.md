# Layer legend

How each layer looks in the two shots, with places to see it. Coordinates are
metal-shot pixels. Useful zoom: 2.5x for tracing, 4-5x (blurry, but it resolves edge
order) when a junction is unclear. Beyond 2x there is no new detail, only bigger pixels.

| Layer | Metal shot | Acid shot | Example |
|---|---|---|---|
| Metal | Bright yellow, speckled, dark edge line. Dark lines also cross it wherever poly or diffusion edges run underneath | Gone. Leaves a "ghost": pink or rainbow fringes where it lay over oxide, white where it sat on a contact | Rails at x 14408-14460 and 14584-14634, y 14900-15300 |
| Poly | Orange, granular, dark outline. Hidden under metal | Orange, granular, dark outline. Pale under a metal ghost | Load gate 14524-14576 x 14956-15019 |
| Diffusion | Plain area inside a dark outline, slightly pinker than field | Plain tan inside a dark outline; field is greener | Output band y 14975-15002, x 14460-14520 |
| Metal contact | Ring or oval in the metal | Rounded box with black pits | 14606,14972 and 14423,14920 |
| Buried contact (poly to diffusion) | Small dark-outlined box, about 30 x 25 px, at a poly end | Same box, lighter centre, no pits | 14520-14550 x 14927-14955 |
| Channel | Poly crossing a diffusion region; the diffusion edges show as dark lines across the poly | Same, clearer | Load channel 14524-14576 x 14975-15002 |

## Logic style

Depletion-load NMOS. A gate is a pull-down network under a ground rail, a diffusion
band carrying the output to a load, and a load transistor whose other end contacts a
supply rail. The load is a wide poly block over the band (long channel, W/L below 1)
whose gate is tied back to the output by a buried contact. That gate-to-output tie is
how loads are recognised; whether the depletion implant itself is visible has not been
settled and is not relied on.

Outputs often leave a gate in diffusion and reach the next gate's poly through a
buried contact, with no metal involved (for example 14348-14380 x 14980-15016).

Single metal layer, so metal crossings are made with poly or diffusion cross-unders:
a contact, a short run underneath, another contact.

## Dimensions seen so far

| Feature | Size (px) |
|---|---|
| Signal metal | 16-20 wide |
| Power rail in logic | about 50 wide |
| Poly gate | 20-22 long |
| Metal contact | about 30 x 34 |
| Buried contact | about 30 x 28 |
| Edge line | 6-8 wide, so every edge is uncertain by about 3 |

## Repeat pitches (autocorrelation)

| Array | Pitch |
|---|---|
| Central and right datapaths, horizontal | 390.3 |
| Left and mid-right vertical arrays | 477 |
| Latch column below the decode array, vertical | 304 |
| Decode array columns | 87 |

## Automatic segmentation: tried, not used

Brightness and texture separate metal from the rest in open areas, but in dense logic
the edges of poly and diffusion underneath print through the metal as dark lines and
cut every wire into fragments. Bridging those gaps would also bridge real gaps between
neighbouring wires, so the result cannot be trusted for connectivity. Geometry is
entered by hand; image processing is kept for checking and for comparing repeated
cells.

## The chip-1 shots (added 2026-11-14)

Three more shots, of a different die, registered into the same frame by
`tools/align.py` (about 0.5 px residual for the metal shot, 1 px for the stripped
ones). An existing trace of chip 2 laid over them sits on the features to within a
few pixels.

| Layer name | File | What it is |
|---|---|---|
| `metal1` | hd6845metal.jpg | metal intact; a second look at any metal join |
| `acid1` | hd6845acid.jpg | metal stripped; still has fringes, a little less than `acid` |
| `acid1b` | hd6845acid2.jpg | metal stripped, clean: no fringes at all |

`acid1b` is the important one. Under the wide rails, where `acid` shows only
interference fringes, it shows gates, diffusion and contacts plainly.

Colour legend for `acid1b`. Calibrated on the pilot cell, the R/W gate group, the
two plain diffusion rectangles at 14700-15002 x 18600-18820, the MA3 pre-driver
under the VCC band, the wide E poly line at 16660-16705 x 18130-18552 and the
clock driver logic. What an area looks like depends on whether metal was above it:

| Layer | Protected (metal above, or within about 10 px of a metal edge) | In the open |
|---|---|---|
| Poly | salmon with a sharp red outline | dark red-brown, textured, with a thin green rim. Same over field and over thin oxide |
| Diffusion | flat tan with a dark outline; dark specks where metal contacts were | bright green |
| Field | pink | khaki |
| Buried contact | small box at a poly end with a heavy dark outline, tan inside | the same |

Traps
- Metal protects a margin of about 10 px beyond its edges. A 25-30 px gap between
  two parallel metal lines therefore does not show open colours: over diffusion or
  poly it is a thin dark bar across the feature, over field a narrow olive strip
  with a dark outline. These bars and strips are not layout.
- Tan (protected diffusion) and khaki (open field) are close. Check where the metal
  is before calling a tan area diffusion.
- A diffusion edge under metal is a dark line in `acid1b` and in the metal shots,
  so a dark line across a metal line is not evidence of a gap in the metal.

How to use the shots together
- Geometry of poly and diffusion: `acid1b`, with the metal shot beside it to know
  which colour table applies.
- Poly in the open is also plain in `acid` (orange).
- Metal and its contacts: `metal`, with `metal1` as a second opinion. Contacts to
  diffusion also show as specks in `acid1b`.
- `tools/quad.py x y w h [--layers a,b,c,d]` renders several shots side by side.

The salmon/brown difference in poly follows the metal above it, not the implant:
load gates and ordinary gates look the same when both are in the open. AMB-002
stays open.

Registration of `acid1b` against chip 2 measures within about 1 px wherever the
measurement is confident (random logic, pads). In the regular arrays the measurement
itself fails, so there the fit is interpolated; `metal1` measures within 1 px
everywhere. A per-pixel median of the three stripped shots (`acidmed`) is worse than
`acid1b` alone.
