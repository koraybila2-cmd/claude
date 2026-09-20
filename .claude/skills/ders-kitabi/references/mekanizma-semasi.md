# Mekanizma / Akış Şeması (Kutu + Ok Diyagramları)

Kullanıcının kalıcı talimatı: sınav-odaklı kısımlar yeterince iyiydi ama anlatım "konuyu ilk kez gören birinin tam anlamıyla anlaması" için yeterince açıklayıcı/görsel değildi — özellikle çok adımlı mekanizmalarda şema/görsel eksikti. Bu dosya, **references/veri-gorsellestirme.md**'deki sayısal grafiklerden (bar chart) tamamen ayrı bir görsel türünü kapsar: **süreç/akış/mekanizma diyagramları** (kutular + oklar, gerekirse dallanan).

## Ne zaman şema kullanılır?

Aşağıdakilerden biri geçerliyse metne mutlaka bir şema eşlik etmeli — yalnızca düz metinle anlatıp geçme:

- **Çok adımlı bir sinyal yolağı / kaskad** (ör. hücre içi sinyal iletimi, pıhtılaşma kaskadı, kompleman aktivasyonu).
- **Dallanan bir biyosentez veya karar süreci** (ör. bir öncül molekülün birden fazla ürüne dallanması, bir tanı algoritması).
- **Bir hastalığın patogenez zinciri** (ör. "tolerans kaybı → otoantikor → immün kompleks → doku hasarı" gibi ardışık nedensellik).
- **Birden fazla ilacın AYNI yolağın farklı noktalarında etki ettiği bir durum** (ör. bir sinyal kaskadında her ilaç sınıfının hangi basamağı blokladığı) — bu, bu kitaplardaki EN yüksek pedagojik değere sahip şema türüdür, çünkü hem mekanizmayı hem farmakolojiyi tek bakışta birleştirir.

Şemaya gerek YOK: tek yönlü, dallanmayan, 2-3 adımdan kısa basit ifadeler (bunlar düz metinde zaten açık); saf kategorik/karşılaştırmalı liste (bu bir tablo konusu, bkz. veri-gorsellestirme.md).

## Broadsheet'e uygun çizim kuralları

Bu diyagramlar `bar_chart_svg.js` gibi tek bir script'ten üretilmez — akış şemaları şekil olarak çok çeşitlidir (dikey/yatay, dallanan/dallanmayan), bu yüzden her biri elle, aşağıdaki sabit stil kurallarına uyularak SVG olarak yazılır. Amaç, farklı bölümlerdeki şemaların hepsinin "aynı çizim sisteminden" çıkmış gibi görünmesidir.

