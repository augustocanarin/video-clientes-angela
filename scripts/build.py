import sys, os, json, subprocess, hashlib, wave
import numpy as np
from PIL import Image, ImageOps, ImageDraw
sys.path.insert(0,'/home/user/media/scripts')
from edl import SEGS, IMG, V, TR, R
W,H,FPS,SR=1080,1920,30,48000
WK='/home/user/media/work'; CACHE=WK+'/cache'; PCS=WK+'/pieces'
HDR="zscale=w=1080:h=1920:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0:peak=4,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,eq=saturation=1.06"
SDR="scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,format=yuv420p"
ISHDR={}
def run(c): subprocess.run(c,check=True)
def is_hdr(v):
    if v not in ISHDR:
        o=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=color_transfer','-of','csv=p=0',R+V[v]],capture_output=True,text=True).stdout
        ISHDR[v]='b67' in o or '2084' in o
    return ISHDR[v]
def F(sec): return int(round(sec*FPS))
_imgc={}
def load(k, cover):
    key=(k,cover)
    if key in _imgc: return _imgc[key]
    im=ImageOps.exif_transpose(Image.open(R+IMG[k])).convert('RGB')
    cw,ch=cover; s=max(cw/im.width, ch/im.height)*1.3
    if s<1: im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
    _imgc[key]=im; return im
def ease(x): return x*x*(3-2*x)
def rects(im, size, m):
    iw,ih=im.size; ar=size[0]/size[1]
    if iw/ih>ar: bh=ih; bw=ih*ar
    else: bw=iw; bh=iw/ar
    cx,cy=iw/2,ih/2
    def r(cx,cy,w,h): return (cx-w/2,cy-h/2,cx+w/2,cy+h/2)
    if m=='zin': return r(cx,cy,bw,bh), r(cx,cy,bw*0.86,bh*0.86)
    if m=='zout': return r(cx,cy,bw*0.86,bh*0.86), r(cx,cy,bw,bh)
    sc=0.92; w,h=bw*sc,bh*sc
    span=min((iw-w)/2, iw*0.16)
    a=r(cx-span,cy,w,h); b=r(cx+span,cy,w,h)
    return (a,b) if m=='panlr' else (b,a)
def lerp(a,b,t): return tuple(x+(y-x)*t for x,y in zip(a,b))
def frames_img(k,n,m,size=(W,H)):
    im=load(k,size); a,b=rects(im,size,m)
    for i in range(n):
        t=ease(i/max(1,n-1))
        yield im.transform(size,Image.EXTENT,lerp(a,b,t),Image.BICUBIC)
def frames_split(ka,kb,n):
    hh=(H-6)//2
    ga=frames_img(ka,n,'zin',(W,hh)); gb=frames_img(kb,n,'zin',(W,hh))
    for fa,fb in zip(ga,gb):
        c=Image.new('RGB',(W,H),(214,178,110)); c.paste(fa,(0,0)); c.paste(fb,(0,hh+6)); yield c
def enc_frames(gen,n,out,fi,fo):
    p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
        '-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-r',str(FPS),out],stdin=subprocess.PIPE)
    fin,fon=F(fi),F(fo)
    for i,fr in enumerate(gen):
        g=1.0
        if fin and i<fin: g=min(g,(i+1)/fin)
        if fon and i>=n-fon: g=min(g,(n-i)/fon)
        a=np.asarray(fr,dtype=np.float32 if g<1 else np.uint8)
        if g<1: a=(a*g).astype(np.uint8)
        p.stdin.write(a.tobytes())
    p.stdin.close(); assert p.wait()==0
def enc_clip(v,a,n,out,fi,fo):
    vf=(HDR if is_hdr(v) else SDR)+f',fps={FPS}'
    if fi: vf+=f',fade=t=in:d={fi}'
    if fo: vf+=f',fade=t=out:st={n/FPS-fo:.3f}:d={fo}'
    run(['ffmpeg','-v','error','-y','-ss',f'{a:.3f}','-i',R+V[v],'-an','-vf',vf,'-frames:v',str(n),
         '-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-r',str(FPS),out])
def piece(spec,n,fi=0,fo=0):
    h=hashlib.md5(json.dumps([spec,n,fi,fo],sort_keys=True).encode()).hexdigest()[:12]
    out=f'{PCS}/{h}.mp4'
    if not os.path.exists(out):
        kind=spec[0]
        if kind=='img': enc_frames(frames_img(spec[1],n,spec[2]),n,out,fi,fo)
        elif kind=='split': enc_frames(frames_split(spec[1],spec[2],n),n,out,fi,fo)
        elif kind=='clip': enc_clip(spec[1],spec[2],n,out,fi,fo)
    return out
