goto starting

:body
    set fold=tests\
    set fil=%fold%test3
	for %%i in (%fil%.led) do (
		set p=%fold%%%~ni.p
        
        set parse=py ledparser.py %%i
        set transl=py translator.py %%i
        
        REM type %%i
        
        REM !parse!
        
        REM !parse! > !p!
        REM type !p!
        
        !transl!
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
