import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "build"))
from svglib import SVG, NEU, TXT, CYAN, MAG, FONT, esc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "svg")
os.makedirs(OUT, exist_ok=True)
BONE = 'stroke="var(--color-neutral-700)" stroke-opacity="0.42" stroke-linecap="round" fill="none"'
CART = 'stroke="var(--color-accent)" stroke-opacity="0.45" stroke-linecap="round" fill="none"'


def save(s, name):
    s.save(os.path.join(OUT, name + ".svg"))


def lead(s, x1, y1, x2, y2, color=NEU, op=0.55):
    s.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-opacity="{op}" stroke-width="0.9"/>')


def dot(s, x, y, color=NEU, r=2.2):
    s.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>')


# =============================================================== 1.2 Tipik kaburga ve eklemleri (ustten)
s = SVG(640, 362, "Tipik kaburganin bolumleri, vertebra ile eklemleri ve collum boyunca uzanan donme ekseni; ustten gorunus", "k71a")
s.text(16, 18, "ARKA", "cap")
s.text(16, 352, "ÖN", "cap")
# vertebra
s.add(f'<circle cx="230" cy="150" r="38" fill="white" stroke="{NEU}" stroke-opacity="0.55" stroke-width="1.2"/>')
s.add(f'<circle cx="230" cy="90" r="16" fill="none" stroke="{NEU}" stroke-opacity="0.35" stroke-width="1"/>')
s.add(f'<path d="M205,118 Q196,72 230,64 Q264,72 255,118" stroke-width="8" {BONE}/>')
s.add(f'<line x1="230" y1="64" x2="230" y2="24" stroke-width="9" {BONE}/>')
s.add(f'<line x1="206" y1="76" x2="162" y2="54" stroke-width="10" {BONE}/>')
s.add(f'<line x1="254" y1="76" x2="298" y2="54" stroke-width="10" {BONE}/>')
# kaburga + kikirdak + sternum
s.add(f'<path d="M266,132 L302,66 C318,54 334,52 350,56 C410,66 462,118 464,182 C466,250 420,304 344,320" stroke-width="11" {BONE}/>')
s.add(f'<path d="M344,320 C314,326 280,330 256,331" stroke-width="10" {CART}/>')
s.add(f'<rect x="206" y="318" width="48" height="26" rx="7" fill="white" stroke="{NEU}" stroke-opacity="0.55"/>')
# eklem noktalari
dot(s, 266, 132, CYAN, 3.2)
dot(s, 302, 66, CYAN, 3.2)
# donme ekseni
s.add(f'<line x1="248" y1="165" x2="336" y2="4" stroke="{CYAN}" stroke-width="1.6"/>')
s.text(342, 13, "dönme ekseni", "cyanb", fs2=11.5)
s.text(342, 26, "(collum costae boyunca)", "cyan", fs2=10.5)
# vertebra etiketleri
s.text(222, 26, "processus spinosus", "small", anchor="end")
s.text(156, 50, "processus transversus", "small", anchor="end")
s.text(186, 150, "corpus vertebrae", "small", anchor="end")
s.text(230, 356, "sternum", "small", anchor="middle")
s.text(320, 352, "cartilago costalis", "small", anchor="start")
# kaburga etiketleri
lead(s, 312, 92, 305, 71)
s.text(314, 102, "tuberculum costae", "body", fs2=11.5)
s.text(314, 114, "art. costotransversaria", "cyan", fs2=10)
lead(s, 300, 126, 287, 104)
s.text(302, 136, "collum costae", "body", fs2=11.5)
lead(s, 284, 158, 270, 138)
s.text(286, 168, "caput costae", "body", fs2=11.5)
s.text(286, 181, "art. capitis costae (iki vertebra + disk)", "cyan", fs2=10)
s.text(362, 44, "angulus costae", "body", fs2=11.5)
s.text(362, 56, "(en zayıf nokta)", "small")
s.text(476, 150, "corpus costae", "body", fs2=11.5)
s.text(476, 163, "iç yüzünün alt kenarında", "small")
s.text(476, 175, "sulcus costae (VAN)", "small")
s.text(476, 270, "Kaburga, arka ucundaki", "small")
s.text(476, 282, "eksen etrafında dönen", "small")
s.text(476, 294, "uzun bir kaldıraçtır: boyunda", "small")
s.text(476, 306, "birkaç derecelik dönme ön", "small")
s.text(476, 318, "uçta 1-2 cm'lik harekete", "small")
s.text(476, 330, "dönüşür.", "small")
save(s, "m4k7_kaburga")

# =============================================================== 1.5 Inspirasyon zinciri
s = SVG(640, 574, "Sessiz inspirasyonda diyafram ve interkostal kaslarin kasilmasindan havanin iceri akmasina kadar olan zincir", "k71b")
s.box(170, 8, 300, 50, ["Solunum merkezi (medulla oblongata)", "n. phrenicus (C3-C5) ve nn. intercostales"], fs1=12.5)
s.path("M250,58 L150,58 L150,88")
s.path("M390,58 L470,58 L470,88")
s.box(10, 90, 280, 58, ["Diyafram kasılır", "kubbeler iner: sessiz solukta ~1,5 cm,", "derin solukta 6-10 cm"], fs1=12.5)
s.box(310, 90, 320, 58, ["Mm. intercostales externi (+ skalenler)", "kaburgalar collum ekseninde döner", "ve yukarı kalkar"], fs1=12.5)
s.arrow(75, 148, 75, 180)
s.arrow(220, 148, 220, 180)
s.box(10, 182, 130, 64, ["Karın boşluğu", "hacim ↓, basınç ↑", "karın duvarı öne çıkar"], fs1=12, fs2=10.5)
s.box(150, 182, 140, 64, ["Dikey çap ↑", "göğüs uzar"], kind="key", fs1=13)
s.arrow(388, 148, 388, 180)
s.arrow(552, 148, 552, 180)
s.box(310, 182, 156, 64, ["Üst kaburgalar", "tulumba kolu", "ön-arka çap ↑"], fs1=12, fs2=11)
s.box(474, 182, 156, 64, ["Alt kaburgalar", "kova sapı", "enine çap ↑"], fs1=12, fs2=11)
s.path("M220,246 L220,266 L290,266 L290,286")
s.path("M388,246 L388,266 L350,266 L350,286")
s.path("M552,246 L552,272 L440,272 L440,286")
s.box(170, 288, 300, 44, ["Göğüs boşluğunun hacmi artar"], kind="key", fs1=13.5)
s.arrow(320, 332, 320, 362)
s.box(150, 364, 340, 56, ["Plevral basınç daha negatif olur", "≈ −5 cmH₂O'dan ≈ −8 cmH₂O'ya; akciğer", "duvarı izleyerek genişler"], fs1=12.5)
s.arrow(320, 420, 320, 446)
s.box(150, 448, 340, 56, ["Alveol basıncı atmosferin altına iner", "≈ −1 cmH₂O (Boyle yasası: hacim ↑ → basınç ↓)"], fs1=12.5)
s.arrow(320, 504, 320, 528)
s.box(170, 530, 300, 40, ["Hava alveollere akar: inspirasyon"], kind="key", fs1=13.5)
save(s, "m4k7_inspirasyon")

# =============================================================== 2.3 Diyafram acikliklari (sol yandan sematik)
s = SVG(640, 372, "Diyaframin uc buyuk acikligi: T8 foramen venae cavae, T10 hiatus oesophageus, T12 hiatus aorticus; sol yandan sematik gorunus", "k72a")
s.text(16, 16, "ÖN", "cap")
s.text(624, 16, "ARKA", "cap", anchor="end")
# vertebralar
lv = ["T6", "T7", "T8", "T9", "T10", "T11", "T12", "L1", "L2"]
for i, n in enumerate(lv):
    y = 22 + i * 38
    s.add(f'<rect x="548" y="{y}" width="60" height="30" rx="4" fill="white" stroke="{NEU}" stroke-opacity="0.45"/>')
    s.text(578, y + 20, n, "body", anchor="middle", fs2=11.5)
VY = {n: 22 + i * 38 + 15 for i, n in enumerate(lv)}
# aorta (vertebralarin onunde)
s.add(f'<line x1="522" y1="8" x2="522" y2="364" stroke="{NEU}" stroke-opacity="0.28" stroke-width="16" stroke-linecap="round"/>')
s.text(522, 362, "aorta", "small", anchor="middle")
# diyafram: kas (gri) + centrum tendineum (acik)
s.add(f'<path d="M70,150 C110,118 160,102 205,98" stroke="{NEU}" stroke-opacity="0.55" stroke-width="9" fill="none" stroke-linecap="round"/>')
s.add(f'<path d="M205,98 C250,94 300,96 335,104" stroke="{NEU}" stroke-opacity="0.22" stroke-width="9" fill="none"/>')
s.add(f'<path d="M335,104 C390,118 425,160 452,{VY["T10"]} C480,220 500,250 512,{VY["T12"]}" stroke="{NEU}" stroke-opacity="0.55" stroke-width="9" fill="none"/>')
s.add(f'<path d="M512,{VY["T12"]} C520,290 528,320 538,352" stroke="{NEU}" stroke-opacity="0.55" stroke-width="7" fill="none" stroke-linecap="round"/>')
# lig. arcuatum medianum: aortanin onunde kemer
s.add(f'<path d="M506,{VY["T12"]-2} Q522,{VY["T12"]-16} 538,{VY["T12"]-2}" stroke="{NEU}" stroke-opacity="0.8" stroke-width="2" fill="none"/>')
s.text(270, 88, "centrum tendineum", "small", anchor="middle")
s.text(95, 170, "pars sternalis", "small", anchor="middle")
s.text(508, 334, "crus dextrum", "small", anchor="end")
s.text(150, 40, "göğüs boşluğu", "cap", anchor="middle")
s.text(150, 200, "karın boşluğu", "cap", anchor="middle")
# VCI (centrum tendineumdan dik gecer)
s.add(f'<line x1="300" y1="30" x2="300" y2="190" stroke="{NEU}" stroke-opacity="0.3" stroke-width="14" stroke-linecap="round"/>')
s.text(300, 24, "VCİ", "small", anchor="middle")
# ozofagus (kas kisimdan egik gecer)
s.add(f'<line x1="412" y1="24" x2="472" y2="232" stroke="{CYAN}" stroke-opacity="0.35" stroke-width="13" stroke-linecap="round"/>')
s.text(404, 24, "özofagus", "small", anchor="end")
# acikliklar ve duzey cizgileri
for (x, y, lvl) in ((300, 96, "T8"), (452, VY["T10"], "T10"), (522, VY["T12"] - 8, "T12")):
    s.add(f'<line x1="{x}" y1="{y}" x2="548" y2="{VY[lvl]}" stroke="{CYAN}" stroke-opacity="0.5" stroke-width="1"/>')
    s.add(f'<circle cx="{x}" cy="{y}" r="5" fill="white" stroke="{CYAN}" stroke-width="2"/>')
