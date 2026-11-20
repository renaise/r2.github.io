#!/usr/bin/env python3
"""Atlas for the renaise.com rail globe, Moshpit-style (2026-11-19).

The globe is laid out like a Moshpit map: a round cloud of small images, one tight cluster
per project. That needs hundreds of images, so it draws on every project's stage folder:
each image once (near-duplicates dropped by look), each at its own proportions, small.

Left out: other people's work (the Depictions film shots and show photos, the Artifact
Index pieces, Aputure's pre-redesign site), the globe's own sources, near-empty frames.
The earlier 20-object cutout set is build-atlas-objects.py.

Run: python3 stage/globe/build-atlas.py
"""
import json, os, re, subprocess, tempfile, hashlib
from PIL import Image
R = os.path.expanduser('~/SEANCE/r2.github.io'); G = f'{R}/stage/globe'
TILE, COLS = 160, 16; TW, TH = 160, 120  # every tile the same 4:3 shape: the cohesion
html = open(f'{R}/index.html').read()
slugs = re.findall(r'<a class="proj" data-slug="([^"]+)"', html)
SKIP_SLUG = {'depictions-of-original-sin'}            # the six artists' film
SKIP_FILE = re.compile(r'(system|clusters|before|/globe/|atlas|og\.|favicon|frame-\d|show-\d|/art/|artifice-brand/plate|shell-turn|shell-card)', re.I)  # artifacts come from src/objects once
def dhash(im):
    g = im.convert('L').resize((17, 16), Image.LANCZOS); px = list(g.getdata())
    return sum(1 << i for i in range(256) if px[(i // 16) * 17 + i % 16] > px[(i // 16) * 17 + i % 16 + 1])

tmp = tempfile.mkdtemp(); tiles = []; hashes = []; zooms = []  # zooms: the full image behind each tile, for the hover zoom

def fit43(im):
    # Never crop (2026-11-19): the whole image sits inside the 4:3 tile on its dark ground.
    im = im.convert('RGB'); im.thumbnail((TW - 8, TH - 8), Image.LANCZOS)
    t = Image.new('RGB', (TW, TH), (13, 13, 14)); t.paste(im, ((TW - im.width) // 2, (TH - im.height) // 2))
    return t

# artifacts first: each cutout centred on the tile's dark ground
OBJ = f'{G}/src/objects'
ART = {'shell': 'idler', 'vector': 'idler', 'petri': 'osmosis', 'symbiota': 'biota', 'humanoid': 'studio-artifice'}
for fn in sorted(os.listdir(OBJ)) if os.path.isdir(OBJ) else []:
    key = fn.split('.')[0].split('-')[0]
    slug = ART.get(key) or {'primitive': 'artifice-brand', 'object': 'the-artifact-index'}.get(key)
    if not slug: continue
    o = Image.open(f'{OBJ}/{fn}').convert('RGBA'); o.thumbnail((int(TW * .86), int(TH * .86)), Image.LANCZOS)
    t = Image.new('RGBA', (TW, TH), (13, 13, 14, 255)); t.alpha_composite(o, ((TW - o.width) // 2, (TH - o.height) // 2))
    tiles.append((slug, t.convert('RGB'), 'globe/src/objects/' + fn)); hashes.append(dhash(t.convert('RGB')))
    zooms.append(Image.open(f'{OBJ}/{fn}').convert('RGBA'))


def _unused_dhash(im):
    g = im.convert('L').resize((17, 16), Image.LANCZOS); px = list(g.getdata())
    return sum(1 << i for i in range(256) if px[(i // 16) * 17 + i % 16] > px[(i // 16) * 17 + i % 16 + 1])

for slug in slugs:
    if slug in SKIP_SLUG: continue
    d = f'{R}/stage/{slug}'
    if not os.path.isdir(d): continue
    files = []
    for root, _, fs in os.walk(d):
        for f in sorted(fs):
            p = os.path.join(root, f)
            if SKIP_FILE.search(p): continue
            if re.search(r'\.(jpe?g|png|webp)$', f, re.I): files.append(('img', p))
            elif f.endswith('.mp4'): files += [('mp4', p, 0.6), ('mp4', p, 2.5)]
    for src in files:
        try:
            if src[0] == 'mp4':
                out = os.path.join(tmp, hashlib.md5(f'{src[1]}{src[2]}'.encode()).hexdigest() + '.png')
                subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(src[2]), '-i', src[1], '-frames:v', '1', out], check=True)
                if not os.path.exists(out): continue
                im = Image.open(out)
            else:
                im = Image.open(src[1])
            im = im.convert('RGB')
            lo, hi = im.convert('L').getextrema()
            if hi - lo < 24: continue
            h = dhash(im)
            if any(bin(h ^ o).count('1') < 34 for o in hashes): continue
            hashes.append(h)
            tiles.append((slug, fit43(im), os.path.relpath(src[1], f'{R}/stage'))); zooms.append(im)
        except Exception as e:
            print('skip', src[1], e)

# hover zoom: each tile's own image at up to 720px, loaded only when that tile opens
Z = f'{G}/z'; os.makedirs(Z, exist_ok=True)
for f in os.listdir(Z): os.remove(f'{Z}/{f}')
ars = []
for i, im in enumerate(zooms):
    im = im.copy(); im.thumbnail((720, 720), Image.LANCZOS); ars.append(round(im.width / im.height, 4))
    im.save(f'{Z}/{i:03d}.webp', 'WEBP', quality=86, method=6)

rows = (len(tiles) + COLS - 1) // COLS
atlas = Image.new('RGB', (COLS * TW, rows * TH), (13, 13, 14)); rects = []
for i, (_, im, _) in enumerate(tiles):
    x, y = (i % COLS) * TW, (i // COLS) * TH
    atlas.paste(im, (x, y)); rects.append([x, y, TW, TH])
atlas.save(f'{G}/atlas.png')
subprocess.run(['cwebp', '-quiet', '-q', '84', f'{G}/atlas.png', '-o', f'{G}/atlas.webp'], check=True)
os.remove(f'{G}/atlas.png')
names = dict(re.findall(r'"([a-z0-9-]+)": \{"name": "([^"]+)"', html))
json.dump({'tile': TILE, 'cols': COLS, 'slugs': [t[0] for t in tiles], 'labels': [names.get(t[0], t[0]) for t in tiles],
           'rects': rects, 'src': [t[2] for t in tiles], 'ar': ars}, open(f'{G}/atlas.json', 'w'))
from collections import Counter
print(len(tiles), 'images', atlas.size, os.path.getsize(f'{G}/atlas.webp') // 1024, 'KB'); print(Counter(t[0] for t in tiles))
