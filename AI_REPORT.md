# Báo cáo điều tra nguyên nhân lỗi Backend dừng giữa chừng (AI_REPORT)

## 1. Tổng quan dự án
Ứng dụng Skirk Macro gồm:
- **Frontend**: Electron + HTML + JS vanilla (`src/UI/`)
- **Backend**: Python HTTP Server + `pynput` listener (`src/macro/main.py`)
- **Build**: PyInstaller (`Cryss.exe`) + Electron Builder (`win-unpacked/Cryss.exe`)

## 2. Kiến trúc & Luồng hoạt động
```
[Electron main.js] ──(spawn)──> [Cryss.exe (Python Backend)]
                                        │
                                   (IsAdmin Check)
                                        │
                                (Init pynput Hooks)
                                        │
                                (Start HTTP :5000)
                                        │
[Electron Renderer] ──(POST /run, /save)──> [HTTP Server]
        │                                     │
   (Key Press)                          (Active Bindings)
        │                                     │
   (pynput listener) ──(Trigger Thread)──> [worker(key)]
                                              │
                                        [skkC0_EQA_...]
                                              │
                                    (Loop steps + sleep)
                                              │
                                   if is_no_key_pressed():
                                        return None  <-- [DỪNG GIỮA CHỪNG]
```

## 3. Danh sách nghi vấn & Đánh giá xác suất

| STT | Nguyên nhân | Xác suất | Lý do | File / Code liên quan |
|-----|-------------|----------|-------|----------------------|
| 1 | **Nhả phím sớm làm `is_no_key_pressed()` abort combo** | ★★★★★ | `is_no_key_pressed()` kiểm tra `bind_key not in pressed`. Nếu người dùng nhấn nhả (tap) thay vì giữ phím trong suốt combo, listener `on_release`/`on_click` loại phím khỏi `pressed`. Combo dừng ngay bước tiếp theo mà không báo lỗi. Khác biệt máy do thói quen gõ hoặc polling rate thiết bị. | `src/macro/main.py` L424-428, L700-875 |
| 2 | **Lỗi PyInstaller `--windowed` crash do `print()`** | ★★★★☆ | Trong PyInstaller `--windowed`, `sys.stdout` bị set thành `None`. Dòng `print(ctypes.windll.shell32.IsUserAnAdmin())` hoặc các lệnh `print` khác gây `AttributeError` khi chạy packaged. | `src/macro/main.py` L27 |
| 3 | **UAC Admin Re-launch làm đứt kết nối process** | ★★★★☆ | `ShellExecuteW` tạo process elevated mới và `sys.exit()` process cũ. Tham số truyền `sys.executable` kèm `__file__` trong `--onefile` gây sai tham số CLI. | `src/macro/main.py` L16-25, `src/UI/main.js` L22-25 |
| 4 | **LowLevelHooksTimeout của Windows unhook `pynput`** | ★★★☆☆ | Windows tự động hủy hook `SetWindowsHookEx` nếu callback xử lý chậm hơn `LowLevelHooksTimeout` (300ms) hoặc bị Antivirus can thiệp. Phím không được discard/add đúng làm logic dừng combo. | `src/macro/main.py` L1154-1155 |
| 5 | **Timer Resolution Windows làm sai lệch timing & Starvation** | ★★★☆☆ | Timer mặc định Windows là 15.6ms. `time.sleep(1/120)` thiếu `timeBeginPeriod(1)` gây trễ gấp đôi. Busy-wait loop (`while ... pass`) gây 100% CPU core làm nghẽn thread. | `src/macro/main.py` L147, L216 |

## 4. Kết luận nguyên nhân chính
Nguyên nhân gốc rễ cao nhất làm "hàm chỉ chạy được một đoạn đầu rồi dừng giữa chừng không có exception" là:
1. **Logic `is_no_key_pressed()`**: Combo được thiết kế giả định người dùng **giữ chặt phím** trong suốt thời gian combo chạy. Khi người dùng nhả phím (hoặc phím mouse side button nhả signal trước khi combo xong), `is_no_key_pressed()` trả về `True` và `return None` ngắt hàm lập tức.
2. **Thiếu logging trong Packaged EXE**: Vì `stdio: 'ignore'` và `sys.stdout = None` trong PyInstaller `--windowed`, mọi Exception hay log dừng đều bị nuốt hoàn toàn, làm ứng dụng không có log lỗi.

## 5. Kế hoạch đề xuất sửa lỗi (Phase 5)

### Step 1: Bổ sung File Logging an toàn trong Python Backend
- Thêm file logger ghi ra `%APPDATA%\SkirkMacro\backend.log` hoặc thư mục làm việc để bắt toàn bộ exception và lý do dừng combo.
- Bọc `sys.stdout` / `sys.stderr` tránh crash khi gọi `print()` trong `--windowed`.

### Step 2: Cấu hình chế độ Trigger phím (Hold vs Toggle/Press)
- Bổ sung tùy chọn hoặc sửa logic `is_no_key_pressed()`: Cho phép combo chạy trọn vẹn (Hold vs One-shot trigger) hoặc thêm debounce/grace period trước khi abort.

### Step 3: Sửa đoạn UAC Admin Re-launch trong `main.py`
- Kiểm tra đúng `getattr(sys, 'frozen', False)` khi gọi `ShellExecuteW` để không truyền `__file__` thừa làm sai lệnh `Cryss.exe`.

### Step 4: Tối ưu Timer & CPU Resolution trên Windows
- Gọi `ctypes.windll.winmm.timeBeginPeriod(1)` khi khởi động backend để đảm bảo `time.sleep()` chính xác tới 1ms.
- Thay thế các vòng lặp busy-wait `while ... pass` bằng sleep ngắn ngắt nhỏ để tránh 100% CPU core starvation.
