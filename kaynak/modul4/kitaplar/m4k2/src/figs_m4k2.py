import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "build"))
from svglib import SVG, NEU, TXT, CYAN, MAG, FONT, esc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "svg")
os.makedirs(OUT, exist_ok=True)


def save(s, name):
    s.save(os.path.join(OUT, name + ".svg"))


def grid_y(s, x1, x2, y, label=None, lx=None):
    s.add(f'<line x1="{x1}" y1="{y:.1f}" x2="{x2}" y2="{y:.1f}" stroke="{NEU}" stroke-opacity="0.18" stroke-width="1"/>')
    if label is not None:
        s.text(lx if lx is not None else x1 - 6, y + 4, label, "small", anchor="end")


def bar(s, x, w, base, top, color):
    h = base - top
    if h <= 0:
        return
    r = min(4, w / 2, h)
    s.add(f'<path d="M{x:.1f},{base:.1f} L{x:.1f},{top + r:.1f} Q{x:.1f},{top:.1f} {x + r:.1f},{top:.1f} '
          f'L{x + w - r:.1f},{top:.1f} Q{x + w:.1f},{top:.1f} {x + w:.1f},{top + r:.1f} L{x + w:.1f},{base:.1f} Z" fill="{color}"/>')


def smooth(P):
    d = f"M{P[0][0]:.1f},{P[0][1]:.1f}"
    for i in range(1, len(P)):
        x0, y0 = P[i - 1]
        x1, y1 = P[i]
        xm1, ym1 = P[i - 2] if i >= 2 else P[i - 1]
        x2, y2 = P[i + 1] if i + 1 < len(P) else P[i]
        c1 = (x0 + (x1 - xm1) / 6, y0 + (y1 - ym1) / 6)
        c2 = (x1 - (x2 - x0) / 6, y1 - (y2 - y0) / 6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {x1:.1f},{y1:.1f}"
    return d


# =============================================================== 2.1 T_H2 patogenez agi
s = SVG(640, 492, "Alerjik astim patogenezi: TH2 hucresinin orkestra sefi olarak yonettigi hucreler ve ilaclarin hedefleri", "m42a")
s.box(170, 4, 300, 48, [("Alerjen · virüs · kirletici", "title"), ("hava yolu epiteli → alarminler: TSLP, IL-33, IL-25", "sub")], fs1=12.5, fs2=10.5)
s.arrow(320, 52, 320, 78)
s.box(170, 80, 300, 48, [("Dendritik hücre", "title"), ("alerjeni işler, lenf nodunda naif T hücresine sunar", "sub")], fs1=12.5, fs2=10.3)
s.arrow(320, 128, 320, 154)
s.box(170, 156, 300, 52, [("T yardımcı 2 (Tʜ2) hücresi: orkestra şefi", "title"), ("IL-4 · IL-5 · IL-9 · IL-13", "cyanb")], kind="key", fs1=12.5, fs2=11)
s.text(480, 24, "tezepelumab:", "magb", fs2=10)
s.text(480, 37, "anti-TSLP", "mag", fs2=10)
cells = [(4, "B hücresi", ["IL-4, IL-13 ile", "IgE'ye sınıf geçişi"]),
         (164, "Mast hücresi", ["FcεRI'ye IgE bağlanır", "(duyarlanma); IL-9"]),
         (324, "Eozinofil", ["IL-5 (+IL-3, GM-CSF)", "eotaksin ile çağrılır"]),
         (484, "Epitel, goblet, düz kas", ["IL-13: mukus ↑,", "hiperreaktivite"])]
for x, t, sub in cells:
    s.box(x, 250, 146, 58, [(t, "title")] + [(u, "sub") for u in sub], kind="mag" if t == "Eozinofil" else "normal", fs1=12, fs2=10.2, lh=15)
s.path("M220,208 L80,246", NEU)
s.path("M290,208 L240,246", NEU)
s.path("M350,208 L400,246", NEU)
s.path("M420,208 L560,246", NEU)
s.text(118, 226, "IL-4, IL-13", "cyan", anchor="end", fs2=10)
s.text(212, 238, "IL-9", "cyan", anchor="end", fs2=10)
s.text(392, 226, "IL-5", "cyan", fs2=10)
s.text(500, 226, "IL-13", "cyan", fs2=10)
s.arrow(151, 279, 162, 279, CYAN)
s.text(157, 322, "IgE", "cyanb", anchor="middle", fs2=10.5)
outs = [(4, 230, "Erken faz (dakikalar)", ["histamin, LTC₄/D₄, PGD₂", "→ bronkospazm, ödem, mukus"], "normal"),
        (246, 232, "Geç faz ve kronik inflamasyon", ["MBP, ECP, EPO, LTC₄", "→ epitel yıkımı, hiperreaktivite"], "mag"),
        (494, 142, "Remodeling (yıllar)", ["fibrozis, düz kas ↑,", "→ kalıcı obstrüksiyon"], "key")]
for x, w, t, sub, k in outs:
    s.box(x, 352, w, 58, [(t, "title")] + [(u, "sub") for u in sub], kind=k, fs1=11.8, fs2=10.2, lh=15)
s.path("M240,308 L150,348", NEU)
s.path("M400,308 L380,348", NEU)
s.path("M560,308 L566,348", NEU)
s.arrow(479, 381, 492, 381)
s.text(4, 432, "İlaçların hedefleri:", "cap")
tg = ["omalizumab → serbest IgE · mepolizumab, reslizumab → IL-5 · benralizumab → IL-5 reseptörü",
      "dupilumab → IL-4Rα (IL-4 ve IL-13) · montelukast → LTD₄ reseptörü (CysLT₁) · β₂ agonist → bronkospazm",
      "inhale kortikosteroid → Tʜ2 sitokinleri, eozinofil, mast hücresi göçü: zincirin hemen her halkası"]
for i, t in enumerate(tg):
    s.text(4, 448 + i * 14, t, "mag", fs2=10.2)
save(s, "m4k2_patogenez")

# =============================================================== 2.2 erken ve gec faz yaniti
s = SVG(640, 280, "Alerjen inhalasyonu sonrasi FEV1: erken ve gec faz yaniti", "m42b")
L, R, T, B = 60, 600, 26, 220
X = lambda h: L + (R - L) * h / 10
Y = lambda p: B - (B - T) * (p - 50) / 50
s.add(f'<rect x="{X(0):.1f}" y="{T}" width="{X(2) - X(0):.1f}" height="{B - T}" fill="{CYAN}" fill-opacity="0.07"/>')
s.add(f'<rect x="{X(3.5):.1f}" y="{T}" width="{X(10) - X(3.5):.1f}" height="{B - T}" fill="{MAG}" fill-opacity="0.06"/>')
for p in (60, 70, 80, 90, 100):
    grid_y(s, L, R, Y(p), f"%{p}", L - 6)
s.add(f'<line x1="{L}" y1="{B}" x2="{R}" y2="{B}" stroke="{NEU}" stroke-opacity="0.55" stroke-width="1"/>')
for h in range(0, 11, 2):
    s.text(X(h), B + 15, str(h), "small", anchor="middle")
s.text((L + R) / 2, B + 30, "alerjen inhalasyonundan sonra geçen süre (saat)", "small", anchor="middle")
s.text(14, (T + B) / 2, "FEV₁ (başlangıcın %'si)", "small", anchor="middle", rotate=-90)
pts = [(0, 100), (0.15, 82), (0.4, 70), (0.8, 78), (1.5, 92), (2.5, 96), (3.5, 92), (4.5, 82), (5.5, 74), (6.5, 76), (8, 84), (10, 90)]
s.add(f'<path d="{smooth([(X(h), Y(p)) for h, p in pts])}" fill="none" stroke="{CYAN}" stroke-width="2.4"/>')
s.text(X(1), T + 14, "Erken faz", "cyanb", anchor="middle", fs2=11)
s.text(X(6.75), T + 14, "Geç faz", "magb", anchor="middle", fs2=11)
s.text(X(0.55), Y(66) + 2, "15-30 dk'da en derin", "body", fs2=10)
s.text(X(0.55), Y(66) + 15, "1-2 saatte düzelir", "body", fs2=10)
s.text(X(4.3), Y(70) + 4, "3-4 saatte başlar,", "body", fs2=10)
s.text(X(4.3), Y(70) + 17, "4-8 saatte en derin", "body", fs2=10)
s.text(R, Y(57), "β₂ agonist erken fazı geri çevirir · İKS geç fazı önler", "mag", anchor="end", fs2=10.5)
save(s, "m4k2_faz")

# =============================================================== 2.3 akut - kronik - remodeling
s = SVG(640, 214, "Astimda akut inflamasyon, kronik inflamasyon ve remodeling; geri donuslulugun azalmasi", "m42c")
cols = [(6, "Akut inflamasyon", "dakikalar-saatler", ["bronkokonstriksiyon", "ödem", "sekresyon artışı", "öksürük"], "normal"),
        (220, "Kronik inflamasyon", "haftalar-aylar", ["hücre infiltrasyonu", "epitel hasarı", "erken yapısal değişiklikler"], "key"),
        (434, "Remodeling", "yıllar", ["bazal membran kalınlaşması", "düz kas hipertrofisi", "mukus bezi hipertrofisi", "subepitelyal fibrozis"], "mag")]
for x, t, tm, items, k in cols:
    s.box(x, 6, 200, 142, [(t, "title"), (tm, "cyan")] + [("· " + u, "body") for u in items], kind=k, fs1=12.5, fs2=10.5, lh=17, pad_top=22)
s.arrow(206, 77, 218, 77)
s.arrow(420, 77, 432, 77)
s.add(f'<line x1="20" y1="176" x2="610" y2="176" stroke="{MAG}" stroke-width="1.6" marker-end="url(#m42cm)"/>')
s.text(20, 168, "tedaviyle tam geri döner", "cyanb", fs2=10.5)
s.text(320, 168, "tedaviyle büyük ölçüde geri döner", "body", anchor="middle", fs2=10.5)
s.text(610, 168, "kalıcıdır", "magb", anchor="end", fs2=10.5)
s.text(320, 200, "geri dönüşlülük azalır, obstrüksiyon kalıcı hâle gelir", "mag", anchor="middle", fs2=10.5)
save(s, "m4k2_evre")

# =============================================================== 3.1 SFT ornegi (sunumdaki hasta)
s = SVG(640, 268, "Sunumdaki astimli hastanin bronkodilator oncesi ve sonrasi spirometri degerleri, beklenen degerin yuzdesi", "m42d")
L, R, T, B = 60, 620, 44, 214
Y = lambda v: B - (B - T) * v / 100
for v in (25, 50, 75, 100):
    grid_y(s, L, R, Y(v), f"%{v}", L - 8)
s.text(L - 8, B + 4, "%0", "small", anchor="end")
s.add(f'<line x1="{L}" y1="{B}" x2="{R}" y2="{B}" stroke="{NEU}" stroke-opacity="0.55" stroke-width="1"/>')
s.add(f'<line x1="{L}" y1="{Y(80):.1f}" x2="{R}" y2="{Y(80):.1f}" stroke="{NEU}" stroke-width="1.2" stroke-dasharray="5 4"/>')
s.text(R, Y(80) - 5, "%80", "small", anchor="end")
data = [("FEV₁", 58, 82, "2,25 → 3,20 L"), ("FVC", 93, 97, "4,25 → 4,40 L"), ("FEF25-75", 45, 83, "2,1 → 3,9 L/sn"), ("PEF", 65, 98, "5,5 → 8,3 L/sn")]
slot = (R - L) / len(data)
bw, gap = 30, 6
for i, (lab, a, b, raw) in enumerate(data):
    c = L + slot * (i + 0.5)
    x1, x2 = c - bw - gap / 2, c + gap / 2
    bar(s, x1, bw, B, Y(a), MAG)
    bar(s, x2, bw, B, Y(b), CYAN)
    s.text(x1 + bw / 2, Y(a) - 6, str(a), "title", anchor="middle", fs1=11.5)
    s.text(x2 + bw / 2, Y(b) - 6, str(b), "title", anchor="middle", fs1=11.5)
    s.text(c, B + 18, lab, "plain", anchor="middle", fs1=12)
    s.text(c, B + 32, raw, "small", anchor="middle")
s.add(f'<rect x="{L + 4}" y="12" width="12" height="12" rx="2" fill="{MAG}"/>')
s.text(L + 22, 22, "Bronkodilatör öncesi", "body", fs2=11)
s.add(f'<rect x="{L + 170}" y="12" width="12" height="12" rx="2" fill="{CYAN}"/>')
s.text(L + 188, 22, "400 µg salbutamol sonrası", "body", fs2=11)
s.text(R, 22, "beklenen değerin %'si", "small", anchor="end")
save(s, "m4k2_sft")

# =============================================================== 3.2 PEF gunlugu (ornek)
s = SVG(640, 262, "Ornek PEF gunlugu: sabah ve aksam olcumleri ve gunluk degiskenlik", "m42e")
L, R, T, B = 60, 600, 30, 210
lo, hi = 250, 500
X = lambda d: L + (R - L) * (d - 1) / 13
Y = lambda v: B - (B - T) * (v - lo) / (hi - lo)
for v in (300, 350, 400, 450, 500):
    grid_y(s, L, R, Y(v), str(v), L - 6)
s.text(L - 6, B + 4, str(lo), "small", anchor="end")
s.add(f'<line x1="{L}" y1="{B}" x2="{R}" y2="{B}" stroke="{NEU}" stroke-opacity="0.55" stroke-width="1"/>')
for d in range(1, 15):
    s.text(X(d), B + 15, str(d), "small", anchor="middle")
s.text((L + R) / 2, B + 30, "gün", "small", anchor="middle")
s.text(14, (T + B) / 2, "PEF (L/dk)", "small", anchor="middle", rotate=-90)
morn = [330, 340, 320, 350, 310, 335, 345, 325, 340, 330, 315, 350, 335, 320]
eve = [420, 430, 425, 440, 415, 430, 435, 420, 445, 425, 430, 440, 425, 420]
for vals, col in ((eve, CYAN), (morn, MAG)):
    pts = " ".join(f"{X(i + 1):.1f},{Y(v):.1f}" for i, v in enumerate(vals))
    s.add(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2" stroke-linejoin="round"/>')
    for i, v in enumerate(vals):
        s.add(f'<circle cx="{X(i + 1):.1f}" cy="{Y(v):.1f}" r="3.5" fill="{col}" stroke="#f3f2f2" stroke-width="1.5"/>')
s.text(X(14) + 8, Y(420) + 4, "akşam", "cyanb", fs2=11)
s.text(X(14) + 8, Y(320) + 4, "sabah", "magb", fs2=11)
s.add(f'<line x1="{X(1):.1f}" y1="{Y(420) + 5:.1f}" x2="{X(1):.1f}" y2="{Y(330) - 5:.1f}" stroke="{NEU}" stroke-width="1" marker-end="url(#m42e)"/>')
s.text(X(1) + 6, Y(375) + 4, "1. gün: (420 − 330) / 375 = %24", "body", fs2=10.5)
s.text(R, 18, "örnek veri · en iyi PEF ≈ 450 L/dk", "small", anchor="end")
save(s, "m4k2_pef")

# =============================================================== 4.1 basamak tedavisi (sunumdaki sema)
s = SVG(640, 330, "Astimda basamakli tedavi: sunumdaki bes basamak", "m42f")
steps = [("1. basamak", ["Gerektiğinde", "hızlı etkili β₂"], ["kontrol edici", "gerekmez"]),
         ("2. basamak", ["Düşük doz İKS"], ["alternatif:", "LTRA"]),
         ("3. basamak", ["Düşük doz İKS", "+ LABA"], ["alternatif:", "orta doz İKS ya da", "düşük doz İKS +", "LTRA / teofilin"]),
         ("4. basamak", ["Orta-yüksek doz", "İKS + LABA"], ["± LTRA ve/veya", "teofilin", "uzman merkeze", "sevk"]),
         ("5. basamak", ["4. basamak", "+ oral KS"], ["ve/veya", "anti-IgE", "(bugün diğer", "biyolojikler de)"])]
base = 254
for i, (t, main, alt) in enumerate(steps):
    x = 6 + i * 126
    h = 92 + i * 34
    y = base - h
    s.box(x, y, 120, h, [], kind="key" if i in (1, 2) else "normal")
    s.text(x + 60, y + 16, t, "cap", anchor="middle")
    for j, m in enumerate(main):
        s.text(x + 60, y + 34 + j * 14, m, "title", anchor="middle", fs1=11.5)
    y2 = y + 34 + len(main) * 14 + 6
    for j, a in enumerate(alt):
        s.text(x + 60, y2 + j * 13, a, "sub", anchor="middle", fs2=10)
s.box(6, 262, 624, 28, [("Gerektiğinde hızlı etkili β₂ agonist (semptom giderici): bütün basamaklarda", "body")], fs1=11, fs2=10.8, fill="white")
s.box(6, 296, 624, 28, [("Hasta eğitimi ve çevresel kontrol (tetikleyicilerden kaçınma): bütün basamaklarda", "body")], fs1=11, fs2=10.8, fill="white")
s.add(f'<path d="M40,66 L360,40" fill="none" stroke="{CYAN}" stroke-width="1.4" marker-end="url(#m42fc)"/>')
s.text(40, 22, "kontrol yoksa basamak artır", "cyanb", fs2=10.5)
s.text(40, 36, "3 ay kontrolde kalırsa azalt", "cyan", fs2=10.5)
save(s, "m4k2_basamak")
print("ok")
