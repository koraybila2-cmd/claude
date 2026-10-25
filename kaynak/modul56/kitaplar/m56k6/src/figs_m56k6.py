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
    s.add(f'<rect x="{x0:.1f}" y="{y:.1f}" width="{x1 - x0:.1f}" height="{h:.1f}" rx="4" fill="{color}" fill-opacity="{opacity}"/>')


def grid_v(s, x, y0, y1, base=False):
    s.add(f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y1}" stroke="{NEU}" stroke-opacity="{0.45 if base else 0.15}" stroke-width="1"/>')


def darrow(s, x1, y1, x2, y2, color=NEU, width=1.4):
    """kesikli ok: acikta azalan ya da kapanan yol"""
    s.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" stroke-dasharray="4 3" '
          f'stroke-opacity="0.7" marker-end="url(#{s.mid}{s._m(color)})"/>')


def lines(s, x, y, rows, anchor="start", lh=14, fs1=12, fs2=10.5):
    for i, (t, st) in enumerate(rows):
        s.text(x, y + i * lh, t, st, anchor, fs1, fs2)


# ============================================================ Sekil 1.1 aclik evreleri
s = SVG(640, 238, "Açlığın beş evresi: postabsorptif, erken açlık, orta düzey açlık, uzun süreli açlık ve son evre; kan glukozunun kaynağı ve beynin yakıtı", "k6a")
cols = [(100, 195, "Postabsorptif", "yemekten 2-4 saat"), (195, 300, "Erken açlık", "ilk 24 saat"),
        (300, 420, "Orta düzey açlık", "glikojen bitince"), (420, 540, "Uzun süreli açlık", "~20. günden sonra"),
        (540, 630, "Son evre", "yağ bitince")]
for i, (x0, x1, t, sub) in enumerate(cols):
    rbar(s, x0 + 1, 10, 44, x1 - 1, ACC, 0.12 + 0.1 * i)
    s.text((x0 + x1) / 2, 29, t, "title", "middle", fs1=11.5)
    s.text((x0 + x1) / 2, 44, sub, "sub", "middle", fs2=10)
s.text(92, 92, "Kan glukozu", "title", "end", fs1=11)
s.text(92, 140, "Beynin yakıtı", "title", "end", fs1=11)
s.text(92, 190, "Öne çıkan", "title", "end", fs1=11)
for x0, x1, t, op in ((100, 195, "besinler", 0.18), (195, 300, "karaciğer glikojeni", 0.3), (300, 540, "glukoneogenez (40. günde yarıya iner)", 0.45), (540, 630, "protein yıkımı", 0.6)):
    rbar(s, x0 + 1, 74, 28, x1 - 1, ACC, op)
    s.text((x0 + x1) / 2, 92, t, "body", "middle", fs2=10.5)
for x0, x1, t, op in ((100, 300, "glukoz", 0.18), (300, 420, "glukoz, keton artar", 0.35), (420, 540, "çoğu keton cismi", 0.6), (540, 630, "yeniden glukoz", 0.25)):
    rbar(s, x0 + 1, 122, 28, x1 - 1, CYAN, op)
    s.text((x0 + x1) / 2, 140, t, "body", "middle", fs2=10.5)
notes = [["insülin ↑, glikojen", "ve yağ depolanır"], ["glikojenoliz;", "glikojen ~18 saatte", "biter"],
         ["lipoliz, ketogenez;", "Cori ve glukoz-", "alanin döngüleri"], ["kas proteini korunur;", "T3 ↓, asidoz olabilir"],
         ["proteinin yarısı", "gidince ölüm"]]
for (x0, x1, *_), ns in zip(cols, notes):
    lines(s, (x0 + x1) / 2, 178, [(n, "sub") for n in ns], "middle", lh=13, fs2=10)
s.text(100, 230, "Zaman ekseni ölçeksizdir. Evrelerin sınırları sunumdaki tanımlardır.", "small")
save(s, "m56k6_evre")

