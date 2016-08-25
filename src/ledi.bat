goto starting

:body
    set fold=tests\
    set fil=ifWhere
    set fils=aggregation, boolean, comparison, quantification, set
	for %%i in (%fil%) do (
		set base=%fold%%%~ni
        set led=!base!.led
        set sl=!base!.sl
        set parse=py ledparser.py !led!
        set transl=py translator.py !led!

        REM py -i unparser.py

        echo !base!
        REM type !led!

        REM !parse!
        REM !parse! >> !led!
        REM !led!

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
