#!/usr/bin/env python3
"""Build the derived data in cache/ from the inputs.

- cache/metal.npy, cache/acid.npy : the die shots as raw uint8 RGB arrays, for
  memory-mapped cropping (about 1.25 GB each)
- cache/ds/p-NN.png               : datasheet pages at 110 dpi (the PDF is a scan)
- cache/accc.txt                  : text of the CPC document

Existing outputs are kept; delete a file to rebuild it.
"""
import os
import subprocess
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, 'cache')


def main():
    os.makedirs(os.path.join(CACHE, 'ds'), exist_ok=True)

    for layer in ('metal', 'acid'):
        out = os.path.join(CACHE, f'{layer}.npy')
        if os.path.exists(out):
            print('have', out)
            continue
        src = os.path.join(ROOT, 'dieshots', f'hd6845{layer}2ndchip.jpg')
        a = np.asarray(Image.open(src))
        np.save(out, a)
        print('wrote', out, a.shape)
        del a

    if not os.path.exists(os.path.join(CACHE, 'ds', 'p-01.png')):
        subprocess.run(['pdftoppm', '-r', '110', '-png',
                        os.path.join(ROOT, 'datasheets', 'Hd6845.hitachi.pdf'),
                        os.path.join(CACHE, 'ds', 'p')], check=True)
        print('rendered datasheet pages')

    txt = os.path.join(CACHE, 'accc.txt')
    if not os.path.exists(txt):
        subprocess.run(['pdftotext', '-layout',
                        os.path.join(ROOT, 'docs', 'ACCC1.8-EN.pdf'), txt], check=True)
        print('wrote', txt)


if __name__ == '__main__':
    main()