# ============================================================ Sekil 1.2 3. ve 40. gun yakit
s = SVG(640, 300, "Açlığın 3. ve 40. gününde günlük yakıt kullanımı ve üretimi, gram: beyin glukozu 100 ve 40, beyin keton cismi 50 ve 100, diğer glukoz kullanımı 50 ve 40, lipoliz 180 ve 180, kas proteini yıkımı 75 ve 20, karaciğer glukoz üretimi 150 ve 80, karaciğer keton üretimi 150 ve 150", "k6b")
x0, x1, vmax = 230, 590, 200
sx = lambda v: x0 + (x1 - x0) * v / vmax
for v in (0, 50, 100, 150, 200):
    grid_v(s, sx(v), 40, 270, base=(v == 0))
    s.text(sx(v), 286, f"{v} g", "small", "middle")
rbar(s, x0, 12, 12, x0 + 14, ACC, 0.4)
s.text(x0 + 20, 22, "3. gün", "body", fs2=10.5)
rbar(s, x0 + 80, 12, 12, x0 + 94, ACC, 1)
s.text(x0 + 100, 22, "40. gün", "body", fs2=10.5)
rows = [("Beyin: glukoz", 100, 40), ("Beyin: keton cisimleri", 50, 100), ("Diğer dokular: glukoz", 50, 40),
        ("Yağ dokusu lipolizi", 180, 180), ("Kas proteini yıkımı", 75, 20), ("Karaciğer: glukoz üretimi", 150, 80),
        ("Karaciğer: keton üretimi", 150, 150)]
for i, (t, a, b) in enumerate(rows):
    yc = 54 + i * 32
    s.text(x0 - 10, yc + 6, t, "body", "end", fs2=11)
    hbar(s, x0, yc - 6, 10, sx(a), ACC, 0.4)
    hbar(s, x0, yc + 6, 10, sx(b), ACC, 1)
    s.text(sx(a) + 5, yc + 3, str(a), "small")
    s.text(sx(b) + 5, yc + 15, str(b), "small")
save(s, "m56k6_yakit")

# ============================================================ Sekil 1.3 aclikta karaciger
s = SVG(640, 408, "Açlıkta karaciğer: glikojenoliz, glukoneogenez ve glukoz-6-fosfataz artar; glikojen sentezi, glikoliz, piruvat dehidrogenaz ve pentoz fosfat yolu azalır; yağ asitleri β-oksidasyona ve keton cisimlerine gider", "k6c")
s.box(360, 6, 272, 44, [("Glukagon ↑, insülin ↓", "title"), ("cAMP → protein kinaz A → fosforilasyon", "sub")], fs1=12, fs2=10.5)
B = {"gly": (190, 64, "Glikojen"), "g6p": (190, 136, "Glukoz-6-fosfat"), "f16": (190, 208, "Fruktoz 1,6-bisfosfat"),
     "pep": (190, 280, "Fosfoenolpiruvat"), "pyr": (190, 352, "Piruvat")}
for k, (x, y, t) in B.items():
    s.box(x, y, 120, 34, [(t, "title")], fs1=11)
