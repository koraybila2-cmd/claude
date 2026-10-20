// kullanim: NODE_PATH=$(npm root -g) node kareler.js <bolum.html> <zaman_cizelgesi.json> <cikti_klasoru>
// Zaman cizelgesindeki her ipucu icin kitabin ilgili blogunu vurgular, sayfayi yumusakca kaydirir
// ve 1920x1080 kareler uretir. Cikti klasorune kareleri ve ffmpeg concat listesini (liste.txt) yazar.
const fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const [, , htmlYol, cizelgeYol, cikti] = process.argv;
const cz = JSON.parse(fs.readFileSync(cizelgeYol, "utf8"));
const { W, H, UST, hazirla } = require("./sayfa");
const FPS = 30, GECIS = 0.5;

const ease = t => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2);

(async () => {
  fs.mkdirSync(cikti, { recursive: true });
  const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
  const p = await b.newPage({ viewport: { width: W, height: H } });
  await p.goto("file://" + path.resolve(htmlYol), { waitUntil: "networkidle" });
  await hazirla(p, cz.ust_baslik);

  // Her ipucunun hedef kaydirma konumunu ve sahne durumunu hazirla
  const durumKur = async (ip) => p.evaluate(({ sel, acik, UST, H }) => {
    document.querySelectorAll(".aktif").forEach(e => e.classList.remove("aktif"));
    document.querySelectorAll(".card").forEach(c => {
      const ac = acik.includes(c.id);
      c.classList.toggle("kapali", !ac);
      c.querySelectorAll(".opt").forEach(s => s.classList.toggle("dogru", ac && s.dataset.harf === c.dataset.dogru));
    });
    const els = [...document.querySelectorAll(sel)];
    if (!els.length) throw new Error("secici bulunamadi: " + sel);
    els.forEach(e => e.classList.add("aktif"));
    const y = window.scrollY;
    const ust = Math.min(...els.map(e => e.getBoundingClientRect().top)) + y;
    const alt = Math.max(...els.map(e => e.getBoundingClientRect().bottom)) + y;
    const alan = H - UST, h = alt - ust;
    let hedef = h + 80 <= alan ? ust - UST - (alan - h) / 2 : ust - UST - 50;
    const maks = document.documentElement.scrollHeight - H;
    return Math.max(0, Math.min(maks, hedef));
  }, { sel: ip.sel, acik: ip.acik, UST, H });

  const toplam = cz.ipuclari.reduce((s, i) => s + i.sure, 0);
  const liste = []; let n = 0, onceki = null, gecen = 0;
  const kare = async (y, t) => {
    await p.evaluate(({ y, oran }) => { window.scrollTo(0, y); document.querySelector(".vid-ilerleme").style.width = (oran * 100) + "%"; },
      { y, oran: Math.min(1, t / toplam) });
    const ad = `k${String(n++).padStart(5, "0")}.png`;
    await p.screenshot({ path: path.join(cikti, ad) });
    return ad;
  };
  for (const ip of cz.ipuclari) {
    const hedef = await durumKur(ip);
    let kalan = ip.sure;
    if (onceki !== null && Math.abs(hedef - onceki) > 2 && ip.sure > GECIS + 0.3) {
      const nk = Math.round(GECIS * FPS);
      for (let i = 1; i <= nk; i++) {
        const ad = await kare(onceki + (hedef - onceki) * ease(i / nk), gecen + (i / nk) * GECIS);
        liste.push([ad, 1 / FPS]);
      }
      kalan -= nk / FPS; gecen += nk / FPS;
    }
    // Duragan kisim: ilerleme cubugu icin saniyede bir kare yeterli
    while (kalan > 1e-6) {
      const d = Math.min(1, kalan);
      liste.push([await kare(hedef, gecen), d]);
      kalan -= d; gecen += d;
    }
    onceki = hedef;
  }
  const son = liste[liste.length - 1][0];
  fs.writeFileSync(path.join(cikti, "liste.txt"),
    liste.map(([a, d]) => `file '${a}'\nduration ${d.toFixed(4)}`).join("\n") + `\nfile '${son}'\n`);
  await b.close();
  console.log("kare:", n, "sure:", gecen.toFixed(1), "sn");
})().catch(e => { console.error(e.message); process.exit(1); });
