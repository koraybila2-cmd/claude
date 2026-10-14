import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "build"))
from svglib import SVG, NEU, TXT, CYAN, MAG

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "svg")


def save(s, name):
    s.save(os.path.join(OUT, name + ".svg"))


# =============================================================== esitsizlik mi, hakkaniyetsizlik mi?
s = SVG(640, 372, "Saglik farkinin esitsizlik mi hakkaniyetsizlik mi oldugunu ayirt etme", "m46a")
s.box(120, 6, 400, 46, [("İki grup arasında sağlık farkı var", "title"), ("örnek: yoksul mahallede bebek ölüm hızı daha yüksek", "sub")], fs1=12, fs2=10.2, lh=15)
s.arrow(320, 52, 320, 72)
s.box(170, 74, 300, 40, [("Fark kaçınılabilir mi?", "title")], kind="key", fs1=12)
s.path("M470,94 L512,94 L512,122")
s.text(491, 88, "hayır", "small", anchor="middle")
s.box(430, 124, 200, 58, [("Doğal, biyolojik fark", "title"), ("yaşlıda kronik hastalık çok,", "sub"), ("yalnız erkekte prostat kanseri", "sub")], fs1=11.4, fs2=9.9, lh=14)
s.arrow(320, 114, 320, 140)
s.text(330, 131, "evet", "small")
s.box(150, 142, 260, 52, [("Fark, kişinin seçimi dışındaki", "title"), ("sosyal koşullardan mı doğuyor?", "title")], kind="key", fs1=11.6, lh=16)
s.path("M150,168 L100,168 L100,212")
s.text(125, 162, "hayır", "small", anchor="middle")
s.box(10, 214, 190, 58, [("Özgürce seçilmiş davranış", "title"), ("tehlikeli spor; ilk benimseyenlerin", "sub"), ("geçici sağlık avantajı", "sub")], fs1=11.2, fs2=9.9, lh=14)
s.arrow(320, 194, 320, 220, MAG)
s.text(330, 211, "evet", "small")
s.box(220, 222, 410, 72, [("HAKKANİYETSİZLİK (inequity)", "magb"),
                          ("kaçınılabilir ve adaletsiz: yoksulluk, eğitimsizlik, kötü konut ve iş", "body"),
                          ("koşulları, seçimi kısıtlayan ortam, sağlık hizmetine erişememe", "body")],
      kind="mag", fs1=12, fs2=10.2, lh=16)
s.arrow(425, 294, 425, 318, CYAN)
s.box(220, 320, 410, 46, [("Hedef: hakkaniyet (equity)", "cyanb"), ("herkesin sağlık potansiyeline tam ulaşabilmesi; politikayla azaltılabilir", "sub")],
      kind="key", fs1=12, fs2=10, lh=15)
s.text(10, 300, "İlk iki kutudaki farklar da birer", "small")
s.text(10, 313, "eşitsizliktir (inequality), ama", "small")
s.text(10, 326, "hakkaniyetsizlik sayılmaz.", "small")
save(s, "m4k6_esit")

# =============================================================== Dahlgren-Whitehead gokkusagi
s = SVG(640, 400, "Sagligin belirleyicileri: Dahlgren ve Whitehead gokkusagi modeli", "m46b")
cx, cy = 320, 330
rings = [(0, 62, 0.62, "Yaş, cinsiyet,", "kalıtsal faktörler"), (62, 118, 0.42, "Bireysel yaşam tarzı", ""),
         (118, 174, 0.30, "Sosyal ve toplumsal ağlar", ""), (174, 238, 0.19, "Yaşam ve çalışma koşulları", ""),
         (238, 300, 0.09, "Genel sosyoekonomik, kültürel ve çevresel koşullar", "")]
for r1, r2, op, t1, t2 in reversed(rings):
    if r1 == 0:
        d = f"M{cx - r2},{cy} A{r2},{r2} 0 0 1 {cx + r2},{cy} Z"
    else:
        d = f"M{cx - r2},{cy} A{r2},{r2} 0 0 1 {cx + r2},{cy} L{cx + r1},{cy} A{r1},{r1} 0 0 0 {cx - r1},{cy} Z"
    s.add(f'<path d="{d}" fill="{CYAN}" fill-opacity="{op}" stroke="white" stroke-width="2"/>')
for r1, r2, op, t1, t2 in rings:
    if r1 == 0:
        s.text(cx, cy - 30, t1, "title", anchor="middle", fs1=10.8)
        s.text(cx, cy - 16, t2, "title", anchor="middle", fs1=10.8)
    else:
        s.text(cx, cy - (r1 + r2) / 2 + 4, t1, "title", anchor="middle", fs1=11.2)
# yasam ve calisma kosullari sektorleri (halka 4 icinde, yanlarda)
for ang, lab in ((160, "konut"), (138, "eğitim"), (118, "iş ortamı"), (62, "işsizlik"), (42, "su, sanitasyon"), (20, "sağlık hizmeti")):
    a = math.radians(ang)
    r = 206
    x, y = cx + r * math.cos(a), cy - r * math.sin(a)
    s.text(x, y + 4, lab, "body", anchor="middle", fs2=9.6)