s.box(440, 136, 100, 34, [("Glukoz", "title")], fs1=11.5, kind="key")
s.arrow(540, 153, 600, 153)
s.text(605, 157, "kana", "small")
s.box(20, 136, 120, 34, [("Pentoz fosfat yolu", "title"), ("NADPH", "sub")], fs1=10.5, fs2=10, lh=12)
s.box(20, 316, 120, 34, [("Oksaloasetat", "title")], fs1=11)
s.box(440, 208, 120, 34, [("Yağ asitleri", "title"), ("yağ dokusundan", "sub")], fs1=11, fs2=10, lh=12)
s.box(440, 280, 120, 34, [("Asetil-CoA", "title")], fs1=11)
s.box(440, 352, 120, 34, [("Keton cisimleri", "title"), ("kana, dokulara", "sub")], fs1=11, fs2=10, lh=12, kind="key")
# glikojen <-> G6P
s.arrow(236, 98, 236, 134, CYAN, True, 1.8)
s.text(228, 120, "glikojen fosforilaz ↑", "cyanb", "end", fs2=10.5)
darrow(s, 264, 134, 264, 100)
s.text(272, 120, "glikojen sentaz ↓", "sub", fs2=10.5)
# G6P -> glukoz, HMP
s.arrow(310, 153, 438, 153, CYAN, True, 1.8)
s.text(374, 146, "glukoz-6-fosfataz ↑", "cyanb", "middle", fs2=10.5)
darrow(s, 190, 153, 142, 153)
s.text(166, 172, "G6PD ↓", "sub", "middle", fs2=10.5)
# G6P <-> F16
darrow(s, 236, 170, 236, 206)
s.text(228, 192, "PFK-1 ↓", "sub", "end", fs2=10.5)
s.arrow(264, 206, 264, 172, CYAN, True, 1.8)
s.text(272, 192, "fruktoz 1,6-bisfosfataz ↑", "cyanb", fs2=10.5)
# F16 <- PEP
s.arrow(250, 278, 250, 244, CYAN, True, 1.8)
s.text(258, 266, "trioz fosfatlar", "small")
# PEP -> PYR
darrow(s, 236, 314, 236, 350)
s.text(228, 338, "piruvat kinaz ↓", "sub", "end", fs2=10.5)
# PYR -> OAA -> PEP
s.path("M190,369 L80,369 L80,352", CYAN, True, 1.8)
s.text(84, 400, "piruvat karboksilaz ↑", "cyanb", "start", fs2=10.5)
s.path("M80,316 L80,297 L188,297", CYAN, True, 1.8)
s.text(86, 290, "PEPCK ↑", "cyanb", fs2=10.5)
# PYR -> AcCoA, FA -> AcCoA -> keton
darrow(s, 310, 362, 438, 302)
s.text(380, 344, "PDH ↓", "sub", "middle", fs2=10.5)
s.arrow(500, 242, 500, 278, CYAN, True, 1.8)
s.text(508, 264, "β-oksidasyon ↑", "cyanb", fs2=10.5)
s.arrow(500, 314, 500, 350, CYAN, True, 1.8)
s.text(508, 336, "ketogenez ↑", "cyanb", fs2=10.5)
s.text(566, 301, "TCA ↓", "sub", fs2=10.5)
s.text(20, 24, "Düz mavi ok: açlıkta artan", "small")
s.text(20, 38, "Kesikli ok: açlıkta azalan", "small")
save(s, "m56k6_karaciger")

