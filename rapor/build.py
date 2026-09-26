#!/usr/bin/env python3
"""Bölüm Markdown dosyalarını tek bir kitap HTML'ine dönüştürür.

Kullanım: python3 build.py [--pages pages.json] [--out rapor.html]
--pages verilmezse içindekiler sayfa numaraları yer tutucu olur ve başlıklara
sayfa eşleme işaretleri (.pm) eklenir; pagemap.py bu işaretlerden pages.json üretir.
"""
import argparse
import json
import re
from pathlib import Path

import markdown
from bs4 import BeautifulSoup, NavigableString

ROOT = Path(__file__).resolve().parent
BOLUMLER = ROOT / "bolumler"
SOZLUK = ROOT / "sozluk"

PARTS = [
    ("Kısım I", "Temeller", "Bilimsel kanıtı okumayı ve kasın nasıl büyüyüp güçlendiğini anlamak.", ["01", "02"]),
    ("Kısım II", "Ağırlık Antrenmanı", "Hacimden tükenişe, egzersiz seçiminden periyotlamaya kadar direnç antrenmanının tüm değişkenleri.", ["03", "04", "05", "06", "07", "08", "09"]),
    ("Kısım III", "Kardiyo, Futbol ve Koşu Sakatlıkları", "Kardiyorespiratuvar fizyoloji, kardiyo programlama ve lateral baldır ağrısının yönetimi.", ["10", "11", "12"]),
    ("Kısım IV", "Beslenme ve Takviyeler", "Enerji dengesi, protein, diğer makro ve mikro besinler, kreatin ve diğer takviyeler.", ["13", "14", "15", "16", "17"]),
    ("Kısım V", "Toparlanma ve Yaşam Tarzı", "Uyku, toparlanma, esneklik, ilerleme takibi ve sürdürülebilirlik.", ["18"]),
    ("Kısım VI", "Uygulama Rehberi", "Tüm bu kanıtların sana özel bir antrenman, kardiyo ve beslenme planına dönüştürülmesi.", ["19"]),
    ("Ekler", "Başvuru Bölümleri", "Mitler ve gerçekler, formüller ve tablolar, terimler sözlüğü.", ["EA", "EB", "EC"]),
]

CALLOUTS = {
    "TERİM": ("term", "Kavram"), "TERIM": ("term", "Kavram"), "KAVRAM": ("term", "Kavram"),
    "PRATİK": ("practice", "Pratikte"), "PRATIK": ("practice", "Pratikte"), "UYGULAMA": ("practice", "Pratikte"),
    "DİKKAT": ("warn", "Dikkat"), "DIKKAT": ("warn", "Dikkat"), "UYARI": ("warn", "Dikkat"),
    "MİT": ("myth", "Yaygın yanılgı"), "MIT": ("myth", "Yaygın yanılgı"), "YANILGI": ("myth", "Yaygın yanılgı"),
    "ÖZET": ("summary", "Bölüm özeti"), "OZET": ("summary", "Bölüm özeti"),
    "SENİN İÇİN": ("you", "Senin için"), "SENIN ICIN": ("you", "Senin için"), "SENİN İÇİN:": ("you", "Senin için"),
    "ÇALIŞMA": ("study", "Çalışma kutusu"), "CALISMA": ("study", "Çalışma kutusu"),
    "KANIT": ("evidence", "Kanıt notu"), "KANIT NOTU": ("evidence", "Kanıt notu"),
}

EV_LABEL = {"A": "Kanıt A", "B": "Kanıt B", "C": "Kanıt C", "D": "Kanıt D"}

TR_ALPHABET = "aâbcçdefgğhıiîjklmnoöpqrsştuûüvwxyz"
TR_INDEX = {c: i for i, c in enumerate(TR_ALPHABET)}


def tr_lower(s):
    return s.replace("I", "ı").replace("İ", "i").lower()


def tr_upper(s):
    return s.replace("i", "İ").replace("ı", "I").upper()


def tr_key(s):
    s = tr_lower(re.sub(r"^[^\wçğıöşüÇĞİÖŞÜ]+", "", s))
    return [-1 if c in " -/()" else TR_INDEX.get(c, 100 + ord(c)) for c in s]


def chapter_files():
    files = {}
    for p in sorted(BOLUMLER.glob("*.md")):
        key = p.name.split("-", 1)[0]
        files.setdefault(key, []).append(p)
    return files


