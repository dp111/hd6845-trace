#!/usr/bin/env python3
"""Which write strobes connect each data bus line to a register bit (from the extraction).

usage: bust_fanout.py        (honours TRACE)
For each data line (by its central datapath name) lists the strobe nets (wr_*) of the
pass transistors that have the line on one side: the registers that bit is written into.
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import netlist
LINES = [('cdp1_c5_bl', 'bit 0'), ('cdp1_c4_bl', 'bit 1'), ('cdp1_c3_bl', 'bit 2'),
         ('cdp1_c2_bl', 'bit 3'), ('cdp1_c1_bl', 'bit 4'), ('cdp1_a0_bl', 'bit 5'),
         ('cdp1_lw2', 'bit 6'), ('cdp1_a2_bl', 'bit 7'), ('cdp1_a3_bl', 'cdp1_a3_bl'),
         ('cdp1_lw1', 'cdp1_lw1')]
n = netlist.Netlist()
nid = {}
for k, nd in n.nodes.items():
    for nm in nd.names:
        for line, label in LINES:
            if nm == line:
                nid[k] = label
out = collections.defaultdict(set)
for t in n.transistors:
    g = n.nm(t.gate)
    if not g.startswith('wr_'):
        continue
    for a in (t.c1, t.c2):
        if a in nid:
            out[nid[a]].add(g)
for line, label in LINES:
    print('%-11s %-11s %s' % (label, line, ' '.join(sorted(out.get(label, []))) or '-'))
