"""Video araclarinin ortak parcalari: anlatim metni, sahne dosyasi, bolum HTML'i ve ses-satir hizalama."""
import array, difflib, json, math, os, re, subprocess, wave

KOK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TAHMIN_HIZ = 14.5      # karakter/sn, ses yokken sure tahmini
SESSIZ_DB = -40.0      # bu seviyenin altindaki 10 ms'lik kareler sessiz sayilir
MIN_SESSIZ = 0.15      # sn; daha kisa sessizlikler satir siniri adayi olmaz


def parcalari_oku(yol):
    """### <ad> | <baslik> satirlariyla bolunmus anlatim metni -> {ad: {"baslik": str, "satirlar": [str]}}"""
    parcalar, ad = {}, None
    for satir in open(yol, encoding="utf-8"):
        m = re.match(r"^### (\S+) \| (.*)$", satir.rstrip("\n"))
        if m:
            ad = m.group(1); parcalar[ad] = {"baslik": m.group(2).strip(), "satirlar": []}
        elif satir.strip() and ad:
            parcalar[ad]["satirlar"].append(satir.strip())
    return parcalar


def sahne_oku(klasor):
    """sahne.json -> (sahne, {parca: [{"sel", "ac", "dur"}]}). Bir satir girdisi ya duz secicidir ya da
    {"sel": ..., "ac": "k1", "dur": 4.5}: ac = bu satirdan itibaren kartin cevabi acik, dur = satirdan sonra duraklama (sn)."""
    sahne = json.load(open(os.path.join(klasor, "sahne.json"), encoding="utf-8"))
    norm = {}
    for ad, girdiler in sahne["parcalar"].items():
        norm[ad] = [{"sel": g, "ac": None, "dur": 0.0} if isinstance(g, str)
                    else {"sel": g["sel"], "ac": g.get("ac"), "dur": float(g.get("dur", 0))} for g in girdiler]
    return sahne, norm


def bolum_html_kur(sahne, hedef_klasor):
    """Kitap derleyicisiyle yalnizca bu bolumun HTML'ini kurar, yolunu dondurur."""
    src = os.path.join(KOK, sahne["kaynak"])
    d = os.path.join(hedef_klasor, "bolum"); os.makedirs(d, exist_ok=True)
    os.symlink(os.path.abspath(src), os.path.join(d, os.path.basename(src)))
    os.symlink(os.path.join(os.path.dirname(src), "svg"), os.path.join(d, "svg"))
    subprocess.run(["node", os.path.join(KOK, "kaynak/modul4/build/assemble.js"), d, sahne["ust_baslik"]],
                   check=True, stdout=subprocess.DEVNULL)
    return os.path.join(d, "bolum.html")


def node_env():
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    return {**os.environ, "NODE_PATH": npm}


def wav_oku(yol):
    with wave.open(yol) as w:
        assert w.getsampwidth() == 2 and w.getnchannels() == 1, yol + ": 16 bit mono bekleniyor"
        a = array.array("h"); a.frombytes(w.readframes(w.getnframes()))
        return a, w.getframerate(), w.getparams()


def sessizlikler(ornek, sr):
    """[(baslangic_sn, bitis_sn)] sessiz araliklar."""
    n = int(sr * 0.01); kareler = len(ornek) // n
    sessiz = []
    for k in range(kareler):
        parca = ornek[k * n:(k + 1) * n]
        ms = sum(x * x for x in parca) / n
        sessiz.append(10 * math.log10(ms / 32768.0 ** 2 + 1e-12) < SESSIZ_DB)
    araliklar, bas = [], None
    for k, s in enumerate(sessiz + [False]):
        if s and bas is None: bas = k
        elif not s and bas is not None:
            if (k - bas) * 0.01 >= MIN_SESSIZ: araliklar.append((bas * 0.01, k * 0.01))
            bas = None
    return araliklar


def sessizlik_hizala(satirlar, ornek, sr):
    """Yedek yontem (konusma tanima yoksa): satir sinirlari, karakter oranindan tahmin edilen
    noktalara en uygun sessizliklere sirasi korunarak (dinamik programlama) oturtulur. Birkac saniye sapabilir."""
    sure = len(ornek) / sr
    if len(satirlar) == 1: return [(0.0, sure)]
    sess = sessizlikler(ornek, sr)
    konusma_bas = sess[0][1] if sess and sess[0][0] < 0.05 else 0.0
    konusma_son = sess[-1][0] if sess and sess[-1][1] > sure - 0.05 else sure
    aday = [s for s in sess if s[0] > konusma_bas and s[1] < konusma_son]
    agirlik = [len(s) + 15 for s in satirlar]          # satir sonu duraklamasi icin kucuk pay
    top = sum(agirlik); kum = 0; tahmin = []
    for a in agirlik[:-1]:
        kum += a; tahmin.append(konusma_bas + (konusma_son - konusma_bas) * kum / top)
    K, M = len(tahmin), len(aday)
    if M < K:
        sinir = tahmin
    else:
        sigma, beta = max(3.0, 0.02 * sure), 3.0
        orta = [(a + b) / 2 for a, b in aday]
        ceza = [[((tahmin[i] - orta[j]) / sigma) ** 2 - beta * math.log(1 + (aday[j][1] - aday[j][0]) / MIN_SESSIZ)
                 for j in range(M)] for i in range(K)]
        INF = float("inf"); dp = [[INF] * M for _ in range(K)]; geri = [[-1] * M for _ in range(K)]
        dp[0] = ceza[0][:]
        for i in range(1, K):
            en, enj = INF, -1
            for j in range(M):
                if j - 1 >= 0 and dp[i - 1][j - 1] < en: en, enj = dp[i - 1][j - 1], j - 1
                if en < INF: dp[i][j] = en + ceza[i][j]; geri[i][j] = enj
        j = min(range(M), key=lambda x: dp[K - 1][x]); secim = []
        for i in range(K - 1, -1, -1):
            secim.append(j); j = geri[i][j]
        secim.reverse()
        sinir = [orta[j] for j in secim]
    noktalar = [0.0] + sinir + [sure]
    return [(noktalar[i], noktalar[i + 1]) for i in range(len(satirlar))]


