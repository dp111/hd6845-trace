#!/usr/bin/env python3
"""Extraction report restricted to a box: errors/warnings and transistors whose position
lies inside it. Multi-name errors of other blocks (their joins are in zz_joins.txt, which
a single-block run does not load) are dropped.

usage: wl_net.py [x0 y0 x1 y1]     (default: the block west of the 4-bit counter)
Run through tools/t.sh BLOCK wl_net.py so that TRACE is set.
"""
import re
import subprocess
import sys
import os

here = os.path.dirname(os.path.abspath(__file__))
box = [int(v) for v in sys.argv[1:5]] if len(sys.argv) >= 5 else [11000, 6900, 11700, 9450]
out = subprocess.run([sys.executable, os.path.join(here, 'netlist.py')], capture_output=True, text=True).stdout
for line in out.splitlines():
    m = re.search(r' at\s+(\d+),\s*(\d+)', line)
    inside = m and box[0] <= int(m.group(1)) <= box[2] and box[1] <= int(m.group(2)) <= box[3]
    if line.startswith(('ERROR', 'WARN')):
        if inside or not m:
            print(line)
    elif inside or re.match(r'\d+ nets', line) or re.search(r'\bwl_\w+\s+=', line):
        print(line)
