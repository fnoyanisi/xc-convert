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

:Run
:: Check a few possible locations for a
:: Python interpreter

if exist "C:\Program Files\Python\Python39" (
	call :DisplayHeader
	"C:\Program Files\Python\Python39\python.exe" src\xc-convert.py
	exit
)

if exist "C:\Program Files\Anaconda3\condabin\activate.bat" (
	call :DisplayHeader
	call "C:\Program Files\Anaconda3\condabin\activate.bat" activate
	python src\xc-convert.py
	exit
)

echo NO PYTHON INTERPRETER IS FOUND. EXISTING...
endlocal