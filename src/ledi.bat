goto starting

:body
    set fold=tests\
    set fil=aggregation
    set fils=aggregation, boolean, comparison, quantification, set
	for %%i in (%fil%) do (
		set base=%fold%%%~ni
        set led=!base!.led
        set p=!base!.p
        set sl=!base!.sl
        
        set parse=py ledparser.py !led!
        set transl=py translator.py !led!
        
        py -i unparser.py        
        
        REM !parse!
        REM !parse! >> !led!
        REM !led!
        
        REM !transl!
        REM type !led!
        REM !transl! > !sl!
        REM !sl!
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
