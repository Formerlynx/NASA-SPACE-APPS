@echo off
echo Creating standalone executable for PROMETHEUS Waste-to-Fuel Simulator...
echo.

REM Try to find a working Python installation
echo Checking for Python installations...

REM Try with MSYS64 Python first
if exist C:\msys64\ucrt64\bin\python3.exe (
    echo Found MSYS64 Python installation.
    echo Installing PyInstaller...
    C:\msys64\ucrt64\bin\python3.exe -m pip install pyinstaller
    
    echo Creating executable...
    C:\msys64\ucrt64\bin\python3.exe -m PyInstaller --onefile simple_demo.py --name PROMETHEUS_Simulator
    
    echo Moving executable to main folder...
    move dist\PROMETHEUS_Simulator.exe .\
    
    echo Cleaning up temporary files...
    rmdir /s /q build
    rmdir /s /q dist
    del PROMETHEUS_Simulator.spec
    
    echo Done! You can now run PROMETHEUS_Simulator.exe
    goto :end
)

REM Try with python3 command
python3 -m pip install pyinstaller 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Found Python3 installation.
    echo Creating executable...
    python3 -m PyInstaller --onefile simple_demo.py --name PROMETHEUS_Simulator
    
    echo Moving executable to main folder...
    move dist\PROMETHEUS_Simulator.exe .\
    
    echo Cleaning up temporary files...
    rmdir /s /q build
    rmdir /s /q dist
    del PROMETHEUS_Simulator.spec
    
    echo Done! You can now run PROMETHEUS_Simulator.exe
    goto :end
)

REM Try with python command
python -m pip install pyinstaller 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Found Python installation.
    echo Creating executable...
    python -m PyInstaller --onefile simple_demo.py --name PROMETHEUS_Simulator
    
    echo Moving executable to main folder...
    move dist\PROMETHEUS_Simulator.exe .\
    
    echo Cleaning up temporary files...
    rmdir /s /q build
    rmdir /s /q dist
    del PROMETHEUS_Simulator.spec
    
    echo Done! You can now run PROMETHEUS_Simulator.exe
    goto :end
)

REM If all attempts fail
echo ERROR: Could not find a working Python installation with pip.
echo Please install Python 3.x with pip and try again.
echo.
echo Alternatively, you can run the simulator using the run_simulator.bat file
echo if you have a working Python installation.

:end
pause