// Social card (assets/og.jpg 2400x1260 + og-1200.jpg), rendered from the live globe so it never drifts
// from the site. 2026-11-24: a still replaces the 800px animated GIF (5MB, low-res, X never animates it,
// one frame caught an unloaded tile).
// Run from the repo root with `python3 -m http.server 8731` up, Playwright + system Chrome:
//   node scripts/og-card.mjs
import { chromium } from 'playwright';
import fs from 'fs';
const URL='http://localhost:8731/';
const b=await chromium.launch({channel:'chrome'});
// 1. the globe, large, untouched by hover
const g=await b.newPage({viewport:{width:1600,height:1600},deviceScaleFactor:2,colorScheme:'dark'});
await g.goto(URL,{waitUntil:'networkidle'});
await g.addStyleTag({content:`.side{width:1000px !important} .sig.globe{height:1000px !important;max-height:none !important;flex:none !important}`});
await g.mouse.move(1590,1590); await g.waitForTimeout(5000);
const globe=(await g.locator('.g3').first().screenshot()).toString('base64');
// 2. the card
const c=await b.newPage({viewport:{width:1200,height:630},deviceScaleFactor:2});
await c.goto(URL+'assets/');
await c.setContent(`<!doctype html><html><head><style>
@font-face{font-family:R;src:url("${URL}fonts/Redaction-Regular.woff2")}
@font-face{font-family:D;src:url("${URL}fonts/Cargo-DiatypePlusVariable.woff2");font-weight:100 900}
html,body{margin:0;width:1200px;height:630px;background:#161718;overflow:hidden}
.g{position:absolute;width:660px;height:660px;left:540px;top:-15px;background:url(data:image/png;base64,${globe}) center/contain no-repeat}
.l{position:absolute;left:64px;top:56px;bottom:56px;width:430px;display:flex;flex-direction:column;justify-content:space-between}
.mk{height:64px;aspect-ratio:3802/1888;background:#c4c4c4;-webkit-mask:url(${URL}assets/signature.svg) left center/contain no-repeat}
p{margin:0;font:400 38px/1.18 R,serif;color:#c4c4c4;letter-spacing:-.005em}
.u{margin-top:22px;font:400 15px/1 D,sans-serif;color:#6e6e6e;letter-spacing:.01em}
</style></head><body><div class="g"></div><div class="l"><div class="mk"></div><div><p>Renaise is a designer and curator working from web to world.</p><div class="u">renaise.com</div></div></div></body></html>`);
await c.evaluate(()=>document.fonts.ready); await c.waitForTimeout(800);
await c.screenshot({path:'assets/og.jpg',type:'jpeg',quality:88});
await b.close();
import { execFileSync } from 'child_process';
execFileSync('sips',['-Z','1200','assets/og.jpg','--out','assets/og-1200.jpg']);
console.log('og.jpg + og-1200.jpg written');
