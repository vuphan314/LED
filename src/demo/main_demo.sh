function set_paths {
  base_path=$1 # with trailing `.`

  led_path=${base_path}led
  sl_path=${base_path}sl
  tex_path=${base_path}tex
  pdf_path=${base_path}pdf
}

function process_led_file {
  led_path=$1

  ../led $led_path -f -v
  # atom $led_path $sl_path $tex_path
  # latexmk -pdf $tex_path # -synctex=1
  # evince $pdf_path &
}

function run_one {
  base_path=$1

  set_paths $base_path
  process_led_file $led_path
}

function run_all {
  base_paths=(aggregation. boolean. comment. comparison. countingGame. definition. nonstrict. precedence. quantification. set. tictactoe.)
  for base_path in ${base_paths[@]}; do
    set_paths $base_path
    process_led_file $led_path
  done
}

clear
run_one $1
# run_all
latexmk -c
