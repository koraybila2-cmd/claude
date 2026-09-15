#!/usr/bin/env node
// Bir "kitap manifestosu" (JSON) alır, ders-kitabı formatında bir .docx üretir.
// Kullanim: node kitap_uret.js manifesto.json cikti.docx
// Manifesto semasi icin ../references/manifesto-semasi.md dosyasina bakin.

const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, TableOfContents,
  Header, Footer, PageNumber, AlignmentType, PageBreak, LevelFormat,
  BorderStyle, convertInchesToTwip,
} = require("docx");

const [, , manifestPath, outPath] = process.argv;
if (!manifestPath || !outPath) {
  console.error("Kullanim: node kitap_uret.js <manifesto.json> <cikti.docx>");
  process.exit(1);
}

const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf-8"));

const HIGHYIELD_COLOR = "B00020";
const MUTED_COLOR = "666666";
const BULLET_REF = "madde-listesi";

function paragraphFromEntry(entry) {
  if (typeof entry === "string") {
    return [new Paragraph({ children: [new TextRun(entry)], spacing: { after: 160 } })];
  }
  if (entry.list) {
    return entry.list.map(
      (item) =>
        new Paragraph({
          numbering: { reference: BULLET_REF, level: 0 },
          spacing: { after: 60 },
          children: [new TextRun(item)],
        }),
    );
  }
  if (entry.style === "highYield") {
    return [
      new Paragraph({
        spacing: { after: 160 },
        border: { left: { style: BorderStyle.SINGLE, size: 12, color: HIGHYIELD_COLOR, space: 8 } },
        children: [
          new TextRun({ text: "Sik Sorulur: ", bold: true, color: HIGHYIELD_COLOR }),
          new TextRun({ text: entry.text }),
        ],
      }),
    ];
  }
  return [new Paragraph({ children: [new TextRun(entry.text)], spacing: { after: 160 } })];
}

function sectionToParagraphs(section) {
  const out = [new Paragraph({ text: section.heading, heading: HeadingLevel.HEADING_2 })];
  (section.paragraphs || []).forEach((p) => out.push(...paragraphFromEntry(p)));
  return out;
}

function qaToParagraphs(items, startIndex) {
  const out = [];
  items.forEach((qa, i) => {
    out.push(
      new Paragraph({
        spacing: { before: 160, after: 60 },
        children: [new TextRun({ text: `${startIndex + i}. ${qa.question}`, bold: true })],
      }),
    );
    out.push(
      new Paragraph({
        spacing: { after: qa.source ? 20 : 120 },
        indent: { left: convertInchesToTwip(0.25) },
        children: [new TextRun({ text: qa.answer })],
      }),
    );
    if (qa.source) {
      out.push(
        new Paragraph({
          indent: { left: convertInchesToTwip(0.25) },
          spacing: { after: 120 },
          children: [new TextRun({ text: qa.source, italics: true, color: MUTED_COLOR, size: 18 })],
        }),
      );
    }
  });
  return out;
}

const children = [];

children.push(
  new Paragraph({
    spacing: { before: 2400 },
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: manifest.title, bold: true, size: 56 })],
  }),
);
if (manifest.subtitle) {
  children.push(
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 200 },
      children: [new TextRun({ text: manifest.subtitle, size: 30, color: MUTED_COLOR })],
    }),
  );
}
if (manifest.date) {
  children.push(
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 600 },
      children: [new TextRun({ text: manifest.date, size: 22, color: MUTED_COLOR })],
    }),
  );
}
children.push(new Paragraph({ children: [new PageBreak()] }));

children.push(new Paragraph({ text: "Icindekiler", heading: HeadingLevel.HEADING_1 }));
children.push(new TableOfContents("Icindekiler", { hyperlink: true, headingStyleRange: "1-2" }));
children.push(new Paragraph({ children: [new PageBreak()] }));

(manifest.chapters || []).forEach((chapter, idx) => {
  if (idx > 0) children.push(new Paragraph({ children: [new PageBreak()] }));
  children.push(new Paragraph({ text: chapter.title, heading: HeadingLevel.HEADING_1 }));
  (chapter.sections || []).forEach((section) => children.push(...sectionToParagraphs(section)));
  if (chapter.practiceQuestions && chapter.practiceQuestions.length) {
    children.push(
      new Paragraph({ text: "Bolum Sonu Sorulari", heading: HeadingLevel.HEADING_2, spacing: { before: 300 } }),
    );
    children.push(...qaToParagraphs(chapter.practiceQuestions, 1));
  }
});

if (manifest.finalExam && manifest.finalExam.questions && manifest.finalExam.questions.length) {
  children.push(new Paragraph({ children: [new PageBreak()] }));
  children.push(
    new Paragraph({ text: manifest.finalExam.title || "Genel Deneme Sinavi", heading: HeadingLevel.HEADING_1 }),
  );
  children.push(...qaToParagraphs(manifest.finalExam.questions, 1));
}

const doc = new Document({
  numbering: {
    config: [
      {
        reference: BULLET_REF,
        levels: [
          {
            level: 0,
            format: LevelFormat.BULLET,
            text: "•",
            alignment: AlignmentType.LEFT,
            style: {
              paragraph: {
                indent: { left: convertInchesToTwip(0.35), hanging: convertInchesToTwip(0.25) },
              },
            },
          },
        ],
      },
    ],
  },
  sections: [
    {
      properties: {},
      headers: {
        default: new Header({
          children: [
            new Paragraph({
              alignment: AlignmentType.RIGHT,
              children: [new TextRun({ text: manifest.title, size: 16, color: MUTED_COLOR })],
            }),
          ],
        }),
      },
      footers: {
        default: new Footer({
          children: [
            new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [new TextRun({ children: [PageNumber.CURRENT] })],
            }),
          ],
        }),
      },
      children,
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(outPath, buf);
  console.log(`Yazildi: ${outPath}`);
});