# ============================================================ Sekil 1.4 malonil-CoA anahtari
s = SVG(640, 336, "Malonil-CoA anahtarı: toklukta asetil-CoA karboksilaz aktif, malonil-CoA yüksek, yağ asidi sentezlenir ve CPT-1 baskılanır; açlıkta ACC fosforillenip kapanır, malonil-CoA düşer, CPT-1 açılır ve β-oksidasyon artar", "k6d")
for px, head, hormon, acc, mal, top_box, bottom_box, fed in (
        (10, "TOKLUK", ("İnsülin ↑", "sitrat ↑"), ("Asetil-CoA karboksilaz", "aktif: defosforile, sitratla uyarılmış"), "Malonil-CoA ↑",
         ("Yağ asidi sentezi", "trigliserit → VLDL"), ("CPT-1 baskılanır", "yağ asidi mitokondriye", "giremez, yakılmaz"), True),
        (330, "AÇLIK", ("Glukagon ↑, AMP ↑", "AMPK ve PKA"), ("Asetil-CoA karboksilaz", "inaktif: fosforile"), "Malonil-CoA ↓",
         ("Yağ asidi sentezi durur", ""), ("CPT-1 serbest", "açil-karnitin", "mitokondriye girer"), False)):
    s.text(px + 150, 20, head, "cap", "middle")
    s.box(px, 30, 300, 40, [(hormon[0], "title"), (hormon[1], "sub")], fs1=11.5, fs2=10.5)
    s.arrow(px + 150, 70, px + 150, 90)
    s.box(px, 92, 300, 40, [(acc[0], "title"), (acc[1], "sub")], fs1=11.5, fs2=10.5, kind=("key" if fed else "normal"))
    s.arrow(px + 150, 132, px + 150, 152, CYAN if fed else NEU)
    s.box(px + 75, 154, 150, 32, [(mal, "title")], fs1=12)
    # sol: sentez, sag: CPT-1
    if fed:
        s.arrow(px + 110, 186, px + 70, 218, CYAN, True, 1.6)
    else:
        darrow(s, px + 110, 186, px + 70, 218)
    s.box(px, 220, 140, 46, [(top_box[0], "title")] + ([(top_box[1], "sub")] if top_box[1] else []), fs1=11, fs2=10, lh=14,
          kind=("key" if fed else "normal"))
    if fed:
        s.add(f'<line x1="{px + 190}" y1="186" x2="{px + 222}" y2="214" stroke="{NEU}" stroke-width="1.6"/>')
        s.block(px + 222, 216, 18, NEU)
    s.box(px + 150, 220, 150, 52, [(bottom_box[0], "title"), (bottom_box[1], "sub"), (bottom_box[2], "sub")], fs1=11, fs2=10, lh=14, kind=("normal" if fed else "key"))
    if not fed:
        s.arrow(px + 225, 272, px + 225, 288, CYAN, True, 1.6)
        s.box(px + 130, 288, 170, 40, [("β-oksidasyon ↑", "title"), ("asetil-CoA → keton cisimleri", "sub")], fs1=11.5, fs2=10, kind="key")
s.add(f'<line x1="320" y1="14" x2="320" y2="330" stroke="{NEU}" stroke-opacity="0.25" stroke-width="1"/>')
lines(s, 10, 296, [("Malonil-CoA hem yağ asidi sentezinin ilk ürünüdür", "small"), ("hem de yeni yapılan yağ asidinin yakılmasını", "small"), ("engeller.", "small")], lh=12)
save(s, "m56k6_malonil")

# ============================================================ Sekil 1.5 keton cisimleri
s = SVG(640, 392, "Keton cisimleri karaciğer mitokondrisinde asetil-CoA'dan HMG-CoA üzerinden yapılır; karaciğer dışı dokularda süksinil-CoA'dan koenzim A alan asetoasetat asetoasetil-CoA'ya ve iki asetil-CoA'ya döner", "k6e")
s.add(f'<rect x="10" y="10" width="300" height="372" rx="6" fill="{ACC}" fill-opacity="0.06" stroke="{NEU}" stroke-opacity="0.3"/>')
s.add(f'<rect x="330" y="10" width="300" height="372" rx="6" fill="{CYAN}" fill-opacity="0.05" stroke="{NEU}" stroke-opacity="0.3"/>')
s.text(20, 28, "KARACİĞER MİTOKONDRİSİ: SENTEZ", "cap")
s.text(340, 28, "KALP, KAS, BEYİN: KULLANIM", "cap")
L = [(40, "Yağ asitleri"), (100, "Asetil-CoA"), (160, "Asetoasetil-CoA"), (220, "HMG-CoA"), (280, "Asetoasetat")]
for y, t in L:
    s.box(60, y, 150, 30, [(t, "title")], fs1=11.5)
for (y0, y1, lab) in ((70, 98, "β-oksidasyon"), (130, 158, "tiyolaz (2 asetil-CoA)"), (190, 218, "HMG-CoA sentaz (hız kısıtlayıcı)"), (250, 278, "HMG-CoA liyaz")):
    s.arrow(135, y0, 135, y1)
    s.text(143, (y0 + y1) / 2 + 4, lab, "sub", fs2=10)
