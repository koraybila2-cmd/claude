# Modul 3 kitabinin semalarini uretir -> svg/*.svg   (python3 -I svg_uret.py)
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

# 1) belirtec zaman egrileri
def egri(t, t0, tp, t1, h):  # yukselis-inis
    if t <= t0 or t >= t1: return 0
    return h * (math.sin(math.pi / 2 * (t - t0) / (tp - t0)) if t < tp else (math.cos(math.pi / 2 * (t - tp) / (t1 - tp))) ** 1.5)
kn = [(0, 0), (6, 90), (12, 160), (24, 250), (48, 330), (72, 390), (168, 480), (336, 560)]  # saat -> x (parcali)
def X(t):
    for (a, xa), (b, xb) in zip(kn, kn[1:]):
        if t <= b: return 70 + xa + (xb - xa) * (t - a) / (b - a)
    return 70 + kn[-1][1]
g = [f'<line x1="70" y1="230" x2="640" y2="230" stroke="{INK}"/>', f'<line x1="70" y1="30" x2="70" y2="230" stroke="{INK}"/>',
     T(22, 130, "Kandaki düzey", fs=11) .replace("<text ", '<text transform="rotate(-90 22 130)" ')]
for t, ad in [(0, "0"), (6, "6 sa"), (12, "12 sa"), (24, "1 gün"), (48, "2 gün"), (72, "3 gün"), (168, "7 gün"), (336, "14 gün")]:
    g += [f'<line x1="{X(t)}" y1="230" x2="{X(t)}" y2="235" stroke="{INK}"/>', f'<line x1="{X(t)}" y1="30" x2="{X(t)}" y2="230" stroke="{GRID}" stroke-width="0.6"/>' if t else "", T(X(t), 249, ad, fs=10.5)]
g.append(T(355, 268, "Enfarktüsten sonra geçen süre", fs=11))
seri = [("Miyoglobin", 1, 7, 24, 120, C[1]), ("H-FABP", 1.5, 5, 20, 80, C[3]), ("CK-MB", 4, 20, 72, 150, C[2]), ("Troponin", 3.5, 26, 336, 185, C[0])]
ts = [x / 4 for x in range(0, 336 * 4 + 1)]
for ad, t0, tp, t1, h, renk in seri: g.append(yol([(X(t), 230 - egri(t, t0, tp, t1, h)) for t in ts if t0 <= t <= t1], renk))
g += [T(X(7) + 4, 230 - 126, "Miyoglobin", "start", 11, 700, C[1]), T(X(5) - 2, 230 - 84, "H-FABP", "end", 11, 700, C[3]), T(X(22), 230 - 155, "CK-MB", "end", 11, 700, C[2]), T(X(40), 230 - 188, "Troponin I ve T", "start", 11, 700, C[0]),
      T(X(250), 150, "troponin 7-14 gün yüksek kalır", fs=10, it=True), T(X(96), 222, "CK-MB 2-3 günde normale döner", "start", 10, 400, INK, True)]
yaz("belirtec_zaman", 680, 276, g, "Kardiyak belirteclerin zamana gore seyri")

# 2) aksiyon potansiyeli
g = []
ox, oy = 50, 40   # ventrikul
V = [(0, 170), (40, 170), (46, 30), (58, 48), (150, 62), (205, 170), (290, 170)]
g += [T(ox + 150, 22, "Ventrikül hücresi (hızlı yanıt)", fs=12, w=700), yol([(ox + x, oy + y) for x, y in V], INK, 2.4),
      f'<line x1="{ox}" y1="{oy+170}" x2="{ox+300}" y2="{oy+170}" stroke="{GRID}" stroke-dasharray="3 3"/>', T(ox - 6, oy + 174, "−90 mV", "end", 9.5), T(ox - 6, oy + 34, "+20", "end", 9.5)]
for (x, y, s, s2) in [(30, 105, "Faz 0", "Na⁺ girişi"), (72, 26, "Faz 1", ""), (118, 44, "Faz 2 (plato)", "Ca²⁺ girişi = K⁺ çıkışı"), (228, 110, "Faz 3", "K⁺ çıkışı"), (262, 160, "Faz 4", "")]:
    g += [T(ox + x, oy + y, s, "start" if x > 60 else "end", 10.5, 700), T(ox + x, oy + y + 12, s2, "start" if x > 60 else "end", 9.5)]
g += [T(ox + 28, oy + 140, "Sınıf I", "end", 10.5, 700, C[4]), T(ox + 28, oy + 152, "(Na⁺ blokeri)", "end", 9.5, 400, C[4]),
      T(ox + 232, oy + 78, "Sınıf III", "start", 10.5, 700, C[4]), T(ox + 232, oy + 90, "(K⁺ blokeri; QT uzar)", "start", 9.5, 400, C[4])]
