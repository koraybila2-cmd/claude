# MSD-7 cikmis soru kitabini tek PDF olarak uretir: on + b1..b10 + ezber, yer imleriyle.
# kullanim: python3 -I birlestir.py
import io, os, subprocess
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
K = os.path.dirname(os.path.abspath(__file__)); Y = f"{K}/yapi"; os.makedirs(Y, exist_ok=True)
CIKTI = "/home/user/claude/ciktilar/blok2/MSD7_Ders_Kitabi_2026-27.pdf"
ALT = "Blok 2 · MSD-7 · Ders kitabı · 2026-27"
BOL = {1: "İshale Yaklaşım, Klinik Tipler ve Viral Etkenler", 2: "Dehidratasyon ve Sıvı Tedavisi", 3: "Su ve Besin Kaynaklı Salgınlar",
       4: "Bağırsak Mikrobiyotası ve Probiyotikler", 5: "Salmonella, Shigella, E. coli, Yersinia ve Laboratuvar Tanısı",
       6: "Toksin Kaynaklı İshaller ve Diğer Bakteriler", 7: "Sindirim Sistemi Protozoonları", 8: "Bağırsak Nematodları",
       9: "Sestodlar ve Trematodlar", 10: "Antihelmintik ve Antiprotozoal İlaçlar"}
subprocess.run(["python3", "-I", f"{K}/olustur.py"], check=True)
env = dict(os.environ, NODE_PATH=subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip())
def bas(ad):
    subprocess.run(["python3", "-I", f"{K}/uret.py", f"{Y}/{ad}.txt", f"{Y}/{ad}.html", "MSD-7 · 2026-27"], check=True)
    subprocess.run(["node", "/home/user/claude/kaynak/modul56/build/pdf.js", f"{ad}.html", f"{ad}.pdf", ALT], check=True, env=env, cwd=Y, stdout=subprocess.DEVNULL)
    return PdfReader(f"{Y}/{ad}.pdf")
on = bas("on"); bol = {n: bas(f"b{n}") for n in range(1, 11)}; ezb = bas("ezber")
w = PdfWriter(); isaret = []
def ekle(sayfalar):
    ilk = len(w.pages)
    for s in sayfalar: w.add_page(s)
    return ilk
isaret.append(("Giriş: kitabın yapısı ve konu dağılımı", ekle(on.pages)))
for n in range(1, 11):
    isaret.append((f"Bölüm {n}: {BOL[n]}", ekle(bol[n].pages)))
isaret.append(("Son gün ezber özeti", ekle(ezb.pages)))
pdfmetrics.registerFont(TTFont("Serif", "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"))
for i, pg in enumerate(w.pages):
    W, H = float(pg.mediabox.width), float(pg.mediabox.height)
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(W, H))
    c.setFillColorRGB(243 / 255, 242 / 255, 242 / 255); c.rect(42, 8, W - 84, 15, stroke=0, fill=1)
    c.setFillColorRGB(0x57 / 255, 0x53 / 255, 0x4e / 255); c.setFont("Serif", 6.6)
    c.drawString(64, 13, ALT); c.drawRightString(W - 44, 13, str(i + 1)); c.save()
    pg.merge_page(PdfReader(io.BytesIO(buf.getvalue())).pages[0])
for a, s in isaret: w.add_outline_item(a, s)
w.add_metadata({"/Title": "MSD-7 Ders Kitabı 2026-27"})
os.makedirs(os.path.dirname(CIKTI), exist_ok=True)
for p in w.pages: p.compress_content_streams()
w.compress_identical_objects()
with open(CIKTI, "wb") as f: w.write(f)
print("Yazıldı:", CIKTI, len(w.pages), "sayfa")
print("Bölüm sayfaları:", {n: len(bol[n].pages) for n in bol}, "on", len(on.pages), "ezber", len(ezb.pages))
