# Kitap Yazımı ve Word/PDF Üretimi

## 1. Bölüm bölüm yazım

`konu-semasi.md` + `soru-analizi.md` kullanarak her ana bölüm için tam ders kitabı derinliğinde metin yaz: tanımlar, mekanizmalar, klinik korelasyon, gerekirse mnemonikler. Yüksek olasılıklı noktaları düz yazı içinde ayrı bir `highYield` paragraf girdisi olarak işaretle (aşağıdaki şema) — kitapta görsel olarak vurgulanır.

Her bölümün sonuna "Bölüm Sonu Soruları" ekle: gerçek çıkmış sorular (aynen, kaynağıyla) + konuya uygun birkaç yeni benzer soru (kaynak belirtme — kaynaksız olması "yeni" olduğunu ima eder).

Uzun dersler için bölümleri **tek tek** yaz; her biri bitince `scratchpad/manifesto.json` içindeki ilgili bölümü tamamla. Tüm kitabı tek seferde belleğe/bağlama yüklemeye çalışma — SKILL.md'de belirtildiği gibi bu, kullanıcının bahsettiği limit sorununu burada yeniden yaratır.

## 2. Manifest şeması

`scripts/kitap_uret.js` şu JSON yapısını bekler:

```json
{
  "title": "Kitabın başlığı",
  "subtitle": "Alt başlık, opsiyonel",
  "date": "Tarih/dönem, opsiyonel",
  "chapters": [
    {
      "title": "1. Bölüm: ...",
      "sections": [
        {
          "heading": "Alt başlık",
          "paragraphs": [
            "düz metin paragrafı",
            { "list": ["madde 1", "madde 2"] },
            { "style": "highYield", "text": "vurgulanacak, sık sorulan metin" }
          ]
        }
      ],
      "practiceQuestions": [
        { "question": "...", "answer": "...", "source": "opsiyonel, örn. '2023 Vize - Soru 5'" }
      ]
    }
  ],
  "finalExam": {
    "title": "opsiyonel, varsayılan 'Genel Deneme Sınavı'",
    "questions": [{ "question": "...", "answer": "..." }]
  }
}
```

`paragraphs` dizisindeki her öğe ya düz string, ya `{"list": [...]}` (madde imli liste), ya da `{"style": "highYield", "text": "..."}` olabilir.

## 3. Docx üretimi

```bash
node .claude/skills/ders-kitabi/scripts/kitap_uret.js scratchpad/manifesto.json scratchpad/kitap.docx
```

Script `docx` (npm, v9+) paketine ihtiyaç duyar. Ortamda `require('docx')` başarısız olursa: `npm install docx --no-save` (registry'ye proxy üzerinden erişilebilir, test edildi).

Üretilen belge: kapak sayfası → otomatik İçindekiler alanı (Word/LibreOffice'te ilk açılışta alanların güncellenmesi istenebilir — kabul et / F9) → her bölüm yeni sayfada başlar → üst bilgide kitap başlığı, alt bilgide sayfa numarası → `highYield` paragrafları kırmızı kenarlıkla vurgulanır.

## 4. Doğrulama

Mümkünse docx skill'inin kendi kuralını uygula — görmeden teslim etme:

```bash
soffice --headless --convert-to pdf scratchpad/kitap.docx
pdftoppm -jpeg -r 100 kitap.pdf sayfa
```

sonra `sayfa-*.jpg` dosyalarını Read tool ile aç ve göz gezdir.

**Not:** bazı oturumlarda `soffice` (LibreOffice) kurulu olsa bile headless dönüşüm hatalı davranabilir ("source file could not be loaded" — herhangi bir dosya için, sadece üretilenler için değil). Bu durumda önce `apt-get update` çalıştırıp tekrar dene; hâlâ çalışmıyorsa ortamın kendi kısıtıdır, script çıktısını sorgulamana gerek yok. Bu durumda yerine:

- `file scratchpad/kitap.docx` → "Microsoft Word 2007+" dönmeli.
- `unzip -l scratchpad/kitap.docx` → `word/document.xml`, `word/styles.xml`, `word/numbering.xml`, `word/header1.xml`, `word/footer1.xml` içermeli.
- Metin sırasını doğrudan XML'den kontrol et:
  ```bash
  python3 -c "
  import xml.etree.ElementTree as ET
  ns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'
  t = ET.parse('unpacked/word/document.xml')
  print(' | '.join(x.text for x in t.getroot().iter(ns) if x.text))
  "
  ```
  (önce `unzip -o scratchpad/kitap.docx -d unpacked` ile aç). Başlıkların, bölüm sırasının ve soru-cevapların doğru sırada göründüğünü teyit et.

## 5. PDF isteniyorsa

`soffice --headless --convert-to pdf scratchpad/kitap.docx` komutu aynı zamanda nihai PDF çıktısını üretir — ekstra bir adım gerekmez. `soffice` bu oturumda çalışmıyorsa kullanıcıya PDF'in bir sonraki normal oturumda (bu araç genelde kuruludur) üretilebileceğini belirt ve .docx'i teslim et.

## 6. Teslim

Üretilen `.docx` (ve varsa `.pdf`) dosyasını `SendUserFile` ile gönder.
