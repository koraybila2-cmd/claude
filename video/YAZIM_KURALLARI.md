# Anlatım metni yazım kuralları

Modül 4 kitaplarının her bölüm dosyası (`kaynak/modul4/kitaplar/m4kN/*.html`) anlatıcı sesli bir videoya dönüşür. Bunun için her bölüm dosyasına bir klasör açılır ve iki dosya yazılır:

- `parcalar.txt`: seslendirilecek anlatım metni. Ses modeli bu metni **kelimesi kelimesine** okur.
- `sahne.json`: `parcalar.txt`'teki her satır okunurken ekranda hangi kitap bloğunun vurgulanacağı.

Videoda ekranda kitabın kendi sayfası durur. Okunan blok vurgulanır ve sayfa sesle birlikte kayar. Satırların sesteki yeri konuşma tanımayla otomatik bulunur.

Örnek bölüm: `video/k5b3/` (kaynak `m4k5/03_tani.html`). Üslubu, okunuş biçimini ve seçici kullanımını bu örnekten öğren. Yalnızca parça boyutu eski: o bölüm küçük parçalarla üretildi, yeni bölümlerde parçalar büyük olacak.

## 1. Temel şart: hiçbir bilgi eksilmez

Kitaptaki her bilgi hem ekranda hem seste yer alır.

- **Her cümle:** her paragraf, her liste maddesi.
- **Tablolar:** her satır, iki sütunuyla birlikte. Başlık satırı (`thead`) ayrıca okunmaz, ama sütunların anlamı cümlenin içinde geçer ("Birinci bulgu: … Mekanizması: …").
- **Şekiller (`.chart-figure`):** şeklin içindeki bütün yazılar, etiketler, değerler, eksenler ve okların anlattığı ilişki, ardından altyazı (`figcaption`). Şekil, `<!--SVG:ad-->` yer tutucusudur; içeriği `kitaplar/m4kN/svg/ad.svg` dosyasındaki `<text>` öğelerindedir. Dosyayı oku ve şekli dinleyene ekrandaki görüntüyü anlatır gibi aktar ("Ekrandaki şekilde…").
- **Yıllara göre soru grafiği (`<!--YIL:a,b,c,d-->`):** sırasıyla 2022-2023, 2023-2024, 2024 ve 2025-2026 sınavlarındaki soru sayısıdır. Her yılın sayısını ve altyazıyı oku.
- **Kutular ve etiketler:** "Sık karıştırılan nokta" kutuları (`.hl-block`) ve etiketleri.
- **Sınav notları:** paragraf içindeki parantezli sınav notları (`.cite`). Sınav yılını, soru numarasını ve notun içeriğini doğal bir cümleyle söyle ("Bu bilgi 2025 2026 sınavının on sekizinci sorusunda doğru ifade olarak geçti.").
- **Soru kartları:** üst satır (`.card-kicker`: yıllar ve soru numaraları), soru cümlesi, her şık, cevap açıklamasının bütün paragrafları, itiraz ve kaynak farkı kutusu (`.card-dispute`) ve kaynak satırı (`.card-source`). Kaynak satırı kicker'da söylenenden farklı bilgi içermiyorsa ayrıca okunmaz, ama seçicisi cevap satırına eklenir (örnek: `"#k1 .card-body p:nth-child(1), #k1 .card-source"`).
- **Kapak dosyası (`00_kapak.html`):** kurum ve modül satırı, kitap başlığı, kaynaklar satırı, "nasıl okunmalı" metni, içindekiler (her bölümün adı ve alt başlıkları) ve yıl grafiği.

Sıra kitaptaki sırayla aynıdır, çünkü ekranda o an okunan blok vurgulanır. Bilgi eklenmez. Anlatımı akıcı kılan kısa geçişler eklenebilir ("Şimdi…", "Peki neden?", "Birinci bulgu:"), ama yeni bir tıbbi bilgi, örnek ya da yorum eklenmez. Kitaptaki hiçbir ayrıntı (sayı, yüzde, eşik, istisna, "ama", "yalnızca", "en sık" gibi sınırlayıcı sözcükler) düşürülmez ya da değiştirilmez.

## 2. Üslup

Sosyal medyadaki tıp eğitimi videoları gibi enerjik, samimi ve akıcı ol. Dinleyene "sen" diye hitap et. Cümleler kulakla anlaşılacak uzunlukta olsun; kitaptaki uzun bir cümleyi iki üç cümleye bölebilirsin.

- **Açılış:** "<Kitap adı>. Bölüm <sayı>: <bölüm adı>." Ardından bölümün giriş metni (`.chapter-lead`) gelir.
- **Kapanış:** "Bölüm <sayı>'ün sonuna geldik. Bir sonraki bölümde <sonraki bölümün konusu> konuşacağız." Sonraki bölümün adını kapak dosyasındaki içindekilerden al. Kitabın son bölümünde kitabın bittiğini söyle.
- **İki dosyaya bölünmüş bölümler** (`03a_…`, `03b_…`): ilk dosya "Bölüm <sayı>'e bir sonraki videoda devam edeceğiz." diye biter. İkinci dosya "<Kitap adı>. Bölüm <sayı>'e devam ediyoruz: <ilk başlığın konusu>." diye başlar; bu dosyada `.chapter-lead` ve `#bas` yoktur.

