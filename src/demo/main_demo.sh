input_base=$1 # dir `demo/`: tab-autocompletion appends `.`
# aggregation, boolean, comment, comparison, countingGame, definition, nonstrict, precedence, quantification, set, tictactoe

demo_path=.
base_path=$demo_path/$input_base
led_path=${base_path}led
sl_path=${base_path}sl
tex_path=${base_path}tex
out_path=$demo_path
pdf_path=$out_path/${base_path}pdf

clear
../led $led_path -f $2 # -v
# atom $led_path $sl_path $tex_path
# latexmk -pdf -outdir=$out_path $tex_path # -synctex=1
# evince $pdf_path &
