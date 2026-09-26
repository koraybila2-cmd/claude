#!/usr/bin/env python3
"""Bölüm dosyasında '(—)' yer tutucu kaynakları siler ve atıf numaralarını yeniden sıralar."""
import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
body, refs = s.split("## Kaynaklar", 1)
entries = []
for ln in refs.strip("\n").split("\n"):
    m = re.match(r"^(\d+)\. (.*)$", ln)
    if m:
        entries.append((m.group(1), m.group(2)))
mapping, kept = {}, []
for old, txt in entries:
    if txt.strip() in ("(—)", "(-)"):
        continue
    kept.append(txt)
    mapping[old] = str(len(kept))
def rep(mo):
    toks = [t.strip() for t in re.split(r",", mo.group(1))]
    if not all(t.isdigit() for t in toks):
        return mo.group(0)
    return "[" + ", ".join(mapping.get(t, "?" + t) for t in toks) + "]"
body = re.sub(r"\[(\d{1,3}(?:\s*,\s*\d{1,3})*)\]", rep, body)
out = body + "## Kaynaklar\n\n" + "\n".join(f"{i}. {t}" for i, t in enumerate(kept, 1)) + "\n"
open(p, "w", encoding="utf-8").write(out)
missing = re.findall(r"\[\?\d+", body)
used = set(int(x) for g in re.findall(r"\[(\d{1,3}(?:\s*,\s*\d{1,3})*)\]", body) for x in re.split(r"\s*,\s*", g))
print(f"{len(kept)} kaynak; atıf yapılmayan: {sorted(set(range(1, len(kept)+1)) - used)}; eksik: {missing}")
