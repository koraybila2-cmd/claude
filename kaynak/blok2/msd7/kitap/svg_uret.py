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

# 4) enterosit iyon transportu: emilim (villus) ve salgi (kript)
g = []
INKL = "#8a857f"
def hucre(x, y, w, h, bas):
    return [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#fbf9f6" stroke="{INK}" stroke-width="1.4"/>',
            T(x + w / 2, y - 8, bas, fs=11.5, w=700)]
# --- sol: villus emici hucre ---
x0, y0, W0, H0 = 60, 60, 230, 180
g += hucre(x0, y0, W0, H0, "Villus ucu: EMİCİ hücre")
g += [T(x0 - 8, y0 + 16, "Lümen", "end", 10, 700, MUTED), T(x0 + W0 + 8, y0 + 16, "Kan", "start", 10, 700, MUTED)]
# apikal tasiyicilar
g += [kutu(x0 - 2, y0 + 26, 86, 26, "SGLT1", "#e8f0f4", C[0], 10, True),
      T(x0 + 92, y0 + 36, "Na⁺ + glukoz", "start", 9.5), T(x0 + 92, y0 + 47, "(ORS burada çalışır)", "start", 8.5, 400, MUTED, True)]
g += [kutu(x0 - 2, y0 + 70, 86, 26, "NHE3", "#e8f0f4", C[0], 10, True),
      T(x0 + 92, y0 + 78, "Na⁺ içeri / H⁺ dışarı", "start", 9.5), T(x0 + 92, y0 + 89, "Cl⁻/HCO₃⁻ ile eşleşir", "start", 8.5, 400, MUTED, True)]
# bazolateral pompa
g += [kutu(x0 + W0 - 84, y0 + 120, 86, 30, "Na⁺/K⁺", "#e6f0ea", C[3], 10, True, "ATPaz"),
      T(x0 + W0 - 92, y0 + 128, "Na⁺ dışarı", "end", 9.5), T(x0 + W0 - 92, y0 + 140, "→ su izler", "end", 9, 400, MUTED, True)]
g += [ok(x0 + 86, y0 + 39, x0 + W0 - 92, y0 + 125, C[0], "3 3")]
g += [T(x0 + W0 / 2, y0 + H0 + 20, "Net sonuç: Na⁺ ve su EMİLİR", fs=10.5, w=700, fill=C[3])]
# --- sag: kript hucresi ---
x1 = 420
g += hucre(x1, y0, W0, H0, "Kript: SALGI yapan hücre")
g += [T(x1 - 8, y0 + 16, "Lümen", "end", 10, 700, MUTED), T(x1 + W0 + 8, y0 + 16, "Kan", "start", 10, 700, MUTED)]
g += [kutu(x1 - 2, y0 + 40, 86, 28, "CFTR", "#f6e4ea", C[4], 10, True),
      T(x1 + 92, y0 + 48, "Cl⁻ lümene", "start", 9.5), T(x1 + 92, y0 + 60, "Na⁺ ve su peşinden", "start", 8.5, 400, MUTED, True)]
g += [kutu(x1 + 60, y0 + 108, 110, 30, "cAMP ↑ / cGMP ↑", "#f6e9df", C[1], 10, True, "Ca²⁺ ↑")]
g += [ok(x1 + 100, y0 + 106, x1 + 60, y0 + 70, C[1])]
g += [T(x1 + W0 / 2, y0 + H0 + 20, "Net sonuç: Cl⁻ ve su SALGILANIR", fs=10.5, w=700, fill=C[4])]
# toksin kutulari
g += [kutu(x1 + 36, y0 + 152, 158, 24, "Kolera toksini · ETEC LT → cAMP", "#fff", C[1], 9, False),
      kutu(x1 + 36, y0 + 180, 158, 22, "ETEC ST → cGMP", "#fff", C[1], 9, False)]
g += [T(360, 28, "İshalin iki kutbu: emilim mi azaldı, salgı mı arttı?", fs=13, w=700)]
yaz("enterosit", 720, 300, g, "Villus emici hucresi ve kript salgi hucresinde iyon tasinimi")

