import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "build"))
from svglib import SVG, NEU, TXT, CYAN, MAG, FONT, esc

# Bolum 8 (yuzey ve radyolojik anatomi) sekilleri
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "svg")
os.makedirs(OUT, exist_ok=True)
BONE = 'stroke="var(--color-neutral-700)" stroke-opacity="0.42" stroke-linecap="round" fill="none"'
CART = 'stroke="var(--color-accent)" stroke-opacity="0.45" stroke-linecap="round" fill="none"'
SKIN = f'stroke="{NEU}" stroke-opacity="0.6" stroke-width="1.3" fill="none"'


def save(s, name):
    s.save(os.path.join(OUT, name + ".svg"))


def lead(s, x1, y1, x2, y2, color=NEU, op=0.55):
    s.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-opacity="{op}" stroke-width="0.9"/>')


def dot(s, x, y, color=NEU, r=2.2):
    s.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>')


def num(s, x, y, n, color=CYAN, r=7.5):
    s.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="white" stroke="{color}" stroke-width="1.3"/>')
    s.text(x, y + 3.5, str(n), "cyanb" if color == CYAN else "magb", anchor="middle", fs2=9.5)


def vline(s, x, y1, y2, color=CYAN, dash="5 3", w=1.2, op=1):
    s.add(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{color}" stroke-opacity="{op}" stroke-width="{w}" stroke-dasharray="{dash}"/>')


# =============================================================== 8.2 Oryantasyon cizgileri
def torso_side(cx, sg, top, bottom):
    return (f"M{cx+sg*15},{top} L{cx+sg*16},{top+18} C{cx+sg*30},{top+28} {cx+sg*66},{top+26} {cx+sg*84},{top+38} "
            f"C{cx+sg*94},{top+46} {cx+sg*93},{top+66} {cx+sg*90},{top+84} L{cx+sg*82},{top+190} "
            f"C{cx+sg*78},{top+220} {cx+sg*74},{top+240} {cx+sg*72},{bottom}")


s = SVG(640, 418, "Gogus duvarinin oryantasyon cizgileri: onden, sag yandan ve arkadan; cizgiler bir tarafta gosterilmistir", "k78a")
TOP, BOT = 40, 300
A, B, C = 110, 322, 532
s.text(A, 16, "ÖNDEN", "cap", anchor="middle")
s.text(B, 16, "SAĞ YANDAN · KOL YUKARIDA", "cap", anchor="middle")
s.text(C, 16, "ARKADAN", "cap", anchor="middle")
# --- A: on
for sg in (-1, 1):
    s.add(f'<path d="{torso_side(A, sg, TOP, BOT)}" {SKIN}/>')
    s.add(f'<path d="M{A+sg*10},{TOP+44} C{A+sg*30},{TOP+38} {A+sg*52},{TOP+48} {A+sg*80},{TOP+38}" stroke-width="5" {BONE}/>')
    s.add(f'<path d="M{A+sg*9},{TOP+168} C{A+sg*30},{TOP+196} {A+sg*55},{TOP+222} {A+sg*76},{TOP+232}" stroke-width="3" {CART}/>')
    s.add(f'<circle cx="{A+sg*47}" cy="{TOP+116}" r="3" fill="{NEU}" fill-opacity="0.55"/>')
s.add(f'<path d="M{A-12},{TOP+42} L{A+12},{TOP+42} L{A+9},{TOP+76} L{A-9},{TOP+76} Z" fill="white" stroke="{NEU}" stroke-opacity="0.55"/>')
s.add(f'<path d="M{A-9},{TOP+77} L{A+9},{TOP+77} L{A+9},{TOP+168} L{A-9},{TOP+168} Z" fill="white" stroke="{NEU}" stroke-opacity="0.55"/>')
s.add(f'<path d="M{A-6},{TOP+169} L{A+6},{TOP+169} L{A},{TOP+188} Z" fill="white" stroke="{NEU}" stroke-opacity="0.55"/>')
# isaretler (hastanin sagi, resmin solu)
s.text(A - 14, TOP + 80, "angulus sterni", "magb", anchor="end", fs2=10)
s.text(A - 47, TOP + 132, "meme başı", "small", anchor="middle")
s.text(A - 40, TOP + 250, "arcus costalis", "small", anchor="middle")
# cizgiler (hastanin solu)
for x, n, yy in ((A, 1, BOT + 14), (A + 11, 2, BOT + 32), (A + 28, 3, BOT + 14), (A + 44, 4, BOT + 32)):
    vline(s, x, TOP + 36, yy - 8)
    num(s, x, yy, n)
# --- B: sag yan, kol yukarida (on sagda)
s.add(f'<path d="M{B-60},{TOP+92} C{B-68},{TOP+150} {B-66},{TOP+210} {B-58},{BOT}" {SKIN}/>')
s.add(f'<path d="M{B+52},{TOP+72} C{B+64},{TOP+130} {B+62},{TOP+200} {B+50},{BOT}" {SKIN}/>')
s.add(f'<path d="M{B-40},{TOP+42} L{B-28},{TOP-20}" {SKIN}/>')
s.add(f'<path d="M{B+30},{TOP+40} L{B+20},{TOP-20}" {SKIN}/>')
s.add(f'<path d="M{B-40},{TOP+42} C{B-46},{TOP+64} {B-56},{TOP+84} {B-60},{TOP+96}" {SKIN}/>')
s.add(f'<path d="M{B+30},{TOP+40} C{B+38},{TOP+52} {B+46},{TOP+62} {B+52},{TOP+74}" {SKIN}/>')
s.add(f'<path d="M{B-40},{TOP+42} Q{B-4},{TOP+76} {B+30},{TOP+40}" stroke="{NEU}" stroke-opacity="0.45" stroke-width="1" fill="none"/>')
s.text(B - 5, TOP + 36, "koltuk altı", "small", anchor="middle")
lead(s, B + 44, TOP + 60, B + 60, TOP + 20)
s.text(B + 62, TOP + 16, "ön aksiller pli", "small")
lead(s, B - 50, TOP + 74, B - 62, TOP + 20)
s.text(B - 64, TOP + 16, "arka aksiller pli", "small", anchor="end")
for x, n, y0 in ((B + 40, 5, TOP + 66), (B - 4, 6, TOP + 60), (B - 46, 7, TOP + 74)):
    vline(s, x, y0, BOT + 6)
    num(s, x, BOT + 14, n)
s.text(B - 60, BOT + 18, "arka", "small", anchor="end")
s.text(B + 54, BOT + 18, "ön", "small")
# --- C: arka
for sg in (-1, 1):
    s.add(f'<path d="{torso_side(C, sg, TOP, BOT)}" {SKIN}/>')
    sup, spm, inf, lat = (C + sg * 40, TOP + 57), (C + sg * 41, TOP + 72), (C + sg * 46, TOP + 130), (C + sg * 86, TOP + 66)
    s.add(f'<path d="M{sup[0]},{sup[1]} L{inf[0]},{inf[1]} L{lat[0]},{lat[1]} Q{C+sg*62},{TOP+50} {sup[0]},{sup[1]} Z" fill="white" stroke="{NEU}" stroke-opacity="0.5" stroke-width="1.2"/>')
    s.add(f'<path d="M{spm[0]},{spm[1]} L{C+sg*90},{TOP+54}" stroke-width="3.2" {BONE}/>')
for i in range(13):
    y = TOP + 28 + i * 14.5
    dot(s, C, y, NEU, 3.4 if i == 0 else 2.3)
s.text(C - 8, TOP + 31, "C7", "small", anchor="end")
for yy, t in ((TOP + 71.5, "T3"), (TOP + 129.5, "T7")):
    s.add(f'<line x1="{C-44}" y1="{yy}" x2="{C-4}" y2="{yy}" stroke="{MAG}" stroke-opacity="0.7" stroke-width="1" stroke-dasharray="2 2"/>')
    s.text(C - 8, yy - 4, t, "magb", anchor="end", fs2=10)
s.text(C - 48, TOP + 146, "angulus inferior", "small", anchor="middle")
s.text(C - 8, TOP + 205, "T12", "small", anchor="end")
for x, n, yy, y0 in ((C + 46, 8, BOT + 14, TOP + 40), (C + 16, 9, BOT + 32, TOP + 30), (C, 10, BOT + 14, TOP + 34)):
    vline(s, x, y0, yy - 8)
    num(s, x, yy, n)
# lejant
leg = [(A - 92, [(1, "orta hat (l. mediana anterior)"), (2, "l. sternalis"), (3, "l. parasternalis"), (4, "l. medioclavicularis")]),
       (B - 92, [(5, "l. axillaris anterior"), (6, "l. axillaris media"), (7, "l. axillaris posterior")]),
       (C - 92, [(8, "l. scapularis"), (9, "l. paravertebralis"), (10, "orta hat (l. mediana posterior)")])]
for x0, items in leg:
    for i, (n, t) in enumerate(items):
        y = 356 + i * 16
        num(s, x0 + 8, y, n, r=6.8)
        s.text(x0 + 20, y + 3.8, t, "body", fs2=10.5)
save(s, "m4k7_cizgiler")

# =============================================================== 8.4 Kalbin izdusumu, kapaklar ve oskultasyon odaklari
s = SVG(640, 340, "Kalbin on gogus duvarina izdusumu, kapaklarin anatomik yeri ve oskultasyon odaklari", "k78c")
CX = 290
def yc(n):
    return 40 + n * 36
# kaburga kikirdaklari ve kaburgalar
for n in range(1, 8):
    for sg in (-1, 1):
        L = 46 + n * 8
        y0, y1 = yc(n), yc(n) + (n - 1) * 4
        s.add(f'<path d="M{CX+sg*20},{y0} L{CX+sg*L},{y1}" stroke-width="9" {CART}/>')
        s.add(f'<path d="M{CX+sg*L},{y1} Q{CX+sg*(L+60)},{y1+4} {CX+sg*(L+92)},{y1+22}" stroke-width="9" stroke="{NEU}" stroke-opacity="0.16" stroke-linecap="round" fill="none"/>')
for sg in (-1, 1):
    s.add(f'<path d="M{CX+sg*20},{yc(1)-26} C{CX+sg*60},{yc(1)-34} {CX+sg*100},{yc(1)-26} {CX+sg*150},{yc(1)-40}" stroke-width="7" {BONE}/>')
# sternum
s.add(f'<path d="M{CX-24},48 L{CX+24},48 L{CX+17},{yc(2)} L{CX+18},{yc(7)-2} L{CX+8},{yc(7)+2} L{CX},{yc(7)+26} L{CX-8},{yc(7)+2} L{CX-18},{yc(7)-2} L{CX-17},{yc(2)} Z" fill="white" stroke="{NEU}" stroke-opacity="0.55"/>')
s.add(f'<line x1="{CX-17}" y1="{yc(2)}" x2="{CX+17}" y2="{yc(2)}" stroke="{NEU}" stroke-opacity="0.5"/>')
for n in (2, 3, 4, 5):
    s.text(52, (yc(n) + yc(n + 1)) / 2 + 4, f"{n}. İKA", "small")
s.text(52, yc(2) + 4, "2. kıkırdak", "small", anchor="start")
# midklavikuler cizgi
MCL = CX + 120
vline(s, MCL, 30, 318, NEU, "4 3", 1, 0.55)
s.text(MCL, 332, "sol l. medioclavicularis", "small", anchor="middle")
# kalp
Ap, Bp, Cp, Dp = (CX + 32, yc(2) + 6), (CX - 32, yc(3) - 6), (CX - 32, yc(6)), (CX + 108, (yc(5) + yc(6)) / 2)
d = (f"M{Ap[0]},{Ap[1]} C{CX+10},{Ap[1]+6} {CX-10},{Bp[1]-8} {Bp[0]},{Bp[1]} "
     f"C{CX-44},{yc(4)} {CX-44},{yc(5)+16} {Cp[0]},{Cp[1]} "
     f"C{CX+10},{Cp[1]+6} {CX+70},{Cp[1]} {Dp[0]},{Dp[1]} "
     f"C{CX+132},{yc(4)+6} {CX+82},{Ap[1]+12} {Ap[0]},{Ap[1]} Z")
s.add(f'<path d="{d}" fill="{MAG}" fill-opacity="0.06" stroke="{MAG}" stroke-opacity="0.75" stroke-width="1.6"/>')
for p in (Ap, Bp, Cp, Dp):
    dot(s, p[0], p[1], MAG, 3.2)
# kapaklarin anatomik yeri
valves = {"P": (CX + 20, yc(3)), "A": (CX + 8, (yc(3) + yc(4)) / 2), "M": (CX + 10, yc(4)), "T": (CX - 6, (yc(4) + yc(5)) / 2)}
for k, (x, y) in valves.items():
    s.add(f'<rect x="{x-6}" y="{y-2.5}" width="12" height="5" rx="2" fill="{TXT}"/>')
# odaklar
foci = {"A": (CX - 30, (yc(2) + yc(3)) / 2), "P": (CX + 30, (yc(2) + yc(3)) / 2), "T": (CX + 30, (yc(4) + yc(5)) / 2 + 18), "M": (Dp[0], Dp[1])}
s.path(f"M{valves['A'][0]-6},{valves['A'][1]-3} C{CX-6},{yc(3)+2} {CX-16},{foci['A'][1]+10} {foci['A'][0]+12},{foci['A'][1]+4}", CYAN, width=1.3)
s.path(f"M{valves['P'][0]+3},{valves['P'][1]-4} L{foci['P'][0]-3},{foci['P'][1]+11}", CYAN, width=1.3)
s.path(f"M{valves['M'][0]+7},{valves['M'][1]+2} C{CX+40},{yc(4)+14} {CX+70},{Dp[1]-14} {Dp[0]-13},{Dp[1]-5}", CYAN, width=1.3)
s.path(f"M{valves['T'][0]+2},{valves['T'][1]+4} C{CX},{foci['T'][1]-2} {CX+6},{foci['T'][1]} {foci['T'][0]-12},{foci['T'][1]}", CYAN, width=1.3)
for k, (x, y) in foci.items():
    s.add(f'<circle cx="{x}" cy="{y}" r="11" fill="white" fill-opacity="0.9" stroke="{CYAN}" stroke-width="1.6"/>')
    s.text(x, y + 4.2, k, "cyanb", anchor="middle", fs2=11.5)
ex, ey = CX + 30, (yc(3) + yc(4)) / 2
s.add(f'<circle cx="{ex}" cy="{ey}" r="8" fill="white" stroke="{CYAN}" stroke-width="1" stroke-dasharray="2 2"/>')
s.text(ex, ey + 3.5, "E", "cyanb", anchor="middle", fs2=9.5)
# kenar etiketleri
s.text(CX - 46, yc(4) + 29, "sağ atriyum", "magb", anchor="end", fs2=10.5)
lead(s, CX + 82, yc(6) - 8, MCL + 6, yc(6) + 9, MAG, 0.8)
s.text(MCL + 8, yc(6) + 12, "sağ ventrikül", "magb", fs2=10.5)
s.text(MCL + 8, yc(5) + 2, "sol ventrikül", "magb", fs2=10.5)
# lejant
lx = 470
items = [("A", "Aort odağı", "sağ 2. İKA, sternum kenarı"), ("P", "Pulmoner odak", "sol 2. İKA, sternum kenarı"),
         ("E", "Erb noktası", "sol 3. İKA, sternum kenarı"), ("T", "Triküspit odağı", "sternumun sol alt kenarı"),
         ("M", "Mitral odak", "apeks: sol 5. İKA, MKÇ'nin içi")]
for i, (k, t1, t2) in enumerate(items):
    y = 40 + i * 30
    s.add(f'<circle cx="{lx}" cy="{y}" r="8" fill="white" stroke="{CYAN}" stroke-width="1.3"/>')
    s.text(lx, y + 3.6, k, "cyanb", anchor="middle", fs2=9.5)
    s.text(lx + 14, y + 1, t1, "title", fs1=10.5)
    s.text(lx + 14, y + 13, t2, "small")
s.add(f'<rect x="{lx-6}" y="{184-2.5}" width="12" height="5" rx="2" fill="{TXT}"/>')
s.text(lx + 14, 188, "kapağın gerçek yeri", "small")
dot(s, lx, 201, MAG, 3.2)
s.text(lx + 14, 205, "kalbin dört köşe noktası", "small")
save(s, "m4k7_kalp_odak")


# =============================================================== yardimcilar (bezier ornekleme, kirpma)
def bez(p0, p1, p2, p3, n=14):
    pts = []
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t ** 2, t ** 3
        pts.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return pts


def poly(pts):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


def lobe_fill(s, cid, outline, polys):
    """outline: lung path d; polys: [(points, fill, opacity)]"""
    s.add(f'<clipPath id="{cid}"><path d="{outline}"/></clipPath>')
    s.add(f'<g clip-path="url(#{cid})">' + "".join(
        f'<path d="{poly(p)}" fill="{f}" fill-opacity="{o}"/>' for p, f, o in polys) + '</g>')
    s.add(f'<path d="{outline}" fill="none" stroke="{TXT}" stroke-opacity="0.75" stroke-width="1.4"/>')


UL, ML, LL = (CYAN, 0.22), (MAG, 0.20), (NEU, 0.20)

# =============================================================== 8.3 Loblarin gogus duvarina izdusumu
s = SVG(640, 526, "Akciger loblarinin ve fissurlerin gogus duvarina izdusumu: onden, arkadan, sag ve sol yandan", "k78b")
P = {"A": (0, 0), "B": (320, 0), "C": (0, 252), "D": (320, 252)}
cap = {"A": "A · ÖNDEN", "B": "B · ARKADAN", "C": "C · SAĞ YANDAN", "D": "D · SOL YANDAN"}
for k, (ox, oy) in P.items():
    s.text(ox + 160, oy + 14, cap[k], "cap", anchor="middle")
# --- A: onden
ox, oy = P["A"]
s.add(f'<g transform="translate({ox},{oy})">')
s.add(f'<path d="M151,38 L169,38 L167,62 L166,162 L160,176 L154,162 L153,62 Z" fill="white" stroke="{NEU}" stroke-opacity="0.45"/>')
for sg in (-1, 1):
    s.add(f'<path d="M{160+sg*9},40 C{160+sg*40},34 {160+sg*70},40 {160+sg*100},30" stroke-width="5" {BONE}/>')
r_out = "M118,22 C134,24 150,44 156,62 L156,142 C140,146 118,148 100,150 C80,158 56,174 40,190 C34,150 36,90 58,52 C76,32 100,20 118,22 Z"
l_out = ("M202,22 C186,24 170,44 164,62 L164,102 C176,103 190,104 196,108 C200,118 196,130 188,138 C182,142 178,145 176,148 "
         "C190,150 206,152 220,152 C240,160 264,176 280,190 C286,150 284,90 262,52 C244,32 220,20 202,22 Z")
lobe_fill(s, "k78bAr", r_out, [([(0, 0), (160, 0), (160, 101.4), (42, 121), (0, 121.5)], *UL),
                               ([(42, 121), (160, 101.4), (160, 172)], *ML),
                               ([(0, 121.5), (42, 121), (160, 172), (160, 260), (0, 260)], *LL)])
lobe_fill(s, "k78bAl", l_out, [([(160, 0), (320, 0), (320, 102.9), (160, 175.6)], *UL),
                               ([(160, 175.6), (320, 102.9), (320, 260), (160, 260)], *LL)])
s.add(f'<path d="M156,102 L42,120 M42,122 L108,150 M278,122 L212,152" stroke="{TXT}" stroke-width="1.3" fill="none"/>')
s.text(100, 84, "üst lob", "body", anchor="middle", fs2=10)
s.text(126, 132, "orta lob", "body", anchor="middle", fs2=10)
s.text(224, 84, "üst lob", "body", anchor="middle", fs2=10)
lead(s, 50, 176, 30, 214)
s.text(30, 226, "alt lob", "body", anchor="middle", fs2=10)
lead(s, 268, 176, 288, 214)
s.text(288, 226, "alt lob", "body", anchor="middle", fs2=10)
lead(s, 186, 136, 222, 124)
s.text(226, 128, "lingula", "small")
s.add('</g>')
# --- B: arkadan
ox, oy = P["B"]
s.add(f'<g transform="translate({ox},{oy})">')
for i in range(14):
    dot(s, 160, 26 + i * 14, NEU, 2.8 if i == 0 else 1.8)
r_out = "M202,24 C226,26 262,52 276,90 C284,114 284,134 282,148 C250,152 212,160 178,168 L178,46 C180,34 190,26 202,24 Z"
l_out = "M118,24 C94,26 58,52 44,90 C36,114 36,134 38,148 C70,152 108,160 142,168 L142,46 C140,34 130,26 118,24 Z"
ob_r = bez((178, 68), (212, 84), (250, 108), (282, 132))
ob_l = bez((142, 68), (108, 84), (70, 108), (38, 132))
lobe_fill(s, "k78bBr", r_out, [([(160, 0), (320, 0), (320, 140), (300, 140)] + ob_r[::-1] + [(160, 60)], *UL),
                               ([(160, 60)] + ob_r + [(300, 140), (320, 140), (320, 260), (160, 260)], *LL)])
lobe_fill(s, "k78bBl", l_out, [([(160, 0), (0, 0), (0, 140), (20, 140)] + ob_l[::-1] + [(160, 60)], *UL),
                               ([(160, 60)] + ob_l + [(20, 140), (0, 140), (0, 260), (160, 260)], *LL)])
s.add(f'<path d="M178,68 C212,84 250,108 282,132 M142,68 C108,84 70,108 38,132" stroke="{TXT}" stroke-width="1.3" fill="none"/>')
s.text(164, 72, "T3", "magb", fs2=9.5)
s.text(92, 66, "üst lob", "body", anchor="middle", fs2=10)
s.text(228, 66, "üst lob", "body", anchor="middle", fs2=10)
s.text(92, 132, "alt lob", "body", anchor="middle", fs2=10)
s.text(228, 132, "alt lob", "body", anchor="middle", fs2=10)
s.text(70, 190, "sol akciğer", "small", anchor="middle")
s.text(250, 190, "sağ akciğer", "small", anchor="middle")
s.add('</g>')
# --- C: sag yandan (on sagda)
ox, oy = P["C"]
s.add(f'<g transform="translate({ox},{oy})">')
c_out = ("M138,24 C184,28 226,70 238,116 C244,138 242,156 238,168 C200,176 166,182 138,186 "
         "C104,190 72,196 46,200 C34,160 30,110 50,66 C70,38 104,22 138,24 Z")
s1 = bez((52, 62), (92, 90), (120, 112), (138, 124))
s2 = bez((138, 124), (170, 146), (200, 162), (224, 172))
obl = s1 + s2[1:]
lobe_fill(s, "k78bC", c_out, [([(0, 0), (320, 0), (320, 115), (240, 118)] + obl[:len(s1)][::-1] + [(20, 40), (0, 30)], *UL),
                              ([(320, 115), (240, 118)] + s2 + [(260, 190), (320, 190)], *ML),
                              ([(0, 30), (20, 40)] + obl + [(260, 190), (260, 260), (0, 260)], *LL)])
s.add(f'<path d="M52,62 C92,90 120,112 138,124 C170,146 200,162 224,172 M138,124 L240,118" stroke="{TXT}" stroke-width="1.3" fill="none"/>')
s.text(122, 72, "üst lob", "body", anchor="middle", fs2=10)
s.text(196, 146, "orta lob", "body", anchor="middle", fs2=10)
s.text(96, 160, "alt lob", "body", anchor="middle", fs2=10)
s.text(188, 112, "f. horizontalis", "cyan", anchor="middle", fs2=9.5)
s.text(70, 104, "f. obliqua", "cyan", anchor="middle", fs2=9.5)
s.text(44, 58, "T3", "magb", anchor="end", fs2=9.5)
s.text(246, 121, "4. kıkırdak", "magb", fs2=9.5)
s.text(232, 190, "6. kıkırdak", "magb", fs2=9.5)
dot(s, 138, 124, MAG, 3)
s.text(132, 140, "OAÇ'de 5. kaburga", "mag", anchor="end", fs2=9.5)
s.text(30, 228, "arka", "small")
s.text(250, 228, "ön", "small", anchor="end")
s.add('</g>')
# --- D: sol yandan (on solda)
ox, oy = P["D"]
s.add(f'<g transform="translate({ox},{oy})">')
d_out = ("M182,24 C136,28 94,70 82,116 C96,122 100,136 92,146 C86,152 80,158 82,168 C120,176 154,182 182,186 "
         "C216,190 248,196 274,200 C286,160 290,110 270,66 C250,38 216,22 182,24 Z")
t1 = bez((268, 62), (228, 90), (200, 112), (182, 124))
t2 = bez((182, 124), (150, 146), (120, 162), (96, 172))
obl = t1 + t2[1:]
lobe_fill(s, "k78bD", d_out, [([(320, 0), (0, 0), (0, 190), (60, 190)] + obl[::-1] + [(300, 40), (320, 30)], *UL),
                              ([(320, 30), (300, 40)] + obl + [(60, 190), (60, 260), (320, 260)], *LL)])
s.add(f'<path d="M268,62 C228,90 200,112 182,124 C150,146 120,162 96,172" stroke="{TXT}" stroke-width="1.3" fill="none"/>')
s.text(188, 76, "üst lob", "body", anchor="middle", fs2=10)
s.text(226, 162, "alt lob", "body", anchor="middle", fs2=10)
lead(s, 104, 163, 112, 196)
s.text(112, 207, "lingula", "small", anchor="middle")
lead(s, 92, 130, 64, 120)
s.text(62, 116, "inc. cardiaca", "small", anchor="end")
s.text(250, 104, "f. obliqua", "cyan", anchor="middle", fs2=9.5)
s.text(276, 58, "T3", "magb", fs2=9.5)
s.text(88, 190, "6. kıkırdak", "magb", anchor="end", fs2=9.5)
s.text(40, 228, "ön", "small")
s.text(290, 228, "arka", "small", anchor="end")
s.add('</g>')
# lejant
for i, ((col, op), t) in enumerate((((CYAN, 0.22), "üst lob (solda lingula dahil)"), ((MAG, 0.20), "orta lob (yalnız sağda)"), ((NEU, 0.20), "alt lob"))):
    x = 40 + i * 200
    s.add(f'<rect x="{x}" y="{503}" width="16" height="11" rx="2" fill="{col}" fill-opacity="{op}" stroke="{TXT}" stroke-opacity="0.5"/>')
    s.text(x + 22, 512, t, "body", fs2=10.5)
save(s, "m4k7_loblar")


# =============================================================== 8.6 PA akciger grafisinin anatomisi (sematik)
s = SVG(640, 470, "PA akciger grafisinin sematik anatomisi: mediastinal konturlar, hiluslar, diyafram, kostofrenik acilar ve kardiyotorasik oran", "k78e")
LUNG = 'fill="var(--color-neutral-700)" fill-opacity="0.24"'
r_f = ("M262,60 C228,60 186,92 164,142 C144,194 134,290 134,384 C150,350 200,332 236,336 C252,338 264,344 272,352 "
       "C252,324 244,288 264,260 C272,250 280,244 284,236 L288,130 C289,110 290,92 288,80 C282,66 272,60 262,60 Z")
l_f = ("M378,60 C412,60 454,92 476,142 C496,194 506,290 506,402 C500,378 490,364 474,360 C460,358 440,366 424,374 "
       "C434,352 436,318 426,296 C418,282 404,272 390,268 L386,250 C392,244 394,232 384,222 C376,214 376,208 382,200 "
       "C398,194 400,170 382,160 C372,140 360,110 352,80 C356,66 366,60 378,60 Z")
s.text(16, 18, "SAĞ", "cap")
s.text(624, 18, "SOL", "cap", anchor="end")
# omurga (kalbin arkasindan secilir)
for j in range(14):
    s.add(f'<rect x="304" y="{40+j*30}" width="32" height="24" rx="3" fill="none" stroke="{NEU}" stroke-opacity="0.22"/>')
s.add(f'<path d="{r_f}" {LUNG}/><path d="{l_f}" {LUNG}/>')
s.add(f'<clipPath id="k78eL"><path d="{r_f}"/><path d="{l_f}"/></clipPath>')
g = ['<g clip-path="url(#k78eL)">']
for i in range(10):
    y = 62 + i * 30
    g.append(f'<path d="M300,{y} C250,{y-14} 170,{y-10} 110,{y+34}" stroke="white" stroke-opacity="0.5" stroke-width="6" fill="none"/>')
    g.append(f'<path d="M340,{y} C390,{y-14} 470,{y-10} 530,{y+34}" stroke="white" stroke-opacity="0.5" stroke-width="6" fill="none"/>')
ves = [("M282,256 C270,236 252,214 236,188", 5), ("M236,188 C226,170 216,152 210,130", 3.2), ("M236,188 C220,184 204,176 190,166", 2.4),
       ("M280,268 C262,268 238,264 214,258", 4), ("M214,258 C200,254 186,250 172,248", 2.2), ("M282,276 C276,296 268,312 258,326", 4.4),
       ("M268,304 C252,312 236,318 214,322", 2.8),
       ("M414,232 C418,212 422,192 428,168", 4.4), ("M428,168 C434,152 440,136 446,116", 2.8), ("M428,168 C444,164 458,158 472,150", 2.2),
       ("M418,246 C432,250 446,252 460,254", 3.6), ("M460,254 C474,256 486,258 496,260", 2), ("M414,252 C428,274 442,298 456,318", 3.4),
       ("M440,298 C456,302 472,306 486,312", 2)]
for d_, w in ves:
    g.append(f'<path d="{d_}" stroke="white" stroke-opacity="0.85" stroke-width="{w}" stroke-linecap="round" fill="none"/>')
g.append('<ellipse cx="274" cy="268" rx="9" ry="20" fill="white" fill-opacity="0.75"/>')
g.append('<ellipse cx="414" cy="236" rx="10" ry="14" fill="white" fill-opacity="0.75"/>')
g.append('</g>')
s.add("".join(g))
s.add(f'<path d="{r_f}" fill="none" stroke="{TXT}" stroke-opacity="0.55" stroke-width="1.1"/><path d="{l_f}" fill="none" stroke="{TXT}" stroke-opacity="0.55" stroke-width="1.1"/>')
# klavikulalar
for d_ in ("M300,96 C260,88 200,74 150,64", "M340,96 C380,88 440,74 490,64"):
    s.add(f'<path d="{d_}" stroke="{NEU}" stroke-opacity="0.5" stroke-width="11" stroke-linecap="round" fill="none"/>')
    s.add(f'<path d="{d_}" stroke="white" stroke-width="8" stroke-linecap="round" fill="none"/>')
# trakea ve ana bronslar (hava: koyu)
for d_, w in (("M320,24 L320,150 C320,170 318,188 320,208", 15), ("M318,210 L294,252", 10), ("M323,210 L378,252", 9)):
    s.add(f'<path d="{d_}" stroke="{NEU}" stroke-opacity="0.42" stroke-width="{w}" stroke-linecap="round" fill="none"/>')
# mide gazi
s.add(f'<ellipse cx="462" cy="389" rx="22" ry="10" fill="{NEU}" fill-opacity="0.38"/>')
# KTO olcumu
s.add(f'<line x1="320" y1="282" x2="320" y2="350" stroke="{NEU}" stroke-opacity="0.6" stroke-dasharray="3 3"/>')
for (x1, x2, y, lab) in ((320, 254, 304, "a"), (320, 432, 335, "b")):
    s.add(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{CYAN}" stroke-width="1.4"/>')
    s.add(f'<line x1="{x2}" y1="{y-5}" x2="{x2}" y2="{y+5}" stroke="{CYAN}" stroke-width="1.4"/>')
    s.text((x1 + x2) / 2, y - 5, lab, "cyanb", anchor="middle", fs2=11)
s.add(f'<line x1="134" y1="368" x2="506" y2="368" stroke="{CYAN}" stroke-width="1.2" stroke-dasharray="5 3"/>')
for x in (134, 506):
    s.add(f'<line x1="{x}" y1="363" x2="{x}" y2="373" stroke="{CYAN}" stroke-width="1.4"/>')
s.text(176, 364, "c", "cyanb", anchor="middle", fs2=11)
s.text(320, 440, "Kardiyotorasik oran = (a + b) / c", "title", anchor="middle", fs1=12)
s.text(320, 456, "PA grafide normalde 0,5'ten küçük", "small", anchor="middle")
# etiketler
s.text(332, 30, "trakea", "small")
L = [(166, "v. cava superior", (286, 176)), (232, "sağ hilus (aşağıda)", (272, 262)), (300, "sağ atriyum", (255, 302)),
     (334, "sağ kubbe (yüksekte)", (226, 336)), (392, "kostofrenik açı", (137, 381))]
for y, t, (px, py) in L:
    lead(s, 126, y - 4, px, py)
    s.text(124, y, t, "body", anchor="end", fs2=10.5)
R = [(164, "aort topuzu", (395, 182)), (192, "AP pencere", (380, 208)), (218, "sol hilus (yukarıda)", (420, 228)),
     (244, "truncus pulmonalis", (391, 239)), (270, "sol aurikula (düz)", (388, 260)), (326, "sol ventrikül", (432, 334)),
     (354, "sol kubbe (aşağıda)", (476, 361)), (384, "mide gazı", (482, 388)), (412, "kostofrenik açı", (504, 401))]
for y, t, (px, py) in R:
    lead(s, 514, y - 4, px, py)
    s.text(516, y, t, "body", fs2=10.5)
save(s, "m4k7_pa_grafi")

# =============================================================== 8.7 Siluet isareti (aksiyel kesitte mekanizma)
s = SVG(640, 292, "Siluet isaretinin mekanizmasi: PA isin demeti kalbin sag kenarina teget gecer; kenar ancak kalp ile hava dolu orta lob arasinda yogunluk farki varsa gorulur", "k78f")
WATER = f'fill="{NEU}" fill-opacity="0.42"'
for k, ox in (("A", 0), ("B", 330)):
    s.add(f'<g transform="translate({ox},0)">')
    s.text(10, 14, "A · ORTA LOB DOLU" if k == "A" else "B · ALT LOB DOLU", "cap")
    s.add(f'<rect x="14" y="22" width="282" height="7" rx="2" fill="{NEU}" fill-opacity="0.55"/>')
    s.text(296, 14, "dedektör (önde)", "small", anchor="end")
    s.add(f'<ellipse cx="155" cy="152" rx="140" ry="88" fill="white" stroke="{NEU}" stroke-opacity="0.55" stroke-width="1.2"/>')
    rl = "M126,72 C80,76 32,104 28,150 C26,186 58,222 120,232 L150,214 L152,154.5 A52,42 0 0,1 152,89.5 L140,76 Z"
    ll = "M176,72 C230,74 282,104 286,150 C288,186 258,222 214,230 L206,214 L228,158 C244,140 246,104 224,86 C212,78 194,73 176,72 Z"
    mlp = [(0, 0), (160, 0), (160, 148), (146, 150), (28, 178), (0, 184)]
    llp = [(0, 184), (28, 178), (146, 150), (160, 148), (160, 300), (0, 300)]
    s.add(f'<clipPath id="k78f{k}"><path d="{rl}"/></clipPath>')
    filled = mlp if k == "A" else llp
    s.add(f'<g clip-path="url(#k78f{k})"><path d="{poly(filled)}" {WATER}/></g>')
    s.add(f'<path d="{rl}" fill="none" stroke="{TXT}" stroke-opacity="0.6" stroke-width="1.1"/>')
    s.add(f'<path d="{ll}" fill="none" stroke="{TXT}" stroke-opacity="0.45" stroke-width="1"/>')
    s.add(f'<line x1="28" y1="178" x2="146" y2="150" stroke="{TXT}" stroke-opacity="0.8" stroke-width="1.2" stroke-dasharray="4 2"/>')
    s.add(f'<ellipse cx="185" cy="122" rx="52" ry="42" {WATER} stroke="{TXT}" stroke-opacity="0.5"/>')
    s.add(f'<circle cx="196" cy="206" r="10" {WATER}/>')
    s.add(f'<circle cx="165" cy="220" r="15" fill="{NEU}" fill-opacity="0.3"/><circle cx="165" cy="226" r="5" fill="white"/>')
    s.add(f'<rect x="140" y="62" width="30" height="8" rx="2" fill="{NEU}" fill-opacity="0.3"/>')
    for x in (44, 88, 282):
        s.add(f'<line x1="{x}" y1="262" x2="{x}" y2="34" stroke="{NEU}" stroke-opacity="0.28" stroke-dasharray="3 3" marker-end="url(#k78f)"/>')
    col = MAG if k == "A" else CYAN
    s.add(f'<line x1="133" y1="262" x2="133" y2="34" stroke="{col}" stroke-width="1.6" marker-end="url(#k78f{"m" if k == "A" else "c"})"/>')
    s.add(f'<circle cx="133" cy="122" r="4" fill="white" stroke="{col}" stroke-width="1.6"/>')
    s.text(185, 120, "kalp", "body", anchor="middle", fs2=10.5)
    s.text(185, 133, "(su yoğunluğu)", "small", anchor="middle")
    s.text(74, 126, "orta lob", "title" if k == "A" else "body", anchor="middle", fs1=10.5, fs2=10.5)
    s.text(74, 139, "dolu" if k == "A" else "havalı", "small", anchor="middle")
    s.text(84, 204, "alt lob", "title" if k == "B" else "body", anchor="middle", fs1=10.5, fs2=10.5)
    s.text(84, 217, "dolu" if k == "B" else "havalı", "small", anchor="middle")
    if k == "A":
        s.add(f'<line x1="133" y1="18" x2="133" y2="33" stroke="{MAG}" stroke-width="2.5" stroke-dasharray="2 2"/>')
        s.text(140, 52, "sağ kalp kenarı: yok", "magb", fs2=10.5)
    else:
        s.add(f'<line x1="133" y1="18" x2="133" y2="33" stroke="{CYAN}" stroke-width="3"/>')
        s.text(140, 52, "sağ kalp kenarı: keskin", "cyanb", fs2=10.5)
    s.text(155, 282, "X ışını arkadan girer (PA)", "small", anchor="middle")
    s.add('</g>')
save(s, "m4k7_siluet")

# =============================================================== 8.7b Lateral grafi (sematik)
s = SVG(640, 410, "Lateral akciger grafisinin sematik anatomisi: retrosternal ve retrokardiyak bosluk, fissurler, hilus, diyafram kubbeleri, arka kostofrenik sinusler", "k78g")
s.text(186, 18, "ÖN", "cap", anchor="middle")
s.text(470, 18, "ARKA", "cap", anchor="middle")
lung = ("M206,58 C250,44 400,40 460,50 C468,130 474,260 478,392 C452,360 410,326 360,316 "
        "C300,306 236,322 186,340 L204,82 Z")
s.add(f'<path d="{lung}" {LUNG}/>')
# omurga: asagi dogru koyulasir (daha fazla akciger ust uste biner)
for j in range(12):
    y = 52 + j * 29
    x = 418 + 14 * math.sin(math.pi * j / 11)
    op = 0.04 + 0.24 * j / 11
    s.add(f'<rect x="{x:.1f}" y="{y}" width="30" height="24" rx="3" fill="{NEU}" fill-opacity="{op:.2f}" stroke="{NEU}" stroke-opacity="0.35"/>')
# sternum
s.add(f'<path d="M198,66 C192,140 186,240 180,330" stroke="{NEU}" stroke-opacity="0.5" stroke-width="11" stroke-linecap="round" fill="none"/>')
s.add('<path d="M198,66 C192,140 186,240 180,330" stroke="white" stroke-width="8" stroke-linecap="round" fill="none"/>')
# aorta
ao = "M262,196 C258,150 264,110 296,92 C326,78 360,90 376,124 C390,160 396,260 400,380"
s.add(f'<path d="{ao}" stroke="{NEU}" stroke-opacity="0.45" stroke-width="24" fill="none"/>')
s.add(f'<path d="{ao}" stroke="white" stroke-width="21.5" fill="none"/>')
# trakea
s.add(f'<path d="M300,26 C306,90 316,150 330,196" stroke="{NEU}" stroke-opacity="0.42" stroke-width="16" stroke-linecap="round" fill="none"/>')
# fissurler (kalbin golgesinde gorulmez)
s.add(f'<path d="M420,150 C380,210 300,280 228,328" stroke="{TXT}" stroke-width="1" fill="none"/>')
s.add(f'<path d="M284,190 L206,182" stroke="{TXT}" stroke-width="1" fill="none"/>')
# kalp
heart = ("M214,214 C242,198 286,192 316,206 C336,218 344,244 340,264 C338,286 326,304 306,320 "
         "C268,326 232,334 194,344 L202,264 C204,242 206,226 214,214 Z")
s.add(f'<path d="{heart}" fill="white" stroke="{TXT}" stroke-opacity="0.6" stroke-width="1.2"/>')
# hilus: sag PA uctan, sol PA kemer
s.add(f'<ellipse cx="300" cy="198" rx="14" ry="10" fill="white" stroke="{NEU}" stroke-opacity="0.6"/>')
s.add(f'<path d="M318,196 C330,176 352,176 366,204" stroke="{NEU}" stroke-opacity="0.55" stroke-width="14" fill="none" stroke-linecap="round"/>')
s.add('<path d="M318,196 C330,176 352,176 366,204" stroke="white" stroke-width="11" fill="none" stroke-linecap="round"/>')
# diyafram kubbeleri
s.add(f'<path d="M478,384 C450,346 400,300 330,298 C268,298 222,314 186,334" stroke="{TXT}" stroke-width="1.4" fill="none"/>')
s.add(f'<path d="M484,398 C460,370 420,334 370,322 C346,318 326,318 306,320" stroke="{TXT}" stroke-width="1.4" fill="none"/>')
s.add(f'<path d="M306,320 C270,324 232,334 196,346" stroke="{MAG}" stroke-width="1.2" stroke-dasharray="3 3" fill="none"/>')
s.add(f'<ellipse cx="352" cy="342" rx="18" ry="8" fill="{NEU}" fill-opacity="0.4"/>')
s.text(318, 22, "trakea", "small")
L = [(128, "retrosternal boşluk", (222, 140)), (194, "f. horizontalis", (226, 184)), (280, "sağ ventrikül (ön kenar)", (203, 280)),
     (326, "sağ kubbe: öne kadar", (214, 318)), (350, "sol kubbe: kalbin altında", (240, 336)), (366, "görünmez (silüet)", (240, 336))]
for y, t, (px, py) in L:
    if t != "görünmez (silüet)":
        lead(s, 172, y - 4, px, py, MAG if "sol kubbe" in t else NEU)
    s.text(170, y, t, "magb" if "sol kubbe" in t or "silüet" in t else "body", anchor="end", fs2=10.5)
R = [(92, "arcus aortae", (352, 88)), (150, "f. obliqua", (404, 172)), (198, "hilus (pulmoner arterler)", (354, 186)),
     (236, "sol atriyum (arka kenar)", (339, 242)), (270, "retrokardiyak boşluk", (380, 274)), (300, "sol ventrikül", (332, 292)),
     (330, "omurga aşağıda koyulaşır", (444, 334)), (358, "mide gazı", (368, 344)), (388, "arka kostofrenik sinüs", (478, 388))]
for y, t, (px, py) in R:
    lead(s, 494, y - 4, px, py)
    s.text(496, y, t, "body", fs2=10.5)
save(s, "m4k7_lateral")


# =============================================================== 8.8 BT: truncus pulmonalis bifurkasyonu duzeyi (T5-T6)
s = SVG(640, 330, "Toraks BT aksiyel kesit semasi, truncus pulmonalis bifurkasyonu duzeyi: ayak tarafindan bakis, hastanin sagi resmin solunda", "k78h")
s.text(16, 16, "HASTANIN SAĞI", "cap")
s.text(624, 16, "HASTANIN SOLU", "cap", anchor="end")
s.add(f'<ellipse cx="320" cy="165" rx="200" ry="135" fill="white" stroke="{NEU}" stroke-opacity="0.6" stroke-width="1.3"/>')
rl = ("M300,46 C220,40 140,84 128,160 C122,232 170,290 266,294 C284,280 290,268 290,258 C286,244 278,236 276,224 "
      "C268,212 248,210 238,200 C226,188 216,180 198,180 C186,176 184,160 198,152 C210,144 218,136 222,124 "
      "C224,110 234,100 248,96 C266,88 282,72 300,46 Z")
ll = ("M340,46 C420,40 500,84 512,160 C518,232 470,290 392,292 C384,286 398,276 404,262 C410,246 408,230 398,222 "
      "C394,214 394,206 392,202 C404,196 418,192 420,180 C422,166 410,146 398,134 C388,120 378,104 372,90 "
      "C362,72 350,58 340,46 Z")
for d_ in (rl, ll):
    s.add(f'<path d="{d_}" fill="{NEU}" fill-opacity="0.10" stroke="{NEU}" stroke-opacity="0.45"/>')
# kemik
s.add(f'<rect x="298" y="34" width="44" height="14" rx="5" fill="{NEU}" fill-opacity="0.35"/>')
s.add(f'<path d="M298,262 L302,284 L314,296 L320,302 L326,296 L338,284 L342,262 Z" fill="{NEU}" fill-opacity="0.35"/>')
s.add(f'<path d="M302,268 L274,278 M338,268 L366,278" stroke="{NEU}" stroke-opacity="0.35" stroke-width="7" stroke-linecap="round"/>')
s.add(f'<circle cx="320" cy="252" r="26" fill="{NEU}" fill-opacity="0.35"/>')
s.add('<circle cx="320" cy="282" r="8" fill="white"/>')
# pulmoner arterler (tek parca, esit opaklik)
s.add(f'<g opacity="0.32"><circle cx="348" cy="104" r="24" fill="{CYAN}"/>'
      f'<path d="M352,110 C376,124 392,146 402,172" stroke="{CYAN}" stroke-width="22" stroke-linecap="round" fill="none"/>'
      f'<path d="M340,118 C330,150 292,158 250,160 C232,161 220,162 208,165" stroke="{CYAN}" stroke-width="20" stroke-linecap="round" fill="none"/></g>')
# aorta
s.add(f'<g opacity="0.32"><circle cx="288" cy="118" r="26" fill="{MAG}"/><circle cx="380" cy="240" r="20" fill="{MAG}"/></g>')
s.add(f'<circle cx="288" cy="118" r="26" fill="none" stroke="{MAG}" stroke-width="1.2"/><circle cx="380" cy="240" r="20" fill="none" stroke="{MAG}" stroke-width="1.2"/>')
# venler
for (x, y, r) in ((238, 124, 15), (294, 226, 8)):
    s.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{NEU}" fill-opacity="0.3" stroke="{NEU}" stroke-opacity="0.7"/>')
# hava yollari ve ozofagus
for (x, y) in ((250, 190), (378, 192)):
    s.add(f'<circle cx="{x}" cy="{y}" r="12" fill="white" stroke="{TXT}" stroke-width="1.4"/>')
s.add(f'<circle cx="338" cy="214" r="11" fill="{NEU}" fill-opacity="0.14" stroke="{NEU}" stroke-opacity="0.7"/>')
s.text(320, 28, "sternum", "small", anchor="middle")
s.text(320, 322, "T5-T6 omuru", "small", anchor="middle")
L = [(70, "aorta ascendens", (266, 104)), (112, "v. cava superior", (226, 120)), (160, "a. pulmonalis dextra", (214, 163)),
     (196, "sağ ana bronş", (238, 192)), (236, "v. azygos", (287, 228))]
for y, t, (px, py) in L:
    lead(s, 118, y - 4, px, py)
    s.text(116, y, t, "body", anchor="end", fs2=10.5)
R = [(70, "truncus pulmonalis", (366, 90)), (150, "a. pulmonalis sinistra", (406, 162)), (194, "sol ana bronş", (390, 194)),
     (214, "özofagus", (349, 212)), (252, "aorta descendens", (400, 244))]
for y, t, (px, py) in R:
    lead(s, 522, y - 4, px, py)
    s.text(524, y, t, "body", fs2=10.5)
# lejant
lg = [(14, 286, MAG, 0.32, "aorta"), (96, 286, CYAN, 0.32, "pulmoner arter"), (14, 306, NEU, 0.3, "ven"), (96, 306, "white", 1, "hava yolu")]
for x, y, c, o, t in lg:
    st = f'stroke="{TXT}" stroke-width="1.2"' if c == "white" else 'stroke="none"'
    s.add(f'<rect x="{x}" y="{y-9}" width="14" height="11" rx="2" fill="{c}" fill-opacity="{o}" {st}/>')
    s.text(x + 20, y, t, "body", fs2=10.5)
s.text(626, 322, "ayak tarafından bakış", "small", anchor="end")
save(s, "m4k7_bt_kesit")

# =============================================================== 8.8b Hounsfield olcegi ve pencereler
s = SVG(640, 212, "Hounsfield olcegi ve akciger ile mediasten pencereleri: hangi yogunluk araligi gri tonlara yayiliyor", "k78i")
def hx(h):
    return 60 + (h + 1000) * 0.27
s.add('<defs>'
      '<linearGradient id="k78iL" x1="60" x2="600" y1="0" y2="0" gradientUnits="userSpaceOnUse">'
      '<stop offset="0" stop-color="#3c3c3c"/><stop offset="0.575" stop-color="#ffffff"/><stop offset="1" stop-color="#ffffff"/></linearGradient>'
      '<linearGradient id="k78iM" x1="60" x2="600" y1="0" y2="0" gradientUnits="userSpaceOnUse">'
      '<stop offset="0" stop-color="#1a1a1a"/><stop offset="0.42" stop-color="#1a1a1a"/><stop offset="0.62" stop-color="#ffffff"/>'
      '<stop offset="1" stop-color="#ffffff"/></linearGradient></defs>')
s.add(f'<line x1="{hx(-1000)}" y1="72" x2="{hx(1000)}" y2="72" stroke="{NEU}" stroke-opacity="0.6"/>')
for h, t in ((-1000, "−1000"), (-500, "−500"), (0, "0"), (500, "+500"), (1000, "+1000")):
    s.add(f'<line x1="{hx(h)}" y1="69" x2="{hx(h)}" y2="75" stroke="{NEU}" stroke-opacity="0.6"/>')
    s.text(hx(h), 87, t, "small", anchor="middle")
for a_, b_ in ((-900, -700), (-150, -50), (20, 60), (400, 1000)):
    s.add(f'<line x1="{hx(a_):.1f}" y1="70" x2="{hx(b_):.1f}" y2="70" stroke="{TXT}" stroke-opacity="0.55" stroke-width="5"/>')
marks = [(hx(-1000), 22, "hava −1000", "start"), (hx(-850), 40, "akciğer ≈ −850", "start"), (hx(-100), 22, "yağ ≈ −100", "end"),
         (hx(0), 40, "su 0", "middle"), (hx(40), 58, "kas, kan ≈ +40", "start"), (hx(400), 22, "kemik +400 … +1000", "start")]
for x, y, t, anc in marks:
    s.text(x if anc != "start" or t.startswith("hava") or t.startswith("kemik") else x - 12, y, t, "body", anchor=anc, fs2=10.5)
    if not t.startswith("kemik"):
        s.add(f'<line x1="{x:.1f}" y1="{y+4}" x2="{x:.1f}" y2="67" stroke="{NEU}" stroke-opacity="0.45" stroke-dasharray="2 2"/>')
for y, gid, title, note, lims in ((112, "k78iL", "Akciğer penceresi · S −600, G 1500", "akciğer dokusu gri tonlarda ayrışır; yumuşak doku ve kemik beyazlaşır", [(150, "+150")]),
                                  (174, "k78iM", "Mediasten penceresi · S +40, G 400", "akciğer tamamen siyah; kalp, damar, lenf düğümü ve yağ ayrışır", [(-160, "−160"), (240, "+240")])):
    s.text(60, y - 8, title, "title", fs1=11)
    s.add(f'<rect x="60" y="{y}" width="540" height="14" fill="url(#{gid})" stroke="{NEU}" stroke-opacity="0.4"/>')
    for h, t in lims:
        s.add(f'<line x1="{hx(h):.1f}" y1="{y-4}" x2="{hx(h):.1f}" y2="{y+18}" stroke="{CYAN}" stroke-width="1.2"/>')
        s.text(hx(h) + 4, y - 6, t, "cyanb", fs2=10)
    s.text(60, y + 28, note, "small")
save(s, "m4k7_hu_pencere")
