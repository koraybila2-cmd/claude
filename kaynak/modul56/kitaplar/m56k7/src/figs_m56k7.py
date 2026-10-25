import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "build"))
from svglib import SVG, NEU, TXT, CYAN, MAG, FONT, esc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "svg")
os.makedirs(OUT, exist_ok=True)
ACC = "var(--color-accent)"
GRAY = "var(--color-neutral-700)"


def save(s, name):
    s.save(os.path.join(OUT, name + ".svg"))


def lines(s, x, y, rows, anchor="start", lh=14, fs1=12, fs2=10.5):
    for i, (t, st) in enumerate(rows):
        s.text(x, y + i * lh, t, st, anchor, fs1, fs2)


def dot(s, x, y, r=2.4, color=ACC, op=1):
    s.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}" fill-opacity="{op}"/>')


def ring(s, x, y, r, color=ACC, fill="white", fop=1, width=1.3):
    s.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" fill-opacity="{fop}" stroke="{color}" stroke-width="{width}"/>')


def line(s, x1, y1, x2, y2, color=ACC, width=1.6, extra=""):
    s.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"{extra}/>')


def curve(s, d, color=ACC, width=1.6, fill="none", fop=1, extra=""):
    s.add(f'<path d="{d}" fill="{fill}" fill-opacity="{fop}" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{extra}/>')


# ============================================================ Sekil 1.1 kaynak ve konagin tepkisi
s = SVG(640, 262, "Kaynağa göre dermatofitler: antropofilik türler insandan insana geçer ve hafif, kronik enfeksiyon yapar; zoofilik ve jeofilik türler hayvandan ve topraktan geçer, şiddetli ve akut enfeksiyon yapar", "k7a")
tops = [(8, "Antropofilik", "insandan insana", "T. rubrum, T. tonsurans,", "T. schoenleinii, E. floccosum"),
        (222, "Zoofilik", "hayvandan insana", "M. canis (kedi, köpek),", "T. mentagrophytes, T. verrucosum"),
        (436, "Jeofilik", "topraktan insana", "Nannizzia gypsea", "(çiftçi, çömlekçi, arkeolog)")]
for x, t, sub, a, b in tops:
    s.box(x, 8, 196, 76, [(t, "title"), (sub, "sub"), (a, "body"), (b, "body")], fs1=12.5, fs2=10.5, lh=15)
    s.arrow(x + 98, 86, x + 98, 122)
s.box(8, 126, 196, 100, [("Kronik, hafif enfeksiyon", "title"), ("az iltihap, az kaşıntı", "sub"), ("aylar-yıllar sürer", "sub"),
                         ("tip I yanıt: IgE, atopi", "sub"), ("sık; kişiden kişiye yayılır", "sub")], fs1=12.5, fs2=10.5, lh=15)
s.box(222, 126, 410, 100, [("Akut, şiddetli enfeksiyon", "title"), ("güçlü iltihap: kızarıklık, püstül, kerion", "sub"),
                           ("haftalar sürer", "sub"), ("tip IV aşırı duyarlılık, IgG", "sub"), ("tedaviye yanıt çok iyi", "sub")],
      kind="key", fs1=12.5, fs2=10.5, lh=15)
s.arrow(150, 244, 490, 244)
s.text(142, 248, "insana uyum çok", "sub", "end", fs2=10.5)
s.text(498, 248, "insana uyum az", "sub", "start", fs2=10.5)
s.text(320, 238, "konağın tepkisi şiddetlenir", "cyan", "middle", fs2=10.5)
save(s, "m56k7_kaynak")


# ============================================================ Sekil 1.2 sac invazyonu
def hair(s, cx, top, bottom=196, dashed=False, broken=False):
    x0, x1 = cx - 11, cx + 11
    dash = ' stroke-dasharray="3 2"' if dashed else ""
    s.add(f'<ellipse cx="{cx}" cy="{bottom + 3}" rx="15" ry="10" fill="{NEU}" fill-opacity="0.14" stroke="{NEU}" stroke-width="1.2"/>')
    if broken:
        d = (f"M{x0},{bottom} L{x0},{top + 4} L{x0 + 5},{top} L{x0 + 9},{top + 5} L{x0 + 13},{top - 1} "
             f"L{x0 + 17},{top + 5} L{x1},{top + 1} L{x1},{bottom}")
    else:
        d = f"M{x0},{bottom} L{x0},{top + 8} Q{x0},{top} {cx},{top} Q{x1},{top} {x1},{top + 8} L{x1},{bottom}"
    s.add(f'<path d="{d}" fill="{NEU}" fill-opacity="0.07" stroke="{NEU}" stroke-width="1.3"{dash}/>')


