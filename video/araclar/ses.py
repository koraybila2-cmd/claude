#!/usr/bin/env python3
"""parcalar.txt'teki parcalari Gemini TTS ile seslendirir (Interactions API).

kullanim (repo kokunden, GEMINI_API_KEY ortamda olmali):
  python3 -I video/araclar/ses.py video/k5b3                            # butun parcalar -> video/k5b3/ses/ (ses: video/sesler.json)
  python3 -I video/araclar/ses.py video/k5b3 --ses Puck --parca k5b3_01 --cikti ornek.wav
Var olan wav dosyalari yeniden uretilmez (gunluk kota icin).
"""
import argparse, base64, json, os, re, sys, time, urllib.error, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bolum

MODEL = "gemini-3.8-flash-tts"
URL = "https://generativelanguage.googleapis.com/v1beta/interactions"
USLUP = ("Aşağıdaki Türkçe metni, sosyal medyada tıp eğitimi videoları anlatan enerjik, samimi ve akıcı bir anlatıcı gibi oku. "
         "Hızın orta-hızlı olsun. Önemli terimleri, sayıları ve doğru cevapları sesinle hafifçe vurgula; soru cümlelerinden ve "
         "\"Durdur ve düşün\" cümlesinden sonra kısa bir es ver. Metni kelimesi kelimesine oku: hiçbir şeyi atlama, ekleme, "
         "çevirme ya da özetleme.")


def parcalari_oku(yol):
    return {a: "\n".join(p["satirlar"]) for a, p in bolum.parcalari_oku(yol).items()}


def seslendir(metin, ses, anahtar):
    govde = {
        "model": MODEL,
        "input": [{"type": "user_input", "content": [{"type": "text", "text": metin,
                   "annotations": [{"type": "speech_metadata", "style": USLUP}]}]}],
        "response_format": {"type": "audio"},
        "generation_config": {"speech_config": [{"voice": ses}]},
    }
    istek = urllib.request.Request(URL, data=json.dumps(govde).encode(), method="POST",
                                   headers={"x-goog-api-key": anahtar, "Content-Type": "application/json"})
    for deneme in range(4):
        try:
            with urllib.request.urlopen(istek, timeout=600) as r:
                yanit = json.load(r)
            break
        except urllib.error.HTTPError as e:
            govde_hata = e.read().decode(errors="replace")[:500]
            if e.code in (429, 500, 503) and deneme < 3:
                print(f"  {e.code}, {30 * (deneme + 1)} sn sonra tekrar", file=sys.stderr); time.sleep(30 * (deneme + 1)); continue
            sys.exit(f"HTTP {e.code}: {govde_hata}")
    sesler = [c["data"] for s in yanit.get("steps", []) if s.get("type") == "model_output"
              for c in s.get("content", []) if c.get("type") == "audio"]
    if not sesler:
        sys.exit("yanitta ses yok: " + json.dumps(yanit)[:500])
    return base64.b64decode(sesler[-1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("klasor"); ap.add_argument("--ses")
    ap.add_argument("--parca"); ap.add_argument("--cikti")
    a = ap.parse_args()
    if not a.ses:
        kitap = re.match(r"k(\d+)b", os.path.basename(os.path.abspath(a.klasor))).group(1)
        a.ses = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sesler.json")))[kitap]
    anahtar = os.environ.get("GEMINI_API_KEY", "").strip()
    if not anahtar:
        sys.exit("GEMINI_API_KEY tanimli degil")
    parcalar = parcalari_oku(os.path.join(a.klasor, "parcalar.txt"))
    secili = [a.parca] if a.parca else list(parcalar)
    for ad in secili:
        hedef = a.cikti or os.path.join(a.klasor, "ses", ad + ".wav")
        if os.path.exists(hedef) and not a.cikti:
            print(ad, "var, atlandi"); continue
        os.makedirs(os.path.dirname(os.path.abspath(hedef)), exist_ok=True)
        t = time.time()
        veri = seslendir(parcalar[ad], a.ses, anahtar)
        open(hedef, "wb").write(veri)
        print(ad, a.ses, f"{len(veri) / 48000:.1f} sn ses, {time.time() - t:.0f} sn surdu ->", hedef)


if __name__ == "__main__":
    main()
