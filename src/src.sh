#!/bin/bash

input_base=comment

examples_path=../examples
base_path=$examples_path/$input_base
led_path=$base_path.led
tex_path=$base_path.tex
out_path=$examples_path

# python3 led_parser.py $led_path
python3 led_engine.py -f $led_path
latexmk -pdf -outdir=$out_path $base_path
