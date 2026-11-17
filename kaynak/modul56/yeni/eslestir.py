# 2026-27 MSD 5-6 sorularini kitaptaki eski kartlarla (2025-26, 2024-25, BSD 2025-26) ve BSD-1 arsiviyle esler.
# kullanim: python3 -I eslestir.py sorular.md m56.txt bsd.tsv
import re, sys, json
import math, collections
def tok(t):
    w = re.findall(r"[a-zçğıöşü0-9]+", t.lower().replace("İ", "i").replace("I", "ı"))
    w = [x[:6] for x in w if len(x) > 2]
    return w + [a + "_" + b for a, b in zip(w, w[1:])]
class TfidfVectorizer:
    def fit(self, docs):
        df = collections.Counter(); [df.update(set(tok(d))) for d in docs]; N = len(docs)
        self.idf = {k: math.log((1 + N) / (1 + v)) + 1 for k, v in df.items()}; return self
    def transform(self, docs):
        r = []
        for d in docs:
            c = collections.Counter(tok(d)); v = {k: (1 + math.log(n)) * self.idf.get(k, 1) for k, n in c.items()}
            z = math.sqrt(sum(x * x for x in v.values())) or 1; r.append({k: x / z for k, x in v.items()})
        return r
def cosine_similarity(q, D): return [[sum(x * d.get(k, 0) for k, x in q[0].items()) for d in D]]
md, kt, bsd = sys.argv[1:4]
Y = open(md, encoding="utf-8").read()
yeni = []
for m in re.finditer(r"\*\*(\d+)\. (.+?)\*\*\n(.*?)\*\*Doğru Şık:\*\* ([A-E])", Y, re.S):
    n, kok, govde, c = int(m.group(1)), m.group(2), m.group(3), m.group(4)
    sik = re.findall(r"^- ([A-E])\) (.*)$", govde, re.M)
    onc = [l.strip() for l in govde.split("\n") if re.match(r"^\s*[IVX]+[-.]", l)]
    yeni.append(dict(no=n, kok=kok, sik=sik, onc=onc, cevap=c))
T = open(kt, encoding="utf-8").read().split("\n")
eski, cur = [], None
for s in T:
    s = s.strip()
    m = re.match(r"^MODÜL 5-6 (\d{4}-\d{2}) · SORU( \d+)?$", s) or re.match(r"^(BSD-1 \d{4}-\d{2}) · SORU( \d+)?$", s)
    if m:
        cur = dict(etiket=s, metin=[]); eski.append(cur); continue
    if cur is not None: cur["metin"].append(s)
for e in eski:
    t = " ".join(e["metin"]); e["onceki"] = (re.search(r"Önceki yıllar: (.*?)(?=  | [A-E] (doğru|yanlış))", t) or re.search(r"Önceki yıllar: ([^.]*\.)", t) or [None, ""])[1] if "Önceki yıllar" in t else ""
    e["kisa"] = t[:400]
import csv
B = list(csv.DictReader(open(bsd, encoding="utf-8"), delimiter="\t"))
B = [b for b in B if b["Modül"] == "Modül 5-6"]
docs = [e["kisa"] for e in eski] + [b["Soru kökü"] for b in B]
lab = [e["etiket"] for e in eski] + [f'BSD {b["Yıl"]} S{b["Soru"]}' for b in B]
v = TfidfVectorizer().fit(docs + [y["kok"] for y in yeni])
D = v.transform(docs)
out = {}
for y in yeni:
    q = v.transform([y["kok"] + " " + " ".join(s for _, s in y["sik"])])
    sc = cosine_similarity(q, D)[0]
    top = sorted(range(len(sc)), key=lambda i: -sc[i])[:3]
    out[y["no"]] = [(lab[i], round(float(sc[i]), 2), (eski[i]["onceki"] if i < len(eski) else "")) for i in top]
    print(y["no"], y["cevap"], y["kok"][:70])
    for l, s_, o in out[y["no"]]: print("      ", s_, l, "|", o[:110])
json.dump(dict(yeni=yeni, eslesme=out), open("yeni/eslesme.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(yeni), "yeni soru,", len(eski), "eski kart,", len(B), "BSD M5-6 sorusu")
