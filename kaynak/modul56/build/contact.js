// kullanim: node contact.js <dir> <out.png> <from> <to> [cols]
const fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const [, , dir, out, from, to, colsArg] = process.argv;
const cols = +(colsArg || 6);
const files = fs.readdirSync(dir).filter(f => /^p-\d+\.jpg$/.test(f)).sort();
const pick = files.filter(f => { const n = +f.match(/\d+/)[0]; return n >= +from && n <= +to; });
const html = `<html><body style="margin:0;background:#888;display:grid;grid-template-columns:repeat(${cols},1fr);gap:6px;padding:6px">` +
  pick.map(f => `<div style="position:relative"><img src="file://${path.resolve(dir, f)}" style="width:100%;display:block"><span style="position:absolute;top:2px;left:4px;font:bold 14px sans-serif;color:#d6006c">${+f.match(/\d+/)[0]}</span></div>`).join("") + "</body></html>";
const tmp = path.resolve(dir, "_contact.html"); fs.writeFileSync(tmp, html);
(async () => {
  const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
  const p = await b.newPage({ viewport: { width: 1500, height: 800 } });
  await p.goto("file://" + tmp); await p.waitForTimeout(300);
  await p.screenshot({ path: out, fullPage: true }); await b.close(); console.log("ok", out);
})();
