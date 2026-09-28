#!/usr/bin/env node
// HTML kitabı PDF'e basar. Kullanım: NODE_PATH=$(npm root -g) node render.js girdi.html cikti.pdf
const path = require("path");
const { chromium } = require("playwright");

const [, , inputPath, outputPath] = process.argv;
const CHROMIUM_PATH = process.env.CHROMIUM_PATH || "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";

(async () => {
  const browser = await chromium.launch({ executablePath: CHROMIUM_PATH });
  try {
    const page = await browser.newPage();
    await page.goto("file://" + path.resolve(inputPath), { waitUntil: "load", timeout: 180000 });
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({
      path: outputPath,
      format: "A4",
      printBackground: true,
      preferCSSPageSize: true,
      timeout: 600000,
    });
    console.log(`yazıldı: ${outputPath}`);
  } finally {
    await browser.close();
  }
})().catch((e) => {
  console.error("HATA:", e.message);
  process.exit(1);
});
