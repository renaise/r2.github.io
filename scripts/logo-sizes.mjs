// Derive every card wordmark's --lw from its ink, so the logos share one optical size.
//
// Rule (2026-11-23): width = C x r^P x coverage^-Q, with r the mark's ink ratio.
// P = 0.5 would be strict equal area, which shrank long lockups until MAESTRO stood 9px
// tall beside a 15px SOOT. P = 0.75 is the damped version, picked by eye from a contact
// sheet against 0.5 / 0.65 / 0.85: long marks still run longer + shorter, never illegibly.
// Q = 0.1 is a light stroke-density correction; at 0.25 it pushed MAESTRO back down.
// OPTICAL holds the only hand factors, each with its reason. Keep it short.
// C holds the set's median height where it was, so the row as a whole keeps its size.
//
// Run from the repo root with a local server up:
//   python3 -m http.server 8731 &
//   NODE_PATH=<dir with puppeteer-core>/node_modules node scripts/logo-sizes.mjs          # report
//   NODE_PATH=... node scripts/logo-sizes.mjs --write                                   # rewrite index.html
// Re-run whenever a logo file or its --r changes. Glyph rows (.nmw.glyph) keep fixed height.
import fs from 'fs';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const puppeteer = require('puppeteer-core');

const URL = process.env.URL || 'http://localhost:8731/';
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new' });
const pg = await b.newPage();
await pg.setViewport({ width: 1440, height: 900 });
await pg.goto(URL, { waitUntil: 'networkidle2' });
const rows = await pg.evaluate(async () => {
  const out = [];
  for (const a of document.querySelectorAll('.proj[data-slug]')) {
    const cl = a.querySelector('.c0 .nmw:not(.glyph) .cl'); if (!cl) continue;
    const st = cl.getAttribute('style');
    const url = getComputedStyle(cl).webkitMaskImage.slice(5, -2);
    const img = new Image(); img.src = url; await img.decode();
    const W = 2000, H = Math.round(W / (img.naturalWidth / img.naturalHeight));
    const c = document.createElement('canvas'); c.width = W; c.height = H;
    const x = c.getContext('2d'); x.drawImage(img, 0, 0, W, H);
    const d = x.getImageData(0, 0, W, H).data;
    let n = 0, x0 = W, x1 = 0, y0 = H, y1 = 0, cov = 0;
    for (let y = 0; y < H; y++) for (let i = 0; i < W; i++) {
      const al = d[(y * W + i) * 4 + 3] / 255; if (al < 0.4) continue;
      cov += al; n++; if (i < x0) x0 = i; if (i > x1) x1 = i; if (y < y0) y0 = y; if (y > y1) y1 = y;
    }
    const iw = (x1 - x0 + 1) / W, ih = (y1 - y0 + 1) / W;     // ink box in units of the file's width
    const coverage = cov / ((x1 - x0 + 1) * (y1 - y0 + 1));
    const r = +st.match(/--r:([\d.]+)/)[1];
    const lw = +(st.match(/--lw:([\d.]+)em/) || [, 6])[1];
    out.push({ slug: a.dataset.slug, r, lw, iw, ih, coverage, style: st });
  }
  return out;
});
await b.close();

const P = 0.75, Q = 0.1;
const OPTICAL = {
  flora: 1.1, // the swash F sets the box height, so LORA's thin caps read a step small
};
const med = a => [...a].sort((x, y) => x - y)[Math.floor(a.length / 2)];
const raw = rows.map(m => Math.pow(m.iw / m.ih, P) * Math.pow(m.coverage, -Q) * (OPTICAL[m.slug] || 1));
const C = med(rows.map(m => m.lw / m.r)) / med(rows.map((m, i) => raw[i] / m.r));
let html = fs.readFileSync('index.html', 'utf8');
for (const [i, m] of rows.entries()) {
  const lw = C * raw[i];
  console.log(`${m.slug.padEnd(28)} cov ${m.coverage.toFixed(2)}  lw ${m.lw.toFixed(3)} -> ${lw.toFixed(3)}em  (height ${(lw / m.r).toFixed(3)}em)`);
  const next = m.style.replace(/--lw:[\d.]+em/, `--lw:${lw.toFixed(3)}em`);
  if (next !== m.style) html = html.split(`style="${m.style}"`).join(`style="${next}"`);
}
if (process.argv.includes('--write')) { fs.writeFileSync('index.html', html); console.log('index.html written'); }
