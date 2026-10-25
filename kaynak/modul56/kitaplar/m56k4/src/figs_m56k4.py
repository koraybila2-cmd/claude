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


def vbar(s, x, w, base, top, color, opacity=1):
    h = base - top
    if h <= 0:
        return
    r = min(4, w / 2, h)
    s.add(f'<path d="M{x:.1f},{base:.1f} L{x:.1f},{top + r:.1f} Q{x:.1f},{top:.1f} {x + r:.1f},{top:.1f} '
          f'L{x + w - r:.1f},{top:.1f} Q{x + w:.1f},{top:.1f} {x + w:.1f},{top + r:.1f} L{x + w:.1f},{base:.1f} Z" '
          f'fill="{color}" fill-opacity="{opacity}"/>')


def vblock(s, x, y, length=22, color=MAG):
    s.add(f'<line x1="{x}" y1="{y - length / 2}" x2="{x}" y2="{y + length / 2}" stroke="{color}" stroke-width="2.5"/>')


def grid_v(s, x, y0, y1, base=False):
    s.add(f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y1}" stroke="{NEU}" stroke-opacity="{0.45 if base else 0.15}" stroke-width="1"/>')


def grid_h(s, y, x0, x1, base=False):
    s.add(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{NEU}" stroke-opacity="{0.45 if base else 0.15}" stroke-width="1"/>')


def curve(s, pts, color, width=2, dash=None, opacity=1):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    s.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-opacity="{opacity}" stroke-linejoin="round" stroke-linecap="round"{da}/>')


# ============================================================ Sekil 1.1 dort yaprakli yonca
s = SVG(640, 384, "Dört yapraklı yonca: süt ve süt ürünleri; et, yumurta ve kurubaklagil; sebze ve meyveler; tahıl ve tahıl ürünleri", "k4a")
cx, cy, sz = 320, 190, 114


def heart(angle, op):
    p = (f"M0,-6 C{-0.98 * sz:.1f},{-0.62 * sz:.1f} {-0.66 * sz:.1f},{-1.52 * sz:.1f} 0,{-1.1 * sz:.1f} "
         f"C{0.66 * sz:.1f},{-1.52 * sz:.1f} {0.98 * sz:.1f},{-0.62 * sz:.1f} 0,-6 Z")
    s.add(f'<path d="{p}" transform="translate({cx},{cy}) rotate({angle})" fill="{ACC}" fill-opacity="{op}" '
          f'stroke="{CYAN}" stroke-width="1.5"/>')


leaves = [(0, 0.10, (cx, cy - 99), [("Süt ve", "title"), ("süt ürünleri", "title"), ("süt, yoğurt, peynir", "sub")]),
          (90, 0.18, (cx + 74, cy + 2), [("Et, yumurta,", "title"), ("kurubaklagil", "title"), ("balık, nohut", "sub")]),
          (180, 0.10, (cx, cy + 99), [("Sebze ve", "title"), ("meyveler", "title"), ("taze ve kuru", "sub")]),
          (270, 0.18, (cx - 74, cy + 2), [("Tahıl ve", "title"), ("tahıl ürünleri", "title"), ("ekmek, bulgur", "sub")])]
for ang, op, _, _ in leaves:
    heart(ang, op)
for _, _, (lx, ly), lines in leaves:
    for i, (t, st) in enumerate(lines):
        s.text(lx, ly - 14 + i * 15, t, st, anchor="middle", fs1=12.5, fs2=10.5)
s.add(f'<circle cx="{cx}" cy="{cy}" r="5" fill="{CYAN}"/>')
s.text(cx, 376, "YETERLİ VE DENGELİ BESLENME", "cap", anchor="middle")
s.text(520, 80, "+ su", "title", anchor="middle", fs1=12.5)
s.text(520, 95, "ayrıca eklenir", "small", anchor="middle")
s.text(120, 300, "yoncada yok:", "small", anchor="middle")
s.text(120, 314, "çay, meyve suyu", "small", anchor="middle")
save(s, "m56k4_yonca")

# ============================================================ Sekil 1.2 protein oranlari
s = SVG(640, 214, "Bazı besinlerin protein oranı: hamsi yüzde 29, nohut-mercimek-fasulye yüzde 21, yumurta yüzde 13, lor peyniri yüzde 11, yoğurt yüzde 10", "k4b")
x0, x1, vmax = 220, 590, 30
sx = lambda v: x0 + (x1 - x0) * v / vmax
for v in (0, 10, 20, 30):
    grid_v(s, sx(v), 10, 180, base=(v == 0))
    s.text(sx(v), 196, f"%{v}", "small", anchor="middle")
rows = [("Hamsi", 29), ("Nohut, mercimek, fasulye", 21), ("Yumurta", 13), ("Lor peyniri", 11), ("Yoğurt", 10)]
for i, (t, v) in enumerate(rows):
    yc = 28 + i * 34
    s.text(208, yc + 4, t, "title" if i == 0 else "body", anchor="end", fs1=12, fs2=11.5)
    hbar(s, x0, yc - 8, 16, sx(v), ACC, 1 if i == 0 else 0.55)
    s.text(sx(v) + 7, yc + 4, f"%{v}", "body", fs2=11.5)
s.text(x0, 210, "Besinin ağırlıkça protein oranı, sunumdaki yaklaşık değerler.", "small")
save(s, "m56k4_protein")

# ============================================================ Sekil 2.1 siluetler
s = SVG(640, 300, "Normal, zayıf, bodur, düşük kilolu ve obez çocuk: yaşa göre normal boy çizgisine göre", "k4c")
top = 40
s.add(f'<line x1="20" y1="{top}" x2="620" y2="{top}" stroke="{NEU}" stroke-width="1" stroke-dasharray="4 4"/>')
s.text(620, top - 6, "yaşa göre normal boy", "small", anchor="end")
foot = 214


def person(x, height, body_rx, fill_op=0.22):
    head_r = 13 * height
    total = foot - top
    h = total * height
    y_top = foot - h
    hc = y_top + head_r
    body_top = hc + head_r + 2
    leg_len = h * 0.33
    body_bot = foot - leg_len
    bcy = (body_top + body_bot) / 2
    bry = (body_bot - body_top) / 2
    s.add(f'<circle cx="{x}" cy="{hc:.1f}" r="{head_r:.1f}" fill="{ACC}" fill-opacity="{fill_op}" stroke="{CYAN}" stroke-width="1.4"/>')
    s.add(f'<ellipse cx="{x}" cy="{bcy:.1f}" rx="{body_rx}" ry="{bry:.1f}" fill="{ACC}" fill-opacity="{fill_op}" stroke="{CYAN}" stroke-width="1.4"/>')
    for dx in (-0.45, 0.45):
        s.add(f'<line x1="{x + dx * body_rx:.1f}" y1="{body_bot - 4:.1f}" x2="{x + dx * body_rx * 1.4:.1f}" y2="{foot}" stroke="{CYAN}" stroke-width="2.2" stroke-linecap="round"/>')
    ay = body_top + bry * 0.45
    for sg in (-1, 1):
        s.add(f'<line x1="{x + sg * body_rx * 0.9:.1f}" y1="{ay:.1f}" x2="{x + sg * (body_rx + 18):.1f}" y2="{ay + 34 * height:.1f}" stroke="{CYAN}" stroke-width="2.2" stroke-linecap="round"/>')


people = [(70, 1.0, 22, "Normal", ["", ""]), (190, 1.0, 10, "Zayıf", ["boya göre", "düşük ağırlık · akut"]),
          (320, 0.74, 19, "Bodur", ["yaşa göre", "kısa boy · kronik"]), (450, 0.8, 12, "Düşük kilolu", ["yaşa göre", "düşük ağırlık · bileşke"]),
          (570, 1.0, 38, "Obez", ["boya göre", "yüksek ağırlık"])]
for (x, hgt, rx, name, subs) in people:
    person(x, hgt, rx)
    s.add(f'<line x1="{x - 50}" y1="{foot}" x2="{x + 50}" y2="{foot}" stroke="{NEU}" stroke-opacity="0.45" stroke-width="1"/>')
    s.text(x, foot + 22, name, "title", anchor="middle", fs1=12.5)
    for i, t in enumerate(subs):
        if t:
            s.text(x, foot + 38 + i * 14, t, "sub", anchor="middle", fs2=10.5)
save(s, "m56k4_siluet")

# ============================================================ Sekil 2.2 z-skoru ve persantil
s = SVG(640, 322, "Normal dağılım eğrisi üzerinde z-skoru ile persantilin karşılığı ve malnütrisyon sınırları", "k4d")
X0, X1, BASE, HGT = 50, 600, 234, 150
zx = lambda z: X0 + (X1 - X0) * (z + 4) / 8
zy = lambda z: BASE - HGT * math.exp(-z * z / 2)
regs = [(-4, -3, GRAY, 0.45), (-3, -2, GRAY, 0.22), (-2, 2, ACC, 0.13), (2, 4, GRAY, 0.22)]
for (a, b, col, op) in regs:
    pts = [(zx(z), zy(z)) for z in [a + (b - a) * i / 40 for i in range(41)]]
    d = f"M{zx(a):.1f},{BASE} " + " ".join(f"L{x:.1f},{y:.1f}" for x, y in pts) + f" L{zx(b):.1f},{BASE} Z"
    s.add(f'<path d="{d}" fill="{col}" fill-opacity="{op}"/>')
curve(s, [(zx(z), zy(z)) for z in [-4 + i * 0.05 for i in range(161)]], CYAN, 2)
s.add(f'<line x1="{X0}" y1="{BASE}" x2="{X1}" y2="{BASE}" stroke="{NEU}" stroke-opacity="0.6" stroke-width="1"/>')
for z, p in ((-3, ""), (-2, "3."), (-1, "15."), (0, "50."), (1, "85."), (2, "97."), (3, "")):
    s.add(f'<line x1="{zx(z):.1f}" y1="{BASE}" x2="{zx(z):.1f}" y2="{BASE + 5}" stroke="{NEU}" stroke-width="1"/>')
    s.text(zx(z), BASE + 18, f"{z:+d}" if z else "0", "title", anchor="middle", fs1=12)
    if p:
        s.text(zx(z), BASE + 34, p, "body", anchor="middle", fs2=11)
    if z in (-2, 2):
        s.add(f'<line x1="{zx(z):.1f}" y1="{zy(z) - 4:.1f}" x2="{zx(z):.1f}" y2="{BASE}" stroke="{NEU}" stroke-width="1" stroke-dasharray="3 3"/>')
s.text(X0 - 6, BASE + 18, "z", "cap", anchor="end")
s.text(X0 - 6, BASE + 34, "p", "cap", anchor="end")
s.text(zx(0), BASE + 52, "z-skoru (SD) ve karşılık gelen persantil", "small", anchor="middle")
s.text(zx(-3.5), 142, "ağır", "body", anchor="middle", fs2=10.5)
s.text(zx(-3.5), 155, "malnütrisyon", "body", anchor="middle", fs2=10.5)
s.text(zx(-3.5), 168, "z < −3", "small", anchor="middle")
s.text(zx(-2.5), 94, "malnütrisyon", "body", anchor="middle", fs2=10.5)
s.text(zx(-2.5), 107, "−3 ile −2", "small", anchor="middle")
s.text(zx(0), 42, "normal: −2 ile +2", "title", anchor="middle", fs1=12)
s.text(zx(0), 56, "çoğu çocuk −1 ile +1 arasında", "small", anchor="middle")
s.text(zx(3), 142, "aşırı", "body", anchor="middle", fs2=10.5)
s.text(zx(3), 155, "beslenme", "body", anchor="middle", fs2=10.5)
s.text(zx(3), 168, "z > +2", "small", anchor="middle")
save(s, "m56k4_zskor")

# ============================================================ Sekil 2.3 persantil kanali
s = SVG(640, 340, "Büyüme eğrisi: 10. persantil kanalında kararlı büyüyen sağlıklı çocuk ve iki ana persantil çizgisini aşağı kesen çocuk", "k4e")
X0, X1, Y0, Y1 = 60, 560, 290, 20
med = [(0, 3.3), (1, 4.5), (2, 5.6), (3, 6.4), (4, 7.0), (6, 7.9), (9, 8.9), (12, 9.6), (15, 10.3), (18, 10.9), (21, 11.5), (24, 12.2)]


def mval(t):
    for (a, va), (b, vb) in zip(med, med[1:]):
        if a <= t <= b:
            u = (t - a) / (b - a)
            return va + (vb - va) * u
    return med[-1][1]


Z = {3: -1.88, 10: -1.28, 25: -0.67, 50: 0, 75: 0.67, 90: 1.28, 97: 1.88}
wv = lambda t, z: mval(t) * (1 + 0.115 * z)
tx = lambda t: X0 + (X1 - X0) * t / 24
wy = lambda w: Y0 - (Y0 - Y1) * (w - 2) / (16 - 2)
for w in (2, 4, 6, 8, 10, 12, 14, 16):
    grid_h(s, wy(w), X0, X1, base=(w == 2))
    s.text(X0 - 8, wy(w) + 3.5, f"{w}", "small", anchor="end")
for t in (0, 3, 6, 9, 12, 15, 18, 21, 24):
    grid_v(s, tx(t), Y1, Y0, base=(t == 0))
    s.text(tx(t), Y0 + 15, f"{t}", "small", anchor="middle")
ts = [i * 0.25 for i in range(97)]
for p, z in Z.items():
    major = p in (25, 10)
    curve(s, [(tx(t), wy(wv(t, z))) for t in ts], NEU, 1.6 if major else 1.1, opacity=0.75 if major else 0.45)
    s.text(X1 + 10, wy(wv(24, z)) + 3.5, f"{p}.", "body" if major else "small", fs2=10.5)
s.text(X1 + 10, wy(wv(24, 1.88)) - 14, "persantil", "small")
# kararli cocuk: 10. persantil
st = [0, 2, 4, 6, 9, 12, 15, 18, 21, 24]
for t in st:
    s.add(f'<circle cx="{tx(t):.1f}" cy="{wy(wv(t, -1.25)):.1f}" r="3.6" fill="{GRAY}" fill-opacity="0.75" stroke="white" stroke-width="1.5"/>')
# dusen cocuk
fz = [(0, 0), (2, 0.02), (4, 0), (6, -0.02), (9, -0.6), (12, -1.1), (15, -1.5), (18, -1.55)]
curve(s, [(tx(t), wy(wv(t, z))) for t, z in fz], ACC, 2.4)
for t, z in fz:
    s.add(f'<circle cx="{tx(t):.1f}" cy="{wy(wv(t, z)):.1f}" r="4.4" fill="{ACC}" stroke="white" stroke-width="1.8"/>')
s.text(tx(1.2), wy(14.6), "Mavi çocuk 6. aydan sonra 25. ve", "cyanb", fs2=11)
s.text(tx(1.2), wy(14.6) + 14, "10. persantil çizgilerini kesti", "cyanb", fs2=11)
s.add(f'<line x1="{tx(7.5):.1f}" y1="{wy(14.6) + 20:.1f}" x2="{tx(11.6):.1f}" y2="{wy(wv(12, -1.1)) - 8:.1f}" stroke="{CYAN}" stroke-width="1" stroke-dasharray="3 3"/>')
s.text(tx(13), wy(wv(13, -1.25)) + 30, "10. persantilde kararlı büyüme: normal", "body", fs2=10.5)
s.text((X0 + X1) / 2, Y0 + 32, "Yaş (ay)", "small", anchor="middle")
s.text(18, (Y0 + Y1) / 2, "Ağırlık (kg)", "small", anchor="middle", rotate=-90)
save(s, "m56k4_kanal")

# ============================================================ Sekil 2.4 bodurluk
s = SVG(640, 236, "Türkiye'de beş yaş altı çocuklarda bodurluk sıklığı: 1998 yüzde 16,0; 2003 yüzde 12,2; 2008 yüzde 10,3; 2013 yaklaşık yüzde 10-11; 2018 yüzde 6,0", "k4f")
X0, X1, B, T = 60, 600, 192, 20
vmax = 18
sy = lambda v: B - (B - T) * v / vmax
for v in (0, 5, 10, 15):
    grid_h(s, sy(v), X0, X1, base=(v == 0))
    s.text(X0 - 8, sy(v) + 3.5, f"%{v}", "small", anchor="end")
data = [("1998", 16.0, "%16,0", 1), ("2003", 12.2, "%12,2", 1), ("2008", 10.3, "%10,3", 1), ("2013", 10.5, "≈%10-11", 0.45), ("2018", 6.0, "%6,0", 1)]
gw = (X1 - X0) / len(data)
for i, (yl, v, lab, op) in enumerate(data):
    x = X0 + gw * i + gw / 2 - 22
    vbar(s, x, 44, B, sy(v), ACC, op)
    s.text(x + 22, sy(v) - 7, lab, "body", anchor="middle", fs2=11.5)
    s.text(x + 22, B + 17, yl, "body", anchor="middle", fs2=11)
s.text(X0, 230, "TNSA, beş yaş altında yaşa göre boy −2 SD'nin altı. 2013 değeri için sunumlar farklı rakam verir.", "small")
save(s, "m56k4_bodurluk")

# ============================================================ Sekil 3.1 marasmus ve kwashiorkor
s = SVG(640, 356, "Marasmus ve kwashiorkorun gelişimi: eksik olan besin vücudun açlığa uyumunu belirler", "k4g")
s.text(160, 16, "MARASMUS", "cap", anchor="middle")
s.text(480, 16, "KWASHIORKOR", "cap", anchor="middle")
L = [("Enerji (kalori) yetersiz", "her besin az alınır"),
     ("İnsülin ↓, kortizol ↑", "açlığa fizyolojik uyum"),
     ("Yağ ve kas yıkılır", "amino asitler karaciğere gider"),
     ("Albümin yapımı sürer", "onkotik basınç korunur")]
R = [("Protein yetersiz", "karbonhidrat (nişasta) yeterli"),
     ("İnsülin yüksek kalır", "karbonhidrat insülini uyarır"),
     ("Kas proteini yıkılmaz", "karaciğere amino asit gelmez"),
     ("Albümin ↓", "onkotik basınç ↓, sıvı dokuya geçer")]
ys = [26, 92, 158, 224]
for col, (x, items) in enumerate(((20, L), (340, R))):
    cx = x + 140
    for i, (t, sub) in enumerate(items):
        s.box(x, ys[i], 280, 44, [(t, "title"), (sub, "sub")], lh=15)
        s.arrow(cx, ys[i] + 44, cx, ys[i] + 62)
s.box(20, 290, 280, 58, [("Ödem yok, “bir deri bir kemik”", "title"), ("deri altı yağ kaybolmuş, kaslar erimiş,", "sub"), ("yaşlı yüz, sık enfeksiyon ve ishal", "sub")], kind="key", lh=14)
s.box(340, 290, 280, 58, [("Ödem, ağırlık normale yakın", "title"), ("yağ kısmen korunmuş, apati,", "sub"), ("deri kuru, saç ince", "sub")], kind="key", lh=14)
save(s, "m56k4_pem")

# ============================================================ Sekil 3.2 yari omurler
s = SVG(640, 196, "Serum proteinlerinin yaklaşık yarı ömrü: albümin 20 gün, transferrin 8-10 gün, prealbümin 2 gün, retinol bağlayan protein 12 saat", "k4h")
x0, x1, vmax = 230, 590, 27
sx = lambda v: x0 + (x1 - x0) * v / vmax
for v in (0, 5, 10, 15, 20, 25):
    grid_v(s, sx(v), 10, 160, base=(v == 0))
    s.text(sx(v), 176, f"{v}", "small", anchor="middle")
rows = [("Albümin", 20, "≈20 gün", "uzun dönem"), ("Transferrin", 9, "8-10 gün", ""), ("Prealbümin (transtiretin)", 2, "≈2 gün", "yakın dönem"),
        ("Retinol bağlayan protein", 0.5, "≈12 saat", "")]
for i, (t, v, lab, note) in enumerate(rows):
    yc = 30 + i * 36
    s.text(218, yc + 4, t, "title" if i == 2 else "body", anchor="end", fs1=12, fs2=11.5)
    hbar(s, x0, yc - 8, 16, sx(v), ACC, 1 if i == 2 else 0.55)
    s.text(sx(v) + 7, yc + 4, lab + (f" · {note}" if note else ""), "body", fs2=11)
s.text(x0, 192, "Gün", "small")
save(s, "m56k4_yariomur")

# ============================================================ Sekil 3.3 yeniden beslenme
s = SVG(640, 470, "Yeniden beslenme sendromunun mekanizması ve önleme noktaları", "k4i")
s.box(150, 10, 340, 48, [("Uzun açlık", "title"), ("insülin ↓, hücre içi fosfat, potasyum, magnezyum depoları boş", "sub")], fs2=10.5)
s.arrow(320, 58, 320, 80)
s.box(150, 84, 340, 44, [("Karbonhidrattan zengin, yüksek kalorili beslenme", "title"), ("hızla başlanırsa", "sub")])
s.arrow(320, 128, 320, 168)
s.block(320, 148)
s.box(410, 129, 220, 38, [("Karbonhidratı sınırla,", "magb"), ("kaloriyi yavaş artır (ilk hafta <%75)", "sub")], kind="mag", fs2=10.5, lh=14)
s.add(f'<line x1="334" y1="148" x2="410" y2="148" stroke="{MAG}" stroke-width="1.4"/>')
s.box(200, 172, 240, 40, [("İnsülin birden yükselir", "title")], kind="key")
s.path("M320,212 L320,224 L165,224 L165,236")
s.path("M320,212 L320,224 L475,224 L475,236")
s.box(20, 240, 290, 58, [("Glukoz, fosfat, magnezyum ve", "title"), ("potasyum hücre içine girer", "title"), ("serum düzeyleri ani düşer", "sub")], lh=15)
s.box(330, 240, 290, 58, [("Sodyum ve su tutulur", "title"), ("hücre içinde sodyum birikir, insülin", "sub"), ("böbrekte sodyumu tutar: hiponatremi yok", "sub")], lh=14)
s.arrow(165, 298, 165, 338)
s.block(165, 318)
s.text(180, 322, "K⁺, Mg²⁺, fosfat desteği", "magb", fs2=10.5)
s.arrow(475, 298, 475, 338)
s.block(475, 318)
s.text(490, 315, "sodyum kısıtla,", "magb", fs2=10.5)
s.text(490, 329, "sıvı yükünden kaçın", "magb", fs2=10.5)
s.box(20, 342, 290, 46, [("Hipofosfatemi, hipomagnezemi, hipokalemi", "title"), ("tiamin de tükenir", "sub")], lh=15, fs1=12)
s.box(330, 342, 290, 46, [("Sıvı yükü", "title"), ("incelmiş kalbe biner", "sub")], lh=15)
s.path("M165,388 L165,400 L300,400 L300,412")
s.path("M475,388 L475,400 L340,400 L340,412")
s.box(60, 416, 520, 46, [("Kalp yetmezliği, aritmi, solunum yetmezliği, rabdomiyoliz", "title"), ("nöromüsküler bulgular, konvülziyon, koma, ani ölüm", "sub")], kind="key", lh=15)
save(s, "m56k4_refeeding")

# ============================================================ Sekil 4.1 D vitamini metabolizmasi
s = SVG(640, 486, "D vitamininin metabolizması: deri ve besin, karaciğerde 25-hidroksilasyon, böbrekte 1-alfa hidroksilasyon, etkiler ve raşitizm nedenlerinin yerleri", "k4j")
s.box(20, 10, 200, 52, [("Deri", "title"), ("7-dehidrokolesterol", "sub"), ("UVB ile → D3 (kolekalsiferol)", "sub")], lh=14)
s.box(240, 10, 200, 52, [("Besin", "title"), ("ergosterol → D2 (ergokalsiferol);", "sub"), ("balık yağı, karaciğer, yumurta", "sub")], lh=14, fs2=10.5)
s.path("M120,62 L120,76 L230,76 L230,88")
s.path("M340,62 L340,76 L230,76", marker=False)
s.box(120, 92, 220, 44, [("Karaciğer: 25-hidroksilaz", "title"), ("1. hidroksilasyon", "sub")], lh=15)
s.arrow(230, 136, 230, 158)
s.box(110, 162, 240, 48, [("25-OH D vitamini", "title"), ("dolaşımdaki depo biçimi, kanda ölçülen", "sub")], kind="key", lh=15)
s.arrow(230, 210, 230, 232)
s.box(110, 236, 240, 48, [("Böbrek: 1α-hidroksilaz", "title"), ("PTH uyarır (kalsiyum düşünce)", "sub")], lh=15)
s.arrow(230, 284, 230, 306)
s.box(110, 310, 240, 48, [("1,25-(OH)₂ D vitamini (kalsitriol)", "title"), ("en aktif biçim", "sub")], kind="key", lh=15)
for x, t2, sub in ((20, "Barsak", "Ca ve P emilimi ↑ (en önemli)"), (230, "Böbrek", "Ca ve P atılımı ↓"), (440, "Kemik", "PTH ile Ca mobilizasyonu")):
    s.box(x, 410, 180, 48, [(t2, "title"), (sub, "sub")], lh=15, fs2=10.5)
s.path("M230,358 L230,384 L110,384 L110,406")
s.path("M230,384 L320,384 L320,406")
s.path("M230,384 L530,384 L530,406")
notes = [(36, 442, ["güneşlenmeme, koyu ten,", "örtünme; takviyesiz anne", "sütü, annenin eksikliği"], "sub"),
         (114, 342, ["karaciğer hastalığı:", "25-hidroksilasyon ↓; safra", "tıkanıklığı, malabsorpsiyon:", "emilim ↓"], "sub"),
         (186, 352, ["antikonvülzanlar (fenobarbital,", "fenitoin): D vitamini", "yıkımı ↑"], "magb"),
         (260, 352, ["kronik böbrek yetmezliği,", "1α-hidroksilaz eksikliği"], "sub"),
         (334, 352, ["kalsitriol reseptörü", "eksikliği (kalıtsal)"], "sub")]
for (yc, xs, lines, st) in notes:
    y0 = yc - (len(lines) - 1) * 7 + 3.5
    for i, ln in enumerate(lines):
        s.text(462, y0 + i * 14, ln, st, fs2=10.5)
    col = MAG if st == "magb" else NEU
    s.add(f'<line x1="{xs}" y1="{yc}" x2="456" y2="{yc}" stroke="{col}" stroke-opacity="{1 if st == "magb" else 0.5}" stroke-width="1.2" stroke-dasharray="{"" if st == "magb" else "3 3"}"/>')
save(s, "m56k4_dvit")

# ============================================================ Sekil 4.2 rasitizm biyokimyasi
s = SVG(640, 452, "D vitamini eksikliğine bağlı raşitizmin biyokimyası: kalsiyum emilimi azalır, PTH artar, fosfat düşer, alkalen fosfataz artar", "k4k")
s.box(190, 10, 260, 40, [("D vitamini ↓", "title"), ("25-OH D ↓, 1,25-(OH)₂ D ↓", "sub")], lh=14)
s.arrow(320, 50, 320, 68)
s.box(190, 72, 260, 40, [("Barsaktan Ca ve P emilimi ↓", "title")])
s.arrow(320, 112, 320, 130)
s.box(190, 134, 260, 40, [("Serum Ca düşme eğiliminde", "title")])
s.arrow(320, 174, 320, 192)
s.box(170, 196, 300, 44, [("PTH ↑", "title"), ("sekonder hiperparatiroidizm", "sub")], kind="key", lh=15)
s.path("M320,240 L320,252 L165,252 L165,264")
s.path("M320,240 L320,252 L475,252 L475,264")
s.box(20, 268, 290, 52, [("Kemikten Ca çekilir,", "title"), ("böbrekte Ca geri emilimi ↑", "title")], lh=15)
s.box(330, 268, 290, 52, [("Böbrekte fosfat atılımı ↑", "title"), ("barsaktan da az fosfat gelir", "sub")], lh=15)
s.arrow(165, 320, 165, 338)
s.arrow(475, 320, 475, 338)
s.box(20, 342, 290, 40, [("Serum Ca düşük-normal, idrar Ca ↓", "title")], kind="key", fs1=12)
s.box(330, 342, 290, 40, [("Serum fosfat ↓", "title")], kind="key")
s.path("M165,382 L165,394 L300,394 L300,402")
s.path("M475,382 L475,394 L340,394 L340,402")
s.box(90, 406, 460, 40, [("Ca × P ↓: osteoid mineralize olamaz → osteoblastlar fazla çalışır: ALP ↑", "title")], kind="key", fs1=12)
save(s, "m56k4_biyokimya")

print("ok", sorted(f for f in os.listdir(OUT) if f.endswith(".svg")))
