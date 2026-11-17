# Modul 1 farmakoloji semalarini uretir -> svg/*.svg   (python3 -I svg_uret.py)
import math, os
D = os.path.dirname(os.path.abspath(__file__)) + "/svg"
F = 'style="display:block;font-family:Source Serif 4,Georgia,serif"'
INK, GRID = "#3a3533", "#d9d4cf"
C = ["#0b6e99", "#b4541a", "#5b3f8c", "#2e7d4f", "#8a1c3c"]
def yaz(ad, w, h, govde, etiket):
    open(f"{D}/{ad}.svg", "w", encoding="utf-8").write(f'<svg viewBox="0 0 {w} {h}" width="100%" {F} role="img" aria-label="{etiket}">\n<defs><marker id="ok" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>\n' + "\n".join(govde) + "\n</svg>\n")
def T(x, y, s, a="middle", fs=11, w=400, fill=INK, it=False): return f'<text x="{x}" y="{y}" text-anchor="{a}" font-size="{fs}" font-weight="{w}" fill="{fill}"' + (' font-style="italic"' if it else "") + f'>{s}</text>'
def yol(pts, renk, sw=2.2, dash=""): return f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{renk}" stroke-width="{sw}" stroke-linejoin="round"' + (f' stroke-dasharray="{dash}"' if dash else "") + "/>"
def kutu(x, y, w, h, s, fill="#fff", st="#57534e", fs=11, bold=False, s2=None):
    r = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{fill}" stroke="{st}"/>']
    if s2: r += [T(x + w / 2, y + h / 2 - 2, s, fs=fs, w=700 if bold else 400), T(x + w / 2, y + h / 2 + 11, s2, fs=fs - 1.5)]
    else: r.append(T(x + w / 2, y + h / 2 + 4, s, fs=fs, w=700 if bold else 400))
    return "".join(r)
