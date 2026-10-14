import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "build"))
from svglib import SVG, NEU, TXT, CYAN, MAG

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "svg")


def save(s, name):
    s.save(os.path.join(OUT, name + ".svg"))


def blockbar(s, x, y, length=22):
    s.add(f'<line x1="{x - length / 2}" y1="{y}" x2="{x + length / 2}" y2="{y}" stroke="{MAG}" stroke-width="3"/>')


# =============================================================== 3.1 hava yolunda muskarinik reseptorler
s = SVG(640, 452, "Hava yolunda parasempatik yol, M1 M2 M3 reseptorleri ve ipratropium ile tiotropiumun farki", "m44e")
s.box(10, 10, 180, 46, [("Vagus siniri", "title"), ("preganglionik lif", "sub")], fs1=11.8, fs2=10, lh=14)
s.box(225, 10, 190, 46, [("Parasempatik ganglion", "title"), ("M₁: iletimi kolaylaştırır", "sub")], fs1=11.8, fs2=10, lh=14)
s.box(450, 10, 170, 46, [("Postganglionik sinir ucu", "title"), ("asetilkolin salınır", "sub")], fs1=11.8, fs2=10, lh=14)
s.arrow(190, 33, 223, 33)
s.arrow(415, 33, 448, 33)
# dagitim
s.add(f'<line x1="535" y1="56" x2="535" y2="82" stroke="{NEU}" stroke-width="1.5"/>')
s.arrow(535, 82, 535, 106)
s.path("M535,82 L320,82 L320,106")
s.path("M320,82 L100,82 L100,106", marker=False)
s.arrow(100, 82, 100, 106)
s.text(545, 75, "ACh", "title", fs1=10.5)
blockbar(s, 320, 95)
blockbar(s, 100, 95)
s.text(338, 99, "M₃ blokajı", "magb", fs2=9.8)
s.text(118, 99, "M₃ blokajı", "magb", fs2=9.8)
s.box(10, 108, 180, 58, [("M₃ · submukozal bez", "title"), ("mukus salgısı ↑", "sub")], kind="mag", fs1=11.6, fs2=10, lh=15)
s.box(225, 108, 190, 58, [("M₃ · bronş düz kası", "title"), ("Gq → IP₃ → Ca²⁺ ↑", "sub"), ("bronkokonstriksiyon", "sub")], kind="mag", fs1=11.6, fs2=10, lh=14)
s.box(450, 108, 170, 58, [("M₂ · sinir ucunda", "title"), ("ACh salınımını frenler", "sub"), ("(negatif geri bildirim)", "sub")], kind="key", fs1=11.6, fs2=10, lh=14)
# M2 geri bildirim: sinir ucuna fren
s.add(f'<path d="M620,137 L632,137 L632,33 L624,33" fill="none" stroke="{CYAN}" stroke-width="1.4" stroke-dasharray="4 3"/>')
s.add(f'<line x1="623" y1="24" x2="623" y2="42" stroke="{CYAN}" stroke-width="2.6"/>')
# ilac kutulari
s.box(10, 190, 300, 104, [("İpratropium · kısa etkili (4-8 saat)", "magb"),
                          ("M₁, M₂ ve M₃'ü ayırt etmeden bloke eder.", "body"),
                          ("M₂ blokajı sinir ucundaki freni kaldırır:", "body"),
                          ("daha çok ACh salınır ve M₃ blokajının", "body"),
                          ("bir kısmı boşa gider.", "body")],
      kind="mag", align="start", fs1=11.6, fs2=10.4, lh=16, pad_top=22)
s.box(330, 190, 300, 104, [("Tiotropium · uzun etkili (≥ 24 saat)", "magb"),
                           ("M₂'den hızlı, M₃ ve M₁'den çok yavaş ayrılır.", "body"),
                           ("M₂ freni kısa sürede yeniden çalışır,", "body"),
                           ("M₃ blokajı ise bir günden uzun sürer:", "body"),
                           ("kinetik seçicilik", "magb")],
      kind="mag", align="start", fs1=11.6, fs2=10.4, lh=16, pad_top=22)
# cubuk grafik: tiotropium ayrilma yari omru
s.text(10, 324, "Tiotropiumun reseptörden ayrılma yarı ömrü (saat)", "title", fs1=11.5)
L, R = 60, 560
X = lambda h: L + (R - L) * h / 36
top = 336
for h in (0, 12, 24, 36):
    s.add(f'<line x1="{X(h):.1f}" y1="{top - 2}" x2="{X(h):.1f}" y2="{top + 3 * 26 - 4}" stroke="{NEU}" stroke-opacity="0.18"/>')
    s.text(X(h), top + 3 * 26 + 10, f"{h}", "small", anchor="middle")