def md_to_soup(text):
    html = markdown.markdown(text, extensions=["tables", "sane_lists", "attr_list", "md_in_html"], output_format="html5")
    return BeautifulSoup(html, "html.parser")


RE_EV = re.compile(r"\[\[\s*([ABCD])\s*\]\]")
RE_CITE = re.compile(r"\[(\d{1,3}(?:\s*[,–\-]\s*\d{1,3})*)\]")
RE_VO2 = re.compile(r"\bVO2(?=max|peak|maks|zirve|\b)")


def replace_in_text(soup, root, in_refs=False):
    for node in list(root.find_all(string=True)):
        if not isinstance(node, NavigableString) or node.parent is None:
            continue
        if node.parent.name in ("a", "code", "script", "style") or node.find_parent("a"):
            continue
        text = str(node)
        new = text
        new = RE_EV.sub(lambda m: f'<span class="ev ev-{m.group(1).lower()}">{EV_LABEL[m.group(1)]}</span>', new)
        if not in_refs and not node.find_parent(class_="refs"):
            new = RE_CITE.sub(lambda m: f'<span class="cite-n">[{m.group(1)}]</span>', new)
        new = RE_VO2.sub("VO<sub>2</sub>", new)
        if new != text:
            escaped_parts = []
            last = 0
            # yeniden kaçışlı HTML üret: yalnız bizim eklediğimiz etiketler ham kalsın
            for m in re.finditer(r'<span class="(?:ev ev-[abcd]|cite-n)">.*?</span>|<sub>2</sub>', new):
                escaped_parts.append(escape_html(new[last:m.start()]))
                escaped_parts.append(m.group(0))
                last = m.end()
            escaped_parts.append(escape_html(new[last:]))
            frag = BeautifulSoup("".join(escaped_parts), "html.parser")
            node.replace_with(frag)


