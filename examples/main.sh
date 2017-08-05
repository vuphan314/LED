input_base=$1 # dir `examples/`: tab-autocompletion appends `.`
# aggregation, boolean, comment, comparison, countingGame, definition, nonstrict, precedence, quantification, set, tictactoe, tmp

examples_path=../examples # relative to dir `src/`
base_path=$examples_path/$input_base
led_path=${base_path}led
tex_path=${base_path}tex
out_path=$examples_path
pdf_path=$out_path/${base_path}pdf

cd ../src/
clear
python3 led_engine.py $led_path -f
latexmk -pdf -synctex=1 -outdir=$out_path $tex_path
cd $examples_path
