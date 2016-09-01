goto starting

:body
    set fold=tests\
    set fil=tictactoe
    set fils=aggregation, boolean, comparison, definition, quantification, set, tictactoe
    for %%i in (%fil%) do (
        set base=%fold%%%~ni
        set led=!base!.led
        set p=!base!.p
        set sl=!base!.sl
        set parse=py ledparser.py !led!
        set transl=py translator.py !led!

        REM py -i translator.py
        REM py -i unparser.py

        echo !base!

        REM !parse!
        REM !parse! >> !led!
        REM !led!
        REM !parse! > !p!
        REM !p!

        REM !transl!
        !transl! > !sl!
        !sl!
        sli -l !sl!
    )
    goto done

:starting
    @echo off
    cls
    setlocal enabledelayedexpansion
    echo starting...
    echo:
    goto body

:done
    echo:
    echo done
