goto starting

:body
    set fold=tests\
    set fil=%fold%test3
    set genparserpy=genparser\src\astgen\main.py
    set genparse=%genparserpy% lexicon.txt grammar.txt %%i
	for %%i in (%fil%.led) do (
		set o=%fold%%%~ni.p
        
        %genparse% > !o!
        !o!
        
        REM parser.py %%i
		REM translator.py %%i
        
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
