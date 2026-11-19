#!/usr/bin/env python3
"""Atlas for the renaise.com rail globe: REAL ARTIFACTS only (2026-11-19).

The globe shows the work itself, not the screens around it: frames from each artifact loop,
the objects and the film. No website screenshots, tables
or type slides. Every image appears once (look-based de-duplication), keeps its own
proportions (fitted inside TILE, never cropped), and carries the project it opens plus the
label the globe shows on hover.

Sources live in stage/globe/src/ so the atlas can be rebuilt without the network or the
23-minute film master. Run: python3 stage/globe/build-atlas.py
"""
import json, os, re, subprocess, tempfile, hashlib, urllib.request
from PIL import Image
R = os.path.expanduser('~/SEANCE/r2.github.io')
G = f'{R}/stage/globe'; SRC = f'{G}/src'
TILE, COLS = 256, 8  # 256px tiles: sharp at 2x on the globe's largest center tile
FILM = os.path.expanduser('~/Downloads/The Depictions of Original Sin-001.mp4')
html = open(f'{R}/index.html').read()
names = dict(re.findall(r'"([a-z0-9-]+)": \{"name": "([^"]+)"', html))

def frames(mp4, times):
    return [('mp4', f'{R}/stage/{mp4}', t) for t in times]

# (slug, label or None for the project name, [sources])
SPEC = [
    # Self-made artifacts only (Renaise, 2026-11-19), on dark grounds. The film is out:
    # its shots were made by the six artists she directed, not by her.
    ('idler', None, [('img', f'{SRC}/shell/{n}', 0) for n in sorted(os.listdir(f'{SRC}/shell'))]
        + [('img', f'{SRC}/vector-dark/{n}', 0) for n in sorted(os.listdir(f'{SRC}/vector-dark'))]),
    ('osmosis', None, frames('osmosis/art/petri.mp4', [0.3, 1.2, 2.2, 3.2, 4.2, 5.0])),
    ('biota', 'Symbiota · Biota', frames('biota/art/fish.mp4', [0.3, 1.2, 2.2, 3.2, 4.2])),
    ('flora', 'Hieronymus · FLORA', frames('flora/art/hieronymus.mp4', [0.3, 1.5, 3.0, 4.5, 6.0, 7.5])),
    ('studio-artifice', 'Humanoid · Studio Artifice', frames('studio-artifice/art/figure.mp4', [0.2, 1.2, 2.2, 3.2, 4.2, 5.2])),
    ('artifice-brand', 'Primitives · Artifice', frames('artifice-brand/plate.mp4', [0.2, 0.8, 1.4, 2.0, 2.6, 3.2])),
    ('the-artifact-index', 'Objects · The Artifact Index', [('img', f'{R}/stage/the-artifact-index/art/objects.webp', 0)]),
]
# Left out: website heroes (Lighthouse), editor interfaces (Artifactory), the light Spaces rail,
# the light Skill Profile and light Vector, other artists' Index pieces, the Artifactory orb.
# The film: curated for an AI audience, dark grounds only; grotesque and near-black shots left out.
FILM_T = []  # self-made only: the film's shots are the six artists' work

os.makedirs(f'{SRC}/film', exist_ok=True)
film_src = []
# one shot per 12s of film: frames closer than that are the same scene
_k = []
for t in sorted(FILM_T):
    if _k and t - _k[-1] < 10: continue
    _k.append(t)
FILM_T = _k
for t in FILM_T:
    out = f'{SRC}/film/t{t:04d}.jpg'
    if not os.path.exists(out) and os.path.exists(FILM):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', FILM, '-frames:v', '1',
                        '-vf', 'scale=960:-2', '-q:v', '2', out], check=True)
    if os.path.exists(out): film_src.append(('img', out, 0))
SPEC.append(('depictions-of-original-sin', None, film_src))

tmp = tempfile.mkdtemp()
tiles, meta = [], []
def load(kind, path, t):
    if kind == 'mp4':
        out = os.path.join(tmp, hashlib.md5(f'{path}{t}'.encode()).hexdigest() + '.png')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', path, '-frames:v', '1', out], check=True)
        return Image.open(out)
    return Image.open(path)

def add(slug, label, src):
    kind, path, t = src[:3]
    im = load(kind, path, t).convert('RGB'); w, h = im.size; k = TILE / max(w, h)
    im = im.resize((max(1, round(w * k)), max(1, round(h * k))), Image.LANCZOS)
    lo, hi = im.convert('L').getextrema()
    g = im.convert('L'); gw, gh = g.size; bw = max(2, gw // 12); bh = max(2, gh // 12)
    band = [g.getpixel((x, y)) for x in range(gw) for y in range(gh) if x < bw or x >= gw - bw or y < bh or y >= gh - bh]
    if sum(band) / len(band) > 70: return  # dark grounds only
    if hi - lo < 24: return
    if '/film/' in path and sum(im.convert('L').getdata()) / (im.size[0] * im.size[1]) < 22: return  # near-black film frames show nothing
    sq = im.resize((16, 16), Image.LANCZOS).convert('L'); q = [v / 255 for v in sq.getdata()]
    m = sum(q) / len(q); sd = (sum((v - m) ** 2 for v in q) / len(q)) ** .5 or 1; q = [(v - m) / sd for v in q]
    cv = [c / 255 for px in im.resize((6, 6), Image.LANCZOS).getdata() for c in px]
    for o_slug, o_q, o_c in meta:
        corr = sum(x * y for x, y in zip(o_q, q)) / len(q)
        cd = sum(abs(a - b) for a, b in zip(o_c, cv)) / len(cv)
        # the set is hand-picked now, so only true repeats are dropped
        if corr > .86 or cd < .02: return
    meta.append((slug, q, cv))
    tiles.append((slug, label or names.get(slug, slug), path.replace(R + '/stage/', '') + (f'@{t}' if kind == 'mp4' else ''), im))

for slug, label, srcs in SPEC:
    for s in srcs: add(slug, label, s)
# Artifact Index pieces are other artists' work: not on the globe (Renaise, 2026-11-19).

rows = (len(tiles) + COLS - 1) // COLS
atlas = Image.new('RGB', (COLS * TILE, rows * TILE), (16, 16, 16)); rects = []
for i, (_, _, _, im) in enumerate(tiles):
    x, y = (i % COLS) * TILE, (i // COLS) * TILE
    atlas.paste(im, (x, y)); rects.append([x, y, im.size[0], im.size[1]])
atlas.save(f'{G}/atlas.jpg', quality=86, optimize=True, progressive=True)
json.dump({'tile': TILE, 'cols': COLS, 'slugs': [t[0] for t in tiles], 'labels': [t[1] for t in tiles],
           'rects': rects, 'src': [t[2] for t in tiles]}, open(f'{G}/atlas.json', 'w'))
from collections import Counter
print(len(tiles), 'tiles', atlas.size, os.path.getsize(f'{G}/atlas.jpg') // 1024, 'KB')
print(Counter(t[0] for t in tiles))
