import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "build"))
from svglib import SVG, NEU, TXT, CYAN, MAG, FONT, esc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "svg")
os.makedirs(OUT, exist_ok=True)
ACC = "var(--color-accent)"


def save(s, name):
    s.save(os.path.join(OUT, name + ".svg"))


def bar(s, x, w, base, top, color):
    h = base - top
    if h <= 0:
        return
    r = min(4, w / 2, h)
    s.add(f'<path d="M{x:.1f},{base:.1f} L{x:.1f},{top + r:.1f} Q{x:.1f},{top:.1f} {x + r:.1f},{top:.1f} '
          f'L{x + w - r:.1f},{top:.1f} Q{x + w:.1f},{top:.1f} {x + w:.1f},{top + r:.1f} L{x + w:.1f},{base:.1f} Z" fill="{color}"/>')


# ============================================================ Sekil 1.1 damar agaci
s = SVG(640, 500, "Böbreğin damar ağacı: renal arterden afferent arteriole, glomerülden efferent arteriol ve ikinci kapiller yatağa", "k1a")
L = [("Renal arter", "aorttan"),
     ("Segmental arterler", "hilusta; uç arter, anastomoz yok"),
     ("İnterlober arterler", "piramitlerin arasından yükselir"),
     ("Arkuat arterler", "korteks-medulla sınırında kavis"),
     ("İnterlobüler (kortikal radyal) arterler", "kortekse dik yükselir"),
     ("Afferent arteriol", "giriş direnci"),
     ("Glomerül kapillerleri", "1. kapiller yatak: yüksek basınç, süzer"),
     ("Efferent arteriol", "çıkış direnci"),
     ("Peritübüler kapillerler · vasa recta", "2. kapiller yatak: düşük basınç, geri emer"),
     ("Venler", "interlobüler → arkuat → interlober → renal ven")]
x, w, h, step, y0 = 30, 330, 36, 48, 10
for i, (t, sub) in enumerate(L):
    y = y0 + i * step
    kind = "key" if i in (6, 8) else "normal"
    s.box(x, y, w, h, [t, sub], kind=kind, fs1=12, fs2=10, lh=13)
    if i < len(L) - 1:
        s.arrow(x + w / 2, y + h, x + w / 2, y + step - 2)
# sag aciklamalar
s.add(f'<path d="M372,{y0 + 5 * step + 4} L384,{y0 + 5 * step + 4} L384,{y0 + 7 * step + h - 4} L372,{y0 + 7 * step + h - 4}" fill="none" stroke="{CYAN}" stroke-width="1.3"/>')
yy = y0 + 6 * step + 4
s.text(394, yy, "Glomerül iki arteriol arasında:", "cyanb", fs2=11)
s.text(394, yy + 15, "afferent daralırsa basınç düşer,", "body", fs2=10.5)
s.text(394, yy + 29, "efferent daralırsa basınç yükselir.", "body", fs2=10.5)
s.text(394, yy + 43, "(otoregülasyon: Bölüm 2.4)", "sub", fs2=10)
yb = y0 + 8 * step + 6
s.text(394, yb, "Vasa recta jukstamedüller", "body", fs2=10.5)
s.text(394, yb + 14, "nefronların efferentinden çıkar.", "body", fs2=10.5)
s.text(394, y0 + 4 * step + 22, "Soru 1.2 → afferent arteriolün", "mag", fs2=10.5)
s.text(394, y0 + 4 * step + 36, "kökeni interlobüler arterdir", "mag", fs2=10.5)
s.text(394, y0 + 1 * step + 22, "Böbrek kan akımı ≈1,2 L/dk", "body", fs2=10.5)
s.text(394, y0 + 1 * step + 36, "= kalp debisinin ≈%20'si", "body", fs2=10.5)
save(s, "m56k1_damar")

