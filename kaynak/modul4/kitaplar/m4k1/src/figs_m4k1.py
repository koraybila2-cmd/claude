import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "build"))
from svglib import SVG, NEU, TXT, CYAN, MAG, FONT, esc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "svg")
os.makedirs(OUT, exist_ok=True)


def save(s, name):
    s.save(os.path.join(OUT, name + ".svg"))


def tr(v, nd=2):
    return f"{v:.{nd}f}".replace(".", ",")


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


# =============================================================== 1.1 Venn: KB, amfizem, astim, obstruksiyon
s = SVG(640, 356, "Kronik bronsit, amfizem, astim ve hava yolu obstruksiyonunun iliskisi; KOAH alani", "m41a")
s.add('<defs><clipPath id="m41clip"><rect x="30" y="125" width="580" height="125"/></clipPath></defs>')
s.add(f'<g opacity="0.16" clip-path="url(#m41clip)"><ellipse cx="235" cy="150" rx="160" ry="80" fill="{CYAN}"/>'
      f'<ellipse cx="405" cy="150" rx="160" ry="80" fill="{CYAN}"/></g>')
s.add(f'<rect x="30" y="125" width="580" height="125" rx="4" fill="none" stroke="{CYAN}" stroke-width="1.6" stroke-dasharray="6 4"/>')
for cx in (235, 405):
    s.add(f'<ellipse cx="{cx}" cy="150" rx="160" ry="80" fill="none" stroke="{NEU}" stroke-opacity="0.75" stroke-width="1.3"/>')
s.add(f'<ellipse cx="320" cy="245" rx="125" ry="58" fill="none" stroke="{MAG}" stroke-width="1.3" stroke-dasharray="3 3"/>')
s.text(36, 22, "Kronik bronşit", "title", fs1=13)
s.text(36, 37, "klinik tanım: ≥ 2 yıl üst üste,", "sub", fs2=10.5)
s.text(36, 50, "yılda ≥ 3 ay öksürük ve balgam", "sub", fs2=10.5)
s.text(604, 22, "Amfizem", "title", anchor="end", fs1=13)
s.text(604, 37, "patolojik tanım: terminal bronşiol", "sub", anchor="end", fs2=10.5)
s.text(604, 50, "distalinde kalıcı genişleme ve yıkım", "sub", anchor="end", fs2=10.5)
s.text(165, 98, "obstrüksiyon", "small", anchor="middle")
s.text(165, 110, "yoksa KOAH değil", "small", anchor="middle")
s.text(475, 98, "obstrüksiyon", "small", anchor="middle")
s.text(475, 110, "yoksa KOAH değil", "small", anchor="middle")
s.text(320, 172, "KOAH", "magb", anchor="middle", fs2=19)
s.add(f'<circle cx="320" cy="200" r="3" fill="{MAG}"/>')
s.add(f'<line x1="317" y1="203" x2="204" y2="284" stroke="{MAG}" stroke-width="1" stroke-opacity="0.8"/>')
s.text(200, 292, "astım-KOAH örtüşmesi", "mag", anchor="end", fs2=10.5)
s.text(456, 282, "Astım", "title", fs1=13)
s.text(456, 297, "değişken, çoğunlukla", "sub", fs2=10.5)
s.text(456, 310, "geri dönüşlü obstrüksiyon", "sub", fs2=10.5)
s.text(36, 330, "- - - kalıcı hava yolu obstrüksiyonu", "cyanb", fs2=10.5)
s.text(36, 344, "(bronkodilatör sonrası FEV₁/FVC < 0,70)", "cyan", fs2=10.5)
save(s, "m4k1_venn")

# =============================================================== 1.2 Sigara OR (Forey 2011), gruplu bar
s = SVG(640, 270, "Sigara icenlerde ve birakanlarda KOAH, kronik bronsit ve amfizem icin olasilik orani (Forey 2011)", "m41b")
L, R, T, B = 60, 620, 44, 220
ymax = 5.0
Y = lambda v: B - (B - T) * v / ymax
for v in range(1, 6):
    grid_y(s, L, R, Y(v), str(v), L - 8)
