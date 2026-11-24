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
