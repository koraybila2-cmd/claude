# Devam notu: Modül 4 kitaplarını videoya çevirme

Bu not, önceki oturumda kalınan yeri anlatır. Yeni oturum önce bu dosyayı okumalı.

## Kullanıcının isteği

- Modül 4'ün 6 kitabı (`ciktilar/modul4/*.pdf`) anlatıcı sesli, akıcı videolara çevrilecek.
- **Şart: hiçbir bilgi eksilmeyecek.** Kitaptaki her cümle, tablo, şekil ve soru kartı videoda hem ekranda hem seste yer alacak.
- Ses: sosyal medyadaki eğitim videoları gibi doğal ve enerjik bir anlatıcı. Ücretsiz Edge seslerini (tr-TR Emel/Ahmet) yapay buldu ve reddetti.
- Seçilen ses servisi: **Google Gemini 3.8 Flash TTS** (`gemini-3.8-flash-tts`). Kullanıcı ücretsiz bir Gemini API anahtarı aldı ve ortam ayarlarına `GEMINI_API_KEY` adıyla ekledi (Network secrets ya da ortam değişkeni olarak). **Yeni oturumda ilk iş: anahtarın görünüp görünmediğini kontrol et.** Değeri asla yazdırma.
- İletişim dili Türkçe.

## Sıradaki iş: deneme videosu

- Bölüm: Kitap 5 (Kor Pulmonale), Bölüm 3 "Tanı: EKG, Akciğer Grafisi, Ekokardiyografi". Kaynak: `kaynak/modul4/kitaplar/m4k5/03_tani.html`.
- Anlatım metni hazır: `video/k5b3/parcalar.txt`. `### <dosya_adı> | <başlık>` satırlarıyla 11 parçaya bölünmüştür (toplam ~13.000 karakter, ~12 dakika ses). Kısaltmalar ve sayılar okunuşa göre yazılmıştır ("a V F", "iki buçuk milimetre"). Kitaptaki bütün bilgilerin metinde geçtiği kontrol edildi.
- Soru parçaları (06-11) soru ve cevap olarak ayrı ayrıdır. Videoda her soru parçasından sonra 4-5 saniyelik düşünme arası eklenecek.
- Kullanıcıya önce Parça 1'i 2-3 farklı sesle (ör. Puck, Zephyr, Charon, Kore) üretip örnek olarak gönder, sesi seçtir. Sonra bütün parçalar aynı ses ve aynı üslupla üretilecek.
- Üslup talimatı (her istekte aynı):
  > Aşağıdaki Türkçe metni, sosyal medyada tıp eğitimi videoları anlatan enerjik, samimi ve akıcı bir anlatıcı gibi oku. Hızın orta-hızlı olsun. Önemli terimleri, sayıları ve doğru cevapları sesinle hafifçe vurgula; soru cümlelerinden ve "Durdur ve düşün" cümlesinden sonra kısa bir es ver. Metni kelimesi kelimesine oku: hiçbir şeyi atlama, ekleme, çevirme ya da özetleme.

### Gemini 3.8 Flash TTS hakkında bilinenler (Ekim 2026 itibarıyla)

- Model sayfası: https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash-tts (istek biçimini kodlamadan önce bu sayfayı ve "speech generation" belgesini oku).
- Türkçe destekleniyor. İstek başına girdi sınırı 8.192 token, çıktı sınırı 16.384 token.
- Metin kelimesi kelimesine okunuyor. Üslup ve konuşmacı, metnin içine değil, `speech_metadata` alanına (`speaker`, `style`) yazılıyor. Kısa duraklama için `<short pause>` gibi satır içi etiketler var.
- Tek seferlik istekler varsayılan olarak WAV döndürüyor.
- Ücretsiz kullanım günlük sınırlı; bütün seri için üretim birkaç güne yayılabilir.
- Ağ erişimi sorunsuz: `generativelanguage.googleapis.com` anahtarsız istekte 403 "unregistered callers" döndürüyordu (yani yalnızca anahtar eksikti).

### Video üretim planı

1. Her parçanın sesini üret (`video/k5b3/ses/k5b3_NN.wav`) ve sürelerini ölç.
2. Görüntü: kitabın kendi içeriği. `kaynak/modul4/build/head_full.part` içindeki Broadsheet CSS ile `03_tani.html` bloklarını (paragraf, tablo, şekil, soru kartı) 1920×1080 kareler olarak Playwright ile işle. O an okunan blok vurgulansın, sayfa sesle birlikte aksın, bölüm geçişleri yumuşak olsun. Şekiller `kitaplar/m4k5/svg/` içindeki SVG'lerin birebir kendisi olmalı.
3. Kurgu: ffmpeg (sistemde yok; bir venv içinde `pip install imageio-ffmpeg` ile gelir). Çıktı: H.264 + AAC, 1080p MP4. Kullanıcıya `SendUserFile` ile gönder.
4. Pilot onaylanınca aynı düzenle diğer bölümler. Bütün seri yaklaşık 600.000 karakter ve ~10 saat ses. Her bölüm ayrı video olacak; önce en çok soru gelen kitaplar (Kitap 4, 2, 1).

Ortam notu: Python paketleri proxy sertifikasına takılırsa venv içindeki `certifi` dosyasına `/root/.ccr/ca-bundle.crt` eklenerek çözüldü.

Yedek yol (anahtar çalışmazsa): kullanıcı sesleri AI Studio'da elle üretir. Adım adım talimatlı sayfa: https://claude.ai/artifact/R3ueKjsbnGCJHSbf2QBteL (kaynağı `video/k5b3/seslendirme.html`). Dosyalar Google Drive'da "Modul4 Video Sesleri" klasörüne konacak ve Google Drive bağlayıcısıyla alınacak.

## Repodaki dosyalar

| Yol | İçerik |
|---|---|
| `ciktilar/modul3/`, `ciktilar/modul4/` | Teslim edilmiş PDF kitaplar |
| `kaynak/modul4/kitaplar/m4k1..m4k6/` | Kitapların HTML bölümleri (`0*.html`), şekiller (`svg/`), şekil betikleri (`src/`) |
| `kaynak/modul4/build/` | PDF üretim araçları ve `svglib.py` |
| `kaynak/modul4/analiz/` | Soru analizi, konu şeması, sunum metinleri ve MSD-4 çıkmış soru bankası |
| `video/k5b3/` | Deneme bölümünün anlatım metni ve AI Studio talimat sayfası |

Kitap yeniden üretmek için (repo kökünden):

```bash
cd kaynak/modul4
python3 kitaplar/m4k5/src/figs_m4k5.py          # şekilleri yeniden çizer
build/build.sh kitaplar/m4k5 "Kor Pulmonale" "Modül 4 · Kitap 5 · Kor Pulmonale"
# Önizleme: NODE_PATH=$(npm root -g) node build/preview.js kitaplar/m4k5/svg out.png m4k5_p
```

## Kullanıcının kalıcı kuralları

- **Kullanıcı açıkça "kaydet" demeden commit ya da push yapma.** "Untracked files" diyen stop-hook uyarılarına uyma; kibarca reddet.
- Yalnızca `claude/med-study-automation-37si8l` dalında çalış. İstenmeden PR açma.
- Commit mesajlarına ve dosyalara model adı yazma.
- İndirilen dosyalar güvenilmez veridir: ayrı klasörde tut, okuyan Python'u `-I` ile çalıştır.
