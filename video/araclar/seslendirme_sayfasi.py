#!/usr/bin/env python3
"""Butun bolumlerin seslendirme parcalarini tek bir calisma sayfasinda toplar (AI Studio'da elle uretim icin).

kullanim (repo kokunden): python3 video/araclar/seslendirme_sayfasi.py [--kitaplar 4,5] [cikti.html]
Varsayilan cikti: video/seslendirme.html. --kitaplar: yalnizca denetimi bitmis kitaplarin parcalari listelenir,
digerleri "metin hazirlaniyor" gorunur (kullanici sesini urettigi metin sonradan degismesin diye). Sesi zaten bulunan parcalar (video/<bolum>/ses/<parca>.wav) "hazir" isaretlenir.
"""
import glob, html, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bolum, ses

KOK = bolum.KOK
SIRA = ["4", "2", "1", "3", "5", "6"]          # once en cok soru gelen kitaplar


def bolum_sirasi(klasor):
    m = re.match(r"k(\d+)b(\d+)([a-z]?)$", klasor)
    return (int(m.group(2)), m.group(3))


def veri(hazir=None):
    sesler = json.load(open(os.path.join(KOK, "video/sesler.json"), encoding="utf-8"))
    kitaplar = []
    for k in SIRA:
        kapak = open(os.path.join(KOK, f"kaynak/modul4/kitaplar/m4k{k}/00_kapak.html"), encoding="utf-8").read()
        ad = html.unescape(re.search(r'class="book-title">([^<]*)', kapak).group(1)).strip()
        bolumler = []
        for d in [] if hazir is not None and k not in hazir else sorted((os.path.basename(p) for p in glob.glob(os.path.join(KOK, f"video/k{k}b*"))
                         if os.path.exists(os.path.join(p, "parcalar.txt"))), key=bolum_sirasi):
            yol = os.path.join(KOK, "video", d)
            try:
                ust = json.load(open(os.path.join(yol, "sahne.json"), encoding="utf-8"))["ust_baslik"]
            except Exception:
                ust = d
            parcalar = []
            for pid, p in bolum.parcalari_oku(os.path.join(yol, "parcalar.txt")).items():
                metin = "\n".join(p["satirlar"])
                parcalar.append({"id": pid, "baslik": p["baslik"], "metin": metin, "kar": len(metin),
                                 "hazir": os.path.exists(os.path.join(yol, "ses", pid + ".wav"))})
            bolumler.append({"klasor": d, "baslik": ust, "parcalar": parcalar})
        kitaplar.append({"no": k, "ad": ad, "ses": sesler[k], "bolumler": bolumler})
    return {"kitaplar": kitaplar, "uslup": ses.USLUP}


