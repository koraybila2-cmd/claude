# Basit metin -> Broadsheet HTML -> PDF.
# Bicim: "= baslik", "~ alt baslik", "# bolum | giris", "## alt baslik", "### kucuk baslik", paragraf,
# "- madde", "1. madde", "| a | b" tablo (ilk satir baslik), "|= tablo aciklamasi",
# "!! metin" (sinav notu kutusu), "?? metin" (ezber ipucu kutusu), "@SVG dosya.svg" (sekil), "@SEKIL aciklama".
# Satir ici: **kalin**, _italik_, <sub>, <sup>.
# Ek: "@EKLE dosya" (baska bicim dosyasini araya alir), soru kartlari: "@QB kisim basligi", "@Q baslik | rozet | etiket",
# "@K kok", "A) sik ✓", "@O onceki yillar", aciklama paragraflari, "@@"; "@E eski soru maddesi".
# kullanim: python3 -I uret.py girdi.txt cikti.html "kicker"
import html, re, sys
src, outp, kicker = sys.argv[1:4]
B = "/home/user/claude/kaynak/modul56/build"
import os
K = os.path.dirname(os.path.abspath(__file__))
SVG = K + "/svg"

def ic(t):
    t = html.escape(t, quote=False)
    for a in ("sub", "sup"): t = t.replace(f"&lt;{a}&gt;", f"<{a}>").replace(f"&lt;/{a}&gt;", f"</{a}>")
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return re.sub(r"(?<![\w*])_(.+?)_(?![\w])", r"<em>\1</em>", t)

def oku(p):
    r = []
    for s in open(p, encoding="utf-8").read().split("\n"):
        if s.startswith("@EKLE "): r += oku(os.path.join(K, s[6:].strip()))
        else: r.append(s)
    return r
L = oku(src)
QB = {"BU YILIN": "Bu yılın soruları (2026-27)", "GEÇEN YILIN MSD": "Geçen yılın MSD soruları (2025-26)", "GEÇEN YILIN BLOK": "Geçen yılın blok sınavı (2025-26)", "DAHA ESKİ": "Daha eski sorular"}
def kart(i):
    bas, rozet, etiket = [x.strip() for x in (L[i][3:] + " | | ").split("|")[:3]]
    cls = "tag-accent-2" if rozet == "BU YIL" else "tag-soft"
    h = [f'<div class="qcard"><div class="q-head"><span class="q-no">{ic(bas)}</span>' + (f'<span class="tag {cls}">{ic(rozet.capitalize())}</span>' if rozet else "") + "</div>"]
    if etiket: h.append(f'<div class="q-src">{ic(etiket.capitalize() if False else etiket)}</div>')
    i += 1; kok, sik, onc, ac = [], [], "", []
    while L[i].strip() != "@@":
        t = L[i].strip(); i += 1
        if t.startswith("@K "): kok.append(t[3:])
        elif t.startswith("@O "): onc = t[3:]
        elif re.match(r"^[A-E]\) ", t) and not ac and not onc: sik.append(t)
        elif t: ac.append(t)
    h.append('<div class="q-stem">' + "<br>".join(ic(k) for k in kok) + "</div>")
    h.append('<div class="q-opts">' + "".join(f'<div class="q-opt{" ok" if "✓" in t else ""}"><b>{t[:2]}</b>{ic(t[2:])}</div>' for t in sik) + "</div>")
    if onc: h.append(f'<div class="q-var">{ic(onc)}</div>')
    if ac:
        ilk = re.sub(r"^(.+?\.)( |$)", r"**\1** ", ac[0], count=1) if not ac[0].startswith("**") else ac[0]
        h.append('<div class="q-why">' + "".join(f"<p>{ic(p)}</p>" for p in [ilk] + ac[1:]) + "</div>")
    h.append("</div>")
    return "\n".join(h), i + 1
out, liste, title, byline, n_ch, n_sec = [], None, "", "", 0, 0
def kapat():
    global liste
    if liste: out.append(f"</{liste}>"); liste = None
