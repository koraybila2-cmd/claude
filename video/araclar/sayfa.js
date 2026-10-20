// Video karesi icin bolum sayfasini hazirlar: kitap CSS'ine video duzenini ekler, bloklara
// sahne.json secicilerinin dayandigi kimlikleri verir. kareler.js ve dogrula.js ortak kullanir.
const W = 1920, H = 1080, UST = 84;

const CSS = `
  html { font-size: 30px; }
  body { background: var(--color-bg); }
  main.book-page { width: 1280px; margin: 0 auto; padding: ${UST + 70}px 0 ${H}px 0; }
  .chapter-kicker, .card-kicker, .book-kicker { font-size: 17px; }
  .tag { font-size: 16px; }
  .chart-figure svg { max-height: 600px; }
  .vid-ust { position: fixed; z-index: 10; left: 0; right: 0; top: 0; height: ${UST}px; display: flex; align-items: center;
    padding: 0 64px; background: color-mix(in oklch, var(--color-bg), white 40%); border-bottom: 1px solid color-mix(in oklch, var(--color-text) 12%, white);
    font-family: var(--font-heading); font-size: 22px; letter-spacing: 0.1em; text-transform: uppercase; color: var(--color-accent-700); }
  .vid-ilerleme { position: fixed; z-index: 11; left: 0; bottom: 0; height: 6px; background: var(--color-accent); }
  .aktif { background: color-mix(in oklch, var(--color-accent) 13%, white);
    box-shadow: 0 0 0 12px color-mix(in oklch, var(--color-accent) 13%, white); border-radius: 3px; }
  tr.aktif { box-shadow: none; } tr.aktif td { background: color-mix(in oklch, var(--color-accent) 13%, white); }
  .card .opt { display: block; }
  .card.kapali .card-body, .card.kapali .card-source { filter: blur(12px); opacity: 0.35; }
  .card .opt.dogru { color: var(--color-accent-700); font-weight: 700; }
  .card .opt.dogru::after { content: "  ✓"; }
`;

// Sayfa icinde calisir. #bas: bolum basligi, #s1..: .book-section sirasi, #k1..: soru kartlari,
// .qtext: soru cumlesi, .opt: tek tek siklar.
function dom({ css, baslik }) {
  const st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
  const ust = document.createElement("div"); ust.className = "vid-ust"; ust.textContent = baslik; document.body.appendChild(ust);
  const il = document.createElement("div"); il.className = "vid-ilerleme"; document.body.appendChild(il);
  const kick = document.querySelector(".chapter-kicker"), tit = document.querySelector(".chapter-title");
  if (kick && tit) { const kb = document.createElement("div"); kb.id = "bas"; kick.before(kb); kb.append(kick, tit); }
  document.querySelectorAll(".book-section").forEach((s, i) => (s.id = "s" + (i + 1)));
  document.querySelectorAll(".card").forEach((c, i) => {
    c.id = "k" + (i + 1);
    const t = c.querySelector(".card-title"); if (!t) return;
    const o = t.querySelector(".opts");
    const q = document.createElement("span"); q.className = "qtext";
    while (t.firstChild && t.firstChild !== o) q.appendChild(t.firstChild);
    t.insertBefore(q, o);
    if (o) o.innerHTML = o.textContent.split(" · ").map(s => `<span class="opt">${s}</span>`).join("");
    const dc = c.querySelector(".opt-correct");
    const m = dc && (dc.textContent.match(/:\s*([A-E])\.\s*$/) || [])[1];
    if (m && o) [...o.children].forEach(s => (s.dataset.harf = s.textContent.trim()[0])), (c.dataset.dogru = m);
  });
}

async function hazirla(page, baslik) {
  await page.evaluate(dom, { css: CSS, baslik });
  await page.evaluate(() => document.fonts.ready);
}

module.exports = { W, H, UST, CSS, hazirla };
