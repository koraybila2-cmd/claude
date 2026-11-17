# 2026-27 MSD 5-6 sorularindan bolum bolum isaretleme dosyalari uretir: yeni/yapi_txt/b{n}.txt, on.txt, ezber.txt
# kullanim: python3 -I olustur.py
import os, re, collections
K = os.path.dirname(os.path.abspath(__file__)); O = f"{K}/yapi_txt"; os.makedirs(O, exist_ok=True)
MD = f"{K}/../msd2627/D3_MSD_5-6_2026-2027_Sorular.md"
BOL = {1: "Beslenme ve Büyüme İzlemi", 2: "Malnütrisyon ve Raşitizm", 3: "İshal, Malabsorbsiyon ve Çölyak", 4: "Sindirim Sistemi Anatomisi ve Histolojisi",
       5: "Açlık Biyokimyası ve Üre Döngüsü", 6: "Sıvı-Elektrolit Dengesi ve Tübül Fizyolojisi", 7: "Akut Böbrek Hasarı, Diyaliz ve Nefrotoksisite",
       8: "Glomerül Hastalıkları", 9: "Kronik Böbrek Hastalığı, Diyabetik Nefropati ve Hipertansiyon", 10: "Diüretikler, ACE İnhibitörleri, ARB ve Kalsiyum Kanal Blokerleri",
       11: "Dermatofitler ve Diğer Mantarlar"}
ESKI = {1: 7, 2: 4, 3: 6, 4: 5, 5: 5, 6: 12, 7: 8, 8: 3, 9: 10, 10: 9, 11: 6}
def tex(t):
    t = re.sub(r"\$(.+?)\$", lambda m: m.group(1), t)
    t = re.sub(r"\\text\{(.*?)\}", r"\1", t)
    t = t.replace("\\%", "%").replace("^+", "⁺").replace("^-", "⁻").replace("\\ge", "≥").replace("\\le", "≤").replace("{", "").replace("}", "")
    t = t.replace("\\", "")
    return re.sub(r"\s+", " ", t).strip()
# sorular
Y = open(MD, encoding="utf-8").read()
S = {}
for m in re.finditer(r"\*\*(\d+)\. (.+?)\*\*\n(.*?)\*\*Doğru Şık:\*\* ([A-E])", Y, re.S):
    n = int(m.group(1)); govde = m.group(3).split("\n"); ek, sik = [], []
    for l in govde:
        l = l.rstrip()
        if not l.strip(): continue
        mm = re.match(r"^- ([A-E])\) (.*)$", l.strip())
        if mm: sik.append((mm.group(1), tex(mm.group(2))))
        elif not sik and not l.startswith(">") and not l.startswith("*"): ek.append(tex(l.strip().lstrip("- ")))
    S[n] = dict(kok=tex(m.group(2)), ek=ek, sik=sik, c=m.group(4))
assert len(S) == 76, len(S)
# aciklamalar
A = {}
for blok in open(f"{K}/aciklamalar.txt", encoding="utf-8").read().split("=== ")[1:]:
    satir = blok.strip().split("\n"); bas = [x.strip() for x in satir[0].split("|")]
    n = int(bas[0]); d = dict(bolum=int(bas[1]), etiket=bas[2], onceki="", ezber="", par=[])
    for l in satir[1:]:
        if l.startswith("O: "): d["onceki"] = l[3:]
        elif l.startswith("E: "): d["ezber"] = l[3:]
        elif l.strip(): d["par"].append(l)
    A[n] = d
assert sorted(A) == list(range(1, 77)), set(range(1, 77)) - set(A)
for n in S:
    dogru = [h for h, t in S[n]["sik"] if "✓" in t]
    assert not dogru
    # aciklamanin ilk harfi cevapla uyumlu mu
    assert A[n]["par"][0].startswith(S[n]["c"]), (n, S[n]["c"], A[n]["par"][0][:20])
