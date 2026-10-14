import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "build"))
from svglib import SVG, NEU, TXT, CYAN, MAG, FONT, esc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "svg")
os.makedirs(OUT, exist_ok=True)


def save(s, name):
    s.save(os.path.join(OUT, name + ".svg"))


def circ(s, x, y, r, hot=False):
    if hot:
        s.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{MAG}" fill-opacity="0.16" stroke="{MAG}" stroke-width="1.3"/>')
    else:
        s.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="white" stroke="{NEU}" stroke-opacity="0.8" stroke-width="1.1"/>')


def line(s, x1, y1, x2, y2, w=1.6, col=NEU, op=0.8):
    s.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-opacity="{op}" stroke-width="{w}" stroke-linecap="round"/>')


# =============================================================== 1.1 asinus ve amfizem tipleri
s = SVG(640, 300, "Normal asinus ve amfizem tiplerinde genislemis hava bosluklarinin asinus icindeki yeri", "m43a")
panels = [("Normal", "none", ["terminal bronşiolün distali:", "respiratuvar bronşiol,", "alveol kanalı, alveoller"]),
          ("Sentriasiner", "proximal", ["asinüsün merkezi (respiratuvar", "bronşiol) genişler · üst lob", "sigara · en sık (%95)"]),
          ("Panasiner", "all", ["bütün asinüs eşit genişler", "alt lob, ön yüz", "α1-antitripsin eksikliği"]),
          ("Paraseptal", "distal", ["distal asinüs, septum ve plevra", "komşuluğu · üst yarı · büller", "genç erişkinde pnömotoraks"])]
for i, (title, mode, notes) in enumerate(panels):
    x0 = 4 + i * 159
    s.add(f'<rect x="{x0}" y="4" width="153" height="292" rx="4" fill="white" stroke="{NEU}" stroke-opacity="0.2"/>')
    s.text(x0 + 76, 22, title, "title", anchor="middle", fs1=12.5)
    cx = x0 + 76
    # terminal bronsiol
    line(s, cx, 34, cx, 66, 5, NEU, 0.55)
    # respiratuvar bronsiol dallari
    rb = [(cx - 34, 108), (cx + 34, 108)]
    for (bx, by) in rb:
        line(s, cx, 66, bx, by, 3)
    # respiratuvar bronsiol uzerindeki alveol tomurcuklari
    for (bx, by) in rb:
        mx, my = (cx + bx) / 2, (66 + by) / 2
        side = -1 if bx < cx else 1
        if mode == "proximal":
            circ(s, mx + side * 10, my + 2, 15, True)
        elif mode == "all":
            circ(s, mx + side * 8, my + 2, 9, True)
        else:
            circ(s, mx + side * 7, my + 2, 5)
    # alveol kanallari ve keseler
    for (bx, by) in rb:
        for dx in (-16, 16):
            ex, ey = bx + dx, 150
            line(s, bx, by, ex, ey, 1.8)
            if mode == "distal":
                r, hot = 9.5, True
            elif mode == "all":
                r, hot = 9, True
            else:
                r, hot = 6.5, False
            for ox, oy in ((-r * 0.95, 8), (r * 0.95, 8), (0, 8 + r * 1.55)):
                circ(s, ex + ox, ey + oy, r, hot)
    s.add(f'<line x1="{x0 + 8}" y1="196" x2="{x0 + 145}" y2="196" stroke="{CYAN}" stroke-width="1.4" stroke-dasharray="5 4"/>')
    for j, n in enumerate(notes):
        s.text(x0 + 76, 226 + j * 15, n, "sub", anchor="middle", fs2=10)
s.text(10, 48, "terminal", "small")
s.text(10, 60, "bronşiol", "small")
s.text(10, 205, "lobül septumu / plevra", "cyan", fs2=9.8)
save(s, "m4k3_asinus")

