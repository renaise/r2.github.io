// Artifactory card cover: a sculpting pass in edit mode on the live tool, captured by CDP screencast (2026-11-24).
// Needs headed Chrome (WebGL). P=<outdir> node scripts/artifactory-edit-capture.mjs, then ffmpeg -f concat list.txt to stage/artifactory/edit.mp4.
import { chromium } from 'playwright';
import fs from 'fs';
const OUT=process.env.P+'/rec/';
fs.mkdirSync(OUT,{recursive:true});
const b=await chromium.launch({channel:'chrome',headless:false,args:['--window-position=-2400,0']});
const pg=await b.newPage({viewport:{width:1440,height:810},deviceScaleFactor:2});
await pg.goto('https://artifactory.codexfoundry.com',{waitUntil:'networkidle'}); await pg.waitForTimeout(3000);
await pg.getByText('Edit mode',{exact:true}).first().click(); await pg.waitForTimeout(1200);
await pg.mouse.click(82,421); await pg.waitForTimeout(1500);           // base mesh: sphere
await pg.mouse.click(522,781); await pg.waitForTimeout(300); await pg.mouse.click(372,781); await pg.waitForTimeout(300);
await pg.mouse.move(1300,500);
const cdp=await pg.context().newCDPSession(pg); const frames=[];
cdp.on('Page.screencastFrame',async f=>{ frames.push({t:f.metadata.timestamp,d:f.data}); try{await cdp.send('Page.screencastFrameAck',{sessionId:f.sessionId});}catch(e){} });
await cdp.send('Page.startScreencast',{format:'jpeg',quality:88,maxWidth:2880,maxHeight:1620,everyNthFrame:1});
const W=ms=>pg.waitForTimeout(ms);
async function stroke(pts,steps=40){ await pg.mouse.move(...pts[0]); await pg.mouse.down();
  for(let i=1;i<pts.length;i++){ const [x0,y0]=pts[i-1],[x1,y1]=pts[i]; for(let k=1;k<=steps;k++){ await pg.mouse.move(x0+(x1-x0)*k/steps,y0+(y1-y0)*k/steps); await W(8);} }
  await pg.mouse.up(); }
await W(900);
await stroke([[560,300],[720,260],[880,320]]);
await stroke([[540,420],[720,400],[900,440]]);
await W(300);
await pg.keyboard.press('i'); await W(400);
await stroke([[700,520],[740,560],[780,520]],30);
await W(300);
await pg.keyboard.press('Shift+C'); await W(400);
await stroke([[600,600],[720,640],[840,600]]);
await W(400);
await W(600);
await pg.keyboard.press('s'); await W(300);
await stroke([[600,330],[800,350]],30);
await W(1200);
await cdp.send('Page.stopScreencast');
let list=''; frames.forEach((f,i)=>{ const fn=`f${String(i).padStart(4,'0')}.jpg`; fs.writeFileSync(OUT+fn,Buffer.from(f.d,'base64')); const dur=i<frames.length-1?frames[i+1].t-f.t:0.04; list+=`file '${fn}'\nduration ${dur.toFixed(4)}\n`; });
fs.writeFileSync(OUT+'list.txt',list); await pg.screenshot({path:OUT+'../rec-end.png'}); console.log('frames',frames.length,'secs',(frames.at(-1).t-frames[0].t).toFixed(2));
await b.close();
