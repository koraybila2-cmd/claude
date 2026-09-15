# Kaynak Toplama, Çıkarma ve Konu Şeması

## 1. Drive'da kaynakları bulma

`mcp__Google_Drive__search_files` ile ara. Önemli kısıt: `title contains` / `fullText contains` içine dosya türü kelimeleri (sunum, slayt, pdf, doküman) **koyma** — bunlar `mimeType` koşuluna gider.

Örnek sorgular:

- Sunumlar: `fullText contains '<konu>' and (mimeType = 'application/vnd.google-apps.presentation' or mimeType = 'application/pdf' or mimeType contains 'officedocument.presentationml')`
- Çıkmış sorular: `title contains '<konu>' and (title contains 'sınav' or title contains 'çıkmış' or title contains 'soru')` — anahtar kelimeleri tek tek de deneyin, gerçek başlıklandırma kullanıcıdan kullanıcıya değişir.
- Belirli klasörden: `parentId = '<folderId>'` (klasör linki/ID'si kullanıcıdan istenebilir; linkteki `/folders/<ID>` kısmı folderId'dir).

Klasör/isim belirsizse `list_recent_files` ile keşif yapılabilir. Bulunan dosya listesini kullanıcıya kısaca özetle; eşleşme net değilse (çok fazla alakasız sonuç) hangi dosyaların dahil edileceğini sor, net ise onay beklemeden devam et.

## 2. İçerik çıkarma (OCR dahil)

Öncelik sırası:

1. **`read_file_content`** — her dosya için önce bunu dene. Google Slides/Docs, PDF, DOCX, PPTX, PNG/JPG dahil çoğu formatı native olarak metne çevirir; taranmış/resim ağırlıklı slaytlarda da genelde makul sonuç verir çünkü bu katman kendi içinde bir OCR adımı içerir.
2. Çıktı bozuk/eksik görünüyorsa (çok kısa, anlamsız karakter yığını, slayt sayısına göre orantısız az metin): `download_file_content` ile ham dosyayı al ve Claude'un çok modlu okuma yeteneğiyle (Read tool) sayfaları doğrudan görsel olarak oku. El yazısı olmayan taranmış slaytlarda genelde en güvenilir yol budur.
3. Çok sayıda dosya birikip tek tek okumak yavaş kalıyorsa: `mcp__PDF_net__upload_file` ile yükleyip `mcp__PDF_net__find_in_documents` ile toplu/semantik arama yap.
4. Az sayıda ama ağır taranmış PDF varsa `pdf` skill'ini çağır — pytesseract tabanlı toplu OCR akışı içerir.

Her dosyanın çıkarılan metnini kaydet: `scratchpad/kaynaklar/<tur>/<dosya-adi>.md` (`tur` = `sunum` veya `soru`). Bu hem tekrar indirmeyi önler hem de sohbet bağlamını şişirmeden ilerlemeyi kalıcı hale getirir — kullanıcının bahsettiği kota/limit sorununun asıl çözümü budur: her dosya bir kere işlenir, sonucu diskte kalır.

## 3. Konu şeması çıkarma (NotebookLM'in yerine)

Tüm sunum metinleri toplandıktan sonra, ayrı bir araca geçmeden, doğrudan hiyerarşik bir konu şeması üret: Bölüm → Alt konu → (varsa) alt-alt konu. Şemayı `scratchpad/konu-semasi.md` içine yaz; her düğümü kaynaklandığı sunum dosyasına referansla (izlenebilirlik ve sonradan kontrol için).

## 4. Çıkmış sorularla eşleme

- Her çıkmış soruyu konu şemasındaki en yakın düğüme eşle.
- Düğüm başına soru sayısını say → 3 veya daha fazla soru gelen düğümleri "yüksek olasılıklı / sık sorulan" işaretle.
- Eşlemeyi `scratchpad/soru-analizi.md` içine yaz: konu → [soru listesi + kaynak (yıl/sınav adı, biliniyorsa)].

Bu iki dosya (`konu-semasi.md`, `soru-analizi.md`) SKILL.md'nin 2. adımındaki kitap yazımının doğrudan girdisidir.
