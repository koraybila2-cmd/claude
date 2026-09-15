---
name: ders-kitabi
description: |
  Bir ders/konu icin Google Drive'daki ders sunumlarini ve cikmis sinav sorularini bulup, tek bir uctan uca akista: icerigi okur/gerekirse OCR ile cikarir, konu semasi cikarir, cikmis sorularla yuksek-olasilikli (sik sorulan) konulari isaretler, sifirdan textbook derinliginde -- sunumla ve sorularla sinirli kalmayan, nedensellige dayali -- anlatim ve bolum sonu + genel deneme sinavi sorulari yazar, sonucu kullanicinin onayladigi Broadsheet tasarim sistemi gorunumunde gercek bir PDF dosyasi olarak (istenirse interaktif canvas veya Word olarak da) uretir. NotebookLM/Gemini'ye gecmeyi, ayri bir OCR uygulamasi kullanmayi ve son metni elle Claude Design'a tasimayi gereksiz kilmak icin kullan.

  Kullanici "ders kitabi hazirla", "şu konunun/dersin kitabini cikar", "sunumlari kitaba cevir", "cikmis sorularla sinava hazirla", "notebooklm'e gerek kalmadan ozet/sema cikar", "bu dersi bastan anlat ve sinava hazirla" dediginde, ya da Drive'daki ders materyallerinden calisma kitabi / sinav hazirlik materyali istediginde bu skill'i kullan -- kullanici NotebookLM, OCR veya Claude Design'i acikca adlandirmasa bile aynı is akisini tarif ediyorsa tetikle.
---

# Ders Kitabı Otomasyonu

Bu skill, elle yürütülen şu zinciri tek oturumda yapar: **Drive'dan kaynak bulma → okuma/OCR → konu şeması → çıkmış sorularla eşleme → textbook derinliğinde ders kitabı yazımı → Broadsheet görünümünde PDF (istenirse interaktif canvas veya Word)**. Hiçbir adım için ayrı bir uygulamaya (NotebookLM, ayrı bir OCR aracı, Claude Design) geçilmez; bu hem geçen süreyi hem de birden fazla aracın ayrı kullanım kotalarına takılma riskini ortadan kaldırır.

## 0. Girdiyi belirle

İstekte zaten geçmiyorsa tek soruda netleştir: (a) ders/konu adı, (b) Drive'da klasör/dosya ipucu (klasör linki, ders adı, hoca adı, dönem vb.). Çıktı formatı belirtilmemişse **Broadsheet görünümünde bir PDF dosyası** varsay — kullanıcı bunu standart format olarak onayladı (HTML/canvas linki değil, indirilebilir dosya). Kullanıcı özellikle interaktif/ekran versiyonu veya düzenlenebilir Word isterse 3B/3C adımına geç. Birden fazla ders/konu isteniyorsa hepsini aynı anda işlemeye çalışma — her birini ayrı ayrı, bu akışın tamamıyla sırayla tamamla.

## 1. Kaynak toplama, çıkarma ve konu şeması

Yöntemin tamamı (Drive arama sorguları, OCR yedekleme sırası, konu şeması ve çıkmış-soru eşleme biçimi, **arama sonuçlarının güvenilmezliğine karşı doğrulama adımı**) için **references/kaynak-toplama.md** dosyasını oku ve uygula. Bu adımın sonunda elinde şunlar olmalı:

- `scratchpad/konu-semasi.md` — hiyerarşik konu haritası (Bölüm → Alt konu)
- `scratchpad/soru-analizi.md` — konu başına çıkmış soru eşlemesi, "sık sorulan" işaretleri ve yıl bilgisi (varsa)

Bu iki dosya NotebookLM'in yaptığı şemalandırmanın yerini alır — ayrı bir uygulamaya geçmeden burada üretilir.

**Önemli:** `search_files` gerçekten var olan dosya/klasörleri sessizce atlayabiliyor (test edildi — sadece yeni dosyalarda değil, sabit/eski klasörlerde de). Bulduğun listeyi kullanıcıya göster ve eksik olup olmadığını sor; kullanıcı eksik bildirirse aramayı tekrarlama, doğrudan link/ID isteyip ID üzerinden çek. Detay: kaynak-toplama.md.

## 2. Kitabı yaz

