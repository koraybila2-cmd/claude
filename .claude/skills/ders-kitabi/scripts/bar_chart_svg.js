#!/usr/bin/env node
// Broadsheet-stilinde, tek-seri, statik/print bar chart SVG'si uretir.
// dataviz skill metodolojisine gore: tek seri = tek renk (sequential),
// <=24px bar kalinligi, 4px yuvarlatilmis uc, cizgi izgara (gridline)
// hairline/recessive, deger etiketleri bar ucunda.
//
// Kullanim: node bar_chart_svg.js girdi.json > cikti-svg.txt
// girdi.json semasi:
// {
//   "width": 640, "height": 320,
//   "categories": [{"label": "2018-2019", "value": 4}, ...],
//   "maxValue": 10,          // opsiyonel, verilmezse otomatik yuvarlanir
//   "unit": "",              // deger etiketlerinin sonuna eklenir (orn. "%")
//   "colorVar": "var(--color-accent-700)"  // opsiyonel, varsayilan cyan-700
// }

const fs = require("fs");

const inputPath = process.argv[2];
if (!inputPath) {
  console.error("Kullanim: node bar_chart_svg.js girdi.json");
  process.exit(1);
}

const cfg = JSON.parse(fs.readFileSync(inputPath, "utf-8"));
const W = cfg.width || 640;
const H = cfg.height || 320;
const cats = cfg.categories;
const unit = cfg.unit || "";
const color = cfg.colorVar || "var(--color-accent-700)";

const leftMargin = 20;
const rightMargin = 20;
const topPad = 28; // deger etiketi icin ust bosluk
const xAxisBand = 46; // kategori etiketleri icin alt bosluk (2 satira kadar)
const baselineY = H - xAxisBand;
const plotTop = topPad;
const plotHeight = baselineY - plotTop;

const rawMax = Math.max(...cats.map((c) => c.value));
const maxValue = cfg.maxValue || niceCeil(rawMax);

function niceCeil(v) {
  if (v <= 5) return 5;
  if (v <= 10) return 10;
  const mag = Math.pow(10, Math.floor(Math.log10(v)));
  return Math.ceil(v / mag) * mag;
}

const n = cats.length;
const plotWidth = W - leftMargin - rightMargin;
const slotWidth = plotWidth / n;
const barWidth = Math.min(24, slotWidth * 0.55);
const barRadius = 4;

const gridSteps = 4; // baseline + 4 aralik
let gridlines = "";
for (let i = 1; i <= gridSteps; i++) {
  const y = baselineY - (plotHeight * i) / gridSteps;
  gridlines += `<line x1="${leftMargin}" y1="${y.toFixed(1)}" x2="${(W - rightMargin).toFixed(1)}" y2="${y.toFixed(1)}" stroke="var(--color-neutral-700)" stroke-opacity="0.18" stroke-width="1"/>\n  `;
}

let bars = "";
let valueLabels = "";
let axisLabels = "";

cats.forEach((c, i) => {
  const slotCenter = leftMargin + slotWidth * (i + 0.5);
  const barX = slotCenter - barWidth / 2;
  const barH = (c.value / maxValue) * plotHeight;
  const barY = baselineY - barH;

  // Ust kenarlar yuvarlatilmis, alt kose keskin (baseline'a oturan) tek path.
  const r = Math.min(barRadius, barWidth / 2, Math.max(barH, 1));
  const path = barH <= 0
    ? ""
    : `M${barX},${baselineY} L${barX},${(barY + r).toFixed(1)} Q${barX},${barY.toFixed(1)} ${(barX + r).toFixed(1)},${barY.toFixed(1)} L${(barX + barWidth - r).toFixed(1)},${barY.toFixed(1)} Q${(barX + barWidth).toFixed(1)},${barY.toFixed(1)} ${(barX + barWidth).toFixed(1)},${(barY + r).toFixed(1)} L${(barX + barWidth).toFixed(1)},${baselineY} Z`;

  bars += `<path d="${path}" fill="${color}"/>\n  `;
  valueLabels += `<text x="${slotCenter.toFixed(1)}" y="${(barY - 8).toFixed(1)}" text-anchor="middle" font-family="var(--font-body)" font-size="13" font-weight="700" fill="var(--color-text)">${c.value}${unit}</text>\n  `;

  // Kategori etiketi iki satira kadar sarilabilir (orn. "2021-2022" tek satir kalsin, uzunsa boluruz).
  const label = String(c.label);
  const words = label.length > 10 && label.includes(" ") ? label.split(" ") : [label];
  words.forEach((w, li) => {
    axisLabels += `<text x="${slotCenter.toFixed(1)}" y="${(baselineY + 18 + li * 14).toFixed(1)}" text-anchor="middle" font-family="var(--font-body)" font-size="12" fill="var(--color-neutral-700)">${escapeXml(w)}</text>\n  `;
  });
});

function escapeXml(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

const svg = `<svg viewBox="0 0 ${W} ${H}" width="100%" style="display:block" role="img" aria-label="${escapeXml(cfg.ariaLabel || "Bar chart")}">
  <line x1="${leftMargin}" y1="${baselineY}" x2="${(W - rightMargin).toFixed(1)}" y2="${baselineY}" stroke="var(--color-neutral-700)" stroke-opacity="0.35" stroke-width="1"/>
  ${gridlines}${bars}${valueLabels}${axisLabels}
</svg>`;

console.log(svg);
