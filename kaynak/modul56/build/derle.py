# kullanim: python3 -I derle.py <kitapdir> "<Baslik>"
# Kitap klasorundeki NN_*.html parcalarini birlestirir ve yer tutuculari doldurur:
#   <!--SVG:ad-->        kitapdir/svg/ad.svg
#   <!--KARTLAR:b-->     kartlar.json'daki "b" bolumunun cikmis soru kartlari
#   <!--DIZIN-->         kitaptaki butun cikmis sorularin kisa dizini
#   <!--SUREKLI-->       uc veya daha fazla sinavda gelen soru kaliplari
#   <!--YIL:b-->         "b" bolumunun (ya da * = butun kitap) yillara gore soru grafigi
# Her sorunun tam olarak bir kartta yer aldigini da denetler.
import html, json, os, re, sys
from collections import Counter, defaultdict

B = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.join(B, "..")
kitapdir, baslik = sys.argv[1], sys.argv[2]
SOR = {s["id"]: s for s in json.load(open(os.path.join(KOK, "analiz", "sorular.json"), encoding="utf-8"))}
K = json.load(open(os.path.join(kitapdir, "kartlar.json"), encoding="utf-8"))

AY = {"MSD": {"2018-2019": "2018-19", "2019": "2019-20", "2020": "2020-21", "2021-2022": "2021-22", "2022-2023": "2022-23",
              "2023-2024": "2023-24", "2024": "2024-25", "2025-2026": "2025-26"},
      "BSD": {"2019-2020": "2019-20", "2021-2022": "2021-22", "2022-2023": "2022-23", "2023-2024": "2023-24",
              "2024-2025": "2024-25", "2025-2026": "2025-26"}}
