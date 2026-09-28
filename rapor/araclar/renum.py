#!/usr/bin/env python3
"""Bölüm dosyasında kaynak listesini normalleştirir.

- '(—)' yer tutucu kaynakları siler,
- '(a) ... — (b) ...' biçimindeki birleşik kaynakları ayrı girdilere böler,
- metindeki [3], [5, 7], [20a], [20b, 21] gibi atıfları yeni numaralara çevirir.
"""
import re
import sys

p = sys.argv[1]
s = open(p, encoding="utf-8").read()
body, refs = s.split("## Kaynaklar", 1)

entries = []
for ln in refs.strip("\n").split("\n"):
    m = re.match(r"^(\d+)\. (.*)$", ln)
    if m:
        entries.append((m.group(1), m.group(2)))

mapping, kept = {}, []
for num, txt in entries:
    if txt.strip() in ("(—)", "(-)"):
        continue
    markers = list(re.finditer(r"\(([a-z])\)\s", txt))
    if markers and markers[0].group(1) == "a":
        for i, mk in enumerate(markers):
            end = markers[i + 1].start() if i + 1 < len(markers) else len(txt)
            sub = txt[mk.end():end].strip().rstrip("—").strip()
            kept.append(sub)
            mapping[num + mk.group(1)] = str(len(kept))
        continue
    kept.append(txt)
    mapping[num] = str(len(kept))


def rep(mo):
    toks = [t.strip() for t in mo.group(1).split(",")]
    if not all(re.fullmatch(r"\d{1,3}[a-z]?", t) for t in toks):
        return mo.group(0)
    return "[" + ", ".join(mapping.get(t, "?" + t) for t in toks) + "]"


body = re.sub(r"\[(\d{1,3}[a-z]?(?:\s*,\s*\d{1,3}[a-z]?)*)\]", rep, body)
out = body + "## Kaynaklar\n\n" + "\n".join(f"{i}. {t}" for i, t in enumerate(kept, 1)) + "\n"
open(p, "w", encoding="utf-8").write(out)

missing = re.findall(r"\[\?[^\]]*\]|\?\d+[a-z]?", body)
used = set()
for g in re.findall(r"\[(\d{1,3}(?:\s*,\s*\d{1,3})*)\]", body):
    used.update(int(x) for x in re.split(r"\s*,\s*", g))
print(f"{len(kept)} kaynak; atıf yapılmayan: {sorted(set(range(1, len(kept) + 1)) - used)}; eksik: {missing}")
