const path = require("path");
const { chromium } = require("playwright");
const [, , inputPath, outputPath, title] = process.argv;
(async () => {
  const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
  const page = await browser.newPage();
  await page.goto("file://" + path.resolve(inputPath), { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({
    path: outputPath, format: "A4", printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: `<div style="width:100%;font-family:Georgia,serif;font-size:8px;color:#57534e;padding:0 20mm;display:flex;justify-content:space-between;"><span>${title || ""}</span><span class="pageNumber"></span></div>`,
  });
  await browser.close();
  console.log("Yazildi:", outputPath);
})().catch((e) => { console.error("HATA:", e.message); process.exit(1); });
