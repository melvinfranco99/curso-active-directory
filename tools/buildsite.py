# -*- coding: utf-8 -*-
"""
Genera el sitio web estático del curso a partir de las lecciones (content/lXX.py).
- index.html: portada + temario por módulos.
- lessons/lXX.html: página de cada lección con vídeo + contenido detallado en HTML.
- Renderiza los diagramas a PNG para incrustarlos.
"""
import os, sys, html, subprocess, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.path.join(ROOT, "docs")
sys.path.insert(0, HERE)
import slidekit as sk

LESSON_IDS = ["l%02d" % i for i in range(1, 16)]

MODULES = [
    ("Módulo 1 · Fundamentos", "Qué es Active Directory y cómo funciona por dentro.", ["l01","l02","l03","l04"]),
    ("Módulo 2 · Administración", "Cómo se gestiona y se diseña de forma segura en una empresa.", ["l05","l06","l07"]),
    ("Módulo 3 · Hacking de AD", "La metodología y las técnicas reales de un atacante.", ["l08","l09","l10","l11","l12","l13"]),
    ("Módulo 4 · Defensa", "Hardening, detección y respuesta ante incidentes.", ["l14","l15"]),
]
ACCENT_HEX = {"cyan":"#38bdf8","green":"#34d399","red":"#f87171","amber":"#fbbf24","purple":"#a78bfa","blue":"#608ee6"}

