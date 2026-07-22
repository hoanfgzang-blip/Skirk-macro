# Skirk Macro

## Tính năng

- Giao diện người dùng dễ tiếp cận
- Lựa chọn các combo mì ăn liền hoặc tự custom combo dựa trên các khối sẵn có
- Hỗ trợ tạo nhiều combo custom và mỗi combo 1 phím tắt
- Combo tự chỉnh độ trễ phù hợp đối với FPS người dùng nhập vào
- Người dùng có thể tự do bật tắt Macro để không ảnh hưởng tới công việc khác mà không cần đóng app
- Không yêu cầu về chuột xịn

## CÁCH TẢI
- Truy cập vào Link [DOWNLOAD](https://github.com/hoanfgzang-blip/Skirk-macro/releases)
- Chọn phiên bản mới nhất
- Đối với WINDOWS: tải file .zip và giải nén, đối với Linux thì theo dõi cách build ở dưới
- Mở folder được giải nén và chạy file Cryss.exe ngay đầu

**DEV**
## Yêu cầu
- Linux
- Windows
- Python 3 
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

## Nhược điểm của ứng dụng
- Đây không phải driver chuột nên nút được gán macro sẽ bị nhận diện là được sử dụng
- Phải gán chuẩn xác FPS trung bình thấp khi thực chiến chứ không phải FPS trung bình nếu máy không quá mạnh
- Khi chạy mà bị drop FPS thì macro sẽ xảy ra hiện tượng cancel bị lỗi
- Khi thực hiện thao tác đánh thường máy yếu thường có hiện tượng drop FPS và CPU bị chiếm dụng cao ở 1 coreA
- Chỉ khuyến khích cho người có máy khoẻ

## Liên hệ

- Discord: `rururu_11`
- Facebook: [HoanfGZang.UwU](https://www.facebook.com/HoanfGZang.UwU)