# ============================================================ Sekil 2.1 Starling
s = SVG(640, 318, "Glomerülde Starling güçleri ve net filtrasyon basıncı", "k1b")
s.box(30, 14, 580, 64, [("Glomerül kapilleri (kan)", "title"), ("plazma proteinleri burada kalır", "sub")], fill="white")
s.add(f'<line x1="30" y1="124" x2="610" y2="124" stroke="{NEU}" stroke-opacity="0.55" stroke-width="2"/>')
s.text(168, 118, "filtrasyon bariyeri", "small")
s.box(30, 170, 580, 64, [("Bowman boşluğu (süzüntü)", "title"), ("proteinsiz, plazmayla izotonik", "sub")], fill="white")
# kuvvetler
s.arrow(130, 80, 130, 166, color=CYAN, width=2.2)
s.text(140, 138, "P", "cyanb", fs2=12); s.text(149, 141, "GK", "cyan", fs2=8.5)
s.text(140, 154, "≈45 mmHg · iter", "cyanb", fs2=10.5)
s.arrow(285, 166, 285, 82, width=1.8)
s.text(295, 138, "π", "title", fs1=12); s.text(303, 141, "GK", "sub", fs2=8.5)
s.text(295, 154, "≈25 mmHg · tutar", "body", fs2=10.5)
s.arrow(440, 166, 440, 82, width=1.8)
s.text(450, 138, "P", "title", fs1=12); s.text(458, 141, "B", "sub", fs2=8.5)
s.text(450, 154, "≈10 mmHg · geri iter", "body", fs2=10.5)
s.text(560, 104, "π", "title", fs1=12); s.text(568, 107, "B", "sub", fs2=8.5)
s.text(560, 120, "≈0", "body", fs2=10.5)
s.text(560, 148, "süzüntüde", "small"); s.text(560, 160, "protein yok", "small")
s.box(120, 252, 400, 52, [("Net filtrasyon basıncı = (45 + 0) − (25 + 10) ≈ 10 mmHg", "title"),
                          ("küçük bir fark: birkaç mmHg'lik değişiklik GFR'yi belirgin etkiler", "sub")], kind="key", fs1=12.5, fs2=10.5)
save(s, "m56k1_starling")

# ============================================================ Sekil 2.2 otoregulasyon / TGF
s = SVG(640, 400, "Perfüzyon düşünce GFR'yi koruyan yanıtlar: afferent dilatasyon, renin-anjiyotensin II ile efferent daralma", "k1c")
s.box(190, 10, 260, 46, [("Perfüzyon basıncı ↓", "title"), ("glomerül basıncı ve GFR düşme eğiliminde", "sub")])
# sol dal
s.box(20, 92, 190, 50, [("Miyojenik yanıt", "title"), ("afferent duvarı daha az gerilir", "sub")])
s.box(225, 92, 190, 50, [("Makula densada NaCl ↓", "title"), ("tübül sıvısı yavaş, NaCl az", "sub")])
s.box(430, 92, 190, 50, [("Renin ↑", "title"), ("granüler hücreler; + sempatik β1", "sub")])
for cx in (115, 320, 525):
    s.path(f"M320,56 L320,72 L{cx},72 L{cx},88")
s.box(20, 182, 395, 50, [("Afferent arteriol genişler", "title"), ("adenozinin daraltıcı etkisi azalır; glomerüle daha çok kan girer", "sub")], kind="key")
s.arrow(115, 142, 115, 178); s.arrow(320, 142, 320, 178)
s.box(430, 168, 190, 40, [("Anjiyotensin II ↑", "title")])
s.arrow(525, 142, 525, 164)
s.box(430, 236, 190, 50, [("Efferent arteriol daralır", "title"), ("glomerülün çıkışı kısılır", "sub")], kind="key")
s.arrow(525, 208, 525, 232)
s.box(20, 262, 395, 40, [("Mezangial hücreler gevşer → filtrasyon yüzeyi ↑", "title")])
s.box(170, 330, 300, 48, [("Glomerül basıncı ve GFR korunur", "title"), ("I + II + III birlikte (Soru 2.6)", "cyan")], kind="key")
s.path("M217,232 L217,252 L217,258", marker=True)
s.path("M217,302 L217,312 L300,312 L300,326")
s.path("M525,286 L525,312 L340,312 L340,326")
s.text(20, 392, "Ters yön: GFR ↑ → makula densaya NaCl ↑ → adenozin (A1) → afferent daralır → GFR ↓, renin ↓", "mag", fs2=10.5)
save(s, "m56k1_tgf")

# ============================================================ Sekil 3.1 Na emilimi
s = SVG(640, 250, "Süzülen sodyumun nefron segmentlerine göre geri emilim yüzdesi", "k1d")
cats = [("Proksimal tübül", 65, "%65"), ("Kalın çıkan kol", 25, "%25"), ("Distal kıvrımlı tübül", 6, "%5-8"),
        ("Toplayıcı kanal", 3, "%2-5"), ("İdrarla atılan", 0.8, "<%1")]
