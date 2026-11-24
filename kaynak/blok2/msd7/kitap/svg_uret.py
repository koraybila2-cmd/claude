# MSD-7 kitabinin sekilleri -> svg/*.svg   (python3 -I svg_uret.py)
import math, os
D = os.path.dirname(os.path.abspath(__file__)) + "/svg"
F = 'style="display:block;font-family:Source Serif 4,Georgia,serif"'
INK, GRID, MUTED = "#3a3533", "#d9d4cf", "#6b6460"
C = ["#0b6e99", "#b4541a", "#5b3f8c", "#2e7d4f", "#8a1c3c"]
def yaz(ad, w, h, govde, etiket):
    open(f"{D}/{ad}.svg", "w", encoding="utf-8").write(f'<svg viewBox="0 0 {w} {h}" width="100%" {F} role="img" aria-label="{etiket}">\n<defs><marker id="ok" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>\n' + "\n".join(govde) + "\n</svg>\n")
def T(x, y, s, a="middle", fs=11, w=400, fill=INK, it=False): return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{a}" font-size="{fs}" font-weight="{w}" fill="{fill}"' + (' font-style="italic"' if it else "") + f'>{s}</text>'
def kutu(x, y, w, h, s, fill="#fff", st="#57534e", fs=11, bold=False, s2=None, s3=None):
    r = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{fill}" stroke="{st}"/>']
    satir = [z for z in (s, s2, s3) if z]; y0 = y + h / 2 - (len(satir) - 1) * 6.5 + 4
    for i, z in enumerate(satir): r.append(T(x + w / 2, y0 + i * 13, z, fs=fs if i == 0 else fs - 1.5, w=700 if (bold and i == 0) else 400))
    return "".join(r)