## 3. Okunuş kuralları

Ses modeli metni yazıldığı gibi okur. Rakamlar, semboller ve kısaltmalar yanlış okunur.

- **Sayılar yazıyla:**

  | Kitapta | Anlatımda |
  |---|---|
  | `2,5 mm` | iki buçuk milimetre |
  | `0,12 sn` | sıfır virgül on iki saniye |
  | `%70` | yüzde yetmiş |
  | `> +110°` | artı yüz on dereceden büyük |
  | `25 mmHg` | yirmi beş milimetre cıva |
  | `3,5 m/sn` | saniyede üç buçuk metre |
  | `20-30 mL/yıl` | yılda yirmi ile otuz mililitre |
  | `FEV₁/FVC < 0,70` | FEV bir bölü FVC oranı sıfır virgül yetmişin altında |

- **Yıllar rakamla kalabilir,** ama aradaki tire yazılmaz: "2025 2026 sınavı", "2024 sınavı". Soru numaraları yazıyla yazılır: "S18" → "on sekizinci soru".
- **Hiç kullanılmayacak semboller:** `% < > = ± ° × / ~ → ↑ ↓ ( ) [ ] + & * #`, alt ve üst simgeler (`₁ ² ⁺`), Yunan harfleri. Bunların yerine okunuşları yazılır:
  - α1-antitripsin → alfa bir antitripsin
  - β2 agonist → beta iki agonist
  - TGF-β → TGF beta
  - IL-8 → interlökin sekiz
  - TNF-α → TNF alfa
  - CD8⁺ → CD sekiz pozitif
  - PaO₂ → P a O iki
  - FEV₁ → FEV bir
  - μg → mikrogram
  - Parantez içindeki açıklamalar virgülle ya da "yani" ile cümleye katılır.
- **EKG derivasyonları:** "D iki", "D üç", "a V F", "V bir".
- **Kısaltmalar:** sınıfta nasıl söyleniyorsa öyle yazılır. KOAH, EKG, QRS, GOLD, CAT, DLCO, PEF olduğu gibi kalır. Harf harf okunması gereken alışılmamış bir kısaltmada harfler boşlukla ayrılır.
- **Yabancı terimler:** kitapta geçen İngilizce terimler aynen kalır. Latince ve Fransızca ifadeler okunuşuyla yazılır ("cor en sabot" → "kor an sabo").
- **Şıklar** "A: …" biçiminde, her biri ayrı satırda yazılır.
- **Durdur ve düşün:** her sorunun şıklarından sonra ayrı bir satırda "Durdur ve düşün." gelir.

## 4. `parcalar.txt` biçimi

```
### k4b1_01 | Kısa parça başlığı
Birinci satır…
İkinci satır…

### k4b1_02 | …
```

- **Parça adı:** `<klasör adı>_NN`. Numara 01'den başlar ve sırayla artar.
- **Parça boyutu:** hedef 5.500-7.000 karakter, en fazla 7.500. Ses modeli bir istekte en fazla yaklaşık 11 dakika ses üretebiliyor; 7.000 karakter yaklaşık 7-8 dakika eder. Bütün bölüm 7.000 karakteri geçmiyorsa tek parça yaz. Parçalar mümkün olduğunca eşit büyüklükte olsun.
- **Parça sınırı:** kitabın bölüm kesimlerinde (`.book-section`) ya da en azından bir blok sonunda olur, paragraf ortasında olmaz. Bir sorunun soru kısmı ile cevabı aynı parçada kalır.
- **Satır:** her dolu satır bir ekran vurgusudur ve tek bir bloğu (ya da birlikte görünen birkaç küçük bloğu) anlatır. Uzun bir paragraf aynı seçiciyle iki üç satıra bölünebilir. Bir satır 900 karakteri geçmez. Satır içinde satır sonu olmaz.

## 5. `sahne.json` biçimi

```json
{
  "_aciklama": "…",
  "kaynak": "kaynak/modul4/kitaplar/m4k4/01_genel.html",
  "ust_baslik": "Antiastmatik İlaçlar · Bölüm 1 · Genel bakış",
  "parcalar": {
    "k4b1_01": ["#bas", ".chapter-lead", "#s1 > h3, #s1 > p:nth-of-type(1)", "…"],
    "k4b1_02": ["…", {"sel": "#k1 .card-title", "dur": 4.5}, {"sel": "#k1 .card-body p:nth-child(1), #k1 .card-source", "ac": "k1"}, "…"]
  }
}
```

