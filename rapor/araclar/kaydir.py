#!/usr/bin/env python3
"""Araya yeni bölüm eklemek için bölüm numaralarını kaydırır.

Kullanım: python3 araclar/kaydir.py <eşik> [--uygula]
<eşik> ve üzerindeki bölüm numaraları bir artırılır: dosya adları (bolumler/, sozluk/)
ve metindeki "Bölüm N" atıfları (Türkçe bulunma ekleri ses uyumuna göre düzeltilerek).
--uygula verilmezse yalnızca yapılacak değişiklikleri listeler.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ESIK = int(sys.argv[1])
UYGULA = "--uygula" in sys.argv

LOC = {1: "de", 2: "de", 3: "te", 4: "te", 5: "te", 6: "da", 7: "de", 8: "de", 9: "da"}


def bulunma(n):
    if n % 10:
        return LOC[n % 10]
    return {10: "da", 20: "de", 30: "da"}[n % 100 if n % 100 else 10]


def yeni(n):
    return n + 1 if n >= ESIK else n


RE = re.compile(r"(Bölüm\s)(\d+(?:(?:\s*,\s*|\s*[–-]\s*|\s+ve\s+)\d+)*)('(?:de|da|te|ta)(?:ki|dır|dir|tır|tir)?)?")


def cevir(m):
    nums = m.group(2)
    parts = re.split(r"(\s*,\s*|\s*[–-]\s*|\s+ve\s+)", nums)
    out, last = [], None
    for p in parts:
        if p.isdigit():
            last = yeni(int(p))
            out.append(str(last))
        else:
            out.append(p)
    suf = m.group(3) or ""
    if suf:
        rest = suf[3:]
        loc = bulunma(last)
        if rest in ("dır", "dir", "tır", "tir"):
            rest = {"de": "dir", "da": "dır", "te": "tir", "ta": "tır"}[loc]
        suf = "'" + loc + rest
    return m.group(1) + "".join(out) + suf


degisen = 0
for p in sorted((ROOT / "bolumler").glob("*.md")) + [ROOT / "build.py"]:
    s = p.read_text(encoding="utf-8")
    t = RE.sub(cevir, s)
    if t != s:
        for a, b in zip(RE.findall(s), RE.findall(t)):
            if a != b:
                degisen += 1
                print(f"{p.name}: Bölüm {a[1]}{a[2]} -> Bölüm {b[1]}{b[2]}")
        if UYGULA:
            p.write_text(t, encoding="utf-8")

# dosya adlarını büyükten küçüğe yeniden adlandır
for klasor in ("bolumler", "sozluk"):
    dosyalar = [f for f in (ROOT / klasor).glob("*.md") if re.match(r"\d{2}", f.name)]
    for f in sorted(dosyalar, key=lambda f: f.name, reverse=True):
        n = int(f.name[:2])
        if n >= ESIK:
            hedef = f.with_name(f"{n + 1:02d}" + f.name[2:])
            print(f"{klasor}/{f.name} -> {hedef.name}")
            if UYGULA:
                f.rename(hedef)
print(f"{degisen} atıf değişikliği")
