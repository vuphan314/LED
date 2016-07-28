goto starting

:body
    set fold=tests\
    set fil=quantification
    set fils=boolean, comparison, set
	for %%i in (%fil%) do (
		set base=%fold%%%~ni
        set led=!base!.led
        set p=!base!.p
        set sl=!base!.sl
        
        set parse=py ledparser.py !led!
        set transl=py translator.py !led!
        
        py -i unparser.py
        
        REM !led!
        
        REM !parse! & echo:
        
        REM !transl! > !sl!
        REM type !sl!
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