# etiket bloklari
s.text(14, 236, "T8 · Foramen venae cavae", "cyanb", fs2=12)
s.text(14, 250, "centrum tendineum'da; VCİ, sağ n. phrenicus dalları", "small")
s.text(14, 263, "kasılınca gerilip açılır → venöz dönüş artar", "body", fs2=10.5)
s.text(14, 286, "T10 · Hiatus oesophageus", "cyanb", fs2=12)
s.text(14, 300, "sağ krusun kas lifleri arasında; özofagus, trunci vagales", "small")
s.text(14, 313, "kasılınca sıkışır → reflüye karşı dış sfinkter", "body", fs2=10.5)
s.text(14, 336, "T12 · Hiatus aorticus", "cyanb", fs2=12)
s.text(14, 350, "krusların arkasında, lig. arcuatum medianum altında;", "small")
s.text(14, 362, "aorta, ductus thoracicus, (v. azygos) · kasılmadan etkilenmez", "body", fs2=10.5)
save(s, "m4k7_diyafram_aciklik")

# =============================================================== 2.8 Kaldirac modeli (Hamberger)
s = SVG(640, 286, "Interkostal kaslarin kaldirac modeli: eksternal interkostal lifi alttaki kaburgaya daha uzak noktada tutundugu icin kaburgalari kaldirir; internal interkostal tersini yapar", "k72b")
def panel(ox, ext):
    # omurga
    s.add(f'<line x1="{ox+40}" y1="22" x2="{ox+40}" y2="232" stroke="{NEU}" stroke-opacity="0.45" stroke-width="9" stroke-linecap="round"/>')
    s.text(ox + 40, 250, "omurga", "small", anchor="middle")
    s.text(ox + 262, 250, "sternum", "small", anchor="middle")
    # kaburgalar (one dogru asagi egimli) + sternum
    y_up0, y_lo0 = 70, 150
    def ry(y0, x):
        return y0 + (x - (ox + 40)) * 0.2
    s.add(f'<line x1="{ox+40}" y1="{y_up0}" x2="{ox+262}" y2="{ry(y_up0, ox+262):.1f}" stroke="{NEU}" stroke-opacity="0.55" stroke-width="6" stroke-linecap="round"/>')
    s.add(f'<line x1="{ox+40}" y1="{y_lo0}" x2="{ox+262}" y2="{ry(y_lo0, ox+262):.1f}" stroke="{NEU}" stroke-opacity="0.55" stroke-width="6" stroke-linecap="round"/>')
    s.add(f'<line x1="{ox+262}" y1="{ry(y_up0, ox+262):.1f}" x2="{ox+262}" y2="{ry(y_lo0, ox+262):.1f}" stroke="{NEU}" stroke-opacity="0.35" stroke-width="4"/>')
    for yy in (y_up0, y_lo0):
        s.add(f'<circle cx="{ox+40}" cy="{yy}" r="5" fill="white" stroke="{NEU}" stroke-width="1.5"/>')
    s.text(ox + 150, 58, "üst kaburga", "small", anchor="middle")
    s.text(ox + 150, 196, "alt kaburga", "small", anchor="middle")
    if ext:
        xu, xl = ox + 92, ox + 176
    else:
        xu, xl = ox + 176, ox + 92
    yu, yl = ry(y_up0, xu), ry(y_lo0, xl)
    s.add(f'<line x1="{xu}" y1="{yu:.1f}" x2="{xl}" y2="{yl:.1f}" stroke="{CYAN}" stroke-width="3"/>')
    dot(s, xu, round(yu, 1), CYAN, 3.5)
    dot(s, xl, round(yl, 1), CYAN, 3.5)
    # kaldirac kollari
    s.add(f'<line x1="{ox+40}" y1="{y_up0-12}" x2="{xu}" y2="{ry(y_up0, xu)-12:.1f}" stroke="{CYAN}" stroke-opacity="0.6" stroke-width="1.2"/>')
    s.add(f'<line x1="{ox+40}" y1="{y_lo0+14}" x2="{xl}" y2="{ry(y_lo0, xl)+14:.1f}" stroke="{CYAN}" stroke-opacity="0.6" stroke-width="1.2"/>')
    kisa_ust = "kısa kol" if ext else "uzun kol"
    kisa_alt = "uzun kol" if ext else "kısa kol"
    s.text(ox + 60, y_up0 - 18, kisa_ust, "cyan", fs2=10.5)
    s.text(ox + 60, y_lo0 + 34, kisa_alt, "cyan", fs2=10.5)
    # hareket oku
    if ext:
        s.arrow(ox + 222, 186, ox + 222, 150, CYAN)
        s.text(ox + 232, 176, "kalkar", "cyanb", fs2=11)
    else:
        s.arrow(ox + 222, 70, ox + 222, 106, CYAN)
        s.text(ox + 232, 90, "iner", "cyanb", fs2=11)
panel(0, True)
panel(330, False)
s.text(150, 16, "A · M. intercostalis externus", "title", anchor="middle", fs1=12.5)
s.text(480, 16, "B · M. intercostalis internus (interosseöz kısım)", "title", anchor="middle", fs1=12.5)
s.text(150, 270, "Lif alttaki kaburgaya daha uzakta tutunur:", "small", anchor="middle")
s.text(150, 282, "alttaki kaburgayı kaldıran tork büyük → kaburgalar kalkar", "small", anchor="middle")
s.text(480, 270, "Lif üstteki kaburgaya daha uzakta tutunur:", "small", anchor="middle")
s.text(480, 282, "üstteki kaburgayı indiren tork büyük → kaburgalar iner", "small", anchor="middle")
save(s, "m4k7_kaldirac")

# =============================================================== 3.2 Interkostal aralik katmanlari, VAN ve torasentez
s = SVG(640, 404, "Interkostal araligin katmanlari, sulcus costae icinde ven-arter-sinir dizilimi, kollateral dallar ve torasentez ignesinin gecis yeri", "k73a")
Y0, Y1 = 34, 300
s.text(14, 20, "DIŞ", "cap")
s.text(470, 20, "İÇ (göğüs boşluğu)", "cap")
s.add(f'<rect x="96" y="{Y0}" width="12" height="{Y1-Y0}" fill="{NEU}" fill-opacity="0.30"/>')
s.add(f'<rect x="108" y="{Y0}" width="34" height="{Y1-Y0}" fill="{NEU}" fill-opacity="0.08"/>')
s.add(f'<rect x="142" y="{Y0}" width="46" height="{Y1-Y0}" fill="{NEU}" fill-opacity="0.18"/>')
s.add(f'<rect x="196" y="46" width="108" height="72" rx="28" fill="white" stroke="{NEU}" stroke-opacity="0.6" stroke-width="1.4"/>')
s.add(f'<rect x="196" y="212" width="108" height="72" rx="28" fill="white" stroke="{NEU}" stroke-opacity="0.6" stroke-width="1.4"/>')
s.add(f'<path d="M262,118 Q262,98 284,98 L304,98 L304,118 Z" fill="{TXT}" fill-opacity="0.05"/>')
s.text(236, 80, "üst kaburga", "small", anchor="middle")
s.text(236, 252, "alt kaburga", "small", anchor="middle")
s.add(f'<rect x="198" y="118" width="36" height="94" fill="{NEU}" fill-opacity="0.14"/>')
for k in range(5):
    y = 124 + k * 18
    s.add(f'<line x1="200" y1="{y}" x2="232" y2="{y+14}" stroke="{NEU}" stroke-opacity="0.45" stroke-width="1"/>')
s.add(f'<rect x="234" y="118" width="30" height="94" fill="{NEU}" fill-opacity="0.24"/>')
for k in range(5):
    y = 138 + k * 18
    s.add(f'<line x1="236" y1="{y}" x2="262" y2="{y-14}" stroke="{NEU}" stroke-opacity="0.45" stroke-width="1"/>')
