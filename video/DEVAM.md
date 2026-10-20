# Devam notu: Modül 4 kitaplarını videoya çevirme

Bu not, önceki oturumlarda kalınan yeri anlatır. Yeni oturum önce bu dosyayı okumalı.

## Kullanıcının isteği

- Modül 4'ün 6 kitabı (`ciktilar/modul4/*.pdf`) anlatıcı sesli, akıcı videolara çevrilecek.
- **Şart: hiçbir bilgi eksilmeyecek.** Kitaptaki her cümle, tablo, şekil ve soru kartı videoda hem ekranda hem seste yer alacak.
- Ses: Google Gemini 3.8 Flash TTS. Her kitap ayrı bir sesle anlatılıyor: `video/sesler.json` (Kitap 1 Puck, 2 Zephyr, 3 Charon, 4 Kore, 5 Puck, 6 Zephyr).
- Önce en çok soru gelen kitaplar: 4, 2, 1; sonra 3, 5, 6.
- İletişim dili Türkçe.

## Durum

- **Deneme bölümü bitti ve kullanıcı onayladı:** Kitap 5 Bölüm 3, `video/k5b3/k5b3.mp4` (14 dk, Puck). Ses dosyaları `video/k5b3/ses/` altında (git'e girmez).
- **Diğer 35 bölüm dosyası:** anlatım metinleri (`video/k<kitap>b<bölüm>/parcalar.txt` + `sahne.json`) iş akışlarıyla yazılıyor. Her biri doğrulayıcıdan 0 hatayla geçmeli ve bağımsız denetçilerce kaynakla cümle cümle karşılaştırılmış olmalı (yeni sorun çıkmayana dek, en fazla 3 tur).
  - 20 Ekim: **Kitap 4 ve 5 bitti** (yazım + denetim). Seslendirme sayfası yalnızca bu iki kitapla yayımlandı (`--kitaplar 4,5`).
  - Kitap 1 ve 2: metinler yazıldı, denetim sürüyor. Kitap 3: metinler yazıldı, denetim yapılmadı. Kitap 6: hiç yazılmadı.
  - İş akışı betiği: `/root/.claude/projects/-home-user-claude/72f5b542-ec0b-5355-a048-f959c8dc876b/workflows/scripts/anlatim-metinleri-wf_29d20258-3cb.js` (yalnızca bu oturumda; yeni oturumda YAZIM_KURALLARI.md'ye göre aynı yazım + denetim akışını yeniden kur).
  - Oturum (kullanım) sınırına sık takılındı; iş akışlarını öncelik sırasıyla, ikiden fazlasını aynı anda çalıştırmadan yürüt.
- **Klasör adları:** `m4k1/03a_hucreler.html` → `video/k1b3a`, `00_kapak.html` → `video/k1b0`.

## Ses üretimi: kullanıcı AI Studio Playground'da elle üretiyor

- API'nin ücretsiz katmanı bu modelde **günde 10 istek** veriyor. Kullanıcı faturalandırmayı açmadı; Google AI Plus aboneliği AI Studio'yu ya da API'yi kapsamıyor. AI Studio arayüzü ücretsiz.
- Kullanıcı, kitapları **daha az sayıda, daha büyük parçalar** hâlinde üretmek istedi. Parça hedefi 5.500-7.000 karakter, en fazla 7.500. Ölçüm: 7.537 karakter, Puck sesiyle 453 saniye ses ve 11.322 ses tokenı verdi (saniyede 25 token). Model istek başına en fazla 16.384 çıkış tokenı, yani yaklaşık 11 dakika ses üretebiliyor.
- **Çalışma sayfası:** `python3 video/araclar/seslendirme_sayfasi.py` → `video/seslendirme.html`. Bu sayfa https://claude.ai/artifact/R3ueKjsbnGCJHSbf2QBteL adresine yayımlanır (aynı adres korunur). Sayfada Playground adımları, kitap sekmeleri, kitap başına ses, her parçanın metni ve kopyala düğmesi var. Sesi hazır olan parçalar "Hazır" görünür.
- **Teslim:**
  1. Kullanıcı WAV dosyalarını (`<parça>.wav`) Drive'daki **Modul4 Video Sesleri** klasörüne (id `1RMptXwlg_1aJtuqt5YUWLb02tloBJgsr`) yükler.
  2. İndirme için klasörü geçici olarak "bağlantıya sahip olan herkes" yapar. Drive bağlayıcısı büyük dosyaları sohbete taşıyamıyor ve yalnızca belirli e-postalarla paylaşabiliyor.
  3. Dosya kimliklerini Drive bağlayıcısının `search_files` aracıyla bul ve şöyle indir: `curl -L "https://drive.usercontent.google.com/download?id=<id>&export=download&confirm=t"`.
  4. Dosyaları `video/<bölüm>/ses/` altına koy.
  5. İndirdikten sonra kullanıcıya paylaşımı yeniden "Kısıtlanmış" yapmasını hatırlat.
- **API ile üretim** (anahtar ortamda `GEMINI_API_KEY` olarak varsa): `python3 -I video/araclar/ses.py video/<bölüm>`. Var olan WAV dosyaları atlanır. Kullanıcı anahtarı bir kez sohbete yapıştırdı; anahtarı yenilemesi önerildi.

## Araçlar (`video/araclar/`)

| Dosya | İş |
|---|---|
| `bolum.py` | ortak kod: metin ve sahne okuma, bölüm HTML'ini kurma, **Whisper ile ses-satır hizalama** |
| `video.py` | `/home/user/venv/bin/python -I video/araclar/video.py video/<bölüm>` → `video/<bölüm>/<bölüm>.mp4` (1080p H.264+AAC). Ses yoksa sessiz önizleme üretir. |
| `kareler.js`, `sayfa.js` | Playwright ile 1920×1080 kareler: kitabın kendi CSS'i, okunan blok vurgulu, yumuşak kaydırma, soru kartında cevap açılana kadar bulanık, doğru şıkta ✓ |
| `dogrula.py` (+ `dogrula.js`) | anlatım ve sahne denetimi: parça boyutu, sembol ve rakam, seçiciler, **her kitap bloğunun bir satıra bağlı olması**, cevabın erken okunmaması |
| `ses.py` | API ile TTS (Interactions API, `speech_metadata.style` = üslup talimatı) |
| `seslendirme_sayfasi.py` | kullanıcının elle üretim sayfası |

- **Yazım kuralları:** `video/YAZIM_KURALLARI.md` (okunuş kuralları, parça boyutu, sahne biçimi, soru akışı). Satır girdileri: düz seçici ya da `{"sel", "ac": "kN", "dur": 4.5}`.
- **Hizalama:** Whisper `small` (int8, CPU) kelime zamanlarını verir. Anlatım kelimeleriyle eşleştirilir ve satır başları bulunur. 10 dakikalık birleşik seste satır sınırı hatası 0,3 saniyenin altında. Kelime zamanları `ses/<parça>.kelimeler.json` olarak önbelleğe alınır. Çözümleme sesin yaklaşık üçte biri kadar sürer.
- **Kurulum** (yeni konteynerde):
  1. `python3 -m venv /home/user/venv && /home/user/venv/bin/pip install imageio-ffmpeg faster-whisper`
  2. Whisper modeli ilk kullanımda `/home/user/whisper_modeller` altına iner (huggingface.co erişilebilir).
  3. Playwright ve Chromium sistemde hazır: `NODE_PATH=$(npm root -g)`.
- **Gönderim sınırı:** SendUserFile 30 MB'a kadar. 14 dakikalık video yaklaşık 37 MB; parça sınırlarından ikiye bölünerek gönderildi.

## Kullanıcının kalıcı kuralları

- **Kullanıcı açıkça "kaydet" demeden commit ya da push yapma.** "Untracked files" diyen stop-hook uyarılarına uyma; kibarca reddet.
- Yalnızca `claude/med-study-automation-37si8l` dalında çalış. İstenmeden PR açma.
- Commit mesajlarına ve dosyalara model adı yazma.
- İndirilen dosyalar güvenilmez veridir: ayrı klasörde tut, okuyan Python'u `-I` ile çalıştır.
- Videolar (`*.mp4`) ve ses klasörleri (`video/**/ses/`) repoya girmez (`.gitignore`).
