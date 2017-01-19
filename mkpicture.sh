#!/bin/bash
mkdir -p latex
python mkvalues.py mkvalues_params.py < $1 > latex/values.txt
python mktable.py < latex/values.txt > latex/table.tex
cd latex
pdflatex table.tex
pdftoppm -rx 200 -ry 200 table.pdf > table.ppm
convert table.ppm -trim ../out.png
cd ..