s.add(f'<rect x="286" y="146" width="18" height="52" fill="{NEU}" fill-opacity="0.24"/>')
for (y, lab) in ((108, "V"), (122, "A"), (137, "N")):
    s.add(f'<circle cx="275" cy="{y}" r="6" fill="white" stroke="{CYAN}" stroke-width="1.6"/>')
    s.text(275, y + 4, lab, "cyanb", anchor="middle", fs2=8.5)
for x in (270, 282):
    s.add(f'<circle cx="{x}" cy="204" r="4" fill="white" stroke="{CYAN}" stroke-width="1.3"/>')
s.add(f'<line x1="310" y1="{Y0}" x2="310" y2="{Y1}" stroke="{NEU}" stroke-opacity="0.5" stroke-width="1"/>')
s.add(f'<rect x="316" y="{Y0}" width="10" height="{Y1-Y0}" fill="{CYAN}" fill-opacity="0.12"/>')
s.add(f'<line x1="316" y1="{Y0}" x2="316" y2="{Y1}" stroke="{CYAN}" stroke-width="2"/>')
s.add(f'<line x1="326" y1="{Y0}" x2="326" y2="{Y1}" stroke="{CYAN}" stroke-width="2"/>')
s.add(f'<rect x="326" y="{Y0}" width="140" height="{Y1-Y0}" fill="{NEU}" fill-opacity="0.07"/>')
s.text(400, 60, "akciğer", "small", anchor="middle")
s.add(f'<line x1="20" y1="164" x2="338" y2="164" stroke="{MAG}" stroke-width="2.4" marker-end="url(#k73am)"/>')
s.text(20, 156, "torasentez iğnesi", "magb", fs2=11)
s.text(20, 182, "aralığın ortasından", "mag", fs2=10.5)
marks = [(102, 58, "1"), (125, 58, "2"), (165, 58, "3"), (216, 196, "4"), (249, 196, "5"), (295, 186, "6")]
for (x, y, n) in marks:
    s.add(f'<circle cx="{x}" cy="{y}" r="7.5" fill="white" stroke="{NEU}" stroke-width="1"/>')
    s.text(x, y + 3.6, n, "title", anchor="middle", fs1=9.5)
for (x, xm, n) in ((313, 304, "7"), (321, 322, "8"), (380, 340, "9")):
    s.add(f'<line x1="{x}" y1="300" x2="{xm}" y2="310" stroke="{NEU}" stroke-opacity="0.6" stroke-width="0.9"/>')
for (xm, n) in ((300, "7"), (322, "8"), (344, "9")):
    s.add(f'<circle cx="{xm}" cy="316" r="7.5" fill="white" stroke="{NEU}" stroke-width="1"/>')
    s.text(xm, 319.6, n, "title", anchor="middle", fs1=9.5)
leg = ["1 deri", "2 deri altı yağ dokusu", "3 m. serratus anterior (yan duvarda)", "4 m. intercostalis externus",
       "5 m. intercostalis internus", "6 m. intercostalis intimus", "7 fascia endothoracica + pleura parietalis",
       "8 cavitas pleuralis (sıvı)", "9 pleura visceralis + akciğer"]
for i, t in enumerate(leg):
    col, row = (0, i) if i < 5 else (1, i - 5)
    s.text(14 + col * 300, 344 + row * 12.5, t, "small")
s.text(486, 106, "sulcus costae içinde", "cyanb", fs2=10.5)
s.text(486, 119, "V-A-N: ven, arter, sinir;", "cyan", fs2=10)
s.text(486, 131, "5 ile 6 arasında; sinir en", "cyan", fs2=10)
s.text(486, 143, "altta, en az korunan", "cyan", fs2=10)
s.text(486, 200, "kollateral dallar:", "cyanb", fs2=10.5)
s.text(486, 213, "alt kaburganın üst", "cyan", fs2=10)
s.text(486, 225, "kenarı boyunca", "cyan", fs2=10)
lead(s, 482, 122, 284, 122, CYAN, 0.45)
lead(s, 482, 206, 288, 204, CYAN, 0.45)
save(s, "m4k7_ik_katman")

# =============================================================== 3.5 Gogus duvari arterlerinin kokenleri
s = SVG(640, 360, "Gogus duvari arterlerinin kokenleri: posterior interkostal arterler a. intercostalis suprema ve aortadan, anterior interkostal arterler a. thoracica interna ve a. musculophrenica'dan", "k73b")
s.text(160, 16, "ARKA (POSTEROLATERAL) · 12 ÇİFT", "cap", anchor="middle")
s.text(480, 16, "ÖN · 9 ÇİFT", "cap", anchor="middle")
s.box(20, 30, 130, 40, ["A. subclavia"], fs1=12.5)
s.box(170, 30, 130, 40, ["Truncus", "costocervicalis"], fs1=11.5, fs2=11.5, lh=14)
s.arrow(150, 50, 168, 50)
s.arrow(235, 70, 235, 92)
s.box(170, 94, 130, 40, ["A. intercostalis", "suprema"], fs1=11.5, fs2=11.5, lh=14)
s.arrow(235, 134, 235, 156)
s.box(150, 158, 150, 44, ["Aa. intercostales", "posteriores I-II"], kind="key", fs1=12, fs2=12, lh=15)
s.box(20, 222, 130, 40, ["Aorta thoracica"], fs1=12.5)
s.arrow(150, 242, 168, 242)
s.box(170, 222, 130, 40, ["Aa. intercostales", "posteriores III-XI"], kind="key", fs1=11.5, fs2=11.5, lh=14)
s.arrow(85, 262, 85, 280)
s.box(20, 282, 130, 36, ["A. subcostalis (12.)"], kind="key", fs1=11.5)
s.box(340, 30, 140, 40, ["A. thoracica interna", "(a. subclavia 1. kısım)"], fs1=11.5, fs2=10)
s.path("M150,40 L160,40 L160,22 L320,22 L320,42 L338,42")
s.arrow(410, 70, 410, 92)
s.box(340, 94, 140, 44, ["Aa. intercostales", "anteriores 1-6"], kind="key", fs1=12, fs2=12, lh=15)
s.path("M480,44 L560,44 L560,92")
s.box(500, 94, 120, 40, ["A. musculo-", "phrenica"], fs1=11.5, fs2=11.5, lh=14)
s.arrow(560, 134, 560, 156)
s.box(490, 158, 140, 44, ["Aa. intercostales", "anteriores 7-9"], kind="key", fs1=12, fs2=12, lh=15)
s.path("M480,60 L488,60 L488,300 L482,300")
s.box(340, 282, 140, 36, ["A. epigastrica superior"], fs1=11)
s.text(410, 334, "(6. İKA'da a. musculophrenica ile", "small", anchor="middle")
s.text(410, 346, "birlikte a. thoracica interna'nın uç dalı)", "small", anchor="middle")
s.add(f'<path d="M300,180 C330,180 330,120 340,118" stroke="{CYAN}" stroke-width="1.6" fill="none"/>')
s.add(f'<path d="M300,244 C400,244 450,200 490,184" stroke="{CYAN}" stroke-width="1.6" fill="none"/>')
s.text(372, 170, "her aralıkta", "cyanb", anchor="middle", fs2=10.5)
s.text(372, 183, "anastomoz", "cyanb", anchor="middle", fs2=10.5)
s.text(500, 236, "10. ve 11. aralıklarda ön", "small")
s.text(500, 248, "arter yoktur; buraları uzayan", "small")
s.text(500, 260, "posterior arterler besler.", "small")
s.text(160, 340, "A. axillaris'ten ayrıca a. thoracica superior ve lateralis", "small", anchor="middle")
save(s, "m4k7_ik_arterler")

# =============================================================== 3.5 Koarktasyonda kollateral dolasim
s = SVG(640, 350, "Aort koarktasyonunda kollateral dolasim ve kaburga centiklenmesinin mekanizmasi", "k73c")
s.box(150, 8, 340, 46, ["Aort koarktasyonu", "a. subclavia sinistra çıkışının hemen distalinde darlık"], kind="key", fs1=12.5)
s.arrow(320, 54, 320, 76)
s.box(150, 78, 340, 46, ["Proksimalde yüksek basınç", "a. subclavia → a. thoracica interna genişler"], fs1=12.5)
s.arrow(320, 124, 320, 146)
s.box(150, 148, 340, 46, ["Aa. intercostales anteriores", "her aralıkta posterior arterlerle anastomoz"], fs1=12.5)
s.arrow(320, 194, 320, 216)
s.box(150, 218, 340, 46, ["Aa. intercostales posteriores'te akım tersine döner", "kan aortaya, darlığın distaline ulaşır → alt vücut"], fs1=12.5)
s.arrow(320, 264, 320, 286)
s.box(150, 288, 340, 52, ["Genişleyen, kıvrılan posterior arterler (3-8)", "kaburganın alt kenarını aşındırır → kaburga çentiklenmesi"], kind="key", fs1=12.5)
s.box(500, 148, 136, 116, ["1. ve 2. kaburgalar", "korunur: arterleri", "a. intercostalis suprema", "üzerinden darlığın", "proksimalinden gelir;", "ters akım olmaz"], kind="key", fs1=11.5, fs2=10.5, lh=15)
s.box(4, 148, 136, 116, ["Kollateraller", "yetmez:", "kolda yüksek, bacakta", "düşük basınç;", "radyal-femoral", "nabız gecikmesi"], fs1=11.5, fs2=10.5, lh=15)
save(s, "m4k7_koarktasyon")

