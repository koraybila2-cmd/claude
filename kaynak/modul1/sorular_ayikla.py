# Kisaltilmis tek kitap PDF metninden bolum bolum soru kartlarini ayiklar -> sorular/sN.txt (uret.py bicimi).
# kullanim: python3 -I sorular_ayikla.py m3.txt cikti_klasoru
import re, sys
src, outd = sys.argv[1:3]
T = open(src, encoding="utf-8").read().replace("\f", "\n").split("\n")
# sayfa alt bilgisi -> isaret
L, i = [], 0
while i < len(T):
    s = T[i].strip()
    if re.fullmatch(r"Modül \d(-\d)? · Kısaltılmış tek kitap · 2026-27", s):
        j = i + 1
        while j < len(T) and not T[j].strip(): j += 1
        if j < len(T) and re.fullmatch(r"\d+", T[j].strip()): j += 1
        while L and not L[-1]: L.pop()
        while j < len(T) and not T[j].strip(): j += 1
        L.append("\x00"); i = j; continue
    L.append(s); i += 1
M = []
for s in L:
    if s.startswith("SORU ") and M and M[-1].endswith(" ·"): M[-1] += " " + s
    else: M.append(s)
L = M
bol = [k for k, s in enumerate(L) if re.fullmatch(r"MODÜL \d · BÖLÜM \d+", s)]
BAS = re.compile(r"^((MODÜL \d|MSD-\d|BSD-\d|BSD) \d{4}-\d{2} · SORU( \d+)?)$")
KISIM = re.compile(r"^(BU YILIN SORULARI?|GEÇEN YILIN .*|DAHA ESKİ( BLOK SINAVI)? SORULAR(I)?)$")
ROZET = {"BU YIL", "GEÇEN YIL", "BLOK SINAVI", "BU", "YIL"}
ACIK = re.compile(r"^([A-E]( ve [A-E])? [a-zçğıöşü(]|Doğru |Cevap |Anahtar|İptal|Soru |Yalnız|I[, ])")
def birles(par):  # satirlari paragraflara
    out, cur = [], ""
    for s in par:
        if s == "\x00":
            if cur and cur[-1] in ".!?:”)": out.append(cur); cur = ""
            continue
        if not s:
            if cur: out.append(cur); cur = ""
            continue
        cur = (cur[:-1] if cur.endswith("-") and s[:1].islower() else cur + (" " if cur else "")) + s if cur else s
    if cur: out.append(cur)
    return out
