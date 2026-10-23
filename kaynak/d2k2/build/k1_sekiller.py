"""Kitap 1 (D2K2 dolaşım anatomisi) mekanizma şemaları -> kitaplar/k1/svg/*.svg"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from svglib import SVG, NEU, CYAN, MAG  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "kitaplar", "k1", "svg")
os.makedirs(OUT, exist_ok=True)


def both(s, x1, y1, x2, y2, color=NEU):
    """iki uclu ok (kapaksiz venlerde iki yonlu akim)"""
    m = s.mid + {CYAN: "c", MAG: "m"}.get(color, "")
    s.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.5" '
          f'marker-start="url(#{m})" marker-end="url(#{m})"/>')


# 1. Büyük ve küçük dolaşım
s = SVG(640, 345, "Büyük ve küçük dolaşımın şeması", "dl")
s.box(220, 12, 200, 48, ["Akciğer kapillerleri", "gaz alışverişi: kan oksijenlenir"], kind="key")
s.box(150, 110, 140, 46, ["Sağ ventrikül", "venöz kan"])
s.box(350, 110, 140, 46, ["Sol atriyum", "arteriyel kan"])
s.box(150, 196, 140, 46, ["Sağ atriyum", "venöz kan"])
s.box(350, 196, 140, 46, ["Sol ventrikül", "arteriyel kan"])
s.box(220, 288, 200, 48, ["Vücut kapillerleri", "O₂ verilir, CO₂ alınır"])
s.arrow(250, 109, 250, 62)
s.text(244, 92, "Truncus pulmonalis", "body", "end")
s.arrow(390, 61, 390, 108)
s.text(396, 92, "Vv. pulmonales (4)", "body", "start")
s.arrow(205, 195, 205, 158)
s.text(199, 181, "Triküspit kapak", "body", "end")
s.arrow(435, 157, 435, 194)
s.text(441, 181, "Mitral kapak", "body", "start")
s.arrow(390, 243, 390, 286)
s.text(396, 270, "Aorta", "body", "start")
s.arrow(250, 287, 250, 244)
s.text(244, 270, "VCS ve VCİ", "body", "end")
s.text(20, 36, "KÜÇÜK (PULMONER) DOLAŞIM", "cap")
s.text(20, 50, "sağ ventrikül → akciğer → sol atriyum", "small")
s.text(20, 316, "BÜYÜK (SİSTEMİK) DOLAŞIM", "cap")
s.text(20, 330, "sol ventrikül → doku → sağ atriyum", "small")
s.text(620, 140, "SOL KALP", "cap", "end")
s.text(620, 226, "basınçlı pompa", "small", "end")
s.text(20, 140, "SAĞ KALP", "cap")
s.text(20, 226, "düşük basınçlı pompa", "small")
s.save(os.path.join(OUT, "k1_dolasim.svg"))

# 2. Lenf kanallarının venöz açılara dökülmesi
s = SVG(640, 380, "Lenf trunkuslarının ductus thoracicus ve ductus lymphaticus dexter aracılığıyla venöz açılara dökülmesi", "lf")
s.text(125, 14, "SAĞ ÜST ÇEYREK", "cap", "middle")
s.text(430, 14, "VÜCUDUN GERİ KALANI", "cap", "middle")
s.box(20, 24, 210, 50, ["Sağ angulus venosus", "v. jugularis interna + v. subclavia dx."], kind="key")
s.box(20, 112, 210, 50, ["Ductus lymphaticus dexter", "≈1 cm, kısa ve kalın"])
s.box(20, 200, 210, 70, [("Truncus jugularis dexter", "plain"), ("Truncus subclavius dexter", "plain"), ("Truncus bronchomediastinalis dx.", "plain")], fs1=12)
s.arrow(125, 199, 125, 165)
s.arrow(125, 111, 125, 77)
s.box(20, 300, 210, 70, [("Drene ettiği bölge:", "title"), "başın ve boynun sağ yarısı,", "sağ üst ekstremite,", "toraksın sağ yarısı"], fs1=11.5, lh=14)
s.box(300, 24, 220, 50, ["Sol angulus venosus", "v. jugularis interna + v. subclavia sin."], kind="key")
s.box(300, 104, 220, 82, ["Ductus thoracicus", "≈40 cm · hiatus aorticus (T12)", "mediastinum posterius'ta yükselir", "T4-T5'te sağdan sola geçer", "C7 düzeyinde kavis yapar"], lh=14)
s.box(300, 222, 220, 46, ["Cisterna chyli", "L1-L2 önünde, aortanın sağında"])
s.box(300, 302, 220, 56, ["Truncus lumbalis dexter", "truncus lumbalis sinister", "truncus intestinalis (şilus)"], lh=14)
s.arrow(410, 301, 410, 271)
s.arrow(410, 221, 410, 189)
s.arrow(410, 103, 410, 77)
s.box(540, 104, 92, 82, [("Sol", "plain"), ("jugularis,", "body"), ("subclavius,", "body"), ("broncho-", "body"), ("mediastinalis", "body")], fs1=12, lh=13)
s.arrow(539, 130, 523, 130)
s.save(os.path.join(OUT, "k1_lenf.svg"))

# 3. Koroner arter ağacı
s = SVG(640, 400, "Koroner arterlerin dallanma şeması ve besleme alanları", "kr")
s.box(220, 10, 200, 46, ["Aorta ascendens", "bulbus aortae · sinus aortae"])
s.box(20, 92, 240, 46, ["A. coronaria dextra (RCA)", "sağ (ön) sinüsten çıkar"])
s.box(380, 92, 240, 46, ["A. coronaria sinistra (LMCA)", "sol (sol arka) sinüsten · 1-2 cm"])
s.arrow(270, 56, 180, 90)
s.arrow(370, 56, 460, 90)
s.box(330, 172, 140, 46, ["R. interventric.", "anterior (LAD)"], kind="key")
s.box(490, 172, 140, 46, ["R. circumflexus", "(LCx)"])
s.arrow(470, 139, 400, 170)
s.arrow(530, 139, 560, 170)
s.box(20, 172, 240, 218, [("Dalları", "cap"), ("R. coni arteriosi", "body"), ("R. nodi sinuatrialis (≈%60)", "body"), ("Rr. atriales · r. atrialis intermedius", "body"), ("R. marginalis dexter (akut marjinal)", "body"), ("R. nodi atrioventricularis (≈%80)", "body"), ("R. interventricularis posterior (PDA)", "body"), ("Rr. posterolaterales dextri", "body"), ("Beslediği alan", "cap"), ("sağ atriyum, sağ ventrikül,", "body"), ("septumun arka 1/3'ü, SA ve AV düğüm,", "body"), ("sol ventrikülün diyafragmatik yüzü", "body")], align="start", pad_top=20, lh=16.5)
s.arrow(140, 139, 140, 170)
s.box(330, 250, 140, 140, [("Dalları", "cap"), ("R. coni arteriosi", "body"), ("Rr. laterales", "body"), ("(diyagonal)", "body"), ("Rr. septales", "body"), ("Beslediği alan", "cap"), ("sol ventrikül ön", "body"), ("duvarı, apeks,", "body"), ("septumun ön 2/3'ü", "body")], align="start", pad_top=18, lh=14.5)
s.arrow(400, 219, 400, 248)
s.box(490, 250, 140, 140, [("Dalları", "cap"), ("R. marginalis sin.", "body"), ("R. posterior ventr. sin.", "body"), ("Rr. atriales", "body"), ("R. nodi SA (≈%40)", "body"), ("R. nodi AV (≈%20)", "body"), ("Beslediği alan", "cap"), ("sol atriyum,", "body"), ("kalbin sol kenarı", "body")], align="start", pad_top=18, lh=14.5)
s.arrow(560, 219, 560, 248)
s.save(os.path.join(OUT, "k1_koroner.svg"))

# 4. Kalbin venleri
s = SVG(640, 300, "Kalbin venlerinin sinus coronarius'a ve doğrudan kalp boşluklarına dökülmesi", "kv")
cols = [("V. cordis parva", "sulcus coronarius sağ", "sağ kenar boyunca"),
        ("V. cordis media", "sulcus IV posterior", "PDA'ya eşlik eder"),
        ("V. post. ventr. sin.", "sol ventrikül", "arka yüzü"),
        ("V. obliqua atrii sin.", "sol atriyum arka", "duvarı (Marshall)"),
        ("V. cordis magna", "sulcus IV anterior +", "sulcus coronarius sol")]
for i, (a, b, c) in enumerate(cols):
    x = 8 + i * 126
    s.box(x, 12, 120, 62, [a, b, c], fs1=12, lh=15)
    s.arrow(x + 60, 75, x + 60, 106)
s.box(8, 108, 624, 44, ["Sinus coronarius", "sulcus coronarius'un arka kısmında, 2-3 cm · kalbin venöz kanının çoğunu toplar"], kind="key")
s.text(14, 168, "← sağ uç", "small")
s.text(626, 168, "sol uç →", "small", "end")
s.arrow(150, 153, 150, 214)
s.box(8, 216, 300, 72, ["Sağ atriyum", "ostium sinus coronarii", "(VCİ ağzı ile triküspit ağzı arasında)", "valvula sinus coronarii (Thebesius)"], lh=14.5)
s.box(340, 186, 292, 46, ["Vv. cardiacae anteriores", "sağ ventrikül ön yüzü → doğrudan sağ atriyuma"])
s.box(340, 244, 292, 46, ["Vv. cardiacae minimae (Thebesius)", "endokard altı → tüm boşluklar, en çok sağ atriyum"])
s.arrow(339, 209, 311, 236)
s.arrow(339, 267, 311, 260)
s.save(os.path.join(OUT, "k1_venler.svg"))

# 5. İleti sistemi
s = SVG(640, 470, "Kalbin ileti sisteminde uyarının yolu, yerleşim yerleri ve gecikme", "il")
s.box(170, 10, 300, 52, ["Nodus sinuatrialis (Keith-Flack)", "crista terminalis'in üst ucu, VCS ağzı · 60-100/dk"], kind="key")
s.box(170, 92, 300, 52, ["İnternodal yollar (ön, orta, arka)", "+ Bachmann demeti → sol atriyum"])
s.box(170, 174, 300, 52, ["Nodus atrioventricularis (Aschoff-Tawara)", "Koch üçgeninin tepesi · iletim yavaşlar"])
s.box(170, 256, 300, 52, ["Fasciculus atrioventricularis (His)", "corpus fibrosum centrale'yi deler"])
s.box(20, 340, 270, 52, ["Crus dextrum", "trabecula septomarginalis → ön papiller kas"])
s.box(350, 340, 270, 52, ["Crus sinistrum", "ön ve arka fasikül · septumun sol yüzü"])
s.box(170, 412, 300, 50, ["Purkinje lifleri → ventrikül kası", "subendokardiyal · önce papiller kaslar ve apeks"])
for y1, y2 in ((63, 90), (145, 172), (227, 254)):
    s.arrow(320, y1, 320, y2)
s.arrow(280, 309, 190, 338)
s.arrow(360, 309, 450, 338)
s.arrow(155, 393, 230, 410)
s.arrow(485, 393, 410, 410)
s.text(482, 30, "0 sn", "cyanb")
s.text(482, 196, "≈0,03 sn: AV düğüme ulaşır", "body")
s.text(482, 210, "+≈0,09 sn gecikme", "body")
s.text(482, 276, "≈0,13 sn", "body")
s.text(482, 290, "kendi hızı 40-60/dk", "small")
s.text(482, 432, "≈0,16 sn: ventriküller", "body")
s.text(482, 446, "kendi hızı 15-40/dk", "small")
s.text(158, 114, "Atriyum kası", "small", "end")
s.text(158, 128, "kasılır", "small", "end")
s.text(158, 196, "Gecikme sayesinde", "small", "end")
s.text(158, 210, "ventrikül dolumu", "small", "end")
s.text(158, 224, "tamamlanır", "small", "end")
s.save(os.path.join(OUT, "k1_ileti.svg"))

# 6. Kalbin sinirleri
s = SVG(640, 400, "Kalbin sempatik ve parasempatik innervasyonu ile ağrı liflerinin yolu", "sn")
s.text(150, 14, "SEMPATİK", "cap", "middle")
s.text(490, 14, "PARASEMPATİK", "cap", "middle")
s.box(20, 24, 260, 52, ["Medulla spinalis T1-T4 (T5)", "cornu laterale · preganglionik nöron"])
s.box(20, 102, 260, 66, ["Truncus sympathicus", "ggl. cervicale superius, medium,", "ggl. cervicothoracicum (stellatum), T1-T4"], lh=14.5)
s.box(20, 194, 260, 52, ["Nn. cardiaci cervicales", "+ rr. cardiaci thoracici (postganglionik)"])
s.box(360, 24, 260, 52, ["Nucleus dorsalis n. vagi", "+ nucleus ambiguus (medulla oblongata)"])
s.box(360, 102, 260, 66, ["N. vagus [X]", "rr. cardiaci cervicales sup. ve inf.,", "rr. cardiaci thoracici (n. laryngeus recurrens)"], lh=14.5)
s.box(360, 194, 260, 52, ["Ganglia cardiaca", "kalp duvarında · kısa postganglionik lif"])
for x in (150, 490):
    s.arrow(x, 77, x, 100)
    s.arrow(x, 169, x, 192)
s.box(170, 270, 300, 52, ["Plexus cardiacus", "superficialis (arcus altı) · profundus (bifurkasyon önü)"], kind="key")
s.arrow(150, 247, 240, 268)
s.arrow(490, 247, 400, 268)
s.box(20, 340, 280, 52, ["Kalp hızı ↑ · iletim ↑ · kasılma gücü ↑", "noradrenalin → β₁ reseptör"])
s.box(340, 340, 280, 52, ["Kalp hızı ↓ · AV iletim ↓", "asetilkolin → M₂ reseptör (SA ve AV düğüm)"])
s.arrow(250, 323, 190, 338)
s.arrow(390, 323, 450, 338)
s.save(os.path.join(OUT, "k1_sinir.svg"))

# 7. Fetal dolaşım
s = SVG(640, 520, "Fetal dolaşımda kanın yolu ve üç şant", "ft")
s.box(250, 8, 140, 38, ["Plasenta"], fs1=13)
s.box(200, 76, 240, 44, ["V. umbilicalis", "O₂ doygunluğu ≈ %80"])
s.box(30, 150, 230, 46, ["1 · Ductus venosus", "kanın yaklaşık yarısı karaciğeri atlar"], kind="key")
s.box(380, 150, 230, 46, ["Karaciğer sinüzoidleri", "→ vv. hepaticae"])
s.box(200, 226, 240, 44, ["V. cava inferior → sağ atriyum", "alt gövdenin venöz kanıyla karışır"])
s.box(20, 302, 250, 52, ["2 · Foramen ovale", "→ sol atriyum → sol ventrikül"], kind="key")
s.box(370, 302, 250, 52, ["Sağ ventrikül", "VCS + sinus coronarius + VCİ'nin azı"])
s.box(20, 384, 250, 46, ["Aorta ascendens", "koroner arterler, baş, boyun, kollar"])
s.box(300, 384, 170, 46, ["3 · Ductus arteriosus", "→ arcus aortae"], kind="key")
s.box(490, 384, 130, 46, ["Akciğerler", "yaklaşık %10"])
s.box(130, 460, 380, 50, ["Aorta descendens → gövde ve alt ekstremite", "aa. umbilicales (a. iliaca interna) → plasenta"])
s.arrow(320, 47, 320, 74)
s.arrow(260, 121, 175, 148)
s.arrow(380, 121, 465, 148)
s.arrow(175, 197, 255, 224)
s.arrow(465, 197, 385, 224)
s.arrow(270, 271, 175, 300)
s.arrow(370, 271, 465, 300)
s.text(150, 284, "VCİ akımının çoğu", "small", "end")
s.text(150, 296, "(crista dividens)", "small", "end")
s.text(490, 284, "VCS kanı", "small", "start")
s.arrow(145, 355, 145, 382)
s.arrow(460, 355, 400, 382)
s.arrow(530, 355, 555, 382)
s.arrow(170, 431, 230, 458)
s.arrow(385, 431, 360, 458)
s.path("M511,485 L630,485 L630,27 L392,27", NEU)
s.text(616, 250, "deoksijene kan", "small", "end", rotate=None)
s.save(os.path.join(OUT, "k1_fetal.svg"))

# 8. Arcus aortae ve a. subclavia dalları
s = SVG(640, 360, "Arcus aortae'nin dalları ve a. subclavia'nın dalları", "ar")
s.box(200, 8, 240, 46, ["Arcus aortae", "manubrium arkası · T4'te sonlanır"])
s.box(10, 86, 200, 46, ["1 · Truncus brachiocephalicus", "en kalın dal · ≈4-5 cm"])
s.box(250, 86, 140, 46, ["2 · A. carotis", "communis sinistra"])
s.box(430, 86, 200, 46, ["3 · A. subclavia sinistra", "arcus'un son dalı"])
s.arrow(260, 55, 140, 84)
s.arrow(320, 55, 320, 84)
s.arrow(380, 55, 500, 84)
s.box(10, 160, 190, 40, ["A. carotis communis dextra"], fs1=12)
s.box(10, 214, 190, 40, ["A. subclavia dextra"], fs1=12)
s.arrow(60, 133, 60, 158)
s.path("M211,109 L224,109 L224,234 L203,234", NEU)
s.text(12, 272, "sağ art. sternoclavicularis", "small")
s.text(12, 285, "arkasında ikiye ayrılır", "small")
s.box(240, 160, 390, 190, [("A. subclavia'nın dalları (her iki tarafta aynı)", "cap"),
                           ("1. bölüm (m. scalenus anterior'un medialinde)", "cyanb"),
                           ("A. vertebralis → C6 foramen transversarium → beyin", "body"),
                           ("A. thoracica interna → a. pericardiacophrenica,", "body"),
                           ("   aa. intercostales ant., a. musculophrenica, a. epigastrica sup.", "body"),
                           ("Truncus thyrocervicalis → a. thyroidea inferior,", "body"),
                           ("   a. cervicalis ascendens, a. suprascapularis, a. transversa cervicis", "body"),
                           ("2. bölüm (kasın arkasında)", "cyanb"),
                           ("Truncus costocervicalis → a. intercostalis suprema (1-2. İKA)", "body"),
                           ("   ve a. cervicalis profunda", "body"),
                           ("3. bölüm (kasın lateralinde) → a. dorsalis scapulae", "cyanb")],
      align="start", pad_top=18, lh=15.5)
s.arrow(530, 133, 530, 158)
s.save(os.path.join(OUT, "k1_arcus.svg"))

# 9. A. carotis externa dalları
s = SVG(640, 440, "A. carotis externa'nın dallarının çıkış sırası ve yönleri", "ce")
s.add('<line x1="320" y1="395" x2="320" y2="70" stroke="var(--color-text)" stroke-width="3"/>')
s.box(230, 396, 180, 42, ["A. carotis externa", "bifurkasyonda (C4) başlar"], fs1=12, lh=14)
s.text(10, 421, "A. carotis interna boyunda dal vermez →", "small")
s.box(390, 320, 240, 44, ["1 · A. thyroidea superior", "a. laryngea superior · gl. thyroidea"])
s.box(10, 300, 230, 44, ["2 · A. pharyngea ascendens", "medialden · en ince · a. meningea post."])
s.box(390, 254, 240, 44, ["3 · A. lingualis", "cornu majus ossis hyoidei · dil"])
s.box(390, 188, 240, 44, ["4 · A. facialis", "tonsilla, gl. submandibularis, yüz"])
s.box(10, 220, 230, 44, ["5 · A. occipitalis", "ense derisi, m. SCM, mastoid"])
s.box(10, 140, 230, 44, ["6 · A. auricularis posterior", "kulak arkası · a. stylomastoidea"])
s.box(390, 96, 240, 50, ["7 · A. maxillaris (uç dal)", "collum mandibulae arkasından öne:", "dişler, dura, burun, damak"], lh=14)
s.box(200, 10, 240, 50, ["8 · A. temporalis superficialis (uç dal)", "tragusun önü (nabız) · saçlı deri"], fs1=12)
for y, side in ((342, 1), (276, 1), (210, 1)):
    s.arrow(320, y, 388, y)
s.arrow(320, 322, 242, 322)
s.arrow(320, 242, 242, 242)
s.arrow(320, 162, 242, 162)
s.arrow(320, 85, 388, 115)
s.arrow(320, 70, 320, 62)
s.text(390, 384, "ÖN DALLAR: 1, 3, 4", "cap")
s.text(10, 368, "ARKA DALLAR: 5, 6 · MEDİAL: 2", "cap")
s.save(os.path.join(OUT, "k1_externa.svg"))

# 10. Yüzün ve boynun venöz drenajı
s = SVG(640, 560, "Yüz ve boyun venlerinin bağlantıları ve sinus cavernosus ile ilişkisi", "vn")
s.box(220, 8, 200, 46, ["Sinus cavernosus", "kafa içi · kapaksız bağlantılar"], kind="key")
s.box(10, 90, 200, 46, ["V. ophthalmica superior", "orbita"])
s.box(230, 90, 200, 46, ["V. ophthalmica inferior", "+ vv. emissariae"])
s.box(10, 172, 200, 52, ["V. angularis", "v. supratrochlearis +", "v. supraorbitalis"], lh=14)
s.box(230, 172, 200, 52, ["Plexus pterygoideus", "fossa infratemporalis,", "m. pterygoideus lateralis çevresi"], lh=14)
s.box(450, 172, 180, 52, ["V. temporalis", "superficialis", "saçlı deri, şakak"], lh=14)
s.box(10, 262, 180, 46, ["V. facialis", "a. facialis'in arkasında"])
s.box(230, 262, 120, 46, ["V. profunda", "faciei"])
s.box(370, 262, 120, 46, ["V. maxillaris", "kısa gövde"])
s.box(400, 344, 230, 46, ["V. retromandibularis", "gl. parotidea içinde oluşur"])
s.box(10, 344, 230, 46, ["V. facialis communis", "v. facialis + ön dal"])
s.box(10, 424, 230, 46, ["V. jugularis interna", "sinus sigmoideus'un devamı"])
s.box(400, 424, 230, 46, ["V. jugularis externa", "arka dal + v. auricularis post."])
s.box(10, 502, 380, 50, ["V. brachiocephalica (angulus venosus)", "art. sternoclavicularis arkası → VCS"], kind="key")
s.box(430, 502, 200, 46, ["V. subclavia"])
both(s, 110, 137, 110, 170)          # angularis <-> ophthalmica sup
both(s, 140, 89, 230, 50)            # ophthalmica sup <-> cavernosus
both(s, 330, 89, 330, 56)            # ophthalmica inf <-> cavernosus
both(s, 330, 137, 330, 170)          # ophthalmica inf <-> plexus
s.arrow(110, 225, 110, 260)          # angularis -> facialis
both(s, 192, 285, 228, 285)          # facialis <-> profunda
both(s, 290, 261, 300, 227)          # profunda <-> plexus
s.arrow(390, 225, 420, 260)          # plexus -> maxillaris
s.arrow(450, 309, 480, 342)          # maxillaris -> retromandibularis
s.arrow(560, 225, 560, 342)          # temporalis sup -> retromandibularis
s.arrow(110, 309, 110, 342)          # facialis -> communis
s.arrow(398, 362, 243, 362)          # ön dal
s.text(320, 356, "ön dal", "small", "middle")
s.arrow(515, 391, 515, 422)          # arka dal
s.text(522, 410, "arka dal", "small")
s.arrow(110, 391, 110, 422)
s.arrow(110, 471, 110, 500)
s.arrow(515, 471, 530, 500)
s.arrow(429, 525, 392, 525)
s.save(os.path.join(OUT, "k1_venoz.svg"))

print("svg:", sorted(os.listdir(OUT)))