def ok(x1, y1, x2, y2, renk=INK, dash=""): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{renk}" stroke-width="1.3" marker-end="url(#ok)"' + (f' stroke-dasharray="{dash}"' if dash else "") + "/>"

# ---- Modul 1 semalari ----
# 1) iyon tuzagi
g = [f'<rect x="20" y="40" width="250" height="210" rx="10" fill="#fdecec" stroke="#b42318"/>', T(145, 64, "Plazma (pH 7,4)", fs=12.5, w=700),
     f'<rect x="420" y="40" width="250" height="210" rx="10" fill="#fff7e0" stroke="#b4541a"/>', T(545, 64, "Mide sıvısı (pH 1,5)", fs=12.5, w=700),
     f'<rect x="300" y="30" width="90" height="230" fill="#e9e4dc" stroke="#9a8f80"/>', T(345, 22, "Mide mukozası (lipit zar)", fs=10.5, it=True),
     kutu(70, 100, 70, 34, "B", "#fff", INK, 13, True, "yüksüz"), kutu(160, 170, 80, 34, "BH⁺", "#fff", INK, 13, True, "yüklü"),
     kutu(450, 100, 70, 34, "B", "#fff", INK, 13, True, "yüksüz"), kutu(560, 170, 80, 34, "BH⁺", "#fff", INK, 13, True, "yüklü"),
     ok(140, 112, 448, 112), T(300, 104, "yalnız yüksüz B geçer", fs=10.5, w=700), ok(140, 126, 168, 166), ok(520, 126, 568, 166),
     T(105, 226, "BH⁺ : B ≈ 4 : 1", fs=11), T(575, 226, "BH⁺ : B ≈ 3 milyon : 1", fs=11, w=700, fill=C[4]),
     f'<line x1="452" y1="210" x2="392" y2="210" stroke="{C[4]}" stroke-width="2"/>', T(420, 202, "✕ geri dönemez", "middle", 10.5, 700, C[4]),
     T(345, 282, "Zayıf baz (pKa 8, ör. morfin) damardan verilse de asidik midede yüklenip birikir. Asit ilaç ise bazik bölmede (alkali idrar) birikir.", fs=10.5, it=True)]
yaz("iyon_tuzagi", 690, 292, g, "Zayif bazik ilacin mide sivisinda iyon tuzagi ile birikmesi")

# 2) doz-yanit
def sig(x, ec, em): return em / (1 + 10 ** (1.2 * (ec - x)))
def panel(ox, baslik, seri, notlar):
    r = [T(ox + 150, 20, baslik, fs=12, w=700), f'<line x1="{ox}" y1="230" x2="{ox+300}" y2="230" stroke="{INK}"/>', f'<line x1="{ox}" y1="40" x2="{ox}" y2="230" stroke="{INK}"/>',
         T(ox + 150, 250, "log doz (derişim) →", fs=10.5), T(ox - 10, 135, "Etki", fs=10.5).replace("<text ", f'<text transform="rotate(-90 {ox-10} 135)" '),
         f'<line x1="{ox}" y1="60" x2="{ox+300}" y2="60" stroke="{GRID}" stroke-dasharray="3 3"/>', T(ox + 302, 63, "E<tspan>max</tspan>", "start", 9.5)]
    for ec, em, renk, dash, ad, lx, ly in seri:
        pts = [(ox + 15 + i * 2.8, 230 - sig(i / 20, ec, em)) for i in range(0, 101)]
        r.append(yol(pts, renk, 2.2, dash)); r.append(T(ox + lx, ly, ad, "start", 10.5, 700, renk))
    return r + notlar
g = panel(40, "Potens ve efikasi", [(1.6, 170, C[0], "", "A", 70, 80), (3.0, 170, C[1], "", "B", 165, 80), (2.2, 95, C[3], "", "C (parsiyel)", 210, 128)],
          [T(190, 280, "A, B'den daha potent (sola kaymış), efikasileri eşit.", fs=10, it=True), T(190, 294, "C'nin efikasisi düşük: doz artsa da A'ya ulaşmaz.", fs=10, it=True)])
g += panel(420, "Antagonizma", [(1.6, 170, C[0], "", "Agonist", 40, 80), (2.9, 170, C[2], "6 4", "+ yarışmalı", 205, 112), (2.0, 100, C[4], "6 4", "+ yarışmasız", 205, 150)],
          [T(570, 280, "Yarışmalı: eğri sağa kayar, E<tspan>max</tspan> aynı (aşılabilir).", fs=10, it=True), T(570, 294, "Yarışmasız: E<tspan>max</tspan> düşer (aşılamaz).", fs=10, it=True)])
yaz("doz_yanit", 760, 300, g, "Doz-yanit egrileri: potens, efikasi ve antagonizma")

# 3) opioid sinaps
g = [f'<path d="M40,30 h220 v120 q-110,50 -220,0 z" fill="#eef6f9" stroke="#0088b0"/>', T(150, 52, "1. nöron (C lifi) presinaptik uç", fs=11.5, w=700),
     f'<circle cx="110" cy="100" r="13" fill="#fff" stroke="#57534e"/><circle cx="145" cy="112" r="13" fill="#fff" stroke="#57534e"/><circle cx="180" cy="98" r="13" fill="#fff" stroke="#57534e"/>',
     T(145, 136, "glutamat, P maddesi", fs=10, it=True),
     f'<rect x="250" y="80" width="26" height="40" rx="4" fill="#fff" stroke="{C[4]}" stroke-width="2"/>', T(263, 105, "Ca", fs=10, w=700),
     T(290, 90, "Voltaj kapılı Ca²⁺ kanalı", "start", 10.5, 700), T(290, 104, "KAPANIR → verici salınamaz", "start", 10.5, 700, C[4]),
     f'<path d="M40,230 h220 v120 h-220 z" fill="#f7f4f2" stroke="#57534e"/>', T(150, 330, "2. nöron (arka boynuz)", fs=11.5, w=700),
     f'<rect x="250" y="250" width="26" height="40" rx="4" fill="#fff" stroke="{C[3]}" stroke-width="2"/>', T(263, 275, "K", fs=10, w=700),
     T(290, 262, "K⁺ kanalı (GIRK)", "start", 10.5, 700), T(290, 276, "AÇILIR → hiperpolarizasyon", "start", 10.5, 700, C[3]),
     ok(150, 172, 150, 226, INK, "4 3"), T(160, 202, "ağrı iletisi", "start", 10, 400, INK, True),
     kutu(70, 150, 70, 22, "μ reseptörü", "#fdecec", C[4], 10), kutu(70, 232, 70, 22, "μ reseptörü", "#fdecec", C[4], 10),
     f'<rect x="470" y="150" width="210" height="72" rx="4" fill="#fff" stroke="{INK}"/>', T(575, 172, "Opioid → G<tspan baseline-shift=\"sub\" font-size=\"8\">i/o</tspan>", fs=11.5, w=700),
     T(575, 192, "adenilat siklaz ↓, cAMP ↓", fs=10.5), T(575, 208, "Ca²⁺ kanalı kapanır, K⁺ kanalı açılır", fs=10.5),
     f'<rect x="470" y="250" width="210" height="82" rx="4" fill="#fff7e0" stroke="{C[1]}"/>', T(575, 272, "Beyin sapında (PAG)", fs=11, w=700),
     T(575, 292, "GABA ara nöronları susturulur", fs=10.5), T(575, 308, "→ inici serotonerjik ve noradrenerjik", fs=10.5), T(575, 322, "yol serbest kalır, ağrıyı keser", fs=10.5)]
yaz("opioid_sinaps", 700, 360, g, "Opioidlerin arka boynuzdaki presinaptik ve postsinaptik etkisi")

# 4) arasidonik asit
R_ = C[4]
g = [kutu(240, 14, 220, 32, "Zar fosfolipitleri", "#f7f4f2", "#57534e", 11.5, True), ok(350, 46, 350, 76), T(362, 64, "fosfolipaz A2", "start", 10.5),
     T(200, 64, "✕ glukokortikoidler", "end", 10.5, 700, R_),
     kutu(250, 80, 200, 32, "Araşidonik asit", "#eef6f9", "#0088b0", 12, True),
     ok(310, 112, 190, 150), ok(390, 112, 520, 150),
     T(230, 132, "COX-1, COX-2", "end", 10.5, 700), T(130, 116, "✕ NSAİİ, aspirin (geri dönüşsüz),", "start", 10.5, 700, R_).replace('x="130"', 'x="20"'), T(20, 130, "   koksibler (yalnız COX-2)", "start", 10.5, 700, R_),
     T(465, 132, "5-lipoksijenaz", "start", 10.5, 700), T(560, 146, "✕ zileuton", "start", 10.5, 700, R_),
     kutu(120, 154, 140, 30, "PGH2", "#fff", INK, 11.5, True), kutu(450, 154, 150, 30, "Lökotrienler", "#fff", INK, 11.5, True),
     T(560, 204, "bronş daralması, kemotaksi", fs=10.5), T(560, 218, "(montelukast reseptörü bloke eder)", fs=10, it=True),
     T(560, 236, "COX kapanınca araşidonik asit buraya kayar:", fs=10, it=True), T(560, 250, "aspirine duyarlı astım", fs=10, w=700, it=True),
     ok(150, 184, 75, 226), ok(190, 184, 225, 226), ok(230, 184, 375, 226),
     kutu(15, 230, 120, 30, "PGE2", "#fff", INK, 11, True), kutu(165, 230, 120, 30, "PGI2", "#fff", INK, 11, True), kutu(315, 230, 120, 30, "TXA2", "#fff", INK, 11, True),
     T(75, 276, "ağrı eşiği ↓, ateş,", fs=10), T(75, 289, "mide koruma, böbrek akımı", fs=10),
     T(225, 276, "endotelde (COX-2):", fs=10), T(225, 289, "antiagregan, vazodilatör", fs=10),
     T(375, 276, "trombositte (COX-1):", fs=10), T(375, 289, "agregasyon, vazokonstriksiyon", fs=10)]
yaz("arasidonik", 700, 300, g, "Arasidonik asit yolu ve ilaclarin etki noktalari")
print("4 svg yazildi")
