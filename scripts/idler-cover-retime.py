# Idler cover retime (2026-11-24): holds shortened, each morph/turn ~1.5x faster on a
# cubic-bezier(.42,0,.58,1) ease-in-out, fractional positions blended between source frames.
import sys,subprocess,numpy as np
SRC,OUT=sys.argv[1],sys.argv[2]; W,H,FPS=2560,1440,30
d=[float(l.split('=')[1]) for l in open('diff.txt') if 'YAVG' in l]
n=len(d)+0  # diff i = change between frame i-1 and i (tblend), first frame has none
N=n+1 if len(d)<480 else n
N=480
d=[0.0]+d[:N-1]
mov=[x>0.05 and x<5 for x in d]
# grow motion by 3 frames each side to catch soft tails
m=mov[:]
for i,v in enumerate(mov):
    if v:
        for j in range(max(0,i-3),min(N,i+4)): m[j]=True
# a hold shorter than 10 frames between two moves is part of one move
i=0
while i<N:
    if not m[i]:
        j=i
        while j<N and not m[j]: j+=1
        if 0<i and j<N and j-i<10:
            for k in range(i,j): m[k]=True
        i=j
    else: i+=1
cut=[x>=5 for x in d]
segs=[];i=0
while i<N:
    j=i
    while j+1<N and m[j+1]==m[i] and not cut[j+1]: j+=1
    segs.append((i,j+1,m[i])); i=j+1
def bez(x,p1=.42,p2=.58):
    lo,hi=0.0,1.0
    for _ in range(40):
        t=(lo+hi)/2; bx=3*(1-t)**2*t*p1+3*(1-t)*t*t*p2+t**3
        lo,hi=(t,hi) if bx<x else (lo,t)
    t=(lo+hi)/2; return 3*(1-t)*t*t+t**3   # y control points 0,1
pos=[]
for a,b,mv in segs:
    L=b-a
    if mv:
        k=L if L<6 else max(4,round(L/1.5))
        pos+= [a+(L-1)*bez(q/(k-1)) for q in range(k)] if k>1 else [a]
    else:
        k=max(1,round(L/1.9)) if L>6 else L
        pos+= [a+(L-1)*q/max(1,k-1) for q in range(k)] if k>1 else [a]
print('segments',[(a,b,mv) for a,b,mv in segs]); print('out frames',len(pos),'secs',len(pos)/FPS)
dec=subprocess.Popen(['ffmpeg','-v','error','-i',SRC,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
enc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
  '-c:v','libx264','-preset','slow','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart','-an',OUT],stdin=subprocess.PIPE)
fs=W*H*3; buf={}; nxt=0
def get(i):
    global nxt
    i=min(i,N-1)
    while nxt<=i:
        raw=dec.stdout.read(fs)
        if len(raw)<fs: buf[nxt]=buf[nxt-1]
        else: buf[nxt]=np.frombuffer(raw,np.uint8).reshape(H,W,3)
        nxt+=1
    for k in [k for k in buf if k<i-1]: del buf[k]
    return buf[i]
for p in pos:
    i=int(p); f=p-i
    if f<1e-3 or i+1>=N: fr=get(i)
    else:
        a=get(i).astype(np.float32); b=get(i+1).astype(np.float32); fr=(a*(1-f)+b*f+.5).astype(np.uint8)
    enc.stdin.write(fr.tobytes())
enc.stdin.close(); enc.wait(); dec.kill(); print('done')
