#!/usr/bin/env python3
"""Several views side by side in one image (to follow a long vertical line cheaply).

usage: rde_strip.py OUT view-args ... // view-args ...
Each group of arguments (separated by //) is passed to tools/view.py; the results are
pasted left to right.
"""
import sys, os, subprocess
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = sys.argv[1]
groups, cur = [], []
for a in sys.argv[2:]:
    if a == '//':
        groups.append(cur); cur = []
    else:
        cur.append(a)
groups.append(cur)
ims = []
for i, g in enumerate(groups):
    tmp = out + '.%d.png' % i
    subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'view.py')] + g + ['--out', tmp],
                   check=True, stdout=subprocess.DEVNULL)
    ims.append(Image.open(tmp).copy()); os.remove(tmp)
w = sum(i.width for i in ims) + 6 * (len(ims) - 1); h = max(i.height for i in ims)
o = Image.new('RGB', (w, h), (255, 0, 255)); x = 0
for i in ims:
    o.paste(i, (x, 0)); x += i.width + 6
o.save(out); print(out, o.size)