# =============================================================== 3.6 Azygos sistemi (onden, sematik)
s = SVG(640, 486, "Azygos sistemi: v. azygos, v. hemiazygos, v. hemiazygos accessoria ve superior interkostal venlerin dokulme yollari, onden sematik gorunus", "k73d")
lv = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12", "L1", "L2"]
Y = {n: 78 + i * 26 for i, n in enumerate(lv)}
VEIN = f'stroke="{NEU}" stroke-opacity="0.75" fill="none" stroke-linecap="round"'
XA, XH, C0, C1 = 274, 368, 306, 342
s.text(150, 16, "HASTANIN SAĞI", "cap", anchor="middle")
s.text(500, 16, "HASTANIN SOLU", "cap", anchor="middle")
# capraz gecisler (vertebralar arasindaki aralikta)
s.add(f'<path d="M{XH},{Y["T8"]+13} L{XA+2},{Y["T8"]+13}" stroke-width="4.5" {VEIN}/>')
s.add(f'<path d="M{XH},{Y["T7"]+13} L{XA+2},{Y["T7"]+13}" stroke-width="4.5" {VEIN}/>')
for n in lv:
    s.add(f'<rect x="{C0}" y="{Y[n]-10}" width="{C1-C0}" height="20" rx="3" fill="white" stroke="{NEU}" stroke-opacity="0.4"/>')
    s.text((C0 + C1) / 2, Y[n] + 4, n, "small", anchor="middle")
# brakiyosefalik venler ve VCS
s.add(f'<path d="M120,44 L212,60" stroke-width="7" {VEIN}/>')
s.add(f'<path d="M590,36 C470,40 320,46 212,60" stroke-width="7" {VEIN}/>')
s.add(f'<path d="M212,60 L212,214" stroke-width="10" {VEIN}/>')
s.text(120, 34, "v. brachiocephalica dx.", "small", anchor="start")
s.text(590, 28, "v. brachiocephalica sin.", "small", anchor="end")
s.text(200, 176, "VCS", "title", anchor="end", fs1=12)
s.text(200, 190, "→ sağ atriyum", "small", anchor="end")
# azygos + kemer
s.add(f'<path d="M{XA},{Y["L2"]+24} L{XA},{Y["T4"]+8} C{XA},{Y["T4"]-16} 238,{Y["T4"]-24} 216,{Y["T4"]-16}" stroke-width="6" {VEIN}/>')
s.text(XA + 16, Y["T11"], "v. azygos", "title", fs1=11.5, rotate=-90)
s.text(204, Y["T3"] + 22, "arcus v. azygos (T4)", "cyanb", anchor="end", fs2=10.5)
lead(s, 206, Y["T3"] + 18, 238, Y["T4"] - 14, CYAN, 0.6)
for n in ["T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12"]:
    s.add(f'<line x1="226" y1="{Y[n]+4}" x2="{XA}" y2="{Y[n]}" stroke-width="2" {VEIN}/>')
s.text(220, Y["T8"] + 6, "vv. int. post. dx. 4/5-11", "small", anchor="end")
s.text(220, Y["T12"] + 6, "v. subcostalis dx.", "small", anchor="end")
# sag superior interkostal
s.add(f'<path d="M254,{Y["T2"]} L254,{Y["T4"]-14}" stroke-width="3" {VEIN}/>')
for n in ["T2", "T3"]:
    s.add(f'<line x1="226" y1="{Y[n]+3}" x2="254" y2="{Y[n]}" stroke-width="2" {VEIN}/>')
s.text(214, Y["T2"] + 6, "v. int. sup. dx. (2-3)", "small", anchor="end")
s.add(f'<path d="M230,{Y["T1"]+4} L170,52" stroke-width="2" {VEIN}/>')
s.text(160, Y["T1"] + 10, "1. ven", "small", anchor="end")
# hemiazygos ve accessoria
s.add(f'<path d="M{XH},{Y["L2"]+24} L{XH},{Y["T8"]+13}" stroke-width="4.5" {VEIN}/>')
s.add(f'<path d="M{XH},{Y["T4"]+4} L{XH},{Y["T7"]+13}" stroke-width="4.5" {VEIN}/>')
s.text(XH - 10, Y["T11"] + 22, "v. hemiazygos", "title", fs1=11, rotate=-90)
s.text(XH - 10, Y["T6"] + 32, "v. hemiaz. acc.", "title", fs1=11, rotate=-90)
for n in ["T5", "T6", "T7", "T8"]:
    s.add(f'<line x1="430" y1="{Y[n]+4}" x2="{XH}" y2="{Y[n]}" stroke-width="2" {VEIN}/>')
for n in ["T9", "T10", "T11", "T12"]:
    s.add(f'<line x1="430" y1="{Y[n]+4}" x2="{XH}" y2="{Y[n]}" stroke-width="2" {VEIN}/>')
s.text(436, Y["T6"] + 8, "vv. int. post. sin. 4/5-8", "small")
s.text(436, Y["T6"] + 21, "→ v. hemiazygos accessoria", "small")
s.text(436, Y["T10"] + 8, "vv. int. post. sin. 9-11 ve", "small")
s.text(436, Y["T10"] + 21, "v. subcostalis → v. hemiazygos", "small")
s.text(436, Y["T7"] + 34, "T7-T8 arasında sağa geçer", "cyan", fs2=10)
s.text(436, Y["T8"] + 34, "T8-T9 arasında sağa geçer", "cyan", fs2=10)
# sol superior interkostal
s.add(f'<path d="M420,{Y["T3"]} L420,46" stroke-width="3" {VEIN}/>')
for n in ["T2", "T3"]:
    s.add(f'<line x1="456" y1="{Y[n]+3}" x2="420" y2="{Y[n]}" stroke-width="2" {VEIN}/>')
s.text(462, Y["T2"] + 6, "v. int. sup. sin. (2-3)", "small")
s.text(462, Y["T2"] + 19, "→ v. brachiocephalica sin.", "small")
s.text(462, Y["T2"] + 32, "(arcus aortae'yı çaprazlar)", "small")
# lomber baslangic
s.text(XA - 8, Y["L2"] + 24, "v. lumbalis asc. dx.", "small", anchor="end")
s.text(XH + 8, Y["L2"] + 24, "v. lumbalis asc. sin.", "small")
s.text(XA - 8, Y["L1"] + 4, "sağ krustan girer", "cyan", anchor="end", fs2=10)
s.text(XH + 8, Y["L1"] + 4, "sol krustan girer", "cyan", fs2=10)
save(s, "m4k7_azygos")

# =============================================================== 4.4 Plevral resesler: koronal ve enine sematik
s = SVG(640, 372, "Plevral resesler: koronal kesitte kostodiyafragmatik ve frenikomediastinal, enine kesitte kostomediastinal ve vertebromediastinal resesler", "k74a")
PL = f'stroke="{CYAN}" stroke-width="2" fill="{CYAN}" fill-opacity="0.10"'
LUNG = f'stroke="{CYAN}" stroke-width="1" stroke-opacity="0.8" fill="#e9e7e5"'
WALL = f'stroke="{NEU}" stroke-opacity="0.5" stroke-linecap="round" fill="none"'
s.text(160, 16, "A · Koronal kesit (sağ taraf, önden)", "title", anchor="middle", fs1=12)
s.add(f'<line x1="40" y1="44" x2="40" y2="300" stroke-width="9" {WALL}/>')
s.add(f'<line x1="270" y1="44" x2="270" y2="290" stroke-width="5" {WALL}/>')
s.add(f'<path d="M40,302 C70,232 120,214 155,216 C200,218 240,240 270,270" stroke-width="7" {WALL}/>')
s.add(f'<path d="M45,48 Q155,-4 265,48 L265,262 C240,238 200,222 155,222 C120,222 76,238 46,294 Z" {PL}/>')
s.add(f'<path d="M64,64 Q155,8 254,64 L254,240 C232,222 200,210 155,210 C118,210 84,224 62,252 Z" {LUNG}/>')
s.add(f'<circle cx="257" cy="146" r="5" fill="white" stroke="{NEU}"/><circle cx="257" cy="160" r="4" fill="white" stroke="{NEU}"/>')
s.text(155, 130, "akciğer", "small", anchor="middle")
s.text(155, 144, "(pleura visceralis ile örtülü)", "small", anchor="middle")
s.text(155, 32, "cupula pleurae", "small", anchor="middle")
s.text(28, 196, "pars costalis", "small", anchor="middle", rotate=-90)
s.text(286, 150, "pars mediastinalis", "small", anchor="middle", rotate=-90)
s.text(300, 150, "mediastinum", "cap", anchor="middle", rotate=-90)
s.text(155, 248, "pars diaphragmatica", "small", anchor="middle")
s.text(224, 160, "hilus", "small", anchor="end")
s.text(244, 206, "lig. pulmonale", "small", anchor="end")
lead(s, 246, 202, 262, 196)
# reses etiketleri
lead(s, 56, 316, 49, 288, CYAN, 0.8)
s.text(58, 322, "recessus costodiaphragmaticus (sinüs): keskin", "cyanb", fs2=10.5)
lead(s, 262, 336, 262, 262, CYAN, 0.8)
s.text(256, 340, "recessus phrenicomediastinalis: keskin", "cyanb", anchor="end", fs2=10.5)
s.text(160, 360, "karın boşluğu", "cap", anchor="middle")
# ---- B: enine kesit
s.text(486, 16, "B · Enine kesit (kalp düzeyi, aşağıdan)", "title", anchor="middle", fs1=12)
s.add(f'<ellipse cx="486" cy="182" rx="146" ry="128" stroke-width="9" {WALL}/>')
s.add(f'<rect x="473" y="50" width="26" height="16" rx="3" fill="white" stroke="{NEU}"/>')
s.text(486, 44, "sternum", "small", anchor="middle")
s.add(f'<circle cx="486" cy="286" r="22" fill="white" stroke="{NEU}"/>')
s.text(486, 290, "vertebra", "small", anchor="middle")
# sag plevral bosluk (izleyicinin solu)
s.add(f'<path d="M470,66 C430,58 372,88 352,150 C338,214 368,272 420,292 C440,300 458,302 466,288 C456,268 440,250 432,224 C420,190 420,150 438,112 C448,92 462,78 470,66 Z" {PL}/>')
s.add(f'<path d="M448,96 C412,92 370,116 362,160 C354,212 382,262 428,280 C444,284 452,276 448,262 C438,240 428,214 426,186 C424,150 432,118 448,96 Z" {LUNG}/>')
# sol plevral bosluk (izleyicinin sagi) - kalp nedeniyle on reses daha genis
s.add(f'<path d="M502,66 C542,58 600,88 620,150 C634,214 604,272 552,292 C532,300 514,302 506,288 C516,268 528,250 538,226 C552,196 556,160 540,124 C530,100 514,80 502,66 Z" {PL}/>')
s.add(f'<path d="M546,120 C580,112 606,132 612,166 C618,214 590,262 546,280 C530,284 522,276 526,262 C536,240 546,216 548,190 C552,166 552,140 546,120 Z" {LUNG}/>')
# mediasten yapilari
s.add(f'<ellipse cx="490" cy="172" rx="50" ry="58" fill="white" stroke="{NEU}" stroke-opacity="0.6"/>')
s.text(490, 170, "kalp", "small", anchor="middle")
s.text(490, 183, "(perikard)", "small", anchor="middle")
s.add(f'<circle cx="512" cy="256" r="11" fill="white" stroke="{NEU}" stroke-opacity="0.6"/>')
s.add(f'<circle cx="490" cy="250" r="6" fill="white" stroke="{NEU}" stroke-opacity="0.6"/>')
lead(s, 600, 330, 514, 266)
s.text(604, 334, "aorta", "small")
# resesler
lead(s, 396, 334, 462, 290, CYAN, 0.8)
s.text(336, 346, "recessus vertebromediastinalis: yuvarlak", "cyanb", fs2=10.5)
lead(s, 420, 54, 466, 74, CYAN, 0.8)
lead(s, 556, 54, 510, 78, CYAN, 0.8)
s.text(380, 50, "rec. costomediastinalis", "cyanb", anchor="middle", fs2=10)
s.text(598, 50, "solda daha geniş", "cyanb", anchor="middle", fs2=10)
s.text(598, 62, "(incisura cardiaca)", "cyan", anchor="middle", fs2=9.5)
save(s, "m4k7_resesler")

