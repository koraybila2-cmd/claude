#!/usr/bin/env node
// Broadsheet-stilinde, bagimsiz (DC sarmalayicisiz) bir HTML kitap sayfasini PDF'e basar.
// Kullanim: node kitap_pdf_uret.js girdi.html cikti.pdf
// Playwright + Chromium bu ortamda onceden kurulu; farkli bir kurulumda
// executablePath'i o ortamin chromium binary'sine gore guncelleyin.

const path = require("path");
const { chromium } = require("playwright");

const [, , inputPath, outputPath] = process.argv;
if (!inputPath || !outputPath) {
  console.error("Kullanim: node kitap_pdf_uret.js <girdi.html> <cikti.pdf>");
  process.exit(1);
}

const CHROMIUM_PATH = process.env.CHROMIUM_PATH || "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";

(async () => {
  const browser = await chromium.launch({ executablePath: CHROMIUM_PATH });
  try {
    const page = await browser.newPage();
    await page.goto("file://" + path.resolve(inputPath), { waitUntil: "networkidle" });
    // Google Fonts webfont'unun yuklenmesini garantiye al.
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({
      path: outputPath,
      format: "A4",
      printBackground: true,
      preferCSSPageSize: true,
      margin: { top: "0mm", bottom: "0mm", left: "0mm", right: "0mm" },
    });
    console.log(`Yazildi: ${outputPath}`);
  } finally {
    await browser.close();
  }
})().catch((e) => {
  console.error("HATA:", e.message);
  process.exit(1);
});
