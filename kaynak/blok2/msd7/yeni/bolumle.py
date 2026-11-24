import json, re, collections
d = {f'{o["yil"]}-{o["no"]}': o for o in json.load(open("yeni/sorular.json", encoding="utf-8"))}
K = json.load(open("yeni/kumeler.json"))
def tum(o): return (" ".join(o["kok"]) + " " + " ".join(s for _, s in o["sik"]) + " " + o["cevap_metin"]).lower()
KUR = [
 (9, r"antihelmint|ilaç|tedavi.*(enfestasyon|teniaz)|prazik|praziq|albendazol|mebendazol|pirantel|niklozamid|ivermektin|metrifonat|piperazin|levamizol|dietilkarbamazin|benzimidazol|triklabendazol"),
 (2, r"dehidratasyon|ors\b|ağızdan sıvı|parenteral sıvı|sıvı tedavi"),
 (3, r"su ve (besin|gıda)|gıda kaynaklı|besin kaynaklı|içme ve kullanma|filyasyon|enfeksiyon zincir|karantina"),
 (4, r"mikrobiyot|mikrobiyom|bifido|firmicutes|lactobacillus|bacteroides|kısa zincirli yağ|helicobacter|nf-kappa"),
 (8, r"sestod|taenia|tenya|hymenolep|diphyllobot|echinococ|trematod|fasciol|cysticerc|schistosom|kapaklı yumurta|cüce"),
 (7, r"nematod|ascaris|askaris|enterobius|trichuris|strongyloid|necator|ancylost|anemi yapan helmint|larva göçü|rabd"),
 (6, r"protozo|entamoeba|e\. h[iy]stolytica|giardia|cryptospor|isospora|cyclospora|balantid|dientamoeba|chilomastix|microspor|vittaforma|trichomonas|amip|string test|sporozo|coccidi"),
 (5, r"salmonella|shigella|coli|vibrio|campylobacter|yersinia|listeria|aeromonas|clostridium|bacillus|aureus|besiyeri|agar|tsi|toksin|enterobacter|oksidaz|üreaz|botulin|gaita kültür|gayta kültür|norovir|norwalk|rotavir|adenovir|katalaz"),
 (1, r".*"),
]
atama = []
for g in K:
    o = d[g[0]]; t = tum(o)
    b = next(n for n, r in KUR if re.search(r, t))
    atama.append(dict(bolum=b, sorular=g))
c = collections.Counter(a["bolum"] for a in atama)
print(sorted(c.items()), "| soru:", sorted(collections.Counter({}).items()))
json.dump(atama, open("yeni/atama.json", "w"), ensure_ascii=False, indent=0)
for b in range(1, 10):
    print(f"== {b}:", " ".join("/".join(x[2:4] + "-" + x.split("-")[-1] for x in a["sorular"]) for a in atama if a["bolum"] == b))
# --- elle duzeltmeler ve yeni bolum numaralari ---
# 1 yaklasim/klinik/viral, 2 dehidratasyon, 3 su-besin, 4 mikrobiyota, 5 Enterobacteriaceae+lab, 6 diger bakteriler/toksin, 7 protozoon, 8 nematod, 9 sestod-trematod, 10 ilaclar
ELLE = {"2025-26-10": 3, "2025-26-43": 5, "2020-21-31": 5, "2019-20-42": 5, "2025-26-1": 6, "2025-26-2": 1,
        "2023-24-9": 1, "2023-24-10": 1, "2022-23-3": 1, "2021-22-8": 1, "2020-21-29": 1, "2020-21-43": 1, "2020-21-11": 1,
        "2024-25-46": 1, "2024-25-1": 1, "2024-25-4": 1, "2023-24-38": 1, "2022-23-50": 1, "2019-20-38": 1, "2019-20-39": 1,
        "2024-25-3": 1, "2021-22-7": 1, "2020-21-12": 8, "2020-21-37": 1, "2025-26-38": 7, "2022-23-22": 8, "2019-20-26": 8,
        "2019-20-31": 7, "2023-24-31": 7, "2023-24-33": 7, "2022-23-39": 6, "2025-26-37": 6, "2025-26-4": 1, "2021-22-9": 1}
ESKI2YENI = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 7, 7: 8, 8: 9, 9: 10}
ENTERO = r"salmonella|shigella|coli|yersinia|tsi|emb|hektoen|besiyeri|agar|enterobacter|kauffmann|vi antijen|o antijen|tifo|typhi|üreaz"
for a in atama:
    k = a["sorular"][0]
    if k in ELLE: a["bolum"] = ELLE[k]; continue
    b = ESKI2YENI[a["bolum"]]
    if b == 5 and not re.search(ENTERO, tum(d[k])): b = 6
    a["bolum"] = b
atama = [a for a in atama if a["sorular"][0] != "2021-22-33"]
json.dump(atama, open("yeni/atama.json", "w"), ensure_ascii=False, indent=0)
c = collections.Counter(a["bolum"] for a in atama); s = collections.Counter(); [s.update({a["bolum"]: len(a["sorular"])}) for a in atama]
print("YENI:", sorted(c.items()), "soru:", sorted(s.items()))
for b in range(1, 11):
    print(f"== {b}:", " ".join("/".join(x[2:4] + "-" + x.split("-")[-1] for x in a["sorular"]) for a in atama if a["bolum"] == b))