- **Girdi sayısı:** her parçanın listesinde, `parcalar.txt`'teki o parçanın dolu satır sayısı kadar girdi olur, aynı sırayla.
- **Girdi biçimi:** düz bir CSS seçici ya da `{"sel": …, "dur": 4.5}` (bu satırdan sonra 4,5 saniyelik düşünme arası) ya da `{"sel": …, "ac": "k3"}` (bu satırdan itibaren 3. kartın cevabı ekranda açılır; o ana kadar bulanıktır).
- **`ust_baslik`:** ekranın üst şeridindeki yazı. Kısa kitap adı · Bölüm sayısı · kısa bölüm adı. Kapakta: kısa kitap adı · Giriş.
- **Sayfadaki kimlikler** (video aracı bunları kendisi ekler):
  - `#bas`: bölüm üst satırı ve başlığı birlikte (yalnızca `.chapter-kicker` olan dosyalarda).
  - `#s1, #s2, …`: dosyadaki `.book-section` blokları, sırayla.
  - `#k1, #k2, …`: dosyadaki soru kartları, sırayla.
  - `.qtext`: kartın soru cümlesi.
  - `.opt`: kartın şıkları, her biri ayrı. `#k2 .opt:nth-child(3)` üçüncü şıktır.
- **Sık kullanılan seçiciler:**

  | Seçici | Anlamı |
  |---|---|
  | `.chapter-lead` | bölüm giriş paragrafı |
  | `#s2 > h3, #s2 > p:nth-of-type(1)` | başlık ve ilk paragraf birlikte |
  | `#s2 > p:nth-of-type(3)` | bölümün doğrudan çocuğu olan 3. paragraf |
  | `#s1 > h4:nth-of-type(2)` | 2. ara başlık |
  | `#s1 tbody tr:nth-child(4)` | tablonun 4. satırı (birden çok tablo varsa `#s1 > table:nth-of-type(2) tbody tr:nth-child(1)`) |
  | `#s3 > ul > li:nth-child(2)` | listenin 2. maddesi (birden çok liste varsa `#s3 > ul:nth-of-type(2) > li:nth-child(1)`; numaralı liste `ol`) |
  | `#s1 > figure` ya da `#s1 > figure:nth-of-type(2)` | şekil |
  | `#s1 > .hl-block` | sık karıştırılan nokta kutusu |
  | `#s4` | yalnızca başlık ve grafikten oluşan kısa yıl grafiği bölümü gibi küçük bir bölümün tamamı |
  | `#s6 > h2, #k1 .card-kicker` | "Bölüm Sonu Soruları" başlığı ve ilk kartın üst satırı |
  | `#k1 .card-body p:nth-child(2)` | cevap açıklamasının 2. paragrafı |
  | `#k1 .card-dispute` | itiraz ve kaynak farkı kutusu |
  | kapakta `.book-kicker`, `.book-title`, `.book-byline`, `#s2 .toc > li:nth-child(1)` | kapak öğeleri |

  `nth-of-type` aynı etiketli kardeşleri sayar: `#s1 > p:nth-of-type(2)` bölümün doğrudan çocuğu olan ikinci `<p>`'dir. HTML'de saymadan önce yapıyı dikkatle oku.
- **Soru akışı:**
  1. Kicker satırı: `#kN .card-kicker`.
  2. Soru cümlesi: `#kN .qtext`.
  3. Şıklar, her biri ayrı satırda: `#kN .opt:nth-child(1)` … `(5)`.
  4. "Durdur ve düşün." satırı: `{"sel": "#kN .card-title", "dur": 4.5}`.
  5. Cevabın ilk satırı: `{"sel": "#kN .card-body p:nth-child(1), #kN .card-source", "ac": "kN"}`.
  6. Cevabın diğer paragrafları ve varsa `#kN .card-dispute`.

  Şıkkı olmayan açık uçlu kartta 3. adım atlanır ve düşünme arası `{"sel": "#kN .qtext", "dur": 4.5}` satırına konur.

## 6. Denetim

Dosyaları yazdıktan sonra repo kökünden şunu çalıştır:

```
python3 video/araclar/dogrula.py video/<klasör>
```

- **Hata sayısı 0 olmalı.** Doğrulayıcı şunları denetler: parça biçimi ve boyutu, satır ve seçici sayısı, her seçicinin sayfada karşılığı, kitaptaki **her içerik bloğunun** bir satıra bağlı olması, cevabı açılmadan okunan kart kısmı.
- **Uyarılar:**
  - Sembol ve rakam uyarıları sıfır olmalı.
  - "Çok geniş seçici" uyarısını gidermek için daha dar seçiciler kullan.
  - Boyut uyarısı yalnızca bölüm küçük olduğu için tek parçaysa kalabilir.

Doğrulayıcı blok düzeyinde denetler. Bir paragraftaki bir cümlenin unutulduğunu yakalayamaz; cümle düzeyindeki eksiksizlik senin sorumluluğundadır.

Commit ya da push yapma.
