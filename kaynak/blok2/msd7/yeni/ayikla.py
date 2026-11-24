# MSD-7 cikmis soru md dosyasini yapilandirilmis JSON'a cevirir. kullanim: python3 -I ayikla.py girdi.md cikti.json
import re, sys, json
t = open(sys.argv[1], encoding="utf-8").read()
YIL = {1: "2025-26", 2: "2024-25", 3: "2023-24", 4: "2022-23", 5: "2021-22", 6: "2020-21", 7: "2019-20"}
def tex(s):
    s = re.sub(r"\$(.+?)\$", lambda m: m.group(1), s); s = re.sub(r"\\text\{(.*?)\}", r"\1", s)
    s = s.replace("\\times", "×").replace("\\%", "%").replace("\\ge", "≥").replace("\\le", "≤").replace("\\mu", "µ").replace("^{", "").replace("{", "").replace("}", "").replace("\\", "")
    return s.strip()
out = []
for bi, blok in enumerate(re.split(r"\n## \d+\. ", t)[1:], 1):
    for m in re.finditer(r"\n\*\*(\d+)\.\*\*\s*(.*?)(?=\n\*\*\d+\.\*\*|\Z)", "\n" + blok, re.S):
        n, govde = int(m.group(1)), m.group(2)
        cev = re.search(r"(?:^-\s*)?\*\*(?:Doğru Şık|Cevap|Doğru Cevap)[^*]*\*\*\s*([^\n]*)", govde, re.M)
        govde2 = govde[:cev.start()] if cev else govde
        sik = [(h, tex(x)) for h, x in re.findall(r"^\s*-\s*\*\*([A-E])\)\*\*\s*(.*)$", govde2, re.M)]
        ilk = re.search(r"^\s*-\s*\*\*[A-E]\)\*\*", govde2, re.M)
        kok = govde2[:ilk.start()] if ilk else govde2
        kok = [tex(l.strip().lstrip("*-").strip()) for l in kok.split("\n") if l.strip() and not l.strip().startswith("---") and not l.strip().startswith(">")]
        out.append(dict(sinav=bi, yil=YIL[bi], no=n, kok=kok, sik=sik, cevap=(re.match(r"^([A-E])\b", cev.group(1).strip()).group(1) if cev and re.match(r"^[A-E](\s|$|\)|\.|,)", cev.group(1).strip()) else ""), cevap_metin=(tex(cev.group(1).strip()) if cev else ""), ham=govde.strip()[:3000]))
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
import collections
print(len(out), collections.Counter(o["yil"] for o in out))
print("cevapsiz:", [(o["yil"], o["no"]) for o in out if not re.fullmatch(r"[A-E]", o["cevap"])])
print("sik sayisi 5 degil:", [(o["yil"], o["no"], len(o["sik"])) for o in out if len(o["sik"]) != 5])
