#!/usr/bin/env python3
"""Print highlight / balayage / volume / parting image coverage.

Usage: python extra_progress.py <catalog_dir> [<raw_dir>]

Target rules (must match /workspace/colorgen/extra_todo.txt):
  highlight  — every style
  balayage   — female only
  volume-up  — every style
  parting    — each non-native option, excluding implausible ones:
      skip female full bangs × side (native center; side breaks the fringe)
      skip female side bangs × center (native side; center breaks side bangs)
      female none / seethrough and male down: both center and side
      m-short-natural-up-straight: center only (native side)
      m-medium-*-up-*: side only (native center)
      other m-short-*-up-*: both (parting is ambiguous)
"""
import sys, re, json, os

def style_keys(cat):
    text = open(os.path.join(cat, 'data.js')).read()
    return re.findall(
        r"'([fm]-[a-z]+-[a-z]+-[a-z]+-[a-z]+)'",
        re.search(r"function STYLE_KEYS\(\) \{ return \[(.*?)\]", text, re.S).group(1),
    )

def native_parting(k):
    g, length, _cut, bangs, _curl = k.split('-')
    if bangs == 'full':
        return 'center'
    if g == 'f' and bangs == 'side':
        return 'side'
    if k == 'm-short-natural-up-straight':
        return 'side'
    if g == 'm' and bangs == 'up' and length == 'medium':
        return 'center'
    return None

def targets_for(k):
    g, length, _cut, bangs, _curl = k.split('-')
    out = [f'{k}-t-highlight', f'{k}-vol']
    if g == 'f':
        out.append(f'{k}-t-balayage')
    if bangs == 'full':
        pass
    elif g == 'f' and bangs == 'side':
        pass
    elif bangs in ('none', 'seethrough', 'down'):
        out += [f'{k}-part-center', f'{k}-part-side']
    elif bangs == 'up':
        if k == 'm-short-natural-up-straight':
            out.append(f'{k}-part-center')
        elif length == 'medium':
            out.append(f'{k}-part-side')
        else:
            out += [f'{k}-part-center', f'{k}-part-side']
    return out

def kind(t):
    for suffix, name in (
        ('-t-highlight', 'highlight'),
        ('-t-balayage', 'balayage'),
        ('-vol', 'volume'),
        ('-part-center', 'part-center'),
        ('-part-side', 'part-side'),
    ):
        if t.endswith(suffix):
            return name
    return '?'

def names_from_manifest(cat):
    path = os.path.join(cat, 'img/manifest.js')
    return set(json.loads(open(path).read().split('=', 1)[1].rstrip(';\n')))

def names_from_raw(raw):
    return {os.path.splitext(f)[0] for f in os.listdir(raw) if f.endswith('.jpg')}

def main():
    cat = sys.argv[1]
    raw = sys.argv[2] if len(sys.argv) > 2 else None
    styles = style_keys(cat)
    targets = [t for s in styles for t in targets_for(s)]
    names = names_from_manifest(cat)
    if raw:
        names |= names_from_raw(raw)
    done = [t for t in targets if t in names]
    missing = [t for t in targets if t not in names]
    by = {}
    for t in targets:
        by.setdefault(kind(t), [0, 0])
        by[kind(t)][1] += 1
        if t in names:
            by[kind(t)][0] += 1
    print(f'extra images {len(done)}/{len(targets)}')
    for k in ('highlight', 'balayage', 'volume', 'part-center', 'part-side'):
        d, n = by.get(k, [0, 0])
        print(f'  {k:12s} {d}/{n}')
    # styles whose every target exists
    full = [s for s in styles if all(t in names for t in targets_for(s))]
    print(f'styles complete {len(full)}/{len(styles)}')
    if missing:
        print('next:', missing[0])
        print('remaining:', ' '.join(missing))
    else:
        print('all extra images present')

if __name__ == '__main__':
    main()
