import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "build"))
from svglib import SVG, NEU, TXT, CYAN, MAG, FONT, esc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "svg")
os.makedirs(OUT, exist_ok=True)
ACC = "var(--color-accent)"
GRAY = "var(--color-neutral-700)"


def save(s, name):
    s.save(os.path.join(OUT, name + ".svg"))


def vbar(s, x, w, base, top, color, opacity=1):
    h = base - top
    if h <= 0:
        return
    r = min(4, w / 2, h)
    s.add(f'<path d="M{x:.1f},{base:.1f} L{x:.1f},{top + r:.1f} Q{x:.1f},{top:.1f} {x + r:.1f},{top:.1f} '
          f'L{x + w - r:.1f},{top:.1f} Q{x + w:.1f},{top:.1f} {x + w:.1f},{top + r:.1f} L{x + w:.1f},{base:.1f} Z" '
          f'fill="{color}" fill-opacity="{opacity}"/>')


def hbar(s, x0, y, h, x1, color, opacity=1):
    w = x1 - x0
    if w <= 0:
        return
    r = min(4, h / 2, w)
    s.add(f'<path d="M{x0:.1f},{y:.1f} L{x1 - r:.1f},{y:.1f} Q{x1:.1f},{y:.1f} {x1:.1f},{y + r:.1f} '
          f'L{x1:.1f},{y + h - r:.1f} Q{x1:.1f},{y + h:.1f} {x1 - r:.1f},{y + h:.1f} L{x0:.1f},{y + h:.1f} Z" '
          f'fill="{color}" fill-opacity="{opacity}"/>')


def vblock(s, x, y, length=22, color=MAG):
    """yatay bir oku kesen dikey magenta cubuk"""
    s.add(f'<line x1="{x}" y1="{y - length / 2}" x2="{x}" y2="{y + length / 2}" stroke="{color}" stroke-width="2.5"/>')


def grid_v(s, x, y0, y1, base=False):
    s.add(f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y1}" stroke="{NEU}" stroke-opacity="{0.45 if base else 0.15}" stroke-width="1"/>')


