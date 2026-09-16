# Veri Görselleştirme (Grafik, Tablo, Sayısal Veri)

Kullanıcının onayladığı kalıcı kural: metinde ham sayısal/karşılaştırmalı veri geçtiğinde bunu düz cümle içinde boğmak yerine **gerekli yerlerde** grafik, zenginleştirilmiş tablo veya öne çıkan sayısal veri (stat) olarak göster. Bu, her bölümde otomatik uygulanacak bir adımdır — istisnası, verinin gerçekten grafiğe değecek bir karşılaştırma/büyüklük içermediği durumlardır (aşağıya bakın).

## Önce karar ver: grafik mi, tablo mu, düz metin mi?

`dataviz` skill'inin "is it even a chart" ayrımı burada da geçerli:

- **Büyüklük/karşılaştırma içeren sayısal seri** (yıllara göre soru sayısı, prevalans, laboratuvar değer aralıkları, duyarlılık/özgüllük yüzdeleri) → **bar chart**.
- **Kategorik/referans bilgi** (mekanizma karşılaştırması, ilaç-etki eşleşmesi, soru kaynak listesi) → **tablo** olarak kalmalı, grafiğe zorlanmamalı — bkz. `dataviz` skill'inin anti-patterns.md dosyası: "sekiz kategorik renk hikaye tek sayıyken" gibi hatalar.
- **Tek, çarpıcı bir sayı** (ör. "%95 kristal pozitifliği") → ayrı bir grafiğe gerek yok, metin içinde **kalın/vurgulu** yazmak yeterli.
- Elindeki veri 2 kategoriden azsa veya tek bir çubuğa sığıyorsa grafik yapma (`dataviz`'in "one-bar bar chart" anti-pattern'i) — direkt cümle içinde söyle.

## Broadsheet'e uygulanan somut kurallar

Tam metodoloji için önce `dataviz` skill'ini yükle (`Skill` tool, `skill: "dataviz"`) — form seçimi, işaret (mark) ölçüleri ve anti-pattern listesi oradan gelir. Broadsheet'in kısıtlı paleti (sadece cyan + magenta + nötr gri) bu metodolojiye şöyle uygulanır:

- **Bu kitaplardaki grafiklerin neredeyse tamamı tek-seridir** (yıl→soru sayısı, kategori→değer). Tek seri = **tek renk** (`var(--color-accent-700)`, cyan) — `dataviz`'in "sequential = one hue" kuralı. Birden fazla seri gerekiyorsa ikinci seri için magenta (`var(--color-accent-2-900)`) kullanılabilir ama Broadsheet'in "iki accent'i aynı küçük bileşende kullanma" kuralı burada da geçerli — iki seri varsa bile sade tut.
- **Tek seri lejant istemez** — başlık/alt başlık zaten neyin çizildiğini söylüyor.
- **Bu bir print/statik PDF'tir, hover/tooltip yok** — bu yüzden `dataviz`'in "tooltip tek okuma yolu olmasın" kuralı burada "her çubuğun değeri doğrudan çubuğun ucunda yazılı olsun" haline gelir. Bu kitaplardaki küçük veri setlerinde (tipik 5-8 kategori) her çubuğu etiketlemek doğru ve gereklidir.
- **İşaret ölçüleri:** çubuk ≤24px kalınlık, üst köşeler 4px yuvarlatılmış + taban keskin, izgara çizgileri (gridline) ince/saydam/düz (asla kesikli), çubuğun kendi rengi yerine metin renginde (var(--color-text)) değer etiketi.
- Grafik bir `<figure>` içinde, altında küçük italik bir `<figcaption>` ile verilir (kaynağı belirtir) — Broadsheet'in "her tabloya benzer sade referans" hissini korur.

## Hazır araç: `scripts/bar_chart_svg.js`

Tek-seri bar chart SVG'sini elle hesaplamak yerine bu scripti kullan:

```bash
node .claude/skills/ders-kitabi/scripts/bar_chart_svg.js girdi.json > cikti-svg.txt
```

`girdi.json` şeması:

```json
{
  "width": 640, "height": 300,
  "ariaLabel": "Kısa açıklama",
  "unit": "",
  "categories": [{"label": "2018-2019", "value": 4}, {"label": "2019", "value": 3}]
}
```

Çıktı, doğrudan HTML'e yapıştırılacak bir `<svg>...</svg>` bloğudur — Broadsheet CSS değişkenlerini (`var(--color-accent-700)` vb.) referans alır, bu yüzden sayfanın `<style>` bloğunda bu değişkenler tanımlı olduğu sürece renkler otomatik doğru çıkar. Yapıştırdıktan sonra **mutlaka PDF'e basıp görsel olarak kontrol et** (etiket çakışması, taşma) — `dataviz`'in 7. adımı ("render edip bak") burada da geçerli.

## Standart kullanım yeri: "Bu Konudan Yıllara Göre Kaç Soru Çıktı"

Her bölümün sonunda zaten üretilen bu tablo artık **varsayılan olarak bar chart'a çevrilir** (tablo tutmaya gerek yok, grafik zaten her değeri doğrudan etiketliyor). Kaynak kod deseni için mevcut bir bölümdeki (ör. `broadsheet-pdf-sablon/kitap-sablonu.html`) bu chart'ı örnek al.

## Diğer kullanım yerleri (içerik bazlı, zorlamadan)

Metin içinde gerçek, karşılaştırmaya değer sayısal veri geçtiğinde (epidemiyolojik prevalans, laboratuvar eşik değerleri, duyarlılık/özgüllük gibi) aynı script ile küçük bir grafik ekle — ama her paragrafı grafiğe çevirme, sadece verinin görsel karşılaştırmayla gerçekten daha anlaşılır olacağı yerlerde (`dataviz`'in "is it even a chart" tablosuna göre karar ver).
