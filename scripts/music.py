import numpy as np, wave
SR=44100
def midi(n): return 440*2**((n-69)/12)
N={'C':60,'D':62,'E':64,'F':65,'G':67,'A':69,'B':71}
def p(s):
    o=12*s.count("'"); return N[s[0]]+o-(12 if s.endswith(',') else 0)
mel="G 1.5,A .5,G 1,E 3|G 1.5,A .5,G 1,E 3|D' 2,D' 1,B 3|C' 2,C' 1,G 3|A 2,A 1,C' 1.5,B .5,A 1|G 1.5,A .5,G 1,E 3|A 2,A 1,C' 1.5,B .5,A 1|G 1.5,A .5,G 1,E 3|D' 2,D' 1,F' 1.5,D' .5,B 1|C' 3,E' 3|C' 1.5,G .5,E 1,G 1.5,F .5,D 1|C 6"
chords=[[48,55,64],[48,55,64],[43,53,59],[48,55,64],[41,57,65],[48,55,64],[41,57,65],[48,55,64],[43,53,59],[48,55,64],[48,55,64],[48,55,64]]
E8=0.36; BAR=6*E8
def bell(f,dur,amp):
    t=np.arange(int(SR*dur))/SR
    s=(np.sin(2*np.pi*f*t)*np.exp(-t*2.2)+0.35*np.sin(2*np.pi*f*2.0*t)*np.exp(-t*4)+0.15*np.sin(2*np.pi*f*3.01*t)*np.exp(-t*6)+0.06*np.sin(2*np.pi*f*4.2*t)*np.exp(-t*9))
    s*=np.minimum(1,t/0.004); return amp*s
def pad(fs,dur,amp):
    t=np.arange(int(SR*dur))/SR; s=np.zeros_like(t)
    for f in fs:
        for d in (-0.15,0.15): s+=np.sin(2*np.pi*(f*(1+d/100))*t)+0.2*np.sin(2*np.pi*2*f*t)
    env=np.minimum(1,t/0.6)*np.minimum(1,(dur-t)/0.6)
    return amp*s*env/len(fs)
def verse(octave, withmel, arp):
    total=int(SR*BAR*12)+SR*4; out=np.zeros(total)
    bars=mel.split('|')
    for b,bar in enumerate(bars):
        t0=b*BAR
        seg=pad([midi(n) for n in chords[b]],BAR+0.5,0.09); i=int(t0*SR); out[i:i+len(seg)]+=seg
        if arp:
            tones=chords[b]+[chords[b][1]+12]
            for k in range(6):
                f=midi(tones[[0,1,2,3,2,1][k]]+12); s=bell(f,2.5,0.05); j=int((t0+k*E8)*SR); out[j:j+len(s)]+=s
        if withmel:
            t=t0
            for nd in bar.split(','):
                n,d=nd.split(); s=bell(midi(p(n)+octave),3.0,0.22); j=int(t*SR); out[j:j+len(s)]+=s; t+=float(d)*E8
    return out[:int(SR*BAR*12)], out[int(SR*BAR*12):]
parts=[]; tail=np.zeros(SR*4)
plan=[(0,False,True),(12,True,True),(12,True,False),(0,False,True),(24,True,True),(12,True,True)]*2
for o,m,a in plan:
    body,t=verse(o,m,a); body[:len(tail)]+=tail; parts.append(body); tail=t
x=np.concatenate(parts+[tail])
x/=np.max(np.abs(x))*1.12
st=np.stack([x,x],1)
w=wave.open('/home/user/media/work/audio/music_dry.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((st*32767).astype(np.int16).tobytes()); w.close()
print(len(x)/SR)
