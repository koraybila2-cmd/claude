import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "build"))
from svglib import SVG, NEU, TXT, CYAN, MAG, FONT, esc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "svg")
os.makedirs(OUT, exist_ok=True)
ACC = "var(--color-accent)"
GRAY = "var(--color-neutral-700)"


def save(s, name):
    s.save(os.path.join(OUT, name + ".svg"))


def hbar(s, x0, y, h, x1, color, opacity=1):
    w = x1 - x0
    if w <= 0:
        return
    r = min(4, h / 2, w)
    s.add(f'<path d="M{x0:.1f},{y:.1f} L{x1 - r:.1f},{y:.1f} Q{x1:.1f},{y:.1f} {x1:.1f},{y + r:.1f} '
          f'L{x1:.1f},{y + h - r:.1f} Q{x1:.1f},{y + h:.1f} {x1 - r:.1f},{y + h:.1f} L{x0:.1f},{y + h:.1f} Z" '
          f'fill="{color}" fill-opacity="{opacity}"/>')


def rbar(s, x0, y, h, x1, color, opacity=1):
    """iki ucu yuvarlak yatay bant"""
    s.add(f'<rect x="{x0:.1f}" y="{y:.1f}" width="{x1 - x0:.1f}" height="{h:.1f}" rx="4" fill="{color}" fill-opacity="{opacity}"/>')


def grid_v(s, x, y0, y1, base=False):
    s.add(f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y1}" stroke="{NEU}" stroke-opacity="{0.45 if base else 0.15}" stroke-width="1"/>')


