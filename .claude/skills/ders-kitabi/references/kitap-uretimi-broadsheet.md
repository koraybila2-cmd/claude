# Broadsheet Tasarım Sistemiyle PDF Kitap (Standart Format)

Bu, kullanıcının onayladığı **standart çıktı biçimidir**: Broadsheet'in görsel dilini (Source Serif 4, near-black metin/paper-white zemin, cyan + magenta spot renkler, çerçevesiz/boşlukla ayrılan düzen) taşıyan, gerçek bir **PDF dosyası**. Kullanıcı açıkça bir web linki/interaktif canvas istemedikçe HTML/Artifact linki DEĞİL, indirilebilir bir dosya üretilir.

`../broadsheet-pdf-sablon/kitap-sablonu.html` çalışan, PDF'e basılıp görsel olarak doğrulanmış gerçek bir örnektir (konu: Romatoloji — Aşırı Duyarlılık Reaksiyonları, PAÜTF Dönem 3 Modül 2). Yeni bir ders notu için bu dosyayı **şablon olarak kopyala**: `<head>` içindeki `<style>` bloğunu ve genel iskeleti aynen koru, `<main class="book-page">` içindeki başlık/bölüm/tablo/soru içeriğini yeni konuyla değiştir.

## Neden Claude Design canvas'ı değil de bu

Daha önce aynı içerik Claude Design'ın DC/canvas sistemiyle (`../broadsheet-sablon/`) yayınlanmıştı, ama o yol bir web linki üretiyor ve gerçek PDF'e çevirmek tarayıcıda elle tıklanan bir "Export PDF" adımı gerektiriyor — tam otomasyon hedefiyle çelişiyor. Bu yüzden standart yöntem, aynı görsel dili bağımsız bir HTML dosyasında yeniden üretip yerel Chromium (Playwright) ile doğrudan PDF'e basmak: hiçbir manuel adım yok, dosya doğrudan teslim edilebiliyor.

**Not:** Buradaki renk/font değerleri Broadsheet'in belgelenen tokenlarının (aşağıdaki tablo) yerel bir yaklaşıklamasıdır — piksel-birebir aynısı değildir, çünkü tasarım sisteminin derlenmiş CSS paketi yalnızca Claude Design canvas'ı içinde çözülüyor. Kullanıcı pikselinde birebir/interaktif bir sürüm isterse `../broadsheet-sablon/` (design skill, DC canvas) kullan — o yol için references altında ayrı bir not yoktu, `design` skill'ini `Skill` tool ile çağırıp `broadsheet-sablon/Main.dc.html`'i şablon al.

## Kullanılan Broadsheet tokenları (literal yaklaşıklama)

| Token | Değer |
|---|---|
| `--color-bg` | `#f3f2f2` |
| `--color-text` | `#201e1d` |
| `--color-accent` (cyan) | `#0088b0` |
| `--color-accent-2` (magenta) | `#d6006c` |
| Font | Google Fonts "Source Serif 4" (heading + body) |

Koyu tonlar (`-700`/`-900` gibi) `color-mix(in oklch, <renk>, black N%)` ile türetiliyor — bu, gerçek OKLCH ramp'ının yaklaşık bir taklidi.

## Kullanılan sınıflar (sabit tut, yeniden icat etme)

Aynı `.book-page`, `.book-kicker`, `.book-title`, `.book-byline`, `.book-section`, `.book-h2`, `.book-p`/`.book-list`, `.tag.tag-accent-2` + `.highlight-p` (sadece "sık karıştırılan/sorulan" vurgusu için), `.table`, `.qa-list` + `.card` (`.card-kicker`, `.card-title`, `.card-body`) sınıfları — bkz. `kitap-sablonu.html`'in `<style>` bloğu. Broadsheet kuralı aynen geçerli: gövde bölümlerini ayırmak için çerçeve/çizgi kullanma, sadece boşluk; `.card` yalnızca gerçekten ayrık, listelenebilir öğeler (sorular) için.

## Üretim adımları

1. `broadsheet-pdf-sablon/kitap-sablonu.html`'i çalışma dizinine kopyala, `<main class="book-page">` içeriğini yeni konunun bölüm/tablo/soru içeriğiyle değiştir (SKILL.md 2. adımda ve `anlatim-tarzi.md`'de tarif edilen yazım tarzıyla yazılan metni buraya taşı). `<title>` etiketini de güncelle.
2. PDF'e bas:
   ```bash
   GLOBAL_NM=$(npm root -g)
   NODE_PATH="$GLOBAL_NM" node .claude/skills/ders-kitabi/scripts/kitap_pdf_uret.js <konu>.html <konu>.pdf
   ```
   Script Playwright + yerel Chromium kullanır (`/opt/pw-browsers/chromium-*/chrome-linux/chrome` — bu ortamda önceden kurulu). `npm root -g` boş dönerse veya farklı bir ortamdaysan `playwright` paketinin kurulu olduğu yolu bul ve `NODE_PATH` ile ver; Chromium binary'si farklı bir sürüm/yoldaysa scriptin başındaki `CHROMIUM_PATH` ortam değişkenini o yola ayarla.
3. **Doğrula:** `pdfinfo <konu>.pdf` ile sayfa sayısını kontrol et, `pdftoppm -jpeg -r 100 <konu>.pdf sayfa` ile en az ilk ve son sayfayı görsele çevirip Read tool ile göz gezdir — özellikle tabloların ve soru kartlarının doğru kırıldığını (sayfa ortasında bölünmediğini) kontrol et. `pdftoppm` ortamda yoksa `apt-get install -y poppler-utils` ile kurulabilir (bu ortamda sistem paketleri oturumlar arası kalıcı olmayabilir — her ihtiyaç anında tekrar kurmaktan çekinme).
4. Üretilen PDF'i `SendUserFile` ile kullanıcıya gönder.

## Uzun ders notlarında dikkat

`page.pdf()` her zaman tam A4 sayfalar üretir, DC canvas'taki gibi "frame yüksekliği" ayarına gerek yoktur — taşma/kırpılma riski yoktur, script kaç sayfa gerekiyorsa o kadar üretir. Yine de çok uzun bir bölümde `break-inside: avoid` kurallarının (tablo, kart, vurgu paragrafı) sayfa ortasında çirkin kesilmeleri önlediğini doğrulama adımında kontrol et.
