goto starting

:looping
    set fold=..\examples\
    set fil=tictactoe
    set fils=aggregation, boolean, comparison, countingGame, definition, nonstrict, quantification, set, tictactoe, tmp, tmpGame
    for %%i in (%fil%) do (
        set base=%fold%%%~ni
        set led=!base!.led
        set p=!base!.p
        set sl=!base!.sl

        set engine=led_engine.py !led!

        REM !engine!
        !engine! > !sl!
        sli -l !sl!
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