uyari = 0
for b, k0 in enumerate(bol):
    k1 = bol[b + 1] if b + 1 < len(bol) else len(L)
    n = int(L[k0].split()[-1]); seg = L[k0:k1]
    son = next((x for x, s in enumerate(seg) if re.match(rf"^{n}\.1\. Konu tekrarı", s)), len(seg))
    ilk = next(x for x, s in enumerate(seg) if KISIM.match(s))
    seg = seg[ilk:son]; out = []; x = 0
    while x < len(seg):
        s = seg[x]
        if s in ("", "\x00"): x += 1; continue
        if KISIM.match(s):
            out.append("@QB " + s); x += 1
            if s.startswith("DAHA ESKİ"):
                y = x
                while y < len(seg) and not BAS.match(seg[y]) and not KISIM.match(seg[y]): y += 1
                ham = [t for t in seg[x:y]]
                # her "BSD/MSD ..." ile baslayan satir yeni madde
                mad, cur = [], []
                for t in ham:
                    if t in ("", "\x00"): continue
                    if re.match(r"^((BSD|MSD)[ -]|\d{4}-\d{2} S\d+)", t) and cur and cur[-1][-1:] in ".)”":
                        mad.append(cur); cur = []
                    cur.append(t)
                if cur: mad.append(cur)
                for m_ in mad: out.append("@E " + birles(m_ + [""])[0] if len(birles(m_)) == 1 else "@E " + " ".join(birles(m_)))
                x = y
            continue
        m = BAS.match(s)
        if not m:
            print(f"UYARI b{n}: beklenmeyen satir: {s[:80]}"); uyari += 1; x += 1; continue
        bas = s; x += 1
        y = x
        while y < len(seg) and not BAS.match(seg[y]) and not KISIM.match(seg[y]): y += 1
        govde = seg[x:y]; x = y
        # baslik devam (numara ayri satirda), rozet, etiket
        z = 0; etiket = []; rozet = ""
        if bas.endswith("SORU"):
            while z < len(govde) and not re.fullmatch(r"\d+", govde[z]): z += 1
            bas += " " + govde[z]; govde = govde[:z] + govde[z + 1:]; z = 0
        while z < len(govde) and (govde[z] in ("", "\x00") or govde[z] in ROZET or (govde[z].upper() == govde[z] and re.search(r"[A-ZÇĞİÖŞÜ]{3}", govde[z]) and not re.match(r"^[A-E]\) ", govde[z]) and not etiket_bitti)) if (etiket_bitti := False) or True else False:
            t = govde[z]; z += 1
            if t in ROZET: rozet = (rozet + " " + t).strip()
            elif t not in ("", "\x00"): etiket.append(t)
        kalan = govde[z:]
        oi = next((q for q, t in enumerate(kalan) if re.match(r"^A\) ", t)), None)
        if oi is None:
            print(f"UYARI b{n} {bas}: sik bulunamadi"); uyari += 1; continue
        kok, cur = [], ""
        for t in kalan[:oi]:
            if t in ("", "\x00"): continue
            if cur and not re.match(r"^((I{1,3}|IV|V|VI{1,3})[\.\-\)]|[IVX]+\s*[-–])\s?", t) and not re.match(r"^(I{1,3}|IV|V)[\.\-\)]", cur.split(" ")[0] + "") : cur += " " + t
            elif cur and re.match(r"^((I{1,3}|IV|V|VI{1,3})[\.\-\)]|[IVX]+\s*[-–])", t): kok.append(cur); cur = t
            elif cur: 
                # onceki satir oncul; yeni satir oncul degilse: buyuk harfle basliyor ve onceki nokta ile bittiyse yeni satir
                if cur[-1:] in ".?:" and t[:1].isupper(): kok.append(cur); cur = t
                else: cur += " " + t
            else: cur = t
        if cur: kok.append(cur)
        sik, q = [], oi
        while q < len(kalan):
            t = kalan[q]
            if re.match(r"^[A-E]\) ", t): sik.append(t)
            elif t in ("", "\x00"):
                if len(sik) >= 5 or (q + 1 < len(kalan) and not re.match(r"^[A-E]\) ", next((u for u in kalan[q + 1:] if u not in ("", "\x00")), "")) and len(sik) >= 4): 
                    q += 1; break
            elif t.startswith("Önceki yıllar:") or (len(sik) >= 4 and ACIK.match(t)): break
            else: sik[-1] += " " + t
            q += 1
        son_ = kalan[q:]
        onceki, acik = [], son_
        w = next((u for u, t in enumerate(son_) if t not in ("", "\x00")), 0)
        if son_[w:w + 1] and son_[w].startswith("Önceki yıllar:"):
            e = w
            while e < len(son_) and son_[e] != "" and not (e > w and ACIK.match(son_[e]) and son_[e - 1][-1:] in ".”)\x00"): e += 1
            onceki = birles(son_[w:e]); acik = son_[e:]
        ap = birles(acik)
        for t in sik:
            if len(t) > 220: print(f"UYARI b{n} {bas}: uzun sik: {t[:60]}...{t[-60:]}"); uyari += 1
        if not ap: print(f"UYARI b{n} {bas}: aciklama yok"); uyari += 1
        if len(sik) not in (4, 5) or sum("✓" in t for t in sik) != 1: print(f"UYARI b{n} {bas}: sik sayisi {len(sik)} / isaret {sum('✓' in t for t in sik)}"); uyari += 1
        out.append(f"@Q {bas} | {rozet} | {' '.join(etiket)}")
        out += ["@K " + t for t in kok] + sik + ["@O " + " ".join(onceki)] * bool(onceki) + ap + ["@@"]
    open(f"{outd}/s{n}.txt", "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"bolum {n}: {sum(t.startswith('@Q') for t in out)} kart, {sum(t.startswith('@E') for t in out)} eski madde")
print("uyari:", uyari)
