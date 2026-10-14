import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "build"))
from svglib import SVG, NEU, TXT, CYAN, MAG, FONT, esc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "svg")
os.makedirs(OUT, exist_ok=True)


def save(s, name):
    s.save(os.path.join(OUT, name + ".svg"))


def blockbar(s, x, y, horizontal=True, length=22):
    if horizontal:
        s.add(f'<line x1="{x - length / 2}" y1="{y}" x2="{x + length / 2}" y2="{y}" stroke="{MAG}" stroke-width="3"/>')
    else:
        s.add(f'<line x1="{x}" y1="{y - length / 2}" x2="{x}" y2="{y + length / 2}" stroke="{MAG}" stroke-width="3"/>')


def grid_y(s, x1, x2, y, label=None, lx=None):
    s.add(f'<line x1="{x1}" y1="{y:.1f}" x2="{x2}" y2="{y:.1f}" stroke="{NEU}" stroke-opacity="0.18" stroke-width="1"/>')
    if label is not None:
        s.text(lx if lx is not None else x1 - 6, y + 4, label, "small", anchor="end")


# =============================================================== 1.1 bronş düz kası: gevşeme ve kasılma yolları, ilaç hedefleri
s = SVG(640, 486, "Bronş duz kasi hucresinde gevseme ve kasilma yollari ve antiastmatik ilaclarin etki noktalari", "m44a")
# hucre zari
s.add(f'<rect x="4" y="92" width="632" height="390" rx="10" fill="{CYAN}" fill-opacity="0.04" stroke="{NEU}" stroke-opacity="0.35" stroke-width="1.2"/>')
s.text(268, 86, "hücre dışı", "small", anchor="middle")
s.text(268, 106, "hücre içi", "small", anchor="middle")
# ligandlar
s.text(95, 16, "β₂ agonist", "cyanb", anchor="middle", fs2=11)
s.text(95, 29, "salbutamol, formoterol…", "cyan", anchor="middle", fs2=10)
s.text(415, 16, "Asetilkolin", "title", anchor="middle", fs1=11.5)
s.text(415, 29, "(vagus siniri)", "sub", anchor="middle", fs2=10)
s.text(560, 16, "LTC₄, LTD₄", "title", anchor="middle", fs1=11.5)
s.text(560, 29, "(mast, eozinofil)", "sub", anchor="middle", fs2=10)
s.arrow(95, 34, 95, 74, CYAN)
s.arrow(415, 34, 415, 74)
s.arrow(560, 34, 560, 74)
blockbar(s, 415, 54)
blockbar(s, 560, 54)
s.text(402, 51, "antimuskarinik", "magb", anchor="end", fs2=10)
s.text(402, 63, "ipratropium, tiotropium", "mag", anchor="end", fs2=9.6)
s.text(574, 51, "LTRA", "magb", fs2=10)
s.text(574, 63, "montelukast", "mag", fs2=9.6)
# reseptorler
s.box(30, 76, 130, 32, [("β₂ reseptörü", "title")], kind="key", fs1=12)
s.box(360, 76, 110, 32, [("M₃ reseptörü", "title")], fs1=12)
s.box(490, 76, 130, 32, [("CysLT₁ reseptörü", "title")], fs1=12)
s.text(170, 126, "kortikosteroid:", "cyanb", fs2=9.8)
s.text(170, 138, "β₂ reseptör sayısı ↑", "cyan", fs2=9.8)
# sol: gevseme
L = [(122, "Gs proteini", "αs-GTP"), (172, "Adenilil siklaz ↑", ""), (222, "ATP → cAMP ↑", ""), (272, "Protein kinaz A (PKA)", "")]
for y, t, sub in L:
    s.box(30, y, 130, 34, [(t, "title")] + ([(sub, "sub")] if sub else []), fs1=11.6, fs2=10, lh=13)
s.arrow(95, 108, 95, 118, CYAN)
for y in (156, 206, 256):
    s.arrow(95, y, 95, y + 14, CYAN)