# 5) ishal mekanizmasi karar semasi
g = []
g += [T(350, 22, "İshalin mekanizmasına nasıl karar verilir?", fs=13, w=700)]
g += [kutu(250, 38, 200, 30, "Sulu ishali olan hasta", "#faf7f2", INK, 11, True)]
g += [ok(350, 68, 350, 88)]
g += [kutu(230, 88, 240, 30, "48 saat aç bırak (ya da oruç)", "#fff", INK, 10.5, False)]
g += [ok(300, 118, 170, 148), ok(400, 118, 540, 148)]
g += [kutu(60, 148, 220, 34, "İSHAL DURUR", "#e8f0f4", C[0], 11, True, "lümende emilmeyen yük vardı")]
g += [kutu(430, 148, 220, 34, "İSHAL SÜRER", "#f6e4ea", C[4], 11, True, "epitel aktif olarak salgılıyor")]
g += [ok(170, 182, 170, 206), ok(540, 182, 540, 206)]
g += [kutu(40, 206, 260, 58, "OZMOTİK İSHAL", "#e8f0f4", C[0], 11.5, True, "Ozmotik boşluk > 100 mOsm/kg", "laktaz eksikliği, Mg laksatif, sorbitol, rotavirüs")]
g += [kutu(410, 206, 260, 58, "SEKRETUVAR İSHAL", "#f6e4ea", C[4], 11.5, True, "Ozmotik boşluk < 50 mOsm/kg", "kolera, ETEC, VIP-oma, safra asidi")]
# formul kutusu
g += [kutu(170, 282, 370, 30, "Ozmotik boşluk = 290 − 2 × (dışkı Na⁺ + dışkı K⁺)", "#faf7f2", INK, 11, True)]
g += [T(355, 330, "Kanlı, ateşli, tenezmli ise bu akış işletilmez: inflamatuvar ishal düşünülür.", fs=10, w=400, fill=MUTED, it=True)]
yaz("ishal_karar", 710, 345, g, "Ozmotik ve sekretuvar ishal ayrimi karar semasi")
print("enterosit + karar semasi eklendi")

# 6) dehidratasyon tipleri: hucre ici-disi su hareketi
g = []
g += [T(360, 22, "Dehidratasyon tipleri: su nereye gider?", fs=13, w=700)]
basliklar = [("İzonatremik", "Na 130-150", "Su ve tuz eşit kaybedilir", 0, 0),
             ("Hiponatremik", "Na < 130", "Tuz daha çok kaybedildi", 1, 1),
             ("Hipernatremik", "Na > 150", "Su daha çok kaybedildi", 2, 2)]
for i, (ad, na, aciklama, ci, _) in enumerate(basliklar):
    x = 40 + i * 230
    g += [T(x + 95, 50, ad, fs=12, w=700, fill=C[ci]), T(x + 95, 64, na, fs=10, fill=MUTED)]
    # hucre disi kutu
    g += [f'<rect x="{x}" y="78" width="190" height="52" rx="4" fill="#f2ece4" stroke="{INK}"/>',
          T(x + 95, 98, "Hücre dışı (ECF)", fs=10, w=700), T(x + 95, 112, "damar + interstisyum", fs=9, fill=MUTED)]
    g += [f'<rect x="{x}" y="140" width="190" height="52" rx="4" fill="#e4eef2" stroke="{INK}"/>',
          T(x + 95, 160, "Hücre içi (ICF)", fs=10, w=700)]
    # oklar
    if i == 0:
        g += [T(x + 95, 176, "değişmez", fs=9.5, fill=MUTED, it=True)]
        kl = "ECF küçülür, ICF korunur"
    elif i == 1:
        g += [ok(x + 95, 150, x + 95, 128, C[1])]
        g += [T(x + 95, 176, "su ICF'ye kaçar", fs=9.5, fill=C[1], it=True)]
        kl = "ECF en çok küçülür → şok erken"
    else:
        g += [ok(x + 95, 126, x + 95, 148, C[2])]
        g += [T(x + 95, 176, "su ICF'den çıkar", fs=9.5, fill=C[2], it=True)]
        kl = "ECF korunur → bulgular geç, beyin büzüşür"
    g += [T(x + 95, 210, aciklama, fs=9.5), kutu(x, 220, 190, 34, kl, "#fff", C[ci], 9.5, False)]
g += [kutu(140, 268, 440, 30, "Hipernatremide sıvı YAVAŞ verilir (48 saat): hızlı düzeltme beyin ödemi yapar", "#faf7f2", C[4], 10, True)]
yaz("dehidratasyon_tip", 720, 310, g, "Izonatremik hiponatremik hipernatremik dehidratasyonda su hareketi")
print("dehidratasyon semasi eklendi")