s.text(L - 8, B + 4, "0", "small", anchor="end")
s.add(f'<line x1="{L}" y1="{B}" x2="{R}" y2="{B}" stroke="{NEU}" stroke-opacity="0.55" stroke-width="1"/>')
s.add(f'<line x1="{L}" y1="{Y(1):.1f}" x2="{R}" y2="{Y(1):.1f}" stroke="{NEU}" stroke-width="1.3" stroke-dasharray="5 4"/>')
s.text(L + (R - L) / 3, Y(1) - 6, "hiç içmemiş = 1", "small", anchor="middle")
groups = [("KOAH", 3.51, 2.35), ("Kronik bronşit", 3.41, 1.63), ("Amfizem", 4.87, 3.52)]
slot = (R - L) / 3
bw, gap = 30, 6
for i, (lab, a, b) in enumerate(groups):
    c = L + slot * (i + 0.5)
    x1 = c - bw - gap / 2
    x2 = c + gap / 2
    bar(s, x1, bw, B, Y(a), CYAN)
    bar(s, x2, bw, B, Y(b), MAG)
    s.text(x1 + bw / 2, Y(a) - 7, tr(a), "title", anchor="middle", fs1=12)
    s.text(x2 + bw / 2, Y(b) - 7, tr(b), "title", anchor="middle", fs1=12)
    s.text(c, B + 20, lab, "plain", anchor="middle", fs1=12)
s.add(f'<rect x="{L + 4}" y="14" width="12" height="12" rx="2" fill="{CYAN}"/>')
s.text(L + 22, 24, "Halen sigara içen", "body", fs2=11)
s.add(f'<rect x="{L + 150}" y="14" width="12" height="12" rx="2" fill="{MAG}"/>')
s.text(L + 168, 24, "Sigarayı bırakmış", "body", fs2=11)
s.text(R, 24, "olasılık oranı (OR)", "small", anchor="end")
save(s, "m4k1_or")

# =============================================================== 1.3 Fletcher-Peto egrileri
s = SVG(640, 300, "Fletcher-Peto egrileri: yasla FEV1 kaybi, duyarli sigara icici ve sigarayi birakanlar", "m41c")
L, R, T, B = 62, 470, 20, 250
X = lambda a: L + (R - L) * (a - 25) / 50
Y = lambda p: B - (B - T) * p / 100
for p in (25, 50, 75, 100):
    grid_y(s, L, R, Y(p), f"%{p}", L - 6)
s.text(L - 6, B + 4, "%0", "small", anchor="end")
s.add(f'<line x1="{L}" y1="{B}" x2="{R}" y2="{B}" stroke="{NEU}" stroke-opacity="0.55" stroke-width="1"/>')
for a in (25, 35, 45, 55, 65, 75):
    s.text(X(a), B + 16, str(a), "small", anchor="middle")
s.text((L + R) / 2, B + 31, "yaş (yıl)", "small", anchor="middle")
s.text(16, (T + B) / 2, "FEV₁ (25 yaştaki değerin %'si)", "small", anchor="middle", rotate=-90)
for p, lab in ((25, "sakatlık (ağır dispne)"), (10, "ölüm")):
    s.add(f'<line x1="{L}" y1="{Y(p):.1f}" x2="{R}" y2="{Y(p):.1f}" stroke="{MAG}" stroke-opacity="0.7" stroke-width="1" stroke-dasharray="4 4"/>')
    s.text(L + 6, Y(p) - 5, lab, "mag", fs2=10)


