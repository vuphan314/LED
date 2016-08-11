goto starting

:body
    set fold=tests\
    set fil=test
    set fils=aggregation, boolean, comparison, quantification, set
	for %%i in (%fil%) do (
		set base=%fold%%%~ni
        set led=!base!.led
        set p=!base!.p
        set sl=!base!.sl
        
        set parse=py ledparser.py !led!
        set transl=py translator.py !led!
        
        REM py -i unparser.py        
        
        REM !parse!
        REM !parse! >> !led!
        REM !led!
        
        REM !transl!
        type !led!
        !transl! > !sl!
        !sl!
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
