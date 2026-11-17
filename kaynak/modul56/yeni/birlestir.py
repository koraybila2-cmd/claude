# Modul 5-6 tek kitap 2026-27 guncellemesi: her bolumun basina 2026-27 kartlari ve konu eki, basa genel bakis, sona ezber listesi.
# kullanim: python3 -I yeni/birlestir.py
import io, os, re, subprocess
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
K = os.path.dirname(os.path.abspath(__file__)); Y = f"{K}/yapi"; os.makedirs(Y, exist_ok=True)
TEMEL = f"{K}/../temel/Modul5-6_Tek_Kitap_Kisaltilmis_2025-26.pdf"
CIKTI = "/home/user/claude/ciktilar/modul56/Modul5-6_Tek_Kitap_Kisaltilmis_2026-27.pdf"
ALT = "Modül 5-6 · Kısaltılmış tek kitap · 2026-27 sorularıyla güncel"
subprocess.run(["python3", "-I", f"{K}/olustur.py"], check=True)
env = dict(os.environ, NODE_PATH=subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip())
def bas(ad):
    subprocess.run(["python3", "-I", f"{K}/uret.py", f"{K}/yapi_txt/{ad}.txt", f"{Y}/{ad}.html", "Modül 5-6 · 2026-27"], check=True)
    subprocess.run(["node", "/home/user/claude/kaynak/modul56/build/pdf.js", f"{ad}.html", f"{ad}.pdf", ALT], check=True, env=env, cwd=Y, stdout=subprocess.DEVNULL)
    return PdfReader(f"{Y}/{ad}.pdf")
yeni = {n: bas(f"b{n}") for n in range(1, 12)}; on, ezb = bas("on"), bas("ezber")
temel = PdfReader(TEMEL)
tt = subprocess.run(["pdftotext", TEMEL, "-"], capture_output=True, text=True).stdout.split("\f")
bs = {}
for i, p in enumerate(tt):
    m = re.match(r"\s*MODÜL 5-6 · BÖLÜM (\d+)\s*\n", p)
    if m: bs.setdefault(int(m.group(1)), i)
assert sorted(bs) == list(range(1, 12)), bs
BOL = {1: "Beslenme ve Büyüme İzlemi", 2: "Malnütrisyon ve Raşitizm", 3: "İshal, Malabsorbsiyon ve Çölyak", 4: "Sindirim Sistemi Anatomisi ve Histolojisi",
       5: "Açlık Biyokimyası ve Üre Döngüsü", 6: "Sıvı-Elektrolit Dengesi ve Tübül Fizyolojisi", 7: "Akut Böbrek Hasarı, Diyaliz ve Nefrotoksisite",
       8: "Glomerül Hastalıkları", 9: "Kronik Böbrek Hastalığı, Diyabetik Nefropati ve Hipertansiyon", 10: "Diüretikler, ACE İnhibitörleri, ARB ve Kalsiyum Kanal Blokerleri",
       11: "Dermatofitler ve Diğer Mantarlar"}
w = PdfWriter(); isaret = []
def ekle(sayfalar):
    ilk = len(w.pages)
    for s in sayfalar: w.add_page(s)
    return ilk
isaret.append(("2026-27 güncellemesi: genel bakış ve soru dizini", ekle(on.pages), None))
isaret.append(("Önceki baskının girişi (2025-26 analizi)", ekle(temel.pages[:bs[1]]), None))
for n in range(1, 12):
    ilk = ekle(yeni[n].pages)
    isaret.append((f"Bölüm {n}: {BOL[n]}", ilk, None)); isaret.append(("2026-27 soruları ve konu eki", ilk, "alt"))
    son = bs.get(n + 1, len(temel.pages))
    isaret.append(("2025-26 ve 2024-25 soruları, konu tekrarı", ekle(temel.pages[bs[n]:son]), "alt"))
isaret.append(("2026-27 ezber listesi", ekle(ezb.pages), None))
pdfmetrics.registerFont(TTFont("Serif", "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"))
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
w.add_metadata({"/Title": "Modül 5-6 Tek Kitap (Kısaltılmış) 2026-27"})
os.makedirs(os.path.dirname(CIKTI), exist_ok=True)
with open(CIKTI, "wb") as f: w.write(f)
print("Yazıldı:", CIKTI, len(w.pages), "sayfa; yeni sayfalar:", {n: len(r.pages) for n, r in yeni.items()}, "on", len(on.pages), "ezber", len(ezb.pages))
for a, s, tur in isaret: print(("   " if tur else "") + a, s + 1)