# =============================================================== 4.5 Akciger ve plevra alt sinirlari (dumbbell)
s = SVG(640, 300, "Akcigerin ve plevranin alt sinirlarinin uc cizgide kaburga duzeyleri: akciger 6-8-10, plevra 8-10-12", "k74b")
X0, X1 = 120, 610
def yr(r):
    return 40 + (r - 5) * 30
for r in range(5, 13):
    y = yr(r)
    s.add(f'<line x1="{X0}" y1="{y}" x2="{X1}" y2="{y}" stroke="{NEU}" stroke-opacity="0.15" stroke-width="1"/>')
    s.text(X0 - 10, y + 4, f"{r}. kaburga", "small", anchor="end")
cols = [(220, "Midklaviküler çizgi", 6, 8), (380, "Orta aksiller çizgi", 8, 10), (540, "Paravertebral çizgi", 10, 12)]
for (x, lab, a, p_) in cols:
    s.add(f'<line x1="{x}" y1="{yr(a)}" x2="{x}" y2="{yr(p_)}" stroke="{CYAN}" stroke-opacity="0.22" stroke-width="14" stroke-linecap="round"/>')
    s.add(f'<circle cx="{x}" cy="{yr(a)}" r="7" fill="{CYAN}"/>')
    s.add(f'<circle cx="{x}" cy="{yr(p_)}" r="7" fill="white" stroke="{TXT}" stroke-width="2"/>')
    s.text(x + 14, yr(a) + 4, f"akciğer {a}", "cyanb", fs2=11.5)
    s.text(x + 14, yr(p_) + 4, f"plevra {p_}", "title", fs1=11.5)
    s.text(x, 286, lab, "small", anchor="middle")
s.text(X0 + 4, 16, "Dolu daire: akciğerin alt kenarı (sessiz solunum, 6-8-10) · boş daire: plevranın alt kenarı (8-10-12)", "small")
s.text(X0 + 4, 29, "Aradaki bant: akciğerin girmediği recessus costodiaphragmaticus (yaklaşık iki kaburga)", "small")
save(s, "m4k7_projeksiyon")

# =============================================================== 4.6 Tansiyon pnomotoraks zinciri
s = SVG(640, 470, "Tansiyon pnomotoraksin mekanizmasi: tek yonlu kapak, artan plevral basinc, mediastinal kayma, venoz donusun azalmasi", "k74c")
s.box(140, 6, 360, 46, ["Akciğerde ya da göğüs duvarında", "tek yönlü kapakçık gibi davranan bir delik"], fs1=12.5)
s.arrow(320, 52, 320, 74)
s.box(140, 76, 360, 46, ["İnspirasyonda hava plevral boşluğa girer,", "ekspirasyonda delik kapanır, hava çıkamaz"], fs1=12.5)
s.arrow(320, 122, 320, 144)
s.box(140, 146, 360, 46, ["Her solukta plevral basınç biraz daha artar", "ve atmosfer basıncının üstüne çıkar"], kind="key", fs1=12.5)
s.arrow(320, 192, 320, 214)
s.box(140, 216, 360, 46, ["Aynı taraf akciğer tamamen çöker", "mediasten karşı tarafa itilir"], fs1=12.5)
s.path("M240,262 L240,280 L130,280 L130,300")
s.path("M400,262 L400,280 L510,280 L510,300")
s.box(10, 302, 240, 58, ["Karşı akciğer sıkışır", "ventilasyon ve oksijenlenme", "bozulur → hipoksi"], fs1=12)
s.box(390, 302, 240, 58, ["VCS ve VCİ bükülür, sıkışır", "venöz dönüş ve kalp debisi düşer", "→ hipotansiyon, şok"], fs1=12)
s.path("M130,360 L130,380 L300,380 L300,394")
s.path("M510,360 L510,380 L340,380 L340,394")
s.box(110, 396, 420, 30, ["Trakea karşıya, boyun venleri dolgun, hipersonorite, solunum sesi yok"], fs1=11.5)
s.arrow(320, 426, 320, 440)
s.box(170, 442, 300, 26, ["Acil iğne dekompresyonu, sonra göğüs tüpü"], kind="mag", fs1=11.5)
save(s, "m4k7_pnomotoraks")

# =============================================================== 5.1 Hilus duzeni (sag ve sol, medial yuz)
s = SVG(640, 330, "Sag ve sol akciger hilusundaki yapilarin dizilimi: onden arkaya ven-arter-bronş; sagda en ustte eparteriyel bronş, solda en ustte pulmoner arter", "k75a")
BR = f'fill="white" stroke="{NEU}" stroke-width="3.5"'
AR = f'fill="{CYAN}" fill-opacity="0.55" stroke="{CYAN}" stroke-width="1.2"'
VN = f'fill="{NEU}" fill-opacity="0.35" stroke="{NEU}" stroke-opacity="0.7" stroke-width="1.2"'
def hil(ox, title, items, notes):
    s.text(ox + 150, 16, title, "title", anchor="middle", fs1=12.5)
    s.text(ox + 26, 48, "ARKA", "cap", anchor="middle")
    s.text(ox + 274, 48, "ÖN", "cap", anchor="middle")
    s.add(f'<path d="M{ox+150},52 C{ox+215},52 {ox+250},100 {ox+246},150 C{ox+242},196 {ox+205},218 {ox+170},224 L{ox+160},300 L{ox+140},300 L{ox+132},222 C{ox+95},214 {ox+58},188 {ox+56},146 C{ox+54},96 {ox+88},52 {ox+150},52 Z" fill="none" stroke="{CYAN}" stroke-width="1.6"/>')
    for (cx, cy, r, kind, lab, lx, ly, anc) in items:
        style = {"B": BR, "A": AR, "V": VN}[kind]
        s.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" {style}/>')
        s.text(cx, cy + 4, kind, "title", anchor="middle", fs1=11)
        if lab:
            lead(s, cx, cy, lx, ly - 4)
            s.text(lx, ly, lab, "small", anchor=anc)
    s.text(ox + 150, 316, "lig. pulmonale", "small", anchor="middle")
    for (x, y, t, st) in notes:
        s.text(x, y, t, st, anchor="middle", fs2=10.5)
hil(0, "Sağ akciğer hilusu", [
    (130, 92, 13, "B", "", 0, 0, "start"),
    (172, 116, 17, "A", "", 0, 0, "start"),
    (124, 140, 18, "B", "", 0, 0, "start"),
    (206, 152, 15, "V", "", 0, 0, "start"),
    (164, 188, 15, "V", "", 0, 0, "start")], [(150, 31, "arter bronşun önünde, eparteriyel bronşun altında", "cyanb")])
