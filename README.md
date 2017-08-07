<h6>top</h6>

# LED: LANGUAGE OF EFFECTIVE DEFINITIONS
LED system translates [literate language LED][linkLED] into:
- [functional language SequenceL][linkSL]
- formatting language TeX

## DEMO
- input: [LED file][tttLED]
- output:
  - [SequenceL file][tttSL]
  - [TeX file][tttTEX]
    - [PDF file][tttPDF]

## USAGE
- download these 3 files to some directory `d/`:
  - [binary][bin]
  - [SequenceL library `lib.sl`][libSL]
  - [TeX library `lib.cls`][libCLS]
- create a subdirectory `s/` in `d/`
- in `s/`, place some LED file `f.led`
  - or save this [demo LED file][aggrLED]
- open a terminal in `d/` and pass the LED file's path to the binary:
  ```
  ./led s/f.led -f
  ```
  - WARNING: flag `-f` overwrites `.sl` and `.tex` files in `s/`

## GIT SUBMODULES
The [generic parser][genparser] (`src/genparser/`)
is developed by Evgenii Balai.

<!----------------------------------------------------------------------------->

[linkLED]:https://docs.google.com/document/d/1xj5VUX6l9NYXQFuT-gVksSMwx5ovuQFkGymcgoZBagc/edit
[linkSL]:http://texasmulticore.com/wp-content/uploads/2016/07/SequenceL-Language-Reference.pdf

[tttLED]:https://github.com/vuphan314/LED/blob/master/src/demo/tictactoe.led
[tttSL]:https://github.com/vuphan314/LED/blob/master/src/demo/tictactoe.sl
[tttTEX]:https://github.com/vuphan314/LED/blob/master/src/demo/tictactoe.tex
[tttPDF]:https://github.com/vuphan314/LED/blob/master/src/demo/tictactoe.pdf

[bin]:https://github.com/vuphan314/led/tree/master/bin
[libSL]:https://raw.githubusercontent.com/vuphan314/led/master/src/lib.sl
[libCLS]:https://raw.githubusercontent.com/vuphan314/led/master/src/lib.cls
[aggrLED]:https://raw.githubusercontent.com/vuphan314/led/master/src/demo/aggregation.led

[genparser]:https://github.com/iensen/genparser