rows = [("M₃", 34.7, "≈ 35 saat"), ("M₁", 14.6, "≈ 15 saat"), ("M₂", 3.6, "≈ 3,6 saat")]
for i, (lab, v, t) in enumerate(rows):
    y = top + i * 26
    s.text(L - 10, y + 13, lab, "title", anchor="end", fs1=11.5)
    s.add(f'<rect x="{L}" y="{y}" width="{X(v) - L:.1f}" height="18" rx="4" fill="{MAG}"/>')
    s.text(X(v) + 6, y + 13, t, "title", fs1=10.5)
s.text(10, 446, "İpratropium üç reseptörden de 20 dakikadan kısa sürede ayrılır. Değerler insan reseptörleriyle yapılan bağlanma çalışmalarından yuvarlanmıştır.", "small")
save(s, "m4k4_musk")

# =============================================================== 4.1 glukokortikoidlerin genomik mekanizmasi
s = SVG(640, 436, "Glukokortikoidlerin genomik etki mekanizmasi: transaktivasyon ve transrepresyon", "m44f")
s.add(f'<rect x="4" y="40" width="632" height="392" rx="12" fill="{CYAN}" fill-opacity="0.03" stroke="{NEU}" stroke-opacity="0.35" stroke-width="1.2"/>')
s.text(110, 14, "Kortikosteroid", "cyanb", anchor="middle", fs2=11)
s.text(124, 34, "lipofilik, hücre zarından geçer", "small")
s.arrow(110, 20, 110, 70, CYAN)
s.text(620, 58, "sitoplazma", "small", anchor="end")
s.box(30, 72, 180, 46, [("Glukokortikoid reseptörü", "title"), ("HSP90'a bağlı, inaktif", "sub")], fs1=11.6, fs2=10, lh=14)
s.arrow(210, 95, 248, 95)
s.box(250, 72, 180, 46, [("Steroid-GR kompleksi", "title"), ("HSP90 ayrılır", "sub")], kind="key", fs1=11.6, fs2=10, lh=14)
s.add(f'<rect x="20" y="146" width="600" height="196" rx="14" fill="white" fill-opacity="0.6" stroke="{NEU}" stroke-opacity="0.5" stroke-dasharray="5 4"/>')
s.text(34, 162, "çekirdek", "small")
s.add(f'<line x1="340" y1="118" x2="340" y2="160" stroke="{NEU}" stroke-width="1.5"/>')
s.path("M340,160 L175,160 L175,172")
s.path("M340,160 L475,160 L475,172")
s.box(45, 174, 260, 42, [("Transaktivasyon", "title"), ("GR dimeri DNA'daki GRE dizisine bağlanır", "sub")], kind="key", fs1=11.6, fs2=10, lh=14)
s.box(345, 174, 260, 42, [("Transrepresyon", "title"), ("GR, NF-κB ve AP-1'e bağlanır", "sub")], kind="mag", fs1=11.6, fs2=10, lh=14)
s.arrow(175, 216, 175, 230, CYAN)
s.arrow(475, 216, 475, 230, MAG)
s.box(45, 232, 260, 98, [("Antiinflamatuvar genler açılır", "cyanb"),
                         ("· Lipokortin-1 ↑ → fosfolipaz A₂ ↓", "body"),
                         ("· β₂ reseptör geni ↑", "body"),
                         ("· IκBα ↑ → NF-κB sitoplazmada kalır", "body")],
      kind="key", align="start", fs1=11.6, fs2=10.4, lh=17, pad_top=22)
s.box(345, 232, 260, 98, [("HDAC2 çağrılır (HAT ↓, HDAC2 ↑)", "magb"),
                          ("Histonlar deasetillenir, kromatin kapanır:", "body"),
                          ("IL-4, IL-5, IL-13, GM-CSF, COX-2", "body"),
                          ("ve kemokin genleri susturulur", "body")],
      kind="mag", align="start", fs1=11.6, fs2=10.4, lh=17, pad_top=22)
s.arrow(175, 330, 175, 358, CYAN)
s.arrow(475, 330, 475, 358, MAG)
s.box(30, 360, 580, 64, [("Sonuç (etki saatler içinde ortaya çıkar)", "title"),
                         ("inflamatuvar hücreler ve mediatörler ↓ · mukoza ödemi ↓ · aşırı duyarlılık ↓", "sub"),
                         ("β₂ reseptör sayısı ↑ · bronş düz kasına doğrudan gevşetici etkisi yok", "sub")],
      kind="key", fs1=11.8, fs2=10.4, lh=16)
save(s, "m4k4_gr")

