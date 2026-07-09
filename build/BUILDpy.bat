@echo off
setlocal

REM Chuyển về thư mục gốc của project
cd /d "%~dp0.."

REM Build file chính
py -m PyInstaller ^
    --onefile ^
    --clean ^
    --noconfirm ^
    --distpath build\dist ^
    --workpath build\temp ^
    --specpath build ^
    src\macro\main.py

echo.
echo Build completed!
pause