s = SVG(640, 304, "Tinea kapitiste saç invazyonu: endotrikste sporlar saçın içinde, favik invazyonda saçın içinde hifa ve hava boşlukları, ektotrikste sporlar saçın dışında; saçı tutmayan türlerde mantar yalnızca deridedir", "k7b")
panels = [("Endotriks", [("T. tonsurans, T. violaceum", "body"), ("(T. schoenleinii)", "body")],
           [("siyah nokta: saç deri", "cyan"), ("hizasında kırılır", "cyan")]),
          ("Favik", [("T. schoenleinii", "body")], [("skutula, kalıcı", "cyan"), ("alopesi", "cyan")]),
          ("Ektotriks", [("M. canis, M. audouinii,", "body"), ("N. gypsea, T. verrucosum,", "body"), ("T. mentagrophytes", "body")],
           [("kütikula yıkılır;", "cyan"), ("saç geri çıkar", "cyan")]),
          ("Saçı tutmaz", [("T. rubrum, T. concentricum,", "body"), ("T. simii; Epidermophyton", "body")],
           [("mantar yalnızca deride", "cyan")])]
for i, (title, spp, res) in enumerate(panels):
    x0 = 8 + i * 158
    cx = x0 + 75
    s.text(cx, 18, title, "title", "middle", fs1=12.5)
    s.add(f'<rect x="{x0}" y="150" width="150" height="66" fill="{NEU}" fill-opacity="0.06"/>')
    line(s, x0, 150, x0 + 150, 150, NEU, 1.2)
    if i == 0:
        s.text(x0 + 2, 145, "deri yüzeyi", "small")
        hair(s, cx, 134, broken=True)
        for yy in range(142, 192, 7):
            for dx in (-6, 0, 6):
                dot(s, cx + dx, yy + (2 if dx == 0 else 0), 2.3)
    elif i == 1:
        hair(s, cx, 36)
        curve(s, f"M{cx - 4},192 C{cx - 8},170 {cx},150 {cx - 4},128 S{cx - 2},90 {cx - 5},60", ACC, 1.6)
        curve(s, f"M{cx + 4},192 C{cx + 8},166 {cx},146 {cx + 5},120 S{cx + 3},84 {cx + 4},70", ACC, 1.6)
        for yy, dx in ((52, 2), (78, -2), (96, 3), (114, -3), (138, 2), (160, -2), (176, 3)):
            ring(s, cx + dx, yy, 2.6, NEU, "white", 1, 1)
        curve(s, f"M{cx - 34},146 Q{cx - 30},158 {cx - 12},157 L{cx + 12},157 Q{cx + 30},158 {cx + 34},146 "
                 f"Q{cx + 20},151 {cx + 12},148 L{cx - 12},148 Q{cx - 20},151 {cx - 34},146 Z", ACC, 1.2, ACC, 0.35)
        s.text(cx + 38, 140, "skutula", "small")
    elif i == 2:
        hair(s, cx, 100, dashed=True, broken=True)
        for yy in range(104, 194, 7):
            for dx in (-13, 13):
                dot(s, cx + dx, yy + (3 if dx > 0 else 0), 2.4)
    else:
        hair(s, cx, 36)
        for k in range(3):
            yy = 152 + k * 2.2
            curve(s, f"M{x0 + 6},{yy} q8,-3 16,0 t16,0 t16,0 t16,0", ACC, 1.3)
            curve(s, f"M{cx + 16},{yy} q8,-3 16,0 t16,0 t16,0 t8,0", ACC, 1.3)
    lines(s, cx, 234, spp, "middle", lh=14, fs2=10.5)
    lines(s, cx, 234 + 14 * len(spp) + 8, res, "middle", lh=14, fs2=10.5)
save(s, "m56k7_sac")


# ============================================================ Sekil 1.3 siklohekzimid secicilik
s = SVG(640, 236, "Siklohekzimidin seçiciliği: siklohekzimidsiz besiyerinde hızlı üreyen küfler petriyi kaplar; siklohekzimidli besiyerinde küfler baskılanır, dermatofit iki-üç haftada ürer; Cryptococcus neoformans da baskılanır", "k7c")
s.box(8, 82, 128, 72, [("Örnek", "title"), ("deri, saç, tırnak", "sub"), ("+ çevreden küf sporu", "sub"), ("+ deri bakterileri", "sub")],
      fs1=12.5, fs2=10.5, lh=14)