# =============================================================== 2.1 Reid indeksi
s = SVG(640, 250, "Reid indeksi: normal bronsta ve kronik bronsitte submukozal bez kalinliginin duvar kalinligina orani", "m43b")
for i, (title, gtop, gbot, ratio, goblet) in enumerate([("Normal bronş", 62, 96, "Reid ≈ 0,35 (normal ≤ 0,4)", False),
                                                       ("Kronik bronşit", 58, 124, "Reid ≈ 0,65 (artmış, > 0,5)", True)]):
    x0 = 6 + i * 318
    s.add(f'<rect x="{x0}" y="4" width="310" height="240" rx="4" fill="white" stroke="{NEU}" stroke-opacity="0.2"/>')
    s.text(x0 + 155, 22, title, "title", anchor="middle", fs1=12.5)
    L, R = x0 + 16, x0 + 232
    s.text(L, 31, "lümen", "small")
    # epitel
    s.add(f'<rect x="{L}" y="42" width="{R - L}" height="10" fill="{CYAN}" fill-opacity="0.12" stroke="{CYAN}" stroke-opacity="0.6" stroke-width="1"/>')
    for k in range(0, int((R - L) / 8)):
        xx = L + 4 + k * 8
        s.add(f'<line x1="{xx}" y1="42" x2="{xx}" y2="37" stroke="{CYAN}" stroke-opacity="0.6" stroke-width="0.8"/>')
    if goblet:
        for k in range(6):
            xx = L + 18 + k * 34
            s.add(f'<ellipse cx="{xx}" cy="47" rx="5" ry="4" fill="{MAG}" fill-opacity="0.35"/>')
    # bazal membran
    s.add(f'<line x1="{L}" y1="54" x2="{R}" y2="54" stroke="{NEU}" stroke-width="1.6"/>')
    # bezler
    n = 5 if not goblet else 7
    for k in range(n):
        gx = L + 14 + k * ((R - L - 28) / (n - 1))
        cy = (gtop + gbot) / 2
        s.add(f'<ellipse cx="{gx:.1f}" cy="{cy:.1f}" rx="{11 if not goblet else 14}" ry="{(gbot - gtop) / 2:.1f}" fill="{MAG}" fill-opacity="0.14" stroke="{MAG}" stroke-width="1"/>')
    # kikirdak
    s.add(f'<rect x="{L}" y="150" width="{R - L}" height="22" rx="6" fill="{NEU}" fill-opacity="0.12" stroke="{NEU}" stroke-opacity="0.5"/>')
    s.text((L + R) / 2, 165, "kıkırdak", "small", anchor="middle")
    # olcu cizgileri
    bx = R + 14
    s.add(f'<line x1="{bx}" y1="54" x2="{bx}" y2="150" stroke="{NEU}" stroke-width="1.2"/>')
    for yy in (54, 150):
        s.add(f'<line x1="{bx - 4}" y1="{yy}" x2="{bx + 4}" y2="{yy}" stroke="{NEU}" stroke-width="1.2"/>')
    s.text(bx + 8, 106, "W", "title", fs1=12.5)
    gx2 = R + 50
    s.add(f'<line x1="{gx2}" y1="{gtop}" x2="{gx2}" y2="{gbot}" stroke="{MAG}" stroke-width="1.6"/>')
    for yy in (gtop, gbot):
        s.add(f'<line x1="{gx2 - 4}" y1="{yy}" x2="{gx2 + 4}" y2="{yy}" stroke="{MAG}" stroke-width="1.6"/>')
    s.text(gx2 + 8, (gtop + gbot) / 2 + 4, "G", "magb", fs2=12.5)
    s.text(x0 + 155, 196, ratio, "magb" if goblet else "title", anchor="middle", fs1=12, fs2=11.5)
    s.text(x0 + 155, 214, "G: submukozal bez kalınlığı", "small", anchor="middle")
    s.text(x0 + 155, 228, "W: bazal membran ile kıkırdak arası", "small", anchor="middle")
save(s, "m4k3_reid")