def duzelt(e):
    t = e.replace("I", "ı").replace("İ", "i").lower().replace("ı", "ı")
    t = t[0].upper() + t[1:] if not t.startswith("i") else "İ" + t[1:]
    t = re.sub(r"\bs(\d)", r"S\1", t); t = re.sub(r"\b(msd|bsd)\b", lambda m: m.group(1).upper(), t)
    return t.replace("anti-pla2r", "anti-PLA2R")
def tekrar(e): return not e.startswith("İLK KEZ")
bolumler = collections.defaultdict(list)
for n in sorted(A): bolumler[A[n]["bolum"]].append(n)
def kart(n):
    s, a = S[n], A[n]; r = [f"@Q MSD 5-6 2026-27 · SORU {n} | BU YIL | {a['etiket']}", "@K " + s["kok"]] + ["@K " + e for e in s["ek"]]
    r += [f"{h}) {t}" + (" ✓" if h == s["c"] else "") for h, t in s["sik"]]
    r += ["@O " + a["onceki"]] + a["par"] + ["@@"]
    return r
for b, ns in sorted(bolumler.items()):
    tk = sum(tekrar(A[n]["etiket"]) for n in ns)
    lead = (f"Bu yıl {len(ns)} soru (S{', S'.join(map(str, ns))}); geçen yıl {ESKI[b]} soru. {tk} soru daha önceki sınavlarda aynı ya da benzer biçimde geldi, "
            f"{len(ns) - tk} soru ilk kez soruldu. Bu yılın kartlarından sonra konu eki, ardından önceki baskının bu bölümü (2025-26 ve 2024-25 soruları ve konu tekrarı) gelir.")
    L = [f"# {BOL[b]} | {lead} || Modül 5-6 · Bölüm {b} · 2026-27 soruları", "@QB BU YILIN SORULARI"]
    for n in ns: L += kart(n)
    ekp = f"{K}/ek/ek{b}.txt"
    if os.path.exists(ekp): L += ["", open(ekp, encoding="utf-8").read()]
    open(f"{O}/b{b}.txt", "w", encoding="utf-8").write("\n".join(L) + "\n")
# ezber listesi
L = ["# 2026-27 Sorularından Ezber Listesi | Bu yılın 76 sorusunun her birinden akılda kalması gereken bilgi, bölüm sırasıyla tek satırda. Sınavdan önceki gün bu listeyi okuyun. || Modül 5-6 · Ezber listesi"]
for b, ns in sorted(bolumler.items()):
    L.append(f"## {b}. {BOL[b]}")
    L += [f"- **S{n}:** {A[n]['ezber']}" for n in ns]