# 7) epidemi egrileri: nokta kaynak / surekli kaynak / kisiden kisiye
g = []
g += [T(355, 20, "Salgın eğrisi salgının tipini söyler", fs=13, w=700)]
def egri_ciz(x0, y0, w, h, bars, ad, alt, ci):
    r = [T(x0 + w / 2, y0 - 26, ad, fs=11.5, w=700, fill=C[ci]),
         f'<line x1="{x0}" y1="{y0 + h}" x2="{x0 + w}" y2="{y0 + h}" stroke="{INK}"/>',
         f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0 + h}" stroke="{INK}"/>']
    bw = w / (len(bars) + 1)
    mx = max(bars) or 1
    for i, v in enumerate(bars):
        bh = v / mx * h
        if bh > 0:
            r.append(f'<rect x="{x0 + 3 + i * bw:.1f}" y="{y0 + h - bh:.1f}" width="{bw - 3:.1f}" height="{bh:.1f}" fill="{C[ci]}" opacity="0.82"/>')
    r += [T(x0 + w / 2, y0 + h + 16, "zaman →", fs=9, fill=MUTED),
          T(x0 - 6, y0 + h / 2, "olgu", "end", 9, 400, MUTED).replace("<text ", f'<text transform="rotate(-90 {x0 - 6} {y0 + h / 2})" '),
          T(x0 + w / 2, y0 + h + 36, alt, fs=9.5)]
    return r
g += egri_ciz(50, 70, 170, 95, [0, 1, 4, 9, 7, 3, 1, 0, 0, 0], "Nokta kaynak", "Tek seferlik ortak besin", 0)
g += egri_ciz(285, 70, 170, 95, [0, 2, 5, 7, 7, 7, 6, 7, 6, 2], "Sürekli ortak kaynak", "Kirli şebeke suyu", 1)
g += egri_ciz(520, 70, 170, 95, [1, 2, 0, 3, 5, 1, 6, 9, 2, 7], "Kişiden kişiye", "Ardışık kuluçka dalgaları", 2)
g += [kutu(40, 212, 200, 46, "Tek, keskin tepe", "#fff", C[0], 10, True, "Tümü aynı anda maruz kaldı;", "tepe-maruziyet farkı = kuluçka")]
g += [kutu(275, 212, 200, 46, "Yayvan plato", "#fff", C[1], 10, True, "Kaynak sürekli; su kesilince", "eğri birden düşer")]
g += [kutu(510, 212, 200, 46, "Giderek büyüyen dalgalar", "#fff", C[2], 10, True, "Her dalga bir kuluçka uzaklıkta;", "temas yoluyla büyür")]
g += [kutu(140, 272, 470, 26, "Su kaynaklı salgınlar patlayıcıdır: aynı anda çok kişiye ulaşır (nokta ya da sürekli kaynak)", "#faf7f2", INK, 10, False)]
yaz("epidemi_egri", 730, 310, g, "Nokta kaynak surekli kaynak ve kisiden kisiye salgin egrileri")
print("epidemi egrisi eklendi")

# 8) SCFA: uretim ve dort islevi
g = []
g += [T(350, 22, "Kısa zincirli yağ asitleri: lif nasıl sağlığa dönüşür?", fs=13, w=700)]
g += [kutu(20, 48, 150, 44, "Diyet lifi", "#e6f0ea", C[3], 11, True, "+ dirençli nişasta"),
      kutu(205, 48, 170, 44, "Kolon bakterileri", "#e6f0ea", C[3], 11, True, "Firmicutes (bütirat)"),
      kutu(410, 48, 270, 44, "Asetat · Propiyonat · BÜTİRAT", "#f6e9df", C[1], 11, True, "lümen asitleşir (pH ↓)")]
g += [ok(172, 70, 203, 70), ok(377, 70, 408, 70)]
# dort kol
kollar = [(20, "Kolonositin yakıtı", "bütirat enerjinin %70'i;", "mukus ve sıkı bağlantı ↑"),
          (185, "Bariyer güçlenir", "epitel yenilenir,", "geçirgenlik azalır"),
          (350, "Patojene kapalı kapı", "asidik ortam C. difficile,", "Salmonella, E. coli O157'yi engeller"),
          (515, "Bağışıklık dengesi", "düzenleyici T hücresi ↑,", "iltihap dizginlenir, tolerans sürer")]
for x, b, s1, s2 in kollar:
    g += [ok(545 if x == 515 else x + 82, 94, x + 82, 122, C[1], "3 3")]
    g += [kutu(x, 122, 165, 62, b, "#fff", C[0], 10.5, True, s1, s2)]
g += [kutu(120, 200, 460, 30, "Antibiyotik → flora bozulur → SCFA azalır → C. difficile çoğalır", "#f6e4ea", C[4], 10.5, True)]
yaz("scfa", 700, 245, g, "Kisa zincirli yag asitlerinin uretimi ve islevleri")
print("scfa semasi eklendi")
