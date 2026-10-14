import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "build"))
from svglib import SVG, NEU, TXT, CYAN, MAG

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "svg")


def save(s, name):
    s.save(os.path.join(OUT, name + ".svg"))


# =============================================================== patofizyoloji zinciri
s = SVG(640, 530, "Kronik akciger hastaligindan sag ventrikul yetersizligine giden patofizyolojik zincir", "m45a")
s.box(60, 6, 520, 44, [("Kronik akciğer hastalığı", "title"),
                       ("KOAH (en sık) · interstisyel hastalık · kifoskolyoz · uyku apnesi, obezite-hipoventilasyon", "sub")],
      fs1=12, fs2=10.2, lh=15)
for x in (110, 320, 530):
    s.arrow(x, 50, x, 70)
cols = [(15, [("Alveoler hipoksi", "+ hiperkapni, asidoz", "normal"), ("Hipoksik pulmoner", "vazokonstriksiyon", "mag"),
              ("Vasküler yeniden şekillenme", "media hipertrofisi, intima kalınlaşması", "normal")]),
        (225, [("Parenkim yıkımı, fibrozis", "amfizem, interstisyel hastalık", "normal"), ("Kapiller yatağın kaybı", "damarlar basılır, sayıca azalır", "normal")]),
        (435, [("Kronik hipoksemi", "böbrekte eritropoetin ↑", "normal"), ("Polisitemi", "kan viskozitesi ↑, akım yavaşlar", "normal")])]
for x, rows in cols:
    for i, (t, sub, kind) in enumerate(rows):
        y = 72 + i * 64
        s.box(x, y, 190, 44, [(t, "title"), (sub, "sub")], kind=kind, fs1=11.4, fs2=9.9, lh=14)
        if i > 0:
            s.arrow(x + 95, y - 20, x + 95, y - 2)
s.path("M110,244 L110,258 L260,258 L260,270")
s.path("M320,180 L320,270")
s.path("M530,180 L530,258 L380,258 L380,270")
s.box(150, 272, 340, 46, [("Pulmoner vasküler direnç ↑", "title"), ("pulmoner hipertansiyon: ortalama PAB > 25 mmHg (sunum)", "sub")], kind="mag", fs1=12, fs2=10.2, lh=15)
s.arrow(320, 318, 320, 336)
s.box(150, 338, 340, 46, [("Sağ ventrikül ardyükü ↑", "title"), ("akut: dilatasyon (emboli) · kronik: hipertrofi (KOAH)", "sub")], fs1=12, fs2=10.2, lh=15)
s.arrow(320, 384, 320, 402)
s.box(150, 404, 340, 40, [("Sağ ventrikül yetersizliği", "title")], kind="mag", fs1=12.5)
s.path("M250,444 L250,458 L160,458 L160,470")
s.path("M390,444 L390,458 L480,458 L480,470")
s.box(15, 472, 290, 54, [("Sistemik venöz konjesyon", "title"), ("boyun venleri dolgun, hassas hepatomegali,", "sub"), ("asit, periferik ödem", "sub")], fs1=11.6, fs2=10, lh=14)
s.box(335, 472, 290, 54, [("Septum sola itilir", "title"), ("sol ventrikül doluşu ↓ → kalp debisi ↓", "sub"), ("(sol kalp kendisi hasta değildir)", "sub")], fs1=11.6, fs2=10, lh=14)
save(s, "m4k5_patofiz")

# =============================================================== hipoksik pulmoner vazokonstriksiyon
s = SVG(640, 350, "Hipoksiye yanit: sistemik arteriolde vazodilatasyon, pulmoner arteriolde vazokonstriksiyon", "m45b")
s.text(160, 16, "Sistemik arteriol", "title", anchor="middle", fs1=12.5)
s.text(480, 16, "Pulmoner arteriol", "title", anchor="middle", fs1=12.5)
L = [("Doku hipoksisi", "dokuda O₂ ↓", "normal"), ("K⁺ kanalları (KATP) açılır", "NO, adenozin, PGI₂ salınır", "normal"),
     ("Hiperpolarizasyon", "Ca²⁺ girişi ↓", "normal"), ("VAZODİLATASYON", "hipoksik dokuya daha çok kan gider", "key")]
R = [("Alveoler hipoksi", "alveolde O₂ ↓", "normal"), ("O₂'ye duyarlı Kv kanalları kapanır", "K⁺ çıkışı azalır", "normal"),
     ("Depolarizasyon", "L-tipi Ca²⁺ kanalları açılır, Ca²⁺ girer", "normal"), ("VAZOKONSTRİKSİYON", "kan iyi havalanan alveollere yönelir", "mag")]
for x, rows, col in ((15, L, CYAN), (335, R, MAG)):
    for i, (t, sub, kind) in enumerate(rows):
        y = 28 + i * 54
        s.box(x, y, 290, 40, [(t, "title"), (sub, "sub")], kind=kind, fs1=11.4, fs2=9.9, lh=14)
        if i > 0:
            s.arrow(x + 145, y - 14, x + 145, y - 2, col if i == 3 else NEU)
