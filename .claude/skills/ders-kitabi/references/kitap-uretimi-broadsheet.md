# Broadsheet Tasarım Sistemiyle Kitap Sayfası (Standart Format)

Bu, kullanıcının onayladığı **standart görsel çıktı biçimidir** — bundan sonra her ders notu bu şekilde üretilir. Kullanıcının daha önce elle yaptığı "son metni Claude Design'da kitap formatında dizayn ettirme" adımının otomatikleştirilmiş hâlidir.

`../broadsheet-sablon/Main.dc.html` çalışan, yayınlanıp doğrulanmış gerçek bir örnektir (konu: Romatoloji — Aşırı Duyarlılık Reaksiyonları, PAÜTF Dönem 3 Modül 2). Yeni bir ders notu için bu dosyayı **şablon olarak kopyala**: `<helmet>` bloğunu (tasarım sistemi bağlantıları + `<style>` sınıfları) ve genel iskeleti aynen koru, `<div class="book-page">` içindeki başlık/bölüm/tablo/soru içeriğini yeni konuyla değiştir.

## Ön koşul: Broadsheet tasarım sistemi bağlı olmalı

Bu şablon `_ds/broadsheet-f4e082ee-1adb-404a-b470-6741e6a9a194/` yoluna bağımlıdır — bu yol, kullanıcının sohbete eklediği "Broadsheet (design system)" attachment'ı sayesinde çalışır. Bu attachment mevcut değilse (farklı/yeni bir oturumda tekrar eklenmemişse) kullanıcıdan Broadsheet tasarım sistemini tekrar eklemesini iste; o ana kadar **references/kitap-uretimi.md** içindeki Word/PDF akışına geç.

## Kullanılan sınıflar (sabit tut, yeniden icat etme)

| Sınıf | Ne için |
|---|---|
| `.book-page` | Sayfa kapsayıcısı (max-width 780px, kenar boşlukları) |
| `.book-kicker` | Üstte küçük, izlenimci etiket — ör. "PAÜTF · Dönem 3 · Modül 2 · \<ders adı\>" |
| `.book-title` | H1, bölüm/konu başlığı |
| `.book-byline` | İtalik kaynak satırı — ör. "Kaynak: \<hoca adı\> sunumu" |
| `.book-section` | Her ana bölüm için sarmalayıcı — sadece boşlukla ayırır, çerçeve/çizgi yok |
| `.book-h2` | Bölüm içi alt başlık |
| `.book-p` / `.book-list` | Gövde metni / madde işaretli liste |
| `.tag.tag-accent-2` + `.highlight-p` | "Sık karıştırılan / sık sorulan" vurgusu — **sadece bunun için** magenta kullan, başka hiçbir yerde |
| `.table` | Bölüm özeti gibi tablo verileri |
| `.qa-list` + `.card.elev-sm` (`.card-kicker`, `.card-title`, `.card-body`) | Bölüm sonu soru-cevap listesi |

Broadsheet'in temel kuralı: gövde bölümlerini ayırmak için çerçeve/çizgi kullanma — sadece boşluk (whitespace). `.card` yalnızca gerçekten ayrık, listelenebilir öğeler (sorular) için kullanılır, düzen elemanı olarak değil.

## Boyutlandırma (canvas.json)

Tek artboard, `"print": "flow"` (kitap bölümü uzun, akan bir belge — sabit sayfa değil), genişlik `794` (A4 @ 96dpi — yazdırma/PDF dışa aktarımı için doğru ölçü). Yükseklik (`h`) içeriğe göre cömert tutulmalı: bu örnekte (7 bölüm + özet tablosu + 5 soru kartı) `5200` kullanıldı. Daha uzun bir ders notunda `h`'yi artır — taşma/kırpılma tek başarısızlık modudur; fazla yükseklik sadece sayfa arka planını boyar, zararsızdır.

## Üretim adımları

1. `broadsheet-sablon/Main.dc.html` dosyasını çalışma dizinine kopyala, `.book-page` içeriğini yeni konunun bölüm/tablo/soru içeriğiyle değiştir (SKILL.md'nin 2. adımında yazılan bölüm metinlerini buraya taşı).
2. `design` skill'ini çağır (`Skill` tool, `skill: "design"`) — bu sana seed-canvas.mjs / payload.template.html konumunu ve güncel `contract` sürüm numarasını verir. Bunlar zamanla değişebilir; burada sabitlenmiş bir komut yerine skill'in o anki talimatına güven.
3. `node <design-skill-base>/seed-canvas.mjs --template <design-skill-base>/payload.template.html --out <cikti>.html --title "<konu başlığı>" --artboard Main.dc.html --canvas canvas.json`
4. `node <design-skill-base>/seed-canvas.mjs --check <cikti>.html` — `ok:` satırını doğrula.
5. İlk yayınlamadan önce `artifact-capabilities` skill'ini çağırıp bu kullanıcının roster'ını öğren; `self` (artifact-publish) ve `downloads` listede ise `Artifact` tool ile `capabilities: {"self": {}, "downloads": {}}` ve design skill'in belirttiği `contract` değeriyle yayınla.
6. Karmaşık/uzun bir bölümse, design skill'in kendi kuralı gereği yayınladıktan sonra çalışma dosyalarını (yayınlanan çıktıyı değil) arka planda bir ajanla veya kendin tekrar gözden geçir.

## Not

Word/PDF çıktısı hâlâ isteniyorsa (ör. yazdırıp üzerine not almak için) **references/kitap-uretimi.md** kullanılabilir — ama varsayılan/standart çıktı budur, kullanıcı aksini belirtmedikçe bunu üret.