Yazım felsefesi ve kuralları için **references/anlatim-tarzi.md** dosyasını oku ve harfiyen uygula — bu kullanıcının kendi tanımladığı, sabit talimattır (özet: sunum ve sorular sadece bağlam/kapsam göstergesidir, sınır değildir; textbook derinliği; nedensellik; konuyu sorular yokmuş gibi anlatıp sadece örtüştüğü yerlerde vurgu yap).

Konu şemasındaki her bölüm için şunları üret:
- Tam metin anlatım (anlatim-tarzi.md'ye göre)
- Yüksek olasılıklı/sık karıştırılan noktalar için ayrı, görsel olarak vurgulanacak kısa notlar
- Bölüm sonu pratik soruları (gerçek çıkmış sorular varsa kaynağıyla + konuyu pekiştirecek birkaç yeni soru)
- Mümkünse bir özet tablosu
- Konudan yıllara göre kaç soru çıktığı (soru-analizi.md'den)

Bölümleri **tek tek işle**: her biri bitince ilgili çıktı dosyasına (3A/3B/3C'de tarif edilen) ekle ve kullanıcıya kısa bir ilerleme notu ver ("N. bölüm tamamlandı: <başlık>"). Tüm dersi tek seferde yazmaya çalışmak hem bağlamı şişirir hem de kullanıcının şikayet ettiği "limit" sorununu burada yeniden yaratır — bölümlere bölmek ve ilerledikçe diske yazmak bunun çözümüdür. Konu çok kapsamlıysa anlatim-tarzi.md'nin izin verdiği gibi birden fazla mesaja yay, derinlikten ödün verme.

Klinik iddiaları PubMed/Consensus MCP araçlarıyla doğrulamak istersen bunu yalnızca emin olmadığın/karar-kritik noktalarla sınırla — her cümle için yapma, süre maliyeti yüksek.

## 3A. PDF üret (standart, varsayılan)

**references/kitap-uretimi-broadsheet.md** dosyasındaki adımları izle: `broadsheet-pdf-sablon/kitap-sablonu.html`'i şablon olarak kopyala, içeriği 2. adımda yazdığın metinle doldur, Playwright ile yerel Chromium üzerinden PDF'e bas, `pdftoppm` ile görsel doğrulama yap. Manuel bir "Claude Design'da yeniden dizayn etme" adımı yok — otomatik ve dosya çıktısı üretir.

## 3B. İnteraktif/ekran versiyonu isteniyorsa (opsiyonel)

Kullanıcı özellikle tıklanabilir/düzenlenebilir bir canvas isterse: `design` skill'ini (`Skill` tool) çağır, `broadsheet-sablon/Main.dc.html`'i şablon olarak kopyala, `.book-page` içeriğini doldur, seed → check → publish et (bkz. design skill'in kendi talimatları). Bu, Claude Design canvas'ı olarak yayınlanır — piksel-birebir Broadsheet, ama dosya değil web linkidir ve PDF'e çevirmek tarayıcıda elle "Export PDF" gerektirir.

## 3C. Word (.docx) isteniyorsa (opsiyonel)

```bash
node .claude/skills/ders-kitabi/scripts/kitap_uret.js scratchpad/manifesto.json scratchpad/kitap.docx
```

`docx` (npm) paketi gerekir; ortamda yoksa `npm install docx --no-save` ile kurulabilir. Script kapak sayfası, otomatik İçindekiler, bölüm başına sayfa kesmesi, üst/alt bilgide sayfa numarası ve yüksek-olasılık vurgularını otomatik uygular (Broadsheet'in kendisi değil, genel bir Word kitap biçimi). Manifest şeması için **references/kitap-uretimi.md**.

## 4. Teslim

Üretilen PDF'i (standart durumda) `SendUserFile` ile gönder. 3B/3C de üretildiyse onları da ayrıca gönder/ilet. `scratchpad/konu-semasi.md` ve `scratchpad/soru-analizi.md` dosyalarını da istenirse paylaş — kullanıcı bazen kitaptan önce sadece şemayı görmek isteyebilir.

## Kapsam genişletme fikirleri (yalnızca istenirse)

- **Otomatik izleme**: Drive'da belirli bir klasöre yeni dosya düştükçe bu akışı tetiklemek için `create_trigger` ile bir Routine kurulabilir.
- **Çoklu ders/kitaplık**: Birden fazla ders için aynı akış tekrarlanıp her biri ayrı bölüm/dosya olarak üretilebilir.

Kullanıcı açıkça istemeden bu genişletmeleri devreye sokma.
