# Sorulari benzerlige gore kumeler ve konuya atar -> yeni/kumeler.json
import json, re, math, collections, sys
d = json.load(open("yeni/sorular.json", encoding="utf-8"))
def tok(t):
    w = re.findall(r"[a-zçğıöşü0-9]+", t.lower().replace("İ", "i").replace("I", "ı"))
    w = [x[:6] for x in w if len(x) > 2]
    return collections.Counter(w + [a + "_" + b for a, b in zip(w, w[1:])])
def metin(o):
    a = dict(o["sik"]).get(o["cevap"], "") if o["cevap"] else o["cevap_metin"]
    return " ".join(o["kok"]) + " || " + a
V = [tok(metin(o)) for o in d]
df = collections.Counter(); [df.update(set(v)) for v in V]; N = len(V)
def vec(c):
    v = {k: (1 + math.log(n)) * math.log((1 + N) / (1 + df[k])) for k, n in c.items()}; z = math.sqrt(sum(x * x for x in v.values())) or 1
    return {k: x / z for k, x in v.items()}
W = [vec(c) for c in V]
def sim(i, j): a, b = W[i], W[j]; return sum(x * b.get(k, 0) for k, x in a.items())
par = list(range(N))
def f(x):
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
for i in range(N):
    for j in range(i + 1, N):
        if d[i]["sinav"] != d[j]["sinav"] and sim(i, j) >= float(sys.argv[1] if len(sys.argv) > 1 else 0.55): par[f(i)] = f(j)
K = collections.defaultdict(list)
for i in range(N): K[f(i)].append(i)
kum = sorted(K.values(), key=lambda g: min(g))
print(len(kum), "kume;", sum(len(g) > 1 for g in kum), "tekrarli;", max(len(g) for g in kum), "en buyuk")
json.dump([[d[i]["yil"] + "-" + str(d[i]["no"]) for i in g] for g in kum], open("yeni/kumeler.json", "w"), ensure_ascii=False)
for g in kum:
    if len(g) > 1: print(len(g), [d[i]["yil"][2:4] + "-" + str(d[i]["no"]) for i in g], " ".join(d[g[0]]["kok"])[:60])