s.arrow(480, 230, 480, 252, MAG)
s.box(15, 254, 610, 90, [("Hipoksi bütün akciğerde ve sürekli olursa (KOAH, yüksek rakım, hipoventilasyon)", "magb"),
                         ("· Bütün pulmoner arterioller birlikte daralır. Yerel V/Q uyumu sağlayan refleks, direnci artıran bir yüke dönüşür.", "body"),
                         ("· HIF-1α aracılığıyla düz kas ve fibroblastlar çoğalır: damar duvarı kalıcı olarak kalınlaşır.", "body"),
                         ("· Sonuç pulmoner hipertansiyondur. Oksijen, bu daralmayı geri çeviren tek tedavidir.", "body")],
      kind="mag", align="start", fs1=11.4, fs2=10.2, lh=17, pad_top=22)
save(s, "m4k5_hpv")

# =============================================================== sag ve sol dolasimda basinclar
s = SVG(640, 214, "Sag ve sol dolasimda normal basinclar ve pulmoner hipertansiyon esigi", "m45c")
L, R = 190, 600
X = lambda v: L + (R - L) * v / 130
for v in (0, 25, 50, 75, 100, 125):
    s.add(f'<line x1="{X(v):.1f}" y1="26" x2="{X(v):.1f}" y2="174" stroke="{NEU}" stroke-opacity="0.16"/>')
    s.text(X(v), 188, str(v), "small", anchor="middle")
s.text((L + R) / 2, 204, "basınç (mmHg)", "small", anchor="middle")
rows = [(30, "Sağ ventrikül (sistolik)", 25, CYAN, "25"), (54, "Sol ventrikül (sistolik)", 120, NEU, "120"),
        (110, "Pulmoner arter (ortalama)", 15, CYAN, "15 (14-18)"), (134, "Aort (ortalama)", 93, NEU, "≈ 93")]
for y, lab, v, col, t in rows:
    s.text(L - 10, y + 13, lab, "plain", anchor="end", fs1=11)
    op = "1" if col == CYAN else "0.45"
    s.add(f'<rect x="{L}" y="{y}" width="{X(v) - L:.1f}" height="18" rx="4" fill="{col}" fill-opacity="{op}"/>')
    if t.startswith("15"):
        s.add(f'<text x="{X(v) - 6:.1f}" y="{y + 13}" text-anchor="end" font-family="var(--font-body)" font-size="10.5" font-weight="700" fill="white">15</text>')
        s.text(X(25) + 8, y + 13, "normal: 14-18", "body", fs2=10.2)
    else:
        s.text(X(v) + 6, y + 13, t, "title", fs1=10.5)
s.text(10, 20, "Ventriküller", "cap")
s.text(10, 100, "Büyük arterler", "cap")
for v, lab, yy in ((20, "> 20: 2022 tanımı", 164), (25, "> 25: sunumdaki eşik", 104)):
    s.add(f'<line x1="{X(v):.1f}" y1="{106}" x2="{X(v):.1f}" y2="{130}" stroke="{MAG}" stroke-width="1.5" stroke-dasharray="4 3"/>')
s.text(X(25) + 4, 102, "PH eşiği: > 25 (sunum), > 20 (2022)", "magb", fs2=9.8)
save(s, "m4k5_basinc")

# =============================================================== P pulmonale ve P mitrale
s = SVG(640, 250, "Normal P dalgasi, P pulmonale ve P mitrale karsilastirmasi", "m45d")
mm = 8
panels = [(10, "Normal P dalgası", "≤ 2,5 mm yükseklik, < 0,12 sn süre"),
          (220, "P pulmonale (DII, DIII, aVF)", "> 2,5 mm, sivri; süre normal"),
          (430, "P mitrale (DII)", "≥ 0,12 sn, çift tepeli (M biçimi)")]
