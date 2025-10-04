@echo off
echo Starting PROMETHEUS Waste-to-Fuel Simulator (GUI Version)...
echo.

:: Try MSYS64 Python first (known to work)
if exist C:\msys64\ucrt64\bin\python3.exe (
    echo Using MSYS64 Python...
    C:\msys64\ucrt64\bin\python3.exe gui_demo.py
    goto end
)

:: Try other Python commands
echo Trying system Python...

where python3 >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    python3 gui_demo.py
    goto end
)

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    python gui_demo.py
    goto end
)

where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    py gui_demo.py
    goto end
)

:: If we get here, no Python was found
echo ERROR: Could not find Python. Please install Python and try again.
echo.
echo Press any key to exit...
pause >nul

:end