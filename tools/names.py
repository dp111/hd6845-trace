#!/usr/bin/env python3
"""Net names: find rename candidates, and prove that a batch of renames changed only names.

usage: names.py candidates
       names.py snapshot FILE        (before renaming)
       names.py compare FILE         (after: must report "only names changed")

candidates
    Lists, from the full extraction:
    1. nets that carry a functional name and also a placeholder name (a block prefix and a
       local name) or an older name kept as an @alias, on firm geometry: tools/unsure.py does not list the
       net, so the placeholder can be renamed to the functional name;
    2. the same on uncertain geometry: listed so that they are NOT renamed (trap 17);
    3. glossary rows for placeholder patterns whose description says what the signal is
       ("is R8", "is data bit", "= rc3", ...): hints only, to be read and judged.
    A placeholder is a name whose first part is a block prefix (a trace file's name or the
    prefix of a cell's name) or that ends in a coordinate-like number (`tcw_m6404`).

snapshot / compare
    The extraction's transistors (position, size, which nets they join) and, for every
    net, its names. compare fails if any transistor or any connection differs, or if a net
    lost its last name, and otherwise lists every net whose names changed (old -> new).
    A rename that is only a rename passes; anything that moved geometry or merged two nets
    does not.
"""
import glob
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tracelib
import netlist as netlist_mod

ROOT = tracelib.ROOT


def extract():
    os.environ.pop('TRACE', None)
    return netlist_mod.Netlist(tracelib.Trace())


def prefixes():
    ps = {os.path.basename(p)[:-4] for p in glob.glob(os.path.join(ROOT, 'trace', '*.txt'))}
    for p in glob.glob(os.path.join(ROOT, 'trace', '*.txt')):
        for line in open(p):
            m = re.match(r'\s*@cell\s+([a-z0-9]+)_', line)
            if m:
                ps.add(m.group(1))
    ps.discard('zz')
    return ps


def is_placeholder(name, ps):
    head = name.split('_', 1)[0]
    return head in ps or bool(re.search(r'_[a-z]*\d{4,5}[a-z]?$', name))


def snapshot(nl):
    ts = sorted((round(t.x), round(t.y), round(t.w), round(t.l), t.gate, min(t.c1, t.c2), max(t.c1, t.c2))
                for t in nl.transistors)
    return {'transistors': ts, 'names': {str(n.id): sorted(n.names) for n in nl.nodes.values()},
            'nodes': len(nl.nodes)}


def cmd_candidates():
    nl = extract()
    ps = prefixes()
    out = subprocess.run([os.path.join(ROOT, '.venv', 'bin', 'python'), os.path.join(ROOT, 'tools', 'unsure.py')],
                         capture_output=True, text=True, cwd=ROOT, env={k: v for k, v in os.environ.items() if k != 'TRACE'}).stdout
    unsure = set(re.findall(r'^(\S+): \d+ pieces without the uncertain items', out, re.M))
    firm, weak = [], []
    aliased = set(tracelib.ALIASES)          # names written as the second word of an @alias
    for n in nl.nodes.values():
        if len(n.names) < 2:
            continue
        ph = [x for x in n.names if is_placeholder(x, ps) or (x in aliased and not is_placeholder(tracelib.ALIASES[x], ps))]
        func = [x for x in n.names if x not in ph and x not in ('vss', 'vcc') and not is_placeholder(x, ps)]
        if func and ph:
            (weak if any(x in unsure for x in n.names) else firm).append((func, ph))
    print('1. placeholder names on firm geometry beside a functional name (rename them):')
    for func, ph in sorted(firm):
        print('   %s  <-  %s' % (' / '.join(func), ' '.join(ph)))
    print('\n2. the same through uncertain geometry (do NOT rename; trap 17):')
    for func, ph in sorted(weak):
        print('   %s  <-  %s' % (' / '.join(func), ' '.join(ph)))
    print('\n3. glossary rows for placeholders whose text names what they are (judge each):')
    sig = open(os.path.join(ROOT, 'notes', 'signals.md')).read().split('## Former names')[0]
    rx = re.compile(r'\b(is|are|=)\s+\**`?(R\d+|r\d+_b|rc\d|hc\d|sl\d|hsw\d|data (bus )?bit|bit \d of R)', re.I)
    for line in sig.splitlines():
        m = re.match(r'\|\s*`([^`]+)`', line)
        if m and is_placeholder(m.group(1).replace('#', '0').replace('*', 'x'), ps) and rx.search(line):
            print('   ' + line[:220] + ('...' if len(line) > 220 else ''))


def cmd_snapshot(path):
    s = snapshot(extract())
    json.dump(s, open(path, 'w'))
    print('snapshot: %d nets, %d transistors -> %s' % (s['nodes'], len(s['transistors']), path))


def cmd_compare(path):
    a = json.load(open(path))
    b = snapshot(extract())
    bad = []
    if a['nodes'] != b['nodes']:
        bad.append('net count %d -> %d' % (a['nodes'], b['nodes']))
    if [list(t) for t in a['transistors']] != [list(t) for t in b['transistors']]:
        bad.append('transistors or their connections differ')
    changed = []
    for nid, old in a['names'].items():
        new = b['names'].get(nid, [])
        if old != new:
            changed.append((old, new))
            if old and not new:
                bad.append('net %s lost its names %s' % (nid, old))
    for old, new in sorted(changed):
        print('  %s  ->  %s' % (' '.join(old) or '(unnamed)', ' '.join(new) or '(unnamed)'))
    print('%d nets renamed' % len(changed))
    if bad:
        print('FAIL: ' + '; '.join(bad))
        sys.exit(1)
    print('only names changed')


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ('candidates', 'snapshot', 'compare'):
        sys.exit(__doc__)
    if sys.argv[1] == 'candidates':
        cmd_candidates()
    elif len(sys.argv) != 3:
        sys.exit(__doc__)
    elif sys.argv[1] == 'snapshot':
        cmd_snapshot(sys.argv[2])
    else:
        cmd_compare(sys.argv[2])


if __name__ == '__main__':
    main()
