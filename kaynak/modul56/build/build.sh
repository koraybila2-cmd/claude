#!/bin/bash
# kullanim: build.sh <kitapdir> "<Baslik>" "<footer basligi>"
set -e
B=$(dirname "$0"); D="$1"
python3 -I "$B/derle.py" "$D" "$2"
NODE_PATH=$(npm root -g) node "$B/pdf.js" "$D/$(basename $D).html" "$D/$(basename $D).pdf" "$3"
pdfinfo "$D/$(basename $D).pdf" | grep Pages
