# bolumdeki kumeleri okunur bicimde dok: python3 -I yeni/dok.py BOLUM
import json, sys
d = {f"{q['yil']}-{q['no']}": q for q in json.load(open("yeni/sorular.json"))}
b = int(sys.argv[1])
for a in json.load(open("yeni/atama.json")):
    if a["bolum"] != b: continue
    k = a["sorular"]; q = d[k[0]]
    print(f"### {' / '.join(k)}")
    print(" ".join(q["kok"])[:700])
    for h, t in q["sik"]: print(f"  {h}) {t[:150]}" + (" ✓" if h == q["cevap"] else ""))
    if not q["sik"] or not q["cevap"]: print("  CEVAP:", q["cevap"], q["cevap_metin"][:300])
    for x in k[1:]:
        r = d[x]
        if r["cevap"] != q["cevap"] or not r["sik"]:
            print(f"  [{x}] cev={r['cevap']}", "|", " ".join(r['kok'])[:120], "|", next((t for h, t in r["sik"] if h == r["cevap"]), r["cevap_metin"])[:100])