s.box(186, 222, 118, 34, [("Fosfodiesteraz", "title"), ("cAMP → AMP", "sub")], fs1=11.6, fs2=10, lh=13)
s.arrow(161, 239, 184, 239)
blockbar(s, 173, 239, False, 20)
s.text(245, 198, "teofilin, aminofilin", "magb", anchor="middle", fs2=10)
s.text(245, 210, "(PDE inhibitörü)", "mag", anchor="middle", fs2=9.6)
s.box(10, 318, 296, 70, [("PKA'nın etkileri", "title"), ("· MLCK fosforillenir, aktivitesi azalır", "body"),
                         ("· Ca²⁺ SR'ye alınır ve hücreden atılır", "body"), ("· K⁺ kanalları açılır → hiperpolarizasyon", "body")],
      align="start", fs1=11.6, fs2=10.3, lh=14.5)
s.arrow(95, 306, 95, 316, CYAN)
s.box(40, 410, 230, 40, [("GEVŞEME", "title"), ("bronkodilatasyon", "sub")], kind="key", fs1=12.5, fs2=10.5)
s.arrow(155, 388, 155, 406, CYAN)
# sag: kasilma
s.path("M415,108 L470,120", NEU)
s.path("M555,108 L520,120", NEU)
R = [(122, "Gq proteini", ""), (172, "Fosfolipaz C → IP₃", ""), (222, "SR'den Ca²⁺ salınır", "hücre içi Ca²⁺ ↑"),
     (272, "Ca²⁺-kalmodulin", "MLCK aktifleşir"), (322, "Miyozin hafif zinciri", "fosforillenir")]
for y, t, sub in R:
    s.box(430, y, 170, 34, [(t, "title")] + ([(sub, "sub")] if sub else []), kind="normal", fs1=11.6, fs2=10, lh=13)
for y in (156, 206, 256, 306):
    s.arrow(515, y, 515, y + 14)
s.box(430, 410, 170, 40, [("KASILMA", "title"), ("bronkokonstriksiyon", "sub")], kind="mag", fs1=12.5, fs2=10.5)
s.arrow(515, 356, 515, 406)
# capraz etkilesim: PKA -| MLCK
s.add(f'<path d="M160,289 L420,289" fill="none" stroke="{CYAN}" stroke-width="1.4" stroke-dasharray="5 4"/>')
s.add(f'<line x1="424" y1="279" x2="424" y2="299" stroke="{CYAN}" stroke-width="2.6"/>')
s.text(330, 283, "PKA, MLCK'yi baskılar", "cyan", anchor="middle", fs2=10)
save(s, "m4k4_kas")

