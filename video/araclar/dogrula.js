// kullanim: NODE_PATH=$(npm root -g) node dogrula.js <bolum.html> <ipuclari.json>
// ipuclari.json: [{"yer": "k4b1_01:3", "sel": "...", "acik": ["k1"]}] (satir sirasiyla)
// Ciktisi JSON: seciciler, kapsanmayan bloklar, cok genis seciciler, cevabi kapaliyken okunan kart bolumleri.
const fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const { W, H, hazirla } = require("./sayfa");
const [, , htmlYol, ipYol] = process.argv;
const ipuclari = JSON.parse(fs.readFileSync(ipYol, "utf8"));

// Anlatimda karsiligi olmasi gereken her icerik blogu
const BLOK = [".book-kicker", ".book-title", ".book-byline", ".chapter-kicker", ".chapter-title", ".chapter-lead",
  ".book-h2", ".book-h3", ".book-h4", "p.book-p", ".book-list > li", ".toc > li", "table tbody > tr", ".chart-figure",
  ".hl-block", ".keybox", ".card-kicker", ".qtext", ".opt", ".card-body > p", ".card-dispute", ".card-source"].join(", ");

(async () => {
  const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
  const p = await b.newPage({ viewport: { width: W, height: H } });
  await p.goto("file://" + path.resolve(htmlYol), { waitUntil: "networkidle" });
  await hazirla(p, "dogrulama");
  const rapor = await p.evaluate(({ ipuclari, BLOK }) => {
    const bloklar = [...document.querySelectorAll(BLOK)].filter(e => !e.parentElement.closest(".hl-block, .keybox, .chart-figure")
      || e.matches(".hl-block, .keybox, .chart-figure"));
    const kisa = e => (e.textContent || "").replace(/\s+/g, " ").trim().slice(0, 90);
    const etiket = e => e.tagName.toLowerCase() + (e.className ? "." + String(e.className).split(" ")[0] : "");
    const kapsandi = new Set(), seciciler = [], genis = [], kapali = [], hatali = [];
    ipuclari.forEach(ip => {
      let els = [];
      try { els = [...document.querySelectorAll(ip.sel)]; } catch (e) { hatali.push({ yer: ip.yer, sel: ip.sel, hata: e.message }); return; }
      seciciler.push({ yer: ip.yer, sel: ip.sel, n: els.length });
      els.forEach(el => {
        const icerdeki = bloklar.filter(bl => el === bl || el.contains(bl) || bl.contains(el));
        icerdeki.forEach(bl => kapsandi.add(bl));
        const alt = bloklar.filter(bl => el !== bl && el.contains(bl)).length;
        if (alt > 6) genis.push({ yer: ip.yer, sel: ip.sel, blok_sayisi: alt });
        const kart = el.closest(".card");
        if (kart && el.closest(".card-body, .card-dispute, .card-source") && !ip.acik.includes(kart.id))
          kapali.push({ yer: ip.yer, sel: ip.sel, kart: kart.id });
      });
    });
    const kapsanmayan = bloklar.filter(bl => !kapsandi.has(bl)).map(bl => ({ blok: etiket(bl), metin: kisa(bl) }));
    const kartlar = [...document.querySelectorAll(".card")].map(c => ({ id: c.id, sik: c.querySelectorAll(".opt").length,
      dogru: c.dataset.dogru || null }));
    const bolumler = [...document.querySelectorAll(".book-section")].map(s => ({ id: s.id,
      baslik: kisa(s.querySelector("h2, h3") || s).slice(0, 60) }));
    return { seciciler, hatali, kapsanmayan, genis, kapali, kartlar, bolumler, blok_sayisi: bloklar.length };
  }, { ipuclari, BLOK });
  await b.close();
  process.stdout.write(JSON.stringify(rapor));
})().catch(e => { console.error(e.message); process.exit(1); });