def grid_h(s, y, x0, x1, base=False):
    s.add(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{NEU}" stroke-opacity="{0.45 if base else 0.15}" stroke-width="1"/>')


# ============================================================ Sekil 1.1 ABH kategorileri
s = SVG(640, 196, "ABH'nin üç kategorisinin sıklığı: prerenal yüzde 55-60, intrinsik renal yüzde 35-40, postrenal yüzde 5'in altında", "k2a")
x0, x1, vmax = 210, 600, 70
sx = lambda v: x0 + (x1 - x0) * v / vmax
for v in (0, 20, 40, 60):
    grid_v(s, sx(v), 10, 156, base=(v == 0))
    s.text(sx(v), 172, f"%{v}", "small", anchor="middle")
rows = [("Prerenal azotemi", "böbrek sağlam, perfüzyon az", 57.5, "%55-60"),
        ("İntrinsik renal", "bunun %90'ından fazlası ATN", 37.5, "%35-40"),
        ("Postrenal", "idrar yollarının tıkanması", 4, "<%5")]
for i, (t, sub, v, lab) in enumerate(rows):
    yc = 34 + i * 46
    s.text(198, yc - 2, t, "title", anchor="end", fs1=12.5)
    s.text(198, yc + 12, sub, "small", anchor="end")
    hbar(s, x0, yc - 9, 16, sx(v), ACC)
    s.text(sx(v) + 7, yc + 3.5, lab, "body", fs2=11.5)
s.text(x0, 190, "Sunumdaki aralıklar; çubuk aralığın orta noktasını gösterir.", "small")
save(s, "m56k2_kategori")

# ============================================================ Sekil 1.2 prerenal frenler
s = SVG(640, 470, "Prerenal azotemide GFR'yi koruyan iki fren: prostaglandinlerle afferent genişleme, anjiyotensin II ile efferent daralma; NSAİİ ve ACE inhibitörü-ARB bu frenleri kaldırır", "k2b")
s.box(170, 10, 300, 46, [("Etkin dolaşan hacim ↓", "title"), ("hipovolemi, kalp yetmezliği, siroz, sepsis", "sub")])
s.arrow(320, 56, 320, 76)
s.box(170, 80, 300, 46, [("Baroreseptörler daha az gerilir", "title"), ("sempatik sistem, RAAS ve ADH aktive olur", "sub")])
for cx in (115, 320, 525):
    s.path(f"M320,126 L320,138 L{cx},138 L{cx},148")
s.box(20, 152, 190, 54, [("Noradrenalin, ADH, AII", "title"), ("damar daralması,", "sub"), ("mezangial kasılma", "sub")], lh=13)
s.box(225, 152, 190, 54, [("Prostaglandinler, NO ↑", "title"), ("PGE₂ ve PGI₂ böbrekte", "sub"), ("yapılır", "sub")], lh=13)
s.box(430, 152, 190, 54, [("Anjiyotensin II ↑", "title"), ("efferenti afferentten", "sub"), ("daha çok daraltır", "sub")], lh=13)
s.arrow(115, 206, 115, 246)
s.arrow(320, 206, 320, 246)
s.block(320, 226)
s.text(336, 230, "NSAİİ", "magb", fs2=11.5)
s.arrow(525, 206, 525, 246)
s.block(525, 226)
s.text(541, 230, "ACEİ · ARB", "magb", fs2=11.5)
s.box(20, 250, 190, 50, [("GFR düşme eğiliminde", "title"), ("filtrasyon yüzeyi ve akım ↓", "sub")])
s.box(225, 250, 190, 50, [("Afferent arteriol genişler", "title"), ("glomerüle giren kan korunur", "sub")], kind="key")
s.box(430, 250, 190, 50, [("Efferent arteriol daralır", "title"), ("glomerülün çıkışı kısılır", "sub")], kind="key")
s.path("M320,300 L320,316 L400,316 L400,330")
s.path("M525,300 L525,316 L440,316 L440,330")
s.box(225, 334, 395, 48, [("İki fren birlikte: glomerül basıncı ve GFR korunur", "title"),
                          ("plazma akımı azalsa da filtrasyon fraksiyonu artar", "sub")], kind="key")
s.path("M115,300 L115,410")
s.box(20, 414, 600, 46, [("Fren kalkarsa (NSAİİ girişi kapatır, ACEİ-ARB çıkışı açar): glomerül basıncı çöker", "title"),
                         ("hemodinamik ABH gelişir, uzarsa iskemik ATN'ye döner", "sub")], kind="mag", fs1=12)
s.text(127, 360, "frenler bunu", "small")
s.text(127, 372, "dengeler", "small")
save(s, "m56k2_prerenal")

# ============================================================ Sekil 1.3 ATN mekanizmalari
s = SVG(640, 414, "ATN'de GFR'yi düşüren dört mekanizma: tübül tıkanması, geri sızma, tübüloglomerüler geri bildirim ve damar daralması", "k2c")
s.box(170, 10, 300, 46, [("Tübül hücresinde ATP tükenir", "title"), ("iskemi (S3, kalın çıkan kol) ya da toksin (proksimal)", "sub")], fs2=10.5)
s.arrow(320, 56, 320, 76)
s.box(170, 80, 300, 46, [("Na⁺/K⁺-ATPaz durur, polarite kaybolur", "title"), ("hücre şişer, bazal membrandan kopar", "sub")])
s.path("M320,126 L320,138 L165,138 L165,156")
s.path("M320,126 L320,138 L475,138 L475,156")
s.text(20, 150, "TÜBÜL İÇİNDE", "cap")
s.text(620, 150, "DAMARDA", "cap", anchor="end")
L = [("Dökülen hücreler silendir yapar", "lümen tıkanır, tübül basıncı ↑"),
     ("Epitel örtüsü kalkar", "süzüntü kana geri sızar"),
     ("Proksimalde NaCl emilmez", "makula densaya NaCl ↑ → afferent daralır")]
R = [("Endotel hasarı", "endotelin ↑, nitrik oksit ↓"),
     ("Damar daralması, lökosit yapışması", "dış medullada akım durgunlaşır"),
     ("İskemi kendini sürdürür", "yeni tübül hücreleri ölür")]
for i in range(3):
    y = 160 + i * 60
    s.box(20, y, 290, 46, [(L[i][0], "title"), (L[i][1], "sub")])
    s.box(330, y, 290, 46, [(R[i][0], "title"), (R[i][1], "sub")])
    if i < 2:
        s.arrow(165, y + 46, 165, y + 56)
        s.arrow(475, y + 46, 475, y + 56)
s.path("M165,326 L165,338 L300,338 L300,348")
s.path("M475,326 L475,338 L340,338 L340,348")
s.box(120, 352, 400, 52, [("GFR düşer, glomerül sağlam olsa da", "title"),
                          ("idrarda kahverengi granüler silendir, FeNa >%2, izostenüri", "sub")], kind="key")
save(s, "m56k2_atn")

# ============================================================ Sekil 2.1 siklik ve olum orani
s = SVG(640, 268, "ABH'nin sıklığı ve ölüm oranı ortama göre: aralıklar yüzde olarak", "k2d")
x0, x1 = 300, 610
sx = lambda v: x0 + (x1 - x0) * v / 100
for v in (0, 25, 50, 75, 100):
    grid_v(s, sx(v), 14, 238, base=(v == 0))
    s.text(sx(v), 254, f"%{v}", "small", anchor="middle")
groups = [("SIKLIK", [("Genel toplum", 0, 1, "<%1"), ("Hastanede yatanlar", 2, 7, "%2-7"), ("Yoğun bakım", 5, 30, "%5-30")]),
          ("ÖLÜM ORANI", [("Komplike olmayan ABH", 0, 10, "<%5-10"),
                          ("Yoğun bakım, oligürik, diyaliz gereken", 40, 90, "%40-90"),
                          ("Diyaliz gereken oligürik intrinsik ABH", 50, 50, "≈%50")]),
          ("UZUN DÖNEM", [("Son dönem böbrek yetmezliği", 5, 16, "%5-16 (bir seride %13,8)")])]
y = 22
for gname, rows in groups:
    s.text(10, y, gname, "cap")
    y += 18
    for (t, lo, hi, lab) in rows:
        s.text(10, y + 4, t, "body", fs2=11)
        if hi > lo:
            hbar(s, sx(lo), y - 5, 10, sx(hi), ACC)
            if lo > 0:
                s.add(f'<path d="M{sx(lo) + 4:.1f},{y - 5} L{sx(lo):.1f},{y - 5} L{sx(lo):.1f},{y + 5} L{sx(lo) + 4:.1f},{y + 5}" fill="{ACC}"/>')
            tx = sx(hi) + 6
        else:
            s.add(f'<circle cx="{sx(lo):.1f}" cy="{y}" r="5" fill="{ACC}" stroke="white" stroke-width="2"/>')
            tx = sx(lo) + 9
        anchor = "start"
        if tx > 560:
            tx, anchor = sx(lo) - 6, "end"
        s.text(tx, y + 4, lab, "body", anchor=anchor, fs2=10.5)
        y += 22
    y += 8
s.add(f'<circle cx="{sx(13.8):.1f}" cy="{y - 30}" r="3.5" fill="white" stroke="{TXT}" stroke-width="1.2"/>')
save(s, "m56k2_prognoz")

# ============================================================ Sekil 3.1 Turkiye evre 5 etiyoloji
s = SVG(640, 342, "Türkiye'de evre 5 KBH'nin nedenleri, yüzde", "k2e")
data = [("Diyabetes mellitus", 39.04, "39,0", "tip 2: 35,5 · tip 1: 3,6"), ("Hipertansiyon", 24.91, "24,9", ""),
        ("Glomerülonefrit", 5.90, "5,9", ""), ("Polikistik böbrek hastalığı", 4.85, "4,9", ""),
        ("Amiloidoz", 1.89, "1,9", ""), ("Tübülointerstisyel nefrit", 1.45, "1,5", ""),
        ("Obstrüktif nefropati", 1.19, "1,2", ""), ("Renovasküler hastalık", 0.89, "0,9", ""),
        None, ("Nedeni bilinmeyen", 13.15, "13,2", ""), ("Diğer", 7.79, "7,8", "")]
x0, x1, vmax = 200, 600, 45
sx = lambda v: x0 + (x1 - x0) * v / vmax
y = 20
for v in (0, 10, 20, 30, 40):
    grid_v(s, sx(v), 10, 312, base=(v == 0))
    s.text(sx(v), 328, f"%{v}", "small", anchor="middle")
for d in data:
    if d is None:
        s.add(f'<line x1="20" y1="{y - 4}" x2="620" y2="{y - 4}" stroke="{NEU}" stroke-opacity="0.35" stroke-width="1"/>')
        y += 8
        continue
    t, v, lab, sub = d
    gray = t in ("Nedeni bilinmeyen", "Diğer")
    s.text(190, y + 4, t, "body", anchor="end", fs2=11)
    hbar(s, x0, y - 6, 13, sx(v), GRAY if gray else ACC, 0.55 if gray else 1)
    s.text(sx(v) + 6, y + 4, lab, "body", fs2=11)
    if sub:
        s.text(190, y + 17, sub, "small", anchor="end")
        y += 12
    y += 26
save(s, "m56k2_etiyoloji")

# ============================================================ Sekil 3.2 hiperfiltrasyon kisir dongusu
s = SVG(640, 400, "KBH'yi ilerleten kısır döngü: nefron kaybı, hiperfiltrasyon, glomerül hasarı, skleroz ve proteinüri, tübül hasarı; tedavilerin etki noktaları", "k2f")
s.box(200, 10, 240, 48, [("Nefron kaybı", "title"), ("diyabet, GN, hipertansiyon, tıkanıklık", "sub")])
s.box(400, 96, 230, 58, [("Sağlam nefronlarda hiperfiltrasyon", "title"), ("afferent genişler, efferent daralır (AII)", "sub"), ("renin ↑, aldosteron tuz-su tutar", "sub")], fs1=12, lh=14)
s.box(400, 222, 230, 58, [("Glomerül içi basınç ↑", "title"), ("kapiller gerilir, endotel ve", "sub"), ("podosit hasarlanır", "sub")], lh=14)
s.box(200, 322, 240, 58, [("Segmental skleroz, proteinüri", "title"), ("açıkta kalan bazal membran", "sub"), ("Bowman kapsülüne yapışır", "sub")], lh=14)
s.box(10, 222, 230, 58, [("Tübül inflamasyonu", "title"), ("süzülen protein tübülü hasarlar:", "sub"), ("interstisyel fibroz, tübüler atrofi", "sub")], lh=14)
s.path("M440,34 L515,34 L515,92")
s.arrow(515, 154, 515, 218)
s.path("M515,280 L515,351 L444,351")
s.path("M200,351 L125,351 L125,284")
s.path("M125,222 L125,34 L196,34")
vblock(s, 478, 34)
s.text(448, 54, "protein ve tuz kısıtlaması", "magb", fs2=10.5)
s.block(515, 188)
s.text(505, 184, "ACEİ · ARB (efferenti açar)", "magb", anchor="end", fs2=10.5)
s.text(505, 198, "SGLT2i (afferenti daraltır)", "magb", anchor="end", fs2=10.5)
s.text(320, 120, "Kısa vadede uyum başarılıdır:", "small", anchor="middle")
s.text(320, 133, "GFR ve kreatinin korunur,", "small", anchor="middle")
s.text(320, 146, "hasta bir şey hissetmez.", "small", anchor="middle")
s.text(320, 262, "Uzun vadede her tur", "small", anchor="middle")
s.text(320, 275, "yeni nefron kaybıdır.", "small", anchor="middle")
s.block(125, 182)
s.text(143, 178, "bikarbonat (asidoz),", "magb", fs2=10.5)
s.text(143, 192, "proteinürinin azaltılması", "magb", fs2=10.5)
save(s, "m56k2_hiperfiltrasyon")

# ============================================================ Sekil 3.3 kreatinin-GFR egrisi
s = SVG(640, 296, "Serum kreatinini ile GFR arasındaki ters ilişki: kuramsal eğri", "k2g")
X0, X1, Y0, Y1 = 66, 610, 244, 22
gx = lambda g: X0 + (X1 - X0) * (120 - g) / 120
gy = lambda c: Y0 - (Y0 - Y1) * c / 10
s.add(f'<rect x="{X0}" y="{gy(1.3):.1f}" width="{X1 - X0}" height="{gy(0.6) - gy(1.3):.1f}" fill="{ACC}" fill-opacity="0.10"/>')
s.text(X0 + 6, gy(0.6) + 10, "normal kreatinin aralığı (≈0,6-1,3)", "small")
for c in (0, 2, 4, 6, 8, 10):
    grid_h(s, gy(c), X0, X1, base=(c == 0))
    s.text(X0 - 8, gy(c) + 3.5, f"{c}", "small", anchor="end")
for g in (120, 90, 60, 30, 15, 0):
    grid_v(s, gx(g), Y1, Y0, base=(g == 120))
    s.text(gx(g), Y0 + 15, f"{g}", "small", anchor="middle")
for (a, b, lab) in ((120, 90, "G1"), (90, 60, "G2"), (60, 30, "G3"), (30, 15, "G4"), (15, 0, "G5")):
    s.text((gx(a) + gx(b)) / 2, Y1 + 12, lab, "cap", anchor="middle")
pts = []
g = 120.0
while g >= 9.6:
    pts.append((gx(g), gy(96 / g)))
    g -= 0.5
d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
s.add(f'<path d="{d}" fill="none" stroke="{ACC}" stroke-width="2"/>')
for (g, c, lab, dx, dy, anc) in ((120, 0.8, "0,8", 6, -9, "start"), (60, 1.6, "GFR 60: kreatinin yalnızca 1,6", -8, -12, "end"),
                                 (30, 3.2, "3,2", -8, -6, "end"), (15, 6.4, "6,4", -9, -4, "end")):
    s.add(f'<circle cx="{gx(g):.1f}" cy="{gy(c):.1f}" r="4.5" fill="{ACC}" stroke="white" stroke-width="2"/>')
    s.text(gx(g) + dx, gy(c) + dy, lab, "body", anchor=anc, fs2=11)
s.text((X0 + X1) / 2, Y0 + 32, "GFR (mL/dk/1,73 m²) — sağa doğru azalır", "small", anchor="middle")
s.text(18, (Y0 + Y1) / 2, "Serum kreatinini (mg/dL)", "small", anchor="middle", rotate=-90)
save(s, "m56k2_kreatinin")

# ============================================================ Sekil 3.4 mineral-kemik bozuklugu
s = SVG(640, 470, "KBH'de mineral-kemik bozukluğunun gelişme sırası: FGF-23 artışı, kalsitriol azalması, PTH artışı ve en son fosfor artışı; tedavilerin etki noktaları", "k2h")
s.box(190, 10, 260, 46, [("Nefron sayısı azalır", "title"), ("nefron başına fosfat yükü artar", "sub")])
s.arrow(320, 56, 320, 82)
s.block(320, 69)
s.text(340, 73, "fosfat bağlayıcılar, diyet", "magb", fs2=10.5)
s.box(190, 86, 260, 46, [("Osteositler FGF-23 salgılar", "title"), ("ilk ve en erken değişiklik", "sub")], kind="key")
s.path("M320,132 L320,144 L160,144 L160,160")
s.path("M320,132 L320,144 L480,144 L480,160")
s.box(20, 164, 280, 50, [("Tübülde fosfat atılımı ↑", "title"), ("serum fosforu uzun süre normal kalır", "sub")])
s.box(340, 164, 280, 50, [("1α-hidroksilaz baskılanır", "title"), ("kalsitriol ↓ (böbrek dokusu da azalır)", "sub")])
s.arrow(480, 214, 480, 246)
s.block(480, 230)
s.text(500, 234, "kalsitriol, parikalsitol", "magb", fs2=10.5)
s.box(340, 250, 280, 50, [("Barsaktan kalsiyum emilimi ↓", "title"), ("kalsiyum düşme eğiliminde", "sub")])
s.arrow(480, 300, 480, 332)
s.block(480, 316)
s.text(500, 320, "sinakalset (CaSR)", "magb", fs2=10.5)
s.box(340, 336, 280, 50, [("PTH ↑: sekonder hiperparatiroidi", "title"), ("fosfat atılımı ↑, kemikten kalsiyum çekilir", "sub")], kind="key")
s.arrow(160, 214, 160, 332)
s.text(172, 270, "FGF-23 ve PTH", "small")
s.text(172, 283, "uyumu sürdürür", "small")
s.box(20, 336, 280, 50, [("GFR <30: uyum tükenir", "title"), ("fosfor en son yükselir", "sub")], kind="key")
s.path("M160,386 L160,400 L300,400 L300,412")
s.path("M480,386 L480,400 L340,400 L340,412")
s.box(60, 416, 520, 46, [("Kemik ağrısı ve kırık (osteitis fibrosa), vasküler kalsifikasyon, kaşıntı", "title"),
                         ("aylar-yıllar içinde gelişir: KBH'yi ABH'den ayırmaya da yarar", "sub")], fs1=12)
save(s, "m56k2_mkb")

# ============================================================ Sekil 4.1 hiperkalemi
s = SVG(640, 360, "Hiperkalemide EKG'nin ilerleyişi ve acil tedavinin üç basamağı", "k2i")
s.text(20, 18, "EKG'NİN İLERLEYİŞİ (K⁺ YÜKSELDİKÇE)", "cap")
E = [("Sivri T dalgası", "repolarizasyon hızlanır", "normal"), ("PR uzar, P kaybolur", "iletim yavaşlar", "normal"),
     ("QRS genişler", "sodyum kanalları inaktif kalır", "normal"), ("Sinüs dalgası → VF, asistoli", "dakikalar içinde ölüm", "mag")]
for i, (t, sub, k) in enumerate(E):
    y = 28 + i * 80
    s.box(20, y, 250, 50, [(t, "title"), (sub, "sub")], kind=k)
    if i < 3:
        s.arrow(145, y + 50, 145, y + 76)
s.text(300, 18, "ACİL TEDAVİNİN ÜÇ BASAMAĞI", "cap")
T = [("1. Zarı koru: kalsiyum glukonat", "dakikalar içinde etki eder", "K⁺ düzeyini düşürmez, zaman kazandırır", "normal"),
     ("2. Hücre içine sok", "insülin + glukoz, β2-agonist (asidozda bikarbonat)", "etki geçici, vücuttaki toplam K⁺ değişmez", "normal"),
     ("3. Vücuttan at", "diüretik (idrar varsa), K⁺ bağlayıcı, hemodiyaliz", "oligürik hastada hızlı ve kesin tek yol: hemodiyaliz", "key")]
for i, (t, a, b, k) in enumerate(T):
    y = 28 + i * 106
    s.box(300, y, 320, 66, [(t, "title"), (a, "sub"), (b, "sub")], kind=k, lh=15)
    if i < 2:
        s.arrow(460, y + 66, 460, y + 102)
s.text(300, 352, "Soru 4.3: K⁺ >6 ve aritmi → acil hemodiyaliz", "cyan", fs2=11)
save(s, "m56k2_hiperkalemi")

# ============================================================ Sekil 5.1 DN patogenezi
s = SVG(640, 412, "Diyabetik nefropatinin patogenezi: metabolik yol ve hemodinamik yol, tedavilerin etki noktaları", "k2j")
s.box(200, 10, 240, 46, [("Hiperglisemi", "title"), ("glukoz insülinsiz hücrelere dolar", "sub")])
s.arrow(320, 56, 320, 84)
s.block(320, 70)
s.text(340, 74, "glisemik kontrol (HbA1c <%7)", "magb", fs2=10.5)
s.path("M320,84 L320,90 L165,90 L165,110")
s.path("M320,84 L320,90 L475,90 L475,110")
s.text(20, 104, "METABOLİK YOL", "cap")
s.text(620, 104, "HEMODİNAMİK YOL", "cap", anchor="end")
s.box(20, 114, 290, 78, [("Dört yan yol", "title"), ("ileri glikasyon son ürünleri (AGE, RAGE)", "sub"),
                         ("protein kinaz C aktivasyonu", "sub"), ("polyol (NADPH ↓) ve heksozamin yolu", "sub")], lh=15)
s.arrow(165, 192, 165, 212)
s.box(20, 216, 290, 46, [("ROS, TGF-β, büyüme faktörleri ↑", "title"), ("sitokinler, prokoagülan etki", "sub")])
s.arrow(165, 262, 165, 282)
s.box(20, 286, 290, 46, [("Matriks birikir", "title"), ("bazal membran kalınlaşır, mezangium genişler", "sub")])
s.box(330, 114, 290, 46, [("SGLT2 ile glukoz + Na⁺ emilimi ↑", "title"), ("makula densaya daha az NaCl ulaşır", "sub")])
s.arrow(475, 160, 475, 196)
s.block(475, 178)
s.text(495, 182, "SGLT2 inhibitörü", "magb", fs2=10.5)
s.box(330, 200, 290, 46, [("Afferent genişler, efferent daralır", "title"), ("IGF-1, NO, glukagon · intrarenal RAS (AII)", "sub")])
s.arrow(475, 246, 475, 282)
s.block(475, 264)
s.text(495, 268, "ACEİ · ARB (efferent)", "magb", fs2=10.5)
s.box(330, 286, 290, 46, [("Glomerüler hipertansiyon", "title"), ("hiperfiltrasyon: GFR %20 ya da daha fazla ↑", "sub")], kind="key")
s.path("M165,332 L165,344 L300,344 L300,356")
s.path("M475,332 L475,344 L340,344 L340,356")
s.box(120, 360, 400, 46, [("Glomerüloskleroz, Kimmelstiel-Wilson nodülleri", "title"), ("albüminüri → proteinüri → GFR ↓", "sub")], kind="key")
save(s, "m56k2_dn")

# ============================================================ Sekil 5.2 eGFR kaybi
s = SVG(640, 232, "Diyabetik böbrek hastalığında albüminüri durumuna göre yıllık eGFR kaybı, yüzde/yıl", "k2k")
X0, X1, Yb, Yt, vmax = 60, 600, 180, 20, 7
sy = lambda v: Yb - (Yb - Yt) * v / vmax
for v in (0, 2, 4, 6):
    grid_h(s, sy(v), X0, X1, base=(v == 0))
    s.text(X0 - 8, sy(v) + 3.5, f"%{v}", "small", anchor="end")
cats = [("Normoalbüminüri", "<30 mg/gün", 1.2, "%1,2"), ("Mikroalbüminüri", "30-300 mg/gün", 1.7, "%1,7"),
        ("Makroalbüminüri", ">300 mg/gün", 5.7, "%5,7")]
gw = (X1 - X0) / 3
for i, (t, sub, v, lab) in enumerate(cats):
    cx = X0 + gw * (i + 0.5)
    vbar(s, cx - 28, 56, Yb, sy(v), ACC)
    s.text(cx, sy(v) - 7, lab, "body", anchor="middle", fs2=12)
    s.text(cx, Yb + 18, t, "body", anchor="middle", fs2=11.5)
    s.text(cx, Yb + 32, sub, "small", anchor="middle")
s.text(X0, 10, "yıllık eGFR kaybı (%/yıl)", "small")
save(s, "m56k2_egfr")

# ============================================================ Sekil 6.1 nefrotik-nefritik yelpaze
s = SVG(640, 236, "Nefrotik-nefritik yelpaze: podosit hasarıyla proteinüri yapan hastalıklardan inflamasyonla hematüri yapan hastalıklara", "k2l")
s.text(30, 18, "NEFROTİK UÇ", "cap")
s.text(610, 18, "NEFRİTİK UÇ", "cap", anchor="end")
s.text(30, 36, "proteinüri ↑ (>3,5 g/gün)", "cyanb", fs2=11)
s.text(610, 36, "hematüri ↑, GFR ↓", "cyanb", anchor="end", fs2=11)
AX = 84
s.arrow(320, AX, 34, AX, width=1.8)
s.arrow(320, AX, 606, AX, width=1.8)
items = ["Minimal değişiklik", "FSGS", "Membranöz", "Diyabetik nefropati", "MPGN", "Lupus nefriti",
         "IgA nefropatisi", "Postenfeksiyöz GN", "Anti-GBM", "Vaskülit"]
xs = [62, 122, 186, 250, 318, 372, 430, 498, 556, 604]
for i, (t_, x) in enumerate(zip(items, xs)):
    above = (i % 2 == 0)
    s.add(f'<line x1="{x}" y1="{AX - 6 if above else AX}" x2="{x}" y2="{AX if above else AX + 6}" stroke="{NEU}" stroke-width="1.2"/>')
    s.text(x, AX - 11 if above else AX + 22, t_, "body", anchor="end" if i == 9 else "middle", fs2=11)
s.box(20, 126, 285, 72, [("Podosit hasarı", "title"), ("yarık diyafram ve yük bariyeri bozulur", "sub"),
                         ("bazal membran sağlam: kan hücresi geçmez", "sub"), ("ödem, hipoalbüminemi, hiperlipidemi", "sub")], lh=14)
s.box(335, 126, 285, 72, [("Kapiller duvarda inflamasyon", "title"), ("proliferasyon, bazal membran kırılmaları,", "sub"),
                          ("kresent: eritrositler geçer, GFR düşer", "sub"), ("hipertansiyon, oligüri, ödem", "sub")], lh=14)
s.text(320, 222, "ortadaki hastalıklar iki tablonun bulgularını birlikte gösterebilir", "small", anchor="middle")
save(s, "m56k2_yelpaze")

# ============================================================ Sekil 6.2 kompleman yollari
s = SVG(640, 440, "Glomerül hastalıklarında klasik ve alternatif kompleman yolları; C3'te birleşir", "k2m")
s.text(20, 18, "KLASİK YOL", "cap")
s.text(340, 18, "ALTERNATİF YOL", "cap")
s.box(20, 26, 280, 46, [("Antijen-antikor kompleksi", "title"), ("IgG ya da IgM'nin Fc kısmı", "sub")])
s.arrow(160, 72, 160, 92)
s.box(20, 96, 280, 46, [("C1q bağlanır, C1 aktive olur", "title"), ("C4 ve C2'yi keser", "sub")])
s.arrow(160, 142, 160, 162)
s.box(20, 166, 280, 46, [("C3 konvertaz: C4b2a", "title"), ("C4 tüketilir", "sub")], kind="key")
s.box(340, 26, 270, 46, [("C3 kendiliğinden yavaşça yıkılır", "title"), ("plazmada sürekli, az miktarda C3b", "sub")])
s.arrow(475, 72, 475, 92)
s.box(340, 96, 270, 46, [("C3b korunmasız yüzeye tutunur", "title"), ("bakteri, endotoksin, polimerik IgA", "sub")])
s.arrow(475, 142, 475, 162)
s.box(340, 166, 270, 46, [("C3 konvertaz: C3bBb", "title"), ("faktör B bağlanır, faktör D keser", "sub")], kind="key")
s.path("M610,189 L628,189 L628,119 L614,119")
s.text(600, 157, "döngü büyür", "small", anchor="end")
s.text(475, 226, "properdin konvertazı kararlı kılar", "small", anchor="middle")
s.path("M160,212 L160,252 L196,252")
s.path("M475,232 L475,252 L444,252")
s.box(200, 236, 240, 46, [("C3 → C3a + C3b", "title"), ("inflamasyon, opsonizasyon", "sub")], kind="key")
s.arrow(320, 282, 320, 302)
s.box(200, 306, 240, 46, [("C5 konvertaz → C5b-9", "title"), ("membran atak kompleksi, hücre hasarı", "sub")])
s.text(20, 378, "Serumda C3 ↓ ve C4 ↓", "title", fs1=12)
s.text(20, 394, "lupus nefriti, immün kompleks tipi MPGN,", "body", fs2=11)
s.text(20, 408, "kriyoglobulinemi", "body", fs2=11)
s.text(340, 378, "Serumda C3 ↓, C4 normal", "title", fs1=12)
s.text(340, 394, "postenfeksiyöz GN, C3 glomerülopati", "body", fs2=11)
s.text(340, 408, "(C3 nefritik faktör konvertazı yıkılmaz kılar)", "body", fs2=11)
save(s, "m56k2_kompleman")

# ============================================================ Sekil 6.3 NS'de pihtilasma dengesi
s = SVG(640, 312, "Nefrotik sendromda tromboz eğilimi: küçük antikoagülan proteinler idrarla kaybolur, büyük pıhtılaşma proteinleri birikir", "k2n")
s.box(170, 10, 300, 46, [("Glomerül bariyeri bozulur", "title"), ("albümin büyüklüğündeki proteinler süzülür", "sub")])
s.path("M320,56 L320,68 L160,68 L160,84")
s.path("M320,56 L320,68 L480,68 L480,84")
s.box(20, 88, 280, 92, [("İdrarla kaybolur", "title"), ("antitrombin III (≈60 kDa)", "sub"), ("plazminojen: fibrinoliz azalır", "sub"),
                        ("protein C ve S (sunuma göre)", "sub")], lh=16)
s.box(340, 88, 280, 92, [("Birikir: idrara geçemez", "title"), ("fibrinojen (≈340 kDa), faktör V, VIII", "sub"),
                         ("karaciğerde yapım artmıştır", "sub"), ("trombosit agregasyonu, hemokonsantrasyon", "sub")], lh=16)
s.path("M160,180 L160,196 L300,196 L300,210")
s.path("M480,180 L480,196 L340,196 L340,210")
s.box(120, 214, 400, 52, [("Denge pıhtılaşma yönüne kayar", "title"),
                          ("renal ven trombozu (en sık membranöz), DVT, pulmoner emboli", "sub")], kind="key")
s.text(320, 290, "Riski en iyi gösteren: serum albümini (<2-2,5 g/dL'de risk yüksek)", "cyan", anchor="middle", fs2=11)
save(s, "m56k2_koagulasyon")

# ============================================================ Sekil 7.1 birikimlerin yeri
s = SVG(640, 290, "Glomerül kapiller duvarının katmanları ve glomerül hastalıklarında birikimlerin yeri", "k2o")
LT = "var(--color-neutral-700)"
XW0, XW1 = 150, 562
yE0, yE1, yG0, yG1, yP0, yP1 = 50, 60, 66, 88, 88, 108
s.text(XW0 + 2, 24, "Kapiller lümen (kan)", "body", fs2=11)
# mezangium
s.add(f'<rect x="20" y="{yE0}" width="118" height="{yP1 - yE0}" rx="4" fill="{LT}" fill-opacity="0.10" stroke="{NEU}" stroke-opacity="0.35"/>')
s.text(79, yE0 - 6, "mezangium", "small", anchor="middle")
for (cx, cy) in ((46, 68), (68, 84), (94, 66), (112, 88), (58, 98), (88, 96), (118, 74)):
    s.add(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{TXT}"/>')
# endotel (fenestrali)
x = XW0
while x < XW1:
    w = min(26, XW1 - x)
    s.add(f'<rect x="{x}" y="{yE0}" width="{w}" height="{yE1 - yE0}" rx="2" fill="{LT}" fill-opacity="0.30"/>')
    x += w + 5
# GBM
s.add(f'<rect x="{XW0}" y="{yG0}" width="{XW1 - XW0}" height="{yG1 - yG0}" fill="{ACC}" fill-opacity="0.22"/>')
# podosit ayaksi cikintilari: normal (150-498), silinmis (500-562)
x = XW0 + 2
while x < 486:
    s.add(f'<rect x="{x}" y="{yP0 + 1}" width="16" height="{yP1 - yP0 - 1}" rx="6" fill="{LT}" fill-opacity="0.30"/>')
    x += 21
s.add(f'<rect x="500" y="{yP0 + 1}" width="{XW1 - 500}" height="9" rx="4" fill="{LT}" fill-opacity="0.30"/>')
# katman adlari (sagda)
s.text(XW1 + 8, (yE0 + yE1) / 2 + 3.5, "endotel", "small")
s.text(XW1 + 8, (yG0 + yG1) / 2 + 3.5, "GBM", "small")
s.text(XW1 + 8, (yP0 + yP1) / 2 + 3.5, "podosit", "small")
# birikimler
for cx in (172, 186, 200):
    s.add(f'<ellipse cx="{cx}" cy="{(yE1 + yG0) / 2 + 1}" rx="6" ry="3.2" fill="{TXT}"/>')
s.add(f'<rect x="232" y="{yG0 + 8}" width="56" height="6" rx="3" fill="{TXT}"/>')
for cx in (306, 322, 338, 354):
    s.add(f'<circle cx="{cx}" cy="{yG1 + 3}" r="3.2" fill="{TXT}"/>')
    s.add(f'<line x1="{cx + 8}" y1="{yG1}" x2="{cx + 8}" y2="{yG1 + 5}" stroke="{ACC}" stroke-width="2.5"/>')
s.add(f'<path d="M386,{yG1} Q400,{yG1 + 24} 414,{yG1} Z" fill="{TXT}"/>')
s.add(f'<line x1="430" y1="{(yG0 + yG1) / 2}" x2="490" y2="{(yG0 + yG1) / 2}" stroke="{TXT}" stroke-width="3"/>')
# etiketler ve kilavuz cizgileri
LAB = [(79, 1, "Mezangial", "IgA nefropatisi", yP1 + 2),
       (186, 1, "Subendotelyal", "MPGN, lupus nefriti", 66),
       (260, 2, "Bazal membran içi", "dens depozit hastalığı", 82),
       (330, 1, "Subepitelyal, küçük", "membranöz (dikenlerle)", 96),
       (400, 2, "Subepitelyal “hörgüç”", "postenfeksiyöz GN", 104),
       (460, 1, "Lineer", "anti-GBM hastalığı", 80),
       (531, 2, "Birikim yok, silinme", "MDH (ve FSGS)", 100)]
for (x, row, t_, sub, ytop) in LAB:
    yl = 150 if row == 1 else 208
    s.add(f'<line x1="{x}" y1="{ytop}" x2="{x}" y2="{yl - 13}" stroke="{NEU}" stroke-opacity="0.6" stroke-width="0.8"/>')
    s.text(x, yl, t_, "title", anchor="middle", fs1=11.5)
    s.text(x, yl + 14, sub, "body", anchor="middle", fs2=10.5)
s.text(320, 258, "Üstte kan, altta Bowman boşluğu (idrar). Koyu işaretler birikimleri, cyan çizgiler", "small", anchor="middle")
s.text(320, 271, "membranöz nefropatideki “dikenleri” gösterir. Şema ölçeksizdir.", "small", anchor="middle")
save(s, "m56k2_birikim")

print("ok")
