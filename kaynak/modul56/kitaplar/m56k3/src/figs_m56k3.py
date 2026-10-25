import os, sys
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
    """iki ucu yuvarlak aralik cubugu"""
    r = min(4, h / 2, (x1 - x0) / 2)
    s.add(f'<rect x="{x0:.1f}" y="{y:.1f}" width="{x1 - x0:.1f}" height="{h}" rx="{r}" fill="{color}" fill-opacity="{opacity}"/>')


def vblock(s, x, y, length=22, color=MAG):
    """yatay bir oku kesen dikey magenta cubuk"""
    s.add(f'<line x1="{x}" y1="{y - length / 2}" x2="{x}" y2="{y + length / 2}" stroke="{color}" stroke-width="2.5"/>')


def grid_v(s, x, y0, y1, base=False):
    s.add(f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y1}" stroke="{NEU}" stroke-opacity="{0.45 if base else 0.15}" stroke-width="1"/>')


def grid_h(s, y, x0, x1, base=False):
    s.add(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{NEU}" stroke-opacity="{0.45 if base else 0.15}" stroke-width="1"/>')


def dpath(s, d, color=NEU, marker=True, width=1.3):
    m = f' marker-end="url(#{s.mid}{s._m(color)})"' if marker else ""
    s.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-dasharray="4 3"{m}/>')


def curve(s, pts, color, width=2.2):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    s.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>')


# ============================================================ Sekil 1.1 kan basinci kontrolunun yarari
s = SVG(640, 176, "Kan basıncı kontrolünün sağladığı azalma: kalp yetmezliği yüzde 50, inme yüzde 40, miyokard infarktüsü yüzde 25", "k3a")
x0, x1, vmax = 200, 600, 60
sx = lambda v: x0 + (x1 - x0) * v / vmax
for v in (0, 20, 40, 60):
    grid_v(s, sx(v), 10, 140, base=(v == 0))
    s.text(sx(v), 156, f"%{v}", "small", anchor="middle")
for i, (t, v) in enumerate((("Kalp yetmezliği", 50), ("İnme", 40), ("Miyokard infarktüsü", 25))):
    yc = 32 + i * 42
    s.text(190, yc + 4, t, "title", anchor="end", fs1=12.5)
    hbar(s, x0, yc - 8, 16, sx(v), ACC)
    s.text(sx(v) + 7, yc + 4, f"%{v} azalma", "body", fs2=11.5)
s.text(x0, 172, "Görülme sıklığındaki azalma, sunumdaki değerler.", "small")
save(s, "m56k3_kontrol")

# ============================================================ Sekil 1.2 kan basincinin bilesenleri
s = SVG(640, 292, "Kan basıncı eşittir kalp debisi çarpı periferik vasküler direnç; kalp debisi eşittir kalp hızı çarpı atım hacmi; ilaç sınıflarının etki noktaları", "k3b")
s.box(220, 8, 200, 34, [("Kan basıncı", "title")], kind="key")
s.box(40, 72, 260, 40, [("Kalp debisi", "title"), ("kardiyak output", "sub")])
s.box(340, 72, 260, 40, [("Periferik vasküler direnç", "title"), ("esas olarak arteriyol çapı", "sub")])
s.text(320, 97, "×", "title", anchor="middle", fs1=16)
s.path("M170,70 L170,57 L292,57 L292,46")
s.path("M470,70 L470,57 L348,57 L348,46")
s.box(40, 132, 118, 38, [("Kalp hızı", "title")])
s.box(182, 132, 118, 38, [("Atım hacmi", "title"), ("ön yük, kasılma", "sub")], lh=14)
s.text(170, 156, "×", "title", anchor="middle", fs1=14)
s.box(340, 132, 118, 38, [("Arteriyel basınç", "title"), ("arteriyol direnci", "sub")], lh=14)
s.box(482, 132, 118, 38, [("Venöz basınç", "title"), ("venöz tonus", "sub")], lh=14)
for x in (99, 241, 399, 541):
    s.arrow(x, 130, x, 116)
drugs = [(40, 118, "β blokerler", 99), (182, 118, "Diüretikler", 241), (340, 118, "KKB", 399), (482, 118, "ACEİ · ARB", 541)]
for (x, w, t, ax) in drugs:
    s.box(x, 226, w, 30, [(t, "magb")], kind="mag", fs2=12)
    s.arrow(ax, 224, ax, 174, color=MAG)
s.path("M524,224 L446,174", color=MAG)
s.text(320, 278, "Uzun dönemde diüretikler ve β blokerler (renin ↓) de direnci düşürür.", "mag", anchor="middle", fs2=11)
s.text(107, 204, "hız ↓", "small", anchor="start")
s.text(249, 204, "hacim ↓", "small", anchor="start")
s.text(407, 198, "arteriyol", "small", anchor="start")
s.text(407, 210, "dilatasyonu", "small", anchor="start")
s.text(549, 198, "arteriyel ve", "small", anchor="start")
s.text(549, 210, "venöz", "small", anchor="start")
save(s, "m56k3_bilesen")

# ============================================================ Sekil 1.3 tedavi algoritmasi
s = SVG(640, 392, "Hipertansiyonda ilaç tedavisi algoritması, Türk Hipertansiyon Uzlaşı Raporu 2019", "k3c")
s.box(220, 8, 200, 30, [("Antihipertansif tedavi", "title")])
s.box(40, 60, 260, 32, [("Evre 1 hipertansiyon", "title")])
s.box(370, 60, 230, 32, [("Evre 2 hipertansiyon", "title")])
s.path("M290,38 L290,48 L170,48 L170,56")
s.path("M350,38 L350,48 L485,48 L485,56")
s.box(20, 116, 190, 62, [("KB <150/90 mmHg", "title"), ("tek ilaç: ACEİ ya da ARB,", "sub"), ("KKB ya da diüretik", "sub")], lh=14)
s.box(230, 116, 110, 40, [("KB ≥150/90", "title"), ("mmHg", "sub")], lh=14)
s.path("M120,92 L120,112")
s.path("M220,92 L220,104 L285,104 L285,112")
s.box(230, 196, 390, 48, [("İkili kombinasyon", "title"), ("ACEİ ya da ARB + KKB   veya   ACEİ ya da ARB + diüretik", "sub")], kind="key")
s.arrow(285, 156, 285, 192)
s.arrow(485, 92, 485, 192)
s.path("M115,178 L115,220 L226,220")
s.text(122, 210, "hedefte değil", "small")
s.box(230, 268, 390, 40, [("Üçlü kombinasyon", "title"), ("ACEİ ya da ARB + KKB + diüretik", "sub")], kind="key")
s.arrow(425, 244, 425, 264)
s.text(433, 258, "hedefte değil", "small")
s.box(230, 332, 390, 48, [("Dörtlü: + spironolakton", "title"), ("dirençli hipertansiyon (önce uyum ve sekonder neden araştırılır)", "sub")], kind="key")
s.arrow(425, 308, 425, 328)
s.text(433, 322, "hedefte değil", "small")
notes = ["Hedef ≤130 mmHg ise doğrudan", "kombinasyonla başlanabilir.", "",
         "β bloker yalnızca özel nedenle:", "kalp yetmezliği, KAH, anjina,", "atriyal fibrilasyon, gebelik planı.", "",
         "3-4 ilaçta en az biri ayrı", "saatte verilir (sabah-akşam)."]
for i, t in enumerate(notes):
    if t:
        s.text(20, 252 + i * 14, t, "small")
save(s, "m56k3_algoritma")

# ============================================================ Sekil 2.1 RAAS ve etki noktalari
s = SVG(640, 470, "Renin-anjiyotensin-aldosteron sistemi ve ilaçların etki noktaları: beta bloker renin salınımını, ACE inhibitörü ACE'yi, ARB AT1 reseptörünü, spironolakton aldosteron reseptörünü hedefler", "k3d")
s.box(160, 10, 170, 40, [("Anjiyotensinojen", "title"), ("karaciğerde yapılır", "sub")], lh=14)
s.arrow(245, 50, 245, 92)
s.text(236, 76, "renin", "cyanb", anchor="end", fs2=11.5)
s.box(400, 40, 230, 62, [("Jukstaglomerüler hücreler", "title"), ("renin salgılar: perfüzyon ↓,", "sub"), ("β1 uyarısı, makula densaya NaCl ↓", "sub")], lh=14, fs2=10.5)
s.arrow(400, 71, 250, 71)
vblock(s, 330, 71)
s.text(330, 59, "β bloker", "magb", anchor="middle", fs2=11)
s.box(160, 96, 170, 40, [("Anjiyotensin I", "title"), ("dekapeptit", "sub")], lh=14)
s.arrow(245, 136, 245, 180)
s.text(226, 154, "ACE", "cyanb", anchor="end", fs2=11.5)
s.text(226, 167, "(kininaz II)", "small", anchor="end")
s.block(245, 158)
s.text(262, 162, "ACE inhibitörü", "magb", fs2=11)
s.box(160, 184, 170, 40, [("Anjiyotensin II", "title"), ("oktapeptit", "sub")], lh=14)
s.arrow(245, 224, 245, 262)
s.block(245, 243)
s.text(262, 247, "ARB", "magb", fs2=11)
s.box(160, 266, 170, 34, [("AT1 reseptörü", "title")], kind="key")
dpath(s, "M330,204 L410,204 L410,106")
s.text(338, 218, "geri bildirim", "small")
s.box(440, 120, 180, 40, [("Bradikinin", "title"), ("vazodilatör: NO, prostasiklin", "sub")], lh=14, fs2=10.5)
s.arrow(530, 160, 530, 200)
s.text(540, 176, "ACE", "cyanb", fs2=11.5)
s.block(530, 180)
s.text(512, 184, "ACEİ", "magb", anchor="end", fs2=11)
s.box(440, 204, 180, 30, [("İnaktif peptitler", "title")])
s.text(530, 252, "ACEİ ile bradikinin birikir:", "mag", anchor="middle", fs2=10.5)
s.text(530, 265, "kuru öksürük, anjiyoödem", "mag", anchor="middle", fs2=10.5)
eff = [(10, "Damar daralması", "periferik direnç ↑"), (165, "Aldosteron ↑", "adrenal korteks"),
       (320, "ADH ↑, susama", "su tutulur"), (475, "Hipertrofi, fibroz", "kalp, damar, böbrek")]
for (x, t, sub) in eff:
    cx = x + 70
    s.path(f"M245,300 L245,316 L{cx},316 L{cx},334")
    s.box(x, 338, 140, 42, [(t, "title"), (sub, "sub")], lh=14)
s.arrow(235, 380, 235, 416)
s.block(235, 398)
s.text(252, 402, "spironolakton", "magb", fs2=11)
s.box(165, 420, 140, 42, [("Toplayıcı kanal", "title"), ("Na⁺ tutulur, K⁺ atılır", "sub")], lh=14)
save(s, "m56k3_raas")

# ============================================================ Sekil 2.2 ACEI'nin bobrekteki iki yuzu
s = SVG(640, 420, "ACE inhibitörünün böbrekteki iki yüzü: hiperfiltrasyon yapan glomerülü korur, perfüzyonu azalmış glomerülde GFR'yi düşürür", "k3e")
s.text(160, 16, "KORUYUCU YÜZ", "cap", anchor="middle")
s.text(480, 16, "NEFROTOKSİK YÜZ", "cap", anchor="middle")
L = [("Hiperfiltrasyon", ["diyabet, nefron kaybı"]),
     ("AII efferenti daraltır", ["glomerül basıncı gereğinden yüksek"]),
     ("Efferent gevşer", ["fazla basınç kalkar"]),
     ("Glomerül basıncı normale iner", ["proteinüri ve skleroz azalır"]),
     ("Böbrek korunur", ["kreatinin %30'a kadar yükselebilir:", "hasar değil, fazla basıncın kalkması"])]
R = [("Perfüzyon azalmış", ["bilateral renal arter darlığı,", "tek böbrekte darlık, hacim azalması"]),
     ("Renin ↑, AII efferenti daraltır", ["GFR bu daralmaya dayanır"]),
     ("Efferent gevşer", ["GFR'nin dayanağı kalkar"]),
     ("Glomerül basıncı çöker", ["filtrasyon durur"]),
     ("GFR ani düşer", ["hemodinamik ABH, bu hastalarda", "ACEİ ve ARB kontrendikedir"])]
ys = [26, 96, 186, 246, 306]
hs = [48, 48, 42, 42, 56]
for col, (x, items) in enumerate(((20, L), (340, R))):
    cx = x + 140
    for i, (t, subs) in enumerate(items):
        kind = "normal"
        if i == 4:
            kind = "key" if col == 0 else "mag"
        s.box(x, ys[i], 280, hs[i], [(t, "title")] + [(u, "sub") for u in subs], kind=kind, lh=14)
    s.arrow(cx, ys[0] + hs[0], cx, ys[1] - 4)
    s.arrow(cx, ys[1] + hs[1], cx, ys[2] - 4)
    s.block(cx, 164)
    s.text(cx + 16, 168, "ACEİ · ARB", "magb", fs2=11)
    s.arrow(cx, ys[2] + hs[2], cx, ys[3] - 4)
    s.arrow(cx, ys[3] + hs[3], cx, ys[4] - 4)
s.box(340, 376, 280, 36, [("NSAİİ eklenirse afferent de daralır:", "magb"), ("giriş kapanır, çıkış açılır, GFR iki uçtan düşer", "sub")], kind="mag", lh=14, fs2=11)
save(s, "m56k3_ikiyuz")

# ============================================================ Sekil 3.1 aksiyon potansiyelleri
s = SVG(640, 300, "Nodal hücrede ve kasılabilir miyositte aksiyon potansiyeli; L tipi kalsiyum kanalının açık olduğu fazlar magenta", "k3f")
Y = lambda mv: 250 - (mv + 100) * 200 / 140
for (x0, x1, title) in ((44, 300, "Nodal (pacemaker) hücre"), (364, 630, "Kasılabilir miyosit")):
    s.text((x0 + x1) / 2, 18, title, "title", anchor="middle")
    for mv in (20, 0, -40, -90):
        grid_h(s, Y(mv), x0, x1)
    s.add(f'<line x1="{x0}" y1="{Y(30):.1f}" x2="{x0}" y2="{Y(-100):.1f}" stroke="{NEU}" stroke-opacity="0.45" stroke-width="1"/>')
    for mv in (20, 0, -40, -90):
        s.text(x0 - 6, Y(mv) + 3.5, f"{mv:+d}" if mv else "0", "small", anchor="end")
s.text(14, Y(-35), "mV", "small", anchor="middle", rotate=-90)
# nodal
import math
p4a = [(54 + t * 70, Y(-62 + 22 * (t ** 1.4))) for t in [i / 20 for i in range(21)]]
p0 = [(124 + t * 26, Y(-40 + 52 * math.sin(t * math.pi / 2))) for t in [i / 12 for i in range(13)]]
p3 = [(150 + t * 70, Y(12 - 76 * (1 - math.cos(t * math.pi)) / 2)) for t in [i / 20 for i in range(21)]]
p4b = [(220 + t * 60, Y(-64 + 22 * (t ** 1.4))) for t in [i / 20 for i in range(21)]]
curve(s, p4a, ACC)
curve(s, p0, MAG, 3.2)
curve(s, p3, ACC)
curve(s, p4b, ACC)
s.add(f'<line x1="54" y1="{Y(-40):.1f}" x2="300" y2="{Y(-40):.1f}" stroke="{NEU}" stroke-width="1" stroke-dasharray="3 3"/>')
s.text(206, Y(-40) - 5, "eşik ≈ -40 mV", "small", anchor="start")
s.text(88, Y(-50) + 18, "4", "cap", anchor="middle")
s.text(118, Y(-12), "0", "cap", anchor="end")
s.text(192, Y(-22), "3", "cap", anchor="middle")
s.text(52, 270, "faz 4: funny akım (Na⁺) ve T tipi Ca²⁺", "body", fs2=10.5)
s.text(140, Y(20) - 8, "faz 0: L tipi Ca²⁺", "magb", anchor="middle", fs2=11)
s.text(52, 286, "faz 3: K⁺ çıkışı", "body", fs2=10.5)
# miyosit
v4a = [(372, Y(-90)), (398, Y(-90))]
v0 = [(398, Y(-90)), (401, Y(22))]
v1 = [(401, Y(22)), (406, Y(12)), (412, Y(6))]
v2 = [(412 + t * 112, Y(6 - 14 * t ** 2)) for t in [i / 20 for i in range(21)]]
v3 = [(524 + t * 52, Y(-8 - 82 * (1 - math.cos(t * math.pi)) / 2)) for t in [i / 20 for i in range(21)]]
v4b = [(576, Y(-90)), (628, Y(-90))]
for seg in (v4a, v0, v1, v3, v4b):
    curve(s, seg, ACC)
curve(s, v2, MAG, 3.2)
s.text(392, Y(-20), "0", "cap", anchor="end")
s.text(408, Y(22) - 4, "1", "cap", anchor="start")
s.text(468, Y(2) - 18, "2 (plato)", "cap", anchor="middle")
s.text(556, Y(-40), "3", "cap", anchor="start")
s.text(600, Y(-90) - 6, "4", "cap", anchor="middle")
s.text(392, Y(-70), "hızlı Na⁺", "body", anchor="end", fs2=10.5)
s.text(468, Y(-30) + 4, "L tipi Ca²⁺ girişi", "magb", anchor="middle", fs2=11)
s.text(468, Y(-30) + 18, "+ K⁺ çıkışı", "body", anchor="middle", fs2=10.5)
s.text(586, Y(-40) + 14, "K⁺", "body", fs2=10.5)
s.text(372, 270, "faz 4: dinlenme potansiyeli, -90 mV", "body", fs2=10.5)
save(s, "m56k3_ap")

# ============================================================ Sekil 3.2 kasilma zincirleri
s = SVG(640, 390, "Kalp kasında ve damar düz kasında kasılma zinciri ve kalsiyum kanal blokerinin etki noktası", "k3g")
s.text(160, 16, "KALP KASI", "cap", anchor="middle")
s.text(480, 16, "DAMAR DÜZ KASI", "cap", anchor="middle")
K = [("Depolarizasyon", "plato fazı (faz 2)"), ("Ca²⁺ hücreye girer", "L tipi kanal"),
     ("SR'den Ca²⁺ salınır", "ryanodin reseptörü"), ("Ca²⁺ troponine bağlanır", "tropomiyozin kayar"),
     ("Aktin-miyozin: kasılma", "KKB ile kasılma gücü ↓ (negatif inotropi)")]
D = [("Uyarı", "hormon, sinir, mekanik gerim"), ("Ca²⁺ hücreye girer", "L tipi kanal"),
     ("Ca²⁺-kalmodulin kompleksi", "MLCK aktive olur"), ("Miyozin hafif zinciri fosforile", "aktinle etkileşebilir"),
     ("Aktin-miyozin: kasılma", "KKB ile gevşeme, direnç ↓")]
ys = [28, 112, 170, 228, 286]
for col, (x, items) in enumerate(((20, K), (340, D))):
    cx = x + 140
    for i, (t, sub) in enumerate(items):
        s.box(x, ys[i], 280, 40 if i < 4 else 46, [(t, "title"), (sub, "sub")], kind="key" if i == 4 else "normal", lh=14)
    s.arrow(cx, 68, cx, 108)
    s.block(cx, 88)
    s.text(cx + 16, 92, "KKB", "magb", fs2=11.5)
    for i in (1, 2, 3):
        s.arrow(cx, ys[i] + 40, cx, ys[i + 1] - 4)
s.box(20, 346, 600, 36, [("İskelet kası: L tipi kanal voltaj algılayıcısıdır, ryanodin reseptörünü mekanik olarak açar", "title"),
                         ("Ca²⁺ hücre içi havuzdan (SR) gelir, hücre dışından giriş gerekmez: KKB iskelet kasını etkilemez", "sub")], fs1=11.5, lh=14)
save(s, "m56k3_kasilma")

# ============================================================ Sekil 3.3 KKB gruplarinin karsilastirmasi
s = SVG(640, 318, "KKB gruplarının kalp ve damar etkileri: dihidropiridinler, diltiazem ve verapamil; 0 etki yok, üç artı en fazla", "k3h")
cols = ["Dihidropiridinler", "Diltiazem", "Verapamil"]
rows = [("Vazoselektivite", [3, 1, 0], ["+++", "+", "0"]),
        ("Antianjinal etkinlik", [3, 3, 3], ["+++", "+++", "+++"]),
        ("Sistemik vazodilatör etki", [2, 1, 1], ["++", "+", "+"]),
        ("Miyokard depresyonu (negatif inotropi)", [0.5, 1, 3], ["0 / +", "+", "+++"]),
        ("AV iletiyi yavaşlatma (PR uzaması)", [0, 1, 2], ["0", "+", "++"]),
        ("Damar dışı düz kas gevşetme (konstipasyon)", [0, 1, 3], ["0", "+", "+++"])]
op = {0: 0.05, 0.5: 0.13, 1: 0.24, 2: 0.46, 3: 0.85}
cx0, cw, gap = 290, 106, 6
for j, c in enumerate(cols):
    s.text(cx0 + j * (cw + gap) + cw / 2, 26, c, "title", anchor="middle", fs1=12)
for i, (lab, vals, labs) in enumerate(rows):
    y = 38 + i * 40
    s.text(280, y + 22, lab, "body", anchor="end", fs2=11)
    for j, (v, l) in enumerate(zip(vals, labs)):
        x = cx0 + j * (cw + gap)
        s.add(f'<rect x="{x}" y="{y}" width="{cw}" height="34" rx="3" fill="{ACC}" fill-opacity="{op[v]}"/>')
        col = "white" if v == 3 else TXT
        s.add(f'<text x="{x + cw / 2:.1f}" y="{y + 22}" text-anchor="middle" {FONT} font-size="13" font-weight="700" fill="{col}">{esc(l)}</text>')
s.text(cx0, 296, "Sunumdaki karşılaştırma tablosu. Dihidropiridinler arasında", "small")
s.text(cx0, 309, "vazoselektiflik bakımından pek fark yoktur.", "small")
save(s, "m56k3_secicilik")

# ============================================================ Sekil 4.1 diuretiklerin etki yerleri
s = SVG(640, 470, "Diüretiklerin nefrondaki etki yerleri: segmentlerin sodyum geri emilim payları, taşıyıcıları ve bloke eden ilaçlar", "k3i")
seg = [("Glomerül", ["süzüntü oluşur"], None),
       ("Proksimal tübül", ["Na⁺ %60-70, HCO₃⁻ %85", "NHE3, karbonik anhidraz"],
        [("Karbonik anhidraz inhibitörleri", "magb"), ("asetazolamid: HCO₃⁻ emilemez", "sub")]),
       ("İnce inen kol", ["tuz emilmez, su çıkar", "akuaporin-1"],
        [("Ozmotik diüretikler", "magb"), ("mannitol: suyu lümende tutar", "sub"), ("(proksimal tübülde de)", "sub")]),
       ("Kalın çıkan kol", ["Na⁺ %25-30", "NKCC2 (Na⁺, K⁺, 2Cl⁻)"],
        [("Kıvrım diüretikleri", "magb"), ("furosemid, bumetanid, torsemid", "sub"), ("NKCC2'yi bloke eder", "sub")]),
       ("Distal kıvrımlı tübül", ["Na⁺ %5-10", "NCC (Na⁺, Cl⁻); PTH ile Ca²⁺"],
        [("Tiyazidler", "magb"), ("hidroklorotiyazid, indapamid", "sub"), ("NCC'yi bloke eder", "sub")]),
       ("Toplayıcı kanal", ["Na⁺ %2-5 (aldosteron)", "ENaC; V2 ve akuaporin-2"], None)]
y = 10
yc_list = []
for i, (t, subs, drug) in enumerate(seg):
    h = 50 if i else 34
    if i == 5:
        h = 96
    s.box(20, y, 270, h, [(t, "title")] + [(u, "sub") for u in subs], kind="key" if i else "normal", lh=14)
    yc = y + h / 2
    if drug:
        dh = 50 if len(drug) == 3 else 40
        s.box(350, yc - dh / 2, 280, dh, drug, kind="mag", lh=14, fs2=11)
        s.arrow(348, yc, 294, yc, color=MAG)
        vblock(s, 321, yc)
    if i < 5:
        s.arrow(155, y + h, 155, y + h + 14)
    y += h + 18
    yc_list.append(yc)
ytop = y - 18 - 96
for k, (dy, drug) in enumerate(((6, [("Potasyum tutucular", "magb"), ("aldosteron antagonistleri: spironolakton", "sub"), ("Na kanal inhibitörleri: amilorid", "sub")]),
                                (60, [("Vaptanlar", "magb"), ("tolvaptan, konivaptan: V2 reseptörü", "sub")]))):
    dh = 50 if len(drug) == 3 else 36
    s.box(350, ytop + dy, 280, dh, drug, kind="mag", lh=14, fs2=11)
    yy = ytop + dy + dh / 2
    s.arrow(348, yy, 294, yy, color=MAG)
    vblock(s, 321, yy)
s.arrow(155, ytop + 96, 155, ytop + 116)
s.text(165, ytop + 112, "idrar", "small")
save(s, "m56k3_nefron")

# ============================================================ Sekil 4.2 diuretiklerin gucu
s = SVG(640, 196, "Diüretiklerin artırabildiği tuz atılımı, süzülen sodyumun yüzdesi: kıvrım diüretikleri yüzde 20-40, tiyazidler yüzde 5-15, diğerleri yüzde 2'ye kadar, normal yüzde 1", "k3j")
x0, x1, vmax = 260, 610, 45
sx = lambda v: x0 + (x1 - x0) * v / vmax
for v in (0, 10, 20, 30, 40):
    grid_v(s, sx(v), 12, 160, base=(v == 0))
    s.text(sx(v), 176, f"%{v}", "small", anchor="middle")
rows = [("Kıvrım diüretikleri", "", 20, 40, "%20-40"),
        ("Tiyazidler", "", 5, 15, "%5-15"),
        ("Diğerleri", "K tutucu, KA inhibitörü", 0, 2, "%2'ye kadar"),
        ("Diüretik yok", "normal atılım", 1, 1, "≈%1")]
for i, (t, sub, lo, hi, lab) in enumerate(rows):
    yc = 30 + i * 36
    s.text(250, yc + 4 - (6 if sub else 0), t, "title", anchor="end", fs1=12)
    if sub:
        s.text(250, yc + 12, sub, "small", anchor="end")
    if hi > lo:
        rbar(s, sx(lo), yc - 7, 14, sx(hi), ACC if lo > 0 or hi > 2 else GRAY, 1 if hi > 2 else 0.55)
        s.text(sx(hi) + 7, yc + 4, lab, "body", fs2=11)
    else:
        s.add(f'<circle cx="{sx(lo):.1f}" cy="{yc}" r="5" fill="{GRAY}" fill-opacity="0.7" stroke="white" stroke-width="2"/>')
        s.text(sx(lo) + 10, yc + 4, lab, "body", fs2=11)
s.text(x0, 192, "Süzülen sodyumun atılan yüzdesi (sunumdaki değerler).", "small")
save(s, "m56k3_guc")

# ============================================================ Sekil 4.3 kalsiyum: kivrim ve tiyazid
s = SVG(640, 372, "Kıvrım diüretikleri kalın çıkan kolda kalsiyumun hücreler arası emilimini bozar; tiyazidler distal tübülde hücre içi yolu hızlandırır", "k3k")


def cell(x, y, w, h):
    s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{ACC}" fill-opacity="0.07" stroke="{NEU}" stroke-opacity="0.5" stroke-width="1.2"/>')


def tp(x, y, lab=None, side="below"):
    s.add(f'<circle cx="{x}" cy="{y}" r="7" fill="white" stroke="{CYAN}" stroke-width="1.6"/>')


# sol panel: kalin cikan kol
s.text(160, 18, "Kalın çıkan kol", "title", anchor="middle")
s.text(24, 40, "LÜMEN", "cap", anchor="start")
s.text(296, 40, "KAN", "cap", anchor="end")
cell(100, 48, 130, 84)
cell(100, 186, 130, 76)
tp(100, 70)
tp(100, 112)
s.arrow(36, 70, 110, 70, color=CYAN)
s.text(30, 55, "Na⁺ K⁺ 2Cl⁻", "small")
s.text(114, 74, "NKCC2", "cyanb", fs2=10.5)
vblock(s, 70, 70, 18)
s.text(70, 94, "furosemid", "magb", anchor="middle", fs2=11)
s.arrow(112, 112, 40, 112)
s.text(114, 116, "ROMK", "body", fs2=10.5)
s.text(24, 127, "K⁺ geri sızar", "small")
s.text(24, 151, "+ + +  lümen pozitif", "cyanb", fs2=10.5)
s.arrow(24, 159, 284, 159, color=CYAN)
s.text(165, 176, "Ca²⁺ ve Mg²⁺ hücreler arasından kana", "cyanb", anchor="middle", fs2=10.5)
s.text(165, 228, "komşu hücre", "small", anchor="middle")
s.box(20, 280, 290, 84, [("Furosemid NKCC2'yi kapatır", "magb"), ("K⁺ lümene geri sızamaz,", "sub"), ("lümen pozitifliği kaybolur", "sub"),
                         ("Ca²⁺ ve Mg²⁺ emilemez:", "sub"), ("hiperkalsiüri, hipomagnezemi", "sub")], kind="mag", lh=13.5, fs2=11)
# sag panel: distal kivrimli tubul
s.text(480, 18, "Distal kıvrımlı tübül", "title", anchor="middle")
s.text(344, 40, "LÜMEN", "cap", anchor="start")
s.text(630, 40, "KAN", "cap", anchor="end")
cell(420, 48, 130, 214)
tp(420, 70)
tp(420, 196)
tp(550, 72)
tp(550, 197)
s.arrow(356, 70, 430, 70, color=CYAN)
s.text(350, 55, "Na⁺ Cl⁻", "small")
s.text(434, 74, "NCC", "cyanb", fs2=10.5)
vblock(s, 390, 70, 18)
s.text(390, 94, "tiyazid", "magb", anchor="middle", fs2=11)
s.arrow(542, 66, 616, 66)
s.arrow(616, 78, 556, 78)
s.text(624, 58, "3Na⁺", "small", anchor="end")
s.text(624, 94, "2K⁺", "small", anchor="end")
s.text(544, 102, "Na⁺/K⁺-ATPaz", "small", anchor="end")
s.text(485, 140, "hücre içi Na⁺ ↓", "mag", anchor="middle", fs2=11)
s.text(485, 154, "değiştirici hızlanır", "mag", anchor="middle", fs2=11)
s.arrow(356, 196, 430, 196, color=CYAN)
s.text(356, 188, "Ca²⁺", "cyanb", fs2=11)
s.text(434, 200, "TRPV5", "body", fs2=10.5)
s.text(434, 213, "(PTH ↑)", "small")
s.arrow(542, 191, 616, 191, color=CYAN)
s.text(624, 183, "Ca²⁺", "cyanb", anchor="end", fs2=11)
s.arrow(616, 204, 556, 204)
s.text(624, 220, "Na⁺", "small", anchor="end")
s.text(544, 240, "Na⁺/Ca²⁺ değiştirici", "small", anchor="end")
s.box(330, 280, 300, 84, [("Tiyazid NCC'yi kapatır", "magb"), ("hücre içi Na⁺ düşer, değiştirici daha çok", "sub"), ("Ca²⁺ çıkarır, TRPV5'ten giriş artar", "sub"),
                          ("hacim azalması proksimalde de emilimi artırır:", "sub"), ("hipokalsiüri (serumda Ca²⁺ hafif ↑)", "sub")], kind="key", lh=13.5, fs2=11)
save(s, "m56k3_kalsiyum")

# ============================================================ Sekil 5.1 nefrotoksisite haritasi
s = SVG(640, 512, "Nefrotoksik ilaçların böbrekteki hedefleri: damar ve glomerül, proksimal tübül, interstisyum, distal nefron, papilla", "k3l")
nodes = ["Damar ve glomerül", "Proksimal tübül", "İnterstisyum", "Distal nefron ve|toplayıcı kanal", "Papilla"]
left = [[("Hemodinamik hasar", "magb"), ("NSAİİ, ACEİ ve ARB,", "sub"), ("kalsinörin inhibitörleri,", "sub"), ("iyotlu kontrast, kokain", "sub")],
        [("Direkt toksisite (ATN)", "magb"), ("aminoglikozid, amfoterisin B,", "sub"), ("sisplatin, tenofovir, adefovir,", "sub"), ("foskarnet, asetaminofen,", "sub"), ("pemetreksed, ağır metaller", "sub")],
        [("Akut interstisyel nefrit", "magb"), ("beta-laktamlar, kinolonlar,", "sub"), ("NSAİİ, diüretikler, PPI,", "sub"), ("allopürinol, fenitoin", "sub")],
        [("Kristal nefropatisi (lümen)", "magb"), ("asiklovir, metotreksat,", "sub"), ("sülfonamidler, triamteren,", "sub"), ("etilen glikol, oral fosfat", "sub")],
        [("Papiller nekroz", "magb"), ("aspirin + fenasetin", "sub"), ("(analjezik nefropatisi), NSAİİ", "sub")]]
right = [[("Trombotik mikroanjiyopati", "magb"), ("klopidogrel, gemsitabin,", "sub"), ("mitomisin C, kalsinörin", "sub"), ("inhibitörleri, VEGF inhibitörleri", "sub")],
         [("Hücre şişmesi", "magb"), ("ozmotik nefroz: hidroksietil", "sub"), ("nişasta, IVIG (sükroz), mannitol", "sub"), ("gentamisin: fosfolipidoz", "sub")],
         [("Kronik interstisyel nefrit", "magb"), ("lityum, kalsinörin inhibitörleri,", "sub"), ("sisplatin, analjezik karışımları,", "sub"), ("aristolokik asit", "sub")],
         [("Taşıma kusurları", "magb"), ("lityum: nefrojenik DI", "sub"), ("amfoterisin: distal RTA, K⁺ ve Mg²⁺ ↓", "sub"), ("setuksimab: Mg²⁺ kaybı", "sub")],
         [("Böbrek dışından: rabdomiyoliz", "magb"), ("statinler, fibratlar, trisiklik", "sub"), ("antidepresanlar, kokain, alkol", "sub"), ("miyoglobin tübülü tıkar", "sub")]]
pitch = 100
for i, n in enumerate(nodes):
    yc = 52 + i * pitch
    parts = n.split("|")
    nh = 44 if len(parts) > 1 else 34
    s.box(250, yc - nh / 2, 140, nh, [(p, "title") for p in parts], kind="key", fs1=11.5, lh=14)
    lh_ = len(left[i])
    hL = 16 + 14 * lh_
    s.box(10, yc - hL / 2, 222, hL, left[i], kind="mag", lh=14, fs2=10.5)
    hR = 16 + 14 * len(right[i])
    s.box(408, yc - hR / 2, 222, hR, right[i], kind="mag" if i < 4 else "normal", lh=14, fs2=10.5)
    s.add(f'<line x1="232" y1="{yc}" x2="250" y2="{yc}" stroke="{MAG}" stroke-width="1.4"/>')
    if i < 4:
        s.add(f'<line x1="390" y1="{yc}" x2="408" y2="{yc}" stroke="{MAG}" stroke-width="1.4"/>')
        nh2 = 44 if i + 1 == 3 else 34
        s.arrow(320, yc + nh / 2, 320, yc + pitch - nh2 / 2 - 3)
save(s, "m56k3_harita")

# ============================================================ Sekil 5.2 aminoglikozid zinciri
s = SVG(640, 416, "Aminoglikozid nefrotoksisitesinin basamakları: süzülme, megalin aracılı endositoz, lizozomda birikim, fosfolipidoz, lizozom yırtılması ve hücre ölümü, oligürisiz ABH", "k3m")
steps = [("Süzülme", "katyonik aminoglikozid glomerülde serbestçe süzülür"),
         ("Bağlanma ve endositoz", "lümen yüzünde fosfolipid ve megaline bağlanır, hücreye alınır"),
         ("Lizozomda birikim", "serum düzeyinin 100-1000 katına ulaşır"),
         ("Fosfolipidoz", "fosfolipazlar inhibe olur, miyeloid cisimcikler, hücre şişer"),
         ("Lizozom yırtılır", "mitokondri hasarı, apoptoz ve nekroz, inflamasyon"),
         ("Oligürisiz ABH", "tedavinin 5-10. günü; distal tutulumda poliüri, K⁺ ve Mg²⁺ kaybı")]
for i, (t, sub) in enumerate(steps):
    y = 10 + i * 70
    s.box(20, y, 380, 46, [(t, "title"), (sub, "sub")], kind="key" if i in (2, 5) else "normal", lh=15, fs2=10.5)
    if i < 5:
        s.arrow(210, y + 46, 210, y + 66)
s.block(210, 136)
s.add(f'<line x1="222" y1="136" x2="430" y2="136" stroke="{MAG}" stroke-width="1.4"/>')
s.box(430, 90, 200, 92, [("Günde tek doz", "magb"), ("tübülün alım kapasitesi", "sub"), ("doyduğu için tek yüksek tepe", "sub"),
                         ("daha az ilaç biriktirir;", "sub"), ("postantibiyotik etki korunur", "sub")], kind="mag", lh=14, fs2=10.5)
s.box(430, 262, 200, 92, [("Risk faktörleri", "title"), ("ileri yaş, böbrek hastalığı,", "sub"), ("hipotansiyon, sepsis, karaciğer", "sub"),
                          ("hastalığı, vankomisin, diğer", "sub"), ("nefrotoksinler", "sub")], lh=14, fs2=10.5)
save(s, "m56k3_aminogl")

print("ok", sorted(f for f in os.listdir(OUT) if f.endswith(".svg")))
