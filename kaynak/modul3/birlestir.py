# Modul 3 birlesik tek kitap: sorulari ayiklar (metin verilirse), kitabi basar, yer imlerini ekler.
# kullanim: python3 -I birlestir.py [m3.txt]   (m3.txt = temel PDF'in pdftotext ciktisi; verilmezse sorular/ oldugu gibi kullanilir)
import os, re, subprocess, sys
from pypdf import PdfReader, PdfWriter
K = os.path.dirname(os.path.abspath(__file__)); Y = f"{K}/yapi"; os.makedirs(Y, exist_ok=True)
CIKTI = "/home/user/claude/ciktilar/modul3/Modul3_Tek_Kitap_Birlesik_2026-27.pdf"
if len(sys.argv) > 1: subprocess.run(["python3", "-I", f"{K}/sorular_ayikla.py", sys.argv[1], f"{K}/sorular"], check=True)
subprocess.run(["python3", "-I", f"{K}/svg_uret.py"], check=True)
subprocess.run(["python3", "-I", f"{K}/uret.py", f"{K}/kitap.txt", f"{Y}/kitap.html", "Modül 3 · 2026-27"], check=True)
env = dict(os.environ, NODE_PATH=subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip())
subprocess.run(["node", "/home/user/claude/kaynak/modul56/build/pdf.js", "kitap.html", "kitap.pdf", "Modül 3 · Tek kitap · 2026-27"], check=True, env=env, cwd=Y, stdout=subprocess.DEVNULL)
r = PdfReader(f"{Y}/kitap.pdf"); w = PdfWriter(); w.append(r, import_outline=False)
sayfa = subprocess.run(["pdftotext", f"{Y}/kitap.pdf", "-"], capture_output=True, text=True).stdout.split("\f")
w.add_outline_item("Kapak", 0); ust = None
for i, p in enumerate(sayfa):
    bas = [s.strip() for s in p.split("\n") if s.strip()][:3]
    if bas and re.fullmatch(r"MODÜL 3 · (BÖLÜM \d+|EZBER ÖZETİ|2026-27)", bas[0]) and len(bas) > 1 and i > 0:
        m = re.search(r"BÖLÜM (\d+)", bas[0])
        ust = w.add_outline_item((f"Bölüm {m.group(1)}: " if m else "") + bas[1] + (" " + bas[2] if m and bas[2][:1].isupper() and len(bas[2]) < 12 else ""), i)
        if m: w.add_outline_item("Konu anlatımı", i, parent=ust)
    if ust is not None and "Çıkmış sorular" in p and "BU YILIN SORULARI" in p: w.add_outline_item("Çıkmış sorular", i, parent=ust)
w.add_metadata({"/Title": "Modül 3 Tek Kitap (Birleşik) 2026-27"})
os.makedirs(os.path.dirname(CIKTI), exist_ok=True)
with open(CIKTI, "wb") as f: w.write(f)
print("Yazıldı:", CIKTI, len(w.pages), "sayfa")
