# MSD-7 kitabinin bolum dosyalarini uretir: yapi/b{n}.txt (konu + cikmis soru kartlari), yapi/ezber.txt, yapi/on.txt
# girdi: k{n}.txt (konu anlatimi), a{n}.txt (kume aciklamalari), ../yeni/sorular.json, ../yeni/atama.json
# a{n}.txt bicimi: "=== ilk_anahtar" ; "C: harf" (cevap duzeltme) ; "N: not" (Onceki satirina eklenir) ; "E: ezber" ; paragraflar
# kullanim: python3 -I olustur.py
import json, os, re, collections
K = os.path.dirname(os.path.abspath(__file__)); Y = f"{K}/yapi"
BOL = {1: "İshale Yaklaşım, Klinik Tipler ve Viral Etkenler", 2: "Dehidratasyon ve Sıvı Tedavisi", 3: "Su ve Besin Kaynaklı Salgınlar",
       4: "Bağırsak Mikrobiyotası ve Probiyotikler", 5: "Salmonella, Shigella, E. coli, Yersinia ve Laboratuvar Tanısı",
       6: "Toksin Kaynaklı İshaller ve Diğer Bakteriler", 7: "Sindirim Sistemi Protozoonları", 8: "Bağırsak Nematodları",
       9: "Sestodlar ve Trematodlar", 10: "Antihelmintik ve Antiprotozoal İlaçlar"}
YILS = ["2025-26", "2024-25", "2023-24", "2022-23", "2021-22", "2020-21", "2019-20"]
D = {f"{q['yil']}-{q['no']}": q for q in json.load(open(f"{K}/../yeni/sorular.json", encoding="utf-8"))}
AT = json.load(open(f"{K}/../yeni/atama.json", encoding="utf-8"))
KUME = {a["sorular"][0]: a for a in AT}
def yil(k): return k.rsplit("-", 1)[0]
def kisa(k): return f"{yil(k)} S{k.rsplit('-', 1)[1]}"
def temiz(t): return re.sub(r"\s+", " ", t.replace("^circ", "°").replace("$", "")).strip()
def dogru_metin(q, c=None):
    c = c or q["cevap"]
    return next((t for h, t in q["sik"] if h == c), q["cevap_metin"])
def norm(t): return re.sub(r"[^a-zçğıöşü0-9]", "", t.lower())

A = {}
for b in BOL:
    p = f"{K}/a{b}.txt"
    if not os.path.exists(p): continue
    for blok in open(p, encoding="utf-8").read().split("=== ")[1:]:
        sat = blok.strip().split("\n"); k = sat[0].strip()
        d = dict(bolum=b, c="", n="", e="", par=[])
        for l in sat[1:]:
            if l.startswith("C: "): d["c"] = l[3:].strip()
            elif l.startswith("N: "): d["n"] = l[3:].strip()
            elif l.startswith("E: "): d["e"] = l[3:].strip()
            elif l.strip(): d["par"].append(l.strip())
        assert k in KUME, ("bilinmeyen anahtar", k)
        A[k] = d

def kart(k):
    a, ks = A[k], KUME[k]["sorular"]; q = D[k]; c = a["c"] or q["cevap"]
    acik = c.startswith("@")
    n = len(ks); rozet = f"{n} KEZ" if n > 1 else "1 KEZ"
    yillar = sorted({yil(x) for x in ks}, key=YILS.index)
    et = "Çıktığı sınavlar: " + " · ".join(kisa(x) for x in sorted(ks, key=lambda x: YILS.index(yil(x))))
    r = [f"@Q {kisa(k)} | {rozet} | {et}"]
    r += ["@K " + temiz(x) for x in q["kok"]]
    if q["sik"] and not acik: r += [f"{h}) {temiz(t)}" + (" ✓" if h == c else "") for h, t in q["sik"]]
    else: r.append("@A " + (c[1:].strip() if acik else temiz(q["cevap_metin"] or c)))
    ref = norm(c[1:] if acik else dogru_metin(q, c))
    var = []
    for x in ks[1:]:
        dm = dogru_metin(D[x])
        if dm and norm(dm) != ref: var.append(f"{kisa(x)}: **{temiz(dm)}**")
    o = []
    if var: o.append("Diğer yıllarda doğru cevap: " + "; ".join(var) + ".")
    if a["n"]: o.append(a["n"])
    if o: r.append("@O " + " ".join(o))
    r += a["par"] + ["@@"]
    return r

eksik = []
for b, ad in BOL.items():
    kl = [x["sorular"][0] for x in AT if x["bolum"] == b]
    yazilan = [k for k in A if A[k]["bolum"] == b]
    eksik += [k for k in kl if k not in A]
    kp = f"{K}/k{b}.txt"
    L = [open(kp, encoding="utf-8").read().rstrip()] if os.path.exists(kp) else [f"# {ad} || Bölüm {b}"]
    ns = sum(len(KUME[k]["sorular"]) for k in kl); tek = sum(len(KUME[k]["sorular"]) > 1 for k in kl)
    L += ["", f"## Çıkmış sorular: {ad}",
          f"Bu bölümden 7 sınavda **{ns} soru** çıktı; bunlar **{len(kl)} farklı soruya** karşılık geliyor ve **{tek} tanesi** birden fazla yıl soruldu. "
          "Her kartta sorunun en yeni hâli, sağ üstte kaç kez sorulduğu, kartın altında da çıktığı tüm sınavlar yazar. Rozeti koyu olanlar 3 ve daha fazla kez sorulmuş sorulardır.",
          "@QB Çıkmış sorular"]
    for k in yazilan: L += kart(k)
    open(f"{Y}/b{b}.txt", "w", encoding="utf-8").write("\n".join(L) + "\n")
