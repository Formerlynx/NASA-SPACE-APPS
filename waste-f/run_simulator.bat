@echo off
echo Starting PROMETHEUS Waste-to-Fuel Simulator...
echo.

REM Try to run with MSYS64 Python first (which we know works)
if exist C:\msys64\ucrt64\bin\python3.exe (
    C:\msys64\ucrt64\bin\python3.exe simple_demo.py
    goto :end
)

REM Try with python3 command
python3 simple_demo.py 2>nul
if %ERRORLEVEL% EQU 0 goto :end

REM Try with python command
python simple_demo.py 2>nul
if %ERRORLEVEL% EQU 0 goto :end

REM Try with py command
py simple_demo.py 2>nul
if %ERRORLEVEL% EQU 0 goto :end

REM If all attempts fail
echo ERROR: Could not find a working Python installation.
echo Please install Python 3.x and try again.
echo.

:end
pause