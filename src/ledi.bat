goto starting

:body
    set genparserpy=genparser\src\astgen\main.py
    set genparse=%genparserpy% lexicon.txt grammar.txt %%i
    set comm=%genparse%
    
    set fold=tests\
    set fil=%fold%test3
	for %%i in (%fil%.led) do (
        type %%i
        echo:
        
        py parser.py %%i
        REM %comm%
        
		REM set o=%fold%%%~ni.p
        REM %comm% > !o!
        REM !o!
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
