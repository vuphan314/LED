function set_paths {
  base_name=$1 # with trailing `.`

  demo_path=demo/
  base_path=$demo_path/$base_name
  led_path=${base_path}led
  sl_path=${base_path}sl
  tex_path=${base_path}tex
  pdf_path=${base_path}pdf
}

function process_led_file {
  led_path=$1

  echo "Processing $led_path."
  src_path=..
  cd $src_path
  ./led $led_path -f # -v
  # atom $led_path $sl_path $tex_path
  # cd $demo_path && latexmk -pdf && cd $src_path
  # evince $pdf_path &
  cd $demo_path
}

function run_one {
  base_name=$1

  set_paths $base_name
  process_led_file $led_path
}

function run_all {
  base_paths=(aggregation. boolean. comment. comparison. countingGame. definition. nonstrict. precedence. quantification. set. tictactoe.)
  for base_path in ${base_paths[@]}; do
    set_paths $base_path
    process_led_file $led_path
    echo -e "\n"
  done
}

clear
run_one $1
# run_all
latexmk -c