print("eksik aciklama:", len(eksik), eksik[:12])


# --- ezber ozeti: her bolumun ozet maddeleri + ?? ipuclari ---
LE = ["# Son Gün Ezber Özeti | Her bölümün özü tek satırlık maddeler hâlinde: önce bölümün ana hatları, sonra ezber ipuçları. Sınavdan önceki gün yalnız bu bölümü okumak, kitabın tamamını hatırlamaya yeter. || MSD-7 · Ezber"]
for b, ad in BOL.items():
    kp = f"{K}/k{b}.txt"
    if not os.path.exists(kp): continue
    sat = open(kp, encoding="utf-8").read().split("\n")
    ip = [l[3:].strip() for l in sat if l.startswith("?? ")]
    # bolum ozeti maddeleri
    ozet, topla = [], False
    for l in sat:
        if re.match(r"^## .*[Öö]zet", l): topla = True; continue
        if l.startswith("## "): topla = False
        if topla and l.startswith("- "): ozet.append(l[2:].strip())
    if not ip and not ozet: continue
    LE.append(f"## {b}. {ad}")
    if ozet:
        LE.append("### Bölümün özü")
        LE += ["- " + x for x in ozet]
    if ip:
        LE.append("### Ezber ipuçları")
        LE += ["- " + x for x in ip]
open(f"{Y}/ezber.txt", "w", encoding="utf-8").write("\n".join(LE) + "\n")

# --- on sayfa: genel bakis + bolum dagilimi + soru dizini ---
import collections as _c
def tum(t): return re.sub(r"\s+", " ", t)
top = sum(len(KUME[a["sorular"][0]]["sorular"]) for a in AT)
bolum_say = _c.Counter(a["bolum"] for a in AT)
bolum_soru = _c.Counter()
for a in AT: bolum_soru[a["bolum"]] += len(a["sorular"])
tekrar3 = sum(len(a["sorular"]) >= 3 for a in AT)
LO = ["# MSD-7 Ders Kitabı | Blok 2 · Modül 7 — mikrobiyolojik ishal, gastroenterit etkenleri, bağırsak paraziter hastalıkları ve antiparaziter ilaçlar. Konuların tamamı mekanizmasıyla anlatılır; her bölümün sonunda yedi yılın (2019-20 … 2025-26) çıkmış soruları çözümleriyle bulunur. || MSD-7 · 2026-27",
      "~ 10 bölüm · textbook derinliğinde konu anlatımı · 339 çıkmış soru · son gün ezber özeti",
      "## Bu kitap nasıl kullanılır?",
      "Kitabın omurgası **konu anlatımıdır**. Her bölüm, konuyu sorular yokmuş gibi, baştan ve nedenselliğiyle anlatır: olayın hücresel ya da epidemiyolojik mekanizması kurulur, tablolarla karşılaştırmalar yapılır, şemalarla çok adımlı süreçler görselleştirilir. Amaç, soruları tanımak değil konuyu bilmektir; soru tanımak bunun yan ürünüdür.",
      "Her bölümün yapısı şöyledir:",
      "1. **Konu anlatımı:** mekanizmadan kliniğe, tablolar ve şemalarla. Metin içindeki **sınav notu** kutuları sık karıştırılan ya da kaynaklar arasında çelişen noktaları, **ezber ipucu** kutuları ise akılda kalıcı kısayolları verir.",
      "2. **Bölüm özeti:** o bölümün özü, maddeler hâlinde.",
      f"3. **Çıkmış sorular:** yedi sınavda bu bölümden çıkan sorular. Yinelenen sorular tek kartta toplanmıştır: kartın sağ üstünde **kaç kez sorulduğu** (koyu rozet = 3 ve üzeri), altında **çıktığı tüm sınavlar**, ardından doğru şık ve **çeldiricilerin neden yanlış olduğu** yazar. Toplam **339 soru**, **{len(AT)} ayrı soruya** karşılık gelir.",
      "Kitabın sonunda **son gün ezber özeti** vardır: her bölümün özü ve ezber ipuçları tek satırlık maddeler hâlinde toplanmıştır. Sınavdan önceki gün yalnız o bölüm okunabilir.",
      "## Bölümlere dağılım",
      "| # | Bölüm | Farklı soru | Toplam soru |"]
for b, ad in BOL.items():
    LO.append(f"| {b} | {ad} | {bolum_say[b]} | {bolum_soru[b]} |")
LO += [f"| | **Toplam** | **{len(AT)}** | **{top}** |",
       f"|= Yedi sınavın {top} sorusu {len(AT)} ayrı soruya karşılık geliyor; {tekrar3} soru 3 ya da daha fazla kez çıkmış.",
       "## Sınavda en çok tekrar eden konular (3+ kez)"]
cok = sorted([a for a in AT if len(a["sorular"]) >= 3], key=lambda a: -len(a["sorular"]))
LO.append("| Kez | Konu | Bölüm |")
for a in cok:
    k = a["sorular"][0]; q = D[k]
    kok = tum(" ".join(q["kok"])).replace("*", "").replace("|", "/")
    kok = re.sub(r"^(Klinik Bulgular:|Aşağıdakilerden|Aşağıdaki)\s*", "", kok)
    konu = (kok[:66] + "…") if len(kok) > 68 else kok
    LO.append(f"| {len(a['sorular'])} | {konu} | {a['bolum']} |")
LO.append("|= En sık tekrar eden sorular. Bu konuları önce çalışın.")
open(f"{Y}/on.txt", "w", encoding="utf-8").write("\n".join(LO) + "\n")
print("on + ezber yazildi; en cok tekrar:", len(cok))
