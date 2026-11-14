#!/usr/bin/env python3
"""Build everything in out/ from trace/.

  out/hd6845s.svg     the trace as an SVG in metal-shot coordinates, with Inkscape
                      layers and both die photos linked as background layers
  out/netlist.json    extracted transistor netlist
  out/report.txt      rule-check report and recovered gates
  out/floorplan.jpg   the die at reduced scale with the functional blocks outlined
  out/floorplan.svg   the same outlines as a stand-alone SVG over the photo

floorplan.txt (repo root) lists the blocks, one per line:
  x0,y0:x1,y1  kind  name | description
kind is one of: pad io array pla logic route test power unknown
A leading '?' on the kind marks the identification as provisional.
"""
import json
import os
import sys
from xml.sax.saxutils import escape

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tracelib
import netlist as netlist_mod

ROOT = tracelib.ROOT
OUT = os.path.join(ROOT, 'out')
W, H = 19838, 21025     # metal shot

LAYER_NAMES = {'D': 'diffusion', 'P': 'poly', 'M': 'metal', 'C': 'contact', 'B': 'buried', 'A': 'annotation'}
KIND_COL = {
    'pad': (255, 255, 255), 'io': (255, 200, 0), 'array': (0, 220, 255),
    'pla': (255, 0, 255), 'logic': (255, 80, 80), 'route': (150, 150, 150),
    'test': (120, 120, 255), 'power': (255, 140, 0), 'unknown': (255, 255, 0),
}


def read_floorplan():
    path = os.path.join(ROOT, 'floorplan.txt')
    blocks = []
    if not os.path.exists(path):
        return blocks
    for n, line in enumerate(open(path), 1):
        line = line.split('#', 1)[0].strip()
        if not line:
            continue
        head, _, desc = line.partition('|')
        tok = head.split()
        a, b = tok[0].split(':')
        x0, y0 = map(float, a.split(','))
        x1, y1 = map(float, b.split(','))
        kind = tok[1]
        prov = kind.startswith('?')
        kind = kind.lstrip('?')
        if kind not in KIND_COL:
            raise SystemExit(f'floorplan.txt:{n}: unknown kind {kind}')
        blocks.append(dict(x0=min(x0, x1), y0=min(y0, y1), x1=max(x0, x1), y1=max(y0, y1),
                           kind=kind, prov=prov, name=' '.join(tok[2:]), desc=desc.strip()))
    return blocks


def acid_matrix():
    """SVG matrix placing the raw acid shot in metal-shot coordinates."""
    T = np.array(json.load(open(os.path.join(ROOT, 'trace', 'align.json')))['metal_to_acid'])
    A = np.linalg.inv(T[:, :2])
    t = -A @ T[:, 2]
    return 'matrix(%.8f %.8f %.8f %.8f %.4f %.4f)' % (A[0, 0], A[1, 0], A[0, 1], A[1, 1], t[0], t[1])


