#!/usr/bin/env python3
"""Bir bolumun anlatim metninden ve seslerinden video uretir.

kullanim (repo kokunden): /home/user/venv/bin/python -I video/araclar/video.py video/k5b3 [cikti.mp4]

Girdi klasorunde: parcalar.txt (anlatim), sahne.json (satir -> blok eslemesi), ses/<parca>.wav (varsa).
Satirlarin sesteki yeri konusma tanimayla (Whisper) bulunur; "dur" isaretli satirlardan sonra sese ve
goruntuye dusunme arasi eklenir. Ses dosyasi olmayan parcalarin suresi karakter sayisindan tahmin edilir
ve video sessiz uretilir (goruntu onizlemesi).
"""
import json, os, subprocess, sys, tempfile, wave
import imageio_ffmpeg

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bolum

PARCA_ARASI = 0.6      # parcalar arasi sessizlik (sn)
ORNEK_HIZ = 24000


def main():
    klasor = os.path.abspath(sys.argv[1])
    ad_b = os.path.basename(klasor)
    cikti = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.join(klasor, ad_b + ".mp4")
    sahne, girdiler = bolum.sahne_oku(klasor)
    parcalar = bolum.parcalari_oku(os.path.join(klasor, "parcalar.txt"))
    if list(parcalar) != list(girdiler):
        sys.exit("parcalar.txt ile sahne.json parca listesi uyusmuyor")
    sesler = {a: os.path.join(klasor, "ses", a + ".wav") for a in parcalar}
    ses_var = all(os.path.exists(y) for y in sesler.values())

    ipuclari, ses_plan, acik = [], [], []
    for ad, p in parcalar.items():
        satirlar, gs = p["satirlar"], girdiler[ad]
        if len(gs) != len(satirlar):
            sys.exit(f"{ad}: {len(satirlar)} satir var, sahne.json'da {len(gs)} girdi")
        if os.path.exists(sesler[ad]):
            araliklar, oran = bolum.hizala(satirlar, sesler[ad])
            print(f"{ad}: hizalama, kelime eslesmesi %{oran * 100:.0f}", flush=True)
        else:
            sure = sum(map(len, satirlar)) / bolum.TAHMIN_HIZ; t = 0; araliklar = []
            for s in satirlar:
                d = sure * len(s) / sum(map(len, satirlar)); araliklar.append((t, t + d)); t += d
        kesimler = []                       # (sesteki zaman, eklenecek sessizlik)
        for (bas, son), g in zip(araliklar, gs):
            if g["ac"] and g["ac"] not in acik: acik.append(g["ac"])
            ipuclari.append({"parca": ad, "sel": g["sel"], "sure": (son - bas) + g["dur"], "acik": list(acik)})
            if g["dur"]: kesimler.append((son, g["dur"]))
        ipuclari[-1]["sure"] += PARCA_ARASI
        ses_plan.append((sesler[ad], kesimler))

    with tempfile.TemporaryDirectory() as tmp:
        html = bolum.bolum_html_kur(sahne, tmp)
        cz = os.path.join(tmp, "cizelge.json")
        json.dump({"ust_baslik": sahne["ust_baslik"], "ipuclari": ipuclari}, open(cz, "w"), ensure_ascii=False)
        kare_d = os.path.join(tmp, "kareler")
        subprocess.run(["node", os.path.join(bolum.KOK, "video/araclar/kareler.js"), html, cz, kare_d],
                       check=True, env=bolum.node_env())

        ff = imageio_ffmpeg.get_ffmpeg_exe()
        toplam = sum(i["sure"] for i in ipuclari)
        if ses_var:
            ses = os.path.join(tmp, "ses.wav")
            with wave.open(ses, "wb") as out:
                for j, (yol, kesimler) in enumerate(ses_plan):
                    with wave.open(yol) as w:
                        if j == 0: out.setparams(w.getparams())
                        sr, bayt = w.getframerate(), w.getsampwidth() * w.getnchannels()
                        veri = w.readframes(w.getnframes())
                    sessiz = lambda sn: b"\x00" * int(sn * sr) * bayt
                    onceki = 0
                    for zaman, ek in kesimler:
                        k = int(zaman * sr) * bayt
                        out.writeframes(veri[onceki:k] + sessiz(ek)); onceki = k
                    out.writeframes(veri[onceki:] + sessiz(PARCA_ARASI))
            ses_girdi = ["-i", ses]
        else:
            ses_girdi = ["-f", "lavfi", "-t", f"{toplam:.2f}", "-i", f"anullsrc=r={ORNEK_HIZ}:cl=mono"]
        subprocess.run([ff, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(kare_d, "liste.txt"),
                        *ses_girdi, "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                        "-tune", "stillimage", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", cikti],
                       check=True)
    print(("sesli" if ses_var else "SESSIZ onizleme"), "video:", cikti, f"({toplam/60:.1f} dk)")


if __name__ == "__main__":
    main()
