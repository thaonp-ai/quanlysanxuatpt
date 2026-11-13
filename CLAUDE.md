# Ghi chú cho Claude khi cập nhật repo này

Repo chứa web tĩnh tra cứu P&ID/PFD Xưởng Phụ Trợ (Đạm Phú Mỹ). Cloudflare Workers Builds tự triển khai từ nhánh `main` (worker.js + thư mục `web/`).

## Sửa nhanh (không cần OCR lại)
- Thêm/sửa/xóa tag: sửa trực tiếp `web/data/data.json`.
  - `tags[]`: `{"t": tag, "k": "line|equipment|valve", "s": loại, "d": mô tả, "o": [[chỉ số sheet, x, y, w, h(, 1 = chỉ thấy ở khung tiêu đề)]], "l": [nhãn gốc]}`; tọa độ là tỉ lệ 0–1 theo ảnh.
  - `sheets[]`: bản vẽ (`id`, `unit`, `dwg`, `title`, `img`, `w`, `h`).
  - `units[]`: mã Unit và tên.
  - Cập nhật trường `updated` (dd/mm/yyyy).
- Tag có mặt cả trên P&ID và PFD: build.py chỉ giữ vị trí trên P&ID (bỏ vị trí PFD); tag chỉ có trên PFD giữ nguyên.
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
- OneDrive không mở PDF tới trang cụ thể, nên các mục sách gộp (Part 1C/1D/1E) được tách thành file riêng bằng `tools/vendor/split_sections.py` (qpdf) và đã chép vào OneDrive `Vendor Data\Lo hoi phu tro\Tach theo muc\` (78 file); `sections_split.json` ánh xạ mục → file. Doc của mục có `bp`/`bpg` = sách gốc + trang bắt đầu (nút "Sách gốc" trên web). Khi thêm sách mới: OCR, `sections_from_ocr.py`, `split_sections.py`, chép file tách vào OneDrive (SendUserFile + device_commit_files), rồi `build_vendor.py`.
- HRSG 10-B-9001 (SICES, `Vendor Data\HRSG\BOOK1..10.pdf`): `tools/vendor/hrsg/` — `index.json` (mục lục), `pages_b1_5.json` / `pages_b6.json` ([mã, tên, cuốn, trang đầu, trang cuối]), `build_hrsg.py` → `docs.json` (build_vendor.py nạp). Cuốn 7–10 là Inspection book, chỉ gắn nguyên cuốn. File tách theo tài liệu (234 file) đã ở OneDrive `Vendor Data\HRSG\Tach theo tai lieu\`; tách lại: `python3 build_hrsg.py <thư mục Vendor Data> <thư mục ra>`. Gắn mã tài liệu → tag con trong `SUB` của build_hrsg.py.
- Nước làm mát Unit 33 (`Vendor Data\Nuoc lam mat`): `tools/vendor/nlm/` — `listing.json` (danh sách file), `build_nlm.py` (bỏ file trùng giữa các thư mục, đặt tên/nhóm/tag theo thư mục & trang bìa) → `docs.json` + `sizes.json`. Tài liệu cả cụm gắn vào mã gốc (30-CT-3001, 30-P-3001, 30-P-3002, 30-E-3001) — web tự hiện cho A/B/C… Sách tách theo mục ở OneDrive `Nuoc lam mat\Tach theo muc\30-PK-3001\` (theo bookmark, `pk3001_outline.json`) và `...\30-P-3001\` (sách bơm Worthington: trang phân cách màu + OCR, `p3001_sections.json`). Tách lại: `python3 build_nlm.py <thư mục Nuoc lam mat> <thư mục ra>`. File .dwg/.db/.bak không đưa lên web.
- Nước thô / sinh hoạt / cứu hỏa (`Vendor Data\9. Raw-Pot-Fire`): `tools/vendor/rpf/` — `listing.txt` (đường dẫn|byte, đã bỏ file rác FS15/FS16, Thumbs.db, trang bìa mục), `build_rpf.py` → `docs.json` + `sizes.json`. Bơm nước thô gắn `30-P-2001`, bơm sinh hoạt `30-P-2002`, bơm cứu hỏa 30-PK-4001/4002 gắn `30-P-4001`/`30-P-4002`, cụm 30-PK-2001 gắn tag con (FL2 than hoạt tính, FL1 lọc tinh — theo thông số thiết bị của vendor, P1/P2 bơm định lượng, P3 bơm thùng, TK1 bồn hypochlorite, 2Z1 bộ trộn tĩnh). File đã tách sẵn theo mục nên không cần tách sách. build_vendor.py nạp cả `nlm/` và `rpf/`.
- Demi Unit 31 (`Vendor Data\4. Demi`): `tools/vendor/demi/` — `listing.txt` (đã bỏ ảnh `Hình ảnh demi`, .dwg, file Acrobat Catalog FS13/14/18), `build_demi.py` → `docs.json` + `sizes.json`; `e1001_tags.json` = tên mục sách Alfa Laval 30-E-1001 (Tag 1..6). Sách Chemitreat 30-PK-1001 (6 volume) đã là file riêng theo mục; tag con 30-PK-1001/V1..V5, P1..P8, K1/K2, TK3..TK11, BA1… theo từ khóa tên file (cation/anion/degas/MB/NP/Na2SO3/acid/caustic).
- Air System Unit 35 (`Vendor Data\7. Air System`): `tools/vendor/air/` — `listing.txt`, `databook_sections.json` (mục của `3. 30-K-5001/data book.pdf`, Atlas Copco 269 trang scan, tìm trang bìa bằng OCR), `split_sizes.json`, `build_air.py` → `docs.json` + `sizes.json`. 18 file tách đã ở OneDrive `7. Air System\3. 30-K-5001\Tach theo tai lieu\` (doc có `bp`/`bpg`); tách lại: `python3 build_air.py <thư mục 7. Air System> <thư mục ra>`. Tên tài liệu revamp 2539-1031/4171-01-<mã> lấy từ trang bìa (bảng `VDOC`). File > ~30 MB phải SendUserFile rồi device_commit_files bằng fileUuid.
- build_vendor.py nạp `nlm/`, `rpf/`, `demi/`, `air/`.
- Các thư mục mới khác trong Vendor Data chưa xử lý (11/2026): 10GT9001, 6. Bon chua amonia & Flare, 8. Hệ thống Nito, 9. Xử lý nước thải.

## Công nghệ (mô tả công nghệ trích từ tài liệu)
- `web/data/tech.json` do `python3 tools/vendor/tech/build_tech.py` tạo (nội dung viết tay trong script, có nguồn trích). `units{mã Unit}` = trang tổng quan (nút "Công nghệ ›" dưới Unit ở cột trái); `tags{mã}` = đoạn cho thiết bị (nút "Công nghệ" ở dòng tag, nút trên thanh bản vẽ, tab "Công nghệ" trong bảng tài liệu). Web tìm theo tag đầy đủ → bỏ chữ cuối A/B → bỏ "M" của motor (/MP1A → /P1) → phần trước "/". Nguồn `["sheet:<dwg>", nhãn]` mở bản vẽ, còn lại là đường dẫn trong Vendor Data.
- Đã có: Unit 32 (nước thô & nước sinh hoạt) — 30-TK-2001/2002, 30-P-2001/2002, 30-PK-2001 và thiết bị con. Nguồn: sách 30-PK-2001 (Chemitreat, bản scan → OCR), data sheet/biên bản thử bơm Flowserve, PFD 2539-32 as-built.
- Unit 18 (lò hơi phụ & nước cấp lò) viết trong `tools/vendor/tech/u18.py` (build_tech.py import): 10-B-8001 + tag con (V1, V2, SH1/2, E1, K1, MK1, STK1, SK1, SL1/2), 10-PK-8004, 10-V-8001…8004, 10-P-8001/8002/8003, 10-STP-8001/8002, 10-E-8001/8002, 10-PK-8001…8003, 10-SL-8001…8003. Nguồn: sách Macchi Part 1D (mục tách ở `Tach theo muc`, bản scan → OCR), 778-C-073, data sheet trong `1. Cac cum thiet bi_tank lien quan`, PFD 2539-18 case 2/3 as-built.
- Unit 31 (Demi, 30-PK-1001 và thiết bị con, 30-TK-1001…1004, 30-P-1001…1004, 30-E-1001/1002) và Unit 35 (30-K-5001A–E, 30-V-5001/5002, 30-DR-5001/5002) viết trong `tools/vendor/tech/u31_35.py`. Nguồn: PFD 2539-31/35 as-built, bảng thông số trên P&ID, sách Chemitreat (Vol 1 mục 2/5/9/10/11/13, Vol 2 mục 1.3.8 – scan → OCR), mô tả công nghệ revamp 2539-31/35-CN-0009-01, data sheet + instruction book Atlas Copco ZR, O&M máy sấy SPX Hankison (khối bổ sung ở cuối file).