s.box(20, 338, 125, 34, [("Aseton", "title"), ("nefesle atılır", "sub")], fs1=11, fs2=9.5, lh=12)
s.box(170, 338, 125, 34, [("β-Hidroksibütirat", "title")], fs1=11, kind="key")
s.arrow(110, 310, 85, 336)
s.text(16, 326, "kendiliğinden", "small")
s.arrow(160, 310, 220, 336)
s.text(205, 322, "NADH", "small")
s.text(165, 66, "", "small")
# kullanim
R = [(60, "β-Hidroksibütirat"), (130, "Asetoasetat"), (210, "Asetoasetil-CoA"), (290, "2 Asetil-CoA")]
for y, t in R:
    s.box(380, y, 150, 30, [(t, "title")], fs1=11.5)
s.arrow(455, 90, 455, 128)
s.text(463, 112, "NAD+ → NADH", "sub", fs2=10)
s.arrow(455, 160, 455, 208, CYAN, True, 1.8)
s.box(470, 168, 158, 34, [("tioforaz", "cyanb"), ("süksinil-CoA → süksinat", "sub")], kind="key", fs2=10, lh=13)
s.arrow(455, 240, 455, 288)
s.text(463, 266, "tiyolaz", "sub", fs2=10)
s.arrow(455, 320, 455, 334)
s.text(455, 348, "TCA döngüsü → ATP", "title", "middle", fs1=11.5)
s.path("M295,355 L346,355 L346,75 L378,75", NEU, True, 1.4)
s.path("M210,295 L340,295 L340,145 L378,145", NEU, True, 1.4)
s.text(320, 290, "kan", "small", "middle")
s.text(480, 364, "Karaciğerde tioforaz yok:", "cyan", "middle", fs2=10)
s.text(480, 377, "karaciğer keton cisimlerini kullanamaz.", "cyan", "middle", fs2=10)
save(s, "m56k6_keton")

# ============================================================ Sekil 1.6 TPP enzimleri
s = SVG(640, 300, "Tiyamin pirofosfata bağımlı dört enzim: piruvat dehidrogenaz, alfa-ketoglutarat dehidrogenaz, transketolaz, dallı zincirli alfa-keto asit dehidrogenaz", "k6f")
s.box(225, 112, 190, 50, [("Tiyamin pirofosfat", "title"), ("B1 vitamininin koenzim biçimi", "sub")], kind="key", fs1=12.5, fs2=10.5)
E = [(10, 10, "Piruvat dehidrogenaz", "piruvat → asetil-CoA", "glikolizi TCA döngüsüne bağlar"),
     (420, 10, "α-Ketoglutarat dehidrogenaz", "α-KG → süksinil-CoA", "TCA döngüsünün bir basamağı"),
     (10, 194, "Transketolaz", "pentoz fosfat yolu", "oksidatif olmayan kol"),
     (420, 194, "Dallı zincirli α-keto asit", "dehidrogenaz", "valin, lösin, izolösin yıkımı")]
for x, y, t, a, b in E:
    s.box(x, y, 210, 62, [(t, "title"), (a, "body"), (b, "sub")], fs1=11.5, fs2=10.5, lh=15)
for (x1, y1, x2, y2) in ((225, 125, 220, 72), (415, 125, 420, 72), (225, 150, 220, 194), (415, 150, 420, 194)):
    s.arrow(x1, y1, x2, y2, CYAN, True, 1.5)
lines(s, 320, 278, [("Eksiklikte PDH ve α-KGDH yavaşlar: glukozdan ATP üretimi düşer, piruvat laktata kayar.", "small"),
                    ("Karbonhidrat yükü bu enzimlerden geçmesi gereken piruvatı, dolayısıyla tiyamin ihtiyacını artırır.", "small")], "middle", lh=13)
save(s, "m56k6_tpp")