ox2 = 420
S = [(0, 150), (55, 118), (75, 40), (120, 150), (175, 118), (195, 40), (240, 150)]
g += [T(ox2 + 120, 22, "Sinüs düğümü hücresi (yavaş yanıt)", fs=12, w=700), yol([(ox2 + x, oy + y) for x, y in S], INK, 2.4),
      yol([(ox2 + 0, oy + 150), (ox2 + 95, oy + 118)], C[0], 1.6, "4 3"), T(ox2 - 4, oy + 154, "−60", "end", 9.5),
      T(ox2 + 30, oy + 162, "Faz 4: kendiliğinden", "middle", 10, 700), T(ox2 + 30, oy + 174, "depolarizasyon (I<tspan baseline-shift=\"sub\" font-size=\"7\">f</tspan>)", "middle", 9.5),
      T(ox2 + 60, oy + 72, "Faz 0:", "end", 10, 700), T(ox2 + 60, oy + 84, "Ca²⁺ girişi", "end", 9.5), T(ox2 + 104, oy + 70, "Faz 3: K⁺", "start", 10, 700),
      T(ox2 + 110, oy + 186, "Sınıf II (β bloker), ivabradin: eğimi yatırır, hız ↓", "middle", 10, 700, C[4]),
      T(ox2 + 110, oy + 200, "Sınıf IV (verapamil, diltiazem), adenozin: AV iletim ↓", "middle", 10, 700, C[4]),
      T(ox2 + 60, oy + 138, "eğim yatarsa", "start", 9, 400, C[0], True), T(ox2 + 60, oy + 148, "hız düşer", "start", 9, 400, C[0], True)]
yaz("aksiyon_potansiyeli", 720, 250, g, "Ventrikul ve sinus dugumu aksiyon potansiyelleri ve antiaritmik siniflar")

# 3) insulin profilleri
def XI(t): return 60 + t * 23.5
g = [f'<line x1="60" y1="200" x2="640" y2="200" stroke="{INK}"/>', f'<line x1="60" y1="24" x2="60" y2="200" stroke="{INK}"/>', T(20, 112, "İnsülin etkisi", fs=11).replace("<text ", '<text transform="rotate(-90 20 112)" ')]
for t in range(0, 25, 2): g += [f'<line x1="{XI(t)}" y1="200" x2="{XI(t)}" y2="204" stroke="{INK}"/>', T(XI(t), 217, str(t), fs=10)]
g.append(T(350, 236, "Enjeksiyondan sonra geçen süre (saat)", fs=11))
ts = [x / 10 for x in range(0, 241)]
for ad, t0, tp, t1, h, renk in [("h", 0.2, 1.3, 4.5, 165, C[1]), ("r", 0.6, 3, 8, 130, C[2]), ("n", 1.5, 6, 16, 95, C[3])]:
    g.append(yol([(XI(t), 200 - egri(t, t0, tp, t1, h)) for t in ts if t0 <= t <= t1], renk))
g.append(yol([(XI(t), 200 - 42 * min(1, max(0, (t - 1) / 2.5))) for t in ts if t >= 1], C[0]))
g += [T(XI(1.9), 34, "Hızlı etkili analog", "start", 11, 700, C[1]), T(XI(1.9), 46, "(aspart, lispro, glulisin)", "start", 9.5, 400, C[1]),
      T(XI(4.4), 80, "Regüler (kristalize)", "start", 11, 700, C[2]), T(XI(8.2), 112, "NPH (izofan): tepe yapar", "start", 11, 700, C[3]),
      T(XI(18), 138, "Uzun etkili analog: tepe yok", "middle", 11, 700, C[0]), T(XI(18), 150, "(glarjin, detemir, degludek)", "middle", 9.5, 400, C[0])]
yaz("insulin_profil", 680, 244, g, "Insulin preparatlarinin etki profilleri")

# 4) pihtilasma ve ilaclar
M = 330
g = [T(M - 130, 20, "İç yol (aPTT)", fs=11, w=700), T(M - 130, 38, "XII → XI → IX (+VIIIa)", fs=11), T(M + 130, 20, "Dış yol (PT)", fs=11, w=700), T(M + 130, 38, "Doku faktörü + VIIa", fs=11),
     ok(M - 110, 46, M - 40, 84), ok(M + 110, 46, M + 40, 84), kutu(M - 60, 88, 120, 34, "Faktör Xa", "#eef6f9", "#0088b0", 12, True, "(+ Va)"), ok(M, 122, M, 152),
     kutu(M - 60, 156, 120, 34, "Trombin (IIa)", "#eef6f9", "#0088b0", 12, True), ok(M, 190, M, 220), kutu(M - 75, 224, 150, 30, "Fibrinojen → Fibrin", "#f7f4f2", "#57534e", 11.5, True),
     kutu(M + 130, 288, 140, 28, "Plazminojen → Plazmin", "#f7f4f2", "#57534e", 10.5), ok(M + 130, 300, M + 40, 260), T(M + 62, 296, "fibrini eritir", "middle", 9.5, 400, INK, True)]
