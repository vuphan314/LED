goto starting

:body
    set fold=tests\
    set fil=%fold%quantification
	for %%i in (%fil%.led) do (
		set base=%fold%%%~ni
        set p=!base!.p
        set sl=!base!.sl
        set txt=!base!.txt
        
        set parse=py ledparser.py %%i
        set transl=py translator.py %%i
        
        REM type %%i & echo:
        
        !parse! & echo:
        
        REM !transl! > !sl! & type !sl! 
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
