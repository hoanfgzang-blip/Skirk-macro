# Tiến trình công việc (AI_PROGRESS)

- [x] Phase 1: Đọc toàn bộ frontend (Electron, HTML, JS)
- [x] Phase 1: Đọc toàn bộ backend (Python, HTTP server, pynput, combo functions)
- [x] Phase 2: Phân tích luồng hoạt động & dependency
- [x] Phase 3: Điều tra các nguyên nhân tiềm năng & đánh giá xác suất
- [x] Phase 4: Đối chiếu nghi vấn với mã nguồn
- [x] Phase 5: Lập báo cáo chi tiết (AI_REPORT.md) & kế hoạch sửa
- [x] Phase 6: Thực hiện sửa code từng bước:
  - [x] Xử lý `sys.stdout` / `sys.stderr` = `NullWriter` khi PyInstaller windowed mode
  - [x] Sửa UAC Elevate argument `ShellExecuteW` cho frozen executable
  - [x] Thêm `winmm.timeBeginPeriod(1)` tăng độ chính xác 1ms cho sleep trên Windows
  - [x] Nâng cấp `is_no_key_pressed()` & `HOLD_TO_RUN` (One-shot mode mặc định) chống ngắt combo giữa chừng khi nhả phím
  - [x] Bổ sung logging lỗi với `force=True` ra file `debug.log`
- [x] Phase 7: Kiểm thử & xác minh cú pháp Python (Syntax check passed)