s.add(f'<line x1="{cx - 305}" y1="{cy}" x2="{cx + 305}" y2="{cy}" stroke="{NEU}" stroke-opacity="0.4"/>')
s.text(20, cy + 22, "İçeriden dışarıya: bireyin değiştirebileceğinden toplumun ve politikanın değiştirebileceğine.", "small")
s.text(20, cy + 36, "Yaşam ve çalışma koşulları halkası ayrıca tarım ve gıda üretimini kapsar (Dahlgren ve Whitehead, 1991).", "small")
s.text(20, cy + 50, "Dış halkalar \"nedenlerin nedenleri\"dir: iç halkalardaki davranış ve riskleri biçimlendirir.", "small")
save(s, "m4k6_gokkusagi")

# =============================================================== zaman cizelgesi
s = SVG(640, 250, "Saglikta esitlik icin uluslararasi belgelerin zaman cizelgesi", "m46c")
X = lambda yr: 30 + (yr - 1940) * (590 / 92)
LY = 130
s.add(f'<line x1="{X(1942)}" y1="{LY}" x2="{X(2031)}" y2="{LY}" stroke="{NEU}" stroke-width="1.6"/>')
s.add(f'<rect x="{X(2000):.1f}" y="{LY - 5}" width="{X(2015) - X(2000):.1f}" height="10" rx="3" fill="{CYAN}" fill-opacity="0.45"/>')
s.add(f'<rect x="{X(2015):.1f}" y="{LY - 5}" width="{X(2030) - X(2015):.1f}" height="10" rx="3" fill="{CYAN}"/>')
s.text((X(2000) + X(2015)) / 2, LY + 20, "BKH 2000-2015", "cyanb", anchor="middle", fs2=9.6)
s.text((X(2015) + X(2030)) / 2, LY + 20, "SKH 2015-2030", "cyanb", anchor="middle", fs2=9.6)
for yr in (1950, 1960, 1970, 1990):
    s.add(f'<line x1="{X(yr):.1f}" y1="{LY - 3}" x2="{X(yr):.1f}" y2="{LY + 3}" stroke="{NEU}"/>')
    s.text(X(yr), LY + 18, str(yr), "small", anchor="middle")
ev = [(1948, -1, "start", ["1948 · DSÖ Anayasası yürürlükte,", "İnsan Hakları Evrensel Beyannamesi"]),
      (1977, 1, "end", ["1977 · DSÖ 30. Asamble:", "\"2000 yılında herkese sağlık\""]),
      (1978, -2, "start", ["1978 · Alma-Ata Bildirgesi:", "temel sağlık hizmetleri"]),
      (1980, 2, "start", ["1980 · Black Raporu", "(İngiltere)"]),
      (2008, -1, "end", ["2008 · DSÖ Dünya Sağlık Raporu,", "Sosyal Belirleyiciler Komisyonu"]),
      (2018, -2, "start", ["2018 · Astana", "Bildirgesi"])]
lv = {-1: 84, -2: 34, 1: 176, 2: 222}
for yr, level, anc, lines in ev:
    x = X(yr)
    y = lv[level]
    y2 = y + 6 if level < 0 else y - 16
    s.add(f'<line x1="{x:.1f}" y1="{LY}" x2="{x:.1f}" y2="{y2}" stroke="{NEU}" stroke-opacity="0.6"/>')
    s.add(f'<circle cx="{x:.1f}" cy="{LY}" r="4" fill="{MAG}"/>')
    tx = x + 4 if anc == "start" else x - 4
    s.text(tx, y - 4 if level < 0 else y, lines[0], "title", anchor=anc, fs1=10.4)
    s.text(tx, (y - 4 if level < 0 else y) + 13, lines[1], "body", anchor=anc, fs2=10)
save(s, "m4k6_zaman")

# =============================================================== anne olum orani
s = SVG(640, 196, "Anne olum orani: ulke gruplari, Turkiye ve SKH hedefi", "m46d")
L, R = 170, 590
X = lambda v: L + (R - L) * v / 500
for v in (0, 100, 200, 300, 400, 500):
    s.add(f'<line x1="{X(v):.1f}" y1="8" x2="{X(v):.1f}" y2="150" stroke="{NEU}" stroke-opacity="0.16"/>')
    s.text(X(v), 166, str(v), "small", anchor="middle")
s.text((L + R) / 2, 184, "100.000 canlı doğumda anne ölümü (2017; Türkiye: sunumdaki son veri)", "small", anchor="middle")
rows = [("Yüksek gelirli ülkeler", 11, NEU), ("Türkiye", 18, CYAN), ("Dünya", 211, NEU), ("Düşük gelirli ülkeler", 462, MAG)]
for i, (lab, v, col) in enumerate(rows):
    y = 14 + i * 34
    s.text(L - 10, y + 14, lab, "plain", anchor="end", fs1=11)
    op = "0.45" if col == NEU else "1"
    s.add(f'<rect x="{L}" y="{y}" width="{max(X(v) - L, 3):.1f}" height="20" rx="4" fill="{col}" fill-opacity="{op}"/>')
    s.text(X(v) + 6, y + 15, str(v), "title", fs1=10.8)