hil(330, "Sol akciğer hilusu", [
    (474, 96, 18, "A", "", 0, 0, "start"),
    (452, 142, 19, "B", "", 0, 0, "start"),
    (512, 144, 15, "V", "", 0, 0, "start"),
    (482, 190, 15, "V", "", 0, 0, "start")], [(480, 31, "arter en üstte, bronşun üzerinden aşar", "cyanb")])
lead(s, 124, 80, 124, 73)
s.text(30, 66, "eparteriyel bronş (üst lob)", "small")
lead(s, 112, 154, 96, 192)
s.text(20, 208, "bronchus intermedius", "small")
s.text(320, 270, "A: a. pulmonalis", "small", anchor="middle")
s.text(320, 283, "B: bronş", "small", anchor="middle")
s.text(320, 296, "V: vv. pulmonales", "small", anchor="middle")
s.text(320, 309, "(sup. önde, inf. en altta)", "small", anchor="middle")
s.text(320, 60, "Önden arkaya:", "cyanb", anchor="middle", fs2=10.5)
s.text(320, 73, "ven → arter → bronş", "cyan", anchor="middle", fs2=10.5)
s.text(320, 120, "önden n. phrenicus", "small", anchor="middle")
s.text(320, 133, "arkadan n. vagus", "small", anchor="middle")
s.text(320, 160, "üstte: sağda v. azygos,", "small", anchor="middle")
s.text(320, 173, "solda arcus aortae", "small", anchor="middle")
save(s, "m4k7_hilus")

# =============================================================== 5.3 Sag ve sol ana bronslar
s = SVG(640, 300, "Sag ve sol ana bronsun karsilastirilmasi: sag kisa genis dik ve uzerinden v. azygos gecer; sol uzun dar egik ve arcus aortae altindan gecer", "k75b")
# aort kemeri ve inen aorta (arkada, sol)
s.add(f'<path d="M300,118 C296,46 404,40 412,104 L414,286" stroke="{NEU}" stroke-opacity="0.22" stroke-width="24" fill="none"/>')
s.text(430, 60, "arcus aortae", "small")
# azygos kemeri (sag)
s.add(f'<path d="M206,286 L206,156 C206,126 186,112 160,116" stroke="{NEU}" stroke-opacity="0.35" stroke-width="10" fill="none" stroke-linecap="round"/>')
s.text(156, 106, "arcus v. azygos → VCS", "small", anchor="end")
# trakea ve bronslar
s.add(f'<line x1="320" y1="14" x2="320" y2="124" stroke="{NEU}" stroke-opacity="0.55" stroke-width="34" stroke-linecap="butt"/>')
for y in range(22, 120, 13):
    s.add(f'<line x1="304" y1="{y}" x2="336" y2="{y}" stroke="white" stroke-opacity="0.8" stroke-width="2"/>')
s.add(f'<line x1="316" y1="122" x2="282" y2="196" stroke="{NEU}" stroke-opacity="0.55" stroke-width="28" stroke-linecap="round"/>')
s.add(f'<line x1="324" y1="122" x2="436" y2="236" stroke="{NEU}" stroke-opacity="0.55" stroke-width="20" stroke-linecap="round"/>')
s.text(338, 70, "trakea", "small")
# acilar (dikeye gore)
s.add(f'<line x1="320" y1="124" x2="320" y2="250" stroke="{CYAN}" stroke-width="1"/>')
s.add(f'<path d="M320,200 A76,76 0 0 1 288,193" stroke="{CYAN}" stroke-width="1.6" fill="none"/>')
s.add(f'<path d="M320,214 A90,90 0 0 0 384,188" stroke="{CYAN}" stroke-width="1.6" fill="none"/>')
s.text(298, 222, "≈25°", "cyanb", anchor="end", fs2=11)
s.text(360, 222, "≈45°", "cyanb", fs2=11)
lead(s, 298, 116, 316, 124)
s.text(296, 112, "karina (T4-T5)", "small", anchor="end")
# etiketler
s.text(20, 196, "Sağ ana bronş", "title", fs1=12.5)
s.text(20, 211, "kısa (≈2,5 cm), geniş, dik", "body", fs2=11)
s.text(20, 225, "üzerinden v. azygos geçer", "body", fs2=11)
s.text(20, 239, "üst lob bronşu hilustan önce ayrılır", "small")
s.text(20, 266, "Yabancı cisimler çoğunlukla sağa kaçar", "cyanb", fs2=11)
s.text(470, 196, "Sol ana bronş", "title", fs1=12.5)
s.text(470, 211, "uzun (≈5 cm), dar, eğik", "body", fs2=11)
s.text(470, 225, "arcus aortae'nın altından,", "body", fs2=11)
s.text(470, 239, "özofagus ve aortanın önünden", "body", fs2=11)
s.text(470, 253, "geçer", "body", fs2=11)
save(s, "m4k7_ana_bronslar")

# =============================================================== 5.4 Hava yolu basamaklari ve duvar yapisi
rows = [("Trachea", "0", ""), ("Bronchus principalis", "1", "P"), ("Bronchus lobaris", "2", "L"), ("Bronchus segmentalis", "3", "S"),
        ("Küçük bronşlar", "4-10", ""), ("Bronchiolus (lobularis) · < 1 mm", "11-15", "L"), ("Bronchiolus terminalis", "16", "T"),
        ("Bronchiolus respiratorius", "17-19", "R"), ("Ductus alveolaris", "20-22", ""), ("Saccus alveolaris · alveol", "23", "")]
feats = [("kıkırdak", 0, 4), ("bez", 0, 4), ("goblet h.", 0, 5), ("silyalı epitel", 0, 7), ("kulüp h.", 5, 7), ("düz kas", 0, 8), ("gaz değişimi", 7, 9)]
RY0, RH = 72, 27
H = RY0 + len(rows) * RH + 34
s = SVG(640, H, "Hava yolunun basamaklari, kusak (generasyon) numaralari, duvar yapisindaki ogelerin hangi duzeye kadar devam ettigi ve iletici bolge ile solunum bolgesi", "k75c")
s.text(12, 60, "Hava yolu", "cap")
s.text(236, 60, "kuşak", "cap", anchor="middle")
for i, (name, gen, code) in enumerate(rows):
    y = RY0 + i * RH
    s.add(f'<rect x="12" y="{y}" width="200" height="{RH-5}" rx="3" fill="white" stroke="{NEU}" stroke-opacity="0.35"/>')
    s.text(20, y + 15, name, "body", fs2=10.5)
    s.text(236, y + 15, gen, "small", anchor="middle")
    if code:
        s.text(262, y + 15, code, "cyanb", anchor="middle", fs2=12)
for j, (fname, a, b) in enumerate(feats):
    x = 300 + j * 40
    s.text(x - 4, 60, fname, "small", anchor="start", rotate=-38)
    y1, y2 = RY0 + a * RH + 3, RY0 + b * RH + RH - 8
    col = CYAN if fname == "gaz değişimi" else NEU
    op = "0.7" if fname == "gaz değişimi" else "0.45"
    s.add(f'<rect x="{x-7}" y="{y1}" width="14" height="{y2-y1}" rx="4" fill="{col}" fill-opacity="{op}"/>')
# bolge parantezleri
yb = RY0 + 7 * RH - 3
s.add(f'<path d="M588,{RY0} L596,{RY0} L596,{yb} L588,{yb}" stroke="{NEU}" stroke-width="1.2" fill="none"/>')
s.add(f'<path d="M588,{yb+5} L596,{yb+5} L596,{RY0 + 10*RH - 5} L588,{RY0 + 10*RH - 5}" stroke="{CYAN}" stroke-width="1.6" fill="none"/>')
s.text(612, (RY0 + yb) / 2 + 40, "iletici bölge", "small", anchor="middle", rotate=-90)
s.text(626, (RY0 + yb) / 2 + 40, "ölü boşluk ≈150 mL", "small", anchor="middle", rotate=-90)
s.text(614, (yb + RY0 + 10 * RH) / 2 + 28, "solunum", "cyanb", anchor="middle", rotate=-90, fs2=10)
s.text(628, (yb + RY0 + 10 * RH) / 2 + 28, "(asinüs)", "cyan", anchor="middle", rotate=-90, fs2=10)
s.text(12, H - 10, "PLSLTR (\"PLeaSe LaTeR\"): Principalis · Lobaris · Segmentalis · Lobularis · Terminalis · Respiratorius", "cyanb", fs2=10.5)
save(s, "m4k7_hava_yolu")

# =============================================================== 6.5 Akcigerin lenf drenaji
s = SVG(640, 476, "Akcigerin lenf drenaji: subplevral ve derin pleksustan hiler, trakeobronsiyal ve paratrakeal dugumlere, bronkomediastinal govdelere ve venoz acilara; sol alt lobun karina alti dugumler uzerinden saga gecisi", "k76a")
s.text(160, 16, "SAĞ AKCİĞER", "cap", anchor="middle")
s.text(480, 16, "SOL AKCİĞER", "cap", anchor="middle")
for ox in (20, 340):
    s.box(ox, 26, 130, 50, ["Yüzeyel pleksus", "subplevral: parankim,", "visseral plevra"], fs1=11.5, fs2=10, lh=13)
    s.box(ox + 150, 26, 130, 50, ["Derin pleksus", "bronş ve damar", "çevresi"], fs1=11.5, fs2=10, lh=13)
    s.arrow(ox + 215, 76, ox + 215, 96)
    s.box(ox + 150, 98, 130, 40, ["Nodi pulmonales", "lob bronşları üzerinde"], fs1=11.5, fs2=10, lh=13)
    s.path(f"M{ox+65},76 L{ox+65},168 L{ox+70},168")
    s.path(f"M{ox+215},138 L{ox+215},152 L{ox+160},152 L{ox+160},166")
    s.box(ox + 40, 168, 200, 40, ["Nodi bronchopulmonales", "hiler düğümler"], kind="key", fs1=12, fs2=10.5, lh=14)
