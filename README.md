# **CÁC BƯỚC ĐỂ TRỞ THÀNH SKIRKBU MẠNH NHẤT VI EN LÀ GÌ?**
B1: SỞ HỮU CON PÊ CÊ SIÊU KHỦNG.

B2: UNLOCK FPS GENSHIT.

B3: CÀI MACRO SKIRK(?).

**VẬY MACRO SKIRK LẤY Ở ĐÂU?, REPO NÀY CHÍNH LÀ CÂU TRẢ LỜI**
# **Tính năng cơ bản**
- Sử dụng các khối combo (VD: N2D, N3W, N5D, N1CD, N2CD, ...) để sắp xếp tạo thành combo hoàn chỉnh
- Cho phép người dùng sắp xếp, tuỳ chỉnh độ trễ thông qua FPS nhập vào
- Giao diện trực quan, rõ ràng, font chữ đẹp, khối màu nổi để dễ nhìn thân thiện với người dùng
- ...
# **Nghiệp vụ**
- Ngôn ngữ lập trình: Python, Javascrpit
- Các framework: Electron, ...
- Yêu cầu phải tạo file .bat để có thể chạy trực tiếp code mà không cần đóng gói
- Yêu cầu ép CPU đếm chính xác thời gian ở những vị trí như Walk cancel của Skirk, giữa các khối combo thì dùng sleep đơn giản
- Phần xử lý macro phải dùng ngôn ngữ Python, các khối macro phải viết trên 1 funtion được đặt tên tường minh
- Phần giao diện sẽ sử dụng Javascript xử lý với framework Electron
- Có 1 file .bat chạy không giao diện với setup lưu trên json để debug
