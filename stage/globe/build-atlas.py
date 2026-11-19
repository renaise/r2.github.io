#!/usr/bin/env python3
"""Thumbnail atlas for the renaise.com rail globe: up to PER images from every project's
stage folder (stills, plus a frame from each video), square-cropped to TILE px, packed into
one JPEG, with a JSON map of tile -> project slug."""
import json, os, re, subprocess, tempfile, hashlib
from PIL import Image
R = os.path.expanduser('~/SEANCE/r2.github.io')
TILE, PER, COLS = 128, 16, 16
html = open(f'{R}/index.html').read()
cards = re.findall(r'<a class="proj" data-slug="([^"]+)"', html)
stage_dir = {s: s for s in cards}
stage_dir.update({'aputure': 'aputure'})
tmp = tempfile.mkdtemp()
tiles = []
hashes = []
looks = []
for slug in cards:
    d = f'{R}/stage/{stage_dir[slug]}'
    if not os.path.isdir(d): print('no stage for', slug); continue
    files = []
    for root, dirs, fs in os.walk(d):
        dirs[:] = [x for x in dirs if x != 'atoms']  # six flat shape units read as one repeated tile
        for f in sorted(fs):
            p = os.path.join(root, f)
            if re.search(r'\.(jpe?g|png|webp)$', f, re.I) and 'system' not in f and 'clusters' not in f: files.append(p)
            elif f.endswith('.mp4'): files.append(p)
    # stills first, then videos; skip a still when a video of the same name gives the frame
    seen, picked = set(), []
    for p in files:
        key = re.sub(r'\.(mp4|jpe?g|png|webp)$', '', os.path.basename(p))
        if key in seen: continue
        seen.add(key); picked.append(p)
    for p in picked[:PER]:
        try:
            if p.endswith('.mp4'):
                out = os.path.join(tmp, hashlib.md5(p.encode()).hexdigest() + '.png')
                subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '1', '-i', p, '-frames:v', '1', out], check=True)
                im = Image.open(out)
            else:
                im = Image.open(p)
            # Keep the image's own proportions (2026-11-19): fit inside the TILE cell, uncropped.
            im = im.convert('RGB'); w, h = im.size; k = TILE / max(w, h)
            im = im.resize((max(1, round(w * k)), max(1, round(h * k))), Image.LANCZOS)
            # near-empty frames (flat ground) say nothing; skip them
            if max(im.convert('L').getextrema()) - min(im.convert('L').getextrema()) < 24: continue
            # no repeats: drop anything visually near an image already kept (difference hash)
            g = im.convert('L').resize((17, 16), Image.LANCZOS); px = list(g.getdata())
            h = sum(1 << i for i in range(256) if px[(i // 16) * 17 + i % 16] > px[(i // 16) * 17 + i % 16 + 1])
            # and a coarse look: the 12x12 gray thumbnail, normalized; near = same picture
            q = [v / 255 for v in im.convert('L').resize((12, 12), Image.LANCZOS).getdata()]
            m = sum(q) / len(q); sd = (sum((v - m) ** 2 for v in q) / len(q)) ** .5 or 1; q = [(v - m) / sd for v in q]
            near = lambda a: sum(x * y for x, y in zip(a, q)) / len(q) > .80
            if any(bin(h ^ o).count('1') < 40 for o in hashes) or any(near(a) for a in looks): continue
            hashes.append(h); looks.append(q); tiles.append((slug, im))
        except Exception as e:
            print('skip', p, e)
rows = (len(tiles) + COLS - 1) // COLS
atlas = Image.new('RGB', (COLS * TILE, rows * TILE), (16, 16, 16))
rects = []
for i, (slug, im) in enumerate(tiles):
    x, y = (i % COLS) * TILE, (i // COLS) * TILE
    atlas.paste(im, (x, y)); rects.append([x, y, im.size[0], im.size[1]])
os.makedirs(f'{R}/stage/globe', exist_ok=True)
atlas.save(f'{R}/stage/globe/atlas.jpg', quality=80, optimize=True, progressive=True)
names = dict(re.findall(r'<a class="proj" data-slug="([^"]+)".*?<b>([^<]+)</b>', html, re.S))
json.dump({'tile': TILE, 'cols': COLS, 'slugs': [s for s, _ in tiles], 'rects': rects}, open(f'{R}/stage/globe/atlas.json', 'w'))
from collections import Counter
print(len(tiles), 'tiles', atlas.size, os.path.getsize(f'{R}/stage/globe/atlas.jpg') // 1024, 'KB')
print(Counter(s for s, _ in tiles))
