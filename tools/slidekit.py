# -*- coding: utf-8 -*-
"""
SlideKit: motor de renderizado de slides 1280x720 para el curso de Active Directory.
Tema oscuro profesional de ciberseguridad. Sólo usa PIL.
"""
import os, math, textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720

# ----------------------------------------------------------------------------
# Paleta
# ----------------------------------------------------------------------------
BG        = (11, 16, 32)       # fondo navy profundo
BG2       = (9, 13, 26)
PANEL     = (20, 28, 48)
PANEL_HI  = (27, 37, 62)
STROKE    = (44, 58, 92)
GRID      = (24, 33, 55)
TEXT      = (229, 237, 247)
MUTED     = (143, 162, 196)
FAINT     = (104, 122, 156)
CYAN      = (56, 189, 248)
BLUE      = (96, 142, 230)
GREEN     = (52, 211, 153)
RED       = (248, 113, 113)
AMBER     = (251, 191, 36)
PURPLE    = (167, 139, 250)
WHITE     = (245, 250, 255)

ACCENTS = {"cyan": CYAN, "green": GREEN, "red": RED, "amber": AMBER,
           "purple": PURPLE, "blue": BLUE}

# ----------------------------------------------------------------------------
# Fuentes
# ----------------------------------------------------------------------------
FT_SANS  = "/usr/share/fonts/liberation/LiberationSans-Regular.ttf"
FT_BOLD  = "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"
FT_ITAL  = "/usr/share/fonts/liberation/LiberationSans-Italic.ttf"
FT_MONO  = "/usr/share/fonts/TTF/JetBrainsMono-Regular.ttf"
FT_MONOB = "/usr/share/fonts/TTF/JetBrainsMono-Bold.ttf"

_fcache = {}
def font(kind="sans", size=28):
    path = {"sans": FT_SANS, "bold": FT_BOLD, "ital": FT_ITAL,
            "mono": FT_MONO, "monob": FT_MONOB}[kind]
    key = (path, size)
    if key not in _fcache:
        _fcache[key] = ImageFont.truetype(path, size)
    return _fcache[key]

# ----------------------------------------------------------------------------
# Helpers de dibujo
# ----------------------------------------------------------------------------
def _d(img):
    return ImageDraw.Draw(img, "RGBA")

def text_w(draw, s, f):
    return draw.textlength(s, font=f)

def text_h(f):
    a = f.getmetrics()
    return a[0] + a[1]

