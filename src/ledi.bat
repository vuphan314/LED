goto starting

:body
    set fold=tests\
    set fil=%fold%set
	for %%i in (%fil%.led) do (
		set base=%fold%%%~ni
        set p=!base!.p
        set sl=!base!.sl
        set txt=!base!.txt
        
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
