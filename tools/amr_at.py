#!/usr/bin/env python3
"""Name of the net under a point:  amr_at.py LAYER x,y [LAYER x,y ...]   (LAYER M, P or D)

Builds the full extraction (honours TRACE) and prints, for each point, the net that owns
that layer there, or '-' if nothing of that layer is drawn there.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import netlist
from shapely.geometry import Point
n = netlist.Netlist()
args = sys.argv[1:]
for lay, xy in zip(args[0::2], args[1::2]):
    x, y = map(float, xy.split(','))
    geoms, tree = n._trees[lay]
    name = '-'
    if tree is not None:
        for i in tree.query(Point(x, y).buffer(2)):
            if geoms[i].intersects(Point(x, y)):
                name = n.nm(n._node_of(lay, int(i)))
                break
    print(lay, xy, name)
