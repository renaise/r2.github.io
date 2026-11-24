// Artifactory card cover: one whole use case in edit mode on the live tool, captured by CDP screencast.
// Pick a base mesh, frame it small, sculpt with mirror symmetry (draw, inflate, crease, smooth),
// check the topology in wireframe, then open Export. Headed Chrome (WebGL).
// P=<outdir> node scripts/artifactory-edit-capture.mjs ; ZOOM=<wheel ticks> to tune the framing.
import { chromium } from 'playwright';
import fs from 'fs';
const OUT=process.env.P+'/rec/'; fs.mkdirSync(OUT,{recursive:true});
const TICKS=+(process.env.ZOOM||3), PROBE=!!process.env.PROBE;
const b=await chromium.launch({channel:'chrome',headless:false,args:['--window-position=-2400,0']});
const pg=await b.newPage({viewport:{width:1440,height:810},deviceScaleFactor:2});
const W=ms=>pg.waitForTimeout(ms);
await pg.goto('https://artifactory.codexfoundry.com',{waitUntil:'networkidle'}); await W(3000);
await pg.getByText('Edit mode',{exact:true}).first().click(); await W(1200);
await pg.mouse.click(372,781); await W(200);            // radius ~20%
await pg.mouse.click(518,781); await W(200);            // strength ~18%
await pg.mouse.move(1250,300);
let frames=[], cdp;
if(!PROBE){ cdp=await pg.context().newCDPSession(pg);
  cdp.on('Page.screencastFrame',async f=>{ frames.push({t:f.metadata.timestamp,d:f.data}); try{await cdp.send('Page.screencastFrameAck',{sessionId:f.sessionId});}catch(e){} });
  await cdp.send('Page.startScreencast',{format:'jpeg',quality:88,maxWidth:2880,maxHeight:1620}); }
await W(700);
// 1. choose the base mesh, then pull the camera back so the form sits small in the viewport
await pg.mouse.move(82,421,{steps:12}); await W(250); await pg.mouse.click(82,421); await W(700);
await pg.mouse.move(1000,420,{steps:12});
for(let i=0;i<TICKS;i++){ await pg.mouse.wheel(0,200); await W(140); }
await W(600);
if(PROBE){ await pg.screenshot({path:OUT+'../probe.png'}); await b.close(); process.exit(0); }
const C=[720,410], R=+(process.env.R||130);
const at=(u,v)=>[C[0]+u*R, C[1]+v*R];
async function stroke(pts,steps=26,ms=9){ await pg.mouse.move(...at(...pts[0]),{steps:6}); await pg.mouse.down();
  for(let i=1;i<pts.length;i++){ const [x0,y0]=at(...pts[i-1]),[x1,y1]=at(...pts[i]); for(let k=1;k<=steps;k++){ await pg.mouse.move(x0+(x1-x0)*k/steps,y0+(y1-y0)*k/steps); await W(ms);} }
  await pg.mouse.up(); await W(150); }
// 2. draw: a brow ridge and a band, mirrored across X
await stroke([[-.15,-.55],[-.45,-.45],[-.7,-.2]]);
await stroke([[-.1,.05],[-.5,.1],[-.8,.25]]);
// 3. inflate a crown
await pg.keyboard.press('i'); await W(350);
await stroke([[0,-.75],[-.15,-.7],[0,-.65]],18);
// 4. crease a seam
await pg.keyboard.press('Shift+C'); await W(350);
await stroke([[-.05,.45],[-.4,.5],[-.65,.4]]);
// 5. smooth it back
await pg.keyboard.press('s'); await W(300);
await stroke([[-.2,-.2],[-.5,0],[-.2,.25]],22);
// 6. check the topology
await W(300); await pg.mouse.move(1072,71,{steps:14}); await W(200); await pg.mouse.click(1072,71); await W(1600);
await pg.mouse.click(1072,71); await W(500);
// 7. export
await pg.mouse.move(1398,71,{steps:16}); await W(250); await pg.mouse.click(1398,71); await W(1800);
await pg.screenshot({path:OUT+'../rec2-end.png'});
await cdp.send('Page.stopScreencast');
let list=''; frames.forEach((f,i)=>{ const fn=`f${String(i).padStart(4,'0')}.jpg`; fs.writeFileSync(OUT+fn,Buffer.from(f.d,'base64')); const dur=i<frames.length-1?frames[i+1].t-f.t:0.04; list+=`file '${fn}'\nduration ${dur.toFixed(4)}\n`; });
fs.writeFileSync(OUT+'list.txt',list); console.log('frames',frames.length,'secs',(frames.at(-1).t-frames[0].t).toFixed(2));
await b.close();