s.box(220, 246, 200, 44, ["Nodi tracheobronchiales inf.", "karina altı düğümler (orta hat)"], fs1=11.5, fs2=10, lh=14)
s.box(20, 246, 170, 44, ["Nodi tracheobronch. sup.", "sağ"], fs1=11.5, fs2=10, lh=14)
s.box(450, 246, 170, 44, ["Nodi tracheobronch. sup.", "sol"], fs1=11.5, fs2=10, lh=14)
s.arrow(105, 208, 105, 244)
s.arrow(535, 208, 535, 244)
s.path("M200,208 L200,228 L280,228 L280,244")
s.path("M440,208 L440,228 L360,228 L360,244")
s.box(20, 318, 170, 40, ["Nodi paratracheales", "sağ"], fs1=11.5, fs2=10, lh=14)
s.box(450, 318, 170, 40, ["Nodi paratracheales", "sol"], fs1=11.5, fs2=10, lh=14)
s.arrow(105, 290, 105, 316)
s.arrow(535, 290, 535, 316)
s.path(f"M260,290 L260,304 L150,304 L150,316", CYAN, width=2)
s.path("M380,290 L380,304 L480,304 L480,316")
s.text(268, 314, "çoğunlukla sağa:", "cyanb", fs2=10)
s.text(268, 326, "sol alt lob sağ tarafa", "cyan", fs2=10)
s.text(268, 338, "da drene olur", "cyan", fs2=10)
s.arrow(105, 358, 105, 378)
s.arrow(535, 358, 535, 378)
s.box(20, 380, 170, 40, ["Truncus", "bronchomediastinalis dx."], fs1=11.5, fs2=11.5, lh=14)
s.box(450, 380, 170, 40, ["Truncus", "bronchomediastinalis sin."], fs1=11.5, fs2=11.5, lh=14)
s.arrow(105, 420, 105, 434)
s.arrow(535, 420, 535, 434)
s.box(20, 436, 170, 38, ["Ductus lymphaticus dexter", "→ sağ venöz açı"], kind="key", fs1=11, fs2=10.5, lh=14)
s.box(450, 436, 170, 38, ["Ductus thoracicus", "→ sol venöz açı"], kind="key", fs1=11, fs2=10.5, lh=14)
save(s, "m4k7_lenf")

# =============================================================== 6.6 Hava yolunun otonom innervasyonu ve ilaclar
s = SVG(640, 500, "Hava yolu duz kasinin parasempatik ve sempatik innervasyonu; ipratropium ve tiotropiumun M3 reseptorunu bloke ettigi nokta, salbutamol ve formoterolun beta2 reseptorunu uyardigi nokta", "k76b")
s.text(160, 16, "PARASEMPATİK", "cap", anchor="middle")
s.text(480, 16, "SEMPATİK", "cap", anchor="middle")
s.box(40, 26, 240, 42, ["N. vagus (preganglionik)", "beyin sapı → göğüs"], fs1=12)
s.arrow(160, 68, 160, 88)
s.box(40, 90, 240, 42, ["Gangliyonlar: pulmoner pleksus", "ve bronş duvarı (kısa postganglionik)"], fs1=12, fs2=10.5)
s.arrow(160, 132, 160, 190)
s.text(170, 152, "asetilkolin", "small")
s.block(160, 172, 34)
s.text(182, 176, "ipratropium (kısa etkili)", "mag", fs2=10.5)
s.text(182, 188, "tiotropium (uzun etkili)", "mag", fs2=10.5)
s.box(40, 192, 240, 42, ["M₃ reseptörü", "düz kas ve bez hücresi"], kind="key", fs1=12.5)
s.arrow(160, 234, 160, 254)
s.box(40, 256, 240, 42, ["Gq → fosfolipaz C → IP₃", "hücre içi Ca²⁺ ↑"], fs1=12)
s.arrow(160, 298, 160, 318)
s.box(40, 320, 240, 52, ["Bronkokonstriksiyon", "mukus salgısı ↑; pulmoner damarlarda", "vazodilatasyon"], fs1=12.5, fs2=10.5)
# sempatik
s.box(360, 26, 240, 42, ["T2-T4 yan boynuz (preganglionik)", "sempatik gövde"], fs1=12)
s.arrow(480, 68, 480, 88)
s.box(360, 90, 240, 42, ["Servikal ve üst torakal gangliyonlar", "postganglionik lif: noradrenalin (az)"], fs1=11.5, fs2=10.5)
s.box(500, 140, 130, 40, ["Dolaşımdaki", "adrenalin (adrenal)"], fs1=11.5, fs2=11.5, lh=14)
s.arrow(480, 132, 480, 190)
s.arrow(565, 180, 565, 190)
s.text(362, 150, "salbutamol, formoterol", "magb", fs2=10.5)
s.text(362, 162, "(β₂ agonist: yolu", "mag", fs2=10)
s.text(362, 174, "taklit eder)", "mag", fs2=10)
s.arrow(430, 176, 468, 190, MAG)
s.box(360, 192, 240, 42, ["β₂ reseptörü", "düz kas hücresi"], kind="key", fs1=12.5)
s.arrow(480, 234, 480, 254)
s.box(360, 256, 240, 42, ["Gs → adenilil siklaz → cAMP ↑", "protein kinaz A"], fs1=12)
s.arrow(480, 298, 480, 318)
s.box(360, 320, 240, 52, ["Bronkodilatasyon", "Ca²⁺ sarkoplazmik retikuluma alınır;", "bezlerde salgı ↓; damarlarda konstriksiyon"], fs1=12.5, fs2=10.5)
# alt not
s.box(40, 392, 560, 96, ["Aynı düz kas hücresinde iki zıt sinyal", "Vagus tonusu dinlenimde bile hava yolunu hafif daraltır; bu tonus gece artar.",
     "Antimuskarinik ilaç bu tonusu kaldırarak, β₂ agonist ise aynı hücrede ters yönde bir sinyal başlatarak",
     "bronşu genişletir. İnsan hava yolu düz kasında sempatik sinir ucu azdır: β₂ reseptörlerini daha çok",
     "dolaşımdaki adrenalin uyarır."], fs1=12, fs2=10.5, lh=15)
save(s, "m4k7_otonom")

# =============================================================== 7.2 Mediastinumun bolumleri (sagittal sematik)
s = SVG(640, 400, "Mediastinumun bolumleri: angulus sterni ile T4-T5 diski arasindaki duzlem; mediastinum superius ve inferius; inferius'un anterius, medium ve posterius bolumleri", "k77a")
VB = {}
for i in range(12):
    y = 30 + i * 28
    VB[f"T{i+1}"] = y
    s.add(f'<rect x="490" y="{y}" width="50" height="24" rx="4" fill="white" stroke="{NEU}" stroke-opacity="0.45"/>')
    s.text(515, y + 16, f"T{i+1}", "small", anchor="middle")
s.text(20, 20, "ÖN", "cap")
s.text(620, 20, "ARKA", "cap", anchor="end")
# bolge dolgulari
s.add(f'<path d="M98,88 L486,32 L486,140 L112,146 Z" fill="{NEU}" fill-opacity="0.08"/>')
s.add(f'<path d="M114,148 L486,142 L486,362 C400,342 330,300 300,292 C240,300 190,318 162,330 L150,300 Z" fill="{CYAN}" fill-opacity="0.07"/>')
s.add(f'<ellipse cx="300" cy="226" rx="96" ry="70" fill="white" stroke="{NEU}" stroke-opacity="0.7" stroke-width="1.4"/>')
s.add(f'<ellipse cx="300" cy="226" rx="96" ry="70" fill="{NEU}" fill-opacity="0.16"/>')
# sternum ve diyafram
s.add(f'<line x1="96" y1="86" x2="110" y2="142" stroke="{NEU}" stroke-opacity="0.6" stroke-width="12" stroke-linecap="round"/>')
s.add(f'<line x1="113" y1="149" x2="150" y2="300" stroke="{NEU}" stroke-opacity="0.6" stroke-width="12" stroke-linecap="round"/>')
s.add(f'<line x1="152" y1="304" x2="160" y2="330" stroke="{NEU}" stroke-opacity="0.45" stroke-width="7" stroke-linecap="round"/>')
s.add(f'<path d="M160,332 C200,312 250,292 300,292 C360,292 420,322 486,364" stroke="{NEU}" stroke-opacity="0.55" stroke-width="7" fill="none"/>')
s.text(330, 316, "diyafram", "small", anchor="middle")
s.text(60, 112, "manubrium", "small", anchor="middle")
s.text(84, 230, "corpus sterni", "small", anchor="middle", rotate=-76)
# duzlemler
s.add(f'<line x1="98" y1="86" x2="488" y2="30" stroke="{NEU}" stroke-opacity="0.6" stroke-width="1.2"/>')
s.text(200, 60, "apertura thoracis superior", "small", anchor="middle", rotate=-8)
s.add(f'<line x1="112" y1="146" x2="488" y2="140" stroke="{CYAN}" stroke-width="2"/>')
s.text(104, 150, "angulus sterni", "cyanb", anchor="end", fs2=10.5)
s.text(548, 145, "T4-T5 diski", "cyanb", fs2=10.5)
# etiketler
s.text(300, 98, "Mediastinum superius", "title", anchor="middle", fs1=13)
s.text(300, 114, "timus, büyük venler, arcus aortae ve dalları, nn. vagi ve phrenici,", "small", anchor="middle")
s.text(300, 127, "trakea, özofagus, ductus thoracicus", "small", anchor="middle")
s.text(300, 210, "Mediastinum medium", "title", anchor="middle", fs1=12.5)
s.text(300, 226, "perikard ve kalp, büyük damarların", "small", anchor="middle")
s.text(300, 239, "kökleri, ana bronşlar, nn. phrenici", "small", anchor="middle")
s.text(172, 196, "M.", "title", anchor="middle", fs1=11)
s.text(172, 209, "anterius", "title", anchor="middle", fs1=11)
lead(s, 172, 214, 176, 250)
s.text(440, 230, "M.", "title", anchor="middle", fs1=11)
s.text(440, 243, "posterius", "title", anchor="middle", fs1=11)
s.text(440, 262, "aorta desc.,", "small", anchor="middle")
s.text(440, 275, "özofagus, d. thor.,", "small", anchor="middle")
s.text(440, 288, "azygos, vagus", "small", anchor="middle")
s.text(300, 382, "Mediastinum inferius = anterius + medium + posterius (fibröz perikard ayırır)", "small", anchor="middle")
save(s, "m4k7_mediasten_bolum")

