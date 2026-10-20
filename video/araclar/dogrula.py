#!/usr/bin/env python3
"""Bir bolumun anlatim metnini (parcalar.txt) ve sahne dosyasini (sahne.json) denetler.

kullanim (repo kokunden): python3 video/araclar/dogrula.py video/k4b1 [--json]

HATA'lar giderilmeden bolum seslendirmeye gonderilmez. UYARI'lar gozden gecirilir.
Denetimler: parca bicimi ve boyutu, seslendirmeye uygun olmayan karakterler, satir-secici sayisi,
her secicinin sayfada karsiligi, kitaptaki her icerik blogunun (paragraf, tablo satiri, liste maddesi,
sekil, kutu, soru karti bolumleri) en az bir satira bagli olmasi, cevap acilmadan cevap okunmamasi.
"""
import json, os, re, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bolum

AZAMI, HEDEF, ASGARI = 7500, 7000, 2000
YASAK = re.compile(r"[%<>=±°×÷~≈≥≤→←↑↓/\\\[\]{}#*_|&+()α-ωΑ-Ω₀-₉⁰-⁹⁺⁻µμ·–—…]")
YIL = re.compile(r"\b(19|20)\d\d\b")


def denetle(klasor):
    hatalar, uyarilar = [], []
    ad_b = os.path.basename(os.path.abspath(klasor))
    yol = os.path.join(klasor, "parcalar.txt")
    ham = open(yol, encoding="utf-8").read().splitlines()
    for i, s in enumerate(ham, 1):
        if s.startswith("#") and not re.match(rf"^### {ad_b}_\d\d \| \S.*$", s):
            hatalar.append(f"parcalar.txt:{i}: baslik bicimi '### {ad_b}_NN | Baslik' olmali: {s[:60]}")
    parcalar = bolum.parcalari_oku(yol)
    beklenen = [f"{ad_b}_{i:02d}" for i in range(1, len(parcalar) + 1)]
    if list(parcalar) != beklenen:
        hatalar.append(f"parca adlari {beklenen[0]}'den baslayip sirayla artmali; bulunan: {list(parcalar)}")
    try:
        sahne, girdiler = bolum.sahne_oku(klasor)
    except Exception as e:
        return [f"sahne.json okunamadi: {e}"], uyarilar, None
    for alan in ("kaynak", "ust_baslik", "parcalar"):
        if alan not in sahne: hatalar.append(f"sahne.json'da '{alan}' alani yok")
    if list(parcalar) != list(girdiler):
        hatalar.append(f"sahne.json parca listesi parcalar.txt ile ayni olmali: {list(girdiler)}")

    ozet = []
    for n, (ad, p) in enumerate(parcalar.items(), 1):
        kar = sum(len(s) for s in p["satirlar"]) + len(p["satirlar"]) - 1
        ozet.append((ad, p["baslik"], kar, len(p["satirlar"])))
        if kar > AZAMI: hatalar.append(f"{ad}: {kar} karakter, en fazla {AZAMI} olabilir (ses modeli tek istekte ~11 dk uretebiliyor)")
        elif kar > HEDEF: uyarilar.append(f"{ad}: {kar} karakter, hedef en fazla {HEDEF}")
        if kar < ASGARI and n < len(parcalar):
            uyarilar.append(f"{ad}: {kar} karakter; kucuk parcalari komsusuyla birlestir (hedef {HEDEF - 1500}-{HEDEF})")
        g = girdiler.get(ad, [])
        if len(g) != len(p["satirlar"]):
            hatalar.append(f"{ad}: {len(p['satirlar'])} satir var, sahne.json'da {len(g)} girdi")
        for j, s in enumerate(p["satirlar"], 1):
            yasak = sorted(set(YASAK.findall(s)))
            if yasak: uyarilar.append(f"{ad}:{j}: seslendirmede sorun cikarabilecek karakter {' '.join(yasak)}: …{s[:70]}")
            rakam = [m for m in re.findall(r"\d+(?:[.,]\d+)?", YIL.sub(" ", s))]
            if rakam: uyarilar.append(f"{ad}:{j}: yil disindaki sayilar yaziyla yazilmali: {', '.join(rakam[:6])}")
            if len(s) > 900: uyarilar.append(f"{ad}:{j}: satir {len(s)} karakter; 900'u asan satiri bloklarina gore bol")

    # sayfa denetimi
    ipuclari, acik = [], []
    for ad, gs in girdiler.items():
        for j, g in enumerate(gs, 1):
            if g["ac"] and g["ac"] not in acik: acik.append(g["ac"])
            ipuclari.append({"yer": f"{ad}:{j}", "sel": g["sel"], "acik": list(acik), "dur": g["dur"], "ac": g["ac"]})
    with tempfile.TemporaryDirectory() as tmp:
        html = bolum.bolum_html_kur(sahne, tmp)
        ipy = os.path.join(tmp, "ip.json"); json.dump(ipuclari, open(ipy, "w"), ensure_ascii=False)
        r = subprocess.run(["node", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dogrula.js"), html, ipy],
                           capture_output=True, text=True, env=bolum.node_env())
    if r.returncode:
        return hatalar + [f"sayfa denetimi calismadi: {r.stderr.strip()[:300]}"], uyarilar, None
    rap = json.loads(r.stdout)
    for h in rap["hatali"]: hatalar.append(f"{h['yer']}: gecersiz secici {h['sel']!r}: {h['hata']}")
    for s in rap["seciciler"]:
        if s["n"] == 0: hatalar.append(f"{s['yer']}: secici sayfada hicbir seye karsilik gelmiyor: {s['sel']!r}")
    for k in rap["kapsanmayan"]:
        hatalar.append(f"anlatimda karsiligi olmayan blok [{k['blok']}]: {k['metin']}")
    for k in rap["kapali"]:
        hatalar.append(f"{k['yer']}: {k['kart']} kartinin cevabi acilmadan ({{\"ac\": \"{k['kart']}\"}}) cevap kismi okunuyor: {k['sel']!r}")
    for gn in rap["genis"]:
        uyarilar.append(f"{gn['yer']}: secici {gn['blok_sayisi']} blogu birden kapsiyor, daha dar secici kullan: {gn['sel']!r}")
    # her acilan kartin cevabindan once dusunme arasi olmali
    for k in rap["kartlar"]:
        acilis = next((i for i, ip in enumerate(ipuclari) if ip["ac"] == k["id"]), None)
        if acilis is None:
            hatalar.append(f"{k['id']}: kartin cevabi hic acilmiyor; cevabin ilk satirina {{\"ac\": \"{k['id']}\"}} ekle"); continue
        sik = [i for i, ip in enumerate(ipuclari[:acilis]) if f"#{k['id']} " in ip["sel"] + " "]
        if not any(ipuclari[i]["dur"] > 0 for i in range(sik[0] if sik else 0, acilis)):
            uyarilar.append(f"{k['id']}: soru ile cevap arasinda dusunme arasi yok; sorunun son satirina \"dur\": 4.5 ekle")
    return hatalar, uyarilar, {"parcalar": ozet, "blok": rap["blok_sayisi"], "kart": len(rap["kartlar"]), "bolumler": rap["bolumler"]}


def main():
    klasor = sys.argv[1]
    hatalar, uyarilar, ozet = denetle(klasor)
    if "--json" in sys.argv:
        print(json.dumps({"hatalar": hatalar, "uyarilar": uyarilar, "ozet": ozet}, ensure_ascii=False)); return
    if ozet:
        for ad, bas, kar, n in ozet["parcalar"]: print(f"  {ad}  {kar:5d} karakter  {n:3d} satir  {bas}")
        print(f"  sayfada {ozet['blok']} icerik blogu, {ozet['kart']} soru karti")
    for h in hatalar: print("HATA  ", h)
    for u in uyarilar: print("UYARI ", u)
    print(f"{len(hatalar)} hata, {len(uyarilar)} uyari")
    sys.exit(1 if hatalar else 0)


if __name__ == "__main__":
    main()
