goto starting

:body
    set fold=tests\
    set fil=game
    set fils=aggregation, boolean, comparison, definition, quantification, set, tictactoe
	for %%i in (%fil%) do (
		set base=%fold%%%~ni
        set led=!base!.led
        set p=!base!.p
        set sl=!base!.sl
        set parse=py ledparser.py !led!
        set transl=py translator.py !led!

        REM py -i unparser.py

        echo !base!
        REM type !led!

        REM !parse!
        REM !parse! > !p!
        REM type !p!

        REM !transl!
        !transl! > !sl!
        type !sl!
        REM sli -l !sl!
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