# =============================================================== 7.3 Mediastinum superius katmanlari
layers = [("Manubrium sterni", ["ön sınır; arka yüzüne m. sternohyoideus ve", "m. sternothyroideus tutunur"], "neu"),
          ("1 · Bez katmanı", ["timus (erişkinde yağ dokusuna dönüşmüş kalıntısı)"], ""),
          ("2 · Venöz katman", ["vv. brachiocephalicae, VCS'nin üst yarısı,", "v. intercostalis superior sinistra"], ""),
          ("3 · Arteriyel katman", ["arcus aortae ve dalları: truncus brachiocephalicus,", "a. carotis communis sinistra, a. subclavia sinistra"], "key"),
          ("    ilişkili sinirler", ["nn. vagi ve kardiyak dalları, sol n. laryngeus", "recurrens, nn. phrenici"], ""),
          ("4 · Visseral katman", ["trakea (önde) ve özofagus (arkada); paratrakeal", "ve trakeobronşiyal lenf düğümleri"], "key"),
          ("5 · Lenfatik", ["ductus thoracicus (özofagusun solunda)"], ""),
          ("T1-T4 vertebra gövdeleri", ["arka sınır; önlerinde m. longus colli"], "neu")]
RH7 = 46
s = SVG(640, 12 + len(layers) * RH7 + 6, "Mediastinum superius'taki yapilarin onden arkaya katman katman dizilimi", "k77b")
for i, (a_, bl, k) in enumerate(layers):
    y = 10 + i * RH7
    s.add(f'<rect x="60" y="{y}" width="570" height="{RH7-6}" rx="4" fill="white" stroke="{CYAN if k == "key" else NEU}" stroke-opacity="{1 if k == "key" else 0.35}" stroke-width="{1.5 if k == "key" else 1}"/>')
    if k == "neu":
        s.add(f'<rect x="60" y="{y}" width="570" height="{RH7-6}" rx="4" fill="{NEU}" fill-opacity="0.12"/>')
    s.text(72, y + 25, a_, "title", fs1=12)
    if len(bl) == 1:
        s.text(262, y + 25, bl[0], "body", fs2=11)
    else:
        s.text(262, y + 17, bl[0], "body", fs2=11)
        s.text(262, y + 31, bl[1], "body", fs2=11)
s.arrow(30, 20, 30, 10 + len(layers) * RH7 - 10)
s.text(22, 190, "önden arkaya", "small", anchor="middle", rotate=-90)
save(s, "m4k7_sup_katman")

# =============================================================== 7.6 Ductus thoracicus seyri
s = SVG(640, 470, "Ductus thoracicus'un seyri: cisterna chyli, hiatus aorticus, aorta ile v. azygos arasinda yukselis, T5 civarinda saga-sola gecis, sol venoz aci", "k77c")
lv = ["C7", "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12", "L1", "L2"]
Y = {n: 60 + i * 26 for i, n in enumerate(lv)}
MX = 340  # orta hat (vertebra govdelerinin ortasi)
for n in lv:
    s.add(f'<rect x="296" y="{Y[n]-10}" width="88" height="20" rx="3" fill="white" stroke="{NEU}" stroke-opacity="0.4"/>')
    s.text(303, Y[n] + 4, n, "small")
s.add(f'<line x1="{MX}" y1="{Y["C7"]-14}" x2="{MX}" y2="{Y["L2"]+12}" stroke="{NEU}" stroke-opacity="0.45" stroke-dasharray="3 3"/>')
s.text(MX, Y["C7"] - 20, "orta hat", "small", anchor="middle")
s.text(160, 18, "HASTANIN SAĞI", "cap", anchor="middle")
s.text(500, 18, "HASTANIN SOLU", "cap", anchor="middle")
# aorta (orta hattin solunda) ve azygos (sagda)
s.add(f'<path d="M400,{Y["T4"]} L384,{Y["T12"]} L378,{Y["L2"]+20}" stroke="{NEU}" stroke-opacity="0.25" stroke-width="20" fill="none"/>')
s.text(416, Y["T9"], "aorta", "small")
s.add(f'<path d="M280,{Y["L1"]} L280,{Y["T4"]+6} C280,{Y["T4"]-12} 262,{Y["T4"]-16} 244,{Y["T4"]-12}" stroke="{NEU}" stroke-opacity="0.5" stroke-width="5" fill="none"/>')
s.text(268, Y["T9"], "v. azygos", "small", anchor="end")
# venoz acilar
s.add(f'<path d="M560,{Y["C7"]-44} L520,{Y["C7"]-10}" stroke="{NEU}" stroke-opacity="0.55" stroke-width="6"/>')
s.add(f'<path d="M600,{Y["C7"]+6} L520,{Y["C7"]-10} L470,{Y["T1"]+10}" stroke="{NEU}" stroke-opacity="0.55" stroke-width="7" fill="none"/>')
s.text(568, Y["C7"] - 38, "v. jug. int.", "small")
s.text(604, Y["C7"] + 22, "v. subclavia sin.", "small", anchor="end")
s.add(f'<path d="M80,{Y["C7"]-44} L120,{Y["C7"]-10}" stroke="{NEU}" stroke-opacity="0.55" stroke-width="6"/>')
s.add(f'<path d="M40,{Y["C7"]+6} L120,{Y["C7"]-10} L170,{Y["T1"]+10}" stroke="{NEU}" stroke-opacity="0.55" stroke-width="7" fill="none"/>')
s.text(40, Y["C7"] + 26, "sağ venöz açı", "small")
# ductus lymphaticus dexter
s.add(f'<path d="M150,{Y["T2"]} C140,{Y["T1"]} 130,{Y["C7"]} 122,{Y["C7"]-8}" stroke="{CYAN}" stroke-width="2.4" fill="none"/>')
s.text(156, Y["T2"] + 12, "ductus lymphaticus dexter:", "cyanb", fs2=10)
s.text(156, Y["T2"] + 24, "sağ üst çeyreğin lenfi", "cyan", fs2=10)
# ductus thoracicus: T5 altinda orta hattin saginda, ustunde solunda
d = (f'M336,{Y["L2"]+16} C336,{Y["L1"]} 330,{Y["T12"]} 328,{Y["T11"]} L328,{Y["T6"]} '
     f'C328,{Y["T5"]} 352,{Y["T5"]} 354,{Y["T4"]} L354,{Y["T1"]} C356,{Y["C7"]-30} 440,{Y["C7"]-40} 516,{Y["C7"]-12}')
s.add(f'<path d="{d}" stroke="{CYAN}" stroke-width="3.2" fill="none"/>')
s.add(f'<ellipse cx="336" cy="{Y["L2"]+10}" rx="12" ry="18" fill="{CYAN}" fill-opacity="0.35" stroke="{CYAN}"/>')
s.text(318, Y["L2"] + 26, "cisterna chyli (L1-L2)", "cyanb", fs2=10.5, anchor="end")
s.text(422, Y["T12"] + 4, "hiatus aorticus (T12):", "small")
s.text(422, Y["T12"] + 16, "aorta ile v. azygos arasında", "small")
s.text(160, Y["T7"], "orta hattın sağında, özofagusun", "small", anchor="middle")
s.text(160, Y["T7"] + 12, "arkasında, aorta ile azygos arasında", "small", anchor="middle")
s.add(f'<circle cx="{MX}" cy="{Y["T5"]}" r="6" fill="white" stroke="{MAG}" stroke-width="2"/>')
s.text(422, Y["T5"] - 4, "T4-T6 (≈T5): sağdan sola geçer", "magb", fs2=10.5)
s.text(422, Y["T5"] + 10, "altında yaralanma → sağ şilotoraks", "mag", fs2=10)
s.text(422, Y["T5"] + 23, "üstünde yaralanma → sol şilotoraks", "mag", fs2=10)
s.text(422, Y["T4"] - 2, "özofagusun solunda yükselir", "small")
s.text(420, Y["T2"] + 2, "C7'de kemer yapar,", "cyanb", fs2=10.5)
s.text(420, Y["T2"] + 15, "sol venöz açıya açılır", "cyanb", fs2=10.5)
save(s, "m4k7_duktus")