def path_d(g):
    parts = []
    polys = [g] if g.geom_type == 'Polygon' else list(g.geoms)
    for p in polys:
        for ring in [p.exterior] + list(p.interiors):
            c = list(ring.coords)
            parts.append('M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in c[:-1]) + 'Z')
    return ' '.join(parts)


def hexcol(c):
    return '#%02x%02x%02x' % c


def svg_layer(name, body, visible=True):
    style = '' if visible else ' style="display:none"'
    return (f'<g inkscape:groupmode="layer" inkscape:label="{name}" id="layer-{name}"{style}>\n'
            + body + '</g>\n')


def floorplan_svg_body(blocks):
    s = []
    for b in blocks:
        col = hexcol(KIND_COL[b['kind']])
        dash = ' stroke-dasharray="60 40"' if b['prov'] else ''
        w, h = b['x1'] - b['x0'], b['y1'] - b['y0']
        s.append(f'<rect x="{b["x0"]:.0f}" y="{b["y0"]:.0f}" width="{w:.0f}" height="{h:.0f}" '
                 f'fill="{col}" fill-opacity="0.12" stroke="{col}" stroke-width="14"{dash}>'
                 f'<title>{escape(b["name"])}: {escape(b["desc"])}</title></rect>\n')
        fs = max(70, min(170, w / max(4, len(b['name'])) * 1.5))
        s.append(f'<text x="{b["x0"] + 24:.0f}" y="{b["y0"] + fs + 10:.0f}" font-family="sans-serif" '
                 f'font-size="{fs:.0f}" fill="#ffffff" stroke="#000000" stroke-width="{fs / 12:.0f}" '
                 f'paint-order="stroke">{escape(b["name"])}{" ?" if b["prov"] else ""}</text>\n')
    return ''.join(s)


def build_svg(tr, nl, blocks):
    head = (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
            f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
            f'<title>HD6845S trace (coordinates are pixels of hd6845metal2ndchip.jpg)</title>\n')
    out = [head]
    out.append(svg_layer('photo-acid',
                         f'<image xlink:href="../dieshots/hd6845acid2ndchip.jpg" x="0" y="0" '
                         f'width="19857" height="21029" transform="{acid_matrix()}"/>\n', False))
    out.append(svg_layer('photo-metal',
                         f'<image xlink:href="../dieshots/hd6845metal2ndchip.jpg" x="0" y="0" '
                         f'width="{W}" height="{H}"/>\n'))
    for layer in ('D', 'P', 'M', 'C', 'B'):
        col = hexcol(tracelib.COLOURS[layer])
        body = []
        for it in tr.items:
            if it.layer != layer:
                continue
            extra = ' stroke="#ffff00" stroke-width="3"' if it.uncertain else ''
            body.append(f'<path d="{path_d(it.geom)}"{extra}><title>{escape(it.src)}</title></path>\n')
        op = '0.75' if layer in ('C', 'B') else '0.4'
        out.append(f'<g inkscape:groupmode="layer" inkscape:label="{LAYER_NAMES[layer]}" '
                   f'id="layer-{LAYER_NAMES[layer]}" fill="{col}" fill-opacity="{op}" '
                   f'stroke="{col}" stroke-width="1.5">\n' + ''.join(body) + '</g>\n')
    lab = []
    for lb in tr.labels:
        lab.append(f'<circle cx="{lb.x:.0f}" cy="{lb.y:.0f}" r="3" fill="#fff" stroke="#000"/>'
                   f'<text x="{lb.x + 6:.0f}" y="{lb.y + 5:.0f}" font-family="monospace" font-size="14" '
                   f'fill="#fff" stroke="#000" stroke-width="2.5" paint-order="stroke">'
                   f'{escape(lb.name)}</text>\n')
    out.append(svg_layer('labels', ''.join(lab)))
    tl = []
    for t in nl.transistors:
        tl.append(f'<text x="{t.x:.0f}" y="{t.y:.0f}" font-family="monospace" font-size="10" '
                  f'text-anchor="middle" fill="#ff0" stroke="#000" stroke-width="2" '
                  f'paint-order="stroke">t{t.id}<title>gate {escape(nl.nm(t.gate))}: '
                  f'{escape(nl.nm(t.c1))} - {escape(nl.nm(t.c2))}</title></text>\n')
    out.append(svg_layer('transistors', ''.join(tl)))
    out.append(svg_layer('floorplan', floorplan_svg_body(blocks), False))
    out.append('</svg>\n')
    with open(os.path.join(OUT, 'hd6845s.svg'), 'w') as f:
        f.write(''.join(out))


def build_floorplan(blocks, scale=1 / 8):
    a = np.load(os.path.join(ROOT, 'cache', 'metal.npy'), mmap_mode='r')
    step = round(1 / scale)
    # box-filter downsample
    hh, ww = (H // step) * step, (W // step) * step
    small = np.zeros((hh // step, ww // step, 3), np.float32)
    for y0 in range(0, hh, step * 256):
        y1 = min(hh, y0 + step * 256)
        blk = np.asarray(a[y0:y1, :ww]).astype(np.float32)
        blk = blk.reshape((y1 - y0) // step, step, ww // step, step, 3).mean(axis=(1, 3))
        small[y0 // step:y1 // step] = blk
    base = Image.fromarray((small * 0.75).astype(np.uint8)).convert('RGBA')
    lay = Image.new('RGBA', base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    try:
        font = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
        font(10)
    except OSError:
        font = lambda s: ImageFont.load_default()
    for b in blocks:
        col = KIND_COL[b['kind']]
        box = [b['x0'] * scale, b['y0'] * scale, b['x1'] * scale, b['y1'] * scale]
        d.rectangle(box, fill=col + (38,), outline=col + (255,), width=1 if b['prov'] else 3)
    img = Image.alpha_composite(base, lay).convert('RGB')
    d = ImageDraw.Draw(img)
    for b in blocks:
        bw = (b['x1'] - b['x0']) * scale
        bh = (b['y1'] - b['y0']) * scale
        label = b['name'] + (' ?' if b['prov'] else '')
        size = 22
        while size > 9:
            f = font(size)
            words, lines, cur = label.split(), [], ''
            for w_ in words:
                if d.textlength((cur + ' ' + w_).strip(), font=f) <= bw - 8:
                    cur = (cur + ' ' + w_).strip()
                else:
                    if cur:
                        lines.append(cur)
                    cur = w_
            lines.append(cur)
            if (len(lines) * (size + 2) <= bh - 6 and
                    all(d.textlength(l, font=f) <= bw - 6 for l in lines)):
                break
            size -= 1
        f = font(size)
        y = b['y0'] * scale + 4
        for l in lines:
            d.text((b['x0'] * scale + 5, y), l, fill=(255, 255, 255), font=f,
                   stroke_width=2, stroke_fill=(0, 0, 0))
            y += size + 2
    img.save(os.path.join(OUT, 'floorplan.jpg'), quality=88)

    with open(os.path.join(OUT, 'floorplan.svg'), 'w') as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n'
                f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                f'viewBox="0 0 {W} {H}">\n'
                f'<image xlink:href="../dieshots/hd6845metal2ndchip.jpg" x="0" y="0" width="{W}" height="{H}"/>\n'
                + floorplan_svg_body(blocks) + '</svg>\n')


def main():
    os.makedirs(OUT, exist_ok=True)
    tr = tracelib.load()
    nl = netlist_mod.Netlist(tr)
    with open(os.path.join(OUT, 'netlist.json'), 'w') as f:
        json.dump(nl.to_json(), f, indent=1)
    with open(os.path.join(OUT, 'report.txt'), 'w') as f:
        f.write(nl.report() + '\n')
    blocks = read_floorplan()
    build_svg(tr, nl, blocks)
    if '--no-floorplan' not in sys.argv:
        build_floorplan(blocks)
    print(nl.report().split('\n')[0])
    print(f'{len(tr.items)} shapes, {len(blocks)} floor-plan blocks -> out/')


if __name__ == '__main__':
    main()