s.arrow(138, 104, 172, 72)
s.arrow(138, 132, 172, 164)
for cy in (58, 178):
    ring(s, 214, cy, 40, NEU, NEU, 0.05, 1.3)
import random
rnd = random.Random(7)
for _ in range(46):
    a = rnd.uniform(0, 2 * math.pi)
    r = 34 * math.sqrt(rnd.uniform(0, 1))
    x, y = 214 + r * math.cos(a), 58 + r * math.sin(a)
    b = rnd.uniform(0, 2 * math.pi)
    curve(s, f"M{x:.1f},{y:.1f} q{4 * math.cos(b):.1f},{4 * math.sin(b):.1f} {8 * math.cos(b + 0.6):.1f},{8 * math.sin(b + 0.6):.1f}",
          GRAY, 1.1, extra=' stroke-opacity="0.75"')
ring(s, 214, 178, 11, ACC, ACC, 0.35, 1.4)
for x, y in ((190, 160), (236, 196), (200, 204), (238, 160), (186, 190)):
    dot(s, x, y, 1.6, GRAY, 0.6)
s.text(266, 32, "Siklohekzimidsiz SDA", "title", fs1=12)
lines(s, 266, 50, [("Saprofit küfler 1-3 günde", "body"), ("petriyi kaplar. Yavaş", "body"), ("üreyen dermatofit", "body"), ("görülemez.", "body")], lh=14)
s.text(266, 150, "SDA + siklohekzimid", "magb", fs2=12)
lines(s, 266, 166, [("(Aktidion) + kloramfenikol", "sub"), ("Küf ve bakteri baskılanır.", "body"), ("Dermatofit 2-3 haftada", "body"), ("tek başına ürer.", "body")], lh=14)
s.box(452, 14, 180, 96, [("Siklohekzimide dirençli", "title"), ("ürer", "cyan"), ("dermatofitler (Onygenales)", "body"),
                         ("Candida albicans ve", "body"), ("mayaların çoğu", "body")], kind="key", fs1=12, fs2=10.5, lh=14)
s.box(452, 124, 180, 100, [("Siklohekzimide duyarlı", "title"), ("baskılanır", "mag"), ("Aspergillus, Penicillium,", "body"),
                           ("Mucorales gibi küfler", "body"), ("Cryptococcus neoformans", "magb")], kind="mag", fs1=12, fs2=10.5, lh=14)
save(s, "m56k7_siklo")


# ============================================================ Sekil 1.4 mikroskopi
s = SVG(640, 240, "Laktofenol pamuk mavisiyle boyanmış kültür preparatında cinsleri ayırtan yapılar: Trichophyton'da bol mikrokonidya, Microsporum'da kalın duvarlı iğ biçimli makrokonidya, Nannizzia'da ince duvarlı makrokonidyalar, Epidermophyton'da grup makrokonidya, T. schoenleinii'de kel şamdanı ve klamidyokonidya", "k7d")
cxs = [8 + i * 126 + 62 for i in range(5)]


def micro(s, x, y, ang):
    """kisa sap + damla bicimli mikrokonidya"""
    ex, ey = x + 7 * math.cos(ang), y + 7 * math.sin(ang)
    line(s, x, y, ex, ey, ACC, 1.1)
    s.add(f'<ellipse cx="{ex + 3.5 * math.cos(ang):.1f}" cy="{ey + 3.5 * math.sin(ang):.1f}" rx="4.2" ry="3" '
          f'transform="rotate({math.degrees(ang):.0f} {ex + 3.5 * math.cos(ang):.1f} {ey + 3.5 * math.sin(ang):.1f})" '
          f'fill="{ACC}" fill-opacity="0.35" stroke="{ACC}" stroke-width="1"/>')


# 1 Trichophyton
cx = cxs[0]
curve(s, f"M{cx},158 C{cx - 2},130 {cx + 2},90 {cx},34", ACC, 1.8)
curve(s, f"M{cx},104 C{cx + 10},90 {cx + 20},76 {cx + 34},58", ACC, 1.6)
for k, yy in enumerate(range(42, 152, 11)):
    side = 1 if k % 2 else -1
    micro(s, cx + (0.5 if side > 0 else -0.5), yy, 0 if side > 0 else math.pi)
