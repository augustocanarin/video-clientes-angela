import sys, json, os, subprocess, numpy as np
def load(p):
    raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True,check=True).stdout
    return np.frombuffer(raw,np.float32)
from faster_whisper import WhisperModel
m = WhisperModel('medium', device='cpu', compute_type='int8', cpu_threads=4)
for path in sys.argv[1:]:
    base = os.path.splitext(os.path.basename(path))[0]
    out = f'/home/user/media/work/transcripts/{base}.json'
    if os.path.exists(out): continue
    segs, info = m.transcribe(load(path), language='pt', word_timestamps=True, vad_filter=False, beam_size=5)
    data = []
    for s in segs:
        data.append({'start': s.start, 'end': s.end, 'text': s.text.strip(),
                     'words': [{'s': w.start, 'e': w.end, 'w': w.word} for w in (s.words or [])]})
    json.dump({'duration': info.duration, 'segments': data}, open(out, 'w'), ensure_ascii=False, indent=1)
    with open(out.replace('.json', '.txt'), 'w') as f:
        for d in data: f.write(f"[{d['start']:7.2f}-{d['end']:7.2f}] {d['text']}\n")
    print('done', base, info.duration, flush=True)