s.add(f'<line x1="{X(70):.1f}" y1="6" x2="{X(70):.1f}" y2="150" stroke="{MAG}" stroke-width="1.5" stroke-dasharray="4 3"/>')
s.text(X(70) + 5, 50, "SKH 3.1 hedefi: < 70", "magb", fs2=9.8)
save(s, "m4k6_mmr")

# =============================================================== Turkiye: hizmet kapsami (dumbbell)
def dumbbell(name, label, rows, vmax, unit, ticks, high_good, title_note):
    n = len(rows)
    H = 44 + n * 24 + 46
    s = SVG(640, H, label, name)
    L, R = 250, 600
    X = lambda v: L + (R - L) * v / vmax
    top = 30
    for v in ticks:
        s.add(f'<line x1="{X(v):.1f}" y1="{top - 8}" x2="{X(v):.1f}" y2="{top + n * 24 - 6}" stroke="{NEU}" stroke-opacity="0.16"/>')
        s.text(X(v), top + n * 24 + 8, f"{v}", "small", anchor="middle")
    s.text((L + R) / 2, top + n * 24 + 24, unit, "small", anchor="middle")
    for i, (lab, a, b) in enumerate(rows):
        y = top + i * 24
        s.text(L - 12, y + 4, lab, "plain", anchor="end", fs1=10.6)
        s.add(f'<line x1="{X(a):.1f}" y1="{y}" x2="{X(b):.1f}" y2="{y}" stroke="{NEU}" stroke-opacity="0.5" stroke-width="3"/>')
        good, bad = (b, a) if high_good else (a, b)
        s.add(f'<circle cx="{X(bad):.1f}" cy="{y}" r="5.5" fill="{MAG}" stroke="white" stroke-width="2"/>')
        s.add(f'<circle cx="{X(good):.1f}" cy="{y}" r="5.5" fill="{CYAN}" stroke="white" stroke-width="2"/>')
        fmt = lambda v: (f"{v:.1f}".replace(".", ",") if v != int(v) else str(int(v)))
        s.text(X(min(a, b)) - 9, y + 4, fmt(min(a, b)), "small", anchor="end")
        s.text(X(max(a, b)) + 9, y + 4, fmt(max(a, b)), "small")
    yl = 10
    s.add(f'<circle cx="{L}" cy="{yl}" r="5" fill="{CYAN}"/>')
    s.text(L + 9, yl + 4, "en iyi durumdaki alt grup", "body", fs2=10)
    s.add(f'<circle cx="{L + 170}" cy="{yl}" r="5" fill="{MAG}"/>')
    s.text(L + 179, yl + 4, "en kötü durumdaki alt grup", "body", fs2=10)
    s.text(10, H - 6, title_note, "small")
    save(s, name)

dumbbell("m4k6_tr_kapsam", "Turkiyede alt gruplar arasinda hizmet kapsami farklari",
         [("Tüm aşıları tamamlayanlar (1 yaş)", 29.3, 70.6), ("Polio aşısı", 49.2, 83.2), ("Doğum öncesi bakım: ≥ 4 ziyaret", 69.8, 98.7),
          ("AP talebi: modern yöntemle karşılanan", 50, 68), ("Modern AP yöntemi kullanımı", 37, 54), ("DTP aşısı (1 yaş)", 78.1, 92.2),
          ("Erken emzirmeye başlama", 58.0, 70.4), ("Kızamık aşısı (1 yaş)", 80.8, 91.9), ("Nitelikli personelle doğum", 91.1, 99.8),
          ("Doğum öncesi bakım: ≥ 1 ziyaret", 91.2, 99.7), ("BCG aşısı (1 yaş)", 91.5, 97.9)],
         100, "kapsam (%)", (0, 20, 40, 60, 80, 100), True,
         "Satırlar iki uç arasındaki farka göre sıralanmıştır. Kaynak: sunumdaki DSÖ Health Equity Monitor Türkiye profili.")
dumbbell("m4k6_tr_olum", "Turkiyede alt gruplar arasinda olum hizi ve beslenme farklari",
         [("5 yaş altı ölüm hızı (binde)", 8.1, 27.9), ("Bebek ölüm hızı (binde)", 7.8, 22.6), ("Yenidoğan ölüm hızı (binde)", 1.8, 13.0),
          ("Bodurluk, 5 yaş altı (%)", 4.7, 18.7), ("Obezite, 5 yaş altı (%)", 7.6, 16.1), ("Obezite, 15-49 yaş kadın (%)", 18.9, 32.3)],
         35, "binde (ölüm hızları) ya da yüzde (beslenme)", (0, 5, 10, 15, 20, 25, 30, 35), False,
         "Yüksek değer kötü sonuçtur. Kaynak: sunumdaki DSÖ Health Equity Monitor Türkiye profili.")
print("ok")