# =============================================================== 2.2 kronik bronsit ve amfizem gelisimi
s = SVG(640, 356, "Sigaranin bronslarda kronik bronsite, alveollerde amfizeme yol acmasi", "m43c")
s.box(170, 4, 300, 46, [("Süregelen ve yineleyen zedelenme", "title"), ("sigara içimi (± hava kirliliği, meslek)", "sub")], kind="mag", fs1=12.5, fs2=10.5)
s.path("M250,50 L150,84", NEU)
s.path("M390,50 L490,84", NEU)
s.box(20, 86, 260, 44, [("Bronş ve bronşiyol zedelenmesi", "title"), ("bez hipertrofisi, goblet hücre metaplazisi", "sub")], fs1=12, fs2=10.3)
s.box(360, 86, 260, 44, [("Alveol duvarı zedelenmesi", "title"), ("proteaz-antiproteaz dengesizliği", "sub")], fs1=12, fs2=10.3)
s.arrow(150, 130, 150, 156)
s.box(20, 158, 260, 46, [("Aşırı mukus · bronkospazm · enfeksiyon", "title"), ("küçük hava yollarında geri dönüşlü tıkanma", "sub")], fs1=12, fs2=10.3)
s.arrow(150, 204, 150, 230)
s.arrow(490, 130, 490, 230)
s.text(500, 176, "süregelen zedelenme", "small")
s.text(500, 188, "yineleyen enfeksiyon", "small")
s.text(160, 222, "süregelen zedelenme, yineleyen enfeksiyon", "small")
s.box(20, 232, 260, 44, [("Kronik bronşit", "title"), ("klinik tanım · Reid indeksi ↑", "sub")], kind="key", fs1=12.5, fs2=10.5)
s.box(360, 232, 260, 44, [("Amfizem", "title"), ("morfolojik tanım · alveol duvarı yıkımı", "sub")], kind="key", fs1=12.5, fs2=10.5)
s.path("M150,276 L270,308", NEU)
s.path("M490,276 L370,308", NEU)
s.box(150, 310, 340, 42, [("KOAH: çoğu hastada ikisi birlikte", "title"), ("orta-ağır obstrüksiyonda belirgin amfizem de vardır", "sub")], kind="mag", fs1=12, fs2=10.3)
save(s, "m4k3_kb_amf")

# =============================================================== 4.1 bronsektazi kisir dongusu
s = SVG(640, 244, "Bronsektazi patogenezinde obstruksiyon ve enfeksiyonun kisir dongusu", "m43d")
s.box(10, 10, 280, 64, [("1. Obstrüksiyon ya da temizlik bozukluğu", "title"), ("tümör, yabancı cisim, mukus tıkacı;", "sub"), ("kistik fibrozis, silyer diskinezi", "sub")], fs1=12, fs2=10.3, lh=15)
s.box(350, 10, 280, 64, [("2. Sekresyonlar birikir", "title"), ("normal temizleme engellenir,", "sub"), ("sekonder enfeksiyon gelişir", "sub")], fs1=12, fs2=10.3, lh=15)
s.box(350, 160, 280, 64, [("3. Kronik nekrotizan inflamasyon", "title"), ("nötrofil proteazları, bakteri toksinleri:", "sub"), ("kas, elastik doku, kıkırdak yıkılır", "sub")], kind="mag", fs1=12, fs2=10.3, lh=15)
s.box(10, 160, 280, 64, [("4. Duvar zayıflar, kalıcı dilatasyon", "title"), ("silindirik ya da sakküler genişleme;", "sub"), ("dilate bronşta temizlik daha da bozulur", "sub")], kind="key", fs1=12, fs2=10.3, lh=15)
s.arrow(292, 42, 346, 42)
s.arrow(490, 76, 490, 156)
s.arrow(348, 192, 294, 192)
s.arrow(150, 158, 150, 78, CYAN)
s.text(320, 122, "kısır döngü", "magb", anchor="middle", fs2=12)
save(s, "m4k3_bronsektazi")
print("ok")
