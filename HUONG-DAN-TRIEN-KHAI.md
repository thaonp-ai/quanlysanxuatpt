# Web tra cứu P&ID / PFD Xưởng Phụ Trợ – Hướng dẫn triển khai

## Cấu trúc thư mục `web/`

```
web/
  index.html          giao diện tra cứu (một file, không cần build)
  data/data.json      toàn bộ dữ liệu: Unit, bản vẽ, tag (đường ống, thiết bị, van) và vị trí trên bản vẽ
  img/*.png           ảnh bản vẽ (mỗi trang P&ID / PFD một ảnh)
  _headers            cấu hình cache cho Cloudflare Pages
```

Web là trang tĩnh: chỉ cần đưa nguyên thư mục `web/` lên Cloudflare Pages.

## Cách 1 (khuyên dùng): GitHub + Cloudflare Pages – web tự cập nhật khi Claude sửa

1. Tạo tài khoản GitHub, tạo repository riêng tư (private), ví dụ `pid-xuong-phu-tro`.
2. Đưa nội dung thư mục `web/` vào repository (trên GitHub: *Add file → Upload files*, kéo thả cả thư mục).
3. Trên claude.ai: *Settings → Connectors → GitHub* để kết nối GitHub với Claude.
4. Trên Cloudflare: *Workers & Pages → Create → Pages → Connect to Git*, chọn repository vừa tạo.
   - Framework preset: **None**
   - Build command: *để trống*
   - Build output directory: `/` (hoặc `web` nếu bạn để thư mục `web/` bên trong repo)
5. Sau khi mua tên miền trên Cloudflare: vào project Pages → *Custom domains → Set up a custom domain*, nhập ví dụ `pid.tenmien.vn`. Cloudflare tự tạo bản ghi DNS và chứng chỉ HTTPS.
6. Từ đây, mỗi khi bạn nhờ Claude sửa (thêm tag, sửa tên Unit, thêm bản vẽ mới…), Claude sửa `data/data.json` / ảnh và đẩy (push) lên GitHub → Cloudflare tự triển khai lại trong khoảng 1 phút.

## Cách 2: Tải thư mục lên thủ công (không cần GitHub)

Cloudflare: *Workers & Pages → Create → Pages → Upload assets*, kéo thả thư mục `web/`. Mỗi lần có thay đổi, Claude cập nhật thư mục `web/` trên máy bạn, bạn tải lại lên (Create new deployment).

## Bảo mật (nên làm)

Bản vẽ P&ID là tài liệu nội bộ của nhà máy. Nên bật **Cloudflare Zero Trust → Access → Applications → Self-hosted**, chọn tên miền của web và đặt quy tắc chỉ cho phép email công ty (ví dụ `*@pvfcco.com.vn`) hoặc danh sách email cụ thể. Gói miễn phí cho tối đa 50 người dùng.

## Cập nhật dữ liệu

- Tag được nhận dạng tự động (OCR) từ bản vẽ, chỉ trong vùng dòng công nghệ (đã bỏ khung tên, ghi chú, bảng stream, danh sách thiết bị bên phải).
- OCR có thể đọc sai hoặc bỏ sót một số tag. Khi phát hiện, chỉ cần nói với Claude, ví dụ: “Trên bản vẽ 2539-31-PID-0031-05 thiếu van 30-PV-31005” hoặc “Sửa tag 30-P-3O01A thành 30-P-3001A”.
- Khi có bản vẽ mới / sửa đổi: đặt file PDF vào thư mục `PIDvaQLSX` và nhờ Claude chạy lại nhận dạng cho trang đó.

## Chỉnh sửa tag trên web

- Bấm **Sửa** cạnh tag để đổi tên, đổi loại, ghi chú hoặc ẩn tag đọc nhầm. Thiếu tag: mở bản vẽ, bấm **+ Thêm tag** rồi bấm vào vị trí trên bản vẽ.
- Chỉnh sửa lưu chung trên Cloudflare (Workers KV, gói miễn phí), mọi người dùng thấy giống nhau, có lịch sử (ai sửa, lúc nào).
- **Xuất Excel**: danh sách đang lọc hoặc toàn bộ, kèm sheet lịch sử chỉnh sửa.
- Giới hạn quyền sửa (nên làm nếu chưa bật Cloudflare Access): Cloudflare → Workers & Pages → quanlysanxuatpt → **Settings → Variables and Secrets → Add** → loại **Secret**, tên `EDIT_PASSWORD`, giá trị là mã sửa. Người sửa nhập mã này một lần trong hộp thoại Sửa.
- Nếu bật Cloudflare Access, cột "Người sửa" tự lấy email đăng nhập.
