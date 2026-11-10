#!/usr/bin/env python3
"""Danh mục tài liệu HRSG 10-B-9001 (Vendor Data Book SICES, 10 cuốn BOOK1..BOOK10.pdf).

Đầu vào (cùng thư mục):
  index.json        mục lục [mã tài liệu, tên, cuốn] (OCR mục lục ở đầu mỗi cuốn)
  pages_b1_5.json   [mã, tên, cuốn, trang đầu, trang cuối] cho cuốn 1–5 (bản vẽ xếp theo thứ tự mục lục,
                    đã kiểm bằng ảnh thu nhỏ + số bản vẽ đọc ở khung tên)
  pages_b6.json     như trên cho cuốn 6 (tài liệu nhiều trang: trang bìa có "Sheet 1 of N")
Ra:
  docs.json         [{p, t, g, tags, no, src, bp, bpg, from, to}] để build_vendor.py nạp
  và (tuỳ chọn) file tách theo tài liệu: python3 build_hrsg.py <thư mục Vendor Data> <thư mục ra>
  -> <ra>/HRSG/Tach theo tai lieu/<mã> - <tên>.pdf
"""
import json, os, re, subprocess, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
B = "10-B-9001"
SUBDIR = "HRSG/Tach theo tai lieu"

G_GEN = "Tổng quát, móng & lắp dựng"
G_PS = "Phần áp lực (bao hơi, ống, quá nhiệt, hâm nước)"
G_PIPE = "Đường ống & giá đỡ"
G_DUCT = "Ống gió, ống khói, vỏ lò, chịu lửa & bảo ôn"
G_PLAT = "Sàn thao tác & cầu thang"
G_BMS = "Đầu đốt & BMS"
G_INS = "Thiết bị đo & điều khiển"
G_FAN = "Quạt, damper & guillotine"
G_SV = "Van an toàn & bộ tiêu âm"
G_OM = "Vận hành & bảo dưỡng"
G_SP = "Phụ tùng"
G_DS = "Data sheet & tài liệu chính"
G_IB = "Hồ sơ kiểm tra (Inspection book)"


def code_key(c):
    m = re.match(r"6212-([A-Z]+)-(\d+)", c)
    return (m.group(1), int(m.group(2))) if m else ("", 0)


def group_of(c):
    k, n = code_key(c)
    if c in ("6212-P-009.1", "6212-P-009.2", "6212-P-028") or c in ("6212-M-406", "6212-M-409"): return G_SV
    if c.startswith("6212-P-009."): return G_BMS
    if k == "STR" or c == "6212-P-018": return G_FAN
    if c in ("6212-P-027",) or c.startswith("6212-P-043") or c == "6212-P-034": return G_BMS
    if c in ("6212-P-024", "6212-P-035", "6212-P-036", "6212-P-039", "6212-P-053", "6212-P-063.1") or c.startswith("6212-P-037"): return G_INS
    if c == "6212-P-068": return G_OM
    if c in ("6212-P-088", "6212-P-060"): return G_SP
    if c == "6212-P-004": return G_DS
    if c == "6212-P-063": return G_GEN
    if k == "DG":
        if n in (5, 6, 7, 8, 13, 14, 15): return G_PS
        if n == 4: return G_PIPE
        if n in (9, 10): return G_DUCT
        return G_GEN
    if k == "M":
        if n in (140, 141, 200, 201, 202, 203, 204, 205, 208, 700, 710): return G_PS
        if n in (302, 303, 306, 800, 801): return G_GEN
        if 400 <= n < 500 or n == 771: return G_PIPE
        if 500 <= n < 758: return G_DUCT
        if 758 <= n < 800: return G_PLAT
    return G_GEN


