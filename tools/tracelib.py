"""Trace geometry: file format, parsing, geometry construction and overlay drawing.

All coordinates are metal-shot pixels.

File format (trace/*.txt), one item per line, '#' starts a comment:

  LAYER shape [key=value ...]

  LAYER   M metal, P poly, D diffusion, C contact (metal to poly or diffusion),
          B buried contact (poly to diffusion)
  A leading '?' marks the item as uncertain, e.g.  ?P 7140,1700 y1755

  shapes
    rectangle   x0,y0:x1,y1                       D 7082,1790:7232,1985
    polygon     [ p p p ... ]                     D [ 7082,1790 x7232 y1985 x7082 ]
    path        p p p ...  with width w=N         M 7000,1860 x7700 w=50
                (flat ends, square corners; width defaults to the last '@w' value
                for the layer)
    contacts    C p p p ... [s=WxH]               C 7157,1858 7090,1955
                each point is one contact; a rectangle is also accepted

  points
    x,y         absolute point
    xN          move horizontally to absolute x = N
    yN          move vertically to absolute y = N

  labels
    N LAYER x,y name       names the net that owns that layer at that point
                           (LAYER is M, P or D)

  directives
    @w M=24 P=20           default path widths
    @s 24x24               default contact size
    @block name            names the block for the items that follow (reporting only)
"""
import glob
import os
import re
from dataclasses import dataclass, field

from shapely.geometry import LineString, Point, Polygon, box
from shapely.strtree import STRtree

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACE_DIR = os.path.join(ROOT, 'trace')

LAYERS = ('D', 'P', 'M', 'C', 'B')
COLOURS = {            # RGB for overlays and SVG
    'D': (0, 220, 60),
    'P': (255, 40, 40),
    'M': (60, 140, 255),
    'C': (255, 255, 255),
    'B': (255, 0, 255),
}


@dataclass
class Item:
    layer: str
    geom: object              # shapely polygon
    uncertain: bool = False
    src: str = ''             # file:line
    block: str = ''
    attrs: dict = field(default_factory=dict)


@dataclass
class Label:
    layer: str
    x: float
    y: float
    name: str
    src: str = ''


class TraceError(Exception):
    pass


_pt = re.compile(r'^(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)$')
_rect = re.compile(r'^(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?):(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)$')
_mx = re.compile(r'^x(-?\d+(?:\.\d+)?)$')
_my = re.compile(r'^y(-?\d+(?:\.\d+)?)$')


def _points(tokens, src):
    pts = []
    for t in tokens:
        m = _pt.match(t)
        if m:
            pts.append((float(m.group(1)), float(m.group(2))))
            continue
        m = _mx.match(t)
        if m:
            if not pts:
                raise TraceError(f'{src}: relative move before first point')
            pts.append((float(m.group(1)), pts[-1][1]))
            continue
        m = _my.match(t)
        if m:
            if not pts:
                raise TraceError(f'{src}: relative move before first point')
            pts.append((pts[-1][0], float(m.group(1))))
            continue
        raise TraceError(f'{src}: bad point "{t}"')
    return pts


