goto starting

:body
    set fold=tests\
    set fil=%fold%test3
	for %%i in (%fil%.led) do (
		set b=%fold%%%~ni
        set p=!b!.p
        set sl=!b!.sl
        
        set parse=py ledparser.py %%i
        set transl=py translator.py %%i
        
        REM type %%i
        
        REM !parse! & echo:
        
        REM !parse! > !p!
        REM type !p!
        
        !transl! > !sl! & type !sl!
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
