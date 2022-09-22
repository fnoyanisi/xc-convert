@echo off
echo DO NOT CLOSE THIS WINDOW!
echo.
echo starting xc-convert...
call "C:\Program Files\Anaconda3\condabin\activate.bat" activate
cd src
python xc-convert.py