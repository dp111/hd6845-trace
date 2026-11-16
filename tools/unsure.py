#!/usr/bin/env python3
"""Which joins rest on uncertain ('?') items  (re-read item R12, trap 17).

usage: unsure.py [--names REGEX]

Builds the netlist twice, with everything and with every '?' item left out, and compares
where the labels end up. A net whose labels fall into more than one net once the '?' items
are gone is joined only through uncertain geometry: the join is an assumption, whatever the
extraction prints. Output: one block per such net, the labels grouped by the piece they stay
with. Labels that sit on '?' geometry themselves are listed as "on uncertain geometry".

It sees only joins between labelled pieces. Supply nets (vss, vcc) are skipped: they are
joined by name anyway.
"""
import argparse
import copy
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import netlist
import tracelib
from shapely.geometry import Point


def node_at(nl, layer, x, y):
    geoms, tree = nl._trees[layer]
    if tree is None:
        return None
    pt = Point(x, y)
    for i in tree.query(pt):
        if geoms[i].contains(pt):
            return nl._node_of(layer, i)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--names', default=None, help='only nets with a name matching this regex')
    a = ap.parse_args()
    tr = tracelib.load()
    full = netlist.Netlist(tr)
    red_tr = copy.copy(tr)
    red_tr.items = [it for it in tr.items if not it.uncertain]
    red = netlist.Netlist(red_tr)
    n_unc = len(tr.items) - len(red_tr.items)

    by_full = defaultdict(list)
    for lb in tr.labels:
        if lb.name in ('vss', 'vcc'):
            continue
        nf = node_at(full, lb.layer, lb.x, lb.y)
        if nf is None:
            continue
        by_full[nf].append(lb)
    count = 0
    for nf, lbs in sorted(by_full.items(), key=lambda kv: full.nm(kv[0])):
        name = full.nm(nf)
        if a.names and not re.search(a.names, name):
            continue
        groups = defaultdict(list)
        for lb in lbs:
            nr = node_at(red, lb.layer, lb.x, lb.y)
            groups[nr].append(lb)
        if len(groups) < 2:
            continue
        count += 1
        print(f'{name}: {len(groups)} pieces without the uncertain items')
        for nr, g in groups.items():
            tag = 'on uncertain geometry' if nr is None else f'piece {nr}'
            seen = set()
            for lb in g:
                key = (lb.name, round(lb.x), round(lb.y))
                if key in seen:
                    continue
                seen.add(key)
                print(f'    {tag}: {lb.name} {lb.layer} {lb.x:.0f},{lb.y:.0f}  ({lb.src})')
    print(f'{count} nets joined only through uncertain items ({n_unc} uncertain items in the trace)')


if __name__ == '__main__':
    main()
