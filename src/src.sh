#!/bin/bash

python3 ./led_engine.py ../examples/tmp.led > ../examples/tmp.tex
cat ../examples/tmp.tex
latexmk -pdf -outdir=../examples/out/ ../examples/tmp.tex