R_ = C[4]
g += [T(12, 100, "Heparin (antitrombin ile):", "start", 10.5, 700, R_), T(12, 113, "Xa ve IIa", "start", 10.5, 700, R_),
      f'<path d="M{M-66},105 H{M-90} V173 H{M-66}" fill="none" stroke="{R_}" stroke-width="1.2"/>', f'<line x1="{M-90}" y1="105" x2="{M-150}" y2="105" stroke="{R_}" stroke-width="1.2"/>',
      T(12, 136, "DMAH (enoksaparin): Xa &gt; IIa", "start", 10.5, 700, R_), T(12, 156, "Fondaparinuks: yalnız Xa", "start", 10.5, 700, R_),
      T(M + 72, 100, "Rivaroksaban, apiksaban, edoksaban:", "start", 10.5, 700, R_), T(M + 72, 113, "Xa (doğrudan, ağızdan)", "start", 10.5, 700, R_),
      T(M + 72, 170, "Dabigatran (ağızdan), bivalirudin,", "start", 10.5, 700, R_), T(M + 72, 183, "argatroban: IIa (doğrudan)", "start", 10.5, 700, R_),
      T(12, 204, "Varfarin: karaciğerde II, VII, IX, X", "start", 10.5, 700, R_), T(12, 217, "(ve protein C, S) yapımı ↓", "start", 10.5, 700, R_),
      T(M + 280, 298, "Streptokinaz, alteplaz,", "start", 10.5, 700, R_), T(M + 280, 311, "tenekteplaz: etkinleştirir", "start", 10.5, 700, R_),
      T(12, 300, "Trombosit tıkacı: aspirin (TXA2), klopidogrel-tikagrelor (P2Y12),", "start", 10, 400, INK), T(12, 313, "absiksimab-tirofiban (GP IIb/IIIa)", "start", 10, 400, INK)]
yaz("pihtilasma_ilac", 760, 326, g, "Pihtilasma kaskadi ve antikoagulan ilaclarin hedefleri")

# 5) MI zaman cizelgesi
et = ["0", "30 dk", "4 saat", "12 saat", "1 gün", "3 gün", "7 gün", "10 gün", "2 hafta", "2 ay"]
def XM(i): return 150 + i * 56
g = [T(XM(i), 20, s, fs=10.5, w=700) + f'<line x1="{XM(i)}" y1="26" x2="{XM(i)}" y2="272" stroke="{GRID}" stroke-width="0.7"/>' for i, s in enumerate(et)]
def bar(y, a, b, s, renk, not_=""):
    return f'<rect x="{XM(a)}" y="{y}" width="{XM(b)-XM(a)}" height="16" rx="3" fill="{renk}" opacity="0.85"/>' + T(142, y + 12, s, "end", 10.5, 700) + (T(XM(b) + 5, y + 12, not_, "start", 9.5, 400, INK, True) if not_ else "")
g += [bar(36, 0, 1, "Geri dönüşümlü hasar", "#9aa3ab"), bar(58, 2, 5, "Koagülasyon nekrozu", C[2]), bar(80, 3, 6, "Nötrofil", C[1], "en yoğun 1-3. gün; 10. günden sonra yok"), bar(102, 5, 7, "Makrofaj", C[3], "ölü dokuyu temizler"),
      bar(124, 6, 8.4, "Granülasyon dokusu", C[0]), bar(146, 8, 9, "Skar", "#57534e", "2 ayda tamamlanır"),
      f'<line x1="20" y1="174" x2="690" y2="174" stroke="{INK}" stroke-width="0.6"/>', T(20, 190, "Komplikasyonlar", "start", 10.5, 700, C[4]),
      bar(198, 0, 4.5, "Aritmi (VF)", "#c98a96"), bar(220, 4, 5, "Perikardit", "#c98a96"), bar(242, 5, 6, "RÜPTÜR (3-7. gün)", C[4], "duvarın en yumuşak dönemi"), bar(264, 6.4, 9, "Mural trombüs, anevrizma", "#c98a96")]
yaz("mi_zaman", 760, 290, g, "Miyokard enfarktusu sonrasi morfolojik degisikliklerin zaman cizelgesi")
print("5 svg yazildi")