SUB = {  # mã tài liệu (tiền tố) -> tag con
    "V1": "DG-07 DG-08 DG-13 M-202 M-204 M-205",
    "E1": "DG-06 DG-15 M-710 M-200 M-201 M-405",
    "E2": "DG-06 DG-15 M-710 M-140 M-141",
    "E3": "DG-05 DG-14 M-700 M-402 M-404",
    "SK1": "DG-09 M-751 M-759 M-763 M-764 M-765 M-766 M-772 M-773",
    "SK2": "DG-10 M-742 M-760 M-761 M-780 M-781 M-782 M-783 M-784 M-785 M-787 M-788 M-790 M-791 P-009.1",
    "SL1": "P-009.2 M-403",
    "K1": "STR-002 STR-008",
    "MK1": "P-018",
    "K2": "STR-003 M-410 M-743",
    "K3": "STR-003 M-410 M-743",
    "MK2": "P-018",
    "MK3": "P-018",
    "MXV1": "STR-004 STR-005 STR-001 STR-006 STR-007 M-740 M-741",
    "MXV2": "STR-004 STR-005 STR-001 STR-006 STR-007 M-740 M-741",
}


def tags_of(c):
    out = [B]
    short = c.replace("6212-", "")
    for sub, codes in SUB.items():
        if any(short == x or short.startswith(x + "-") or short.startswith(x + ".") for x in codes.split()):
            out.append(B + "/" + sub)
    return out


def safe(s):
    s = s.replace("đ", "d").replace("Đ", "D").replace("–", "-").replace("&", "and").replace('"', " inch")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r'[\\/:*?<>|;]+', " ", s)
    return re.sub(r"\s+", " ", s).strip()[:95]


rows = json.load(open(os.path.join(HERE, "pages_b1_5.json")))
if os.path.exists(os.path.join(HERE, "pages_b6.json")):
    rows += json.load(open(os.path.join(HERE, "pages_b6.json")))
SRC = sys.argv[1] if len(sys.argv) > 2 else None
OUT = sys.argv[2] if len(sys.argv) > 2 else None
docs = []
for c, t, b, a, z in rows:
    book = f"HRSG/BOOK{b}.pdf"
    name = safe(f"{c.replace('6212-', '')} - {t}") + ".pdf"
    rel = SUBDIR + "/" + name
    if OUT:
        dst = os.path.join(OUT, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if not os.path.exists(dst):
            r = subprocess.run(["qpdf", os.path.join(SRC, book), "--pages", ".", f"{a}-{z}", "--", dst], capture_output=True, text=True)
            if r.returncode not in (0, 3):
                raise SystemExit(r.stderr)
        kb = round(os.path.getsize(dst) / 1024)
    else:
        kb = 0
    n = z - a + 1
    docs.append({"p": rel, "t": t, "g": group_of(c), "tags": tags_of(c), "no": c, "kb": kb,
                 "src": f"Book {b} · trang {a}" + (f"–{z} ({n} tr.)" if n > 1 else ""), "bp": book, "bpg": a})

# Hồ sơ kiểm tra (Inspection book, cuốn 7–10) và các cuốn gộp
for b in range(1, 11):
    t = {1: "Book 1 – Hướng dẫn lắp đặt, sổ tay vận hành & bảo dưỡng, phụ tùng, bản vẽ tổng thể",
         2: "Book 2 – Bản vẽ tổng thể, phần áp lực, đường ống", 3: "Book 3 – Giá đỡ ống, liner",
         4: "Book 4 – Vỏ lò, module, ống gió, cửa kiểm tra", 5: "Book 5 – Sàn thao tác, cầu thang, kết cấu vận chuyển",
         6: "Book 6 – Bộ tiêu âm, đầu đốt, damper/quạt, data sheet, thiết bị đo, BMS"}.get(b, f"Book {b} – Inspection book (hồ sơ kiểm tra chế tạo) vol. {b}")
    docs.append({"p": f"HRSG/BOOK{b}.pdf", "t": t, "g": G_IB if b >= 7 else "Bộ sách đầy đủ", "tags": [B], "no": "", "kb": 0,
                 "src": "Vendor Data Book SICES · 2098 MR 0161.01"})
json.dump(docs, open(os.path.join(HERE, "docs.json"), "w"), ensure_ascii=False, indent=0)
print(len(docs), "tài liệu HRSG")