def wrap(draw, s, f, maxw):
    """Ajuste de línea por ancho en píxeles."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(draw, t, f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

def rrect(draw, box, r, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def vgrad(img, box, c1, c2):
    x0, y0, x1, y1 = box
    h = max(1, y1 - y0)
    base = Image.new("RGB", (1, h))
    for i in range(h):
        t = i / (h - 1) if h > 1 else 0
        base.putpixel((0, i), tuple(int(c1[k] + (c2[k] - c1[k]) * t) for k in range(3)))
    base = base.resize((x1 - x0, h))
    img.paste(base, (x0, y0))

def arrow(draw, p1, p2, color=CYAN, width=3, head=12, dashed=False):
    x1, y1 = p1; x2, y2 = p2
    ang = math.atan2(y2 - y1, x2 - x1)
    # acortar para la punta
    xe = x2 - head * 0.9 * math.cos(ang)
    ye = y2 - head * 0.9 * math.sin(ang)
    if dashed:
        _dash_line(draw, (x1, y1), (xe, ye), color, width)
    else:
        draw.line([(x1, y1), (xe, ye)], fill=color, width=width)
    left  = (x2 - head * math.cos(ang - 0.5), y2 - head * math.sin(ang - 0.5))
    right = (x2 - head * math.cos(ang + 0.5), y2 - head * math.sin(ang + 0.5))
    draw.polygon([ (x2, y2), left, right ], fill=color)

def _dash_line(draw, p1, p2, color, width, dash=10, gap=7):
    x1, y1 = p1; x2, y2 = p2
    total = math.hypot(x2 - x1, y2 - y1)
    if total == 0: return
    dx, dy = (x2 - x1) / total, (y2 - y1) / total
    n = int(total // (dash + gap)) + 1
    for i in range(n):
        s = i * (dash + gap)
        e = min(s + dash, total)
        draw.line([(x1 + dx * s, y1 + dy * s), (x1 + dx * e, y1 + dy * e)], fill=color, width=width)

def _lerp(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

# ----------------------------------------------------------------------------
# Lienzo base: fondo + cabecera + pie
# ----------------------------------------------------------------------------
def base_canvas(module="", title="", idx=0, total=0, accent="cyan", chrome=True):
    img = Image.new("RGB", (W, H), BG)
    vgrad(img, (0, 0, W, H), (13, 19, 38), (8, 11, 22))
    d = _d(img)
    # grid de puntos sutil
    for y in range(40, H, 34):
        for x in range(40, W, 34):
            d.point((x, y), fill=GRID)
    ac = ACCENTS.get(accent, CYAN)
    if chrome:
        # barra superior de acento
        d.rectangle((0, 0, W, 6), fill=ac)
        # cabecera
        if module:
            mf = font("bold", 20)
            tw = text_w(d, module.upper(), mf)
            rrect(d, (60, 36, 60 + tw + 36, 36 + 36), 18, fill=(ac[0], ac[1], ac[2], 38), outline=(ac[0], ac[1], ac[2], 120), width=1)
            d.text((78, 44), module.upper(), font=mf, fill=ac)
        if title:
            tf = font("bold", 40)
            d.text((60, 86), title, font=tf, fill=TEXT)
            d.line((60, 140, W - 60, 140), fill=STROKE, width=2)
        # pie
        pf = font("sans", 18)
        d.line((60, H - 44, W - 60, H - 44), fill=STROKE, width=1)
        d.text((60, H - 34), "Curso Active Directory · Hacking & Defensa", font=pf, fill=FAINT)
        if total:
            s = f"{idx:02d} / {total:02d}"
            d.text((W - 60 - text_w(d, s, pf), H - 34), s, font=pf, fill=FAINT)
            # progreso
            pw = (W - 120)
            prog = pw * (idx / total)
            d.rectangle((60, H - 50, 60 + pw, H - 49), fill=STROKE)
            d.rectangle((60, H - 50, 60 + prog, H - 49), fill=ac)
    return img, d, ac

CONTENT_TOP = 168
CONTENT_BOT = H - 70
CONTENT_L = 60
CONTENT_R = W - 60

# ----------------------------------------------------------------------------
# Tipos de slide
# ----------------------------------------------------------------------------
def render_cover(s):
    img = Image.new("RGB", (W, H), BG)
    vgrad(img, (0, 0, W, H), (16, 23, 46), (7, 10, 20))
    d = _d(img)
    ac = ACCENTS.get(s.get("accent", "cyan"), CYAN)
    # glow radial decorativo
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = _d(glow)
    gd.ellipse((W - 560, -220, W + 240, 420), fill=(ac[0], ac[1], ac[2], 26))
    gd.ellipse((-260, H - 360, 360, H + 160), fill=(56, 189, 248, 20))
    img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
    d = _d(img)
    for y in range(40, H, 34):
        for x in range(40, W, 34):
            d.point((x, y), fill=(22, 30, 52))
    # nodos decorativos (mini red AD)
    _deco_network(d, ac)
    # etiqueta
    lab = s.get("kicker", "CURSO PROFESIONAL")
    lf = font("bold", 22)
    rrect(d, (80, 150, 80 + text_w(d, lab, lf) + 40, 196), 20,
          fill=(ac[0], ac[1], ac[2], 40), outline=(ac[0], ac[1], ac[2], 150), width=1)
    d.text((100, 158), lab, font=lf, fill=ac)
    # título grande
    tf = font("bold", 74)
    y = 240
    for ln in s.get("title_lines", ["Active Directory"]):
        d.text((80, y), ln, font=tf, fill=WHITE)
        y += 82
    # subtítulo
    sf = font("sans", 30)
    y += 6
    for ln in wrap(d, s.get("subtitle", ""), sf, 940):
        d.text((82, y), ln, font=sf, fill=MUTED)
        y += 40
    # footer
    ff = font("bold", 22)
    d.text((80, H - 90), s.get("footer", ""), font=ff, fill=ac)
    ff2 = font("sans", 20)
    d.text((80, H - 58), s.get("footer2", ""), font=ff2, fill=FAINT)
    return img

def _deco_network(d, ac):
    import random
    random.seed(7)
    pts = [(980, 250), (1090, 360), (900, 430), (1140, 210), (1010, 470), (1180, 440)]
    for a in range(len(pts)):
        for b in range(a + 1, len(pts)):
            if random.random() < 0.5:
                d.line([pts[a], pts[b]], fill=(ac[0], ac[1], ac[2], 50), width=1)
    for (x, y) in pts:
        r = random.randint(5, 10)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(ac[0], ac[1], ac[2], 160))
        d.ellipse((x - r - 4, y - r - 4, x + r + 4, y + r + 4), outline=(ac[0], ac[1], ac[2], 70), width=1)

def render_section(s):
    img, d, ac = base_canvas(accent=s.get("accent", "cyan"), chrome=False)
    vgrad(img, (0, 0, W, H), (14, 20, 42), (7, 10, 20))
    d = _d(img)
    for y in range(40, H, 34):
        for x in range(40, W, 34):
            d.point((x, y), fill=(22, 30, 52))
    num = s.get("num", "")
    nf = font("bold", 190)
    d.text((70, 96), num, font=nf, fill=(ac[0], ac[1], ac[2], 38))
    kf = font("bold", 24)
    d.text((92, 324), s.get("kicker", "MÓDULO").upper(), font=kf, fill=ac)
    tf = font("bold", 58)
    y = 362
    for ln in s.get("title_lines", [s.get("title", "")]):
        d.text((90, y), ln, font=tf, fill=WHITE)
        y += 70
    if s.get("subtitle"):
        sf = font("sans", 28)
        y += 8
        for ln in wrap(d, s["subtitle"], sf, 1000):
            d.text((92, y), ln, font=sf, fill=MUTED)
            y += 38
    d.rectangle((90, 320, 94, 320 + 0), fill=ac)
    d.line((90, 310, 90, y - 6 if s.get("subtitle") else 410), fill=ac, width=4)
    return img

def render_bullets(s):
    img, d, ac = base_canvas(s.get("module", ""), s.get("title", ""),
                             s.get("idx", 0), s.get("total", 0), s.get("accent", "cyan"))
    items = s.get("items", [])
    x = CONTENT_L + 6
    maxw = CONTENT_R - x - 20
    if s.get("lead"):
        lf = font("ital", 26)
        yy = CONTENT_TOP
        for ln in wrap(d, s["lead"], lf, maxw):
            d.text((x, yy), ln, font=lf, fill=MUTED); yy += 36
        y = yy + 14
    else:
        y = CONTENT_TOP + 6
    bf = font("sans", 27)
    bbf = font("bold", 27)
    avail = CONTENT_BOT - y
    gap = min(96, max(54, int(avail / max(1, len(items)))))
    for it in items:
        if isinstance(it, str):
            head, body = it, None
        else:
            head, body = it.get("h"), it.get("b")
        cy = y + 14
        # marcador
        d.ellipse((x, cy - 9, x + 18, cy + 9), outline=ac, width=3)
        d.ellipse((x + 5, cy - 4, x + 13, cy + 4), fill=ac)
        tx = x + 36
        hl = wrap(d, head, bbf, maxw - 40)
        yy = y
        for i, ln in enumerate(hl):
            d.text((tx, yy), ln, font=bbf, fill=TEXT); yy += 34
        if body:
            for ln in wrap(d, body, bf, maxw - 40):
                d.text((tx, yy), ln, font=bf, fill=MUTED); yy += 32
        y += gap if not body else max(gap, yy - y + 12)
    return img

def render_table(s):
    img, d, ac = base_canvas(s.get("module", ""), s.get("title", ""),
                             s.get("idx", 0), s.get("total", 0), s.get("accent", "cyan"))
    rows = s["rows"]; headers = s["headers"]
    ncol = len(headers)
    weights = s.get("weights", [1] * ncol)
    tot = sum(weights)
    x0 = CONTENT_L; x1 = CONTENT_R
    tw = x1 - x0
    xs = [x0]
    for w in weights:
        xs.append(xs[-1] + tw * w / tot)
    y = CONTENT_TOP + (30 if s.get("lead") else 0)
    if s.get("lead"):
        lf = font("ital", 24)
        d.text((x0, CONTENT_TOP - 6), s["lead"], font=lf, fill=MUTED)
    hf = font("bold", 23)
    cf = font("sans", 22)
    cfm = font("mono", 20)
    rowh = s.get("rowh", 0)
    avail = CONTENT_BOT - y - 54
    if not rowh:
        rowh = min(70, max(40, int(avail / max(1, len(rows)))))
    # cabecera
    rrect(d, (x0, y, x1, y + 48), 10, fill=(ac[0], ac[1], ac[2], 45), outline=(ac[0], ac[1], ac[2], 120), width=1)
    for c in range(ncol):
        d.text((xs[c] + 14, y + 12), headers[c], font=hf, fill=WHITE)
    y += 48
    for ri, row in enumerate(rows):
        bg = PANEL if ri % 2 == 0 else PANEL_HI
        d.rectangle((x0, y, x1, y + rowh), fill=bg)
        # calcula alto real por wrap
        cellf = cfm if s.get("mono_first") and True else cf
        maxlines = 1
        wrapped = []
        for c in range(ncol):
            fnt = cfm if (s.get("mono_cols") and c in s["mono_cols"]) else cf
            cw = xs[c + 1] - xs[c] - 24
            lns = wrap(d, str(row[c]), fnt, cw)
            wrapped.append((lns, fnt))
            maxlines = max(maxlines, len(lns))
        realh = max(rowh, 14 + maxlines * 28)
        d.rectangle((x0, y, x1, y + realh), fill=bg)
        for c in range(ncol):
            lns, fnt = wrapped[c]
            col = TEXT if c == 0 else MUTED
            if s.get("color_map"):
                col = s["color_map"](ri, c, row) or col
            yy = y + (realh - len(lns) * 28) // 2
            for ln in lns:
                d.text((xs[c] + 14, yy), ln, font=fnt, fill=col); yy += 28
        y += realh
    rrect(d, (x0, CONTENT_TOP + (30 if s.get("lead") else 0), x1, y), 10, outline=STROKE, width=1)
    return img

def render_code(s):
    img, d, ac = base_canvas(s.get("module", ""), s.get("title", ""),
                             s.get("idx", 0), s.get("total", 0), s.get("accent", "cyan"))
    y = CONTENT_TOP
    if s.get("lead"):
        lf = font("sans", 24)
        for ln in wrap(d, s["lead"], lf, CONTENT_R - CONTENT_L):
            d.text((CONTENT_L, y), ln, font=lf, fill=MUTED); y += 32
        y += 8
    lines = s["code"]
    title = s.get("term_title", "terminal")
    box_top = y
    cf = font("mono", 21)
    lh = 30
    box_bot = box_top + 52 + len(lines) * lh + 18
    box_bot = min(box_bot, CONTENT_BOT)
    rrect(d, (CONTENT_L, box_top, CONTENT_R, box_bot), 12, fill=(6, 10, 20), outline=STROKE, width=1)
    # barra de ventana
    rrect(d, (CONTENT_L, box_top, CONTENT_R, box_top + 40), 12, fill=(14, 20, 36))
    d.rectangle((CONTENT_L, box_top + 28, CONTENT_R, box_top + 40), fill=(14, 20, 36))
    for i, c in enumerate([RED, AMBER, GREEN]):
        d.ellipse((CONTENT_L + 18 + i * 24, box_top + 14, CONTENT_L + 30 + i * 24, box_top + 26), fill=c)
    tf = font("mono", 18)
    d.text((CONTENT_L + 100, box_top + 11), title, font=tf, fill=FAINT)
    yy = box_top + 54
    for ln in lines:
        if yy + lh > box_bot - 4:
            break
        kind = "out"; txt = ln
        if isinstance(ln, dict):
            kind = ln.get("k", "out"); txt = ln.get("t", "")
        if kind == "cmd":
            d.text((CONTENT_L + 18, yy), "$", font=font("monob", 21), fill=GREEN)
            d.text((CONTENT_L + 40, yy), txt, font=font("monob", 21), fill=WHITE)
        elif kind == "ps":
            d.text((CONTENT_L + 18, yy), "PS>", font=font("monob", 21), fill=CYAN)
            d.text((CONTENT_L + 62, yy), txt, font=font("monob", 21), fill=WHITE)
        elif kind == "hi":
            d.text((CONTENT_L + 40, yy), txt, font=cf, fill=AMBER)
        elif kind == "good":
            d.text((CONTENT_L + 40, yy), txt, font=cf, fill=GREEN)
        elif kind == "bad":
            d.text((CONTENT_L + 40, yy), txt, font=cf, fill=RED)
        elif kind == "cmt":
            d.text((CONTENT_L + 40, yy), txt, font=font("mono", 20), fill=FAINT)
        else:
            d.text((CONTENT_L + 40, yy), txt, font=cf, fill=MUTED)
        yy += lh
    return img

def render_diagram(s):
    """Diagrama basado en nodos y aristas definidos en datos."""
    img, d, ac = base_canvas(s.get("module", ""), s.get("title", ""),
                             s.get("idx", 0), s.get("total", 0), s.get("accent", "cyan"))
    if s.get("lead"):
        lf = font("ital", 24)
        d.text((CONTENT_L, CONTENT_TOP - 8), s["lead"], font=lf, fill=MUTED)
    nodes = s["nodes"]   # dict id -> {x,y,w,h,label,sub,color,shape}
    # aristas primero
    for e in s.get("edges", []):
        a = nodes[e["from"]]; b = nodes[e["to"]]
        p1 = _anchor(a, e.get("fromside"), b)
        p2 = _anchor(b, e.get("toside"), a)
        col = ACCENTS.get(e.get("color", "cyan"), ac)
        arrow(d, p1, p2, color=col, width=e.get("w", 3),
              dashed=e.get("dashed", False), head=e.get("head", 12))
        if e.get("label"):
            mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
            ef = font("bold", 17)
            lw = text_w(d, e["label"], ef)
            rrect(d, (mx - lw / 2 - 8, my - 14, mx + lw / 2 + 8, my + 14), 9,
                  fill=BG2, outline=(col[0], col[1], col[2], 160), width=1)
            d.text((mx - lw / 2, my - 11), e["label"], font=ef, fill=col)
    # nodos
    for nid, n in nodes.items():
        _draw_node(d, n)
    return img

def _anchor(n, side, other):
    x, y, w, h = n["x"], n["y"], n["w"], n["h"]
    cx, cy = x + w / 2, y + h / 2
    if side == "t": return (cx, y)
    if side == "b": return (cx, y + h)
    if side == "l": return (x, cy)
    if side == "r": return (x + w, cy)
    # auto: hacia el otro
    ox = other["x"] + other["w"] / 2
    oy = other["y"] + other["h"] / 2
    dx, dy = ox - cx, oy - cy
    if abs(dx) > abs(dy):
        return (x + w, cy) if dx > 0 else (x, cy)
    return (cx, y + h) if dy > 0 else (cx, y)

def _draw_node(d, n):
    x, y, w, h = n["x"], n["y"], n["w"], n["h"]
    col = ACCENTS.get(n.get("color", "cyan"), CYAN)
    shape = n.get("shape", "box")
    fillc = (col[0], col[1], col[2], n.get("alpha", 34))
    if shape == "cloud":
        d.ellipse((x, y + h * 0.2, x + w * 0.5, y + h), fill=fillc, outline=col, width=2)
        d.ellipse((x + w * 0.3, y, x + w * 0.8, y + h * 0.8), fill=fillc, outline=col, width=2)
        d.ellipse((x + w * 0.5, y + h * 0.2, x + w, y + h), fill=fillc, outline=col, width=2)
        d.rectangle((x + w * 0.1, y + h * 0.55, x + w * 0.9, y + h * 0.98), fill=fillc)
    elif shape == "cyl":
        d.ellipse((x, y, x + w, y + 22), fill=fillc, outline=col, width=2)
        d.rectangle((x, y + 11, x + w, y + h - 11), fill=fillc)
        d.line((x, y + 11, x, y + h - 11), fill=col, width=2)
        d.line((x + w, y + 11, x + w, y + h - 11), fill=col, width=2)
        d.ellipse((x, y + h - 22, x + w, y + h), fill=fillc, outline=col, width=2)
    elif shape == "hex":
        pts = [(x + w * 0.25, y), (x + w * 0.75, y), (x + w, y + h / 2),
               (x + w * 0.75, y + h), (x + w * 0.25, y + h), (x, y + h / 2)]
        d.polygon(pts, fill=fillc, outline=col)
    else:
        rrect(d, (x, y, x + w, y + h), n.get("r", 12), fill=fillc, outline=col, width=2)
    # etiquetas
    lab = n.get("label", "")
    sub = n.get("sub", "")
    lf = font("bold", n.get("fs", 22))
    sf = font("sans", 17)
    total_h = 0
    labl = wrap(d, lab, lf, w - 20)
    total_h = len(labl) * (n.get("fs", 22) + 4)
    subl = wrap(d, sub, sf, w - 20) if sub else []
    total_h += len(subl) * 22
    yy = y + (h - total_h) / 2
    for ln in labl:
        d.text((x + (w - text_w(d, ln, lf)) / 2, yy), ln, font=lf, fill=WHITE); yy += n.get("fs", 22) + 4
    for ln in subl:
        d.text((x + (w - text_w(d, ln, sf)) / 2, yy), ln, font=sf, fill=MUTED); yy += 22

def render_compare(s):
    """Dos (o tres) columnas: típico Ataque vs Defensa."""
    img, d, ac = base_canvas(s.get("module", ""), s.get("title", ""),
                             s.get("idx", 0), s.get("total", 0), s.get("accent", "cyan"))
    cols = s["cols"]
    n = len(cols)
    gap = 24
    x0 = CONTENT_L
    tw = (CONTENT_R - CONTENT_L - gap * (n - 1)) / n
    y0 = CONTENT_TOP
    y1 = CONTENT_BOT
    for i, c in enumerate(cols):
        x = x0 + i * (tw + gap)
        col = ACCENTS.get(c.get("color", "cyan"), CYAN)
        rrect(d, (x, y0, x + tw, y1), 14, fill=PANEL, outline=(col[0], col[1], col[2], 120), width=2)
        rrect(d, (x, y0, x + tw, y0 + 54), 14, fill=(col[0], col[1], col[2], 40))
        d.rectangle((x, y0 + 40, x + tw, y0 + 54), fill=(col[0], col[1], col[2], 40))
        hf = font("bold", 26)
        # punto de color como indicador (en vez de emoji)
        d.ellipse((x + 20, y0 + 20, x + 38, y0 + 38), fill=col)
        d.text((x + 50, y0 + 13), c["title"], font=hf, fill=col)
        yy = y0 + 72
        itf = font("sans", 22)
        ibf = font("bold", 22)
        for it in c["items"]:
            if isinstance(it, dict):
                head = it.get("h"); body = it.get("b")
            else:
                head, body = it, None
            d.text((x + 20, yy + 2), c.get("mark", "▸"), font=ibf, fill=col)
            for j, ln in enumerate(wrap(d, head, ibf if body else itf, tw - 56)):
                d.text((x + 46, yy), ln, font=(ibf if body else itf),
                       fill=TEXT if body else MUTED); yy += 28
            if body:
                for ln in wrap(d, body, itf, tw - 56):
                    d.text((x + 46, yy), ln, font=itf, fill=MUTED); yy += 27
            yy += 12
    return img

def render_stat(s):
    """Tarjetas con cifras/puntos clave."""
    img, d, ac = base_canvas(s.get("module", ""), s.get("title", ""),
                             s.get("idx", 0), s.get("total", 0), s.get("accent", "cyan"))
    cards = s["cards"]
    n = len(cards)
    cols = min(n, s.get("ncol", 3))
    rows = math.ceil(n / cols)
    gap = 22
    y0 = CONTENT_TOP + 10
    cw = (CONTENT_R - CONTENT_L - gap * (cols - 1)) / cols
    ch = (CONTENT_BOT - y0 - gap * (rows - 1)) / rows
    for i, c in enumerate(cards):
        r = i // cols; cc = i % cols
        x = CONTENT_L + cc * (cw + gap)
        y = y0 + r * (ch + gap)
        col = ACCENTS.get(c.get("color", "cyan"), CYAN)
        rrect(d, (x, y, x + cw, y + ch), 14, fill=PANEL, outline=STROKE, width=1)
        d.rectangle((x, y, x + 6, y + ch), fill=col)
        rrect(d, (x, y, x + 6, y + ch), 3, fill=col)
        if c.get("big"):
            nf = font("bold", 46)
            d.text((x + 26, y + 18), c["big"], font=nf, fill=col)
            ty = y + 76
        else:
            ty = y + 20
        hf = font("bold", 24)
        for ln in wrap(d, c.get("h", ""), hf, cw - 44):
            d.text((x + 26, ty), ln, font=hf, fill=TEXT); ty += 30
        bf = font("sans", 20)
        for ln in wrap(d, c.get("b", ""), bf, cw - 44):
            d.text((x + 26, ty), ln, font=bf, fill=MUTED); ty += 26
    return img

def render_quote(s):
    img, d, ac = base_canvas(accent=s.get("accent", "cyan"), chrome=False)
    vgrad(img, (0, 0, W, H), (14, 20, 42), (7, 10, 20))
    d = _d(img)
    qf = font("bold", 92)
    d.text((80, 120), "“", font=qf, fill=(ac[0], ac[1], ac[2], 120))
    tf = font("bold", 40)
    y = 230
    for ln in wrap(d, s["text"], tf, W - 220):
        d.text((110, y), ln, font=tf, fill=WHITE); y += 56
    if s.get("by"):
        bf = font("sans", 26)
        d.text((110, y + 20), "— " + s["by"], font=bf, fill=ac)
    return img

# ----------------------------------------------------------------------------
# Dispatcher
# ----------------------------------------------------------------------------
RENDERERS = {
    "cover": render_cover, "section": render_section, "bullets": render_bullets,
    "table": render_table, "code": render_code, "diagram": render_diagram,
    "compare": render_compare, "stat": render_stat, "quote": render_quote,
}

def render_slide(s):
    return RENDERERS[s["type"]](s)

if __name__ == "__main__":
    # prueba rápida
    demo = {"type": "cover", "accent": "cyan",
            "kicker": "CURSO PROFESIONAL 2026",
            "title_lines": ["Active Directory", "Hacking & Defensa"],
            "subtitle": "De los fundamentos al dominio completo: cómo funciona, cómo se ataca y cómo se protege.",
            "footer": "Módulo 0 · Introducción", "footer2": "Formato vídeo narrado"}
    render_cover(demo).save("/tmp/_demo_cover.png")
    print("ok")
