#!/usr/bin/env python3
"""1. geçiş PDF'indeki ZQ<id>QZ işaretlerinden {id: sayfa} haritası çıkarır."""
import json
import re
import subprocess
import sys

pdf, out = sys.argv[1], sys.argv[2]
text = subprocess.run(["pdftotext", "-enc", "UTF-8", pdf, "-"], capture_output=True, text=True, check=True).stdout
pages = {}
for i, page in enumerate(text.split("\f"), start=1):
    compact = re.sub(r"\s+", "", page)
    for m in re.finditer(r"ZQ([a-z0-9]+)QZ", compact):
        pages.setdefault(m.group(1), i)
json.dump(pages, open(out, "w"), ensure_ascii=False, indent=0)
print(f"{len(pages)} işaret bulundu")
