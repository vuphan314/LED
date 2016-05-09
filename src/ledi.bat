goto starting

:body
    set fold=tests\
    set fil=%fold%testLed
	for %%i in (%fil%.led) do (
		set o=%fold%%%~ni.sl
        REM main %%i
		REM translator %%i 
        translator %%i > !o!
        type !o!
        sli -l !o!
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
