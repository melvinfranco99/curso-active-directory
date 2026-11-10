# -*- coding: utf-8 -*-
"""
Ensambla un vídeo narrado a partir de una lección (lista de slides con narración).
- Renderiza cada slide a PNG (slidekit).
- Genera narración por slide con edge-tts (voz es-ES).
- Mide duración, sincroniza imagen+audio y codifica con ffmpeg (x264 ligero).
"""
import os, sys, subprocess, json, hashlib, shutil, re

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import slidekit as sk

SCRATCH = "/tmp/claude-1000/-home-melvin-Documentos-melvin-proyectos-claude-62-curso-active-directory-ciberseguridad/2af63142-a2c0-4f44-81bd-0a75caea61f1/scratchpad"
EDGE_TTS = os.path.join(SCRATCH, "venv", "bin", "edge-tts")
VOICE = "es-ES-AlvaroNeural"
RATE = "+6%"
PAD_START = 0.45
PAD_END = 0.75
GAP = 0.35          # silencio extra entre slides
FPS = 12
CRF = "30"

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        sys.stderr.write("CMD FAIL: %s\n%s\n" % (" ".join(cmd), r.stderr[-1500:]))
        raise RuntimeError("cmd failed")
    return r

def duration(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", path])
    return float(r.stdout.strip())

def tts(text, out_mp3, cache_dir):
    text = re.sub(r"\s+", " ", text).strip()
    key = hashlib.md5((VOICE + RATE + text).encode()).hexdigest()
    cached = os.path.join(cache_dir, key + ".mp3")
    if os.path.exists(cached) and os.path.getsize(cached) > 500:
        shutil.copy(cached, out_mp3)
        return
    tf = out_mp3 + ".txt"
    with open(tf, "w") as f:
        f.write(text)
    # reintentos: el servicio online a veces falla
    last = None
    for attempt in range(4):
        try:
            run([EDGE_TTS, "-f", tf, "-v", VOICE, "--rate", RATE,
                 "--write-media", out_mp3])
            if os.path.getsize(out_mp3) > 500:
                shutil.copy(out_mp3, cached)
                os.remove(tf)
                return
        except Exception as e:
            last = e
            subprocess.run(["sleep", str(1 + attempt)])
    raise RuntimeError("TTS falló tras reintentos: %s" % last)

def build_lesson(lesson, out_path, workdir):
    os.makedirs(workdir, exist_ok=True)
    cache_dir = os.path.join(os.path.dirname(workdir), "_tts_cache")
    os.makedirs(cache_dir, exist_ok=True)
    slides = lesson["slides"]
    total = len([s for s in slides if s["type"] not in ("cover", "section", "quote")])
    # inyecta metadatos comunes (módulo, idx, total)
    idx = 0
    seg_wavs, img_durs, img_paths = [], [], []
    srt_entries = []
    t_cursor = 0.0
    for i, s in enumerate(slides):
        s = dict(s)
        if s["type"] not in ("cover", "section", "quote"):
            idx += 1
            s.setdefault("module", lesson.get("module", ""))
            s["idx"] = idx
            s["total"] = total
        else:
            s.setdefault("module", lesson.get("module", ""))
        # render
        img = sk.render_slide(s)
        ip = os.path.join(workdir, "slide_%03d.png" % i)
        img.save(ip)
        img_paths.append(ip)
        # narración
        narr = s.get("narration", "").strip()
        seg = os.path.join(workdir, "seg_%03d.mp3" % i)
        if narr:
            tts(narr, seg, cache_dir)
            adur = duration(seg)
        else:
            adur = 2.0
        slide_dur = PAD_START + adur + PAD_END + GAP
        # audio padded exacto a slide_dur
        wav = os.path.join(workdir, "pad_%03d.wav" % i)
        if narr:
            run(["ffmpeg", "-y", "-i", seg, "-af",
                 "adelay=%d|%d,apad" % (int(PAD_START*1000), int(PAD_START*1000)),
                 "-t", "%.3f" % slide_dur, "-ar", "44100", "-ac", "2", wav])
        else:
            run(["ffmpeg", "-y", "-f", "lavfi", "-i",
                 "anullsrc=r=44100:cl=stereo", "-t", "%.3f" % slide_dur, wav])
        seg_wavs.append(wav)
        img_durs.append(slide_dur)
        # subtítulo
        if narr:
            srt_entries.append((t_cursor + PAD_START, t_cursor + PAD_START + adur, narr))
        t_cursor += slide_dur

    # concat audio
    alist = os.path.join(workdir, "audio.txt")
    with open(alist, "w") as f:
        for w in seg_wavs:
            f.write("file '%s'\n" % w)
    full_audio = os.path.join(workdir, "full.wav")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", alist,
         "-c", "copy", full_audio])
    audio_dur = duration(full_audio)

    # concat imágenes (demuxer con duraciones)
    vlist = os.path.join(workdir, "video.txt")
    with open(vlist, "w") as f:
        for ip, dur in zip(img_paths, img_durs):
            f.write("file '%s'\n" % ip)
            f.write("duration %.3f\n" % dur)
        f.write("file '%s'\n" % img_paths[-1])  # requerido por concat

    # codifica
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", vlist,
         "-i", full_audio,
         "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
         "-r", str(FPS), "-crf", CRF, "-preset", "medium",
         "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart",
         "-t", "%.3f" % audio_dur, out_path])

    # genera SRT
    srt_path = os.path.splitext(out_path)[0] + ".srt"
    _write_srt(srt_entries, srt_path)
    total_dur = duration(out_path)
    return total_dur, srt_path

def _fmt_ts(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
    return "%02d:%02d:%06.3f" % (h, m, s).replace(".", ",") if False else \
           "%02d:%02d:%02d,%03d" % (h, m, int(s), int((s - int(s)) * 1000))

def _write_srt(entries, path):
    with open(path, "w") as f:
        for i, (a, b, txt) in enumerate(entries, 1):
            txt = re.sub(r"\s+", " ", txt).strip()
            # trocear en líneas de ~80 chars
            f.write("%d\n%s --> %s\n%s\n\n" % (i, _fmt_ts(a), _fmt_ts(b), _wraptxt(txt)))

def _wraptxt(txt, width=74):
    import textwrap
    return "\n".join(textwrap.wrap(txt, width)[:3])

if __name__ == "__main__":
    import importlib
    name = sys.argv[1]            # p.ej. l01
    out = sys.argv[2]
    mod = importlib.import_module("content.%s" % name)
    wd = os.path.join(SCRATCH, "build", name)
    dur, srt = build_lesson(mod.LESSON, out, wd)
    print("OK %s  dur=%.1fs (%.1f min)  -> %s" % (name, dur, dur/60, out))