gy0, gh, gw = 28, 120, 200
for px, title, sub in panels:
    # izgara
    for i in range(0, gw // mm + 1):
        x = px + i * mm
        w = "0.9" if i % 5 == 0 else "0.4"
        s.add(f'<line x1="{x}" y1="{gy0}" x2="{x}" y2="{gy0 + gh}" stroke="{MAG}" stroke-opacity="0.22" stroke-width="{w}"/>')
    for j in range(0, gh // mm + 1):
        y = gy0 + j * mm
        w = "0.9" if j % 5 == 0 else "0.4"
        s.add(f'<line x1="{px}" y1="{y}" x2="{px + gw}" y2="{y}" stroke="{MAG}" stroke-opacity="0.22" stroke-width="{w}"/>')
    s.text(px + gw / 2, 18, title, "title", anchor="middle", fs1=11.4)
    s.text(px + gw / 2, gy0 + gh + 18, sub, "body", anchor="middle", fs2=10)
y0 = gy0 + 11 * mm  # izoelektrik hat
def beat(px, pwave, pw):
    x0 = px + 3 * mm
    d = f"M{px},{y0} L{x0},{y0} " + pwave(x0)
    x = x0 + pw + 2 * mm
    d += f"L{x},{y0} L{x + 4},{y0 + 6} L{x + 10},{y0 - 70} L{x + 16},{y0 + 14} L{x + 20},{y0} L{x + 34},{y0} "
    d += f"C{x + 42},{y0 - 22} {x + 56},{y0 - 22} {x + 64},{y0} L{px + gw},{y0}"
    s.add(f'<path d="{d}" fill="none" stroke="{TXT}" stroke-width="2" stroke-linejoin="round"/>')
beat(10, lambda x0: f"C{x0 + 5},{y0 - 15} {x0 + 15},{y0 - 15} {x0 + 20},{y0} ", 20)
beat(220, lambda x0: f"Q{x0 + 7},{y0 - 6} {x0 + 10},{y0 - 30} Q{x0 + 13},{y0 - 6} {x0 + 20},{y0} ", 20)
beat(430, lambda x0: f"C{x0 + 3},{y0 - 16} {x0 + 11},{y0 - 16} {x0 + 15},{y0 - 8} C{x0 + 18},{y0 - 18} {x0 + 28},{y0 - 18} {x0 + 32},{y0} ", 32)
# olcu cizgileri
x0 = 220 + 3 * mm
s.add(f'<line x1="{x0 - 6}" y1="{y0 - 30}" x2="{x0 - 6}" y2="{y0}" stroke="{CYAN}" stroke-width="1.4"/>')
s.text(x0 - 9, y0 - 12, "3,5 mm", "cyanb", anchor="end", fs2=9.6)
x0 = 430 + 3 * mm
s.add(f'<line x1="{x0}" y1="{y0 + 10}" x2="{x0 + 32}" y2="{y0 + 10}" stroke="{CYAN}" stroke-width="1.4"/>')
s.text(x0 + 16, y0 + 24, "4 mm = 0,16 sn", "cyanb", anchor="middle", fs2=9.6)
s.text(325, 192, "sağ atriyum büyümesi: cor pulmonale", "magb", anchor="middle", fs2=10)
s.text(535, 192, "sol atriyum büyümesi: mitral darlık", "body", anchor="middle", fs2=10)
s.text(10, 222, "Izgara: 1 küçük kare = 1 mm = 0,04 sn (25 mm/sn kayıt hızında) ve 0,1 mV.", "small")
s.text(10, 238, "Sağ atriyum depolarizasyonu P dalgasının ilk yarısını oluşturur; sağ atriyum büyüyünce P yükselir, ama uzamaz.", "small")
save(s, "m4k5_p")

# =============================================================== nazal kanul akimi ve FiO2
s = SVG(640, 236, "Nazal kanulle oksijen akim hizi ve yaklasik solunan oksijen orani", "m45e")
L, R, B, T = 60, 470, 186, 20
Y = lambda v: B - (B - T) * v / 50
for v in (0, 10, 20, 30, 40, 50):
    s.add(f'<line x1="{L}" y1="{Y(v):.1f}" x2="{R}" y2="{Y(v):.1f}" stroke="{NEU}" stroke-opacity="0.16"/>')
    s.text(L - 8, Y(v) + 4, f"%{v}", "small", anchor="end")
s.add(f'<line x1="{L}" y1="{Y(21):.1f}" x2="{R}" y2="{Y(21):.1f}" stroke="{NEU}" stroke-width="1.2" stroke-dasharray="4 3"/>')
vals = [(1, 24), (2, 28), (3, 32), (4, 36), (5, 40), (6, 44)]
bw, gap = 46, 22
for i, (f, v) in enumerate(vals):
    x = L + 14 + i * (bw + gap)
    hot = f <= 3
    col, op = (CYAN, "1") if hot else (NEU, "0.4")
    s.add(f'<rect x="{x}" y="{Y(v):.1f}" width="{bw}" height="{B - Y(v):.1f}" rx="4" fill="{col}" fill-opacity="{op}"/>')
    s.text(x + bw / 2, Y(v) - 6, f"%{v}", "title", anchor="middle", fs1=10.5)
    s.text(x + bw / 2, B + 16, f"{f} L/dk", "small", anchor="middle")
s.text((L + R) / 2, B + 32, "nazal kanül akım hızı", "small", anchor="middle")
s.box(486, 20, 148, 92, [("1-3 L/dk", "cyanb"), ("hiperkapnik hastada", "body"), ("uzun süreli tedavi;", "body"), ("hedef SpO₂ %88-92", "body")],
      kind="key", align="start", fs1=11.4, fs2=10, lh=16, pad_top=22)
s.box(486, 122, 148, 64, [("8-10 L/dk", "magb"), ("nazal kanülle", "body"), ("uygulanmaz", "body")],
      kind="mag", align="start", fs1=11.4, fs2=10, lh=16, pad_top=22)
save(s, "m4k5_o2")
print("ok")
