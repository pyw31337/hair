#!/usr/bin/env python3
"""Print color-image coverage: which style keys have all 9 shades. Usage: python color_progress.py <catalog_dir>"""
import sys, re, json, os
cat = sys.argv[1]
names = set(json.loads(open(os.path.join(cat, 'img/manifest.js')).read().split('=', 1)[1].rstrip(';\n')))
styles = re.findall(r"'([fm]-[a-z]+-[a-z]+-[a-z]+-[a-z]+)'", re.search(r"function STYLE_KEYS\(\) \{ return \[(.*?)\]", open(os.path.join(cat, 'data.js')).read(), re.S).group(1))
shades = ['ad-stopaz','ad-sapphire','ad-silver','ad-amethyst','il-781','il-57','il-743','mj-58','mj-634']
done = sum(f'{s}-c-{c}' in names for s in styles for c in shades)
full = [s for s in styles if all(f'{s}-c-{c}' in names for c in shades)]
print(f'color images {done}/{len(styles)*len(shades)}; styles fully colored {len(full)}/{len(styles)}')
print('remaining:', ' '.join(s for s in styles if s not in full))
