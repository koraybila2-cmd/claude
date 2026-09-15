---
name: ders-kitabi
description: |
  Bir ders/konu icin Google Drive'daki ders sunumlarini ve cikmis sinav sorularini bulup, tek bir uctan uca akista: icerigi okur/gerekirse OCR ile cikarir, konu semasi cikarir, cikmis sorularla yuksek-olasilikli (sik sorulan) konulari isaretler, sifirdan ders-kitabi derinliginde anlatim ve bolum sonu + genel deneme sinavi sorulari yazar, sonucu bicimlendirilmis bir Word/PDF kitap olarak uretir. NotebookLM/Gemini'ye gecmeyi, ayri bir OCR uygulamasi kullanmayi ve son metni elle Claude Design'a tasimayi gereksiz kilmak icin kullan.

  Kullanici "ders kitabi hazirla", "şu konunun/dersin kitabini cikar", "sunumlari kitaba cevir", "cikmis sorularla sinava hazirla", "notebooklm'e gerek kalmadan ozet/sema cikar", "bu dersi bastan anlat ve sinava hazirla" dediginde, ya da Drive'daki ders materyallerinden calisma kitabi / sinav hazirlik materyali istediginde bu skill'i kullan -- kullanici NotebookLM, OCR veya Claude Design'i acikca adlandirmasa bile aynı is akisini tarif ediyorsa tetikle.
---

# Ders Kitabı Otomasyonu

Bu skill, elle yürütülen şu zinciri tek oturumda yapar: **Drive'dan kaynak bulma → okuma/OCR → konu şeması → çıkmış sorularla eşleme → tam metin ders kitabı yazımı → Word/PDF kitap biçimi**. Hiçbir adım için ayrı bir uygulamaya (NotebookLM, ayrı bir OCR aracı, Claude Design) geçilmez; bu hem geçen süreyi hem de birden fazla aracın ayrı kullanım kotalarına takılma riskini ortadan kaldırır.

## 0. Girdiyi belirle

İstekte zaten geçmiyorsa tek soruda netleştir: (a) ders/konu adı, (b) Drive'da klasör/dosya ipucu (klasör linki, ders adı, hoca adı, dönem vb.). Çıktı formatı belirtilmemişse Word (.docx) varsay; PDF istenirse 3. adımdaki dönüşümü ekle. Birden fazla ders/konu isteniyorsa hepsini aynı anda işlemeye çalışma — her birini ayrı ayrı, bu akışın tamamıyla sırayla tamamla.

## 1. Kaynak toplama, çıkarma ve konu şeması

Yöntemin tamamı (Drive arama sorguları, OCR yedekleme sırası, konu şeması ve çıkmış-soru eşleme biçimi) için **references/kaynak-toplama.md** dosyasını oku ve uygula. Bu adımın sonunda elinde şunlar olmalı:

- `scratchpad/konu-semasi.md` — hiyerarşik konu haritası (Bölüm → Alt konu)
- `scratchpad/soru-analizi.md` — konu başına çıkmış soru eşlemesi ve "sık sorulan" işaretleri

Bu iki dosya NotebookLM'in yaptığı şemalandırmanın yerini alır — ayrı bir uygulamaya geçmeden burada üretilir.

## 2. Kitabı yaz

**references/kitap-uretimi.md** dosyasındaki manifest şemasına göre, konu şemasındaki her bölüm için tam ders kitabı derinliğinde anlatım (tanım, mekanizma, klinik korelasyon, gerekirse mnemonik) + bölüm sonu soruları yaz.

Bölümleri **tek tek işle**: her biri bitince `scratchpad/manifesto.json` içindeki ilgili bölüme ekle ve kullanıcıya kısa bir ilerleme notu ver ("N. bölüm tamamlandı: <başlık>"). Tüm dersi tek seferde yazmaya çalışmak hem bağlamı şişirir hem de kullanıcının şikayet ettiği "limit" sorununu burada yeniden yaratır — bölümlere bölmek ve ilerledikçe diske yazmak bunun çözümüdür.

Yüksek olasılıklı noktaları `{"style": "highYield", ...}` girdisiyle işaretle; kitapta görsel olarak vurgulanır. Klinik iddiaları PubMed/Consensus MCP araçlarıyla doğrulamak istersen bunu yalnızca yüksek-olasılıklı/karar-kritik noktalarla sınırla — her cümle için yapma, süre maliyeti yüksek.

## 3. Word kitabı üret

```bash
node .claude/skills/ders-kitabi/scripts/kitap_uret.js scratchpad/manifesto.json scratchpad/kitap.docx
```

`docx` (npm) paketi gerekir; ortamda yoksa `npm install docx --no-save` ile kurulabilir. Script kapak sayfası, otomatik İçindekiler, bölüm başına sayfa kesmesi, üst/alt bilgide sayfa numarası ve yüksek-olasılık vurgularını otomatik uygular — son metni elle Claude Design'a taşımaya gerek kalmaz. Manifest şeması ve doğrulama adımları için **references/kitap-uretimi.md**.

PDF isteniyorsa:

```bash
soffice --headless --convert-to pdf scratchpad/kitap.docx
```

## 4. Teslim

Üretilen dosyayı (.docx ve varsa .pdf) SendUserFile ile kullanıcıya gönder. `scratchpad/konu-semasi.md` ve `scratchpad/soru-analizi.md` dosyalarını da istenirse ayrıca paylaş — kullanıcı bazen kitaptan önce sadece şemayı görmek isteyebilir.

## Kapsam genişletme fikirleri (yalnızca istenirse)

- **Otomatik izleme**: Drive'da belirli bir klasöre yeni dosya düştükçe bu akışı tetiklemek için `create_trigger` ile bir Routine kurulabilir.
- **Çoklu ders/kitaplık**: Birden fazla ders için aynı akış tekrarlanıp her biri ayrı bölüm/dosya olarak üretilebilir.

Kullanıcı açıkça istemeden bu genişletmeleri devreye sokma.
