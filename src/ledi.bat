goto starting

:body
    set fold=tests\
    set fil=%fold%comparison
	for %%i in (%fil%.led) do (
		set b=%fold%%%~ni
        set p=!b!.p
        set sl=!b!.sl
        
        set parse=py ledparser.py %%i
        set transl=py translator.py %%i
        
        type %%i & echo:
        
        REM !parse! & echo:
        
        !transl! > !sl! & type !sl! 
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