for t in (0.25, 0.55, 0.85):
    x, y = cx + 34 * t, 104 - 46 * t
    micro(s, x, y, -math.pi / 2 - 0.5)
s.add(f'<rect x="{cx - 50}" y="62" width="11" height="46" rx="5.5" fill="{ACC}" fill-opacity="0.12" stroke="{ACC}" stroke-width="1.1"/>')
for yy in (74, 85, 96):
    line(s, cx - 49, yy, cx - 40, yy, ACC, 1)
curve(s, f"M{cx - 0.5},146 Q{cx - 34},140 {cx - 44.5},108", ACC, 1.3)

# 2 Microsporum canis
cx = cxs[1]
curve(s, f"M{cx - 56},146 C{cx - 30},140 {cx + 10},150 {cx + 56},142", ACC, 1.8)
curve(s, f"M{cx - 30},144 L{cx - 34},108", ACC, 1.4)
spindle = f"M{cx - 48},100 Q{cx},64 {cx + 48},100 Q{cx},136 {cx - 48},100 Z"
curve(s, spindle, ACC, 2.6, ACC, 0.12)
for dx in (-30, -18, -6, 6, 18, 30):
    h = 18 * (1 - (dx / 48) ** 2) - 3
    line(s, cx + dx, 100 - h, cx + dx, 100 + h, ACC, 1.1)
for dx, dy in ((40, -6), (44, -3), (36, -9), (-40, 6), (-44, 3), (-36, 9), (42, 6), (-42, -6)):
    line(s, cx + dx, 100 + dy, cx + dx + (2 if dx > 0 else -2), 100 + dy + (-2 if dy < 0 else 2), ACC, 1)

# 3 Nannizzia gypsea
cx = cxs[2]
curve(s, f"M{cx - 56},148 C{cx - 20},142 {cx + 20},152 {cx + 56},144", ACC, 1.8)
for ex, ey, a, hx in ((cx - 28, 112, -35, cx - 40), (cx + 1, 98, -90, cx + 1), (cx + 30, 112, 35, cx + 42)):
    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
    ends = [(ex + 19 * ca, ey + 19 * sa), (ex - 19 * ca, ey - 19 * sa)]
    lx, ly = max(ends, key=lambda e: e[1])
    line(s, hx, 147, lx, ly, ACC, 1.2)
    s.add(f'<g transform="rotate({a} {ex} {ey})">'
          f'<ellipse cx="{ex}" cy="{ey}" rx="19" ry="8" fill="{ACC}" fill-opacity="0.12" stroke="{ACC}" stroke-width="1.2"/>'
          + "".join(f'<line x1="{ex + d}" y1="{ey - 7 * math.sqrt(max(0, 1 - (d / 19) ** 2)) + 0.6:.1f}" x2="{ex + d}" '
                    f'y2="{ey + 7 * math.sqrt(max(0, 1 - (d / 19) ** 2)) - 0.6:.1f}" stroke="{ACC}" stroke-width="1"/>' for d in (-9.5, 0, 9.5))
          + "</g>")

# 4 Epidermophyton floccosum
cx = cxs[3]
curve(s, f"M{cx - 56},148 C{cx - 20},142 {cx + 20},152 {cx + 56},144", ACC, 1.8)
line(s, cx, 147, cx, 132, ACC, 1.4)
club = "M-2.5,0 C-4,-14 -10,-26 -9,-34 Q0,-50 9,-34 C10,-26 4,-14 2.5,0 Z"
for a in (-44, 0, 44):
    sep = "".join(f'<line x1="{-w}" y1="{y}" x2="{w}" y2="{y}" stroke="{ACC}" stroke-width="1"/>'
                  for y, w in ((-16, 4.5), (-25, 7.5), (-34, 8.4)))
    s.add(f'<g transform="translate({cx} 132) rotate({a}) scale(1.2)">'
          f'<path d="{club}" fill="{ACC}" fill-opacity="0.14" stroke="{ACC}" stroke-width="1.1"/>{sep}</g>')