def grid_h(s, y, x0, x1, base=False):
    s.add(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{NEU}" stroke-opacity="{0.45 if base else 0.15}" stroke-width="1"/>')


def dline(s, x1, y1, x2, y2, color=NEU, opacity=0.5, dash="4 3", width=1):
    s.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-opacity="{opacity}" stroke-width="{width}" stroke-dasharray="{dash}"/>')


def dpath(s, d, color=NEU, marker=True, width=1.5):
    m = f' marker-end="url(#{s.mid}{s._m(color)})"' if marker else ""
    s.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-dasharray="5 3"{m}/>')


def lines(s, x, y, rows, anchor="start", lh=14, fs1=12, fs2=10.5):
    for i, (t, st) in enumerate(rows):
        s.text(x, y + i * lh, t, st, anchor, fs1, fs2)


# ============================================================ Sekil 1.1 emilim yuzeyi
s = SVG(640, 392, "İnce bağırsağın emilim yüzeyini büyüten üç düzey: plika 3 kat, villus 10 kat, mikrovillus 20 kat; toplam yaklaşık 600 kat", "k5a")
# panel A: plika
s.text(110, 22, "Plika sirkülaris", "title", "middle", fs1=12.5)
s.add(f'<path d="M40,55 L180,55 M40,125 L180,125" stroke="{NEU}" stroke-width="1.3" fill="none"/>')
s.add(f'<ellipse cx="40" cy="90" rx="12" ry="35" fill="white" stroke="{NEU}" stroke-width="1.3"/>')
s.add(f'<path d="M180,55 A12,35 0 0 1 180,125" stroke="{NEU}" stroke-width="1.3" fill="none"/>')
for x in (68, 94, 120, 146, 170):
    s.add(f'<ellipse cx="{x}" cy="90" rx="6" ry="31" fill="{ACC}" fill-opacity="0.3" stroke="{CYAN}" stroke-width="1.2"/>')
lines(s, 110, 185, [("mukoza + submukoza", "body"), ("kalıcı halka katlantı", "sub")], "middle", lh=15)
s.text(110, 224, "× 3", "title", "middle", fs1=15)
# panel B: villus
s.text(320, 22, "Villus", "title", "middle", fs1=12.5)
base = 132
d = f"M262,{base} L272,{base}"
for cx in (300, 345):
    d += f" L{cx - 15},{base} L{cx - 15},{58} A15,15 0 0 1 {cx + 15},{58} L{cx + 15},{base}"
    if cx == 300:
        d += f" L{322 - 7},{base} L{315},{160} A7,7 0 0 0 {329},{160} L{329},{base}"
d += f" L378,{base}"
for cx in (300, 345):
    s.add(f'<path d="M{cx - 15},{base} L{cx - 15},58 A15,15 0 0 1 {cx + 15},58 L{cx + 15},{base} Z" fill="{ACC}" fill-opacity="0.12"/>')
    dline(s, cx, base, cx, 54, ACC, 0.9, "3 2", 1.6)
s.add(f'<path d="{d}" fill="none" stroke="{CYAN}" stroke-width="2"/>')
s.text(371, 70, "epitel", "small")
s.add(f'<line x1="369" y1="67" x2="361" y2="67" stroke="{NEU}" stroke-width="0.8"/>')
s.text(371, 100, "lakteal", "small")
s.add(f'<line x1="369" y1="97" x2="347" y2="97" stroke="{NEU}" stroke-width="0.8"/>')
s.text(338, 168, "kript", "small")
s.add(f'<line x1="336" y1="165" x2="330" y2="160" stroke="{NEU}" stroke-width="0.8"/>')
lines(s, 320, 185, [("epitel + lamina propria", "body"), ("lakteal ve kapiller taşır", "sub")], "middle", lh=15)
s.text(320, 224, "× 10", "title", "middle", fs1=15)
# panel C: mikrovillus
s.text(530, 22, "Mikrovillus", "title", "middle", fs1=12.5)
for x0 in (491, 532):
    s.add(f'<rect x="{x0}" y="70" width="38" height="90" rx="3" fill="{ACC}" fill-opacity="0.08" stroke="{NEU}" stroke-width="1.2"/>')
    s.add(f'<ellipse cx="{x0 + 19}" cy="138" rx="8" ry="12" fill="{NEU}" fill-opacity="0.3"/>')
    for k in range(11):
        x = x0 + 4 + k * 3
        s.add(f'<line x1="{x}" y1="70" x2="{x}" y2="57" stroke="{CYAN}" stroke-width="1.4"/>')
s.text(578, 52, "fırçamsı", "small")
s.text(578, 63, "kenar", "small")
lines(s, 530, 185, [("hücre zarının çıkıntıları", "body"), ("hücre başına ~3000, enzimler burada", "sub")], "middle", lh=15)
s.text(530, 224, "× 20", "title", "middle", fs1=15)
s.arrow(196, 118, 255, 118)
s.arrow(416, 118, 480, 118)
# alt: birikimli yuzey, log olcek
s.text(20, 262, "YÜZEY ALANI, DÜZ TÜPE GÖRE (LOGARİTMİK ÖLÇEK)", "cap")
x0, x1 = 210, 600
sx = lambda v: x0 + (x1 - x0) * math.log10(v) / 3
for v, lab in ((1, "1 (düz tüp)"), (10, "10"), (100, "100"), (1000, "1000")):
    grid_v(s, sx(v), 274, 360, base=(v == 1))
    s.text(sx(v), 376, lab, "small", "middle" if v > 1 else "start")
rows = [("Plika", 3, 0.4), ("Plika + villus", 30, 0.7), ("Plika + villus + mikrovillus", 600, 1)]
for i, (t, v, op) in enumerate(rows):
    yc = 290 + i * 28
    s.text(x0 - 10, yc + 4, t, "body", "end", fs2=11)
    hbar(s, x0, yc - 8, 16, sx(v), ACC, op)
    s.text(sx(v) + 7, yc + 4, f"{v} kat", "title" if v == 600 else "body", fs1=11.5, fs2=11)
save(s, "m56k5_yuzey")

# ============================================================ Sekil 1.2 kript-villus birimi
s = SVG(640, 336, "Kript-villus birimi: kök hücreler kriptte bölünür, enterosit ve goblet hücreleri villus ucuna göç eder, Paneth hücreleri kript tabanındadır; sağda Peyer plağı üstünde M hücresi", "k5b")
ys = 170
d = (f"M40,{ys} L112,{ys} L112,282 A18,18 0 0 0 148,282 L148,{ys} L165,{ys} L165,65 A35,35 0 0 1 235,65 "
     f"L235,{ys} L252,{ys} L252,282 A18,18 0 0 0 288,282 L288,{ys} L340,{ys}")
s.add(f'<path d="M165,{ys} L165,65 A35,35 0 0 1 235,65 L235,{ys} Z" fill="{ACC}" fill-opacity="0.08"/>')
s.add(f'<path d="{d}" fill="none" stroke="{CYAN}" stroke-width="2.2"/>')
# goblet
for (x, y) in ((171, 112), (229, 140), (171, 150), (118, 215), (282, 200)):
    s.add(f'<ellipse cx="{x}" cy="{y}" rx="4.5" ry="8" fill="white" stroke="{NEU}" stroke-width="1.2"/>')
# Paneth
for cx in (130, 270):
    for (dx, dy) in ((-9, -4), (0, 6), (9, -4)):
        s.add(f'<circle cx="{cx + dx}" cy="{292 + dy}" r="4" fill="{ACC}" fill-opacity="0.85"/>')
# kok hucre
for cx in (130, 270):
    for dx in (-14, 14):
        s.add(f'<rect x="{cx + dx - 3}" y="257" width="6" height="6" fill="{CYAN}"/>')
# enteroendokrin
for (x, y) in ((118, 240), (256, 232)):
    s.add(f'<path d="M{x - 4},{y + 4} L{x + 4},{y + 4} L{x},{y - 4} Z" fill="{NEU}" fill-opacity="0.7"/>')
# goc oku
s.path("M141,258 L141,180 Q141,162 157,162 L157,64 Q158,30 186,22", CYAN, True, 1.6)
s.text(240, 22, "5-6 günde villus ucuna göç", "cyan")
s.arrow(300, 232, 300, 280, NEU, True, 1.2)
# etiketler
s.text(22, 300, "Paneth hücreleri", "small")
s.text(22, 313, "kript tabanı, 20-30 gün", "small")
s.add(f'<line x1="104" y1="297" x2="118" y2="294" stroke="{NEU}" stroke-width="0.8"/>')
s.text(22, 252, "kök hücreler", "body", fs2=10.5)
s.add(f'<line x1="86" y1="257" x2="112" y2="260" stroke="{NEU}" stroke-width="0.8"/>')
s.text(22, 214, "goblet", "body", fs2=10.5)
s.add(f'<line x1="58" y1="212" x2="113" y2="214" stroke="{NEU}" stroke-width="0.8"/>')
s.text(310, 222, "enteroendokrin", "body", fs2=10.5)
s.add(f'<line x1="308" y1="219" x2="261" y2="230" stroke="{NEU}" stroke-width="0.8"/>')
s.text(310, 268, "Paneth hücreleri", "small")
s.text(310, 280, "tabana iner", "small")
s.text(248, 100, "enterositler", "body", fs2=10.5)
s.text(248, 113, "fırçamsı kenar", "small")
s.add(f'<line x1="246" y1="98" x2="236" y2="98" stroke="{NEU}" stroke-width="0.8"/>')
s.text(60, 160, "lümen", "small")
s.text(205, 205, "lamina propria", "small", "middle")
# M hucresi
s.text(530, 30, "Peyer plağı üstünde M hücresi", "title", "middle", fs1=12)
for k, x in enumerate((440, 474, 542, 576)):
    s.add(f'<rect x="{x}" y="86" width="32" height="42" rx="2" fill="{ACC}" fill-opacity="0.08" stroke="{NEU}" stroke-width="1"/>')
    for j in range(8):
        s.add(f'<line x1="{x + 3 + j * 3.7:.1f}" y1="86" x2="{x + 3 + j * 3.7:.1f}" y2="79" stroke="{CYAN}" stroke-width="1.2"/>')
s.add(f'<path d="M508,86 Q516,80 525,86 Q533,80 541,86 L541,128 L533,128 Q525,108 517,128 L508,128 Z" fill="white" stroke="{CYAN}" stroke-width="1.6"/>')
s.add(f'<circle cx="525" cy="122" r="5" fill="{NEU}" fill-opacity="0.55"/>')
for (x, y) in ((519, 58), (527, 52), (533, 60)):
    s.add(f'<path d="M{x},{y - 3} L{x + 3},{y + 2} L{x - 3},{y + 2} Z" fill="{NEU}"/>')
s.arrow(525, 64, 525, 110, CYAN, True, 1.4)
s.add(f'<ellipse cx="525" cy="178" rx="82" ry="34" fill="{ACC}" fill-opacity="0.12"/>')
s.add(f'<circle cx="505" cy="150" r="6" fill="{NEU}" fill-opacity="0.35"/><circle cx="545" cy="152" r="6" fill="{NEU}" fill-opacity="0.35"/>')
s.text(525, 186, "lenfoid folikül", "small", "middle")
s.text(557, 56, "antijen, mikrop", "small")
s.text(452, 148, "dendritik hücre,", "small", "end")
s.text(452, 160, "lenfosit", "small", "end")
s.add(f'<line x1="455" y1="151" x2="498" y2="150" stroke="{NEU}" stroke-width="0.8"/>')
lines(s, 530, 236, [("Antijeni yıkmadan hücrenin içinden", "body"), ("geçirir (transsitoz) ve bazal cepteki", "body"),
                    ("bağışıklık hücrelerine verir.", "body"), ("Lipid emmez: emilim enterositin işidir.", "sub")], "middle", lh=14)
save(s, "m56k5_kript")

# ============================================================ Sekil 1.3 duodenum
s = SVG(640, 300, "Duodenumun dört kısmı ve omurga seviyeleri: pars superior L1, pars descendens L1-L3, pars horizontalis L3, pars ascendens L2; bulbusun komşuları", "k5c")
for lab, y in (("L1", 80), ("L2", 160), ("L3", 240)):
    dline(s, 52, y, 430, y, NEU, 0.35)
    s.text(30, y + 4, lab, "title", "middle", fs1=12)
s.add(f'<ellipse cx="322" cy="168" rx="58" ry="48" fill="{NEU}" fill-opacity="0.12"/>')
s.text(322, 172, "Caput pancreatis", "sub", "middle", fs2=10.5)
duo = "M400,80 L268,80 Q238,80 236,110 L236,212 Q236,240 266,240 L428,240 Q458,240 459,212 L459,163 Q462,148 480,146 L490,146"
s.add(f'<path d="{duo}" fill="none" stroke="{ACC}" stroke-opacity="0.35" stroke-width="22" stroke-linecap="butt" stroke-linejoin="round"/>')
s.add(f'<path d="M400,80 L342,80" fill="none" stroke="{ACC}" stroke-opacity="0.45" stroke-width="22" stroke-linecap="butt"/>')
s.add(f'<path d="M490,146 L562,146" fill="none" stroke="{ACC}" stroke-opacity="0.18" stroke-width="18" stroke-linecap="butt"/>')
s.add(f'<line x1="410" y1="64" x2="410" y2="96" stroke="{NEU}" stroke-width="2.5"/>')
s.text(416, 112, "pilor", "small")
s.add(f'<circle cx="248" cy="175" r="4.5" fill="{CYAN}"/>')
s.text(258, 192, "papilla major", "cyan", fs2=10.5)
dline(s, 208, 175, 262, 175, CYAN, 0.9, "3 2", 1.2)
s.text(374, 58, "Bulbus duodeni", "title", "middle", fs1=11.5)
s.text(272, 58, "Pars superior · L1", "sub", "middle", fs2=10.5)
s.text(200, 135, "Pars descendens", "title", "end", fs1=11.5)
s.text(200, 149, "L1-L3", "sub", "end", fs2=10.5)
s.text(200, 199, "papillanın üstü: truncus coeliacus", "small", "end")
s.text(200, 211, "altı: a. mesenterica superior", "small", "end")
s.text(345, 270, "Pars horizontalis · L3 (aorta ve VCI önünden)", "sub", "middle", fs2=10.5)
s.text(475, 200, "Pars ascendens · L2", "sub", fs2=10.5)
s.text(495, 130, "Flexura duodenojejunalis", "small")
s.text(575, 150, "jejunum", "small")
s.box(452, 8, 180, 96, [("Bulbusun komşuları", "title"), ("önde ve üstte: lobus", "body"), ("quadratus, safra kesesi", "body"),
                        ("arkada: ductus choledochus,", "body"), ("a. gastroduodenalis, v. portae", "body")],
      kind="key", fs1=11.5, fs2=10.5, lh=16)
s.add(f'<line x1="452" y1="62" x2="402" y2="74" stroke="{CYAN}" stroke-width="1"/>')
save(s, "m56k5_duodenum")

# ============================================================ Sekil 1.4 arter alanlari
s = SVG(640, 356, "Bağırsağın arter alanları: truncus coeliacus ön bağırsak, a. mesenterica superior orta bağırsak, a. mesenterica inferior arka bağırsak, a. iliaca interna rektumun alt kısmı ve anal kanal; venöz drenaj portal ve sistemik", "k5d")
seg = [(10, 130, "Truncus coeliacus", ["a. gastroduodenalis", "a. pancreatico-", "duodenalis superior"], "Ön bağırsak",
        ["mide, duodenumun", "papillaya kadarki", "kısmı"], 0.15),
       (130, 345, "A. mesenterica superior", ["a. pancreaticoduodenalis inferior", "aa. jejunales ve ileales (15-18)", "a. ileocolica, a. colica dextra", "a. colica media"], "Orta bağırsak",
        ["duodenumun geri kalanı, jejunum,", "ileum, çekum, appendiks, colon", "ascendens, transversumun sağ 2/3'ü"], 0.32),
       (345, 495, "A. mesenterica inferior", ["a. colica sinistra", "aa. sigmoideae", "a. rectalis superior"], "Arka bağırsak",
        ["transversumun sol 1/3'ü,", "descendens, sigmoideum,", "rektumun üst kısmı"], 0.5),
       (495, 630, "A. iliaca interna", ["a. rectalis media", "a. pudenda interna →", "a. rectalis inferior"], "Pelvis",
        ["rektumun orta ve alt", "kısmı, anal kanal"], 0.7)]
for x0, x1, art, br, band, org, op in seg:
    cx = (x0 + x1) / 2
    s.box(x0 + 4, 10, x1 - x0 - 8, 104, [(art, "title")] + [(b, "body") for b in br], fs1=11, fs2=10.5, lh=15, pad_top=20)
    s.arrow(cx, 114, cx, 146)
    rbar(s, x0 + 2, 150, 34, x1 - 2, ACC, op)
    s.text(cx, 171, band, "title", "middle", fs1=11.5)
    lines(s, cx, 202, [(o, "sub") for o in org], "middle", lh=13, fs2=10.5)
rbar(s, 12, 252, 22, 493, ACC, 0.2)
s.text(252, 267, "Venler: v. mesenterica superior ve inferior → v. portae → karaciğer (portal)", "body", "middle", fs2=10.5)
rbar(s, 497, 252, 22, 628, NEU, 0.18)
s.text(562, 267, "v. iliaca interna", "body", "middle", fs2=10.5)
s.add(f'<circle cx="495" cy="263" r="7" fill="white" stroke="{CYAN}" stroke-width="2"/>')
s.add(f'<line x1="495" y1="270" x2="495" y2="282" stroke="{CYAN}" stroke-width="1"/>')
s.text(400, 296, "plexus venosus rectalis: portal ve sistemik venler rektum ve anal kanalda birleşir", "cyan", "middle", fs2=10.5)
s.text(320, 326, "Lenf arterleri izler: truncus coeliacus, SMA ve IMA çevresindeki preaortik düğümler · pelvis için iliak düğümler", "small", "middle")
save(s, "m56k5_arter")

# ============================================================ Sekil 1.5 lenf yolu
s = SVG(640, 240, "Bağırsak lenfinin yolu: preaortik düğümler, truncus intestinalis, cisterna chyli, ductus thoracicus; alt ekstremite lenfi trunci lumbales ile cisterna chylide katılır", "k5e")
s.box(10, 88, 125, 54, [("Bağırsak duvarı", "title"), ("lakteal →", "sub"), ("mezenterik düğümler", "sub")], fs1=11.5, fs2=10.5, lh=14)
s.box(155, 88, 130, 54, [("Preaortik düğümler", "title"), ("truncus coeliacus,", "sub"), ("SMA ve IMA çevresi", "sub")], fs1=11.5, fs2=10.5, lh=14)
s.box(305, 92, 110, 46, [("Truncus", "title"), ("intestinalis", "title")], fs1=11.5, lh=15)
s.box(440, 85, 130, 60, [("Cisterna chyli", "title"), ("L1-L2", "sub"), ("lenfler burada karışır", "sub")], kind="key", fs1=12, fs2=10.5, lh=15)
s.box(430, 8, 150, 46, [("Ductus thoracicus", "title"), ("→ sol venöz açı", "sub")], fs1=11.5, fs2=10.5, lh=15)
s.box(432, 178, 146, 50, [("Trunci lumbales", "title"), ("alt ekstremite, pelvis", "sub")], fs1=11.5, fs2=10.5, lh=15)
s.arrow(135, 115, 153, 115)
s.arrow(285, 115, 303, 115)
s.arrow(415, 115, 438, 115)
s.arrow(505, 85, 505, 56)
s.arrow(505, 178, 505, 147)
lines(s, 10, 182, [("Pars descendens iki alanın sınırındadır:", "body"), ("üst kısmı truncus coeliacus, alt kısmı", "body"), ("SMA çevresindeki düğümlere akar.", "body")], lh=14, fs2=10.5)
save(s, "m56k5_lenf")

# ============================================================ Sekil 1.6 sinirler
s = SVG(640, 342, "İnce bağırsağın sinirleri: sempatik T9-T10 ve nn. splanchnici, parasempatik n. vagus; pleksusların sırası subserosus, myentericus, submucosus; visseral afferent yollar", "k5f")
s.box(10, 12, 165, 48, [("Medulla spinalis T9-T10", "title"), ("lateral boynuz (sempatik)", "sub")], fs1=11.5, fs2=10.5)
s.box(10, 84, 165, 48, [("N. splanchnicus", "title"), ("major ve minor", "sub")], fs1=11.5, fs2=10.5)
s.box(10, 156, 165, 52, [("Ganglion coeliacum ve", "title"), ("mesentericum superius", "title"), ("sinaps", "sub")], fs1=11.5, fs2=10.5, lh=14)
s.arrow(92, 60, 92, 82)
s.arrow(92, 132, 92, 154)
s.box(290, 12, 160, 48, [("N. vagus", "title"), ("parasempatik, beyin sapı", "sub")], fs1=11.5, fs2=10.5)
s.box(195, 156, 255, 52, [("Plexus coeliacus →", "title"), ("plexus mesentericus superior", "title"), ("SMA'yı saran pleksus", "sub")], fs1=11.5, fs2=10.5, lh=14)
s.arrow(175, 182, 193, 182)
s.arrow(370, 60, 370, 154)
s.text(378, 102, "sinaps yapmadan", "small")
s.text(378, 114, "geçer", "small")
rows = [("1. Plexus subserosus", "seroza altında"), ("2. Plexus myentericus (Auerbach)", "iki kas tabakası arası · peristaltizm"),
        ("3. Plexus submucosus (Meissner)", "submukoza · salgı ve kan akımı")]
for i, (t, sub) in enumerate(rows):
    s.box(195, 226 + i * 38, 255, 34, [(t, "title"), (sub, "sub")], fs1=11, fs2=10, lh=13)
s.arrow(322, 208, 322, 224)
s.text(188, 280, "duvar, dıştan içe", "small", "end")
s.box(468, 150, 168, 70, [("Fizyolojik duyular", "title"), ("dolgunluk, gerilme, irritasyon", "sub"), ("n. vagus → nucleus tractus", "sub"), ("solitarii (beyin sapı)", "sub")], kind="key", fs1=11.5, fs2=10, lh=13)
s.box(468, 248, 168, 70, [("Ağrı", "title"), ("nn. splanchnici → arka kök →", "sub"), ("T9-T10 segmentleri: göbek", "sub"), ("çevresine yansır (T10)", "sub")], kind="key", fs1=11.5, fs2=10, lh=13)
dpath(s, "M450,240 L459,240 L459,185 L466,185", CYAN)
dpath(s, "M450,283 L466,283", CYAN)
s.text(475, 30, "— düz ok: efferent lif", "small")
s.text(475, 46, "- - kesikli ok: afferent lif", "small")
save(s, "m56k5_sinir")

# ============================================================ Sekil 2.1 sureye gore ishal
s = SVG(640, 212, "İshalin süresine göre adı: akut ishal 14 günden kısa, persistan ishal akut başlar ve 14 günü aşar, kronik ishal bir aydan uzun sürer ve kilo alamamayla birliktedir", "k5g")
x0, x1, dmax = 175, 610, 45
sx = lambda d: x0 + (x1 - x0) * d / dmax
for d in (0, 7, 14, 21, 30, 45):
    grid_v(s, sx(d), 34, 172, base=(d == 0))
    s.text(sx(d), 190, f"{d}" + (" gün" if d == 45 else ""), "small", "middle")
for d, lab in ((14, "14. gün"), (30, "30. gün (1 ay)")):
    dline(s, sx(d), 28, sx(d), 176, CYAN, 0.9, "4 3", 1.2)
    s.text(sx(d), 20, lab, "cyanb", "middle", fs2=10.5)
rows = [("Akut ishal", "≥3 sulu dışkı / 24 saat", [(0, 12, 0.45)]),
        ("Persistan ishal", "akut başlar, >14 gün", [(0, 30, 0.16), (14, 30, 0.75)]),
        ("Kronik ishal", ">1 ay + kilo alamama", [(0, 45, 0.16), (30, 45, 1.0)])]
for i, (t, sub, segs) in enumerate(rows):
    yc = 60 + i * 46
    s.text(x0 - 12, yc - 1, t, "title", "end", fs1=12)
    s.text(x0 - 12, yc + 13, sub, "sub", "end", fs2=10.5)
    for a, b, op in segs:
        hbar(s, sx(a), yc - 9, 18, sx(b), ACC, op)
save(s, "m56k5_sure")

# ============================================================ Sekil 2.2 dehidratasyon
s = SVG(640, 392, "Dehidratasyon bulgularının kaynağı: damar içi hacim azalınca sempatik yanıt, ADH ve renin-anjiyotensin-aldosteron, susuzluk; doku sıvısı azalınca turgor ve göz bulguları; kompansasyon tükenince kan basıncı düşer", "k5h")
s.box(210, 8, 220, 36, [("Sıvı kaybı: ishal, kusma", "title")], fs1=12)
s.arrow(320, 44, 320, 64)
s.box(200, 66, 240, 36, [("Hücre dışı sıvı azalır", "title")], fs1=12)
s.arrow(262, 102, 150, 132)
s.arrow(378, 102, 490, 132)
s.box(30, 134, 230, 38, [("Damar içi hacim azalır", "title")], fs1=12)
s.box(380, 134, 230, 38, [("Doku arası sıvı azalır", "title")], fs1=12)
s.arrow(120, 172, 96, 194)
s.arrow(190, 172, 276, 194)
s.arrow(495, 172, 495, 194)
s.box(10, 196, 172, 54, [("Baroreseptör → sempatik", "title"), ("kalp hızlanır, deri ve", "sub"), ("ekstremite damarları daralır", "sub")], fs1=11.5, fs2=10.5, lh=14)
s.box(192, 196, 172, 54, [("Hipotalamus ve böbrek", "title"), ("ADH, renin-anjiyotensin-", "sub"), ("aldosteron, susuzluk merkezi", "sub")], fs1=11.5, fs2=10.5, lh=14)
s.box(384, 196, 222, 54, [("Turgor azalır, ağız kurur", "title"), ("göz küreleri çöker,", "sub"), ("süt çocuğunda fontanel çöker", "sub")], kind="key", fs1=11.5, fs2=10.5, lh=14)
s.arrow(96, 250, 96, 270)
s.arrow(278, 250, 278, 270)
s.box(10, 272, 172, 50, [("Taşikardi", "title"), ("soğuk, alacalı ekstremite,", "sub"), ("kapiller dolum uzar", "sub")], kind="key", fs1=11.5, fs2=10.5, lh=14)
s.box(192, 272, 172, 50, [("İdrar < 1 ml/kg/saat", "title"), ("susuzluk artar", "sub")], kind="key", fs1=11.5, fs2=10.5, lh=15)
lines(s, 495, 282, [("Bu yanıtlar kan basıncını korur.", "body"), ("Normal kan basıncı dehidratasyonu", "body"), ("hafif yapmaz.", "body")], "middle", lh=14, fs2=10.5)
s.arrow(96, 322, 140, 342)
s.arrow(278, 322, 278, 342)
s.box(110, 344, 420, 44, [("Kompansasyon tükenince (≥%10): kan basıncı düşer", "title"), ("beyin perfüzyonu azalır: letarji, koma", "sub")], kind="key", fs1=12, fs2=10.5, lh=16)
save(s, "m56k5_dehid")

# ============================================================ Sekil 3.1 uc evre
s = SVG(640, 336, "Emilimin üç evresi yağın yolunda: lüminal evre, mukozal evre, transport evresi ve her evreyi bozan hastalıklar", "k5i")
cols = [(10, 200, "1. Lüminal evre", [("Lümende sindirim", "title"), ("pankreas lipazı + kolipaz;", "sub"), ("safra tuzları → miçel", "sub")],
         ["kronik pankreatit", "kistik fibrozis", "lipaz-kolipaz eksikliği", "kolestaz, safra asidi defekti", "bakteri çoğalması"], [("Biyopsi normal", "title"), ("mukoza sağlam", "sub")]),
        (225, 415, "2. Mukozal evre", [("Enterositte işlem", "title"), ("fırçamsı kenar enzimleri;", "sub"), ("ApoB-48 + MTP → şilomikron", "sub")],
         ["çölyak hastalığı", "disakkaridaz eksiklikleri", "tropikal spru", "abetalipoproteinemi (MTP)", "Whipple hastalığı"], [("Biyopside bulgu var", "title"), ("villus atrofisi, yağlı enterosit", "sub")]),
        (440, 630, "3. Transport evresi", [("Kana ve lenfe geçiş", "title"), ("şilomikron → lakteal → lenf", "sub"), ("şeker, amino asit → portal kan", "sub")],
         ["intestinal lenfanjiektazi", "Whipple hastalığı", "(lenf yolu tıkanır)"], [("Biyopside bulgu var", "title"), ("genişlemiş lakteal, PAS+ makrofaj", "sub")])]
for x0, x1, head, proc, dis, bx in cols:
    cx = (x0 + x1) / 2
    rbar(s, x0, 8, 30, x1, ACC, 0.25)
    s.text(cx, 28, head, "title", "middle", fs1=12.5)
    s.box(x0, 50, x1 - x0, 62, proc, fs1=11.5, fs2=10.5, lh=15)
    s.box(x0, 146, x1 - x0, 100, [(d, "body") for d in dis], fs2=10.5, lh=17)
    s.box(x0, 278, x1 - x0, 50, bx, kind="key", fs1=11.5, fs2=10.5, lh=15)
s.arrow(200, 81, 223, 81)
s.arrow(415, 81, 438, 81)
s.text(10, 136, "BOZAN HASTALIKLAR", "cap")
s.text(10, 268, "İNCE BAĞIRSAK BİYOPSİSİ", "cap")
save(s, "m56k5_evre")

# ============================================================ Sekil 3.2 karbonhidrat malabsorbsiyonu
s = SVG(640, 336, "Karbonhidrat malabsorbsiyonunun bulguları ve testleri: ozmotik ishal, kolonda fermentasyonla gaz ve asit, hidrojen nefes testi, dışkı pH ve redüktan madde", "k5j")
s.box(170, 8, 300, 46, [("Disakkarit (ör. laktoz) fırçamsı", "title"), ("kenarda yıkılamaz, emilemez", "title")], fs1=12, lh=16)
s.arrow(250, 54, 165, 82)
s.arrow(390, 54, 475, 82)
s.box(20, 84, 285, 42, [("İnce bağırsak: ozmotik yük", "title"), ("su lümene çekilir", "sub")], fs1=11.5, fs2=10.5)
s.box(335, 84, 290, 42, [("Kolon: bakteriyel fermentasyon", "title"), ("emilmeyen şeker bakterilere besin olur", "sub")], fs1=11.5, fs2=10.5)
s.arrow(162, 126, 162, 148)
s.arrow(430, 126, 400, 148)
s.arrow(530, 126, 556, 148)
s.box(20, 150, 285, 50, [("Bol, sulu, köpüklü ishal", "title"), ("ozmotik ishal: açlıkla azalır", "sub")], fs1=11.5, fs2=10.5)
s.box(330, 150, 140, 60, [("H₂, CO₂, metan", "title"), ("gaz, şişkinlik,", "sub"), ("kramp", "sub")], fs1=11.5, fs2=10.5, lh=14)
s.box(482, 150, 148, 60, [("Kısa zincirli yağ", "title"), ("asidi, laktik asit", "title"), ("pişik, asidik dışkı", "sub")], fs1=11.5, fs2=10.5, lh=14)
s.arrow(162, 200, 162, 238)
s.arrow(400, 210, 400, 238)
s.arrow(556, 210, 556, 238)
s.text(170, 224, "dışkıda şeker", "small")
s.text(408, 228, "H₂ kana geçer", "small")
s.box(20, 240, 285, 48, [("Dışkıda redüktan madde (+)", "title"), ("fermente edilmeyen şeker", "sub")], kind="key", fs1=11.5, fs2=10.5)
s.box(330, 240, 140, 48, [("H₂ nefes testi", "title"), ("ekspiryumda H₂ artar", "sub")], kind="key", fs1=11.5, fs2=10.5)
s.box(482, 240, 148, 48, [("Dışkı pH", "title"), ("< 6", "sub")], kind="key", fs1=11.5, fs2=10.5)
s.text(320, 318, "Ödem bu zincirde yoktur: serum proteinleri korunur. Ödem protein malabsorbsiyonunun ya da kaybının bulgusudur.", "small", "middle")
save(s, "m56k5_kh")

# ============================================================ Sekil 3.3 fekal elastaz
s = SVG(640, 170, "Fekal elastaz-1 sonucunun yorumu: 100 mikrogram/g altı ağır yetmezlik, 100-200 hafif-orta yetmezlik, 200 üstü normal", "k5k")
x0, x1, vmax = 40, 600, 500
sx = lambda v: x0 + (x1 - x0) * v / vmax
for a, b, op, lab, sub in ((0, 100, 1.0, "< 100", "ağır yetmezlik"), (100, 200, 0.55, "100-200", "hafif-orta yetmezlik"), (200, 500, 0.18, "> 200", "normal")):
    s.add(f'<rect x="{sx(a) + 1:.1f}" y="58" width="{sx(b) - sx(a) - 2:.1f}" height="26" rx="3" fill="{ACC}" fill-opacity="{op}"/>')
    s.text((sx(a) + sx(b)) / 2, 34, lab, "title", "middle", fs1=12)
    s.text((sx(a) + sx(b)) / 2, 49, sub, "sub", "middle", fs2=10.5)
for v in range(0, 501, 100):
    s.add(f'<line x1="{sx(v):.1f}" y1="86" x2="{sx(v):.1f}" y2="92" stroke="{NEU}" stroke-width="1"/>')
    s.text(sx(v), 105, str(v), "small", "middle")
s.text(x1, 120, "µg/g dışkı", "small", "end")
s.text(x0, 142, "Pankreas enzim tedavisi sonucu bozmaz: test insan elastazını ölçer, ilaçtaki domuz enzimini ölçmez.", "small")
s.text(x0, 157, "Çok sulu dışkıda elastaz seyrelir ve sonuç yalancı düşük çıkabilir.", "small")
save(s, "m56k5_elastaz")

# ============================================================ Sekil 4.1 colyak patogenezi
s = SVG(640, 422, "Çölyak hastalığının patogenezi: gliadin, doku transglutaminazı, HLA-DQ2/DQ8 ile sunum, CD4+ T hücresi, IFN-gama, miyofibroblastların metalloproteinazı ve villus atrofisi; B hücreleri ve antikorlar; CD8+ intraepitelyal lenfositler", "k5l")
s.text(300, 24, "LÜMEN", "cap", "middle")
s.add(f'<rect x="10" y="92" width="620" height="40" fill="{ACC}" fill-opacity="0.1" stroke="{NEU}" stroke-opacity="0.3"/>')
for k in range(1, 20):
    x = 10 + k * 31
    s.add(f'<line x1="{x}" y1="92" x2="{x}" y2="132" stroke="{NEU}" stroke-opacity="0.25" stroke-width="1"/>')
s.text(300, 117, "EPİTEL", "cap", "middle")
s.text(300, 162, "LAMİNA PROPRİA", "cap", "middle")
s.box(14, 10, 186, 46, [("Gluten (gliadin)", "title"), ("proteazlara dirençli peptitler", "sub")], fs1=12, fs2=10.5)
s.arrow(107, 56, 107, 150)
s.block(107, 74, 28)
s.text(126, 79, "glutensiz diyet", "magb", fs2=11)
s.box(14, 152, 186, 54, [("Doku transglutaminazı", "title"), ("deamidasyon: glutamin →", "sub"), ("glutamik asit", "sub")], fs1=11.5, fs2=10.5, lh=14)
s.arrow(107, 206, 107, 228)
s.box(14, 230, 186, 46, [("Dendritik hücre", "title"), ("HLA-DQ2/DQ8 ile sunar", "sub")], fs1=11.5, fs2=10.5)
s.arrow(200, 253, 238, 253)
s.box(240, 230, 160, 46, [("CD4+ T hücresi", "title"), ("gliadine özgü", "sub")], fs1=11.5, fs2=10.5)
s.arrow(400, 253, 438, 253)
s.box(440, 230, 190, 46, [("IFN-γ, TNF-α", "title"), ("IL-18, IL-21", "sub")], fs1=11.5, fs2=10.5)
s.arrow(535, 276, 535, 298)
s.box(440, 300, 190, 46, [("Miyofibroblast", "title"), ("matriks metalloproteinazı", "sub")], fs1=11.5, fs2=10.5)
s.arrow(535, 346, 535, 368)
s.box(440, 370, 190, 46, [("Villus atrofisi", "title"), ("kript hiperplazisi (biyopsi)", "sub")], kind="key", fs1=11.5, fs2=10.5)
s.arrow(320, 276, 320, 298)
s.text(327, 291, "yardım", "small")
s.box(240, 300, 160, 46, [("B hücresi", "title"), ("plazma hücresine döner", "sub")], fs1=11.5, fs2=10.5)
s.arrow(320, 346, 320, 368)
s.box(214, 370, 212, 46, [("Anti-tTG IgA, EMA, antigliadin", "title"), ("seroloji: tanıda ölçülür", "sub")], kind="key", fs1=11.5, fs2=10.5)
s.box(420, 8, 210, 66, [("CD8+ intraepitelyal lenfosit", "title"), ("IL-15 ile çoğalır, NKG2D ile", "sub"), ("MICA'yı tanır, enterositi öldürür", "sub")], kind="key", fs1=11.5, fs2=10.5, lh=15)
s.add(f'<circle cx="526" cy="112" r="7" fill="{NEU}" fill-opacity="0.55"/>')
s.arrow(526, 74, 526, 102, CYAN)
s.text(470, 128, "IL-15, MICA", "small", "end")
save(s, "m56k5_colyak")

# ============================================================ Sekil 4.2 Marsh siniflamasi
s = SVG(640, 300, "Marsh-Oberhuber sınıflaması: Marsh 0 normal, 1 intraepitelyal lenfosit artışı, 2 kript hiperplazisi, 3a kısmi, 3b subtotal, 3c total villus atrofisi; Corazza ve Ensari karşılıkları", "k5m")
stages = [("Marsh 0", "normal", 95, 30), ("Marsh 1", "İEL artışı", 95, 30), ("Marsh 2", "kript hiperplazisi", 82, 55),
          ("Marsh 3a", "kısmi atrofi", 48, 62), ("Marsh 3b", "subtotal atrofi", 22, 68), ("Marsh 3c", "total atrofi", 0, 72)]
PX0, PW, GAP, YMM = 110, 84, 2, 205
s.text(100, 20, "Marsh 1992,", "small", "end")
s.text(100, 32, "Oberhuber 1999", "small", "end")
s.text(100, 228, "villus/kript", "small", "end")
vk = ["V/K ≥ 3", "V/K ≥ 3", "V/K < 3", "V/K < 3", "V/K < 3", "V/K = 0"]


def dot(x, y):
    s.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.9" fill="{TXT}" fill-opacity="0.75"/>')


for i, (lab, sub, hv, hc) in enumerate(stages):
    px = PX0 + i * (PW + GAP)
    cx = px + PW / 2
    s.text(cx, 20, lab, "title", "middle", fs1=11.5)
    s.text(cx, 34, sub, "sub", "middle", fs2=10)
    ys = YMM - 6 - hc
    d = f"M{px + 1},{ys}"
    for kind, x in (("c", px + 10), ("v", px + 26), ("c", px + 42), ("v", px + 58), ("c", px + 74)):
        if kind == "c":
            d += f" L{x - 5},{ys} L{x - 5},{ys + hc - 5} A5,5 0 0 0 {x + 5},{ys + hc - 5} L{x + 5},{ys}"
        elif hv > 0:
            d += f" L{x - 10},{ys} L{x - 10},{ys - hv + 10} A10,10 0 0 1 {x + 10},{ys - hv + 10} L{x + 10},{ys}"
            s.add(f'<path d="M{x - 10},{ys} L{x - 10},{ys - hv + 10} A10,10 0 0 1 {x + 10},{ys - hv + 10} L{x + 10},{ys} Z" fill="{ACC}" fill-opacity="0.1"/>')
    d += f" L{px + PW - 1},{ys}"
    s.add(f'<path d="{d}" fill="none" stroke="{CYAN}" stroke-width="1.6"/>')
    s.add(f'<line x1="{px}" y1="{YMM}" x2="{px + PW}" y2="{YMM}" stroke="{NEU}" stroke-opacity="0.6" stroke-width="1.3"/>')
    for vx in (px + 26, px + 58):
        if hv == 0:
            continue
        if i == 0:
            ys_list = [ys - 8, ys - 22]
        else:
            n = max(2, int((hv - 14) / 13))
            ys_list = [ys - 6 - k * (hv - 16) / max(1, n - 1) for k in range(n)]
        for yy in ys_list:
            dot(vx - 7, yy)
            dot(vx + 7, yy)
        if i > 0:
            dot(vx, ys - hv + 5)
    if hv == 0:
        for x in (px + 4, px + 20, px + 30, px + 52, px + 62, px + 81):
            dot(x, ys + 3)
    s.text(cx, 228, vk[i], "body", "middle", fs2=10.5)
s.text(100, 258, "Corazza 2005", "small", "end")
s.text(100, 288, "Ensari 2010", "small", "end")
px_ = lambda i: PX0 + i * (PW + GAP)
for row_y, spans in ((244, [(1, 2, "A"), (3, 4, "B1"), (5, 5, "B2")]), (274, [(1, 1, "Tip 1"), (2, 4, "Tip 2"), (5, 5, "Tip 3")])):
    for a, b, lab in spans:
        xa, xb = px_(a) + 2, px_(b) + PW - 2
        rbar(s, xa, row_y, 20, xb, ACC, 0.2)
        s.text((xa + xb) / 2, row_y + 14, lab, "title", "middle", fs1=11)
save(s, "m56k5_marsh")
