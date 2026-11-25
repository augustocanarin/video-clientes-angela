import sys, json, re
sys.path.insert(0,'/home/user/media/scripts')
from edl import SEGS, TR
FPS=30; WK='/home/user/media/work'
def F(x): return int(round(x*FPS))
GOLD='&H007AC2E3&'
def ts(t):
    t=max(0,t); h=int(t//3600); m=int(t%3600//60); s=t%60
    return f"{h}:{m:02d}:{s:05.2f}"
# timeline
T=0; ovs=[]; words=[]
for s in SEGS:
    n=F(s['b']-s['a']) if s['t']=='talk' else F(s['d'])
    if s['t']=='talk' and s['v'] in TR:
        d=json.load(open(f"{WK}/transcripts/{TR[s['v']]}.json"))
        for seg in d['segments']:
            for w in seg['words']:
                if w['s']>=s['a']-0.05 and w['e']<=s['b']+0.15:
                    words.append([T/FPS+w['s']-s['a'], T/FPS+min(w['e'],s['b'])-s['a'], w['w'].strip(), (T+n)/FPS])
    for o in s.get('ov',[]): ovs.append((o[0],T/FPS+o[1],T/FPS+o[2])+tuple(o[3:]))
    T+=n
FIX={'3mm,':'3 mm,','Maxi,':'Maxi,'}
EMPH={'maxi','grandioso','reaproveitar','mdf','laser','nevadas','led','silicone','brasil','arquivos','decortela','incrível','papelão','camadas','sombras','lanternas','corre','lema','20','iluminadas','triangulares','choque'}
def clean(w): return re.sub(r'[^\wÀ-ú]','',w).lower()
chunks=[]; cur=[]
for i,w in enumerate(words):
    w[2]=FIX.get(w[2],w[2]); cur.append(w)
    txt=' '.join(x[2] for x in cur)
    nxt=words[i+1] if i+1<len(words) else None
    brk = nxt is None or nxt[0]-w[1]>0.6 or len(txt)>20 or len(cur)>=4 or (w[2][-1] in '.,?!' and len(cur)>=2) or nxt[3]!=w[3]
    if brk: chunks.append(cur); cur=[]
ev=[]
for i,c in enumerate(chunks):
    a=c[0][0]; b=c[-1][1]+0.25
    if i+1<len(chunks): b=min(max(b,c[-1][1]+0.05), chunks[i+1][0][0]) if chunks[i+1][0][0]-c[-1][1]<0.6 else b
    b=min(b,c[-1][3])
    parts=[]
    for w in c:
        t=w[2]
        if clean(t) in EMPH: parts.append('{\\fnInter ExtraBold}'+t+'{\\r}')
        else: parts.append(t)
    ev.append(('Cap',a,b,'{\\fad(60,60)}'+' '.join(parts)))
def rect(x0,y0,x1,y1): return f"m {x0} {y0} l {x1} {y0} l {x1} {y1} l {x0} {y1}"
for o in ovs:
    k,a,b=o[0],o[1],o[2]
    if k in ('title','chapter','env','card','end'):
        fo_=0 if k=='end' else 400
        ev.append(('Dim',a,b,'{\\fad(%d,%d)\\1a&HA6&\\p1}m 0 0 l 1080 0 l 1080 1920 l 0 1920{\\p0}'%(400,fo_)))
    if k=='title':
        ev.append(('Title',a,b,'{\\fad(600,500)\\pos(540,900)}'+o[3]))
        ev.append(('Kicker',a+0.4,b,'{\\fad(500,500)\\pos(540,1030)\\fs28\\fsp6}'+o[4].upper()))
    if k=='chapter':
        y=o[5] if len(o)>5 else 880
        ev.append(('Kicker',a,b,'{\\fad(300,300)\\pos(540,%d)}'%y+o[3].upper()))
        ev.append(('Chapter',a,b,'{\\fad(400,300)\\pos(540,%d)}'%(y+85)+o[4]))
    elif k=='env':
        ev.append(('Kicker',a,b,'{\\fad(300,300)\\pos(540,250)\\fs32}AMBIENTE'))
        ev.append(('Env',a,b,'{\\fad(300,300)\\pos(540,330)}'+o[3]))
    elif k=='chip':
        ev.append(('Chip',a,b,'{\\fad(200,200)\\an7\\pos(56,120)}'+o[3]))
    elif k=='pair':
        ev.append(('Chip',a,b,'{\\fad(200,200)\\an7\\pos(56,70)}PROJETO · IA'))
        ev.append(('Chip',a,b,'{\\fad(200,200)\\an7\\pos(56,1030)}REALIDADE'))
    elif k=='partner':
        ev.append(('PName',a,b,'{\\fad(300,300)\\move(100,1410,76,1410,0,300)}'+o[3]))
        ev.append(('PSub',a,b,'{\\fad(300,300)\\move(100,1500,76,1500,0,300)}'+o[4]))
    elif k=='note':
        ev.append(('Note',a,b,'{\\fad(300,300)\\pos(540,1180)}'+o[3]))
    elif k=='card':
        y=330
        for j,l in enumerate([x for x in o[3] if x]):
            ev.append(('Card',a+0.35*j,b,'{\\fad(500,400)\\pos(540,%d)}%s'%(y+j*92,l)))
    elif k=='end':
        ev.append(('Title',a,b,'{\\fad(600,0)\\pos(540,760)\\fs72}Angelinne Manualidades'))
        ev.append(('Kicker',a+0.4,b,'{\\fad(500,0)\\pos(540,900)}AGRADECIMENTOS'))
        ev.append(('CreditName',a+0.6,b,'{\\fad(500,0)\\pos(540,975)}MODELART'))
        ev.append(('CreditSub',a+0.6,b,'{\\fad(500,0)\\pos(540,1025)}corte a laser em papelão'))
        ev.append(('CreditName',a+0.9,b,'{\\fad(500,0)\\pos(540,1110)}STEIGLEDER TÊXTIL'))
        ev.append(('CreditSub',a+0.9,b,'{\\fad(500,0)\\pos(540,1160)}Decortela'))
        ev.append(('Kicker',a+1.2,b,'{\\fad(500,0)\\pos(540,1290)\\c&HFFFFFF&}IGREJA NAÇÕES'))
hdr="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter SemiBold,66,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,4,0,2,70,70,560,1
Style: Dim,Inter,20,&H00000000,&H00000000,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: Title,Inter ExtraBold,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,50,50,0,1
Style: Chapter,Inter ExtraBold,76,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,50,50,0,1
Style: Kicker,Inter SemiBold,36,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,8,0,1,0,0,5,40,40,0,1
Style: Env,Inter ExtraBold,68,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,40,40,0,1
Style: Card,Inter SemiBold,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,50,50,0,1
Style: Chip,Inter Bold,28,&H00000000,&H00000000,&H00FFFFFF,&H00FFFFFF,0,0,0,0,100,100,5,0,3,12,0,7,0,0,0,1
Style: PName,Inter ExtraBold,46,&H00000000,&H00000000,&H00FFFFFF,&H00FFFFFF,0,0,0,0,100,100,3,0,3,16,0,7,0,0,0,1
Style: PSub,Inter Medium,36,&H00000000,&H00000000,&H00FFFFFF,&H00FFFFFF,0,0,0,0,100,100,0,0,3,16,0,7,0,0,0,1
Style: Note,Inter SemiBold,44,&H00000000,&H00000000,&H00FFFFFF,&H00FFFFFF,0,0,0,0,100,100,0,0,3,16,0,5,40,40,0,1
Style: CreditName,Inter ExtraBold,40,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,4,0,1,0,0,5,0,0,0,1
Style: CreditSub,Inter Medium,36,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
order={'Dim':0}
with open(WK+'/overlay.ass','w') as f:
    f.write(hdr)
    for st,a,b,txt in sorted(ev,key=lambda e:e[1]):
        f.write(f"Dialogue: {order.get(st,1)},{ts(a)},{ts(b)},{st},,0,0,0,,{txt}\n")
print('events',len(ev),'captions',len(chunks),'total',T/FPS)
