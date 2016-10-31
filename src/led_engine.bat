goto starting

:looping
    set fold=examples\
    set fil=tictactoe2
    set fils=aggregation, boolean, comparison, counting, definition, game, nonstrict, quantification, set, tictactoe2, tmp
    for %%i in (%fil%) do (
        set base=%fold%%%~ni
        set led=!base!.led
        set p=!base!.p
        set sl=!base!.sl

        set transl=led_translator.py !led!
        set parse=led_parser.py !led!

        !transl!
        REM !parse! > !p!
    )
    goto ending

:starting
    cls
    @echo off
    setlocal enabledelayedexpansion
    echo starting...
    echo:
    goto looping

:ending
    echo:
    echo done
