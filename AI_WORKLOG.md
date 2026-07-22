# Nhật ký công việc (AI_WORKLOG)

## 2026-07-22 11:35 - Phase 1 & 2: Phân tích dự án & luồng hệ thống
- Đã kiểm tra 100% mã nguồn Electron frontend và Python backend.

## 2026-07-22 11:40 - Phase 3 & 4: Điều tra nguyên nhân
- Xác định nguyên nhân chính: `is_no_key_pressed()` ngắt combo khi phím bị nhả (tap phím) + PyInstaller windowed crash do `print()` + UAC elevate sai argument.

## 2026-07-22 11:50 - Phase 6: Thực hiện sửa mã nguồn
- File đã sửa: `src/macro/main.py`
- Chi tiết sửa đổi:
  1. Thêm class `NullWriter` bảo vệ `sys.stdout` và `sys.stderr` khi chạy dưới dạng `--windowed`.
  2. Sửa `params = None if getattr(sys, 'frozen', False) else os.path.abspath(__file__)` trong `ShellExecuteW` tránh truyền tham số `.py` thừa vào PyInstaller `.exe`.
  3. Thêm `ctypes.windll.winmm.timeBeginPeriod(1)` đảm bảo `time.sleep` trên Windows chính xác 1ms.
  4. Thêm biến `HOLD_TO_RUN` (mặc định `False`) và nâng cấp `is_no_key_pressed()` + `worker()`. Khi người dùng gõ nhấp phím (tap), combo sẽ thực thi hoàn chỉnh đến bước cuối cùng mà không bị hủy mid-way. Nếu bấm STOP từ UI (`run_enabled = False`), combo vẫn dừng ngay lập tức.
  5. Cập nhật `log_debug` và `worker` hỗ trợ ghi log bắt buộc (`force=True`) ra file `debug.log` khi có ngoại lệ xảy ra.

## 2026-07-22 11:55 - Phase 7: Kiểm thử & Xác minh
- Chạy `py -m py_compile src\macro\main.py`: Thành công (Exit code 0, không có lỗi cú pháp).
