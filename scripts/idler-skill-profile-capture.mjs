// idler.ai Skill Profile: all six models, then each model on its own in turn, as if tabbed through.
// STAGED (Renaise, 2026-11-24): idler.ai's model buttons are not interactive, so the one-model state is
// set during capture with the site's own isolation styles (.skwrap[data-iso], .skiso on series + chip). CDP screencast, headed for 2x.
import { chromium } from 'playwright';
import fs from 'fs';
const OUT=process.env.O+'/sprec/'; fs.rmSync(OUT,{recursive:true,force:true}); fs.mkdirSync(OUT,{recursive:true});
const b=await chromium.launch({channel:'chrome',headless:false,args:['--window-position=-2400,0']});
const pg=await b.newPage({viewport:{width:1440,height:810},deviceScaleFactor:2});
await pg.addInitScript(()=>{ addEventListener('DOMContentLoaded',()=>{ const c=document.createElement('div');
  c.innerHTML='<svg width="18" height="22" viewBox="0 0 18 22"><path d="M1 1v17l4.6-4.3 3 6.8 2.8-1.2-3-6.6H15z" fill="#111" stroke="#fff" stroke-width="1.3" stroke-linejoin="round"/></svg>';
  Object.assign(c.style,{position:'fixed',left:'0',top:'0',zIndex:2147483647,pointerEvents:'none',transform:'translate(-100px,-100px)'}); document.body.appendChild(c);
  addEventListener('mousemove',e=>{c.style.transform=`translate(${e.clientX-1}px,${e.clientY-1}px)`},true); }); });
const W=ms=>pg.waitForTimeout(ms);
await pg.goto('https://idler.ai/collections/shelflife',{waitUntil:'networkidle'}); await W(1500);
const top=await pg.evaluate(()=>{const h=[...document.querySelectorAll('body *')].find(e=>e.childElementCount<=1&&/^\s*Skill Profile/.test(e.textContent)&&e.textContent.length<40);return h.getBoundingClientRect().top+scrollY});
await pg.evaluate(y=>scrollTo(0,y-40),top); await pg.mouse.move(1439,809); await W(900);
// hide the pinned nav + tab row so the frame can sit centered on the chart (equal margins)
await pg.evaluate(()=>{const t=[...document.querySelectorAll('a')].find(a=>a.textContent.trim()==='Leaderboard'); if(t) t.parentElement.style.visibility='hidden';
  for(const e of document.querySelectorAll('header,nav')) e.style.visibility='hidden';
  for(const e of document.querySelectorAll('body *')){ if(e.childElementCount<=2&&/^\s*(Skill Profile|Model performance on the tasks tagged)/.test(e.textContent)&&e.textContent.length<80) e.style.visibility='hidden'; }
  const r=[...document.querySelectorAll('svg')].map(s=>s.getBoundingClientRect()).find(r=>r.width>600&&r.height>400);
  const chips=[...document.querySelectorAll('.mtagnm')].map(e=>e.getBoundingClientRect()); window.__box=[r.top, Math.max(...chips.map(c=>c.bottom))]; });
console.log('content y', await pg.evaluate(()=>window.__box));
const chip=n=>pg.evaluate(n=>{const e=[...document.querySelectorAll('button,[role=button],div,span')].filter(e=>e.textContent.trim()===n).sort((a,b)=>a.getBoundingClientRect().width-b.getBoundingClientRect().width).pop();const r=e.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]},n);
const cdp=await pg.context().newCDPSession(pg); const frames=[];
cdp.on('Page.screencastFrame',async f=>{frames.push({t:f.metadata.timestamp,d:f.data});try{await cdp.send('Page.screencastFrameAck',{sessionId:f.sessionId})}catch(e){}});
await cdp.send('Page.startScreencast',{format:'jpeg',quality:90,maxWidth:2880,maxHeight:1620});
await W(1300);
await pg.addStyleTag({content:'.skwrap[data-iso] .skseries.skiso:not(.sktop){display:inline!important;opacity:1!important} .skwrap[data-iso] .skseries.skiso:not(.sktop) .skline{stroke:var(--mc)!important;stroke-width:2.6px!important;fill:var(--mc)!important;fill-opacity:.16!important} .skwrap[data-iso] .skseries.sktop{display:none!important}'});
const iso=i=>pg.evaluate(i=>{const w=document.querySelector('.skwrap'); const ser=[...w.querySelectorAll('.skseries')], chips=[...w.querySelectorAll('.skchip')];
  if(i<0){ w.removeAttribute('data-iso'); ser.forEach(g=>g.classList.remove('skiso')); chips.forEach(c=>c.classList.remove('skiso')); return; }
  w.setAttribute('data-iso',''); const mk=ser[i].getAttribute('data-mk');
  ser.forEach(g=>g.classList.toggle('skiso',g.getAttribute('data-mk')===mk)); chips.forEach((c,k)=>c.classList.toggle('skiso',k===i)); },i);
for(let i=0;i<6;i++){ await iso(i); await W(1700); }
await iso(-1); await W(1400);

await cdp.send('Page.stopScreencast');
let list=''; frames.forEach((f,i)=>{const fn=`f${String(i).padStart(4,'0')}.jpg`; fs.writeFileSync(OUT+fn,Buffer.from(f.d,'base64')); const dur=i<frames.length-1?frames[i+1].t-f.t:0.04; list+=`file '${fn}'\nduration ${dur.toFixed(4)}\n`;});
fs.writeFileSync(OUT+'list.txt',list); console.log('frames',frames.length,'secs',(frames.at(-1).t-frames[0].t).toFixed(2));
await b.close();
