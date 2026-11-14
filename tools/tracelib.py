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
    @cell NAME [tag=T]     start a cell. The items that follow, up to @end, are drawn
                           where they stand (the master) and can be repeated.
    @end
    @inst NAME dx,dy [mx=X] [my=Y] [rot=DEG o=x,y] [tag=T]
                           a copy of the cell: mirrored about the vertical line x=X
                           and/or the horizontal line y=Y, then turned DEG degrees
                           (clockwise as seen on the photo) about the point o, then
                           moved by dx,dy.
                           A label containing {} gets the tag substituted. Supply
                           labels (vss, vcc) are copied as they are. Other labels
                           belong to the master only.
"""
import glob
import os
import re
from dataclasses import dataclass, field

from shapely import affinity
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


def xform(g, mx, my, dx, dy, rot=0, o=(0, 0)):
    if mx is not None:
        g = affinity.scale(g, xfact=-1, yfact=1, origin=(mx, 0))
    if my is not None:
        g = affinity.scale(g, xfact=1, yfact=-1, origin=(0, my))
    if rot:
        # y grows downward on the photo, so a positive shapely angle looks clockwise
        g = affinity.rotate(g, rot, origin=o)
    return affinity.translate(g, dx, dy)


def parse_file(path, items, labels, cells, insts):
    widths = {}
    csize = (24.0, 24.0)
    block = ''
    cell = None           # (name, tag, items, labels) while inside @cell
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
            if head == '@cell':
                if cell is not None:
                    raise TraceError(f'{src}: @cell inside @cell')
                kv = dict(t.split('=', 1) for t in tok[2:])
                cell = (tok[1], kv.get('tag', ''), [], [])
                if tok[1] in cells:
                    raise TraceError(f'{src}: cell {tok[1]} defined twice')
                cells[tok[1]] = cell
                continue
            if head == '@end':
                cell = None
                continue
            if head == '@inst':
                kv = dict(t.split('=', 1) for t in tok[3:])
                (dx, dy), = _points([tok[2]], src)
                o = tuple(map(float, kv['o'].split(','))) if 'o' in kv else (0.0, 0.0)
                insts.append((tok[1], dx, dy,
                              float(kv['mx']) if 'mx' in kv else None,
                              float(kv['my']) if 'my' in kv else None,
                              kv.get('tag', ''), src, float(kv.get('rot', 0)), o))
                continue
            if head.startswith('@'):
                raise TraceError(f'{src}: unknown directive {head}')
            uncertain = head.startswith('?')
            layer = head.lstrip('?')
            if layer == 'N':
                if len(tok) != 4 or tok[1] not in ('M', 'P', 'D'):
                    raise TraceError(f'{src}: label must be "N LAYER x,y name"')
                (x, y), = _points([tok[2]], src)
                lb = Label(tok[1], x, y, tok[3], src)
                if cell is not None:
                    cell[3].append(lb)
                    lb = Label(tok[1], x, y, tok[3].replace('{}', cell[1]), src)
                labels.append(lb)
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
                it = Item(layer, g, uncertain, src, block, dict(attrs))
                items.append(it)
                if cell is not None:
                    cell[2].append(it)

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
        self.cells = {}
        self.insts = []
        if files is None:
            files = sorted(glob.glob(os.path.join(TRACE_DIR, '**', '*.txt'), recursive=True))
        for p in files:
            parse_file(p, self.items, self.labels, self.cells, self.insts)
        for name, dx, dy, mx, my, tag, src, rot, o in self.insts:
            if name not in self.cells:
                raise TraceError(f'{src}: no cell named {name}')
            _, _, citems, clabels = self.cells[name]
            for it in citems:
                self.items.append(Item(it.layer, xform(it.geom, mx, my, dx, dy, rot, o), it.uncertain,
                                       f'{src} <- {it.src}', it.block, dict(it.attrs)))
            for lb in clabels:
                if '{}' not in lb.name and lb.name not in ('vss', 'vcc'):
                    continue
                p = xform(Point(lb.x, lb.y), mx, my, dx, dy, rot, o)
                self.labels.append(Label(lb.layer, p.x, p.y, lb.name.replace('{}', tag),
                                         f'{src} <- {lb.src}'))
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
    order = {'D': 0, 'P': 1, 'M': 2, 'C': 3, 'B': 3}
    its = sorted(tr.query(x, y, x + w, y + h), key=lambda it: order[it.layer])
    # one transparent sheet per layer, so a big shape never wipes out what is under it
    sheets = {}
    for it in its:
        if only and it.layer not in only:
            continue
        if it.layer not in sheets:
            sheets[it.layer] = Image.new('RGBA', base.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(sheets[it.layer])
        col = COLOURS[it.layer]
        polys = [it.geom] if it.geom.geom_type == 'Polygon' else list(it.geom.geoms)
        for p in polys:
            xy = [((px - x) * scale, (py - y) * scale) for px, py in p.exterior.coords]
            outline = (255, 255, 0, 255) if it.uncertain else col + (255,)
            if fill:
                a = 90 if it.layer in ('C', 'B') else 45
                d.polygon(xy, fill=col + (a,))
            d.line(xy, fill=outline, width=3 if it.uncertain else 2)
    lay = Image.new('RGBA', base.size, (0, 0, 0, 0))
    for k in ('D', 'P', 'M', 'C', 'B'):
        if k in sheets:
            lay = Image.alpha_composite(lay, sheets[k])
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
