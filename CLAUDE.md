# Ghi chú cho Claude khi cập nhật repo này

Repo chứa web tĩnh tra cứu P&ID/PFD Xưởng Phụ Trợ (Đạm Phú Mỹ). Cloudflare Workers Builds tự triển khai từ nhánh `main` (worker.js + thư mục `web/`).

## Sửa nhanh (không cần OCR lại)
- Thêm/sửa/xóa tag: sửa trực tiếp `web/data/data.json`.
  - `tags[]`: `{"t": tag, "k": "line|equipment|valve", "s": loại, "d": mô tả, "o": [[chỉ số sheet, x, y, w, h(, 1 = chỉ thấy ở khung tiêu đề)]], "l": [nhãn gốc]}`; tọa độ là tỉ lệ 0–1 theo ảnh.
  - `sheets[]`: bản vẽ (`id`, `unit`, `dwg`, `title`, `img`, `w`, `h`).
  - `units[]`: mã Unit và tên.
  - Cập nhật trường `updated` (dd/mm/yyyy).
- Nhưng lưu ý: nếu sau này dựng lại bằng `tools/build.py`, sửa tay trong data.json sẽ bị ghi đè. Sửa tên tag lâu dài: thêm cặp `"tag OCR": "tag đúng"` vào `tools/overrides.json` (build.py áp dụng ở bước cuối); tên bản vẽ/Unit: `tools/sheetfix.json` / `tools/units.json`. Bỏ một nhãn thiết bị chỉ là chú thích dòng/tín hiệu: thêm `[sheet, x tâm, y tâm, tag]` vào `tools/exclude.json`.

## Chỉnh sửa trên web (người dùng tự sửa)
- `worker.js` (Cloudflare Worker) phục vụ `web/` và API `/api/edits`, lưu chỉnh sửa vào KV binding `EDITS`, khóa `state` = `{edits, log}`.
  - Khóa tag: `o:<tên OCR gốc trong data.json>` (sửa tên/loại/ghi chú/ẩn) hoặc `n:<id>` (tag thêm thủ công, có `o: [[sheet_id, x, y, w, h]]`).
- Đăng nhập bắt buộc (worker chạy trước mọi request, `run_worker_first: true`): cookie `pid_session` ký HMAC; tài khoản ở KV `auth:users` (PBKDF2), quyền admin/editor/viewer; admin dựng sẵn = tên `admin` + secret `ADMIN_PASSWORD`. Trang `/login`, `/account` (đổi mật khẩu, quản lý tài khoản) nằm trong worker.js. Nhập tài khoản từ Excel: `web/account-import.js` + `web/xlsx.js` (đọc/ghi xlsx), mật khẩu băm PBKDF2 ở trình duyệt rồi POST `/api/users` `{action:"bulk"}`. Chỉ editor/admin được POST `/api/edits`; "by" = họ tên tài khoản.
- Web gộp `data.json` + chỉnh sửa khi hiển thị; nút "Xuất Excel" xuất danh sách + sheet lịch sử.
- Khi dựng lại `data.json`, KHÔNG đổi tên OCR gốc của tag đã có chỉnh sửa trên web, nếu không khóa `o:` sẽ không khớp nữa. Muốn đưa chỉnh sửa web vào dữ liệu gốc: lấy file Excel người dùng xuất (cột "Tên OCR gốc" → "Tag"), thêm vào `tools/overrides.json`, rồi nhắc người dùng rằng các mục đó vẫn còn trong KV (vẫn hiển thị đúng vì tên mới trùng).

## Dựng lại dữ liệu từ OCR
Các script dùng đường dẫn cứng `/home/claude/work` và PDF ở `/mnt/user-data/uploads/PIDvaQLSX/`.
1. `mkdir -p /home/claude/work && cp tools/* /home/claude/work/ && cd /home/claude/work && tar xzf ocr-cache.tar.gz` (gồm ocr, ocr2, bub, bub2, verify, fix35, sizecheck, tb)
2. `mkdir -p site && cp -r <repo>/web/. site/`
3. `python3 build.py dd/mm/yyyy` → ghi `site/data/data.json`; chép lại vào `web/data/`.
4. Kiểm tra lại (đã có kết quả trong cache): `verify.py` đọc lại tag ở nhiều cỡ chữ và bỏ phiếu; `sizecheck.py` đọc lại cỡ ống với khung cắt rộng về phía trước nhãn; `fix35.py` phân biệt 3/5 trong số đường ống theo hình dạng chữ (chỉ tin cậy với font đậm của bản vẽ 2098). Chạy lại hai bước này sau khi OCR trang mới, rồi `build.py`.
5. Bản vẽ mới: lấy PDF từ máy người dùng (thư mục `E:\4.DPM\APP Xuong PT\PIDvaQLSX`), chạy `ocr.py`, `bubbles.py`, `titles.py`, `tiles.py` (P&ID), `img.py`, `frame.py` + `area.py` cho trang đó, rồi `build.py`.

Commit thẳng vào `main` (người dùng muốn web cập nhật ngay).

## Tài liệu vendor
- `web/data/vendor.json` (dựng bằng `python3 tools/vendor/build_vendor.py`): `docs[]` `{p: đường dẫn tương đối trong thư mục OneDrive "Vendor Data", t, g: nhóm, no, src, kb, pg: trang trong sách gộp}`, `tags{tag: [chỉ số docs]}`, `base` = link OneDrive "View online" của thư mục Vendor Data (lưu ở `tools/vendor/base_url.txt`). Web chỉ lưu link, không lưu file.
- Web gộp tài liệu theo tag (khớp tên hiện tại hoặc tên OCR gốc) và tài liệu chung của cụm (phần trước "/", hoặc bỏ chữ A/B cuối).
- Nguồn: `listing_lohoi.json` (danh sách file), `titles_778.json` (tên bản vẽ Macchi từ mục lục), `sections.json` (trang bắt đầu các mục Part 1C/1D/1E; `sections_from_ocr.py` tạo từ OCR trang tách mục), `10-V-8001_doclist.csv`. Gắn mã bản vẽ → tag con trong `SUB` của build_vendor.py.