# =============================================================== 5.2 tip 2 inflamasyon ve biyolojik ilaclar
s = SVG(640, 376, "Tip 2 inflamasyon zinciri ve astimda kullanilan monoklonal antikorlarin hedefleri", "m44g")
s.box(10, 6, 190, 46, [("Alerjen, virüs, duman", "title"), ("epiteli uyarır", "sub")], fs1=11.6, fs2=10, lh=14)
s.arrow(200, 29, 223, 29)
s.box(225, 6, 190, 46, [("Hava yolu epiteli", "title"), ("TSLP, IL-33, IL-25 salar", "sub")], fs1=11.6, fs2=10, lh=14)
s.text(630, 22, "magenta çubuk: antikorun", "small", anchor="end")
s.text(630, 35, "engellediği basamak", "small", anchor="end")
s.arrow(320, 52, 320, 82)
blockbar(s, 320, 66)
s.text(334, 70, "tezepelumab (anti-TSLP)", "magb", fs2=9.8)
s.box(225, 84, 190, 44, [("Th2 hücresi, ILC2", "title"), ("tip 2 sitokinler", "sub")], kind="key", fs1=11.6, fs2=10, lh=14)
# sol kol: IL-4/IL-13 -> IgE -> mast
s.path("M225,106 L105,106 L105,148")
s.text(165, 100, "IL-4, IL-13", "title", anchor="middle", fs1=10.5)
blockbar(s, 105, 126)
s.text(119, 124, "dupilumab", "magb", fs2=9.8)
s.text(119, 136, "(IL-4Rα)", "mag", fs2=9.6)
s.box(10, 150, 190, 44, [("B hücresi", "title"), ("IgE'ye sınıf değişimi", "sub")], fs1=11.6, fs2=10, lh=14)
s.arrow(105, 194, 105, 238)
blockbar(s, 105, 214)
s.text(119, 212, "omalizumab", "magb", fs2=9.8)
s.text(119, 224, "(serbest IgE)", "mag", fs2=9.6)
s.box(10, 240, 190, 44, [("Mast hücresi", "title"), ("IgE, FcεRI'ye bağlanır", "sub")], fs1=11.6, fs2=10, lh=14)
s.arrow(105, 284, 105, 306)
s.box(10, 308, 190, 60, [("Alerjen IgE'yi çapraz bağlar", "title"), ("histamin, LTC₄, PGD₂ salınır", "sub"), ("erken faz bronkospazm", "sub")], kind="mag", fs1=11.2, fs2=10, lh=14)
# orta: IL-13 etkileri + ortak ozellikler
s.arrow(320, 128, 320, 148)
s.text(330, 142, "IL-13", "title", fs1=10.5)
s.box(225, 150, 190, 58, [("Epitel, bez, düz kas", "title"), ("mukus ↑, aşırı duyarlılık ↑", "sub"), ("FeNO ↑", "sub")], kind="mag", fs1=11.4, fs2=10, lh=14)
s.box(225, 240, 190, 128, [("Ortak özellikler", "cyanb"),
                           ("· ağır, tip 2 astımda", "body"),
                           ("· alevlenme ve oral", "body"),
                           ("  steroid ihtiyacı ↓", "body"),
                           ("· protein: oral formu yok", "body"),
                           ("· deri altı (reslizumab IV)", "body")],
      kind="key", align="start", fs1=11.4, fs2=10.2, lh=17, pad_top=22)
# sag kol: IL-5 -> eozinofil
s.path("M415,106 L535,106 L535,148")
s.text(475, 100, "IL-5", "title", anchor="middle", fs1=10.5)
blockbar(s, 535, 126)
s.text(518, 124, "mepolizumab (SC)", "magb", anchor="end", fs2=9.8)
s.text(518, 136, "reslizumab (IV)", "magb", anchor="end", fs2=9.8)
s.box(440, 150, 190, 44, [("IL-5 reseptörü (IL-5Rα)", "title"), ("eozinofil yüzeyinde", "sub")], fs1=11.4, fs2=10, lh=14)
s.arrow(535, 194, 535, 238)
blockbar(s, 535, 214)
s.text(518, 212, "benralizumab (SC)", "magb", anchor="end", fs2=9.8)
s.text(518, 224, "(IL-5Rα)", "mag", anchor="end", fs2=9.6)
s.box(440, 240, 190, 58, [("Eozinofil", "title"), ("yapım, olgunlaşma, göç,", "sub"), ("aktivasyon, yaşam süresi ↑", "sub")], fs1=11.6, fs2=10, lh=14)
s.arrow(535, 298, 535, 320)
s.box(440, 322, 190, 46, [("Geç faz inflamasyon", "title"), ("epitel hasarı, alevlenme", "sub")], kind="mag", fs1=11.4, fs2=10, lh=14)
save(s, "m4k4_bio")
print("ok")
