input_base=$1 # dir `src/examples/`: tab-autocompletion appends `.`
# aggregation, boolean, comment, comparison, countingGame, definition, nonstrict, precedence, quantification, set, tictactoe

examples_path=examples # relative to dir `src/`
base_path=$examples_path/$input_base
led_path=${base_path}led
sl_path=${base_path}sl
tex_path=${base_path}tex
out_path=$examples_path
pdf_path=$out_path/${base_path}pdf

src_path=.. # relative to dir `examples/`
cd $src_path
clear
python3 led_engine.py $led_path -f $2 # -v
# atom $led_path $sl_path $tex_path
# latexmk -pdf -outdir=$out_path $tex_path # -synctex=1
# evince $pdf_path &
cd $examples_path
