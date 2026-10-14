#!/usr/bin/env bash
# İki geçişli derleme: 1) işaretli HTML -> PDF -> sayfa haritası  2) sayfa numaralı içindekiler -> nihai PDF
set -euo pipefail
cd "$(dirname "$0")"
export NODE_PATH="${NODE_PATH:-$(npm root -g)}"
OUT="${1:-Agirlik_Antrenmani_Kardiyo_ve_Beslenme.pdf}"
mkdir -p build
python3 build.py --out build/pass1.html
cp style.css build/ && rm -rf build/fonts && cp -r fonts build/fonts
node render.js build/pass1.html build/pass1.pdf
python3 pagemap.py build/pass1.pdf build/pages.json
python3 build.py --pages build/pages.json --out build/rapor.html
node render.js build/rapor.html "$OUT"
pdfinfo "$OUT" | grep -E "Pages|File size"