i = 0
while i < len(L):
    s = L[i].strip(); i += 1
    if not s: kapat(); continue
    if s.startswith("= "): title = s[2:]; continue
    if s.startswith("~ "): byline = s[2:]; continue
    if s.startswith("# "):
        kapat(); t, _, lead = s[2:].partition(" | "); n_ch += 1; n_sec = 0
        if n_ch > 1: out.append("</section>")
        out.append(f'<section class="chapter"><p class="chapter-kicker">{ic(kicker)}</p><h2 class="chapter-title">{ic(t)}</h2>'
                   + (f'<p class="chapter-lead">{ic(lead)}</p>' if lead else "")); continue
    if s.startswith("### "): kapat(); out.append(f'<h4 class="book-h4">{ic(s[4:])}</h4>'); continue
    if s.startswith("## "): kapat(); n_sec += 1; out.append(f'<h3 class="book-h3">{ic(s[3:])}</h3>'); continue
    if s.startswith("!! ") or s.startswith("?? "):
        kapat(); tag = "Sınav notu" if s.startswith("!!") else "Ezber ipucu"
        cls = "tag-accent-2" if s.startswith("!!") else "tag-soft"
        out.append(f'<div class="hl-block"><p class="highlight-tag"><span class="tag {cls}">{tag}</span></p><p class="highlight-p">{ic(s[3:])}</p></div>'); continue
    if s.startswith("@QB "):
        kapat(); ad = next((v for k, v in QB.items() if s[4:].startswith(k)), s[4:])
        out.append(f'<div class="qblock"><p class="qblock-title">{ic(ad)}</p></div>'); continue
    if s.startswith("@Q "):
        kapat(); h, i = kart(i - 1); out.append(h); continue
    if s.startswith("@E "):
        if liste != "ul": kapat(); out.append('<ul class="book-list" style="font-size:0.86rem">'); liste = "ul"
        out.append(f"<li>{ic(s[3:])}</li>"); continue
    if s.startswith("@SVG "):
        kapat(); svg = open(f"{SVG}/{s[5:].strip()}", encoding="utf-8").read()
        cap = ""
        if i < len(L) and L[i].strip().startswith("@SEKIL "): cap = L[i].strip()[7:]; i += 1
        out.append(f'<figure class="chart-figure">{svg}' + (f'<figcaption class="chart-caption">{ic(cap)}</figcaption>' if cap else "") + "</figure>"); continue
    if s.startswith("|"):
        kapat(); rows = [s]
        while i < len(L) and L[i].strip().startswith("|"): rows.append(L[i].strip()); i += 1
        cap = rows.pop()[2:].strip() if rows[-1].startswith("|=") else ""
        cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
        t = ['<table class="table compact split"><thead><tr>' + "".join(f"<th>{ic(c)}</th>" for c in cells[0]) + "</tr></thead><tbody>"]
        t += ["<tr>" + "".join(f"<td>{ic(c)}</td>" for c in r) + "</tr>" for r in cells[1:]]
        t.append("</tbody></table>")
        if cap: t.append(f'<p class="chart-caption">{ic(cap)}</p>')
        out.append("\n".join(t)); continue
    m = re.match(r"(\d+)\. (.*)", s)
    if m:
        if liste != "ol": kapat(); out.append('<ol class="book-list">'); liste = "ol"
        out.append(f"<li>{ic(m.group(2))}</li>"); continue
    if s.startswith("- "):
        if liste != "ul": kapat(); out.append('<ul class="book-list">'); liste = "ul"
        out.append(f"<li>{ic(s[2:])}</li>"); continue
    kapat(); out.append(f'<p class="book-p">{ic(s)}</p>')
kapat()
if n_ch: out.append("</section>")
head = open(f"{B}/head_full.part", encoding="utf-8").read().replace("__TITLE__", html.escape(title))
ust = (f'<p class="book-kicker">{ic(kicker)}</p><h1 class="book-title">{ic(title)}</h1><p class="book-byline">{ic(byline)}</p>') if title else ""
open(outp, "w", encoding="utf-8").write(head + ust + "\n".join(out) + "\n</main></body></html>")