x0, x1, yt, yb = 50, 620, 20, 196
for v in (0, 20, 40, 60):
    y = yb - (yb - yt) * v / 70
    s.add(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{NEU}" stroke-opacity="{0.45 if v == 0 else 0.15}" stroke-width="1"/>')
    s.text(x0 - 6, y + 3.5, f"%{v}", "small", anchor="end")
gw = (x1 - x0) / len(cats)
for i, (lab, v, t) in enumerate(cats):
    cx = x0 + gw * (i + 0.5)
    top = yb - (yb - yt) * v / 70
    bar(s, cx - 12, 24, yb, top, ACC)
    s.text(cx, top - 6, t, "body", anchor="middle", fs2=11)
    s.text(cx, yb + 16, lab, "body", anchor="middle", fs2=10.5)
s.text(x0 + gw * 2.5, yb + 34, "ince ayar: aldosteron, NCC/ENaC → hedeflenen diüretikler (Kitap 3)", "sub", anchor="middle", fs2=10)
save(s, "m56k1_na_emilim")

# ============================================================ Sekil 4.1 RAAS
s = SVG(640, 420, "Renin-anjiyotensin-aldosteron sistemi", "k1e")
s.box(20, 10, 185, 44, [("Afferent perfüzyon ↓", "title"), ("hipovolemi, darlık, KY", "sub")])
s.box(227, 10, 186, 44, [("Makula densada NaCl ↓", "title"), ("hiponatremi, hacim azlığı", "sub")])
s.box(435, 10, 185, 44, [("Sempatik β1 uyarısı", "title"), ("ayağa kalkma, kanama", "sub")])
s.box(230, 82, 180, 40, [("Renin ↑ (granüler hücre)", "title")], kind="key")
for cx in (112, 320, 528):
    s.path(f"M{cx},54 L{cx},66 L320,66 L320,78") if cx != 320 else s.arrow(320, 54, 320, 78)
s.box(20, 150, 170, 44, [("Anjiyotensinojen", "title"), ("karaciğer", "sub")])
s.box(235, 150, 170, 44, [("Anjiyotensin I", "title"), ("etkisiz dekapeptid", "sub")])
s.box(450, 150, 170, 44, [("Anjiyotensin II", "title"), ("oktapeptid", "sub")], kind="key")
s.arrow(190, 172, 231, 172); s.arrow(405, 172, 446, 172)
s.text(210, 188, "renin", "cyan", anchor="middle", fs2=10)
s.text(426, 166, "ACE", "cyan", anchor="middle", fs2=10)
s.text(426, 206, "akciğer endoteli", "small", anchor="middle")
s.path("M320,122 L320,136 L210,136 L210,164", color=CYAN)
eff = [("Vazokonstriksiyon", "efferent > afferent", 20, 138), ("Adrenal KORTEKS", "zona glomerulosa → aldosteron", 164, 172),
       ("Proksimal tübül", "Na⁺ emilimi ↑ (NHE3)", 342, 136), ("Susama ve ADH ↑", "su alımı ve tutulması", 484, 136)]
for t, sub, ex, ew in eff:
    s.box(ex, 248, ew, 46, [t, sub], kind="key" if "KORTEKS" in t else "normal", fs1=12, fs2=10)
    s.path(f"M535,194 L535,222 L{ex + ew / 2:.0f},222 L{ex + ew / 2:.0f},244")
s.box(140, 322, 280, 50, [("Aldosteron → toplayıcı kanal esas hücresi", "title"), ("ENaC, Na-K-ATPaz ↑: Na⁺ tutulur; K⁺ ve H⁺ atılır", "sub")], kind="key")
s.arrow(244, 294, 244, 318)
s.box(440, 322, 180, 50, [("Adrenal MEDULLA", "magb"), ("katekolamin; aldosteron DEĞİL", "mag")], kind="mag", fs2=10.5)
# negatif geri bildirim
s.path("M620,172 L632,172 L632,102 L414,102", color=NEU)
s.block(470, 102, length=16)
s.text(476, 96, "negatif geri bildirim", "mag", fs2=10)
s.text(20, 404, "Renini baskılayanlar: perfüzyon ↑, tuz yükü, hipernatremi, anjiyotensin II, ANP.", "sub", fs2=10.5)
save(s, "m56k1_raas")

# ============================================================ Sekil 5.1 kanama yaniti
s = SVG(640, 486, "Kanamaya kompansatuar yanıtlar: sempatik sistem, RAAS, ADH ve otoinfüzyon", "k1f")
s.box(150, 10, 340, 46, [("Kanama: kan hacmi ↓", "title"), ("venöz dönüş, atım hacmi ve arter basıncı düşer", "sub")])
s.box(170, 82, 300, 40, [("Baroreseptörler daha az uyarılır", "title")])
s.arrow(320, 56, 320, 78)
cols = [(20, "Sempatik sistem", "saniyeler", ["Kalp hızı ve kasılma ↑", "Arteriyoler vazokonstriksiyon", "(deri, bağırsak, böbrek)", "VENOKONSTRİKSİYON:", "venlerdeki kan kalbe itilir", "Böbrek kan akımı ↓"]),
        (226, "RAAS", "dakikalar", ["Renin ↑ (3 yoldan)", "Anjiyotensin II ↑", "→ vazokonstriksiyon,", "   efferent daralır", "Aldosteron ↑", "→ renal Na⁺ emilimi ↑"]),
        (432, "ADH", "dakikalar", ["Su tutulur", "İdrar azalır, yoğunlaşır", "V1 → vazokonstriksiyon", "Susama ↑", "", ""])]
for cx, t, sub, items in cols:
    s.add(f'<rect x="{cx}" y="150" width="188" height="150" rx="4" fill="white" stroke="{NEU}" stroke-opacity="0.35"/>')
    s.text(cx + 10, 170, t, "title", fs1=12.5)
    s.text(cx + 178, 170, sub, "small", anchor="end")
    for j, it in enumerate(items):
        if it:
            st = "cyanb" if it.startswith("VENOKON") else "body"
            s.text(cx + 10, 192 + j * 17, it, st, fs2=10.5)
    s.path(f"M320,122 L320,134 L{cx + 94},134 L{cx + 94},146")
s.box(20, 322, 280, 50, [("Kapiller hidrostatik basınç ↓", "title"), ("interstisyel sıvı damara çekilir; ANP ↓", "sub")])
s.box(170, 400, 300, 50, [("Hacim ve arter basıncı korunur", "title"), ("beyin ve kalp perfüzyonu öncelikli", "sub")], kind="key")
s.path("M114,300 L114,312 L114,318")
s.path("M160,372 L160,386 L300,386 L300,396")
s.path("M320,300 L320,396")
s.path("M526,300 L526,386 L340,386 L340,396")
s.text(20, 474, "Hipovolemide beklenmeyen yanıtlar: venöz dilatasyon, ADH ↓, ANP ↑, renin ↓.", "mag", fs2=10.5)
save(s, "m56k1_kanama")

# ============================================================ Sekil 6.1 odem
s = SVG(640, 400, "Kapillerde Starling dengesi ve ödemin dört mekanizması", "k1g")
s.text(20, 22, "arteriyel uç", "small"); s.text(620, 22, "venöz uç", "small", anchor="end")
s.add(f'<rect x="20" y="30" width="600" height="46" rx="23" fill="white" stroke="{NEU}" stroke-opacity="0.5"/>')
s.text(320, 58, "Kapiller (plazma proteinleri, albümin)", "title", anchor="middle", fs1=12)
for xx in (80, 130, 180):
    s.arrow(xx, 78, xx, 118, color=CYAN, width=1.8)
s.text(80, 136, "hidrostatik basınç sıvıyı dışarı iter", "cyanb", fs2=10.5)
for xx in (460, 510, 560):
    s.arrow(xx, 118, xx, 80, width=1.8)
s.text(620, 136, "onkotik basınç (albümin) geri çeker", "body", anchor="end", fs2=10.5)
s.add(f'<rect x="20" y="146" width="600" height="56" rx="4" fill="var(--color-bg)" stroke="none"/>')
s.text(30, 168, "İnterstisyum", "title", fs1=12)
s.text(30, 186, "geri alınamayan küçük fazla → lenfatiklere", "sub", fs2=10.5)
s.add(f'<rect x="440" y="160" width="170" height="30" rx="15" fill="white" stroke="{NEU}" stroke-opacity="0.5"/>')
s.text(525, 180, "lenfatik", "body", anchor="middle", fs2=10.5)
s.arrow(380, 176, 436, 176)
mech = [("1 · Hidrostatik basınç ↑", ["venöz obstrüksiyon", "kalp yetmezliği", "Na⁺ ve sıvı retansiyonu"]),
        ("2 · Onkotik basınç ↓", ["protein kaybı: nefrotik sendrom, PKE", "sentez azalması: KC hastalığı,", "malnütrisyon"]),
        ("3 · Lenfatik drenaj bozukluğu", ["lenfödem: tümör, cerrahi,", "filariyaz"]),
        ("4 · Kapiller geçirgenlik ↑", ["inflamasyon, yanık,", "sepsis, anafilaksi"])]
for i, (t, items) in enumerate(mech):
    bx = 20 + (i % 2) * 305; by = 222 + (i // 2) * 82
    s.add(f'<rect x="{bx}" y="{by}" width="295" height="72" rx="4" fill="white" stroke="{CYAN if i < 2 else NEU}" stroke-opacity="{1 if i < 2 else 0.35}" stroke-width="{1.5 if i < 2 else 1}"/>')
    s.text(bx + 10, by + 20, t, "title", fs1=12)
    for j, it in enumerate(items):
        s.text(bx + 10, by + 38 + j * 14, it, "body", fs2=10.5)
s.text(20, 393, "Ödem nedeni DEĞİL: hiperkalsemi; plazma protein konsantrasyonunun artması (onkotik basıncı yükseltir)", "mag", fs2=10.5)
save(s, "m56k1_odem")

# ============================================================ Sekil 7.1 dansite
s = SVG(640, 190, "İdrar dansitesi ölçeği ve yorumu", "k1h")
x0, x1 = 40, 610
sx = lambda v: x0 + (x1 - x0) * (v - 1000) / 35
yb = 96
s.add(f'<rect x="{sx(1000):.1f}" y="{yb - 30}" width="{sx(1010) - sx(1000):.1f}" height="30" fill="{ACC}" fill-opacity="0.16"/>')
s.add(f'<rect x="{sx(1015):.1f}" y="{yb - 30}" width="{sx(1025) - sx(1015):.1f}" height="30" fill="{NEU}" fill-opacity="0.12"/>')
s.add(f'<rect x="{sx(1030):.1f}" y="{yb - 30}" width="{sx(1035) - sx(1030):.1f}" height="30" fill="var(--color-accent-2)" fill-opacity="0.16"/>')
s.add(f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{NEU}" stroke-width="1.2"/>')
for v in range(1000, 1036, 5):
    s.add(f'<line x1="{sx(v):.1f}" y1="{yb}" x2="{sx(v):.1f}" y2="{yb + 5}" stroke="{NEU}" stroke-width="1"/>')
    s.text(sx(v), yb + 18, str(v), "small", anchor="middle")
s.text(sx(1005), yb - 40, "< 1010: seyreltik", "cyanb", anchor="middle", fs2=10.5)
s.text(sx(1020), yb - 40, "1015-1025: olağan", "body", anchor="middle", fs2=10.5)
s.text(sx(1032.5), yb - 40, "> 1030: yoğun", "magb", anchor="middle", fs2=10.5)
for v, lab in ((1005, "DI ≈1005"), (1010, "izostenüri (KBH)")):
    s.add(f'<circle cx="{sx(v):.1f}" cy="{yb - 15}" r="3.5" fill="{CYAN}"/>')
s.text(sx(1005), yb - 54, "Soru 7.2: DI", "cyan", anchor="middle", fs2=10)
s.text(sx(1010) + 4, yb - 8, "1010 = plazma", "small")
s.text(40, yb + 44, "Seyreltik: diabetes insipidus, psikojenik polidipsi; KBH'de dansite 1010'a sabitlenir (izostenüri).", "body", fs2=10.5)
s.text(40, yb + 62, "Yoğun: diabetes mellitus (glukoz), kontrast madde, dehidratasyon. Fizyolojik aralık 1003-1030.", "body", fs2=10.5)
save(s, "m56k1_dansite")
print("ok")
