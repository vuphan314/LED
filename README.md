# LED: Language of Effective Definitions
LED system translates [literate language LED][linkLED] into:
- [functional language SequenceL][linkSL]
- formatting language TeX

## Demo
- Input: [LED file][tttLED]
- Output:
  - [SequenceL file][tttSL]
  - [TeX file][tttTEX]
    - [PDF file][tttPDF]
- [All examples][demo] (input: `*.led`; output: `*.sl`, `*.tex`, `*.pdf`)

## Binary download
See [latest release][releases]

## Usage
- Save these 3 files to some directory `d/`:
  - [LED binary for your OS][releases] (Ubuntu `led` or Windows `led.exe`)
  - [LED library for SequenceL][libSL] (`lib.sl`)
  - [LED library for TeX][libCLS] (`lib.cls`)
- Create a subdirectory `s/` in `d/`
- In `s/`: place some LED file `f.led`
  - or save this [demo LED file][aggrLED]
- Open a terminal in `d/` and pass the LED file's path to the binary:
  - Ubuntu:
    ```
    ./led s/f.led -f
    ```
  - Windows:
    ```
    led.exe  s/f.led -f
    ```
  - WARNING: flag `-f` overwrites `.sl` and `.tex` files in `s/`

## Git submodules
- `src/genparser/`: [generic parser][genparser] by Evgenii Balai
- `src/pyinstaller/`: [Python installer][pyinstaller] by David Cortesi

<!-- ####################################################################### -->

[linkLED]:https://docs.google.com/document/d/1xj5VUX6l9NYXQFuT-gVksSMwx5ovuQFkGymcgoZBagc/edit
[linkSL]:http://texasmulticore.com/wp-content/uploads/2016/07/SequenceL-Language-Reference.pdf

[tttLED]:https://github.com/vuphan314/LED/blob/master/src/demo/tictactoe.led
[tttSL]:https://github.com/vuphan314/LED/blob/master/src/demo/tictactoe.sl
[tttTEX]:https://github.com/vuphan314/LED/blob/master/src/demo/tictactoe.tex
[tttPDF]:https://github.com/vuphan314/LED/blob/master/src/demo/tictactoe.pdf
[demo]:https://github.com/vuphan314/led/tree/master/src/demo

[releases]:https://github.com/vuphan314/led/releases

[libSL]:https://raw.githubusercontent.com/vuphan314/led/master/src/lib.sl
[libCLS]:https://raw.githubusercontent.com/vuphan314/led/master/src/lib.cls
[aggrLED]:https://raw.githubusercontent.com/vuphan314/led/master/src/demo/aggregation.led

[genparser]:https://github.com/iensen/genparser
[pyinstaller]:https://www.pyinstaller.org
