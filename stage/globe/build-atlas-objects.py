#!/usr/bin/env python3
"""Atlas for the renaise.com rail globe (2026-11-19).

Rules (Renaise): self-made artifacts only, every image unique (one image per distinct
object, never two states of the same thing), backgrounds removed so the objects float,
dense. Sources are cut out once into src/objects/ and kept in the repo, so the atlas
rebuilds offline.

  objects   one frame of each artifact loop, its ground keyed out; composites (the
            Artifice objects, Primitives) split into their separate pieces
  atoms     Idler's six shape units
  marks     marks Renaise designed (Idler, Artifice, Codex Foundry, Fielder, Biota)

Left out: the film (the six artists' work), other artists' Index pieces, website and
interface screenshots, wordmarks (text), anything that fills its frame (Hieronymus).

Run: python3 stage/globe/build-atlas.py
"""
import json, os, subprocess, tempfile, hashlib
from PIL import Image
R = os.path.expanduser('~/SEANCE/r2.github.io')
G = f'{R}/stage/globe'; SRC = f'{G}/src'; OBJ = f'{SRC}/objects'
TILE, COLS = 256, 8
os.makedirs(OBJ, exist_ok=True)

def frame(mp4, t):
    out = os.path.join(tempfile.mkdtemp(), hashlib.md5(f'{mp4}{t}'.encode()).hexdigest() + '.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', f'{R}/stage/{mp4}', '-frames:v', '1', out], check=True)
    return Image.open(out).convert('RGB')

def cutout(im):
    """Ground = median of the outer band; alpha ramps with distance from it (soft edges)."""
    im = im.convert('RGB'); gw, gh = im.size; bw = max(2, gw // 14); bh = max(2, gh // 14); px = im.load()
    band = [px[x, y] for x in range(gw) for y in range(gh) if x < bw or x >= gw - bw or y < bh or y >= gh - bh]
    bg = [sorted(c[k] for c in band)[len(band) // 2] for k in range(3)]
    out = im.convert('RGBA'); po = out.load()
    for y in range(gh):
        for x in range(gw):
            r, g, b = px[x, y]
            d = max(abs(r - bg[0]), abs(g - bg[1]), abs(b - bg[2]))
            po[x, y] = (r, g, b, max(0, min(255, int((d - 14) * 255 / 38))))
    return out.crop(out.getbbox())

def split(im, n=2):
    """Two side-by-side pieces: cut at the emptiest column in the middle 30-70% (a soft
    shadow can bridge the gap, so there may be no fully empty column)."""
    a = im.split()[-1]; w, h = a.size; ap = a.load()
    col = [sum(ap[x, y] for y in range(0, h, 2)) for x in range(w)]
    cut = min(range(int(w * .3), int(w * .7)), key=lambda x: col[x])
    out = []
    for s, e in ((0, cut), (cut, w)):
        piece = im.crop((s, 0, e, h)); out.append(piece.crop(piece.getbbox()))
    return out

# (file name, slug, label, loader) — each loader returns one RGBA object
OBJECTS = [
    ('shell', 'idler', 'The Shell · Idler', lambda: cutout(Image.open(f'{SRC}/shell/s0040.jpg'))),
    ('vector', 'idler', 'Vector · Idler', lambda: cutout(Image.open(f'{SRC}/vector-dark/v040.jpg'))),
    ('petri', 'osmosis', 'Petri dish · Osmosis', lambda: cutout(frame('osmosis/art/petri.mp4', 2.2))),
    ('symbiota', 'biota', 'Symbiota · Biota', lambda: cutout(frame('biota/art/fish.mp4', 2.2))),
    ('humanoid', 'studio-artifice', 'Humanoid · Studio Artifice', lambda: cutout(frame('studio-artifice/art/figure.mp4', 1.2))),
]
SPLITS = [
    ('primitive', 'artifice-brand', 'Primitives · Artifice', lambda: split(cutout(frame('artifice-brand/plate.mp4', 1.4)), 2)),
    ('object', 'the-artifact-index', 'Objects · The Artifact Index', lambda: split(cutout(Image.open(f'{R}/stage/the-artifact-index/art/objects.webp')), 2)),
]
items = []
for name, slug, label, load in OBJECTS:
    f = f'{OBJ}/{name}.png'
    if not os.path.exists(f): load().save(f)
    items.append((slug, label, f))
for name, slug, label, load in SPLITS:
    fs = sorted(p for p in os.listdir(OBJ) if p.startswith(name + '-'))
    if not fs:
        for i, part in enumerate(load()): part.save(f'{OBJ}/{name}-{i}.png')
        fs = sorted(p for p in os.listdir(OBJ) if p.startswith(name + '-'))
    items += [(slug, label, f'{OBJ}/{p}') for p in fs]
ATOMS = {'circle': 'Circle', 'circle-hole': 'Ring', 'square': 'Square', 'square-hole': 'Socket', 'triangle': 'Triangle', 'triangle-hole': 'Aperture'}
items += [('idler', f'{v} · Idler shape unit', f'{R}/stage/idler/atoms/{k}.png') for k, v in ATOMS.items()]
MARKS = {'idler': ('idler', 'Idler mark'), 'artifice-glyph': ('artifice-brand', 'Artifice glyph'),
         'codex-foundry': ('codex-foundry', 'Codex Foundry mark'), 'fielder': ('fielder', 'Fielder mark'), 'biota': ('biota', 'Biota mark')}
items += [(slug, label, f'{SRC}/marks/{k}.png') for k, (slug, label) in MARKS.items() if os.path.exists(f'{SRC}/marks/{k}.png')]

tiles = []
for slug, label, f in items:
    im = Image.open(f).convert('RGBA'); im = im.crop(im.getbbox()); w, h = im.size; k = TILE / max(w, h)
    tiles.append((slug, label, os.path.relpath(f, f'{R}/stage'), im.resize((max(1, round(w * k)), max(1, round(h * k))), Image.LANCZOS)))

rows = (len(tiles) + COLS - 1) // COLS
atlas = Image.new('RGBA', (COLS * TILE, rows * TILE), (0, 0, 0, 0)); rects = []
for i, (_, _, _, im) in enumerate(tiles):
    x, y = (i % COLS) * TILE, (i // COLS) * TILE
    atlas.paste(im, (x, y)); rects.append([x, y, im.size[0], im.size[1]])
atlas.save(f'{G}/atlas.png', optimize=True)
subprocess.run(['cwebp', '-quiet', '-q', '88', '-alpha_q', '95', '-exact', f'{G}/atlas.png', '-o', f'{G}/atlas.webp'], check=True)
os.remove(f'{G}/atlas.png')
# flat marks and shape units sit smaller than the rendered artifacts, so the work leads
scale = [(.45 if ('/atoms/' in t[2] or '/marks/' in t[2]) else 1) for t in tiles]
json.dump({'tile': TILE, 'cols': COLS, 'slugs': [t[0] for t in tiles], 'labels': [t[1] for t in tiles], 'scale': scale,
           'rects': rects, 'src': [t[2] for t in tiles]}, open(f'{G}/atlas.json', 'w'))
print(len(tiles), 'objects', atlas.size, os.path.getsize(f'{G}/atlas.webp') // 1024, 'KB')
