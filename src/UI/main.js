const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn, execSync } = require('child_process');
const http = require('http');

let pyProc = null;

function startPython() {
    const isPackaged = app.isPackaged;
    let pyPath;
    let args = [];

    if (!isPackaged) {
        // Dev: chạy qua thông dịch viên python
        pyPath = process.platform === 'win32' ? 'python' : 'python3';
        args = [path.join(__dirname, '..', 'macro', 'main.py')];
    } else {
        // Packaged: chạy main.exe được đóng gói trong resources
        pyPath = path.join(process.resourcesPath, 'main.exe');
    }

    pyProc = spawn(pyPath, args, {
        stdio: 'ignore',
        windowsHide: true
    });

    pyProc.on('error', (err) => {
        console.error('Không thể khởi chạy Python backend:', err);
    });
}

function stopPython() {
    // 1. Gửi POST /shutdown để Python tự thoát (xử lý cả trường hợp admin re-launch)
    return new Promise((resolve) => {
        const req = http.request({
            hostname: 'localhost',
            port: 5000,
            path: '/shutdown',
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            timeout: 2000
        }, (res) => {
            resolve();
        });

        req.on('error', () => resolve());   // Server đã tắt hoặc không phản hồi
        req.on('timeout', () => { req.destroy(); resolve(); });
        req.end();
    }).then(() => {
        // 2. Backup: kill child process trực tiếp nếu còn sống
        if (pyProc) {
            try {
                // Kill cả process tree (cho trường hợp admin re-launch tạo child)
                if (process.platform === 'win32') {
                    try { execSync(`taskkill /F /T /PID ${pyProc.pid}`, { stdio: 'ignore' }); } catch {}
                }
                pyProc.kill();
            } catch {}
            pyProc = null;
        }
    });
}

function createWindow() {
    const win = new BrowserWindow({
        width: 1280,
        height: 720,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    win.loadFile('index.html');
}

app.whenReady().then(() => {
    startPython();
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', async () => {
    await stopPython();
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

// Đảm bảo kill Python khi Electron bị force quit
app.on('before-quit', () => {
    stopPython();
});
