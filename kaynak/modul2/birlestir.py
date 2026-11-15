# Modul 2 kisaltilmis tek kitabina ayrintili anlatim bolumlerini ekler.
# kullanim: python3 -I birlestir.py
import glob, os, re, subprocess
from pypdf import PdfReader, PdfWriter

K = "/home/user/claude/kaynak/modul2"
TEMEL = f"{K}/temel/Modul2_Tek_Kitap_Kisaltilmis_2026-27.pdf"
CIKTI = "/home/user/claude/ciktilar/modul2/Modul2_Tek_Kitap_Ayrintili_2026-27.pdf"
PDFJS = "/home/user/claude/kaynak/modul56/build/pdf.js"
YAPI = f"{K}/yapi"
os.makedirs(YAPI, exist_ok=True); os.makedirs(os.path.dirname(CIKTI), exist_ok=True)
NODE = dict(os.environ, NODE_PATH=subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip())

def bas(txt, ad, kicker):
    html = f"{YAPI}/{ad}.html"; pdf = f"{YAPI}/{ad}.pdf"
    subprocess.run(["python3", "-I", f"{K}/uret.py", txt, html, kicker], check=True)
    subprocess.run(["node", PDFJS, html, pdf, "Modül 2 · Ayrıntılı anlatım · 2026-27"], check=True, env=NODE, cwd=YAPI, stdout=subprocess.DEVNULL)
    return PdfReader(pdf)

# 1) ekleri bas
ekler = {}
for txt in sorted(glob.glob(f"{K}/genis/b*.txt")):
    n = int(re.match(r"b(\d+)_", os.path.basename(txt)).group(1))
    ekler[n] = bas(txt, f"b{n}", f"Modül 2 · Bölüm {n} · Ayrıntılı anlatım")
on = bas(f"{K}/genis/on_not.txt", "on_not", "Modül 2 · 2026-27") if os.path.exists(f"{K}/genis/on_not.txt") else None

# 2) temel kitapta bolum baslangiclarini bul
temel = PdfReader(TEMEL)
bas_sayfa, basliklar = {}, {}
for i in range(len(temel.pages)):
    t = subprocess.run(["pdftotext", "-f", str(i + 1), "-l", str(i + 1), "-layout", TEMEL, "-"], capture_output=True, text=True).stdout
    satirlar = [s.strip() for s in t.splitlines() if s.strip()]
    for j, s in enumerate(satirlar[:4]):
        m = re.fullmatch(r"MODÜL 2 · BÖLÜM (\d+)", s)
        if m and int(m.group(1)) not in bas_sayfa:
            n = int(m.group(1)); bas_sayfa[n] = i; basliklar[n] = satirlar[j + 1] if j + 1 < len(satirlar) else ""
print("Bölüm başları:", {k: v + 1 for k, v in sorted(bas_sayfa.items())})
assert sorted(bas_sayfa) == list(range(1, 11)), bas_sayfa

# 3) birlestir
ADLAR = {1: "Akılcı İlaç Kullanımı ve Farmakovijilans", 9: "SLE ve Diğer Bağ Dokusu Hastalıkları"}
w = PdfWriter()
def ekle(reader):
    ilk = len(w.pages)
    for p in reader.pages: w.add_page(p)
    return ilk
isaret = []
sonraki = {n: bas_sayfa.get(n + 1, len(temel.pages)) for n in bas_sayfa}
for i in range(bas_sayfa[1]): w.add_page(temel.pages[i])
if bas_sayfa[1]: isaret.append(("Kapak ve genel bakış", 0, None))
if on: isaret.append(("Bu baskı hakkında", ekle(on), None))
for n in sorted(bas_sayfa):
    ilk = len(w.pages)
    for i in range(bas_sayfa[n], sonraki[n]): w.add_page(temel.pages[i])
    isaret.append((f"Bölüm {n}: {ADLAR.get(n, basliklar[n])}", ilk, None))
    if n in ekler: isaret.append(("Ayrıntılı anlatım", ekle(ekler[n]), "alt"))
ust = None
for ad, sayfa, tur in isaret:
    if tur == "alt": w.add_outline_item(ad, sayfa, parent=ust)
    else: ust = w.add_outline_item(ad, sayfa)
w.add_metadata({"/Title": "Modül 2 Tek Kitap (Ayrıntılı) 2026-27"})
with open(CIKTI, "wb") as f: w.write(f)
print("Yazıldı:", CIKTI, len(w.pages), "sayfa; ekler:", {n: len(r.pages) for n, r in ekler.items()})
