@echo off
setlocal

echo =============================================
echo   DEBUG: Skirk Macro - Kiem tra loi
echo =============================================
echo.

REM === Thư mục log ===
set LOGDIR=%USERPROFILE%\AppData\Roaming\Cryss
set LOGFILE=%LOGDIR%\electron-debug.log
set BELOGFILE=%~dp0debug-backend.log

echo [1] Thu muc log Electron: %LOGFILE%
echo [2] Log backend (chay truc tiep): %BELOGFILE%
echo.

REM === Xem log Electron cũ (nếu có) ===
if exist "%LOGFILE%" (
    echo --- NOI DUNG LOG ELECTRON TRUOC DO ---
    type "%LOGFILE%"
    echo.
    echo --- HET LOG ---
    echo.
) else (
    echo [INFO] Chua co file log Electron tai: %LOGFILE%
    echo       ^(App chua chay lan nao sau khi cap nhat debug^)
    echo.
)

REM === Kiểm tra file backend ===
set BACKEND=%~dp0build\dist\Cryss.exe
echo [3] Kiem tra backend: %BACKEND%
if exist "%BACKEND%" (
    echo     -> TIM THAY: %BACKEND%
) else (
    echo     -> KHONG TIM THAY! Hay chay build.bat truoc.
    echo.
)

REM === Thử chạy backend trực tiếp và bắt lỗi ===
echo.
echo [4] Thu chay backend truc tiep (30 giay)...
echo     Neu co loi UAC, se co popup yeu cau Admin.
echo     Log se ghi vao: %BELOGFILE%
echo.

set CRYSS_DEBUG_LOG=1
"%BACKEND%" > "%BELOGFILE%" 2>&1 &
set BACKEND_PID=%!

timeout /t 5 /nobreak >nul

echo [5] Kiem tra port 5000...
netstat -an | findstr ":5000"
if errorlevel 1 (
    echo     -> KHONG co gi lang nghe tren port 5000!
    echo        Backend co the da crash ngay.
) else (
    echo     -> Port 5000 DANG LAM VIEC ^(tot^)
)

echo.
echo [6] Kiem tra Windows Defender / Firewall...
netsh advfirewall firewall show rule name=all | findstr /i "Cryss"
if errorlevel 1 (
    echo     -> Khong tim thay rule firewall nao cho Cryss
    echo        Co the bi chan boi Windows Firewall
) else (
    echo     -> Tim thay rule firewall
)

echo.
echo [7] Kiem tra log backend...
timeout /t 3 /nobreak >nul
if exist "%BELOGFILE%" (
    echo --- NOI DUNG LOG BACKEND ---
    type "%BELOGFILE%"
    echo --- HET LOG ---
) else (
    echo [INFO] Khong co log backend
)

echo.
echo =============================================
echo   XONG - Hay chup man hinh nay va gui cho dev
echo =============================================
echo.
pause
