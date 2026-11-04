#!/usr/bin/env python3
"""Resize generated renders to 600x800 JPEG (q86). No masks, no effects:
every option in the app maps to one of these real generated images.
Usage: python build_images.py <raw_dir> <out_dir>"""
import sys, glob, os, cv2
raw, out = sys.argv[1:3]
n = 0
for f in sorted(glob.glob(os.path.join(raw, '*.jpg'))):
    name = os.path.basename(f)[:-4]
    img = cv2.resize(cv2.imread(f), (600, 800), interpolation=cv2.INTER_AREA)
    cv2.imwrite(f'{out}/{name}.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 86]); n += 1
print('images', n)
