# D-form

Kênh phát hành bộ cài và cập nhật D-form cho Microsoft Word trên Windows.

Repository này chứa trang tải, công cụ tạo thông tin cập nhật và tài liệu phát hành. Mã nguồn add-in D-form được giữ riêng; bộ cài nằm trong Releases.

## Trạng thái

D-form 1.7.0 preview cho Word desktop 64-bit. Tải tại [trang D-form](https://tronieph.github.io/d-form-releases/) hoặc [Releases](https://github.com/TroniePh/d-form-releases/releases).

## Tải và cập nhật

Các bản phát hành xuất hiện tại [Releases](https://github.com/TroniePh/d-form-releases/releases).

- `AllUsers.exe`: cài cho toàn bộ người dùng, cần quyền quản trị; dùng để cập nhật bản đã cài toàn máy.
- `Free.exe`: cài riêng cho người dùng hiện tại.
- `SHA256SUMS.txt`: mã kiểm tra SHA-256 của bộ cài.
- `update.json`: thông tin phiên bản để D-form kiểm tra và tải cập nhật.
- `RELEASE-NOTES.md`: thay đổi và hướng dẫn của từng phiên bản.

Lưu tài liệu và đóng Word trước khi chạy bộ cài. Cấu hình và mẫu cá nhân được giữ riêng trong tài khoản Windows.

[Liên hệ Phạm Duy](https://www.facebook.com/neull)

## Phát hành bản tiếp theo

1. Build và kiểm thử bộ cài trước khi phát hành. Tăng phiên bản, ví dụ `1.7.1`. Mỗi bộ cài kế tiếp cần giữ thành phần `DFormUpdater.exe`, cấu hình của nó và đăng ký chạy nền. Trong dự án riêng dùng `installer/build-installer.ps1 -AutoUpdate` cho cả Free/AllUsers.
2. Tạo release tag `v1.7.1`; tải lên đủ `D-form-Setup-v1.7.1-Free.exe` và `D-form-Setup-v1.7.1-AllUsers.exe` cùng ghi chú. Phiên bản và tên tệp phải khớp tag.
3. Nếu còn dùng thử, chọn **This is a pre-release**. Chỉ bỏ nhãn này khi đã xác nhận phát hành ổn định.
4. Bấm Publish release. GitHub Actions kiểm tra tên, nguồn tải, dung lượng và SHA-256 do GitHub ghi nhận, tạo thông tin cập nhật/checksum nếu thiếu và triển khai trang tải mới.

Website và `update.json` chọn bản đủ hai bộ cài có phiên bản lớn nhất; `stable.json` chỉ chọn bản ổn định. Bản thử còn mới hơn bản ổn định không được tự cấp cho máy dùng kênh ổn định. Cài gói có bộ cập nhật một lần để nhận các bản mới; Free chờ Word đóng rồi cài, AllUsers cần xác nhận quyền quản trị. Không tự đóng hoặc sửa tài liệu Word.

Workflow là hạ tầng phát hành, không thay thế kiểm thử tính năng/cài nâng cấp. Không tải lên thư mục nguồn add-in, cấu hình cơ quan hoặc tài liệu người dùng. Liên hệ Zalo **0868609901**.