def parse_file(path, items, labels):
    widths = {}
    csize = (24.0, 24.0)
    block = ''
    rel = os.path.relpath(path, ROOT)
    with open(path) as f:
        for n, line in enumerate(f, 1):
            src = f'{rel}:{n}'
            line = line.split('#', 1)[0].strip()
            if not line:
                continue
            tok = line.split()
            head = tok[0]
            if head == '@w':
                for t in tok[1:]:
                    k, v = t.split('=')
                    widths[k] = float(v)
                continue
            if head == '@s':
                w, h = tok[1].split('x')
                csize = (float(w), float(h))
                continue
            if head == '@block':
                block = tok[1] if len(tok) > 1 else ''
                continue
            if head.startswith('@'):
                raise TraceError(f'{src}: unknown directive {head}')
            uncertain = head.startswith('?')
            layer = head.lstrip('?')
            if layer == 'N':
                if len(tok) != 4 or tok[1] not in ('M', 'P', 'D'):
                    raise TraceError(f'{src}: label must be "N LAYER x,y name"')
                (x, y), = _points([tok[2]], src)
                labels.append(Label(tok[1], x, y, tok[3], src))
                continue
            if layer not in LAYERS:
                raise TraceError(f'{src}: unknown layer "{layer}"')
            attrs = {}
            geo = []
            for t in tok[1:]:
                if '=' in t:
                    k, v = t.split('=', 1)
                    attrs[k] = v
                else:
                    geo.append(t)
            if not geo:
                raise TraceError(f'{src}: no geometry')

            def add(g):
                if g.is_empty or not g.is_valid or g.area <= 0:
                    raise TraceError(f'{src}: degenerate or invalid shape')
                items.append(Item(layer, g, uncertain, src, block, dict(attrs)))

            m = _rect.match(geo[0])
            if m and len(geo) == 1:
                x0, y0, x1, y1 = map(float, m.groups())
                add(box(min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)))
            elif geo[0] == '[':
                if geo[-1] != ']':
                    raise TraceError(f'{src}: polygon not closed with ]')
                pts = _points(geo[1:-1], src)
                if len(pts) < 3:
                    raise TraceError(f'{src}: polygon needs 3+ points')
                add(Polygon(pts))
            elif layer in ('C', 'B'):
                w, h = csize
                if 's' in attrs:
                    w, h = map(float, attrs['s'].split('x'))
                for (x, y) in _points(geo, src):
                    add(box(x - w / 2, y - h / 2, x + w / 2, y + h / 2))
            else:
                pts = _points(geo, src)
                if len(pts) < 2:
                    raise TraceError(f'{src}: path needs 2+ points')
                w = float(attrs['w']) if 'w' in attrs else widths.get(layer)
                if not w:
                    raise TraceError(f'{src}: path has no width (use w=N or @w)')
                add(LineString(pts).buffer(w / 2, cap_style='flat', join_style='mitre'))


class Trace:
    def __init__(self, files=None):
        self.items = []
        self.labels = []
        if files is None:
            files = sorted(glob.glob(os.path.join(TRACE_DIR, '**', '*.txt'), recursive=True))
        for p in files:
            parse_file(p, self.items, self.labels)
        self._tree = STRtree([it.geom for it in self.items]) if self.items else None

    def query(self, x0, y0, x1, y1):
        if not self._tree:
            return []
        return [self.items[i] for i in self._tree.query(box(x0, y0, x1, y1))]

    def by_layer(self, layer):
        return [it for it in self.items if it.layer == layer]


_cached = None


def load(force=False):
    global _cached
    if _cached is None or force:
        _cached = Trace()
    return _cached


def overlay(im, x, y, w, h, scale, only=None, fill=True, trace=None):
    """Draw the trace over a PIL image of region (x, y, w, h) rendered at `scale`."""
    from PIL import Image, ImageDraw, ImageFont
    tr = trace or load()
    base = im.convert('RGBA')
    lay = Image.new('RGBA', base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    order = {'D': 0, 'P': 1, 'M': 2, 'C': 3, 'B': 3}
    its = sorted(tr.query(x, y, x + w, y + h), key=lambda it: order[it.layer])
    for it in its:
        if only and it.layer not in only:
            continue
        col = COLOURS[it.layer]
        polys = [it.geom] if it.geom.geom_type == 'Polygon' else list(it.geom.geoms)
        for p in polys:
            xy = [((px - x) * scale, (py - y) * scale) for px, py in p.exterior.coords]
            a = 70 if fill else 0
            if it.layer in ('C', 'B'):
                a = 150 if fill else 0
            outline = (255, 255, 0, 255) if it.uncertain else col + (255,)
            d.polygon(xy, fill=col + (a,), outline=outline)
            if it.uncertain:
                d.line(xy, fill=(255, 255, 0, 255), width=3)
    out = Image.alpha_composite(base, lay).convert('RGB')
    d = ImageDraw.Draw(out)
    try:
        f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 12)
    except OSError:
        f = ImageFont.load_default()
    for lb in tr.labels:
        if x <= lb.x < x + w and y <= lb.y < y + h and (not only or lb.layer in only):
            px, py = (lb.x - x) * scale, (lb.y - y) * scale
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255), outline=(0, 0, 0))
            d.text((px + 5, py - 7), lb.name, fill=(255, 255, 255), font=f,
                   stroke_width=2, stroke_fill=(0, 0, 0))
    return out
