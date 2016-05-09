# LED-TO-SL TRANSLATOR
- translating from [Language of Effective Definitions][LED] to [SequenceL][SL]
- under construction

## CURRENT VERSION
2016-05-09

### LANGUAGE LIMITATION
- values must be numerals
- arithemetic operations only
- functions must be nullary
- at most one function definition in each executable region (delimited by `/$` and `$/`)

### SYSTEM REQUIREMENTS
- Windows
- [SequenceL Interpreter][sli]
  - `sli` in Path variable

### USAGE
- download and extract [ledi.zip][lediZip] (LED Interpreter)
- open extracted folder
- source LED file must be `tests/test.led`
- double-click `ledi.bat`
- after [SequenceL Interpreter][sli] loads
  - query return values of functions
    - try entering `c3`
  - exit with `:quit`
- note: LED `0.(3..)` will be translated to SL `[1, 3]` (numerator & denominator)

[LED]: https://docs.google.com/document/d/1xj5VUX6l9NYXQFuT-gVksSMwx5ovuQFkGymcgoZBagc/edit
[SL]: http://www.texasmulticoretechnologies.com/content/SequenceL_Language_Reference_m.pdf
[sli]: http://www.texasmulticoretechnologies.com/content/SequenceL_Interpreter_Reference.pdf
[lediZip]: https://github.com/vuphan314/LEDtoSLtranslator/blob/master/ledi.zip
