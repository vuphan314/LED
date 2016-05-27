goto starting

:body
    set fold=tests\
    set fil=%fold%test3
    set genparserpy=genparser\src\astgen\main.py
	for %%i in (%fil%.led) do (
        %genparserpy% lexicon.txt grammar.txt %%i
        REM parser.py %%i
		REM translator.py %%i
        
		REM set o=%fold%%%~ni.sl
        REM translator.py %%i > !o!
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
