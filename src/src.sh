#!/bin/bash

input_base=tmp

examples_path=../examples
base_path=$examples_path/$input_base
led_path=$base_path.led
tex_path=$base_path.tex
out_path=$examples_path/out

python3 led_engine.py -f $led_path
# atom $tex_path
latexmk -pdf -outdir=$out_path $base_path
