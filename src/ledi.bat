goto starting

:body
    set comm=py parser.py %%i

    set fold=tests\
    set fil=%fold%test2
	for %%i in (%fil%.led) do (
		set o=%fold%%%~ni.p
        
        REM type %%i
        echo:
        
        %comm%
        
        REM %comm% > !o!
        REM !o!
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
