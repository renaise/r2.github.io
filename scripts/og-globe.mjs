// Moving social card (2026-11-25, Renaise: "the social thumbnail is moving, only the globe, the
// center artifact highlighted while moving"). Renders the LIVE globe alone at 1200x630, turns it one
// full revolution so the loop is seamless, and highlights whichever tile is at the center as it turns
// (lifted, enlarged, outlined; the hand-over between tiles is continuous). Every frame waits for its
// images, which is what the retired 2026-11 GIF did not do (one frame caught an unloaded tile).
//
// Writes assets/og-globe.gif (og:image / twitter:image) and assets/og-globe.mp4 (og:video), plus
// assets/og-globe.jpg (frame 0, the still fallback). X, LinkedIn and iMessage show frame 0 only, so
// frame 0 is composed to stand on its own: the first artifact is already open.
//
// Run from the repo root (needs ffmpeg + system Chrome):
//   NODE_PATH=<dir with puppeteer-core>/node_modules node scripts/og-globe.mjs [https://renaise.com/]
import fs from 'fs';
import os from 'os';
import path from 'path';
import { execFileSync } from 'child_process';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const puppeteer = require('puppeteer-core');

const URL = process.argv[2] || 'https://renaise.com/';
const W = 1200, H = 630, FPS = 10, SECONDS = 14, HOLD = 1.75;   // one turn in 14s; a new artifact every 1.75s
const BOX = 700, Y0 = (BOX - H) / 2;   // render the globe in a taller box and crop the middle, so the sphere fills the card
const FRAMES = FPS * SECONDS;
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'og-globe-'));

const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new' });
const p = await b.newPage();
await p.setViewport({ width: 1600, height: 1000, deviceScaleFactor: 1 });
await p.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: 'dark' }, { name: 'prefers-reduced-motion', value: 'no-preference' }]);
// Expose the globe's closure: rotation, hover and the atlas. The page itself is untouched.
await p.setRequestInterception(true);
p.on('request', async r => {
  if (r.resourceType() !== 'document') return r.continue();
  const res = await fetch(r.url()); let html = await res.text();
  const hook = "window.__g3={setRot:function(y,x){rotY=y;if(x!=null)rotX=x;},hover:function(i){setHover(i);},cur:function(){return hover;},A:A,tiles:tiles,N:N,draw:function(){frame(performance.now());},stop:function(){spin=0;}};";
  if (!html.includes('function kick(){ if(!raf)')) throw new Error('globe hook point moved: update og-globe.mjs');
  html = html.replace('function kick(){ if(!raf)', hook + 'function kick(){ if(!raf)');
  r.respond({ status: 200, contentType: 'text/html; charset=utf-8', body: html });
});
await p.goto(URL, { waitUntil: 'networkidle2' });
// Only the globe, at card size, on the page's own ground.
await p.addStyleTag({ content: `
  html,body{overflow:hidden!important}
  .side{position:fixed!important;inset:0!important;width:${W}px!important;height:${BOX}px!important;padding:0!important;margin:0!important;border:0!important;
        -webkit-mask-image:none!important;mask-image:none!important;box-shadow:none!important;z-index:50!important;display:block!important}
  .side>*:not(.feed){display:none!important}
  .side>.feed{position:absolute!important;inset:0!important;min-height:0!important;margin:0!important}
  .sig.globe{width:${W}px!important;height:${BOX}px!important;max-height:none!important;min-height:0!important;flex:none!important;margin:0!important}
  .wrap,#cs{display:none!important}` });
await p.waitForFunction(() => window.__g3 && window.__g3.tiles.length, { timeout: 20000 });
await p.evaluate(async () => { const i = new Image(); i.src = '/stage/globe/atlas.webp?v=26'; await i.decode(); });
await p.evaluate(() => { window.__g3.stop(); });
await new Promise(r => setTimeout(r, 800));

const X0 = -0.12;   // nearly level, so tiles cross the middle all the way round
// The center highlight: every tile is lifted, enlarged and outlined by how squarely it faces the
// camera, so whichever tile turns through the middle of the globe is highlighted, and the highlight
// hands over smoothly from tile to tile as the globe turns (no pop-up, the globe stays whole).
const highlight = () => p.evaluate(() => {
  const g = window.__g3;
  g.tiles.forEach(o => {
    const op = parseFloat(o.el.style.opacity) || 0;
    // facing value from the opacity the globe just drew is not linear; recompute from the matrix instead
    const r = o.el.getBoundingClientRect(), bx = o.el.closest('.g3').getBoundingClientRect();
    const dx = (r.left + r.width / 2 - (bx.left + bx.width / 2)) / (bx.height * .39);
    const dy = (r.top + r.height / 2 - (bx.top + bx.height / 2)) / (bx.height * .39);
    const d = Math.hypot(dx, dy), h = op > .5 ? Math.pow(Math.max(0, 1 - d / .42), 1.6) : 0;
    o.el.style.transform = o.base + (h ? ' translateZ(' + (60 * h).toFixed(1) + 'px) scale(' + (1 + .9 * h).toFixed(3) + ')' : '');
    o.el.style.boxShadow = h ? '0 0 0 ' + (1.5 * h).toFixed(2) + 'px rgba(255,255,255,' + (.9 * h).toFixed(2) + '), 0 12px 40px rgba(0,0,0,' + (.6 * h).toFixed(2) + ')' : '';
    o.el.style.zIndex = h ? '5' : '';
    if (h) o.el.style.opacity = '1'; else o.el.style.opacity = (op * .72).toFixed(3);
  });
});

for (let f = 0; f < FRAMES; f++) {
  const rot = (f / FRAMES) * Math.PI * 2;
  await p.evaluate((r, x) => { window.__g3.setRot(r, x); window.__g3.draw(); }, rot, X0);
  await highlight();
  await p.screenshot({ path: path.join(tmp, `f${String(f).padStart(4, '0')}.png`), clip: { x: 0, y: Y0, width: W, height: H } });
}
await b.close();

const out = 'assets';
// GIF: X allows 5MB and most crawlers stop near there, so step down width, rate + colors until it fits.
const gif = path.join(out, 'og-globe.gif');
for (const [w, fps, colors] of [[1200, 10, 128], [960, 10, 112], [800, 10, 96], [800, 8, 80], [640, 8, 64]]) {
  execFileSync('ffmpeg', ['-loglevel', 'error', '-y', '-framerate', String(FPS), '-i', path.join(tmp, 'f%04d.png'),
    '-vf', `fps=${fps},scale=${w}:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=${colors}:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle`,
    '-loop', '0', gif]);
  const sz = fs.statSync(gif).size; console.log('gif', w, fps, colors, sz);
  if (sz < 4.8e6) break;
}
execFileSync('ffmpeg', ['-loglevel', 'error', '-y', '-framerate', String(FPS), '-i', path.join(tmp, 'f%04d.png'),
  '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '22', '-movflags', '+faststart', path.join(out, 'og-globe.mp4')]);
execFileSync('sips', ['-s', 'format', 'jpeg', '-s', 'formatOptions', '88', path.join(tmp, 'f0000.png'), '--out', path.join(out, 'og-globe.jpg')]);
fs.rmSync(tmp, { recursive: true, force: true });
for (const f of ['og-globe.gif', 'og-globe.mp4', 'og-globe.jpg']) console.log(f, fs.statSync(path.join(out, f)).size);