# =============================================================== 5.1 arasidonik asit yolu
s = SVG(640, 432, "Arasidonik asit yolu, aspirine duyarli astim ve ilaclarin etki noktalari", "m44b")
s.box(220, 4, 200, 34, [("Membran fosfolipitleri", "title")], fs1=12)
s.arrow(320, 38, 320, 74)
blockbar(s, 320, 56)
s.text(338, 60, "fosfolipaz A₂", "body", fs2=10.2)
s.text(302, 54, "glukokortikoidler", "magb", anchor="end", fs2=10)
s.text(302, 66, "(lipokortin / anneksin-1)", "mag", anchor="end", fs2=9.6)
s.box(220, 76, 200, 34, [("Araşidonik asit", "title")], kind="key", fs1=12)
s.path("M250,110 L150,142", NEU)
s.path("M390,110 L490,142", NEU)
s.box(40, 144, 220, 34, [("Siklooksijenaz (COX-1, COX-2)", "title")], fs1=11.6)
s.box(380, 144, 220, 34, [("5-lipoksijenaz (+ FLAP)", "title")], fs1=11.6)
blockbar(s, 200, 126, True, 24)
s.text(186, 124, "aspirin, NSAİİ", "magb", anchor="end", fs2=10)
blockbar(s, 440, 126, True, 24)
s.text(456, 124, "zileuton", "magb", fs2=10)
s.arrow(90, 178, 90, 210)
s.arrow(205, 178, 205, 210)
s.box(10, 212, 150, 52, [("PGE₂", "title"), ("bronkodilatör; mast hücresi", "sub"), ("ve 5-LOX freni", "sub")], kind="key", fs1=11.6, fs2=9.8, lh=13)
s.box(170, 212, 110, 52, [("PGD₂", "title"), ("bronko-", "sub"), ("konstriktör", "sub")], fs1=11.6, fs2=9.8, lh=13)
s.arrow(430, 178, 430, 210)
s.arrow(545, 178, 545, 210)
s.box(350, 212, 120, 52, [("LTB₄", "title"), ("nötrofil", "sub"), ("kemotaksisi", "sub")], fs1=11.6, fs2=9.8, lh=13)
s.box(480, 212, 150, 52, [("LTC₄ → LTD₄ → LTE₄", "title"), ("sisteinil lökotrienler", "sub")], fs1=11.2, fs2=9.8, lh=14)
s.arrow(555, 264, 555, 296)
blockbar(s, 555, 280)
s.text(572, 282, "montelukast,", "magb", fs2=10)
s.text(572, 294, "zafirlukast", "magb", fs2=10)
s.box(480, 300, 150, 32, [("CysLT₁ reseptörü", "title")], fs1=11.6)
s.arrow(555, 332, 555, 356)
s.box(400, 358, 230, 54, [("Bronkokonstriksiyon, ödem,", "title"), ("mukus, eozinofil çağrısı,", "title"), ("aşırı duyarlılık", "sub")], kind="mag", fs1=11.4, fs2=10, lh=14)
s.box(10, 300, 370, 112, [("Aspirine duyarlı astım", "magb"),
                          ("1. COX bloke olunca araşidonik asit 5-lipoksijenaz", "body"),
                          ("   yoluna kayar: sisteinil lökotrienler artar", "body"),
                          ("2. PGE₂ azalır: mast hücresi ve 5-LOX üzerindeki", "body"),
                          ("   fren kalkar", "body"),
                          ("Sonuç: aspirinden sonra ağır bronkospazm", "magb")],
      kind="mag", align="start", fs1=11.6, fs2=10.4, lh=15.5, pad_top=20)
s.add(f'<path d="M260,170 C330,195 330,195 376,168" fill="none" stroke="{MAG}" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#m44bm)"/>')
s.text(318, 202, "kayma", "mag", anchor="middle", fs2=10)
save(s, "m4k4_aa")

# =============================================================== 2.1 bronkodilatorlerin etki suresi
s = SVG(640, 320, "Inhale bronkodilatorlerin yaklasik etki sureleri ve etki baslangiclari", "m44c")
L, R, T = 150, 620, 40
rows = [("Salbutamol", 3, 6, "başlangıç: dakikalar", CYAN),
        ("Terbutalin", 3, 6, "başlangıç: dakikalar", CYAN),
        ("İpratropium", 4, 8, "başlangıç: 15-30 dk", MAG),
        ("Formoterol", 12, 12, "başlangıç: 1-3 dk", CYAN),
        ("Salmeterol", 12, 12, "başlangıç: 10-20 dk", CYAN),
        ("İndakaterol", 24, 24, "başlangıç: ~5 dk", CYAN),
        ("Tiotropium", 24, 24, "başlangıç: yavaş", MAG)]
X = lambda h: L + (R - L) * h / 30
for h in (0, 6, 12, 18, 24):
    s.add(f'<line x1="{X(h):.1f}" y1="{T - 6}" x2="{X(h):.1f}" y2="{T + len(rows) * 34 + 2}" stroke="{NEU}" stroke-opacity="0.18"/>')
    s.text(X(h), T - 12, f"{h} sa", "small", anchor="middle")