def escape_html(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def convert_callouts(soup):
    for bq in soup.find_all("blockquote"):
        first = bq.find("p")
        if not first or not first.contents:
            continue
        head = first.contents[0]
        if getattr(head, "name", None) != "strong":
            continue
        raw = head.get_text().strip()
        label, _, title = raw.partition(":")
        key = tr_upper(label.strip())
        if key not in CALLOUTS:
            continue
        cls, kicker = CALLOUTS[key]
        title = title.strip()
        head.extract()
        # baştaki ":" ve boşluğu temizle
        if first.contents and isinstance(first.contents[0], NavigableString):
            first.contents[0].replace_with(NavigableString(re.sub(r"^\s*:?\s*", "", str(first.contents[0]))))
        div = soup.new_tag("div", attrs={"class": f"callout {cls}"})
        k = soup.new_tag("div", attrs={"class": "k"})
        k.string = kicker + (f" · {title}" if title else "")
        div.append(k)
        for child in list(bq.contents):
            div.append(child.extract())
        # boş kalan ilk paragrafı sil
        fp = div.find("p")
        if fp is not None and not fp.get_text(strip=True) and not fp.find(True):
            fp.decompose()
        bq.replace_with(div)


def wrap_tables(soup):
    for t in soup.find_all("table"):
        cols = len(t.find("tr").find_all(["th", "td"])) if t.find("tr") else 0
        if cols >= 5:
            t["class"] = t.get("class", []) + ["small"]
        wrap = soup.new_tag("div", attrs={"class": "table-wrap"})
        t.wrap(wrap)


def marker(soup, mid, with_markers):
    if not with_markers:
        return None
    s = soup.new_tag("span", attrs={"class": "pm"})
    s.string = f"ZQ{mid}QZ"
    return s


def process_chapter(key, paths, label, number_prefix, with_markers, toc):
    text = "\n\n".join(p.read_text(encoding="utf-8") for p in paths)
    soup = md_to_soup(text)
    h1 = soup.find("h1")
    title = h1.get_text().strip() if h1 else key
    if h1:
        h1.decompose()
    cid = f"c{key.lower()}"
    toc.append(("ch", cid, label, title))

    s_idx = 0
    ss_idx = 0
    in_refs = False
    for h in soup.find_all(["h2", "h3"]):
        txt = h.get_text().strip()
        if h.name == "h2":
            if tr_lower(txt).startswith("kaynak"):
                in_refs = True
                h["class"] = ["refs-h"]
                h["id"] = f"{cid}-ref"
                nxt = h.find_next_sibling(["ol", "ul"])
                if nxt is not None:
                    nxt["class"] = ["refs"]
                continue
            in_refs = False
            s_idx += 1
            ss_idx = 0
            num = f"{number_prefix}.{s_idx}"
            sid = f"{cid}s{s_idx}"
            h["id"] = sid
            sn = soup.new_tag("span", attrs={"class": "sn"})
            sn.string = num
            h.insert(0, sn)
            m = marker(soup, sid, with_markers)
            if m:
                h.insert(0, m)
            toc.append(("sec", sid, num, txt))
        else:
            if in_refs or s_idx == 0:
                continue
            ss_idx += 1
            sn = soup.new_tag("span", attrs={"class": "sn"})
            sn.string = f"{number_prefix}.{s_idx}.{ss_idx}"
            h.insert(0, sn)

    for lst in soup.find_all(class_="refs"):
        replace_in_text(soup, lst, in_refs=True)
    replace_in_text(soup, soup)
    convert_callouts(soup)
    wrap_tables(soup)

    mk = f'<span class="pm">ZQ{cid}QZ</span>' if with_markers else ""
    return (f'<section class="chapter" id="{cid}"><div class="chapter-head"><div class="ck">{escape_html(label)}</div>'
            f'<h1>{mk}{escape_html(title)}</h1></div>{soup}</section>')


def build_glossary(with_markers, toc):
    entries = {}
    for p in sorted(SOZLUK.glob("*.md")) if SOZLUK.exists() else []:
        for line in p.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\s*[-*]\s*\*\*(.+?)\*\*\s*[:—–-]+\s*(.+?)\s*$", line)
            if not m:
                continue
            term, definition = m.group(1).strip().rstrip(":"), m.group(2).strip()
            k = tr_lower(term)
            if k not in entries or len(definition) > len(entries[k][1]):
                entries[k] = (term, definition)
    if not entries:
        return ""
    items = sorted(entries.values(), key=lambda e: (0 if e[0][:1].isdigit() else 1, tr_key(e[0])))
    cid = "cec"
    toc.append(("ch", cid, "Ek C", "Terimler Sözlüğü"))
    out = [f'<section class="chapter glossary" id="{cid}"><div class="chapter-head"><div class="ck">Ek C</div><h1>']
    if with_markers:
        out.append(f'<span class="pm">ZQ{cid}QZ</span>')
    out.append("Terimler Sözlüğü</h1></div>")
    out.append('<p>Raporda geçen teknik terimlerin kısa açıklamaları. Terimler ilk geçtikleri bölümde daha ayrıntılı anlatılmıştır; burası hızlı başvuru içindir.</p><dl>')
    letter = None
    for term, definition in items:
        first = tr_upper(tr_lower(term)[:1]) if term else ""
        if first.isdigit():
            first = "0–9"
        if first != letter and (first.isalpha() or first == "0–9"):
            letter = first
            out.append(f'<div class="letter">{escape_html(letter)}</div>')
        d = md_to_soup(definition)
        replace_in_text(d, d)
        dd = "".join(str(c) for c in (d.p.contents if d.p else d.contents))
        out.append(f"<dt>{escape_html(term)}</dt><dd>{dd}</dd>")
    out.append("</dl></section>")
    return "".join(out)


FRONT = """
<section class="front">
  <h1>Bu doküman hakkında</h1>
  <p class="lead">Bu rapor, direnç (ağırlık) antrenmanı, kardiyo, beslenme ve takviyeler hakkındaki güncel bilimsel literatürün kapsamlı bir sentezidir. Amaç, konuyu basitleştirmeden ama her teknik kavramı açıklayarak, "neden" sorusunun yanıtıyla birlikte anlatmak; ardından tüm bu kanıtları sana özel, uygulanabilir bir plana dönüştürmektir.</p>
  <h2 style="font-size:13pt;margin:7mm 0 2mm 0">Nasıl hazırlandı?</h2>
  <p>Literatür, Eylül 2026 itibarıyla PubMed ve akademik arama motorları üzerinden taranmıştır. Öncelik sırasıyla şemsiye derlemeler, meta-analizler ve ağ meta-analizleri, büyük ve iyi tasarlanmış randomize kontrollü çalışmalar (RKÇ) ve uluslararası kuruluşların pozisyon bildirileri/uzlaşı raporları (ACSM, ISSN, IOC, NSCA, EFSA, WHO vb.) kullanılmıştır. Daha eski "klasik" çalışmalar yalnızca hâlâ en iyi kanıt olduklarında ve bu durum belirtilerek aktarılmıştır. Her bölümün sonunda o bölümde atıf yapılan kaynakların tam listesi vardır; metindeki köşeli parantezli numaralar <span class="cite-n">[1]</span> bu listeye işaret eder.</p>
  <h2 style="font-size:13pt;margin:7mm 0 2mm 0">Kanıt düzeyi rozetleri</h2>
  <p>Önemli önerilerin yanında, o önerinin dayandığı kanıtın gücünü gösteren bir rozet bulunur. Sınıflama GRADE yaklaşımından uyarlanmıştır (ayrıntılar Bölüm 1'de):</p>
  <div class="legend">
    <div><span class="ev ev-a">Kanıt A</span></div><div><strong>Yüksek.</strong> Birden fazla iyi kaliteli meta-analiz veya büyük RKÇ ile tutarlı biçimde desteklenir. Yeni çalışmaların sonucu değiştirmesi olası değildir.</div>
    <div><span class="ev ev-b">Kanıt B</span></div><div><strong>Orta.</strong> Meta-analiz veya birkaç RKÇ destekler, ancak çalışma sayısı sınırlı, sonuçlar kısmen heterojen ya da popülasyon sana tam uymuyor olabilir.</div>
    <div><span class="ev ev-c">Kanıt C</span></div><div><strong>Düşük.</strong> Az sayıda veya küçük çalışmalar, kısa süreli/akut ölçümler (ör. tek seanslık kas protein sentezi), gözlemsel veriler ya da dolaylı kanıt.</div>
    <div><span class="ev ev-d">Kanıt D</span></div><div><strong>Çok düşük / uzman görüşü.</strong> Doğrudan veri yok; fizyolojik akıl yürütme, başka popülasyonlardan çıkarım veya uygulayıcı deneyimi.</div>
  </div>
  <h2 style="font-size:13pt;margin:7mm 0 2mm 0">Kutular</h2>
  <div class="callout term"><div class="k">Kavram</div><p>Teknik bir terimin ya da mekanizmanın açıklaması.</p></div>
  <div class="callout practice"><div class="k">Pratikte</div><p>Bilginin antrenmana veya sofraya nasıl çevrileceği.</p></div>
  <div class="callout myth"><div class="k">Yaygın yanılgı</div><p>Yaygın bir inanışın kanıt karşısındaki durumu.</p></div>
  <div class="callout warn"><div class="k">Dikkat</div><p>Güvenlik, sağlık veya yorum hatası riski taşıyan noktalar.</p></div>
  <div class="callout you"><div class="k">Senin için</div><p>173 cm, 98 kg, yeniden başlamış, yağ kaybı ve üst vücut hipertrofisi hedefleyen, bacaklarının büyümesini istemeyen, futbol oynayan ve koşarken lateral baldır ağrısı yaşayan bir okura özel çıkarımlar.</p></div>
  <div class="callout warn"><div class="k">Tıbbi uyarı</div><p>Bu rapor eğitim amaçlıdır ve bir hekim, fizyoterapist ya da diyetisyenin bireysel değerlendirmesinin yerini tutmaz. Özellikle ağrı, sakatlık, kronik hastalık (ör. hipertansiyon, böbrek hastalığı, diyabet) veya ilaç kullanımı durumunda antrenman ve beslenme değişikliklerini bir sağlık profesyoneliyle birlikte planla. Kırmızı bayrak belirtileri ilgili bölümlerde ayrıca belirtilmiştir.</p></div>
</section>
"""

COVER = """
<section class="cover">
  <div class="bar"></div>
  <div class="kicker">Kanıta dayalı kapsamlı rehber · Eylül 2026</div>
  <h1>Ağırlık Antrenmanı, Kardiyo ve Beslenme<br><em>Güncel Bilimsel Literatürün Sentezi</em></h1>
  <div class="sub">Hipertrofi ve kuvvetten VO<sub>2</sub>max'a, koşu sakatlıklarından proteine ve kreatine kadar; kanıt düzeyleriyle derlenmiş, terimleri açıklanmış bir başvuru kitabı ve kişiye özel uygulama rehberi.</div>
  <div class="scope">
    <div>Kasın nasıl büyüdüğü ve güçlendiği</div>
    <div>Hacim, frekans, yük, tükeniş, dinlenme</div>
    <div>Egzersiz seçimi ve teknik</div>
    <div>Büyümeden güçlenmek</div>
    <div>VO<sub>2</sub>max, yoğunluk bölgeleri, HIIT</div>
    <div>Futbol kondisyonu</div>
    <div>Lateral baldır ağrısı ve koşuya dönüş</div>
    <div>Enerji dengesi ve yağ kaybı</div>
    <div>Protein: miktar, zamanlama, bitkisel/hayvansal</div>
    <div>Yağ, karbonhidrat, lif, diyet modelleri</div>
    <div>Kreatin: her şey</div>
    <div>Diğer takviyeler, uyku, toparlanma</div>
  </div>
  <div class="foot"><strong>Okur profili:</strong> 173 cm · 98 kg · ~9 ay direnç antrenmanı geçmişi · hedef: yağ kaybı, üst vücut hipertrofisi, büyümeden güçlenen bacaklar, futbol için kondisyon.<br>Literatür taraması ve sentez: Claude (Anthropic) · PubMed ve akademik veri tabanları · Eylül 2026</div>
</section>
"""


def build(pages, out_path):
    with_markers = pages is None
    files = chapter_files()
    toc = []
    body = []
    for pi, (pnum, ptitle, pintro, keys) in enumerate(PARTS):
        pid = f"p{pi + 1}"
        toc.append(("part", pid, pnum, ptitle))
        chapter_lines = []
        part_chapters = []
        for key in keys:
            if key == "EC":
                continue
            if key not in files:
                continue
            if key.startswith("E"):
                label = f"Ek {key[1]}"
                prefix = key[1]
            else:
                label = f"Bölüm {int(key)}"
                prefix = str(int(key))
            part_chapters.append(process_chapter(key, files[key], label, prefix, with_markers, toc))
            chapter_lines.append((label, toc_title(toc, f"c{key.lower()}")))
        if pnum == "Ekler":
            g = build_glossary(with_markers, toc)
            if g:
                part_chapters.append(g)
                chapter_lines.append(("Ek C", "Terimler Sözlüğü"))
        if not part_chapters:
            toc.pop() if toc and toc[-1][1] == pid else None
            continue
        mk = f'<span class="pm">ZQ{pid}QZ</span>' if with_markers else ""
        chs = "".join(f"<div><span>{escape_html(l.replace('Bölüm ', ''))}</span>{escape_html(t)}</div>" for l, t in chapter_lines)
        body.append(f'<section class="part" id="{pid}"><div class="bar"></div>{mk}<div class="num">{pnum}</div><h1>{escape_html(ptitle)}</h1><div class="intro">{escape_html(pintro)}</div><div class="chs">{chs}</div></section>')
        body.extend(part_chapters)

    toc_html = ['<section class="toc"><h1>İçindekiler</h1>']
    for kind, tid, num, title in toc:
        pg = str(pages.get(tid, "")) if pages else "000"
        if kind == "part":
            toc_html.append(f'<div class="toc-part">{escape_html(num)} · {escape_html(title)}</div>')
        elif kind == "ch":
            n = num.replace("Bölüm ", "")
            toc_html.append(f'<div class="row ch"><span class="t"><span class="n">{escape_html(n)}</span>{escape_html(title)}</span><span class="dots"></span><span class="p">{pg}</span></div>')
        else:
            toc_html.append(f'<div class="row sec"><span class="t">{escape_html(num)}&nbsp;&nbsp;{escape_html(title)}</span><span class="dots"></span><span class="p">{pg}</span></div>')
    toc_html.append("</section>")

    html = f"""<!doctype html>
<html lang="tr"><head><meta charset="utf-8">
<title>Ağırlık Antrenmanı, Kardiyo ve Beslenme — Kanıta Dayalı Kapsamlı Rehber</title>
<link rel="stylesheet" href="style.css">
</head><body>
{COVER}
{FRONT}
{''.join(toc_html)}
{''.join(body)}
</body></html>"""
    Path(out_path).write_text(html, encoding="utf-8")
    print(f"yazıldı: {out_path} ({len(toc)} içindekiler girdisi)")


def toc_title(toc, cid):
    for kind, tid, num, title in toc:
        if tid == cid:
            return title
    return cid


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages")
    ap.add_argument("--out", default=str(ROOT / "rapor.html"))
    a = ap.parse_args()
    pages = json.loads(Path(a.pages).read_text()) if a.pages else None
    build(pages, a.out)
