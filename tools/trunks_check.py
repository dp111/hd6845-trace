"""Extract trace/trunks.txt against corrected copies of the traces it joins.

    tools/t.sh trunks trunks_check.py [-v]

trace/trunks.txt follows wires that run into places where trace/clock.txt holds
approximate or wrong shapes (see notes/blocks/trunks.md, Ambiguities). Until those are
corrected in clock.txt itself, the plain extraction reports shorts that are not in the
trunk trace. This tool copies the needed trace files to the scratch folder, applies
the corrections listed in FIXES to the copies, and runs the normal extraction on them,
so the trunk trace can be checked on its own merits. It changes nothing in trace/.
"""
import os
import shutil
import sys

import tracelib

FIXES = {
    'clock.txt': [
        # A1: the link that made ck_src an alias of ck_a does not exist
        ('@alias ck_a ck_src\n', ''),
        ('?M 12095,18455:12755,18480\n', 'M 12095,18455:12755,18480\n'),   # L6 right piece is real (ck_a)
        ('?C 12741,18467 s=22x22\n', ''),      # redrawn in trunks.txt with its poly
        ('?P 12727,18335:12755,18480\n', ''),
        ('?C 12741,18347 s=22x22\n', ''),
        ('?M 11835,18335:12755,18358\n', ''),
        ('?C 11852,18347 s=22x22\n', ''),
        ('?P 11840,18335:11866,18480\n', ''),
        ('?C 11852,18467 s=22x22\n', ''),
        # A3: the VCC band's left end is at x 10862, not 10760 (the S line's contact
        # at 10808,18600 lies left of it)
        ('M 10760,18512:13050,18668 ', 'M 10862,18512:13050,18668 '),
    ],
}


def main():
    scratch = os.path.join(tracelib.ROOT, os.environ.get('HD_SCRATCH', 'cache/scratch/trunks'), 'tracechk')
    os.makedirs(scratch, exist_ok=True)
    for name in os.listdir(tracelib.TRACE_DIR):
        if not name.endswith('.txt'):
            continue
        text = open(os.path.join(tracelib.TRACE_DIR, name)).read()
        for old, new in FIXES.get(name, []):
            if old not in text:
                print(f'note: fix no longer applies to {name}: {old.strip()!r}')
            text = text.replace(old, new)
        open(os.path.join(scratch, name), 'w').write(text)
    for name in os.listdir(tracelib.TRACE_DIR):
        if name.endswith('.json'):
            shutil.copy(os.path.join(tracelib.TRACE_DIR, name), scratch)
    tracelib.TRACE_DIR = scratch
    import netlist
    rep = netlist.Netlist().report()
    if '-v' in sys.argv:
        print(rep)
    else:
        head = rep.split('\ntransistors')[0]
        print(head)
        if 'unnamed open nets' in rep:
            print(rep[rep.index('unnamed open nets'):])


if __name__ == '__main__':
    main()