def dur_str(path):
    try:
        r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                            "-of","csv=p=0", path], capture_output=True, text=True)
        s = float(r.stdout.strip()); m = int(s//60); sec = int(s%60)
        return "%d:%02d" % (m, sec)
    except Exception:
        return "—"

def esc(s): return html.escape(str(s))

# ---------------------------------------------------------------- CSS
CSS = """
:root{--bg:#0b1020;--bg2:#070a14;--panel:#121a2e;--panel2:#18233c;--stroke:#263352;
--text:#e5edf7;--muted:#9fb2cf;--faint:#6b7f9e;--cyan:#38bdf8;--green:#34d399;
--red:#f87171;--amber:#fbbf24;--purple:#a78bfa;--blue:#608ee6;--accent:var(--cyan);}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);
font-family:'Inter',-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;line-height:1.65;
background-image:radial-gradient(circle at 15% -10%,rgba(56,189,248,.08),transparent 40%),radial-gradient(circle at 90% 0,rgba(167,139,250,.07),transparent 35%);}
a{color:var(--cyan);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
header.nav{position:sticky;top:0;z-index:50;background:rgba(9,13,24,.82);
backdrop-filter:blur(12px);border-bottom:1px solid var(--stroke)}
.nav .wrap{display:flex;align-items:center;justify-content:space-between;height:62px}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;color:var(--text)}
.brand .dot{width:12px;height:12px;border-radius:3px;background:var(--cyan);box-shadow:0 0 12px var(--cyan)}
.nav a.navlink{color:var(--muted);font-size:14px;margin-left:22px;font-weight:600}
.nav a.navlink:hover{color:var(--text);text-decoration:none}
.hero{padding:80px 0 50px;position:relative}
.kicker{display:inline-block;font-size:13px;font-weight:800;letter-spacing:.12em;color:var(--cyan);
border:1px solid rgba(56,189,248,.4);background:rgba(56,189,248,.08);padding:7px 16px;border-radius:20px}
.hero h1{font-size:clamp(38px,6vw,68px);line-height:1.05;margin:22px 0 14px;font-weight:800;letter-spacing:-.02em}
.hero h1 .g{background:linear-gradient(120deg,var(--cyan),var(--purple));-webkit-background-clip:text;background-clip:text;color:transparent}
.hero p.lead{font-size:20px;color:var(--muted);max-width:760px}
.chips{display:flex;flex-wrap:wrap;gap:12px;margin-top:28px}
.chip{background:var(--panel);border:1px solid var(--stroke);border-radius:12px;padding:12px 16px;font-size:14px;color:var(--muted)}
.chip b{color:var(--text);font-size:19px;display:block}
.section-h{margin:60px 0 6px;font-size:14px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--faint)}
.module{margin:38px 0}
.module .mh{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;border-left:4px solid var(--accent);padding-left:16px;margin-bottom:18px}
.module .mh h2{font-size:26px;margin:0;font-weight:800}
.module .mh span{color:var(--muted);font-size:15px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px}
.card{display:block;background:linear-gradient(180deg,var(--panel),#0f1627);border:1px solid var(--stroke);
border-radius:16px;padding:20px;transition:.18s;position:relative;overflow:hidden}
.card:hover{border-color:var(--accent);transform:translateY(-3px);text-decoration:none;box-shadow:0 12px 30px rgba(0,0,0,.35)}
.card .num{font-size:13px;font-weight:800;color:var(--accent);letter-spacing:.08em}
.card h3{margin:8px 0 8px;font-size:19px;color:var(--text);font-weight:700;line-height:1.3}
.card p{margin:0;color:var(--muted);font-size:14px}
.card .meta{margin-top:16px;display:flex;align-items:center;gap:14px;color:var(--faint);font-size:13px;font-weight:600}
.card .play{position:absolute;top:18px;right:18px;width:34px;height:34px;border-radius:50%;
background:rgba(56,189,248,.12);border:1px solid var(--accent);display:flex;align-items:center;justify-content:center;color:var(--accent)}
footer{margin-top:70px;border-top:1px solid var(--stroke);padding:34px 0;color:var(--faint);font-size:14px}
.warn{background:rgba(251,191,36,.08);border:1px solid rgba(251,191,36,.4);border-radius:14px;padding:18px 20px;margin:34px 0;color:#f5deb3}
.warn b{color:var(--amber)}
/* ---- lesson page ---- */
.lesson-head{padding:40px 0 10px}
.breadcrumb{color:var(--faint);font-size:14px;margin-bottom:14px}
.lesson-head h1{font-size:clamp(28px,4.5vw,44px);margin:6px 0 10px;font-weight:800;letter-spacing:-.01em}
.tag{display:inline-block;font-size:12px;font-weight:800;letter-spacing:.1em;color:var(--accent);
border:1px solid var(--accent);background:rgba(255,255,255,.03);padding:5px 13px;border-radius:16px;text-transform:uppercase}
.videobox{background:#000;border:1px solid var(--stroke);border-radius:16px;overflow:hidden;margin:22px 0 10px;box-shadow:0 20px 50px rgba(0,0,0,.4)}
.videobox video{width:100%;display:block}
.vmeta{color:var(--faint);font-size:14px;margin-bottom:34px;display:flex;gap:18px;flex-wrap:wrap}
.content h2{font-size:24px;margin:40px 0 4px;font-weight:800;padding-left:16px;border-left:4px solid var(--accent)}
.content h2 .n{color:var(--faint);font-weight:700;margin-right:10px;font-size:18px}
.content p.exp{color:var(--muted);font-size:16.5px;margin:12px 0 4px}
ul.bl{list-style:none;padding:0;margin:14px 0}
ul.bl li{background:var(--panel);border:1px solid var(--stroke);border-left:3px solid var(--accent);
border-radius:10px;padding:13px 16px;margin:9px 0}
ul.bl li b{color:var(--text)}
ul.bl li span{color:var(--muted);display:block;margin-top:3px;font-size:15px}
table.t{width:100%;border-collapse:collapse;margin:16px 0;font-size:15px;background:var(--panel);
border-radius:12px;overflow:hidden;border:1px solid var(--stroke)}
table.t th{background:rgba(56,189,248,.12);color:var(--text);text-align:left;padding:12px 14px;font-weight:700;border-bottom:1px solid var(--stroke)}
table.t td{padding:11px 14px;border-bottom:1px solid var(--stroke);color:var(--muted);vertical-align:top}
table.t td:first-child{color:var(--text);font-weight:600}
table.t tr:last-child td{border-bottom:none}
pre.code{background:#060a14;border:1px solid var(--stroke);border-radius:12px;padding:18px 20px;
overflow-x:auto;font-family:'JetBrains Mono',ui-monospace,Menlo,monospace;font-size:14px;line-height:1.7;margin:16px 0}
pre.code .cmd{color:#fff}.pre .ps{color:var(--cyan)}
pre.code .cmd::before{content:"$ ";color:var(--green);font-weight:700}
pre.code .ps::before{content:"PS> ";color:var(--cyan);font-weight:700}
pre.code .cmt{color:var(--faint)}
pre.code .good{color:var(--green)}
pre.code .bad{color:var(--red)}
pre.code .hi{color:var(--amber)}
pre.code .out{color:var(--muted)}
.diagram-img{width:100%;border:1px solid var(--stroke);border-radius:14px;margin:18px 0;display:block}
blockquote.q{border-left:4px solid var(--accent);background:var(--panel);margin:24px 0;padding:18px 22px;
border-radius:0 12px 12px 0;font-size:18px;color:var(--text);font-style:italic}
blockquote.q cite{display:block;margin-top:10px;font-size:14px;color:var(--accent);font-style:normal}
.pager{display:flex;justify-content:space-between;gap:14px;margin:50px 0 10px}
.pager a{flex:1;background:var(--panel);border:1px solid var(--stroke);border-radius:12px;padding:16px 18px;color:var(--muted)}
.pager a:hover{border-color:var(--accent);text-decoration:none}
.pager a.next{text-align:right}
.pager a small{display:block;color:var(--faint);font-size:12px;text-transform:uppercase;letter-spacing:.08em}
.pager a b{color:var(--text);font-size:16px}
@media(max-width:640px){.hero{padding:50px 0 30px}.grid{grid-template-columns:1fr}.pager{flex-direction:column}}
"""

def nav_html(depth):
    base = "../" if depth else ""
    return f"""<header class="nav"><div class="wrap">
<a class="brand" href="{base}index.html"><span class="dot"></span>AD · Hacking &amp; Defensa</a>
<nav><a class="navlink" href="{base}index.html#temario">Temario</a>
<a class="navlink" href="{base}index.html#modulos">Módulos</a>
<a class="navlink" href="https://github.com" id="ghlink">GitHub</a></nav></div></header>"""

def page(title, body, depth=0, desc=""):
    base = "../" if depth else ""
    return f"""<!doctype html><html lang="es"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/style.css">
</head><body>{nav_html(depth)}{body}
<footer><div class="wrap">Curso <b>Active Directory · Hacking &amp; Defensa</b> — material educativo.
Las técnicas ofensivas se muestran con fines didácticos y de defensa; úsalas solo en entornos propios o con autorización por escrito.
<br>Generado automáticamente · {len(LESSON_IDS)} lecciones en vídeo.</div></footer>
</body></html>"""

def render_bullets_html(s):
    out = ['<ul class="bl">']
    for it in s.get("items", []):
        if isinstance(it, dict):
            out.append(f"<li><b>{esc(it.get('h',''))}</b>" + (f"<span>{esc(it.get('b',''))}</span>" if it.get('b') else "") + "</li>")
        else:
            out.append(f"<li><b>{esc(it)}</b></li>")
    out.append("</ul>")
    return "".join(out)

def render_table_html(s):
    out = ['<table class="t"><thead><tr>']
    for h in s["headers"]:
        out.append(f"<th>{esc(h)}</th>")
    out.append("</tr></thead><tbody>")
    for row in s["rows"]:
        out.append("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in row) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)

def render_code_html(s):
    out = ['<pre class="code">']
    for ln in s["code"]:
        if isinstance(ln, dict):
            k = ln.get("k","out"); t = esc(ln.get("t",""))
        else:
            k = "out"; t = esc(ln)
        out.append(f'<span class="{k}">{t}</span>\n')
    out.append("</pre>")
    return "".join(out)

def render_compare_html(s):
    out = ['<div class="grid" style="grid-template-columns:1fr 1fr">']
    for c in s["cols"]:
        hexc = ACCENT_HEX.get(c.get("color","cyan"),"#38bdf8")
        out.append(f'<div class="card" style="--accent:{hexc}"><h3 style="color:{hexc}">{esc(c["title"])}</h3><ul class="bl" style="margin-top:6px">')
        for it in c["items"]:
            if isinstance(it, dict):
                out.append(f"<li><b>{esc(it.get('h',''))}</b>" + (f"<span>{esc(it.get('b',''))}</span>" if it.get('b') else "") + "</li>")
            else:
                out.append(f"<li><b>{esc(it)}</b></li>")
        out.append("</ul></div>")
    out.append("</div>")
    return "".join(out)

def render_stat_html(s):
    out = ['<div class="grid">']
    for c in s["cards"]:
        hexc = ACCENT_HEX.get(c.get("color","cyan"),"#38bdf8")
        big = f'<div style="font-size:34px;font-weight:800;color:{hexc}">{esc(c["big"])}</div>' if c.get("big") else ""
        out.append(f'<div class="card" style="--accent:{hexc}">{big}<h3>{esc(c.get("h",""))}</h3><p>{esc(c.get("b",""))}</p></div>')
    out.append("</div>")
    return "".join(out)

def build_lesson_page(lid, lesson, prev_l, next_l, accent_hex):
    mp4 = f"../videos/{lid}.mp4"
    srt = f"../videos/{lid}.srt"
    video_path = os.path.join(SITE, "videos", f"{lid}.mp4")
    dur = dur_str(video_path)
    body = [f'<main class="wrap"><div class="lesson-head">',
            f'<div class="breadcrumb"><a href="../index.html">Inicio</a> › {esc(lesson["module"])}</div>',
            f'<span class="tag">{esc(lesson["module"])}</span>',
            f'<h1>{esc(lesson["title"])}</h1></div>']
    # video
    poster = f"../assets/{lid}_poster.png"
    body.append(f'<div class="videobox"><video controls preload="metadata" poster="{poster}">'
                f'<source src="{mp4}" type="video/mp4">'
                f'<track kind="subtitles" srclang="es" label="Español" src="{srt}" default>'
                f'Tu navegador no soporta vídeo HTML5. <a href="{mp4}">Descarga el vídeo</a>.</video></div>')
    body.append(f'<div class="vmeta"><span>▶ Duración {dur}</span><span>🎧 Narración en español</span><span>📝 Subtítulos incluidos</span></div>')
    body.append('<div class="content">')
    # secciones a partir de slides de contenido
    n = 0
    diagram_counter = 0
    for s in lesson["slides"]:
        t = s["type"]
        if t in ("cover","section"):
            continue
        narr = s.get("narration","").strip()
        if t == "quote":
            body.append(f'<blockquote class="q">“{esc(s["text"])}”' + (f'<cite>{esc(s.get("by",""))}</cite>' if s.get("by") else "") + "</blockquote>")
            if narr: body.append(f'<p class="exp">{esc(narr)}</p>')
            continue
        n += 1
        title = s.get("title","")
        body.append(f'<h2><span class="n">{n:02d}</span>{esc(title)}</h2>')
        if s.get("lead"):
            body.append(f'<p class="exp"><em>{esc(s["lead"])}</em></p>')
        if narr:
            body.append(f'<p class="exp">{esc(narr)}</p>')
        if t == "bullets":
            body.append(render_bullets_html(s))
        elif t == "table":
            body.append(render_table_html(s))
        elif t == "code":
            body.append(render_code_html(s))
        elif t == "compare":
            body.append(render_compare_html(s))
        elif t == "stat":
            body.append(render_stat_html(s))
        elif t == "diagram":
            img = f"../assets/{lid}_dia{diagram_counter}.png"
            body.append(f'<img class="diagram-img" src="{img}" alt="{esc(title)}">')
            diagram_counter += 1
    body.append("</div>")
    # pager
    body.append('<div class="pager">')
    if prev_l:
        body.append(f'<a class="prev" href="{prev_l[0]}.html"><small>Anterior</small><b>← {esc(prev_l[1])}</b></a>')
    else:
        body.append('<a class="prev" href="../index.html"><small>Volver</small><b>← Inicio del curso</b></a>')
    if next_l:
        body.append(f'<a class="next" href="{next_l[0]}.html"><small>Siguiente</small><b>{esc(next_l[1])} →</b></a>')
    else:
        body.append('<a class="next" href="../index.html"><small>Fin</small><b>Volver al temario →</b></a>')
    body.append("</div></main>")
    style = f'<style>:root{{--accent:{accent_hex}}}</style>'
    return page(f"{lesson['title']} · Curso AD", style + "".join(body), depth=1, desc=lesson["title"])

def build():
    os.makedirs(os.path.join(SITE,"assets"), exist_ok=True)
    os.makedirs(os.path.join(SITE,"lessons"), exist_ok=True)
    with open(os.path.join(SITE,"assets","style.css"),"w") as f:
        f.write(CSS)
    lessons = {}
    titles = {}
    for lid in LESSON_IDS:
        mod = importlib.import_module(f"content.{lid}")
        lessons[lid] = mod.LESSON
        titles[lid] = mod.LESSON["title"]

    # render diagrams + posters
    for lid, lesson in lessons.items():
        accent = lesson.get("accent","cyan")
        dia_i = 0
        first_content = None
        for s in lesson["slides"]:
            if s["type"] == "diagram":
                s2 = dict(s); s2.setdefault("module", lesson["module"]); s2["idx"]=0; s2["total"]=0
                img = sk.render_slide(s2)
                img.save(os.path.join(SITE,"assets", f"{lid}_dia{dia_i}.png"))
                dia_i += 1
            if s["type"] == "cover" and first_content is None:
                first_content = sk.render_slide(s)
        # poster = cover slide
        if first_content is not None:
            first_content.save(os.path.join(SITE,"assets", f"{lid}_poster.png"))

    # lesson pages
    for i, lid in enumerate(LESSON_IDS):
        lesson = lessons[lid]
        prev_l = (LESSON_IDS[i-1], titles[LESSON_IDS[i-1]]) if i>0 else None
        next_l = (LESSON_IDS[i+1], titles[LESSON_IDS[i+1]]) if i<len(LESSON_IDS)-1 else None
        accent_hex = ACCENT_HEX.get(lesson.get("accent","cyan"),"#38bdf8")
        htmlp = build_lesson_page(lid, lesson, prev_l, next_l, accent_hex)
        with open(os.path.join(SITE,"lessons", f"{lid}.html"),"w") as f:
            f.write(htmlp)

    # index
    total_min = 0
    for lid in LESSON_IDS:
        p = os.path.join(SITE,"videos",f"{lid}.mp4")
        if os.path.exists(p):
            r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],capture_output=True,text=True)
            try: total_min += float(r.stdout.strip())/60
            except: pass
    body = ['<main class="wrap">']
    body.append(f"""<section class="hero">
<span class="kicker">CURSO PROFESIONAL · 2026</span>
<h1>Active Directory<br><span class="g">Hacking &amp; Defensa</span></h1>
<p class="lead">De los fundamentos al dominio completo. Aprende cómo funciona Active Directory,
cómo lo atacan los adversarios paso a paso y cómo protegerlo, con <b>{len(LESSON_IDS)} lecciones en vídeo</b>
narradas, diagramas, tablas y ejemplos de comandos reales.</p>
<div class="chips">
<div class="chip"><b>{len(LESSON_IDS)}</b> lecciones en vídeo</div>
<div class="chip"><b>~{int(round(total_min))} min</b> de contenido narrado</div>
<div class="chip"><b>4</b> módulos: fundamentos → defensa</div>
<div class="chip"><b>Español</b> · subtítulos incluidos</div>
</div>
</section>""")
    body.append("""<div class="warn"><b>Aviso ético y legal.</b> Este curso incluye técnicas ofensivas con fines
estrictamente educativos y defensivos. Practícalas únicamente en laboratorios de tu propiedad o con
autorización explícita por escrito. El uso no autorizado contra sistemas ajenos es ilegal.</div>""")
    body.append('<h2 class="section-h" id="temario">Temario completo</h2>')
    body.append('<div id="modulos">')
    mod_accents = ["#38bdf8","#608ee6","#f87171","#34d399"]
    for mi,(mname, mdesc, ids) in enumerate(MODULES):
        acc = mod_accents[mi]
        body.append(f'<div class="module" style="--accent:{acc}"><div class="mh"><h2>{esc(mname)}</h2><span>{esc(mdesc)}</span></div><div class="grid">')
        for lid in ids:
            lesson = lessons[lid]
            acc2 = ACCENT_HEX.get(lesson.get("accent","cyan"),"#38bdf8")
            p = os.path.join(SITE,"videos",f"{lid}.mp4")
            d = dur_str(p) if os.path.exists(p) else "—"
            num = lesson["id"]
            # breve descripción = lead de la primera slide de contenido o subtitle de cover
            desc = ""
            for s in lesson["slides"]:
                if s["type"]=="cover": desc = s.get("subtitle","")
            body.append(f"""<a class="card" style="--accent:{acc2}" href="lessons/{lid}.html">
<span class="play">▶</span>
<div class="num">LECCIÓN {esc(num)}</div>
<h3>{esc(lesson["title"])}</h3>
<p>{esc(desc)}</p>
<div class="meta"><span>▶ {d}</span><span>· vídeo + guía escrita</span></div></a>""")
        body.append('</div></div>')
    body.append('</div></main>')
    with open(os.path.join(SITE,"index.html"),"w") as f:
        f.write(page("Curso Active Directory · Hacking & Defensa", "".join(body),
                     depth=0, desc="Curso profesional de Active Directory: fundamentos, hacking y defensa, con 15 lecciones en vídeo."))
    print("Sitio generado en", SITE)

if __name__ == "__main__":
    build()
