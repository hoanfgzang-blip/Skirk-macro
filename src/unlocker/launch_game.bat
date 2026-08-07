@echo off
:: ============================================================
:: CUTTOOL UnlockerIsland - Launch Script
:: Chỉnh sửa GAME_PATH bên dưới thành đường dẫn đúng của bạn
:: ============================================================

set GAME_PATH=C:\Program Files\HoYoPlay\games\Genshin Impact game\GenshinImpact.exe

:: ============================================================
:: KHÔNG cần sửa gì bên dưới đây
:: ============================================================

set LAUNCHER=%~dp0Launcher_2.exe
set PLUGINS_DIR=%~dp0Plugins\UnlockerIsland

:: Kiểm tra game tồn tại
if not exist "%GAME_PATH%" (
    echo [ERROR] Khong tim thay game tai:
    echo         %GAME_PATH%
    echo.
    echo Hay chinh sua GAME_PATH trong file nay cho dung.
    pause
    exit /b 1
)

:: Kiểm tra launcher tồn tại
if not exist "%LAUNCHER%" (
    echo [ERROR] Khong tim thay Launcher_2.exe
    echo Chay build.bat truoc de build du an.
    pause
    exit /b 1
)

:: Tạo thư mục Plugins\UnlockerIsland nếu chưa có
if not exist "%PLUGINS_DIR%" (
    mkdir "%PLUGINS_DIR%"
)

:: Tạo config.ini cho plugin nếu chưa có
if not exist "%PLUGINS_DIR%\config.ini" (
    echo File=CUTTOOL.UnlockerIsland.dll> "%PLUGINS_DIR%\config.ini"
    echo [INFO] Da tao Plugins\UnlockerIsland\config.ini
)

:: Copy DLL vào thư mục plugin nếu chưa có
if not exist "%PLUGINS_DIR%\CUTTOOL.UnlockerIsland.dll" (
    copy /Y "%~dp0CUTTOOL.UnlockerIsland.dll" "%PLUGINS_DIR%\" >nul 2>&1
    if exist "%PLUGINS_DIR%\CUTTOOL.UnlockerIsland.dll" (
        echo [INFO] Da copy DLL vao thu muc plugin.
    ) else (
        echo [WARN] Khong the copy DLL. Hay copy thu cong:
        echo        CUTTOOL.UnlockerIsland.dll ^> Plugins\UnlockerIsland\
    )
)

echo [*] Dang khoi dong game voi DLL injection...
start "" "%LAUNCHER%" "%GAME_PATH%"