open(f"{O}/ezber.txt", "w", encoding="utf-8").write("\n".join(L) + "\n")
# on sayfa: genel bakis + dizin
tk_top = sum(tekrar(A[n]["etiket"]) for n in A)
L = ["# Modül 5-6 · 2026-27 sorularıyla güncel baskı | Kısaltılmış tek kitabın 2026-27 MSD 5-6 sorularıyla güncellenmiş hâli. || Modül 5-6 · 2026-27",
     "## Bu baskıda ne değişti?",
     "Önceki baskı 2025-26 sorularıyla hazırlanmıştı ve 2026-27 sınavı henüz yoktu. Bu baskıda **2026-27 MSD 5-6'nın 76 sorusunun tamamı** çözümleriyle eklendi. Her bölümün başına yeni bir “2026-27 soruları” kısmı geldi:",
     "1. **Bu yılın kartları:** doğru şık, çeldiricilerin neden yanlış olduğu ve aynı bilginin daha önce hangi MSD ya da blok sınavında sorulduğu.",
     "2. **Konu eki:** bu yılın sorularının gerektirdiği, önceki konu tekrarında kısa geçen bilgiler tablolar hâlinde.",
     "3. Ardından önceki baskının aynı bölümü değişmeden gelir: 2025-26 MSD, 2025-26 blok sınavı ve 2024-25 MSD soruları ile konu tekrarı.",
     "Kitabın sonuna 76 sorunun her birinden tek satırlık **ezber listesi** eklendi. Önceki baskının giriş sayfaları (konu analizi, kalıp tablosu, 2025-26 soru dizini) bu bölümden sonra olduğu gibi duruyor.",
     "## Bu yılın sınavı geçmişle nasıl örtüşüyor?",
     f"76 sorunun **{tk_top}'i** daha önceki MSD 5-6 ya da blok sınavlarında aynı, ters çevrilmiş ya da aynı bilgiyi soran biçimde çıkmıştı; **{76 - tk_top} soru** arşivde ilk kez görülüyor. Önceki yıllarda olduğu gibi Modül 5-6'nın soru havuzu geniştir, ama bazı kalıplar her yıl döner:",
     "- **z-skoru hesabı** 7. kez (S24), **kronik malnütrisyonda yaşa göre boy** 5. kez (S23), **boya göre ağırlık = akut malnütrisyon** (S6, S20).",
     "- **Raşitizmin biyokimyası** 8. kez (S22; bu kez doğru şık olarak), **yeniden beslenme sendromu** 7. kez (S10; bu kez mekanizma).",
     "- **Diüretik ilaç-mekanizma eşleştirmesi** 5. kez (S67), **ARB'nin anjiyotensin II'yi artırması** (S65), **çölyakta T hücre yanıtı** (S75) ve **çölyak biyopsisi** (S76) geçen yılın neredeyse aynısı.",
     "- **Acil diyaliz endikasyonları**, **KDIGO ölçütleri**, **prerenal azotemi**, **NSAİİ'nin afferent arteriyole etkisi** ve **Microsporum canis** blok sınavı ya da geçen yıl MSD'siyle aynı bilgi.",
     "- **Yeni gelenler:** bebekte bal, tamamlayıcı beslenme, bağırsakların ikili arteriyel beslenmesi, n. pudendus, caecum lenf drenajı, ödemin ağırlığı maskelemesi, konjenital ishal, Paneth hücresi, eGFR ve kas kütlesi, KBH anemisi, diyabette kırmızı bayraklar, Türkiye'de evre 5 KBH nedeni, Guyton modeli, akıllı saatle kan basıncı ölçümü, FGF-23, maküla densa, hemodiyalizde difüzyon, anti-PLA2R, FSGS ve IgA nefropatisi vakaları, C3 nefritik faktör, glutamat dehidrojenaz, Majocchi granülomu, germ tüp, *T. indotineae* ve mantar melanini.",
     "!! İki soruda anahtar standart bilgiyle tam örtüşmüyor: **S46** (acil diyaliz endikasyonu olarak “dirençli üremik kaşıntı”) ve **S69** (anjioinvaziv küf olarak yalnız *Rhizopus*; *Aspergillus* da anjioinvazivdir). Kartlarda kaynak notu var; sınavda anahtarın istediği şıkkı işaretleyin.",
     "## Bölümlere dağılım",
     "| Bölüm | Konu | 2026-27 | 2025-26 |"]
L += [f"| {b} | {BOL[b]} | {len(bolumler[b])} | {ESKI[b]} |" for b in sorted(BOL)]
L += [f"| | **Toplam** | **76** | **{sum(ESKI.values())}** |", "|= Bu yıl böbrek, sıvı-elektrolit ve böbrek farmakolojisi (bölüm 6-10) 43 soru, yani sınavın yarısından fazlası.",
      "## 2026-27 sorularının dizini", "| No | Bölüm | Cevap | Geçmişle ilişkisi |"]
L += [f"| {n} | {A[n]['bolum']}. {BOL[A[n]['bolum']].split(',')[0]} | {S[n]['c']} | {duzelt(A[n]['etiket'])} |" for n in sorted(A)]
L += ["|= Soru dizini. Ayrıntılı geçmiş bilgisi her kartın “Önceki yıllar” satırındadır."]
open(f"{O}/on.txt", "w", encoding="utf-8").write("\n".join(L) + "\n")
print("yazildi:", sorted(os.listdir(O)), "tekrar:", tk_top)
