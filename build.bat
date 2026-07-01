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
    echo Trying to install it automatically via winget...
    echo.
    where winget >nul 2>nul
    if %errorlevel% neq 0 (
        echo.
        echo Winget isn't available on this machine either.
        echo Please install Python yourself from:
        echo   https://www.python.org/downloads/
        echo IMPORTANT: check "Add Python to PATH" during setup.
        echo Then re-run this script.
        pause
        exit /b 1
    )

    winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
    echo.
    echo Python was just installed. Close this window and run build.bat
    echo again so the terminal picks up the new PATH.
    pause
    exit /b 0
)

echo Found Python:
!PYCMD! --version

echo.
echo Installing/updating build tools (pyinstaller, pillow)...
!PYCMD! -m pip install --upgrade pip
!PYCMD! -m pip install --upgrade pyinstaller pillow

echo.
echo Building Lairkeeper.exe...
!PYCMD! -m PyInstaller --onefile --windowed --name "Lairkeeper" --specpath "spec_lairkeeper" code.py
if %errorlevel% neq 0 (
    echo ERROR: Lairkeeper build failed.
    pause
    exit /b 1
)
echo Lairkeeper.exe built successfully.

echo.
echo Building manage_data.exe...
!PYCMD! -m PyInstaller --onefile --windowed --name "manage_data" --specpath "spec_manage" manage_data.py
if %errorlevel% neq 0 (
    echo ERROR: manage_data build failed.
    pause
    exit /b 1
)
echo manage_data.exe built successfully.

echo.
echo ============================================
echo  Done!
echo  Both files are in the dist\ folder:
echo    dist\Lairkeeper.exe
echo    dist\manage_data.exe
echo.
echo  Before sharing, copy your "assets" folder
echo  into "dist", next to the .exe files.
echo ============================================
pause
