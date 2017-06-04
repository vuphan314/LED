<h6>top</h6>

# LED: LANGUAGE OF EFFECTIVE DEFINITIONS
LED system translates [literate language LED][linkLED] into:
- [functional language SequenceL][linkSL]
- formatting language TeX

## EXAMPLES
- input: [LED file][tttLED]
- output:
  - [SequenceL file][tttSL]
  - [TeX file][tttTEX]
    - [PDF file][tttPDF]

## GIT SUBMODULES
The [generic parser][genparser] (`src/genparser/`)
is developed by Evgenii Balai.

<!--------------------------------------------------------->

[tttLED]:https://github.com/vuphan314/LED/blob/master/examples/tictactoe.led
[tttSL]:https://github.com/vuphan314/LED/blob/master/examples/tictactoe.sl
[tttTEX]:https://github.com/vuphan314/LED/blob/master/examples/tictactoe.tex
[tttPDF]:https://github.com/vuphan314/LED/blob/master/examples/tictactoe.pdf

[linkLED]:https://docs.google.com/document/d/1xj5VUX6l9NYXQFuT-gVksSMwx5ovuQFkGymcgoZBagc/edit
[linkSL]:http://texasmulticore.com/wp-content/uploads/2016/07/SequenceL-Language-Reference.pdf

[genparser]:https://github.com/iensen/genparser