def ok(x1, y1, x2, y2, renk=INK, dash=""): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{renk}" stroke-width="1.3" marker-end="url(#ok)"' + (f' stroke-dasharray="{dash}"' if dash else "") + "/>"

def aralik(ad, satirlar, tikler, X, baslik_x, etiket, lejant):
    """yatay aralik cubuklari; satirlar: (isim, a, b, renk_idx, not)"""
    sol, ust, sh = 170, 34, 24; w = 780; h = ust + sh * len(satirlar) + 46
    g = []
    for v, s in tikler:
        x = X(v); g += [f'<line x1="{x:.1f}" y1="{ust - 6}" x2="{x:.1f}" y2="{ust + sh * len(satirlar)}" stroke="{GRID}" stroke-width="0.7"/>', T(x, ust + sh * len(satirlar) + 15, s, fs=10, fill=MUTED)]
    for i, (isim, a, b, ci, nt) in enumerate(satirlar):
        y = ust + i * sh + sh / 2
        g.append(T(sol - 8, y + 4, isim, "end", 11, 400, INK, True))
        x1, x2 = X(a), X(b)
        if x2 - x1 < 6: x1 -= 3; x2 += 3
        g.append(f'<rect x="{x1:.1f}" y="{y - 6}" width="{x2 - x1:.1f}" height="12" rx="4" fill="{C[ci]}"/>')
        if nt: g.append(T(x2 + 6, y + 4, nt, "start", 9.5, 400, MUTED))
    g.append(T(sol + (w - sol - 20) / 2, ust + sh * len(satirlar) + 34, baslik_x, fs=11))
    lx = sol
    for ci, s in lejant:
        g += [f'<rect x="{lx}" y="10" width="12" height="12" rx="3" fill="{C[ci]}"/>', T(lx + 17, 20, s, "start", 10.5)]; lx += 34 + 5.6 * len(s)
    yaz(ad, w, h, g, etiket)

# 1) kulucka suresi (saat, log)
def Xs(v): return 170 + (math.log10(v) - 0) / (math.log10(240) - 0) * 490
aralik("kulucka", [
    ("S. aureus", 1, 6, 0, "1-6 sa"), ("B. cereus (kusmalı)", 1, 6, 0, "1-6 sa"), ("B. cereus (ishalli)", 6, 16, 1, "6-16 sa"),
    ("C. perfringens", 8, 16, 1, "8-16 sa"), ("Norovirüs", 12, 48, 2, "12-48 sa"), ("V. parahaemolyticus", 4, 30, 1, "4-30 sa"),
    ("Salmonella (tifo dışı)", 6, 72, 2, "6-72 sa"), ("Shigella", 12, 72, 2, "1-3 gün"), ("ETEC", 24, 72, 1, "1-3 gün"),
    ("Campylobacter", 48, 120, 2, "2-5 gün"), ("EHEC O157", 24, 192, 2, "1-8 gün"), ("Y. enterocolitica", 24, 144, 2, "1-6 gün")],
    [(1, "1 sa"), (2, "2"), (6, "6 sa"), (16, "16 sa"), (24, "1 gün"), (72, "3 gün"), (168, "7 gün")], Xs,
    "Kuluçka süresi (logaritmik eksen)", "Besin kaynakli ishal etkenlerinin kulucka sureleri",
    [(0, "hazır toksin (besinde)"), (1, "bağırsakta salınan toksin"), (2, "çoğalma / invazyon")])

# 2) enfektif doz (log)
def Xd(v): return 170 + (math.log10(v) - 0.5) / (8.3 - 0.5) * 440
aralik("enfektif_doz", [
    ("Shigella", 10, 100, 4, "10-100 bakteri"), ("E. histolytica", 10, 100, 4, "10-100 kist"), ("Giardia", 10, 100, 4, "10-100 kist"),
    ("Cryptosporidium", 10, 100, 4, "~10-100 ookist"), ("Norovirüs", 10, 100, 4, "< 100 partikül"), ("Campylobacter", 1e2, 1e6, 0, "10²-10⁶"),
    ("Salmonella", 1e5, 1e5, 0, "~10⁵"), ("V. cholerae", 1e8, 1e8, 1, "~10⁸ (aside duyarlı)"), ("ETEC", 1e8, 1e8, 1, "~10⁸")],
    [(10, "10"), (100, "10²"), (1e4, "10⁴"), (1e6, "10⁶"), (1e8, "10⁸")], Xd,
    "Hastalık yapan en küçük etken sayısı (logaritmik)", "Ishal etkenlerinin enfektif dozlari",
    [(4, "çok düşük doz (kişiden kişiye)"), (0, "orta"), (1, "yüksek doz (su, besin)")])
print("svg tamam")

# 3) tifo patogenezi (kutu-ok zinciri)
g = []
def kk(x, y, s, s2=None, fill="#fff", st="#57534e", w=150, h=40, bold=True, ci=None):
    if ci is not None: fill = ["#e8f0f4", "#f6e9df", "#efe7f2", "#e6f0ea", "#f6e4ea"][ci]; st = C[ci]
    return kutu(x, y, w, h, s, fill, st, 10.5, bold, s2)
# üst sıra: giriş -> Peyer -> mezenter lenf -> kan1
yA = 30
g += [kk(20, yA, "Ağızdan alım", "ince bağırsak", ci=0, w=120),
      kk(165, yA, "M hücresi →", "Peyer plakları", ci=2, w=130),
      kk(315, yA, "Mezenterik", "lenf düğümü", ci=2, w=120),
      kk(455, yA, "Birincil", "bakteriyemi", ci=4, w=120)]
for x1, x2 in [(140, 165), (295, 315), (435, 455)]: g.append(ok(x1, yA + 20, x2, yA + 20))
# kan1 -> organlar
yB = 120
g.append(ok(515, yA + 40, 515, yB))
g += [kk(380, yB, "Karaciğer · dalak · kemik iliği", "makrofaj içinde çoğalma (1. hafta: kan + ilik kültürü +)", ci=3, w=280, h=42, bold=False)]
# organ -> kan2 -> safra
yC = 195
g.append(ok(520, yB + 42, 520, yC))
g += [kk(400, yC, "İkincil bakteriyemi → safra kesesi", "safrayla bağırsağa 2. dönüş (2-3. hafta: dışkı + idrar +)", ci=4, w=300, h=42, bold=False)]
# safra -> barsak geri (dongu)
g += [kk(60, yC, "Bağırsak lümeni", "Peyer plağı nekrozu → kanama, perforasyon (3-4. hafta)", ci=0, w=300, h=42, bold=False)]
g.append(ok(400, yC + 21, 362, yC + 21, C[4]))
# klinik kutusu
g += [kutu(60, 265, 620, 34, "Klinik: basamaklı ateş · rölatif bradikardi · gül lekeleri · hepatosplenomegali · önce ishal sonra kabızlık", "#faf7f2", INK, 10.5, False)]
g += [T(360, 20, "Enterik ateş (tifo) patogenezi", fs=13, w=700)]
yaz("tifo", 700, 312, g, "Enterik atesin basamaklari")
print("tifo eklendi")