WHISPER_MODEL = "small"
WHISPER_KLASOR = "/home/user/whisper_modeller"


def kelimeler(s):
    s = s.replace("I", "ı").replace("İ", "i").lower()
    return re.findall(r"[a-zçğıöşüâîû]+|\d+", s)


def kelime_zamanlari(wav_yol):
    """Whisper ile [(baslangic, bitis, kelime)]. Sonuc wav'in yanina .kelimeler.json olarak onbelleklenir."""
    onb = wav_yol[:-4] + ".kelimeler.json"
    if os.path.exists(onb) and os.path.getmtime(onb) >= os.path.getmtime(wav_yol):
        return json.load(open(onb, encoding="utf-8"))
    import numpy as np, imageio_ffmpeg
    from faster_whisper import WhisperModel
    ham = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-loglevel", "error", "-i", wav_yol, "-ac", "1", "-ar", "16000",
                          "-f", "s16le", "-"], capture_output=True, check=True).stdout
    ses = np.frombuffer(ham, np.int16).astype(np.float32) / 32768
    m = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8", download_root=WHISPER_KLASOR)
    segs, _ = m.transcribe(ses, language="tr", word_timestamps=True, beam_size=1, condition_on_previous_text=False)
    out = [(round(float(w.start), 2), round(float(w.end), 2), w.word.strip()) for sg in segs for w in sg.words]
    json.dump(out, open(onb, "w", encoding="utf-8"), ensure_ascii=False)
    return out


def hizala(satirlar, wav_yol):
    """Her satirin sesteki [baslangic, bitis] araligi. Anlatim kelimeleri, konusma tanimadan gelen
    zamanli kelimelerle eslestirilir; eslesmeyen satir baslari komsu eslesmelerden aradegerlenir.
    Doner: (araliklar, eslesme_orani)."""
    ornek, sr, _ = wav_oku(wav_yol)
    sure = len(ornek) / sr
    if len(satirlar) == 1: return [(0.0, sure)], 1.0
    try:
        zk = kelime_zamanlari(wav_yol)
    except ImportError:
        return sessizlik_hizala(satirlar, ornek, sr), 0.0
    metin, satir_no = [], []
    for i, s in enumerate(satirlar):
        k = kelimeler(s); metin += k; satir_no += [i] * len(k)
    asr = [kelimeler(w)[0] if kelimeler(w) else "" for _, _, w in zk]
    sm = difflib.SequenceMatcher(None, metin, asr, autojunk=False)
    bas = [None] * len(metin); son = [None] * len(metin)
    for a, b, n in sm.get_matching_blocks():
        for k in range(n): bas[a + k], son[a + k] = zk[b + k][0], zk[b + k][1]
    eslesen = sum(x is not None for x in bas)
    # her kelimenin baslangicini, eslesen komsulari arasinda konum oraniyla aradegerle
    ankraj = [(i, bas[i]) for i in range(len(metin)) if bas[i] is not None]
    if len(ankraj) < 2: return sessizlik_hizala(satirlar, ornek, sr), 0.0
    def zaman(i):
        if bas[i] is not None: return bas[i]
        onceki = max((a for a in ankraj if a[0] < i), default=(0, 0.0), key=lambda a: a[0])
        sonraki = min((a for a in ankraj if a[0] > i), default=(len(metin), sure), key=lambda a: a[0])
        return onceki[1] + (sonraki[1] - onceki[1]) * (i - onceki[0]) / (sonraki[0] - onceki[0])
    ilk = {}
    for i, sn in enumerate(satir_no): ilk.setdefault(sn, i)
    sinir = []
    for sn in range(1, len(satirlar)):
        i = ilk[sn]; t = zaman(i)
        # onceki kelimenin bitisi biliniyorsa siniri aradaki boslugun ortasina koy
        if i > 0 and son[i - 1] is not None and bas[i] is not None and son[i - 1] < t: t = (son[i - 1] + t) / 2
        sinir.append(max(t, sinir[-1] + 0.05 if sinir else 0.05))
    noktalar = [0.0] + sinir + [sure]
    return [(noktalar[i], noktalar[i + 1]) for i in range(len(satirlar))], eslesen / max(1, len(metin))
