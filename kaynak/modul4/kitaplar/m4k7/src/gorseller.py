"""Kitap 7 (Toraks anatomisi) gorsellerini sunumdan uretir.
kullanim: python3 -I gorseller.py <indirilen_dizini> <cikti_img_dizini>
indirilen_dizini: acik/ (acilmis pptx), kirpik/ (srcRect uygulanmis cikarimlar), hr/ (200 dpi slayt goruntuleri h-NN.png)"""
import sys, os
from PIL import Image

SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
MAXW = 1400
NETTER = (80, 0, 638, 478)  # Netter yaziliminin sol menu seridini atar


def k(name):
    return Image.open(os.path.join(SRC, 'kirpik', name)).convert('RGB')


def m(name, box=None):
    im = Image.open(os.path.join(SRC, 'acik', 'ppt', 'media', name))
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA')
        bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); im = bg
    im = im.convert('RGB')
    return im.crop(box) if box else im


def r(slide, x0, y0, x1, y1):
    im = Image.open(os.path.join(SRC, 'hr', f'h-{slide:02d}.png')).convert('RGB')
    W, H = im.size
    return im.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))


def yan_yana(*ims, h=None, gap=24):
    h = h or max(i.height for i in ims)
    ims = [i.resize((max(1, round(i.width * h / i.height)), h), Image.LANCZOS) for i in ims]
    W = sum(i.width for i in ims) + gap * (len(ims) - 1)
    out = Image.new('RGB', (W, h), 'white'); x = 0
    for i in ims:
        out.paste(i, (x, 0)); x += i.width + gap
    return out


def kaydet(im, name):
    if im.width > MAXW:
        im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
    im.save(os.path.join(OUT, name + '.jpg'), quality=84, optimize=True, progressive=True)
    print(name, im.size)


# Bolum 1 — gogus kafesi, eklemler, hareketler
kaydet(k('s04_1_image1.jpg'), 'g01_gogus_kafesi')
kaydet(r(5, 0.0, 0.24, 0.55, 0.86), 'g01_kostovertebral')
kaydet(yan_yana(k('s07_2_image4.jpg'), k('s06_1_image3.jpg'), h=599), 'g01_kaburga_hareket')
# Bolum 2 — diyafram ve solunum kaslari
kaydet(m('image6.jpeg', NETTER), 'g02_diyafram_abdominal')
kaydet(m('image8.jpeg', NETTER), 'g02_diyafram_torasik')
kaydet(k('s11_1_image7.jpg'), 'g02_diyafram_kadavra')
kaydet(yan_yana(k('s16_1_image9.jpg'), k('s16_2_image10.jpg'), h=500), 'g02_herni')
kaydet(k('s18_1_image11.jpg'), 'g02_inspirasyon')
kaydet(r(19, 0.52, 0.20, 0.96, 0.95), 'g02_frenik_boyun')
kaydet(k('s20_1_image13.jpg'), 'g02_frenik_seyir')
kaydet(m('image14.png', NETTER), 'g02_lateral_duvar')
kaydet(m('image16.png', NETTER), 'g02_solunum_kaslari')
kaydet(r(23, 0.58, 0.17, 1.0, 1.0), 'g02_on_duvar_ic')
kaydet(yan_yana(k('s24_1_image18.jpg'), k('s24_2_image19.jpg'), h=700), 'g02_ik_katmanlar')
kaydet(yan_yana(m('image15.png', NETTER), k('s25_2_image21.jpg'), h=478), 'g02_arka_duvar')
kaydet(yan_yana(k('s27_1_image22.jpg'), k('s27_3_image24.jpg'), k('s28_2_image26.jpg'), h=420), 'g02_yardimci_kaslar')
# Bolum 3 — duvarin sinir, damar, lenfleri
kaydet(k('s29_1_image27.jpg'), 'g03_ik_sinir_dallar')
kaydet(k('s30_1_image29.jpg'), 'g03_ik_sinir_seyir')
kaydet(k('s33_1_image31.jpg'), 'g03_atipik_ik')
kaydet(r(35, 0.13, 0.05, 0.90, 0.99), 'g03_subklavyan')
kaydet(k('s36_1_image33.jpg'), 'g03_duvar_arterleri')
kaydet(m('image34.jpeg', NETTER), 'g03_ik_kesit')
kaydet(k('s39_1_image35.jpg'), 'g03_torasentez')
kaydet(r(40, 0.59, 0.09, 0.95, 0.91), 'g03_aksiller_dallar')
kaydet(k('s41_1_image36.jpg'), 'g03_venler')
kaydet(k('s42_1_image37.jpg'), 'g03_azygos')
kaydet(r(44, 0.12, 0.04, 0.45, 0.96), 'g03_sup_ik_ven')
kaydet(k('s45_1_image40.jpg'), 'g03_meme_lenf')
# Bolum 4 — plevra
kaydet(k('s48_1_image41.jpg'), 'g04_plevra_gelisim')
kaydet(k('s51_1_image43.jpg'), 'g04_plevra_katmanlar')
kaydet(r(50, 0.61, 0.06, 0.94, 0.572), 'g04_parietal_bolumler')
kaydet(k('s54_1_image48.jpg'), 'g04_rontgen_sinus')
kaydet(r(55, 0.12, 0.49, 0.70, 0.985), 'g04_plevra_projeksiyon')
kaydet(r(56, 0.12, 0.48, 0.88, 0.985), 'g04_akciger_projeksiyon')
# Bolum 5 — akciger ve bronslar
kaydet(m('image52.jpeg', NETTER), 'g05_trakea_bronslar')
kaydet(yan_yana(m('image56.png', NETTER), m('image55.png', NETTER), h=478), 'g05_hilus')
kaydet(m('image53.jpeg', NETTER), 'g05_segment_lateral')
kaydet(m('image54.jpeg', NETTER), 'g05_segment_medial')
kaydet(r(60, 0.43, 0.05, 0.86, 0.88), 'g05_segment_sag')
kaydet(r(61, 0.48, 0.12, 0.88, 0.98), 'g05_segment_sol')
# Bolum 6 — akcigerin damar, lenf, sinirleri
kaydet(k('s64_1_image57.jpg'), 'g06_bronsiyal_sema')
kaydet(r(65, 0.12, 0.03, 0.92, 0.94), 'g06_bronsiyal_arterler')
kaydet(r(66, 0.02, 0.03, 0.99, 0.98), 'g06_lenf_akis')
kaydet(r(69, 0.24, 0.04, 0.68, 0.96), 'g06_pulmoner_pleksus')
kaydet(k('s72_1_image65.jpg'), 'g06_solunum_kontrol')
# Bolum 7 — mediastinum
kaydet(k('s75_1_image67.jpg'), 'g07_pozisyon')
kaydet(k('s76_1_image68.jpg'), 'g07_bolumler_gray')
kaydet(k('s85_1_image69.jpg'), 'g07_buyuk_damarlar')
kaydet(k('s82_1_image71.jpg'), 'g07_mediasten_sag')
kaydet(m('image70.jpeg', NETTER), 'g07_mediasten_sol')
kaydet(m('image47.png', NETTER), 'g07_frenik_insitu')
kaydet(k('s86_1_image72.jpg'), 'g07_posterior')