YILLAR = ["2018-19", "2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
e = lambda t: html.escape(str(t), quote=False)


def ayil(s):
    return AY[s["kaynak"]][s["yil"]]


def etiket(s):
    return f'{s["kaynak"]} {ayil(s)}' + (f' S{s["no"]}' if s["no"] is not None else "")


def sinav_sayisi(ids):
    return len({(SOR[i]["kaynak"], SOR[i]["yil"]) for i in ids})


def kaynak_satiri(ids):
    by = defaultdict(list)
    for i in ids:
        by[SOR[i]["kaynak"]].append(SOR[i])
    out = []
    for k in ("MSD", "BSD"):
        L = sorted(by.get(k, []), key=lambda s: YILLAR.index(ayil(s)), reverse=True)
        if L:
            # soru numarasi olmayan ayni sinavdaki sorular "2020-21 (2 soru)" diye birlesir
            etk = [ayil(s) + (f' S{s["no"]}' if s["no"] is not None else "") for s in L]
            say = Counter(etk)
            tek = list(dict.fromkeys(etk))
            out.append(f'<b>{k}</b> ' + ", ".join(x + (f" ({say[x]} soru)" if say[x] > 1 else "") for x in tek))
    return " · ".join(out)


def ic(t):
    """kaynak metnindeki markdown kalintilarini temizler, html'e cevirir"""
    t = t.replace("**", "").replace("*(", "(").replace(")*", ")")
    t = e(t)
    t = re.sub(r"\^([0-9+\-]+)", r"<sup>\1</sup>", t)
    return t


def kok_html(s):
    satir = [x for x in s["kok"].split("\n") if x.strip() and x.strip() != "Yorumlama:"]
    if not satir:
        return ""
    bas, geri = satir[0], satir[1:]
    h = f'<div class="q-stem">{ic(bas)}</div>'
    if geri:
        h += '<ul class="q-list">' + "".join(f"<li>{ic(x)}</li>" for x in geri) + "</ul>"
    return h


def dogru_harfler(s):
    c = (s["cevap"] or "").strip()
    return set(re.findall(r"\b([A-E])\b", c)) if re.match(r"^[A-E]\b", c) else set()


def cevap_metni(s):
    c = (s["cevap"] or "").strip()
    d = dict(s["siklar"])
    hs = dogru_harfler(s)
    if hs and d:
        return " / ".join(f"{h}) {d[h]}" for h in sorted(hs) if h in d)
    return c


def md(t):
    t = e(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", t)
    return t


def paragraflar(x):
    if isinstance(x, str):
        x = [x]
    return "".join(f"<p>{md(p)}</p>" for p in x)


def kart_html(k, bolum_no):
    ids = k["ids"]
    ana = SOR[ids[0]]
    n = sinav_sayisi(ids)
    tag = f'<span class="tag tag-accent-2">{n} sınavda soruldu</span>' if n >= 3 else (
        f'<span class="tag tag-soft">{n} sınavda soruldu</span>' if n == 2 else "")
    h = [f'<div class="qcard" id="s{k["no"].replace(".", "-")}">',
         f'<div class="q-head"><span class="q-no">Soru {k["no"]}</span>{tag}</div>',
         f'<div class="q-src">{kaynak_satiri(ids)}</div>', kok_html(ana)]
    hs = dogru_harfler(ana)
    if ana["siklar"]:
        h.append('<div class="q-opts">')
        for harf, metin in ana["siklar"]:
            ok = harf in hs
            h.append(f'<div class="q-opt{" ok" if ok else ""}"><b>{harf})</b> {ic(metin)}{" ✓" if ok else ""}</div>')
        h.append("</div>")
        if not hs:
            h.append(f'<div class="q-ans">Kaynakta cevap: {ic(ana["cevap"] or "kayıtlı değil")}</div>')
    else:
        h.append(f'<div class="q-ans">Kaynakta yalnızca cevap kayıtlı: <b>{ic(ana["cevap"] or "—")}</b></div>')
    if k.get("cevap"):
        h.append(f'<div class="q-ans">{md(k["cevap"])}</div>')
    if k.get("varyant"):
        h.append(f'<div class="q-var">{paragraflar(k["varyant"])}</div>')
    if k.get("gerekce"):
        h.append(f'<div class="q-why">{paragraflar(k["gerekce"])}</div>')
    h.append("</div>")
    return "\n".join(h)


def bolum_kartlari(b):
    return [k for k in b["kartlar"]]


BOL = {b["no"]: b for b in K["bolumler"]}


def blok(bno):
    b = BOL[bno]
    ks = bolum_kartlari(b)
    toplam = sum(len(k["ids"]) for k in ks)
    sur = sum(1 for k in ks if sinav_sayisi(k["ids"]) >= 3)
    bas = (f'<div class="qblock"><div class="qblock-title">Bu konudan çıkmış sorular</div>'
           f'<p class="qblock-note">{len(ks)} soru kalıbı, toplam {toplam} soru'
           + (f'; {sur} kalıp üç ya da daha fazla sınavda soruldu' if sur else "") + '. '
           'Yıllar arasında neredeyse aynı olan sorular tek kartta birleştirildi. Kartın üst satırı soruyu soran sınavları gösterir: '
           'MSD modül sınavı, BSD blok sonu sınavıdır. Doğru şık ✓ ile işaretlidir.</p></div>')
    return bas + '<div class="qcards">' + "\n".join(kart_html(k, bno) for k in ks) + "</div>"


def kisa(k):
    if k.get("kisa"):
        return md(k["kisa"])
    t = SOR[k["ids"][0]]["kok"].split("\n")[0].replace("**", "")
    return e(t if len(t) < 150 else t[:147].rsplit(" ", 1)[0] + "…")


def kisa_cevap(k):
    if k.get("kisa_cevap"):
        return md(k["kisa_cevap"])
    return ic(cevap_metni(SOR[k["ids"][0]]))


def yil_ozet(ids):
    c = Counter((SOR[i]["kaynak"], ayil(SOR[i])) for i in ids)
    out = []
    for kay in ("MSD", "BSD"):
        ys = sorted({y for (k2, y) in c if k2 == kay}, key=YILLAR.index)
        if ys:
            out.append(kay + " " + ", ".join(y[2:] for y in ys))
    return "; ".join(out)


def dizin():
    h = ['<table class="table compact split dizin"><thead><tr><th>No</th><th>Soru</th><th>Doğru cevap</th><th>Sınav</th></tr></thead><tbody>']
    for b in K["bolumler"]:
        h.append(f'<tr class="dizin-bolum"><td colspan="4">Bölüm {b["no"]} · {e(b["ad"])}</td></tr>')
        for k in b["kartlar"]:
            n = sinav_sayisi(k["ids"])
            h.append(f'<tr><td>{k["no"]}</td><td>{kisa(k)}</td><td>{kisa_cevap(k)}</td>'
                     f'<td class="{"sur" if n >= 3 else ""}">{n} · {yil_ozet(k["ids"])}</td></tr>')
    h.append("</tbody></table>")
    return "\n".join(h)


def surekli():
    L = [(sinav_sayisi(k["ids"]), b, k) for b in K["bolumler"] for k in b["kartlar"] if sinav_sayisi(k["ids"]) >= 3]
    L.sort(key=lambda x: (-x[0], x[2]["no"]))
    if not L:
        return '<p class="book-p">Bu kitapta üç ya da daha fazla sınavda tekrarlanan soru kalıbı yok.</p>'
    h = ['<table class="table compact split surekli"><thead><tr><th>Sınav</th><th>Soru kalıbı</th><th>Doğru cevap</th><th>Kart</th></tr></thead><tbody>']
    for n, b, k in L:
        h.append(f'<tr><td class="sur">{n}</td><td>{kisa(k)}</td><td>{kisa_cevap(k)}</td><td>{k["no"]}</td></tr>')
    h.append("</tbody></table>")
    return "\n".join(h)


def grafik(bno):
    ids = [i for b in K["bolumler"] if bno in ("*", b["no"]) for k in b["kartlar"] for i in k["ids"]]
    c = Counter((SOR[i]["kaynak"], ayil(SOR[i])) for i in ids)
    W, H = 640, 214
    x0, x1, yt, yb = 34, 630, 34, 176
    mx = max([c[(k2, y)] for k2 in ("MSD", "BSD") for y in YILLAR] + [1])
    step = 1 if mx <= 5 else 2 if mx <= 10 else 5 if mx <= 25 else 10
    top = ((mx + step - 1) // step) * step
    sy = lambda v: yb - (yb - yt) * v / top
    p = [f'<svg viewBox="0 0 {W} {H}" width="100%" style="display:block" role="img" aria-label="Yıllara göre çıkmış soru sayısı: MSD ve BSD">']
    v = 0
    while v <= top:
        y = sy(v)
        p.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="var(--color-neutral-700)" stroke-opacity="{0.45 if v == 0 else 0.15}" stroke-width="1"/>')
        p.append(f'<text x="{x0 - 6}" y="{y + 3.5:.1f}" text-anchor="end" font-family="var(--font-body)" font-size="10" fill="var(--color-neutral-700)">{v}</text>')
        v += step
    gw = (x1 - x0) / len(YILLAR)
    bw = 16
    for i, yl in enumerate(YILLAR):
        cx = x0 + gw * (i + 0.5)
        for j, (kay, renk) in enumerate((("MSD", "var(--color-accent)"), ("BSD", "var(--color-accent-2)"))):
            bx = cx - bw - 1 if j == 0 else cx + 1
            var_mi = yl in AY[kay].values()
            val = c[(kay, yl)]
            if not var_mi:
                p.append(f'<text x="{bx + bw / 2:.1f}" y="{yb - 4:.1f}" text-anchor="middle" font-family="var(--font-body)" font-size="9" fill="var(--color-neutral-700)">–</text>')
                continue
            if val > 0:
                yy = sy(val); r = min(4, (yb - yy))
                p.append(f'<path d="M{bx:.1f},{yb:.1f} L{bx:.1f},{yy + r:.1f} Q{bx:.1f},{yy:.1f} {bx + r:.1f},{yy:.1f} L{bx + bw - r:.1f},{yy:.1f} '
                         f'Q{bx + bw:.1f},{yy:.1f} {bx + bw:.1f},{yy + r:.1f} L{bx + bw:.1f},{yb:.1f} Z" fill="{renk}"/>')
            p.append(f'<text x="{bx + bw / 2:.1f}" y="{(sy(val) if val else yb) - 4:.1f}" text-anchor="middle" font-family="var(--font-body)" font-size="10" fill="var(--color-text)">{val}</text>')
        p.append(f'<text x="{cx:.1f}" y="{yb + 16:.1f}" text-anchor="middle" font-family="var(--font-body)" font-size="10.5" fill="var(--color-text)">{yl}</text>')
    lx = x1 - 250
    p.append(f'<rect x="{lx}" y="8" width="10" height="10" rx="2" fill="var(--color-accent)"/>'
             f'<text x="{lx + 15}" y="17" font-family="var(--font-body)" font-size="10.5" fill="var(--color-text)">MSD (modül sınavı)</text>')
    p.append(f'<rect x="{lx + 128}" y="8" width="10" height="10" rx="2" fill="var(--color-accent-2)"/>'
             f'<text x="{lx + 143}" y="17" font-family="var(--font-body)" font-size="10.5" fill="var(--color-text)">BSD (blok sonu)</text>')
    p.append(f'<text x="{x0}" y="{H - 6}" font-family="var(--font-body)" font-size="9.5" fill="var(--color-neutral-700)">– : o yılın sınavı arşivde yok</text>')
    p.append("</svg>")
    return "\n".join(p)


# ---------- denetim: her soru bir kez ----------
konular = set(K["konular"])
say = Counter(i for b in K["bolumler"] for k in b["kartlar"] for i in k["ids"])
eksik = sorted(i for i, s in SOR.items() if s["konu"] in konular and i not in say)
cift = sorted(i for i, n in say.items() if n > 1)
yok = sorted(i for i in say if i not in SOR)
yabanci = sorted(i for i in say if i in SOR and SOR[i]["konu"] not in konular)
if eksik or cift or yok:
    print("DENETIM HATASI\n eksik:", eksik, "\n cift:", cift, "\n bilinmeyen:", yok)
    sys.exit(1)
if yabanci:
    print("not: baska konu kodundan alinan sorular:", yabanci)

# ---------- birlestir ----------
out = open(os.path.join(B, "head_full.part"), encoding="utf-8").read().replace("__TITLE__", e(baslik))
for f in sorted(x for x in os.listdir(kitapdir) if re.match(r"^\d.*\.html$", x)):
    out += open(os.path.join(kitapdir, f), encoding="utf-8").read() + "\n"
out += open(os.path.join(B, "foot.part"), encoding="utf-8").read()
out = re.sub(r"<!--SVG:([\w-]+)-->", lambda m: open(os.path.join(kitapdir, "svg", m.group(1) + ".svg"), encoding="utf-8").read(), out)
out = re.sub(r"<!--KARTLAR:([\w.]+)-->", lambda m: blok(m.group(1)), out)
out = out.replace("<!--DIZIN-->", dizin()).replace("<!--SUREKLI-->", surekli())
out = re.sub(r"<!--YIL:([\w.*]+)-->", lambda m: grafik(m.group(1)), out)
hedef = os.path.join(kitapdir, os.path.basename(os.path.normpath(kitapdir)) + ".html")
open(hedef, "w", encoding="utf-8").write(out)
nk = sum(len(b["kartlar"]) for b in K["bolumler"])
print("HTML:", hedef, "| kart", nk, "| soru", sum(say.values()))
