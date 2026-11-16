#!/usr/bin/env python3
"""List every contact that more than one metal item reaches (re-read item R11, trap 16).

usage: padjoin.py [--min N] [--file NAME]

A metal that runs up to a pad's ring is not thereby on the pad: where two metal items of the
trace meet on one contact, one of them may in fact stop short of it. This prints each contact
(centre, source line) with the metal items that touch it, when they are at least --min (2)
separate items. By default only the suspicious kind is listed: one item covers the contact
and another only grazes it (covers under 60 percent of it), which is what a line that passes
a pad looks like when it has been drawn as joined. --all lists every contact with several
items (most are a pad rectangle plus its line, drawn in two pieces). Check each on a 3x metal
view with the tests of trap 16 in notes/tracing-guide.md. Cell instances are reported once per
instance.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tracelib


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--min', type=int, default=2)
    ap.add_argument('--file', default=None, help='only contacts from trace/NAME.txt')
    ap.add_argument('--all', action='store_true',
                    help='every contact with several metal items (default: only those where one '
                         'item covers the contact and another only grazes it, under 60 percent)')
    a = ap.parse_args()
    tr = tracelib.load()
    metals = [it for it in tr.items if it.layer == 'M']
    from shapely.strtree import STRtree
    tree = STRtree([m.geom for m in metals])
    n = 0
    for c in tr.items:
        if c.layer != 'C':
            continue
        if a.file and a.file + '.txt' not in str(c.src):
            continue
        hits = [metals[i] for i in tree.query(c.geom) if metals[i].geom.intersects(c.geom)]
        if len(hits) < a.min:
            continue
        # two items that overlap each other well beyond the contact are one drawn line in pieces
        ctr = c.geom.centroid
        ends = []
        for m in hits:
            inter = m.geom.intersection(c.geom).area / max(c.geom.area, 1)
            ends.append((m, inter))
        if not a.all:
            full = [m for m, i in ends if i >= 0.6]
            graze = [m for m, i in ends if 0 < i < 0.6]
            if not (full and graze):
                continue
        n += 1
        print(f"{round(ctr.x)},{round(ctr.y)}  {c.src}")
        for m, inter in ends:
            b = m.geom.bounds
            print(f"    M {m.src}  covers {inter:.0%} of the contact; item box "
                  f"{round(b[0])},{round(b[1])}:{round(b[2])},{round(b[3])}")
    print(f"{n} contacts reached by {a.min} or more metal items")


if __name__ == '__main__':
    main()
