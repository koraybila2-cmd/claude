#!/usr/bin/env python3
"""Uygulama rehberinden (Bölüm 20) yalnızca antrenman programını içeren kısa bir HTML üretir.

Kullanım: python3 araclar/program_pdf.py <çıktı.html>
Beslenme, takviye ve uyku bölümleri dışarıda bırakılır; atıf numaraları silinir.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import build  # noqa: E402

KAYNAK = build.BOLUMLER / "20-uygulama-rehberi.md"
BOLUMLER = [
    "16 haftanın genel yapısı",
    "Haftalık program",
    "Ağırlık antrenmanı",
    "Kardiyo planı",
    "Baldır ve peroneal rehabilitasyon zaman çizelgesi",
]


def bolumleri_al(metin):
    parcalar = re.split(r"(?m)^(?=## )", metin)
    secilen = []
    for p in parcalar:
        baslik = p.splitlines()[0][3:].strip() if p.startswith("## ") else ""
        if baslik in BOLUMLER:
            secilen.append(p.rstrip() + "\n")
    return secilen


def beslenme_sutununu_at(bolum):
    """16 haftalık yapı tablosundaki son (Beslenme) sütununu çıkarır."""
    satirlar = []
    for ln in bolum.splitlines():
        if ln.startswith("|"):
            hucreler = ln.strip().strip("|").split("|")
            ln = "|" + "|".join(hucreler[:-1]) + "|"
        satirlar.append(ln)
    return "\n".join(satirlar) + "\n"


def main(cikti):
    metin = KAYNAK.read_text(encoding="utf-8")
    bolumler = bolumleri_al(metin)
    bolumler = [beslenme_sutununu_at(b) if b.startswith("## 16 haftanın") else b for b in bolumler]
    govde = "\n".join(bolumler)
    govde = re.sub(r"\s?\[\d{1,3}(?:\s*[,–-]\s*\d{1,3})*\]", "", govde)

    giris = (
        "# Antrenman Programı: 16 Haftalık Plan\n\n"
        "Bu belge, *Ağırlık Antrenmanı, Kardiyo ve Beslenme* raporunun Bölüm 20'sindeki uygulama rehberinden "
        "yalnızca antrenman kısmını içerir: haftalık düzen, ağırlık antrenmanı seansları, kardiyo planı ve baldır "
        "rehabilitasyonu. Parantez içindeki bölüm numaraları, ana rapordaki ayrıntılı açıklamalara işaret eder.\n\n"
    )
    tmp = build.ROOT / "build" / "program.md"
    tmp.parent.mkdir(exist_ok=True)
    tmp.write_text(giris + govde, encoding="utf-8")

    toc = []
    bolum_html = build.process_chapter("PRG", [tmp], "Uygulama rehberi · antrenman kısmı", "", False, toc)
    bolum_html = bolum_html.replace('<span class="sn">.', '<span class="sn">')
    bolum_html = bolum_html.replace('<section class="chapter"', '<section class="chapter" style="break-before:auto"', 1)

    html = f"""<!doctype html>
<html lang="tr"><head><meta charset="utf-8">
<title>Antrenman Programı — 16 Haftalık Plan</title>
<link rel="stylesheet" href="style.css">
<style>@page {{ @top-right {{ content: "Antrenman Programı · 16 Haftalık Plan"; }} }} .table-wrap {{ break-inside: avoid; }}</style>
</head><body>
{bolum_html}
</body></html>"""
    Path(cikti).write_text(html, encoding="utf-8")
    print(f"yazıldı: {cikti}")


if __name__ == "__main__":
    main(sys.argv[1])
