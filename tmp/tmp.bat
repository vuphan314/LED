goto labelStarting

:labelBody
	goto labelTranslator

:labelSl
	set expr=(myInt: 4)
	sli -l %dirTmp%tmp.sl -x -c "%expr%"
	goto labelDone

:labelTranslator
	set dirTmpTest=%dirTmp%tests\
	set fold=%dirTmpTest%
	for %%i in (%fold%*.led) do (
		set o=%fold%%%~ni.p
		main %%i > !o!
		type !o!
	)
	goto labelDone
	
:labelStarting
	@echo off
	cls
	setlocal enabledelayedexpansion
	echo Starting...
	echo:
	set dirTmp=..\tmp\
	goto labelBody
	
:labelDone
	echo:
	echo Done
