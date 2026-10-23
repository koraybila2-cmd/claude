// kullanim: node assemble.js <kitapdir> "<Baslik>"
// <!--CHART:ad--> -> charts/ad.svg ; <!--YIL:a,b,c,d--> -> yillik soru grafigi (Derleme,23-24,24-25,25-26 uyg.)
const fs = require("fs"), path = require("path"), { execFileSync } = require("child_process");
const [, , dir, title] = process.argv;
const B = __dirname, CH = path.join(B, "..", "charts");
const GEN = "/home/user/claude/.claude/skills/ders-kitabi/scripts/bar_chart_svg.js";
let html = fs.readFileSync(path.join(B, "head_full.part"), "utf8").replace("__TITLE__", title);
const parts = fs.readdirSync(dir).filter(f => /^\d.*\.html$/.test(f)).sort();
let n = 0;
const trDec = (svg) => svg.replace(/>(\d+)\.(\d+)([^<]*)</g, ">$1,$2$3<").replace(/>([\d,]+)%</g, ">%$1<");
for (const f of parts) html += fs.readFileSync(path.join(dir, f), "utf8") + "\n";
html += fs.readFileSync(path.join(B, "foot.part"), "utf8");
html = html.replace(/<!--SVG:([\w-]+)-->/g, (m, name) => fs.readFileSync(path.join(dir, "svg", name + ".svg"), "utf8"));
html = html.replace(/<!--CHART:([\w-]+)-->/g, (m, name) => {
  const js = path.join(CH, name + ".json");
  return trDec(execFileSync("node", [GEN, js]).toString());
});
html = html.replace(/<!--YIL:([\d,]+)(?:\|([^>]*))?-->/g, (m, vals, lbl) => {
  const v = vals.split(",").map(Number);
  const labels = ["Derleme", "2023-2024", "2024-2025", "2025-2026 uyg."];
  const cfg = { width: 640, height: 200, ariaLabel: "Yıllara göre soru sayısı", unit: "", maxValue: Math.max(5, Math.ceil(Math.max(...v) / 5) * 5),
    categories: labels.map((l, i) => ({ label: l, value: v[i] })) };
  const tmp = path.join(CH, `_yil_${n++}.json`); fs.writeFileSync(tmp, JSON.stringify(cfg));
  return trDec(execFileSync("node", [GEN, tmp]).toString());
});
const out = path.join(dir, path.basename(dir) + ".html");
fs.writeFileSync(out, html);
console.log("HTML:", out, parts.length, "parca");
