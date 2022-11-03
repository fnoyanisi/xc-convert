@echo off

:: Skip the function definitions
goto Run

:: Function definitions
:DisplayHeader
setlocal
echo DO NOT CLOSE THIS WINDOW!
echo.
echo starting xc-convert...
exit /b 0

set PYTHONPATH=%cd%

:Run@echo off

:: Skip the function definitions
goto Run

:: Function definitions
:DisplayHeader
setlocal
echo DO NOT CLOSE THIS WINDOW!
echo.
echo starting xc-convert...
exit /b 0

:Run
:: Check a few possible locations for a
:: Python interpreter

if exist "C:\Program Files\Python\Python39" (
	call :DisplayHeader
	set PYTHONPATH=%cd%
	cd src
	"C:\Program Files\Python\Python39\python.exe" xcc.py
	exit
)

if exist "C:\Program Files\Anaconda3\condabin\activate.bat" (
	call :DisplayHeader
	set PYTHONPATH=%cd%
	call "C:\Program Files\Anaconda3\condabin\activate.bat" activate
	cd src
	python xcc.py
	exit
)

echo NO PYTHON INTERPRETER IS FOUND. EXISTING...
endlocal