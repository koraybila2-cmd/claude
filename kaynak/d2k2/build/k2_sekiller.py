"""Kitap 2 (D2K2 damarlar ve lenfatik sistem) şemaları -> kitaplar/k2/svg/*.svg"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
from svglib import SVG, NEU, CYAN, MAG  # noqa: E402

B = os.path.dirname(__file__)
OUT = os.path.join(B, "..", "kitaplar", "k2", "svg")
os.makedirs(OUT, exist_ok=True)

# 1. A. subclavia'nın bölümleri ve dalları
s = SVG(660, 330, "A. subclavia'nın m. scalenus anterior'a göre üç bölümü ve dalları", "sc")
s.text(330, 14, "M. SCALENUS ANTERIOR ARTERİ ÜÇ BÖLÜME AYIRIR", "cap", "middle")
s.box(10, 26, 200, 64, ["1. bölüm", "başlangıçtan kasın medial", "kenarına kadar · en çok dal"], kind="key", lh=14)
s.box(230, 26, 200, 64, ["2. bölüm", "kasın arkasında, plexus brachialis", "ile birlikte · en kısa, en yüksek"], lh=14)
s.box(450, 26, 200, 64, ["3. bölüm", "kasın lateralinden 1. kaburganın", "dış kenarına → a. axillaris"], lh=14)
s.arrow(211, 58, 228, 58)
s.arrow(431, 58, 448, 58)
s.box(10, 110, 200, 210, [("1. bölümün dalları", "cyanb"),
                          ("A. vertebralis", "title"),
                          ("C6 for. transversarium →", "body"),
                          ("for. magnum → beyin", "body"),
                          ("A. thoracica interna", "title"),
                          ("sternumun ≈1 cm lateralinde iner,", "body"),
                          ("6. İKA'da a. musculophrenica", "body"),
                          ("(7-9. İKA) + a. epigastrica sup.", "body"),
                          ("Truncus thyrocervicalis", "title"),
                          ("a. thyroidea inferior,", "body"),
                          ("a. suprascapularis,", "body"),
                          ("a. transversa colli", "body")],
      align="start", pad_top=18, lh=15.5, fs1=12)
s.box(230, 110, 200, 120, [("2. bölümün dalı", "cyanb"),
                           ("Truncus costocervicalis", "title"),
                           ("a. intercostalis suprema", "body"),
                           ("→ 1. ve 2. İKA", "body"),
                           ("a. cervicalis profunda", "body"),
                           ("→ ensenin derin kasları", "body")],
      align="start", pad_top=18, lh=16, fs1=12)
s.box(450, 110, 200, 120, [("3. bölüm ve sonrası", "cyanb"),
                           ("(a. dorsalis scapulae bazen", "body"),
                           ("buradan çıkar)", "body"),
                           ("Kol arkaya-aşağı çekilince", "body"),
                           ("arter klavikula ile 1. kaburga", "body"),
                           ("arasında sıkışır", "body")],
      align="start", pad_top=18, lh=16, fs1=12)
s.box(230, 246, 420, 74, [("Sağ-sol farkı", "magb"),
                          ("Sağ: truncus brachiocephalicus'tan, sağ art.", "body"),
                          ("sternoclavicularis'in arkasında çıkar. Sol: arcus aortae'nin", "body"),
                          ("3. dalı (T4), göğüs içi bölümü olduğu için daha uzundur.", "body")],
      kind="mag", align="start", pad_top=18, lh=15.5)
s.save(os.path.join(OUT, "k2_subclavia.svg"))

# 2. Ekstremite arterlerinin ad değişimleri
s = SVG(660, 420, "Üst ve alt ekstremite ana arterinin ad değiştirdiği sınırlar", "ad")
s.text(105, 16, "ÜST EKSTREMİTE", "cap", "middle")
s.text(435, 16, "ALT EKSTREMİTE", "cap", "middle")
up = [["A. subclavia"], ["A. axillaris"], ["A. brachialis"], ["A. radialis + a. ulnaris"],
      ["Arcus palmaris", "superficialis (ulnaris)", "profundus (radialis)"]]
ul = ["1. kaburganın dış kenarı", "m. teres major'un alt kenarı", "collum radii (fossa cubiti)", "el bileği → avuç içi"]
lo = [["A. iliaca externa"], ["A. femoralis"], ["A. poplitea"], ["A. tibialis anterior", "+ a. tibialis posterior"],
      ["A. dorsalis pedis (önden)", "aa. plantares (arkadan)"]]
ll = ["lig. inguinale (lacuna vasorum)", "hiatus adductorius", "m. popliteus'un alt kenarı", "ayak bileği eklemi"]
for col, (boxes, labels, x) in enumerate(((up, ul, 20), (lo, ll, 350))):
    for i, b in enumerate(boxes):
        y = 28 + i * 80
        kind = "key" if i in (1, 2) else "normal"
        s.box(x, y, 170, 48 if len(b) < 3 else 56, b, kind=kind, lh=14, fs1=12.5)
        if i < len(labels):
            s.arrow(x + 85, y + (49 if len(b) < 3 else 57), x + 85, y + 78)
            s.text(x + 182, y + 66, labels[i], "cyan")
s.save(os.path.join(OUT, "k2_ad.svg"))

# 3. Arka interkostal venlerin dökülme yerleri ve azygos sistemi
s = SVG(660, 420, "Arka interkostal venlerin dökülme yerleri ve azygos sistemi", "az")
s.text(120, 14, "SAĞ TARAF", "cap", "middle")
s.text(540, 14, "SOL TARAF", "cap", "middle")
s.box(255, 24, 150, 46, ["V. cava superior", "→ atrium dextrum"], kind="key")
s.box(20, 24, 200, 46, ["V. brachiocephalica dextra", "VJİ + v. subclavia dx."], fs1=12)
s.box(440, 24, 200, 46, ["V. brachiocephalica sinistra", "daha uzun"], fs1=12)
s.arrow(221, 47, 253, 47)
s.arrow(439, 47, 407, 47)
s.box(255, 112, 150, 150, ["V. azygos", "sağ v. lumbalis", "ascendens'in devamı", "(L1-L2)", "T4'te sağ radix", "pulmonis üzerinden", "kavis yapar"], kind="key", lh=15)
s.arrow(330, 111, 330, 73)
s.box(20, 92, 200, 34, ["1. v. intercostalis post. dx."], fs1=12)
s.arrow(120, 91, 120, 73)
s.box(20, 146, 200, 46, ["2.-4. aralık → v. intercostalis", "superior dextra"], fs1=12)
s.arrow(221, 169, 253, 169)
s.box(20, 212, 200, 46, ["5.-11. vv. intercostales post.", "+ v. subcostalis dextra"], fs1=12)
s.arrow(221, 235, 253, 235)
s.box(440, 92, 160, 34, ["1. v. intercost. post. sin."], fs1=12)
s.arrow(520, 91, 520, 73)
s.box(440, 146, 200, 58, ["2.-4. aralık → v. intercostalis", "superior sinistra", ("v. azygos'a DEĞİL", "magb")], kind="mag", fs1=12, lh=14)
s.path("M641,175 L652,175 L652,47 L643,47", MAG)
s.box(440, 222, 200, 54, ["V. hemiazygos accessoria", "5.-8. aralıklar", "T7'de sağa geçer"], fs1=12, lh=14)
s.arrow(439, 245, 407, 230)
s.box(440, 294, 200, 54, ["V. hemiazygos", "9.-11. + v. subcostalis sin.", "T9'da sağa geçer"], fs1=12, lh=14)
s.arrow(439, 318, 407, 252)
s.box(255, 300, 150, 40, ["Sağ v. lumbalis", "ascendens"], fs1=12)
s.arrow(330, 299, 330, 265)
s.box(440, 370, 200, 40, ["Sol v. lumbalis ascendens", "(crus sinistrum'dan geçer)"], fs1=12, lh=14)
s.arrow(540, 369, 540, 351)
s.box(20, 284, 215, 126, [("V. azygos'a açılanlar", "cyanb"),
                          ("sağ vv. intercostales posteriores", "body"),
                          ("v. intercostalis superior dextra", "body"),
                          ("v. hemiazygos ve accessoria", "body"),
                          ("vv. oesophageales, mediastinales,", "body"),
                          ("pericardiales, v. bronchialis dx.,", "body"),
                          ("v. subcostalis dextra", "body")],
      align="start", pad_top=18, lh=15.5)
s.save(os.path.join(OUT, "k2_azygos.svg"))

# 4. Lenf trunkusları: Kitap 1'deki şema yeniden kullanılır
shutil.copy(os.path.join(B, "..", "kitaplar", "k1", "svg", "k1_lenf.svg"), os.path.join(OUT, "k1_lenf.svg"))
print("ok")