def curve(pts, color, width=2.2, dash=None):
    P = [(X(a), Y(p)) for a, p in pts]
    d = f"M{P[0][0]:.1f},{P[0][1]:.1f}"
    for i in range(1, len(P)):
        x0, y0 = P[i - 1]
        x1, y1 = P[i]
        # catmull-rom -> bezier
        xm1, ym1 = P[i - 2] if i >= 2 else P[i - 1]
        x2, y2 = P[i + 1] if i + 1 < len(P) else P[i]
        c1 = (x0 + (x1 - xm1) / 6, y0 + (y1 - ym1) / 6)
        c2 = (x1 - (x2 - x0) / 6, y1 - (y2 - y0) / 6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {x1:.1f},{y1:.1f}"
    da = f' stroke-dasharray="{dash}"' if dash else ""
    s.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"{da}/>')


normal = [(25, 100), (35, 96), (45, 91), (55, 85), (65, 78), (75, 70)]
susc = [(25, 100), (35, 93), (45, 82), (55, 66), (65, 43), (70, 28), (75, 12)]
stop45 = [(45, 82), (55, 76), (65, 69), (75, 61)]
stop65 = [(65, 43), (70, 39), (75, 35)]
curve(normal, NEU)
curve(susc, MAG, 2.4)
curve(stop45, CYAN, 2.2, "6 4")
curve(stop65, CYAN, 2.2, "2 4")
for a, p in ((45, 82), (65, 43)):
    s.add(f'<circle cx="{X(a):.1f}" cy="{Y(p):.1f}" r="3.5" fill="{CYAN}"/>')
s.text(R + 8, Y(70) + 4, "Hiç içmemiş ya da", "body", fs2=10.5)
s.text(R + 8, Y(70) + 17, "duyarsız içici", "body", fs2=10.5)
s.text(R + 8, Y(61) + 13, "45 yaşında bırakan", "cyanb", fs2=10.5)
s.text(R + 8, Y(35) + 4, "65 yaşında bırakan", "cyanb", fs2=10.5)
s.text(R + 8, Y(12) + 4, "Duyarlı içici", "magb", fs2=10.5)
s.text(R + 8, Y(12) + 17, "(KOAH gelişen)", "mag", fs2=10.5)
save(s, "m4k1_fletcher")

# =============================================================== 2.1 KOAH gelisimi
s = SVG(640, 410, "KOAH gelisimi: zararli etkenden kalici hava akimi kisitlanmasina", "m41d")
s.box(170, 6, 300, 50, [("İnhale edilen zararlı etkenler", "title"), ("sigara dumanı · biyomas · mesleki toz-gaz · hava kirliliği", "sub")], fs1=12.5, fs2=10.5)
s.arrow(320, 56, 320, 84)
s.box(170, 86, 300, 50, [("Akciğerde kronik inflamasyon", "title"), ("duyarlı kişide normalden abartılı yanıt", "sub")], kind="key", fs1=12.5, fs2=10.5)
s.arrow(320, 136, 320, 172)
s.box(220, 174, 200, 44, [("Akciğer hasarı", "title"), ("doku yıkımı ve yanlış onarım", "sub")], kind="mag", fs1=12.5, fs2=10.5)
s.box(8, 168, 186, 56, [("Koruyucu mekanizmalar", "title"), ("antioksidanlar, antiproteazlar", "sub"), ("(sigara bunları zayıflatır)", "sub")], fs1=12, fs2=10.2, lh=14)
s.box(446, 168, 186, 56, [("Tamir mekanizmaları", "title"), ("onarım bozulunca", "sub"), ("fibrozis gelişir", "sub")], fs1=12, fs2=10.2, lh=14)
s.add(f'<line x1="194" y1="196" x2="216" y2="196" stroke="{CYAN}" stroke-width="1.5" stroke-dasharray="4 3"/>')
s.add(f'<line x1="216" y1="186" x2="216" y2="206" stroke="{CYAN}" stroke-width="2.5"/>')
s.path("M424,196 L442,196", NEU, True, 1.3)
xs = [(10, "Küçük hava yolu hastalığı", ["inflamasyon · peribronşiyal", "fibrozis · mukus tıkacı"]),
      (222, "Parankim yıkımı (amfizem)", ["alveol duvarı kaybı", "elastik geri çekim ↓"]),
      (434, "Mukus hipersekresyonu", ["(kronik bronşit) goblet ↑", "submukozal bez hipertrofisi"])]
for x, t, sub in xs:
    s.box(x, 262, 196, 64, [(t, "title")] + [(u, "sub") for u in sub], fs1=12, fs2=10.3, lh=15)
s.path("M300,218 L108,258", NEU)
s.arrow(320, 218, 320, 258)
s.path("M340,218 L532,258", NEU)
s.box(120, 358, 400, 48, [("Kalıcı ve ilerleyici hava akımı kısıtlanması", "title"), ("hava hapsi · hiperinflasyon · V/Q bozukluğu · hipoksemi", "sub")], kind="key", fs1=12.5, fs2=10.5)
s.path("M108,326 L230,354", NEU)
s.arrow(320, 326, 320, 354)
s.path("M532,326 L410,354", NEU)
save(s, "m4k1_gelisim")

# =============================================================== 2.2 hava hapsi ve hiperinflasyon
s = SVG(640, 432, "Amfizem ve kucuk hava yolu hastaligindan hava hapsi, hiperinflasyon ve dispneye", "m41e")
s.box(10, 6, 300, 46, [("Amfizem", "title"), ("alveol duvarları yıkılır", "sub")], fs1=12.5, fs2=10.5)
s.box(330, 6, 300, 46, [("Küçük hava yolu hastalığı", "title"), ("duvar kalınlaşır, fibrozis, lümende mukus", "sub")], fs1=12.5, fs2=10.5)
r2 = [(10, ["Elastik geri çekim ↓", "ekspirasyonu iten", "basınç azalır"]),
      (220, ["Alveoler bağlantı kaybı", "hava yolu dışarıdan", "açık tutulamaz"]),
      (430, ["Hava yolu direnci ↑", "lümen daralır", "(R ∝ 1/r⁴)"])]
for x, ln in r2:
    s.box(x, 92, 200, 60, [(ln[0], "title"), (ln[1], "sub"), (ln[2], "sub")], fs1=12, fs2=10.3, lh=15)
s.arrow(110, 52, 110, 88)
s.path("M210,52 L300,88", NEU)
s.arrow(530, 52, 530, 88)
s.box(110, 190, 420, 56, [("Ekspiratuvar akım kısıtlanması", "title"), ("zorlu ekspirasyonda küçük hava yolları erken kapanır (dinamik kompresyon)", "sub"), ("FEV₁ ↓ · FEV₁/FVC ↓", "sub")], kind="key", fs1=12.5, fs2=10.3, lh=15)
s.path("M110,152 L200,186", NEU)
s.arrow(320, 152, 320, 186)
s.path("M530,152 L440,186", NEU)
s.box(10, 284, 290, 58, [("Hava hapsi → statik hiperinflasyon", "title"), ("istirahatte de: RV ↑, FRC ↑, TLC ↑", "sub"), ("göğüs fıçı şeklini alır", "sub")], fs1=12, fs2=10.3, lh=15)
s.box(340, 284, 290, 58, [("Dinamik hiperinflasyon", "title"), ("efor, taşipne: ekspirasyon süresi yetmez", "sub"), ("her solukta biraz daha hava kalır, oto-PEEP", "sub")], fs1=12, fs2=10.3, lh=15)
s.path("M250,246 L170,280", NEU)
s.arrow(300, 313, 336, 313)
s.box(110, 378, 420, 50, [("İnspiratuvar kapasite ↓ · diyafram düzleşir · solunum işi ↑", "title"), ("sonuç: dispne ve efor kısıtlılığı", "sub")], kind="mag", fs1=12, fs2=10.5)
s.path("M155,342 L250,374", NEU)
s.path("M485,342 L390,374", NEU)
save(s, "m4k1_hiperinf")

# =============================================================== 3.1 hucre agi
s = SVG(640, 372, "KOAH patogenezinde hucre agi: epitel, makrofaj, notrofil, CD8 T hucresi ve uc sonuc", "m41f")
s.box(220, 4, 200, 40, [("Sigara dumanı, biyomas", "title"), ("oksidanlar ve partiküller", "sub")], fs1=12, fs2=10.3, lh=14)
s.box(60, 76, 220, 52, [("Hava yolu epitel hücresi", "title"), ("TNF-α, IL-1β, GM-CSF, CXCL8", "sub")], fs1=12, fs2=10.3)
s.box(360, 76, 220, 52, [("Alveolar makrofaj (5-10 kat ↑)", "title"), ("TNF-α, CXCL8, CXCL1, LTB4, CCL2", "sub")], kind="key", fs1=12, fs2=10.3)
s.path("M300,44 L190,72", NEU)
s.path("M340,44 L450,72", NEU)
r2 = [(4, "Fibroblast", "epitelden TGF-β", "→ kollajen, CTGF", "normal"),
      (160, "Goblet hücresi", "EGFR uyarısı (TGF-α)", "→ MUC5AC, MUC5B", "normal"),
      (316, "Nötrofil", "CXCL8, CXCL1, LTB4 çeker", "→ elastaz, katepsin G, PR3", "normal"),
      (472, "CD8⁺ Tc1 hücresi", "CXCL9-11 (CXCR3) çeker", "→ perforin, granzim B", "normal")]
for x, t, a, b, k in r2:
    s.box(x, 172, 150, 64, [(t, "title"), (a, "sub"), (b, "sub")], kind=k, fs1=12, fs2=10, lh=15)
s.path("M110,128 L80,168", NEU)
s.text(70, 152, "TGF-β", "cyan", anchor="end", fs2=10)
s.path("M170,128 L230,168", NEU)
s.text(214, 150, "EGFR", "cyan", fs2=10)
s.path("M270,128 L370,168", NEU)
s.path("M410,128 L400,168", NEU)
s.text(330, 146, "CXCL8", "cyan", fs2=10)
s.path("M520,128 L545,168", NEU)
s.text(540, 150, "CXCL9-11", "cyan", fs2=10)
outs = [(40, "Küçük hava yolu fibrozisi", "obstrüktif bronşiolit", "normal"),
        (235, "Mukus hipersekresyonu", "kronik bronşit", "normal"),
        (430, "Alveol duvarı yıkımı", "amfizem", "mag")]
for x, t, sub, k in outs:
    s.box(x, 300, 172, 52, [(t, "title"), (sub, "sub")], kind=k, fs1=12, fs2=10.5)
s.path("M79,236 L110,296", NEU)
s.path("M235,236 L300,296", NEU)
s.path("M370,236 L340,296", NEU)
s.text(350, 258, "elastaz", "small", anchor="end")
s.text(350, 270, "salgıyı uyarır", "small", anchor="end")
s.path("M410,236 L480,296", NEU)
s.path("M547,236 L540,296", NEU)
s.path("M580,96 L632,96 L632,326 L606,326", MAG)
s.text(626, 262, "MMP-9, MMP-12", "mag", anchor="end", fs2=10)
save(s, "m4k1_hucre")

# =============================================================== 3.2 oksidatif stres
s = SVG(640, 306, "KOAH'ta oksidatif stres: kaynaklar, radikal zinciri, antioksidan savunma ve hedefler", "m41g")
s.box(10, 6, 300, 50, [("Dış kaynak", "title"), ("sigara dumanı, biyomas, hava kirliliği", "sub")], fs1=12.5, fs2=10.5)
s.box(330, 6, 300, 50, [("İç kaynak", "title"), ("nötrofil-makrofaj NADPH oksidazı, ksantin oksidaz", "sub")], fs1=12.5, fs2=10.3)
s.box(10, 92, 400, 80, [("Oksidan yükü ↑", "title"), ("O₂•⁻ → (SOD) → H₂O₂ → (Fe²⁺: Fenton) → •OH", "body"),
                        ("NO + O₂•⁻ → peroksinitrit (ONOO⁻)", "body"), ("MPO + H₂O₂ + Cl⁻ → HOCl", "body")],
      kind="key", fs1=12.5, fs2=10.5, lh=16)
s.box(440, 92, 190, 80, [("Antioksidan savunma", "title"), ("SOD, katalaz, GPx", "sub"), ("glutatyon, C ve E vitamini", "sub"),
                         ("KOAH'ta Nrf2 ↓ → savunma ↓", "mag")], fs1=12, fs2=10.2, lh=15)
s.add(f'<line x1="438" y1="132" x2="414" y2="132" stroke="{CYAN}" stroke-width="1.5"/>')
s.add(f'<line x1="414" y1="121" x2="414" y2="143" stroke="{CYAN}" stroke-width="2.5"/>')
s.path("M160,56 L160,88", NEU)
s.path("M480,56 L330,88", NEU)
tg = [(4, "α1-AT ve SLPI oksitlenir", "proteaz üstün gelir", "→ amfizem"),
      (164, "NF-κB aktivasyonu", "IL-8, TNF-α ↑", "→ inflamasyon sürer"),
      (324, "HDAC2 inaktive olur", "peroksinitrit etkisi", "→ steroid direnci"),
      (484, "DNA hasarı, apoptoz", "mukus ↑, silyer hasar", "→ hızlı yaşlanma")]
for x, a, b, c in tg:
    s.box(x, 222, 152, 72, [(a, "title"), (b, "sub"), (c, "sub")], kind="mag" if x == 4 else "normal", fs1=11.6, fs2=10.2, lh=16)
for x in (80, 240, 400, 560):
    s.path(f"M{210 + (x - 320) * 0.45:.0f},172 L{x},218", NEU)
save(s, "m4k1_oksidan")

# =============================================================== 3.3 alfa-1 antitripsin genotipleri
s = SVG(640, 276, "Alfa-1 antitripsin genotiplerine gore yaklasik serum duzeyi ve koruyucu esik", "m41h")
L, R, T, B = 60, 620, 46, 228
Y = lambda v: B - (B - T) * v / 100
for v in (25, 50, 75, 100):
    grid_y(s, L, R, Y(v), f"%{v}", L - 8)
s.text(L - 8, B + 4, "%0", "small", anchor="end")
s.add(f'<line x1="{L}" y1="{B}" x2="{R}" y2="{B}" stroke="{NEU}" stroke-opacity="0.55" stroke-width="1"/>')
data = [("PiMM", 100, "100"), ("PiMS", 80, "~80"), ("PiMZ", 60, "~60"), ("PiSS", 60, "~60"), ("PiSZ", 40, "~40"), ("PiZZ", 15, "10-15"), ("Null", 0, "0")]
slot = (R - L) / len(data)
for i, (lab, v, vl) in enumerate(data):
    c = L + slot * (i + 0.5)
    bar(s, c - 15, 30, B, Y(v), CYAN)
    s.text(c, Y(v) - 7, vl, "title", anchor="middle", fs1=11.5)
    s.text(c, B + 18, lab, "plain", anchor="middle", fs1=11.5)
yt = Y(35)
s.add(f'<line x1="{L}" y1="{yt:.1f}" x2="{R}" y2="{yt:.1f}" stroke="{MAG}" stroke-width="1.4" stroke-dasharray="6 4"/>')
s.text(R, 16, "- - - koruyucu eşik ≈ 11 µmol/L (normalin ~%35'i)", "magb", anchor="end", fs2=10.5)
s.text(L - 30, 16, "serum α1-AT düzeyi (PiMM = %100)", "small")
save(s, "m4k1_a1at")

# =============================================================== 4.1 SFT algoritmasi
s = SVG(640, 384, "Spirometri yorumlama algoritmasi ve GOLD agirlik derecesi", "m41i")
s.box(170, 4, 300, 46, [("1. Test kabul edilebilir mi?", "title"), ("akım-volüm eğrisi ve tekrarlanabilirlik", "sub")], fs1=12.5, fs2=10.5)
s.arrow(320, 50, 320, 78)
s.box(170, 80, 300, 46, [("2. Bronkodilatör sonrası FEV₁/FVC", "title"), ("en önemli tek oran", "sub")], kind="key", fs1=12.5, fs2=10.5)
s.path("M250,126 L165,160", NEU)
s.path("M390,126 L475,160", NEU)
s.box(40, 162, 250, 46, [("≥ 0,70: obstrüksiyon yok", "title"), ("normal ya da restriktif patern", "sub")], fs1=12.5, fs2=10.5)
s.box(350, 162, 250, 46, [("< 0,70: obstrüksiyon var", "title"), ("KOAH tanısı için şart", "sub")], kind="mag", fs1=12.5, fs2=10.5)
s.path("M110,208 L80,240", NEU)
s.path("M220,208 L240,240", NEU)
s.path("M420,208 L400,240", NEU)
s.path("M530,208 L555,240", NEU)
r4 = [(6, 150, ["FVC ≥ %80", "→ normal"]),
      (162, 160, ["FVC < %80", "→ restriksiyon olabilir", "TLC ölç"]),
      (328, 144, ["FVC ≥ %80", "→ saf obstrüksiyon"]),
      (480, 154, ["FVC < %80", "→ miks ya da hava", "hapsi: TLC ölç"])]
for x, w, ln in r4:
    s.box(x, 242, w, 58, [(ln[0], "title")] + [(u, "sub") for u in ln[1:]], fs1=12, fs2=10.3, lh=15)
s.path("M400,300 L440,330", NEU)
s.path("M557,300 L520,330", NEU)
s.box(250, 332, 384, 48, [("3. Ağırlık: FEV₁ (% beklenen)", "title"), ("GOLD 1 ≥ 80 · GOLD 2 50-79 · GOLD 3 30-49 · GOLD 4 < 30", "sub")], kind="key", fs1=12, fs2=10.5)
save(s, "m4k1_sft")

# =============================================================== 4.2 akim-volum halkalari
s = SVG(640, 250, "Akim-volum halkalari: normal, obstruktif ve restriktif patern", "m41j")
panels = [(8, "Normal", ["FEV₁/FVC ≥ 0,70"]),
          (219, "Obstrüktif (KOAH)", ["PEF ↓ · iç bükey (kepçe) iniş", "hacimler sola kayar (hiperinflasyon)"]),
          (430, "Restriktif", ["dar ve uzun halka · hacimler ↓", "FEV₁/FVC normal ya da ↑"])]
for x0, title, notes in panels:
    y0 = 128
    s.add(f'<rect x="{x0}" y="6" width="202" height="238" rx="4" fill="white" stroke="{NEU}" stroke-opacity="0.2"/>')
    s.text(x0 + 101, 24, title, "title", anchor="middle", fs1=12.5)
    s.add(f'<line x1="{x0 + 10}" y1="{y0}" x2="{x0 + 192}" y2="{y0}" stroke="{NEU}" stroke-opacity="0.5" stroke-width="1"/>')
    s.text(x0 + 194, y0 - 5, "hacim →", "small", anchor="end")
    s.text(x0 + 12, 44, "akım", "small")
    if title == "Normal":
        ex = f"M{x0 + 18},{y0} L{x0 + 36},{y0 - 78} L{x0 + 156},{y0}"
        ins = f"M{x0 + 156},{y0} C{x0 + 150},{y0 + 70} {x0 + 24},{y0 + 70} {x0 + 18},{y0}"
    elif title.startswith("Obstr"):
        ex = f"M{x0 + 12},{y0} L{x0 + 26},{y0 - 50} C{x0 + 40},{y0 - 14} {x0 + 90},{y0 - 6} {x0 + 134},{y0}"
        ins = f"M{x0 + 134},{y0} C{x0 + 129},{y0 + 60} {x0 + 17},{y0 + 60} {x0 + 12},{y0}"
    else:
        ex = f"M{x0 + 74},{y0} L{x0 + 86},{y0 - 70} L{x0 + 152},{y0}"
        ins = f"M{x0 + 152},{y0} C{x0 + 149},{y0 + 52} {x0 + 77},{y0 + 52} {x0 + 74},{y0}"
    s.add(f'<path d="{ex}" fill="none" stroke="{CYAN if title == "Normal" else MAG}" stroke-width="2.2" stroke-linejoin="round"/>')
    s.add(f'<path d="{ins}" fill="none" stroke="{CYAN if title == "Normal" else MAG}" stroke-width="2.2"/>')
    s.text(x0 + 192, y0 - 60, "ekspirasyon", "small", anchor="end")
    s.text(x0 + 192, y0 + 62, "inspirasyon", "small", anchor="end")
    for i, n in enumerate(notes):
        s.text(x0 + 101, 214 + i * 14, n, "sub", anchor="middle", fs2=10.2)
save(s, "m4k1_akim")
print("ok")
