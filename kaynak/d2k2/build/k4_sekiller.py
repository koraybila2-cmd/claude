"""Kitap 4 (D2K2 biyofizik) şemaları -> kitaplar/k4/svg/*.svg"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from svglib import SVG, NEU, CYAN, MAG  # noqa: E402

B = os.path.dirname(__file__)
OUT = os.path.join(B, "..", "kitaplar", "k4", "svg")
os.makedirs(OUT, exist_ok=True)


DA = ' stroke-dasharray="3 3"'


def dashed(s, d, color, width=2):
    s.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-dasharray="6 4"/>')


def solid(s, d, color=NEU, width=2):
    s.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"/>')


# 1. Sol ventrikül basınç-hacim döngüsünün dört değişimi
W, H = 660, 505
s = SVG(W, H, "Sol ventrikül basınç-hacim döngüsünde önyük, artyük, kontraktilite ve kompliyans değişimleri", "pv")
PW, PH = 268, 175  # çizim alanı


def edp_fn(a, b):
    return lambda v: a * (math.exp(b * (v - 20)) - 1)


F0 = edp_fn(1.25, 0.02)   # normal EDPVR (120 mL'de ≈8 mmHg)
F1 = edp_fn(0.68, 0.04)   # sert ventrikül (100 mL'de ≈16 mmHg)


def panel(ox, oy, title, sub, base, new, espvr=(), edpvr=(), fnew=F0):
    """base/new: (esv, edv, dbp, esp). Dolma kolu EDPVR üzerinde."""
    X = lambda v: ox + v / 200 * PW  # noqa: E731
    Y = lambda p: oy + PH - p / 150 * PH  # noqa: E731
    s.text(ox, oy - 26, title, "title", fs1=12.5)
    s.text(ox, oy - 11, sub, "sub", fs2=10.5)
    s.arrow(ox, oy + PH, ox + PW + 8, oy + PH, width=1)
    s.arrow(ox, oy + PH, ox, oy - 4, width=1)
    s.text(ox + PW + 8, oy + PH + 14, "hacim", "small", "end")
    s.text(ox + 6, oy + 4, "basınç", "small")

    def loop(p, f, color, dash):
        esv, edv, dbp, esp = p
        sv = edv - esv
        peak = max(dbp, esp) + 14
        d = (f"M{X(edv):.1f},{Y(f(edv)):.1f} L{X(edv):.1f},{Y(dbp):.1f} "
             f"C{X(edv - 0.12 * sv):.1f},{Y(peak + 6):.1f} {X(esv + 0.3 * sv):.1f},{Y(peak + 4):.1f} {X(esv):.1f},{Y(esp):.1f} "
             f"L{X(esv):.1f},{Y(max(f(esv), 0.5)):.1f} ")
        pts = [f"L{X(v):.1f},{Y(max(f(v), 0.5)):.1f}" for v in [esv + sv * i / 20 for i in range(1, 21)]]
        d += " ".join(pts) + " Z"
        (dashed if dash else solid)(s, d, color)

    for (v0, esv, esp, color, dash) in espvr:
        k = esp / (esv - v0)
        v1 = v0 + 135 / k
        s.add(f'<path d="M{X(v0):.1f},{Y(0):.1f} L{X(v1):.1f},{Y(135):.1f}" fill="none" stroke="{color}" '
              f'stroke-width="1" stroke-opacity="0.7"{DA if dash else ""}/>')
    for (f, vmax, color, dash) in edpvr:
        pts = [f"{X(v):.1f},{Y(f(v)):.1f}" for v in range(20, vmax + 1, 4)]
        s.add(f'<path d="M{" L".join(pts)}" fill="none" stroke="{color}" stroke-width="1" stroke-opacity="0.7"'
              f'{DA if dash else ""}/>')
    loop(base, F0, NEU, False)
    loop(new, fnew, CYAN, True)


BASE = (50, 120, 80, 100)
panel(40, 55, "a) Önyük artışı", "EDV ↑, EDP ↑, SV ↑, iş ↑ · eğriler aynı", BASE, (54, 150, 84, 104),
      espvr=[(10, 50, 100, NEU, False)], edpvr=[(F0, 160, NEU, False)])
panel(372, 55, "b) Artyük artışı", "fırlatma basıncı ↑, ESV ↑, SV ↓", BASE, (68, 120, 106, 128),
      espvr=[(10, 50, 100, NEU, False)])
panel(40, 300, "c) Kontraktilite artışı", "ESPVR dikleşir, ESV ↓, SV ↑, EF ↑", BASE, (30, 120, 82, 106),
      espvr=[(10, 50, 100, NEU, False), (10, 30, 106, CYAN, True)])
panel(372, 300, "d) Kompliyans azalması", "EDPVR dikleşir, EDV ↓, EDP ↑, SV ↓, iş ↓", BASE, (44, 100, 80, 98),
      edpvr=[(F0, 160, NEU, False), (F1, 118, CYAN, True)], fnew=F1)
s.text(W / 2, H - 4, "düz çizgi: başlangıç döngüsü · kesikli çizgi: değişimden sonra · ince çizgiler: ESPVR (a-c) ve EDPVR (a, d)",
       "small", "middle")
s.save(os.path.join(OUT, "k4_pv.svg"))


# 2. Akciğer basınç-hacim eğrisi: normal, amfizem, fibroz/RDS
W, H = 660, 300
s = SVG(W, H, "Akciğer basınç-hacim eğrisi: amfizemde sola-yukarı, fibroz ve RDS'de sağa-aşağı kayar", "lp")
ox, oy, PW, PH = 70, 25, 300, 220
X = lambda p: ox + p / 32 * PW  # noqa: E731
Y = lambda v: oy + PH - v / 7.5 * PH  # noqa: E731
s.arrow(ox, oy + PH, ox + PW + 8, oy + PH, width=1)
s.arrow(ox, oy + PH, ox, oy - 6, width=1)
s.text(ox + PW / 2, oy + PH + 32, "transpulmoner basınç (cmH₂O)", "small", "middle")
s.text(ox - 10, oy + PH / 2, "akciğer hacmi (L)", "small", "middle", rotate=-90)
for p in (0, 10, 20, 30):
    s.text(X(p), oy + PH + 14, str(p), "small", "middle")
curves = [("Amfizem", 1.6, 6.9, 3.2, MAG, True), ("Normal", 1.0, 6.0, 7.0, NEU, False),
          ("Fibroz · RDS", 0.6, 3.9, 13.0, CYAN, True)]
for name, v0, vmax, k, color, dash in curves:
    pts = [f"{X(p):.1f},{Y(v0 + (vmax - v0) * (1 - math.exp(-p / k))):.1f}" for p in [i * 0.5 for i in range(0, 61)]]
    d = "M" + " L".join(pts)
    (dashed if dash else solid)(s, d, color)
    s.text(X(30) + 6, Y(v0 + (vmax - v0) * (1 - math.exp(-30 / k))) + 4, name, "magb" if color == MAG else ("cyanb" if color == CYAN else "title"), fs1=11.5)
s.box(470, 30, 180, 105, [("Kompliyans ↑ (amfizem, yaşlılık)", "magb"),
                          ("eğri sola-yukarı, dik", "body"),
                          ("FRC, RV, TLC ↑", "body"),
                          ("aynı ΔP ile daha çok hacim", "body"),
                          ("hava hapsi, ekspirasyon güç", "body")],
      kind="mag", align="start", pad_top=18, lh=16, fs2=10.5)
s.box(470, 145, 180, 105, [("Kompliyans ↓ (fibroz, RDS, ödem)", "cyanb"),
                           ("eğri sağa-aşağı, düz", "body"),
                           ("tüm hacimler ↓", "body"),
                           ("şişirmek için büyük basınç", "body"),
                           ("elastik iş ↑, τ = R·C ↓", "body")],
      kind="key", align="start", pad_top=18, lh=16, fs2=10.5)
s.save(os.path.join(OUT, "k4_akc_pv.svg"))
print("ok")