# 5 T. schoenleinii
cx = cxs[4]
curve(s, f"M{cx},158 C{cx - 2},130 {cx + 2},100 {cx},74", ACC, 1.8)
for (bx, by, ex, ey) in ((cx, 74, cx - 24, 52), (cx, 74, cx + 24, 52), (cx, 112, cx - 32, 96)):
    curve(s, f"M{bx},{by} Q{(bx + ex) / 2},{by - 4} {ex},{ey}", ACC, 1.6)
    for dx, dy in ((-10, -12), (8, -12)):
        curve(s, f"M{ex},{ey} q{dx / 2},{dy / 3} {dx},{dy}", ACC, 1.4)
        dot(s, ex + dx, ey + dy, 3.2, ACC, 0.55)
for yy in (126, 142):
    ring(s, cx + 0.5, yy, 5.5, ACC, ACC, 0.25, 1.8)

labels = [("Trichophyton", [("bol mikrokonidya", "body"), ("makrokonidya az", "sub")]),
          ("Microsporum", [("kalın duvarlı, iğ", "body"), ("biçimli makrokonidya", "body"), ("M. canis: 6+ bölme", "sub")]),
          ("Nannizzia", [("ince duvarlı, elips", "body"), ("makrokonidyalar", "body"), ("N. gypsea: bol", "sub")]),
          ("Epidermophyton", [("grup makrokonidya", "body"), ("mikrokonidya yok", "cyanb")]),
          ("T. schoenleinii", [("kel şamdanı", "body"), ("klamidyokonidya", "body"), ("mikrokonidya yok", "cyanb")])]
for cx, (t, rows) in zip(cxs, labels):
    s.text(cx, 182, t, "title", "middle", fs1=12)
    lines(s, cx, 198, rows, "middle", lh=14, fs2=10.5)
save(s, "m56k7_mikro")


# ============================================================ Sekil 2.1 Rhizopus ve mukormikoz
s = SVG(640, 306, "Solda Rhizopus'un laktofenol pamuk mavisiyle görülen yapıları: stolon, rizoid, sporanjiyofor, sporanjium, kolumella; sağda rinoorbitoserebral mukormikozun gelişimi: sporların solunması, savunmanın bozulması, anjioinvazyon, nekroz ve orbitaya, beyne yayılım", "k7e")
s.text(122, 18, "Rhizopus (LPCB)", "title", "middle", fs1=12.5)
curve(s, "M14,262 Q57,255 100,262 T186,262 L230,259", ACC, 1.8)
for nx, top, rr in ((100, 108, 28), (186, 172, 15)):
    for dx, dy in ((-10, 20), (-2, 26), (8, 22), (14, 14)):
        curve(s, f"M{nx},262 q{dx / 2},{dy / 2 + 2} {dx},{dy}", ACC, 1.3)
        curve(s, f"M{nx + dx * 0.6},{262 + dy * 0.62} l{(4 if dx >= 0 else -4)},5", ACC, 1)
    line(s, nx, 262, nx, top + rr, ACC, 2)
    scy = top + rr - rr
    ring(s, nx, top, rr, ACC, ACC, 0.12, 1.6)
    curve(s, f"M{nx - rr * 0.42},{top + rr * 0.95} Q{nx - rr * 0.42},{top + rr * 0.1} {nx},{top + rr * 0.1} "
             f"Q{nx + rr * 0.42},{top + rr * 0.1} {nx + rr * 0.42},{top + rr * 0.95}", ACC, 1.4, "white", 1)
    rnd = random.Random(nx)
    n = 0
    while n < (34 if rr > 20 else 10):
        a, r = rnd.uniform(0, 2 * math.pi), rr * 0.86 * math.sqrt(rnd.uniform(0, 1))
        x, y = nx + r * math.cos(a), top + r * math.sin(a)
        if abs(x - nx) < rr * 0.5 and y > top + rr * 0.02:
            continue
        dot(s, x, y, 1.7, ACC, 0.9)
        n += 1
line(s, 122, 90, 136, 80, NEU, 1)
lines(s, 138, 76, [("sporanjium, içinde", "small"), ("sporanjiosporlar", "small")], lh=12)
line(s, 108, 120, 136, 112, NEU, 1)
s.text(138, 115, "kolumella", "small")
s.text(106, 190, "sporanjiyofor", "small")
s.text(140, 254, "stolon", "small")
line(s, 70, 290, 88, 282, NEU, 1)
s.text(66, 294, "rizoid", "small", "end")