SAYFA = r"""<title>Modül 4 Seslendirme</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=Source+Sans+3:wght@400;600;700&family=JetBrains+Mono:wght@500&display=swap">
<style>
/* Düzen: tek sütunlu çalışma sayfası. Üstte bir kez yapılacak ayarlar, ortada kitap sekmeleri ve sırayla işlenecek parça kartları, altta teslim ve sorun giderme. */
:root {
  --bg: #eef3f4; --surface: #ffffff; --ink: #14272c; --muted: #52666b; --line: #cfdcdf;
  --accent: #00788f; --accent-ink: #ffffff; --accent-soft: #dcf0f3; --mark: #b8005c; --done: #1f7a4d; --done-soft: #e1f3e9;
  --f-display: "Bricolage Grotesque", "Segoe UI", system-ui, sans-serif;
  --f-body: "Source Sans 3", "Segoe UI", system-ui, sans-serif;
  --f-mono: "JetBrains Mono", ui-monospace, "SFMono-Regular", Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #0e1a1d; --surface: #152428; --ink: #e3eef0; --muted: #9db2b7; --line: #29404a;
  --accent: #39b6cc; --accent-ink: #062126; --accent-soft: #163a42; --mark: #ff6fae; --done: #5fd39a; --done-soft: #17362a; color-scheme: dark } }
:root[data-theme="dark"] {
  --bg: #0e1a1d; --surface: #152428; --ink: #e3eef0; --muted: #9db2b7; --line: #29404a;
  --accent: #39b6cc; --accent-ink: #062126; --accent-soft: #163a42; --mark: #ff6fae; --done: #5fd39a; --done-soft: #17362a; color-scheme: dark }
* { box-sizing: border-box; }
body { background: var(--bg); color: var(--ink); font-family: var(--f-body); font-size: 16px; line-height: 1.55; }
.wrap { max-width: 880px; margin: 0 auto; padding-block: 28px 64px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  display: flex; flex-direction: column; gap: 28px; }
h1, h2, h3 { font-family: var(--f-display); text-wrap: balance; margin: 0; letter-spacing: -0.01em; }
h1 { font-size: clamp(1.7rem, 4.5vw, 2.4rem); line-height: 1.1; }
h2 { font-size: 1.3rem; }
h3 { font-size: 1.05rem; }
.eyebrow { font-size: 0.78rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent); margin: 0 0 6px; }
.lead { color: var(--muted); margin: 10px 0 0; max-width: 65ch; }
.meta { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
.chip { font-size: 0.85rem; padding: 4px 10px; border-radius: 999px; background: var(--accent-soft); color: var(--ink); font-variant-numeric: tabular-nums; }
section { display: flex; flex-direction: column; gap: 12px; }
ol.steps { margin: 0; padding-left: 1.4em; display: flex; flex-direction: column; gap: 8px; max-width: 70ch; }
ol.steps li::marker { color: var(--accent); font-weight: 700; }
ol.steps ul { margin: 6px 0 0; padding-left: 1.1em; color: var(--muted); }
code, .mono { font-family: var(--f-mono); font-size: 0.86em; }
.note { font-size: 0.92rem; color: var(--muted); max-width: 70ch; margin: 0; }
.box { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 16px 18px; display: flex; flex-direction: column; gap: 10px; min-width: 0; }
.boxhead { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 10px; }
.label { font-weight: 700; }
.textblock { white-space: pre-wrap; background: var(--bg); border-radius: 8px; padding: 12px 14px; max-height: 12em; overflow: auto; font-size: 0.95rem; min-width: 0; }
button { font: inherit; font-weight: 600; cursor: pointer; border-radius: 8px; border: 1px solid var(--accent); padding: 8px 14px; background: var(--accent); color: var(--accent-ink); }
button.ghost { background: transparent; color: var(--accent); }
button:focus-visible, input:focus-visible, a:focus-visible { outline: 3px solid var(--mark); outline-offset: 2px; }
a { color: var(--accent); }
.tabs { display: flex; flex-wrap: wrap; gap: 8px; }
.tabs button { background: var(--surface); color: var(--ink); border-color: var(--line); text-align: left; display: flex; flex-direction: column; gap: 0; padding: 8px 12px; }
.tabs button small { font-weight: 400; color: var(--muted); font-variant-numeric: tabular-nums; }
.tabs button[aria-selected="true"] { background: var(--accent); color: var(--accent-ink); border-color: var(--accent); }
.tabs button[aria-selected="true"] small { color: var(--accent-ink); }
.key { background: var(--accent-soft); border-radius: 10px; padding: 14px 16px; display: flex; flex-wrap: wrap; gap: 6px 24px; align-items: baseline; }
.key .big { font-family: var(--f-display); font-size: 1.6rem; font-weight: 700; color: var(--accent); }
.chapter { display: flex; flex-direction: column; gap: 10px; }
.part.is-done { border-color: var(--done); background: var(--done-soft); }
.part.is-ready { opacity: .72; }
.part.is-ready .textblock, .part.is-ready .actions { display: none; }
.part .fname { font-family: var(--f-mono); font-size: 0.9rem; color: var(--mark); }
.part .title { font-weight: 700; }
.part .dur { font-size: 0.85rem; color: var(--muted); font-variant-numeric: tabular-nums; }
.badge { font-size: 0.8rem; font-weight: 700; padding: 3px 9px; border-radius: 999px; background: var(--done-soft); color: var(--done); border: 1px solid var(--done); }
.actions { display: flex; flex-wrap: wrap; align-items: center; gap: 12px; }
.check { display: inline-flex; align-items: center; gap: 6px; font-size: 0.95rem; }
.check input { width: 18px; height: 18px; accent-color: var(--done); }
.toast { font-size: 0.88rem; color: var(--done); min-height: 1.2em; }
.warn { border-left: 4px solid var(--mark); padding: 10px 14px; background: var(--surface); border-radius: 0 8px 8px 0; max-width: 70ch; }
.qa { display: flex; flex-direction: column; gap: 10px; }
.qa div { max-width: 70ch; }
.qa b { display: block; }
.empty { color: var(--muted); font-style: italic; }
@media (prefers-reduced-motion: no-preference) { button { transition: filter .15s ease; } button:hover { filter: brightness(1.08); } }
</style>

<div class="wrap">
  <header>
    <p class="eyebrow">Modül 4 · Solunum Sistemi · 6 kitap</p>
    <h1>Modül 4 seslendirme</h1>
    <p class="lead">Her kitabın anlatımı büyük parçalara bölündü. Her parçayı AI Studio Playground'da sese çevirip indireceksin, sonra Google Drive'a yükleyeceksin. Videoları bu dosyalarla ben kuracağım.</p>
    <div class="meta" id="meta"></div>
  </header>

  <section aria-labelledby="h-setup">
    <h2 id="h-setup">1. Playground'u hazırla</h2>
    <ol class="steps">
      <li>Bilgisayarda <a href="https://aistudio.google.com/" target="_blank" rel="noopener">aistudio.google.com</a>'u aç ve sol menüden <b>Playground</b>'a gir.</li>
      <li>Sağdaki ayar panelinde <b>Model</b> listesinden adında TTS geçen <b>Gemini 3.8 Flash TTS</b>'i seç. Normal bir sohbet modeli seçersen ses değil yazı gelir.</li>
      <li><b>Voice</b> listesinden, aşağıda seçtiğin kitabın sesini seç. <b>Her kitabın sesi farklı.</b> Kitap değiştirdiğinde sesi de değiştir.</li>
      <li><b>System instructions</b> kutusuna aşağıdaki üslup talimatını yapıştır. Bu kutu hiç değişmez.</li>
    </ol>
    <div class="box">
      <div class="boxhead"><span class="label">Üslup talimatı (System instructions)</span><button type="button" id="copy-style">Talimatı kopyala</button></div>
      <div class="textblock" id="style-text"></div>
      <div class="toast" id="style-toast" aria-live="polite"></div>
    </div>
  </section>

  <section aria-labelledby="h-loop">
    <h2 id="h-loop">2. Her parça için</h2>
    <ol class="steps">
      <li>Parça kartında <b>Metni kopyala</b>'ya bas.</li>
      <li>Playground'daki yazı kutusunu temizle ve <b>yalnızca bu metni</b> yapıştır. Başına ya da sonuna hiçbir şey ekleme; model ne yazarsan onu okur.</li>
      <li><b>Run</b>'a bas. Uzun parçalarda ses bir iki dakikada hazır olur.</li>
      <li>Dinle: atlanan cümle, sona doğru bozulma ya da kesilme olmamalı. Sorun varsa Run'a yeniden bas.</li>
      <li>İndirme simgesiyle indir ve dosyanın adını kartta pembe yazan adla değiştir (örneğin <span class="mono">k4b1_01.wav</span>).</li>
      <li><b>Tamamlandı</b> kutusunu işaretle, sonraki karta geç.</li>
    </ol>
    <p class="note">Bir parça 7-8 dakikalık ses eder. Soru sonlarındaki düşünme aralarını videoya ben ekliyorum.</p>
  </section>

  <section aria-labelledby="h-parts">
    <h2 id="h-parts">3. Parçalar</h2>
    <div class="tabs" role="tablist" id="tabs"></div>
    <div id="book"></div>
  </section>

  <section aria-labelledby="h-send">
    <h2 id="h-send">4. Drive'a yükle</h2>
    <ol class="steps">
      <li>Dosyaları Google Drive'daki <b>Modul4 Video Sesleri</b> klasörüne yükle.</li>
      <li>Klasörün paylaşımını <b>Bağlantıya sahip olan herkes · Görüntüleyen</b> yap (indirebilmem için), sonra bana "yükledim" yaz.</li>
      <li>İndirdiğimi söyleyince paylaşımı yeniden <b>Kısıtlanmış</b> yap.</li>
    </ol>
    <div class="warn"><b>Dosya adları önemli.</b> Videoyu kuran betik sesleri adlarından tanıyor. <span class="mono">k4b1_01 (1).wav</span> gibi kopya adları kalırsa düzeltmem gerekir.</div>
  </section>

  <section aria-labelledby="h-help">
    <h2 id="h-help">Sorun çıkarsa</h2>
    <div class="qa">
      <div><b>Ses sona doğru bozuluyor ya da kesiliyor.</b>Metni bir paragraf sonundan ikiye böl, iki ayrı ses üret ve dosyaları <span class="mono">k4b1_01a.wav</span> ile <span class="mono">k4b1_01b.wav</span> diye adlandır. Ben birleştiririm.</div>
      <div><b>Bir kelime her denemede yanlış okunuyor.</b>Kelimeyi ve parça adını bana yaz; metinde okunuşunu düzeltip sayfayı güncellerim.</div>
      <div><b>Kullanım sınırı uyarısı çıktı.</b>Kaldığın parçadan ertesi gün devam et. İşaretlediğin kutular bu tarayıcıda kayıtlı kalır.</div>
      <div><b>Ses yerine yazı geliyor.</b>Model listesinde TTS olan modeli seçmemişsin. Model'i Gemini 3.8 Flash TTS yap.</div>
    </div>
  </section>
</div>

<script id="data" type="application/json">__VERI__</script>
<script>
(function () {
  var D = JSON.parse(document.getElementById("data").textContent);
  var KEY = "m4-seslendirme-done", TAB = "m4-seslendirme-tab";
  var done = {};
  try { done = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { done = {}; }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(done)); } catch (e) {} }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function selectText(node) { try { var r = document.createRange(); r.selectNodeContents(node); var s = window.getSelection(); s.removeAllRanges(); s.addRange(r); } catch (e) {} }
  function copy(text, node, toast) {
    function ok() { toast.textContent = "Kopyalandı. Playground'a yapıştırabilirsin."; }
    function fail() { selectText(node); toast.textContent = "Otomatik kopyalama çalışmadı; metin seçildi, Ctrl + C ile kopyala."; }
    try { if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(ok, fail); else fail(); } catch (e) { fail(); }
  }
  function parts(k) { var a = []; k.bolumler.forEach(function (b) { b.parcalar.forEach(function (p) { a.push(p); }); }); return a; }
  function todo(k) { return parts(k).filter(function (p) { return !p.hazir; }); }
  function count(k) { var t = todo(k); return { n: t.filter(function (p) { return done[p.id]; }).length, of: t.length }; }
  function dk(kar) { return Math.max(1, Math.round(kar / 15 / 60)); }

  var st = document.getElementById("style-text"); st.textContent = D.uslup;
  document.getElementById("copy-style").addEventListener("click", function () { copy(D.uslup, st, document.getElementById("style-toast")); });

  var meta = document.getElementById("meta");
  function renderMeta() {
    var tot = 0, ok = 0, kar = 0;
    D.kitaplar.forEach(function (k) { var c = count(k); tot += c.of; ok += c.n; todo(k).forEach(function (p) { kar += p.kar; }); });
    meta.innerHTML = "";
    meta.appendChild(el("span", "chip", tot + " parça senden"));
    meta.appendChild(el("span", "chip", "yaklaşık " + Math.round(kar / 15 / 3600 * 10) / 10 + " saat ses"));
    meta.appendChild(el("span", "chip", ok + " / " + tot + " tamamlandı"));
  }

  var tabs = document.getElementById("tabs"), book = document.getElementById("book");
  var cur = null; try { cur = localStorage.getItem(TAB); } catch (e) {}
  if (!D.kitaplar.some(function (k) { return k.no === cur; })) cur = D.kitaplar[0].no;

  function renderTabs() {
    tabs.innerHTML = "";
    D.kitaplar.forEach(function (k) {
      var c = count(k);
      var b = el("button"); b.type = "button"; b.setAttribute("role", "tab"); b.id = "tab-" + k.no;
      b.setAttribute("aria-selected", String(k.no === cur));
      b.appendChild(el("span", null, "Kitap " + k.no + " · " + k.ses));
      b.appendChild(el("small", null, c.of ? c.n + " / " + c.of + " parça" : "metin hazırlanıyor"));
      b.addEventListener("click", function () { cur = k.no; try { localStorage.setItem(TAB, cur); } catch (e) {} renderTabs(); renderBook(); });
      tabs.appendChild(b);
    });
  }

  function renderBook() {
    var k = D.kitaplar.filter(function (x) { return x.no === cur; })[0];
    book.innerHTML = "";
    var wrap = el("div", "chapter");
    var key = el("div", "key");
    key.appendChild(el("span", "big", k.ses));
    var t = el("span"); t.innerHTML = "Kitap " + k.no + ": <b></b> · Voice listesinde <b></b> seçili olsun";
    t.querySelectorAll("b")[0].textContent = k.ad; t.querySelectorAll("b")[1].textContent = k.ses;
    key.appendChild(t); wrap.appendChild(key);
    if (!k.bolumler.length) wrap.appendChild(el("p", "empty", "Bu kitabın anlatım metinleri henüz hazırlanıyor."));
    k.bolumler.forEach(function (b) {
      var sec = el("div", "chapter"); sec.appendChild(el("h3", null, b.baslik));
      b.parcalar.forEach(function (p) {
        var card = el("article", "box part" + (p.hazir ? " is-ready" : (done[p.id] ? " is-done" : "")));
        var head = el("div", "boxhead"), left = el("div");
        left.appendChild(el("div", "title", p.baslik)); left.appendChild(el("div", "fname", p.id + ".wav"));
        head.appendChild(left);
        if (p.hazir) { head.appendChild(el("span", "badge", "Hazır, atla")); card.appendChild(head); sec.appendChild(card); return; }
        head.appendChild(el("div", "dur", p.kar.toLocaleString("tr-TR") + " karakter · yaklaşık " + dk(p.kar) + " dk"));
        var tb = el("div", "textblock", p.metin);
        var act = el("div", "actions"), btn = el("button", null, "Metni kopyala"); btn.type = "button";
        var lab = el("label", "check"), cb = el("input"); cb.type = "checkbox"; cb.id = "done-" + p.id; cb.checked = !!done[p.id];
        lab.appendChild(cb); lab.appendChild(document.createTextNode("Tamamlandı"));
        var toast = el("div", "toast"); toast.setAttribute("aria-live", "polite");
        btn.addEventListener("click", function () { copy(p.metin, tb, toast); });
        cb.addEventListener("change", function () {
          if (cb.checked) done[p.id] = true; else delete done[p.id];
          card.classList.toggle("is-done", cb.checked); save(); renderMeta(); renderTabs();
        });
        act.appendChild(btn); act.appendChild(lab);
        card.appendChild(head); card.appendChild(tb); card.appendChild(act); card.appendChild(toast);
        sec.appendChild(card);
      });
      wrap.appendChild(sec);
    });
    book.appendChild(wrap);
  }
  renderMeta(); renderTabs(); renderBook();
})();
</script>
"""


def main():
    arg = sys.argv[1:]
    hazir = None
    if "--kitaplar" in arg:
        i = arg.index("--kitaplar"); hazir = set(arg[i + 1].split(",")); del arg[i:i + 2]
    cikti = arg[0] if arg else os.path.join(KOK, "video/seslendirme.html")
    v = veri(hazir)
    open(cikti, "w", encoding="utf-8").write(SAYFA.replace("__VERI__", json.dumps(v, ensure_ascii=False).replace("</", "<\\/")))
    n = sum(len(b["parcalar"]) for k in v["kitaplar"] for b in k["bolumler"])
    print(cikti, f"{n} parca")


if __name__ == "__main__":
    main()
