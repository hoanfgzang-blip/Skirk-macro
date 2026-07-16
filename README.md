# Skirk Macro

Ứng dụng macro cho Windows với giao diện Electron và backend Python. Ứng dụng cho phép chọn combo, đặt FPS, gán phím hoặc nút chuột kích hoạt, sau đó bật/tắt macro trực tiếp từ giao diện.

> Chỉ sử dụng khi việc tự động hóa đầu vào phù hợp với quy định của trò chơi/phần mềm bạn đang dùng.

## Tính năng

- Bốn combo có sẵn để lựa chọn.
- Gán phím bàn phím, phím chức năng hoặc nút chuột cho từng combo.
- Lưu cấu hình FPS và phím đã gán vào `src/macro/config.json` khi chạy mã nguồn.
- Nút **RUN/STOP** để bật hoặc dừng việc nhận phím kích hoạt.
- Backend chạy máy chủ nội bộ tại `localhost:5000` để giao tiếp với giao diện.
- Bản đóng gói yêu cầu quyền quản trị để có thể gửi và lắng nghe input toàn hệ thống.

## Yêu cầu

- Windows
- Python 3 (có lệnh `python` trong `PATH`)
- Node.js và pnpm

## Cài đặt

Tại thư mục dự án, cài các thư viện Python:

```powershell
python -m pip install -r requirements.txt
```

Cài phụ thuộc cho giao diện:

```powershell
cd src\UI
pnpm install
```

## Chạy ở môi trường phát triển

```powershell
cd src\UI
pnpm start
```

Electron sẽ tự khởi động backend Python từ `src/macro/main.py`. Khi Windows hỏi nâng quyền, hãy chấp nhận để macro hoạt động.

## Cách sử dụng

1. Chọn combo trong danh sách.
2. Nhập FPS hiện tại của game/phần mềm.
3. Chọn **Click to bind a key...**, rồi nhấn phím hoặc nút chuột muốn gán.
4. Nhấn **SAVE** để lưu cấu hình.
5. Nhấn **RUN** để bật macro.
6. Giữ phím/nút đã gán để chạy combo; nhả ra để dừng. Nhấn **STOP** khi không dùng nữa.

Nhấn `Esc` trong lúc đang chờ gán phím sẽ xóa phím gán của combo hiện tại.

## Đóng gói ứng dụng

Sau khi đã cài Python dependencies và `pnpm install`, chạy:

```powershell
.\build.bat
```

Script sẽ đóng gói backend thành `Cryss.exe`, sau đó đóng gói Electron. Bản chạy được nằm tại:

```text
build\app\win-unpacked\Cryss.exe
```

### Linux

Trên Linux, cài các gói cần thiết cho Electron, Python 3, `pip`, Node.js và pnpm theo bản phân phối đang dùng. Sau đó cài dependency như phần **Cài đặt**, cấp quyền chạy cho script và thực thi:

```bash
chmod +x build-linux.sh
./build-linux.sh
```

Script tạo backend Python `Cryss` và đóng gói Electron cho Linux. File chạy nằm tại:

```text
build/app-linux/linux-unpacked/Cryss
```

## Cấu trúc dự án

```text
src/
├── macro/
│   ├── main.py       # Macro engine, hotkey listener và HTTP server
│   └── config.json   # FPS và phím gán đã lưu
└── UI/
    ├── main.js       # Electron main process
    ├── fe.js         # Logic giao diện và lưu cấu hình
    ├── index.html
    └── style.css
build.bat             # Script đóng gói Windows
build-linux.sh         # Script đóng gói Linux
requirements.txt      # Thư viện Python
```

## Khắc phục sự cố

- **Không nhận phím hoặc không gửi được input:** chạy ứng dụng bằng quyền Administrator.
- **Giao diện không kết nối backend:** bảo đảm cổng `5000` chưa bị ứng dụng khác sử dụng và khởi động lại ứng dụng.
- **Combo chạy lệch thời điểm:** đặt FPS đúng với FPS thực tế; thời gian combo được nội suy theo FPS.

## Liên hệ

- Discord: `rururu_11`
- Facebook: [HoanfGZang.UwU](https://www.facebook.com/HoanfGZang.UwU)
