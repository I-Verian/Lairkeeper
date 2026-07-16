@echo off
setlocal enabledelayedexpansion

echo ============================================
echo  Lairkeeper Builder
echo ============================================
echo.

set PYCMD=

where python >nul 2>nul
if %errorlevel%==0 (
    set PYCMD=python
) else (
    where py >nul 2>nul
    if %errorlevel%==0 (
        set PYCMD=py
    )
)

if "!PYCMD!"=="" (
    echo Python wasn't found on this computer.
    where winget >nul 2>nul
    if %errorlevel% neq 0 (
        echo Please install Python from https://www.python.org/downloads/
        echo IMPORTANT: check "Add Python to PATH" during setup.
        pause
        exit /b 1
    )
    winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
    echo Python installed. Re-run build.bat.
    pause
    exit /b 0
)

echo Found Python:
!PYCMD! --version

echo.
echo Installing/updating build tools...
!PYCMD! -m pip install --upgrade pip
!PYCMD! -m pip install --upgrade pyinstaller pillow

echo.
echo Building Lairkeeper...
!PYCMD! -m PyInstaller --onedir --windowed --name "Lairkeeper" --specpath "spec_lairkeeper" --collect-all tkinter code.py
if %errorlevel% neq 0 (
    echo ERROR: Build failed.
    pause
    exit /b 1
)

echo.
echo Copying assets...
if exist assets (
    xcopy /E /I /Y assets dist\Lairkeeper\assets >nul
    echo Assets copied.
) else (
    echo WARNING: No assets folder found.
)

if exist README.txt copy /Y README.txt dist\Lairkeeper\README.txt >nul

echo.
echo ============================================
echo  Done! Files are in dist\Lairkeeper\
echo.
echo  To release: select everything INSIDE
echo  dist\Lairkeeper\ and zip those files
echo  (not the Lairkeeper folder itself).
echo ============================================
pause
