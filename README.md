# Tra cứu P&ID / PFD Xưởng Phụ Trợ – Nhà máy Đạm Phú Mỹ

Web tĩnh để tìm đường ống, thiết bị và van trên bản vẽ P&ID / PFD, chia theo Unit, có đánh dấu vị trí trên bản vẽ.

- `web/` – trang web (Cloudflare Pages: build output directory = `web`, không cần build command)
  - `index.html` – giao diện
  - `data/data.json` – Unit, danh sách bản vẽ, tag và vị trí
  - `img/` – ảnh từng trang bản vẽ
- `tools/` – công cụ nhận dạng (OCR) và dựng lại `data.json`; `ocr-cache.tar.gz` lưu kết quả OCR để không phải chạy lại
- `HUONG-DAN-TRIEN-KHAI.md` – hướng dẫn triển khai Cloudflare

Tag được nhận dạng tự động từ bản vẽ (OCR), chỉ trong vùng sơ đồ chính. Luôn đối chiếu bản vẽ gốc trước khi thao tác.
