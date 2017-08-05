input_base=tmp # precedence, tictactoe, tmp

examples_path=../examples
base_path=$examples_path/$input_base
led_path=$base_path.led
tex_path=$base_path.tex
out_path=$examples_path
pdf_path=$out_path/$base_path.pdf

clear
# python3 led_parser.py $led_path
python3 led_engine.py $led_path -f
# latexmk -pdf -outdir=$out_path $tex_path

# less $tex_path
# evince $pdf_path &
