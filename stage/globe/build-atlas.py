#!/usr/bin/env python3
"""Atlas for the renaise.com rail globe: REAL ARTIFACTS only (2026-11-19).

The globe shows the work itself, not the screens around it: frames from each artifact loop,
the objects, the film, and the pieces in the Artifact Index. No website screenshots, tables
or type slides. Every image appears once (look-based de-duplication), keeps its own
proportions (fitted inside TILE, never cropped), and carries the project it opens plus the
label the globe shows on hover. Index pieces are other artists' work, so their label names
the piece and the artist, not only the project.

Sources live in stage/globe/src/ so the atlas can be rebuilt without the network or the
23-minute film master. Run: python3 stage/globe/build-atlas.py
"""
import json, os, re, subprocess, tempfile, hashlib, urllib.request
from PIL import Image
R = os.path.expanduser('~/SEANCE/r2.github.io')
G = f'{R}/stage/globe'; SRC = f'{G}/src'
TILE, COLS = 128, 16
FILM = os.path.expanduser('~/Downloads/The Depictions of Original Sin-001.mp4')
html = open(f'{R}/index.html').read()
names = dict(re.findall(r'"([a-z0-9-]+)": \{"name": "([^"]+)"', html))

def frames(mp4, times):
    return [('mp4', f'{R}/stage/{mp4}', t) for t in times]

# (slug, label or None for the project name, [sources])
SPEC = [
    ('idler', None, [('img', f'{R}/stage/idler/shell-turn.jpg', 0)] + frames('idler/shell-turn.mp4', [3.5, 7.0])),
    ('osmosis', None, frames('osmosis/art/petri.mp4', [0.5, 2.5, 4.5])),
    ('biota', 'Symbiota · Biota', frames('biota/art/fish.mp4', [0.5, 2.0, 3.5])),
    ('flora', 'Hieronymus · FLORA', frames('flora/art/hieronymus.mp4', [0.5, 3.0, 6.0])),
    ('soot', 'Spaces rail · SOOT', frames('soot/art/rail.mp4', [1.0])),
    ('studio-artifice', 'Humanoid · Studio Artifice', frames('studio-artifice/art/figure.mp4', [0.2, 1.5, 4.5])),
    ('artifice-brand', 'Primitives · Artifice', frames('artifice-brand/plate.mp4', [0.3, 1.6, 2.8])),
    # Lighthouse's plate is its website hero, not an artifact, so it is left out.
    # Artifactory's cover is the editor interface, not an object, so it is left out.
    ('the-artifact-index', 'Objects · The Artifact Index', [('img', f'{R}/stage/the-artifact-index/art/objects.webp', 0)]),
]
# The film: one shot from across every part (times in seconds into the 23:14 master).
FILM_T = [40, 80, 100, 120, 160, 180, 220, 240, 280, 300, 540, 600, 900, 940, 1100, 1140, 1280, 1340]

os.makedirs(f'{SRC}/film', exist_ok=True); os.makedirs(f'{SRC}/index', exist_ok=True)
film_src = []
for t in FILM_T:
    out = f'{SRC}/film/t{t:04d}.jpg'
    if not os.path.exists(out) and os.path.exists(FILM):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', FILM, '-frames:v', '1',
                        '-vf', 'scale=640:-2', '-q:v', '3', out], check=True)
    if os.path.exists(out): film_src.append(('img', out, 0))
SPEC.append(('depictions-of-original-sin', None, film_src))

# The Artifact Index: each piece with its title and artist, as the Index captions it.
items = json.load(open(f'{G}/index-items.json'))
idx_src = []
for it in items:
    f = f'{SRC}/index/' + it['src'].split('/')[-1]
    if not os.path.exists(f):
        urllib.request.urlretrieve(it['src'], f)
    t = it['text']; label = f"{t[1]}, {t[2].title()} · The Artifact Index" if len(t) > 2 else None
    idx_src.append(('img', f, 0, label))

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
    if hi - lo < 24: return
    sq = im.resize((16, 16), Image.LANCZOS).convert('L'); q = [v / 255 for v in sq.getdata()]
    m = sum(q) / len(q); sd = (sum((v - m) ** 2 for v in q) / len(q)) ** .5 or 1; q = [(v - m) / sd for v in q]
    cv = [c / 255 for px in im.resize((6, 6), Image.LANCZOS).getdata() for c in px]
    for o_slug, o_q, o_c in meta:
        corr = sum(x * y for x, y in zip(o_q, q)) / len(q)
        cd = sum(abs(a - b) for a, b in zip(o_c, cv)) / len(cv)
        if corr > (.72 if o_slug == slug else .85) or (o_slug == slug and cd < .05): return
    meta.append((slug, q, cv))
    tiles.append((slug, label or names.get(slug, slug), path.replace(R + '/stage/', '') + (f'@{t}' if kind == 'mp4' else ''), im))

for slug, label, srcs in SPEC:
    for s in srcs: add(slug, label, s)
for s in idx_src: add('the-artifact-index', s[3], s[:3])

rows = (len(tiles) + COLS - 1) // COLS
atlas = Image.new('RGB', (COLS * TILE, rows * TILE), (16, 16, 16)); rects = []
for i, (_, _, _, im) in enumerate(tiles):
    x, y = (i % COLS) * TILE, (i // COLS) * TILE
    atlas.paste(im, (x, y)); rects.append([x, y, im.size[0], im.size[1]])
atlas.save(f'{G}/atlas.jpg', quality=82, optimize=True, progressive=True)
json.dump({'tile': TILE, 'cols': COLS, 'slugs': [t[0] for t in tiles], 'labels': [t[1] for t in tiles],
           'rects': rects, 'src': [t[2] for t in tiles]}, open(f'{G}/atlas.json', 'w'))
from collections import Counter
print(len(tiles), 'tiles', atlas.size, os.path.getsize(f'{G}/atlas.jpg') // 1024, 'KB')
print(Counter(t[0] for t in tiles))