def audio(v,a,n,kind):
    ns=n*SR//FPS
    if kind=='mute': return np.zeros((ns,2),np.float32)
    dur=n/FPS
    af='highpass=f=80,afftdn=nr=8:nf=-40,loudnorm=I=-16:TP=-1.5:LRA=9' if kind=='voice' else 'highpass=f=100,loudnorm=I=-30:TP=-8'
    raw=subprocess.run(['ffmpeg','-v','error','-ss',f'{a:.3f}','-i',R+V[v],'-t',f'{dur+0.5:.3f}','-vn','-af',af,'-ar',str(SR),'-ac','2','-f','f32le','-'],capture_output=True,check=True).stdout
    x=np.frombuffer(raw,np.float32).reshape(-1,2)[:ns].copy()
    if len(x)<ns: x=np.vstack([x,np.zeros((ns-len(x),2),np.float32)])
    fl=int(0.03*SR); r=np.linspace(0,1,fl)[:,None]; x[:fl]*=r; x[-fl:]*=r[::-1]
    return x

def build():
    vid=[]; aud=[]; voice_ranges=[]; ovs=[]; caps=[]; T=0
    for s in SEGS:
        fi,fo=s.get('fi',0),s.get('fo',0)
        if s['t']=='img':
            n=F(s['d']); vid.append(piece(('img',s['k'],s['m']),n,fi,fo)); aud.append(audio(None,0,n,'mute'))
        elif s['t']=='split':
            n=F(s['d']); vid.append(piece(('split',s['a'],s['b']),n,fi,fo)); aud.append(audio(None,0,n,'mute'))
        elif s['t']=='clip':
            n=F(s['d']); vid.append(piece(('clip',s['v'],s['a']),n,fi,fo)); aud.append(audio(s['v'],s['a'],n,s['audio']))
        elif s['t']=='talk':
            n=F(s['b']-s['a']); pos=0; cuts=sorted(s['cuts'])
            bounds=[]
            for c0,c1,sp in cuts: bounds.append((F(c0),F(c1),sp))
            segs=[]; 
            for f0,f1,sp in bounds:
                if f0>pos: segs.append((pos,f0,('clip',s['v'],s['a']+pos/FPS)))
                segs.append((f0,min(f1,n),('clip',sp[1],sp[2]) if sp[0]=='clip' else ('img',sp[1],sp[2]))); pos=min(f1,n)
            if pos<n: segs.append((pos,n,('clip',s['v'],s['a']+pos/FPS)))
            for j,(f0,f1,sp) in enumerate(segs):
                vid.append(piece(sp,f1-f0, fi if j==0 else 0, fo if j==len(segs)-1 else 0))
            aud.append(audio(s['v'],s['a'],n,'voice')); voice_ranges.append((T/FPS,(T+n)/FPS))
            if s['v'] in TR and s.get('captions',True):
                d=json.load(open(f"{WK}/transcripts/{TR[s['v']]}.json"))
                for seg in d['segments']:
                    for w in seg['words']:
                        if w['s']>=s['a']-0.05 and w['e']<=s['b']+0.15:
                            caps.append((T/FPS+w['s']-s['a'], T/FPS+min(w['e'],s['b'])-s['a'], w['w'].strip()))
        for o in s.get('ov',[]): ovs.append((o[0],T/FPS+o[1],T/FPS+o[2])+tuple(o[3:]))
        T+=n
    total=T/FPS
    with open(WK+'/concat.txt','w') as f:
        for p in vid: f.write(f"file '{p}'\n")
    run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',WK+'/concat.txt','-c','copy',WK+'/video.mp4'])
    A=np.vstack(aud)
    json.dump(dict(total=total,voice=voice_ranges,ovs=ovs,caps=caps),open(WK+'/timeline.json','w'),ensure_ascii=False,indent=1)
    def wav(path,x):
        w=wave.open(path,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x,-1,1)*32767).astype(np.int16).tobytes()); w.close()
    wav(WK+'/voice.wav',A)
    # trilha com ducking
    raw=subprocess.run(['ffmpeg','-v','error','-i',WK+'/audio/music.wav','-ar',str(SR),'-ac','2','-f','f32le','-'],capture_output=True,check=True).stdout
    M=np.frombuffer(raw,np.float32).reshape(-1,2)[:len(A)].copy()
    if len(M)<len(A): M=np.vstack([M,np.zeros((len(A)-len(M),2),np.float32)])
    t=np.arange(len(A))/SR; g=np.full(len(A),0.75,np.float32)
    lo=0.11
    for a,b in voice_ranges:
        r=0.5; m=(t>=a-r)&(t<=b+r)
        k=np.ones(m.sum(),np.float32); tt=t[m]
        k=np.minimum(k,np.clip((tt-(a-r))/r,0,1)); k=np.minimum(k,np.clip(((b+r)-tt)/r,0,1))
        g[m]=np.minimum(g[m], 0.75-(0.75-lo)*k)
    fo=int(3*SR); g[-fo:]*=np.linspace(1,0,fo); fi=int(1*SR); g[:fi]*=np.linspace(0,1,fi)
    wav(WK+'/music_ducked.wav',M*g[:,None])
    wav(WK+'/mix.wav',A+M*g[:,None]*0.9)
    print('total',total,'pieces',len(vid))
if __name__=='__main__': build()
