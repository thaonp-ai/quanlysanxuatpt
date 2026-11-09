# Ghi chú cho Claude khi cập nhật repo này

Repo chứa web tĩnh tra cứu P&ID/PFD Xưởng Phụ Trợ (Đạm Phú Mỹ). Cloudflare Pages tự triển khai từ nhánh `main`, thư mục `web/`.

## Sửa nhanh (không cần OCR lại)
- Thêm/sửa/xóa tag: sửa trực tiếp `web/data/data.json`.
  - `tags[]`: `{"t": tag, "k": "line|equipment|valve", "s": loại, "d": mô tả, "o": [[chỉ số sheet, x, y, w, h(, 1 = chỉ thấy ở khung tiêu đề)]], "l": [nhãn gốc]}`; tọa độ là tỉ lệ 0–1 theo ảnh.
  - `sheets[]`: bản vẽ (`id`, `unit`, `dwg`, `title`, `img`, `w`, `h`).
  - `units[]`: mã Unit và tên.
  - Cập nhật trường `updated` (dd/mm/yyyy).
- Nhưng lưu ý: nếu sau này dựng lại bằng `tools/build.py`, sửa tay trong data.json sẽ bị ghi đè. Sửa lâu dài nên đưa vào `tools/sheetfix.json` / `tools/units.json` hoặc thêm một bước override trong `build.py`.

## Dựng lại dữ liệu từ OCR
Các script dùng đường dẫn cứng `/home/claude/work` và PDF ở `/mnt/user-data/uploads/PIDvaQLSX/`.
1. `mkdir -p /home/claude/work && cp tools/* /home/claude/work/ && cd /home/claude/work && tar xzf ocr-cache.tar.gz`
2. `mkdir -p site && cp -r <repo>/web/. site/`
3. `python3 build.py dd/mm/yyyy` → ghi `site/data/data.json`; chép lại vào `web/data/`.
4. Bản vẽ mới: lấy PDF từ máy người dùng (thư mục `E:\4.DPM\APP Xuong PT\PIDvaQLSX`), chạy `ocr.py`, `bubbles.py`, `titles.py`, `tiles.py` (P&ID), `img.py`, `frame.py` + `area.py` cho trang đó, rồi `build.py`.

Commit thẳng vào `main` (người dùng muốn web cập nhật ngay).