# ============================================================ Sekil 2.1 transaminasyon
s = SVG(640, 272, "Transaminasyon ve oksidatif deaminasyon: amino asit ile alfa-ketoglutarat PLP ile alfa-keto asit ve glutamata dönüşür; glutamat dehidrogenaz NAD+ ile amonyağı serbest bırakır", "k6g")
s.box(10, 30, 130, 34, [("Amino asit", "title")], fs1=11.5)
s.box(10, 86, 130, 34, [("α-Ketoglutarat", "title")], fs1=11.5, kind="key")
s.box(250, 30, 130, 34, [("α-Keto asit", "title")], fs1=11.5)
s.box(250, 86, 130, 34, [("Glutamat", "title")], fs1=11.5, kind="key")
s.arrow(140, 47, 248, 47, NEU, True, 1.6)
s.arrow(140, 103, 248, 103, NEU, True, 1.6)
s.arrow(195, 50, 195, 99, CYAN, True, 1.6)
s.text(203, 80, "–NH2", "cyanb", fs2=11)
s.text(195, 18, "aminotransferaz", "title", "middle", fs1=11)
s.text(195, 140, "koenzim: PLP (B6)", "cyan", "middle", fs2=10.5)
s.text(195, 154, "NAD ya da NADH yok", "sub", "middle", fs2=10.5)
s.box(440, 86, 190, 46, [("Glutamat dehidrogenaz", "title"), ("mitokondri · NAD(P)+ → NAD(P)H", "sub")], fs1=11.5, fs2=10)
s.arrow(380, 103, 438, 103)
s.box(440, 170, 90, 34, [("NH4+", "title")], fs1=12)
s.box(540, 170, 90, 34, [("α-KG", "title"), ("geri döner", "sub")], fs1=11.5, fs2=9.5, lh=12)
s.arrow(500, 132, 485, 168)
s.arrow(570, 132, 585, 168)
s.box(250, 190, 130, 34, [("Aspartat", "title"), ("glutamat + oksaloasetat", "sub")], fs1=11.5, fs2=9.5, lh=12)
s.arrow(315, 120, 315, 188)
s.text(322, 160, "AST", "sub", fs2=10.5)
s.box(250, 234, 380, 30, [("Üre döngüsü: bir azot NH4+'ten, bir azot aspartattan", "title")], fs1=11, kind="key")
s.arrow(485, 204, 485, 232)
s.arrow(315, 224, 315, 232)
save(s, "m56k6_transaminasyon")

# ============================================================ Sekil 2.2 zonasyon
s = SVG(640, 236, "Karaciğer asinüsünde zonasyon: periportal hepatositlerde glutaminaz ve üre döngüsü, perivenöz hepatositlerde glutamin sentetaz; amonyağın sistemik dolaşıma kaçması önlenir", "k6h")
s.box(10, 60, 110, 58, [("Portal alan", "title"), ("v. portae,", "sub"), ("a. hepatica", "sub")], fs1=11.5, fs2=10, lh=13)
s.box(530, 60, 100, 58, [("Santral ven", "title"), ("→ sistemik", "sub"), ("dolaşım", "sub")], fs1=11.5, fs2=10, lh=13)
rbar(s, 130, 70, 38, 440, ACC, 0.25)
rbar(s, 444, 70, 38, 520, ACC, 0.7)
s.text(285, 94, "Periportal hepatositler", "title", "middle", fs1=11.5)
s.text(482, 94, "Perivenöz", "title", "middle", fs1=11)
s.arrow(130, 132, 518, 132)
s.text(324, 148, "kan akımı", "small", "middle")
lines(s, 285, 24, [("glutaminaz + üre döngüsü", "body"), ("yüksek kapasite, düşük afinite", "sub")], "middle", lh=14, fs2=10.5)
lines(s, 482, 24, [("glutamin sentetaz", "body"), ("yüksek afinite", "sub")], "middle", lh=14, fs2=10.5)
pts = [(130 + i * 3.9, 0) for i in range(101)]
d = "M" + " L".join(f"{x:.1f},{176 + 40 * (1 - math.exp(-(x - 130) / 70)):.1f}" for x, _ in pts)
s.add(f'<path d="{d}" fill="none" stroke="{CYAN}" stroke-width="2"/>')
s.text(136, 172, "NH3 derişimi (şematik)", "cyan", fs2=10)
s.text(10, 228, "Çoğu amonyak periportal bölgede üreye çevrilir. Kaçanı perivenöz hücrelerde glutamine bağlanır.", "small")
save(s, "m56k6_zonasyon")

