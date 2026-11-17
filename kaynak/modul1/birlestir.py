# Modul 1 tek kitap: farmakoloji bolumleri (5-8) genisletilmis yeni sayfalarla degistirilir,
# basa "Bu baska hakkinda", sona farmakoloji ezber ozeti eklenir; sayfa numaralari bastan sona yenilenir.
# kullanim: python3 -I birlestir.py [m1.txt]  (m1.txt verilirse soru kartlari temel PDF metninden yeniden ayiklanir)
import io, os, re, subprocess, sys
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
K = os.path.dirname(os.path.abspath(__file__)); Y = f"{K}/yapi"; os.makedirs(Y, exist_ok=True)
TEMEL = f"{K}/temel/Modul1_Tek_Kitap_Kisaltilmis_2026-27.pdf"
CIKTI = "/home/user/claude/ciktilar/modul1/Modul1_Tek_Kitap_Farmakoloji_Genisletilmis_2026-27.pdf"
ALT = "Modül 1 · Tek kitap (farmakoloji genişletilmiş) · 2026-27"
if len(sys.argv) > 1: subprocess.run(["python3", "-I", f"{K}/sorular_ayikla.py", sys.argv[1], f"{K}/sorular"], check=False)
subprocess.run(["python3", "-I", f"{K}/svg_uret.py"], check=True)
env = dict(os.environ, NODE_PATH=subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip())
def bas(src, ad):
    subprocess.run(["python3", "-I", f"{K}/uret.py", src, f"{Y}/{ad}.html", "Modül 1 · 2026-27"], check=True)
    subprocess.run(["node", "/home/user/claude/kaynak/modul56/build/pdf.js", f"{ad}.html", f"{ad}.pdf", ALT], check=True, env=env, cwd=Y, stdout=subprocess.DEVNULL)
    return PdfReader(f"{Y}/{ad}.pdf")
def metin(path): return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout.split("\f")
farma, on, ozet = bas(f"{K}/farma.txt", "farma"), bas(f"{K}/genis/on_not.txt", "on_not"), bas(f"{K}/genis/ozet.txt", "ozet")
temel = PdfReader(TEMEL); tt = metin(TEMEL)
bas_s = {}
for i, p in enumerate(tt):
    m = re.match(r"\s*MODÜL 1 · BÖLÜM (\d+)\s*$", p.split("\n")[0])
    if m: bas_s.setdefault(int(m.group(1)), i)
assert sorted(bas_s) == list(range(1, 10)), bas_s
# birlestir
w = PdfWriter(); isaret = []
def ekle(sayfalar): 
    ilk = len(w.pages)
    for s in sayfalar: w.add_page(s)
    return ilk
ekle(temel.pages[:bas_s[1]]); isaret.append(("Kapak, soru dizini ve içindekiler", 0, None))
isaret.append(("Bu baskı hakkında", ekle(on.pages), None))
ad = {1: "Hekimlik Hukuku ve Tıbbi Malpraktis", 2: "Periton Anatomisi", 3: "Ağrının Anatomisi: Ağrı Yolları, Visseral, Parietal ve Yansıyan Ağrı",
      4: "Akut Karın ve Peritonit", 5: "Genel Farmakoloji: Farmakokinetik", 6: "Genel Farmakoloji: Farmakodinami", 7: "Genel Anestezikler",
      8: "Ağrı Farmakolojisi: Ağrı Mediyatörleri, Opioidler ve NSAİİ", 9: "Mikrobiyolojik Tanı Yöntemleri"}
for n in range(1, 5):
    isaret.append((f"Bölüm {n}: {ad[n]}", ekle(temel.pages[bas_s[n]:bas_s[n + 1]]), None))
ilk_f = ekle(farma.pages); ft = metin(f"{Y}/farma.pdf")
for i, p in enumerate(ft):
    m = re.match(r"\s*MODÜL 1 · BÖLÜM (\d+)\s*$", p.split("\n")[0])
    if m:
        isaret.append((f"Bölüm {m.group(1)}: {ad[int(m.group(1))]}", ilk_f + i, None)); isaret.append(("Konu anlatımı", ilk_f + i, "alt"))
    if "Kolay ezber: klasik" in p: isaret.append(("Kolay ezber", ilk_f + i, "alt"))
    if "Çıkmış sorular" in p and "BU YILIN MSD-1" in p: isaret.append(("Çıkmış sorular", ilk_f + i, "alt"))
isaret.append((f"Bölüm 9: {ad[9]}", ekle(temel.pages[bas_s[9]:]), None))
isaret.append(("Farmakoloji ezber özeti", ekle(ozet.pages), None))
# altbilgi: eski numarayi ort, yenisini bas
font = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
pdfmetrics.registerFont(TTFont("Serif", font))
for i, pg in enumerate(w.pages):
    W, H = float(pg.mediabox.width), float(pg.mediabox.height)
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(W, H))
    c.setFillColorRGB(243 / 255, 242 / 255, 242 / 255); c.rect(55, 10, W - 110, 16, stroke=0, fill=1)
    c.setFillColorRGB(0x57 / 255, 0x53 / 255, 0x4e / 255); c.setFont("Serif", 6.6)
    c.drawString(78, 15.5, ALT); c.drawRightString(538.6, 15.5, str(i + 1)); c.save()
    pg.merge_page(PdfReader(io.BytesIO(buf.getvalue())).pages[0])
ust = None
for a, s, tur in isaret:
    if tur == "alt": w.add_outline_item(a, s, parent=ust)
    else: ust = w.add_outline_item(a, s)
w.add_metadata({"/Title": "Modül 1 Tek Kitap (Farmakoloji Genişletilmiş) 2026-27"})
os.makedirs(os.path.dirname(CIKTI), exist_ok=True)
with open(CIKTI, "wb") as f: w.write(f)
print("Yazıldı:", CIKTI, len(w.pages), "sayfa; farmakoloji", len(farma.pages), "sayfa (eskisi", bas_s[9] - bas_s[5], ")")
for a, s, tur in isaret: print(("   " if tur else "") + a, s + 1)
