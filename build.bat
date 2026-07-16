@echo off
echo ===================================
echo   Building Skirk Macro App
echo ===================================

echo.
echo [1/2] Building Python backend (Cryss.exe)...

REM Create build folder if it doesn't exist
if not exist "build" (
    mkdir "build"
)

cd build
call pyinstaller --onefile --name "Cryss" --workpath "temp" --distpath "dist" "..\src\macro\main.py"
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to build Python backend!
    pause
    exit /b %errorlevel%
)
cd ..

echo.
echo [2/2] Building Electron UI...
cd src\UI
if exist "..\..\build\app" rmdir /s /q "..\..\build\app"
call pnpm package:win
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to build Electron UI!
    pause
    exit /b %errorlevel%
)
cd ..\..

echo.
echo ===================================
echo   BUILD SUCCESSFUL!
echo   App is located in: build\app\win-unpacked\Cryss.exe
echo ===================================
pause
