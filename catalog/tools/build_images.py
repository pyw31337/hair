#!/usr/bin/env python3
"""Generated renders -> WebP (no masks, no effects).
  img/<name>.webp     480x640 q72  (main view)
  img/t/<name>.webp   150x200 q60  (option chip thumbnails)
  img/manifest.js     list of available image names (app derives color coverage from it)
Usage: python build_images.py <raw_dir> <catalog_dir>"""
import sys, glob, os, json
from PIL import Image
raw, cat = sys.argv[1:3]
out, th = os.path.join(cat, 'img'), os.path.join(cat, 'img', 't')
os.makedirs(th, exist_ok=True)
names = []
for f in sorted(glob.glob(os.path.join(raw, '*.jpg'))):
    name = os.path.basename(f)[:-4]; names.append(name)
    dst = os.path.join(out, name + '.webp')
    if os.path.exists(dst) and os.path.getmtime(dst) > os.path.getmtime(f): continue
    im = Image.open(f).convert('RGB')
    im.resize((480, 640), Image.LANCZOS).save(dst, 'WEBP', quality=72, method=6)
    im.resize((150, 200), Image.LANCZOS).save(os.path.join(th, name + '.webp'), 'WEBP', quality=60, method=6)
# Keep already-built catalog images even if their raw JPG is missing on this machine.
existing = [os.path.splitext(os.path.basename(f))[0]
            for f in glob.glob(os.path.join(out, '*.webp'))]
names = sorted(set(names) | set(existing))
with open(os.path.join(out, 'manifest.js'), 'w') as fh:
    fh.write('window.IMAGES=' + json.dumps(names, separators=(',', ':')) + ';\n')
print('images', len(names))
