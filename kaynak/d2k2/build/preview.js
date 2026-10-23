// kullanim: node preview.js <svgdir> <out.png> name1 name2 ...
const fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const [, , dir, out, ...names] = process.argv;
const head = fs.readFileSync(path.join(__dirname, "head_full.part"), "utf8").replace("__TITLE__", "p");
let body = names.map(n => `<figure class="chart-figure" style="width:170mm">${fs.readFileSync(path.join(dir, n + ".svg"), "utf8")}<figcaption class="chart-caption">${n}</figcaption></figure>`).join("\n");
const html = head + body + "</main></body></html>";
const tmp = path.resolve(dir, "_preview.html"); fs.writeFileSync(tmp, html);
(async () => {
  const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1243/chrome-linux64/chrome" });
  const p = await b.newPage({ viewport: { width: 760, height: 1000 }, deviceScaleFactor: 1.6 });
  await p.goto("file://" + tmp, { waitUntil: "networkidle" });
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: out, fullPage: true });
  await b.close(); console.log("ok", out);
})().catch(e => { console.error(e.message); process.exit(1); });