s.text(377, 18, "Rinoorbitoserebral mukormikoz", "title", "middle", fs1=12.5)
chain = [("Sporlar solunur", "burunda ve sinüslerde tutulur", "normal"),
         ("Savunma bozuk: spor çimlenir", "nötropeni, ketoasidoz, steroid", "normal"),
         ("Anjioinvazyon", "hifa damar duvarına girer, tromboz", "key"),
         ("Enfarkt ve nekroz", "damakta, burunda siyah eskar", "normal"),
         ("Yayılım: sinüs → orbita → beyin", "günler içinde; proptozis, görme kaybı", "normal")]
for i, (t, sub, kind) in enumerate(chain):
    y = 30 + i * 54
    s.box(252, y, 250, 40, [(t, "title"), (sub, "sub")], kind=kind, fs1=12, fs2=10.5, lh=15)
    if i < 4:
        s.arrow(377, y + 41, 377, y + 53)
s.box(514, 84, 118, 94, [("Neden diyabet?", "title"), ("asidozda transferrin", "sub"), ("demiri bırakır:", "sub"),
                         ("serbest demir ↑,", "sub"), ("mantar hızla ürer", "sub")], kind="none", fs1=11, fs2=10, lh=14, fill="none")
s.add(f'<rect x="514" y="84" width="118" height="94" rx="4" fill="none" stroke="{NEU}" stroke-opacity="0.35" stroke-dasharray="4 3"/>')
s.arrow(513, 104, 505, 104)
s.box(514, 192, 118, 94, [("Tedavi", "magb"), ("cerrahi debridman", "body"), ("+ amfoterisin B", "body"), ("+ risk faktörünün", "body"),
                          ("düzeltilmesi", "body"), ("vorikonazol etkisiz", "mag")], kind="mag", fs1=11, fs2=10, lh=13)
s.arrow(513, 212, 505, 212, MAG)
save(s, "m56k7_mukor")


# ============================================================ Sekil 2.2 Aspergillus yelpazesi
s = SVG(640, 298, "Aspergillus hastalıklarının yelpazesi: aşırı bağışıklık yanıtında alerjik hastalıklar (tanı IgE), normal yanıtta kavitede aspergilloma, yetersiz yanıtta invaziv aspergilloz (tanı galaktomannan)", "k7f")
s.text(320, 16, "Konağın bağışıklık yanıtı", "title", "middle", fs1=11.5)
s.add(f'<line x1="60" y1="30" x2="580" y2="30" stroke="{NEU}" stroke-width="1.5" marker-start="url(#k7f)" marker-end="url(#k7f)"/>')
s.text(60, 46, "aşırı", "sub", "start")
s.text(320, 46, "normal", "sub", "middle")
s.text(580, 46, "yetersiz", "sub", "end")
cols = [(8, "key", "Alerjik hastalıklar", ["ABPA, alerjik fungal", "sinüzit, astım alevlenmesi"],
         ["astım, kistik fibrozis, atopi"], ["mantar bronşta çoğalır,", "dokuya girmez; IgE (tip I)", "ve IgG (tip III) yanıtı"],
         [("total ve özgül IgE ↑,", "cyanb"), ("eozinofili", "cyanb")]),
        (220, "normal", "Aspergilloma", ["kavitede mantar topu;", "kronik pulmoner aspergilloz"],
         ["eski tüberküloz kavitesi,", "yapısal akciğer hastalığı"], ["mantar boşlukta çoğalır,", "dokuya girmez"],
         [("görüntüleme,", "sub"), ("Aspergillus IgG", "sub")]),
        (432, "key", "İnvaziv aspergilloz", ["akciğerde kanamalı enfarkt,", "yaygın enfeksiyon"],
         ["nötropeni, kök hücre nakli,", "yüksek doz steroid"], ["hifa dokuya ve damar", "duvarına girer (anjioinvazyon)"],
         [("serumda ve BAL'da", "cyanb"), ("galaktomannan", "cyanb")])]
for x, kind, t, dis, kim, nasil, tani in cols:
    s.box(x, 58, 200, 232, [], kind=kind)
    tx = x + 12
    s.text(tx, 80, t, "title", fs1=12.5)
    lines(s, tx, 98, [(d, "body") for d in dis])
    s.text(tx, 134, "KİMDE", "cap")
    lines(s, tx, 148, [(d, "body") for d in kim])
    s.text(tx, 184, "NASIL", "cap")
    lines(s, tx, 198, [(d, "body") for d in nasil])
    s.text(tx, 248, "TANI", "cap")
    lines(s, tx, 262, tani)
save(s, "m56k7_asper")
print("ok")