# ============================================================ Sekil 2.3 ure dongusu
s = SVG(640, 392, "Üre döngüsü: mitokondride karbamoil fosfat sentetaz I ve ornitin transkarbamoilaz, sitozolde argininosüksinat sentetaz, liyaz ve arginaz; fumarat sitrik asit döngüsüne bağlanır; N-asetilglutamat CPS I'i aktive eder", "k6i")
s.add(f'<rect x="10" y="40" width="250" height="300" rx="6" fill="{ACC}" fill-opacity="0.07" stroke="{NEU}" stroke-opacity="0.35"/>')
s.text(20, 58, "MİTOKONDRİ", "cap")
s.text(290, 58, "SİTOZOL", "cap")
s.text(160, 84, "NH4+ + HCO3-", "title", "middle", fs1=12)
s.arrow(160, 90, 160, 120)
s.text(168, 109, "CPS I · 2 ATP", "body", fs2=10.5)
s.box(90, 122, 140, 30, [("Karbamoil fosfat", "title")], fs1=11.5)
s.box(18, 162, 92, 52, [("NAG", "title"), ("glutamat +", "sub"), ("asetil-CoA", "sub")], kind="key", fs1=12, fs2=10, lh=13)
s.path("M64,162 L64,104 L156,104", CYAN, True, 1.6)
s.text(70, 98, "+ aktive eder", "cyanb", fs2=10)
s.arrow(160, 152, 160, 266)
s.text(152, 240, "OTC", "body", "end", fs2=10.5)
s.box(180, 182, 74, 30, [("Ornitin", "title")], fs1=11.5)
s.arrow(180, 197, 163, 218)
s.box(90, 268, 140, 30, [("Sitrulin", "title")], fs1=11.5)
s.box(410, 268, 140, 30, [("Argininosüksinat", "title")], fs1=11.5)
s.arrow(230, 283, 408, 283)
s.text(335, 262, "argininosüksinat sentetaz", "body", "middle", fs2=10)
s.text(335, 275, "ATP → AMP + PPi", "sub", "middle", fs2=10)
s.box(300, 324, 80, 30, [("Aspartat", "title")], fs1=11.5)
s.arrow(340, 324, 340, 286)
s.box(410, 150, 140, 30, [("Arginin", "title")], fs1=11.5)
s.arrow(480, 268, 480, 182)
s.text(472, 232, "argininosüksinat liyaz", "body", "end", fs2=10)
s.box(410, 66, 140, 36, [("Üre", "title"), ("kana, böbrekten atılır", "sub")], kind="key", fs1=12, fs2=10, lh=13)
s.arrow(480, 150, 480, 104)
s.text(488, 130, "arginaz", "body", fs2=10.5)
s.arrow(410, 166, 256, 194)
s.text(335, 166, "ornitin geri döner", "small", "middle")
s.box(568, 215, 64, 30, [("Fumarat", "title")], fs1=11)
s.arrow(480, 230, 566, 230)
s.box(560, 286, 72, 44, [("malat →", "body"), ("oksaloasetat", "body")], fs2=10, lh=14)
s.arrow(600, 245, 600, 284)
s.path("M596,330 L596,374 L340,374 L340,356", NEU, True, 1.4)
s.text(468, 368, "transaminasyon: glutamattan amino grubu", "small", "middle")
s.text(607, 270, "TCA", "small")
save(s, "m56k6_ure")
print("ok")
