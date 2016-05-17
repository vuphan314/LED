goto starting

:body
    set fold=tests\
    set fil=%fold%test
	for %%i in (%fil%.led) do (
		set o=%fold%%%~ni.sl
        REM parser %%i
		translator %%i
        REM translator %%i > !o!
        REM !o!
        REM sli -l !o!
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