for i, (name, lo, hi, onset, col) in enumerate(rows):
    y = T + i * 34 + 6
    s.text(L - 10, y + 10, name, "plain", anchor="end", fs1=11.5)
    s.text(L - 10, y + 23, onset, "small", anchor="end")
    s.add(f'<rect x="{L}" y="{y}" width="{X(lo) - L:.1f}" height="18" rx="4" fill="{col}"/>')
    if hi > lo:
        s.add(f'<rect x="{X(lo):.1f}" y="{y}" width="{X(hi) - X(lo):.1f}" height="18" rx="4" fill="{col}" fill-opacity="0.35"/>')
    lab = f"{lo}-{hi} saat" if hi > lo else (f"≥ {lo} saat" if lo == 24 else f"{lo} saat")
    s.text(X(hi) + 6, y + 13, lab, "title", fs1=10.5)
yy = T + len(rows) * 34 + 14
s.add(f'<rect x="{L}" y="{yy}" width="12" height="12" rx="2" fill="{CYAN}"/>')
s.text(L + 18, yy + 10, "β₂ agonist", "body", fs2=10.5)
s.add(f'<rect x="{L + 110}" y="{yy}" width="12" height="12" rx="2" fill="{MAG}"/>')
s.text(L + 128, yy + 10, "antimuskarinik", "body", fs2=10.5)
s.text(R, yy + 10, "açık renk: aralığın üst kısmı", "small", anchor="end")
save(s, "m4k4_sure")

# =============================================================== 3.1 teofilin terapotik penceresi
s = SVG(640, 170, "Teofilin serum duzeyine gore etkiler ve toksisite: dar terapotik indeks", "m44d")
L, R, Y0, H = 30, 610, 50, 30
X = lambda c: L + (R - L) * c / 45
zones = [(0, 5, NEU, 0.10, "etkisiz"), (5, 15, CYAN, 0.55, "hedef aralık"), (15, 20, CYAN, 0.22, "eski üst sınır"),
         (20, 40, MAG, 0.22, "bulantı, kusma, baş ağrısı, taşikardi, uykusuzluk"), (40, 45, MAG, 0.6, "")]
for a, b, col, op, lab in zones:
    s.add(f'<rect x="{X(a):.1f}" y="{Y0}" width="{X(b) - X(a):.1f}" height="{H}" fill="{col}" fill-opacity="{op}"/>')
    if lab:
        s.text((X(a) + X(b)) / 2, Y0 + 19, lab, "body", anchor="middle", fs2=10)
s.add(f'<rect x="{L}" y="{Y0}" width="{R - L}" height="{H}" fill="none" stroke="{NEU}" stroke-opacity="0.5"/>')
for c in (0, 5, 10, 15, 20, 25, 30, 35, 40, 45):
    s.add(f'<line x1="{X(c):.1f}" y1="{Y0 + H}" x2="{X(c):.1f}" y2="{Y0 + H + 5}" stroke="{NEU}" stroke-opacity="0.6"/>')
    s.text(X(c), Y0 + H + 18, str(c), "small", anchor="middle")
s.text((L + R) / 2, Y0 + H + 34, "serum teofilin düzeyi (mg/L = µg/mL)", "small", anchor="middle")
s.text(R, Y0 - 8, "> 40: aritmi, nöbet", "magb", anchor="end", fs2=10.5)
s.text(X(10), Y0 - 8, "bronkodilatasyon", "cyanb", anchor="middle", fs2=10.5)
s.add(f'<line x1="{X(5):.1f}" y1="{Y0 - 3}" x2="{X(15):.1f}" y2="{Y0 - 3}" stroke="{CYAN}" stroke-width="1.5"/>')
s.text(L, 160, "Ciddi toksisite bazen hafif belirtiler olmadan doğrudan aritmi ya da nöbetle başlayabilir.", "mag", fs2=10.2)
save(s, "m4k4_teofilin")
print("ok")