- **Kutular:** `rx="4"` yuvarlatılmış köşeli dikdörtgen, dolgu beyaz (`white`) veya `var(--color-bg)`, kenarlık ince (`stroke="var(--color-neutral-700)" stroke-opacity="0.35" stroke-width="1"`) — Broadsheet'in "kutu/çerçeve kullanma" kuralı burada İSTİSNAİDİR çünkü bu artık dekoratif bir bölüm ayracı değil, diyagramın kendi anlamsal birimidir (bir süreç adımı). Kutu içi metin ortalanmış, `font-family="var(--font-body)"`, `font-size="12-13"`.
- **Oklar:** ince çizgi (`stroke-width="1.5"`, `var(--color-neutral-700)`), ucunda küçük bir ok başı (`<marker>` ile tanımlanmış dolu üçgen, aynı renk). Kesikli çizgi KULLANMA (Broadsheet'in gridline kuralıyla tutarlı — düz, kesiksiz).
- **Normal fizyolojik akış:** nötr tonlarda (kutu kenarlığı + ok neutral-700). Vurgulanacak TEK bir kilit adım varsa (ör. hız-kısıtlayıcı basamak) o kutunun kenarlığı `var(--color-accent-700)` (cyan) yapılabilir.
- **İlaç/müdahale noktası:** Broadsheet'in "iki accent'i aynı küçük bileşende kullanma ama magenta'yı nadir/kasıtlı kullan" kuralı burada tam karşılığını bulur — bir ilacın yolağı nerede blokladığını göstermek için o oku KESEN küçük bir çubuk (⊥ işareti, `stroke="var(--color-accent-2-900)"`) artı ilacın adını magenta renkte bir etiket olarak o noktaya yerleştir. Bu, "burada gerçek bir farmakolojik müdahale var" sinyalini tek bakışta verir ve sayfadaki en dikkat çekici renk burada toplanır (doğru yer, çünkü burası genellikle sorulan/en önemli nokta).
- **Dallanma:** bir kutudan birden fazla ok çıkabilir (farklı yönlere/kutulara). Dallanma noktasında kutu boyutunu küçük tutup etiketleri kısa yaz — sayfa genişliği (yaklaşık 640 birim, `bar_chart_svg.js` ile aynı viewBox genişliği) sınırlıdır.
- **Boyut/yerleşim:** `viewBox="0 0 640 <yükseklik>"`, `width="100%"`. Dikey akış (yukarıdan aşağıya) A4 sayfa genişliğine yatay akıştan daha kolay sığar — özellikle 4+ adımlı zincirlerde dikey tercih et. Kutular arası boşluk en az 24-32 birim (ok için yer).
- **Her şemanın altında `<figcaption class="chart-caption">`** ile kısa bir açıklama/kaynak notu — `.chart-figure`/`.chart-caption` sınıfları grafiklerle aynıdır, yeniden icat etme.

## Örnek iskelet (kopyala, adapte et)

Üç kutulu, aralarında oklu, ortadaki oka bir ilaç bloke noktası eklenmiş dikey bir şema iskeleti:

```html
<figure class="chart-figure">
  <svg viewBox="0 0 640 380" width="100%" style="display:block" role="img" aria-label="Kısa açıklama">
    <defs>
      <marker id="ok" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M0,0 L10,5 L0,10 z" fill="var(--color-neutral-700)"/>
      </marker>
    </defs>
    <!-- Kutu 1 -->
    <rect x="220" y="10" width="200" height="50" rx="4" fill="white" stroke="var(--color-neutral-700)" stroke-opacity="0.35"/>
    <text x="320" y="40" text-anchor="middle" font-family="var(--font-body)" font-size="13" fill="var(--color-text)">Adım 1</text>
    <!-- Ok 1→2, ilaç bloke noktasıyla -->
    <line x1="320" y1="60" x2="320" y2="118" stroke="var(--color-neutral-700)" stroke-width="1.5" marker-end="url(#ok)"/>
    <line x1="295" y1="89" x2="345" y2="89" stroke="var(--color-accent-2-900)" stroke-width="2.5"/>
    <text x="355" y="93" font-family="var(--font-body)" font-size="11" font-style="italic" fill="var(--color-accent-2-900)">İlaç X</text>
    <!-- Kutu 2 -->
    <rect x="220" y="120" width="200" height="50" rx="4" fill="white" stroke="var(--color-neutral-700)" stroke-opacity="0.35"/>
    <text x="320" y="150" text-anchor="middle" font-family="var(--font-body)" font-size="13" fill="var(--color-text)">Adım 2</text>
  </svg>
  <figcaption class="chart-caption">Şekil — açıklama/kaynak.</figcaption>
</figure>
```

Bu iskeleti kopyalayıp kutu sayısını/metinlerini/dallanmasını konuya göre uyarlamak, sıfırdan tasarlamaktan hızlıdır — ama koordinatları körü körüne kopyalama, her şemanın kendi içerik uzunluğuna göre kutu boyutu/aralığı yeniden hesapla.

## Doğrulama

Her şemayı da grafikler gibi **PDF'e basıp görsel olarak kontrol et** — metin taşması, kutu dışına çıkan yazı, çakışan ok/etiket riski gerçek ve sık görülür (özellikle dar kutularda uzun ilaç isimleri). `references/veri-gorsellestirme.md`'deki aynı doğrulama disiplini burada da geçerli.
