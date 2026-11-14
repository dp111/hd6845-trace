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
