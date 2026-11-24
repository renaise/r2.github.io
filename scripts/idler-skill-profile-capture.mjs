// idler.ai Skill Profile: all six models, then a clockwise sweep of the ten skills (hover isolates each skill's scores). CDP screencast, headed for 2x.
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
await pg.evaluate(y=>scrollTo(0,y-40),top); await pg.mouse.move(1180,300); await W(900);
const chip=n=>pg.evaluate(n=>{const e=[...document.querySelectorAll('button,[role=button],div,span')].filter(e=>e.textContent.trim()===n).sort((a,b)=>a.getBoundingClientRect().width-b.getBoundingClientRect().width).pop();const r=e.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]},n);
const cdp=await pg.context().newCDPSession(pg); const frames=[];
cdp.on('Page.screencastFrame',async f=>{frames.push({t:f.metadata.timestamp,d:f.data});try{await cdp.send('Page.screencastFrameAck',{sessionId:f.sessionId})}catch(e){}});
await cdp.send('Page.startScreencast',{format:'jpeg',quality:90,maxWidth:2880,maxHeight:1620});
await W(1300);
// sweep the ten skills clockwise from the top; each hover isolates the leader and shows the scores
for(let i=0;i<10;i++){ const t=i*Math.PI/5, x=720+150*Math.sin(t), y=365-150*Math.cos(t); await pg.mouse.move(x,y,{steps:i?14:22}); await W(1250); }
await pg.mouse.move(1180,300,{steps:24}); await W(1300);
await cdp.send('Page.stopScreencast');
let list=''; frames.forEach((f,i)=>{const fn=`f${String(i).padStart(4,'0')}.jpg`; fs.writeFileSync(OUT+fn,Buffer.from(f.d,'base64')); const dur=i<frames.length-1?frames[i+1].t-f.t:0.04; list+=`file '${fn}'\nduration ${dur.toFixed(4)}\n`;});
fs.writeFileSync(OUT+'list.txt',list); console.log('frames',frames.length,'secs',(frames.at(-1).t-frames[0].t).toFixed(2));
await b.close();
