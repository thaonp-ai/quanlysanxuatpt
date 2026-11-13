#!/usr/bin/env python3
"""Danh mục "Vendor Data/7. Air System" (Unit 35 – khí nén) -> docs.json + sizes.json.

Đầu vào: listing.txt (đường dẫn | byte; đã bỏ .dwg, Thumbs.db, file log) và databook_sections.json
(mục của "3. 30-K-5001/data book.pdf" – Atlas Copco ZR200, 269 trang scan; tìm trang bìa bằng OCR).
File tách theo tài liệu nằm ở OneDrive "7. Air System/3. 30-K-5001/Tach theo tai lieu/".
Tách lại: python3 build_air.py <thư mục "7. Air System"> <thư mục ra>
"""
import json, os, re, subprocess, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
R = "7. Air System"
SPLIT = "3. 30-K-5001/Tach theo tai lieu"

G = {"ds": "Data sheet & tài liệu chính", "dw": "Bản vẽ chế tạo", "om": "Vận hành & bảo dưỡng", "ins": "Thiết bị đo & điều khiển",
     "el": "Điện & tủ điều khiển", "sp": "Phụ tùng", "test": "Chạy thử", "gen": "Tổng quát, móng & lắp dựng",
     "mr": "Đơn hàng & yêu cầu kỹ thuật (MR/SR)", "sys": "Hệ thống (P&ID, mô tả công nghệ)", "rev": "Dự án cải tạo 2016–2017 (Revamp)",
     "inc": "Sự cố & trao đổi", "book": "Bộ sách đầy đủ"}

KAD = ["30-K-5001", "30-K-5001A", "30-K-5001B", "30-K-5001C", "30-K-5001D"]
KE = ["30-K-5001", "30-K-5001E"]
D1, D2 = ["30-DR-5001"], ["30-DR-5002"]
SYS = ["30-K-5001", "30-V-5001", "30-V-5002", "30-DR-5001", "30-DR-5002"]

# tài liệu vendor revamp (mã tài liệu Technip 2539-<MR>-01-<code>) – tên lấy từ trang bìa
VDOC = {
    "4171": {"A0001": ("Danh mục tài liệu & bản vẽ nhà cung cấp", "mr"), "A0103": ("P&ID cụm máy sấy", "sys"),
             "A1001": ("Data sheet cụm máy sấy", "ds"), "A1003": ("Tính toán kết cấu skid", "gen"), "A1014": ("Danh mục phụ trợ (utility list)", "ds"),
             "A1103": ("Bản vẽ chế tạo bình áp lực (tháp hấp phụ)", "dw"), "A1112": ("Bản vẽ nhãn thiết bị", "dw"),
             "A2001": ("Bản vẽ bố trí chung (GA)", "dw"), "A2003": ("Danh mục vật tư mua ngoài", "mr"), "A2006": ("Bản vẽ chi tiết kết cấu", "dw"),
             "A3006-002": ("Data sheet thiết bị đo", "ins"), "A3006-003": ("Sơ đồ lắp đặt thiết bị đo (hook-up)", "ins"),
             "A3007": ("Lịch cáp thiết bị đo", "ins"), "A3008-001": ("Danh mục I/O", "ins"), "A3008-002": ("Cause & Effect", "ins"),
             "A3204": ("Bản vẽ bố trí tủ điều khiển", "el"), "A4211": ("Sơ đồ đấu dây", "el"), "A5015": ("Quy trình lắp đặt, khởi động & chạy thử", "test"),
             "A5016": ("Hướng dẫn vận hành & bảo dưỡng", "om"), "B1002": ("Kế hoạch kiểm tra & thử (ITP)", "test"),
             "B1103-001": ("Quy trình thử thủy lực", "test"), "B1103-002": ("Quy trình thử nghiệm tại xưởng (FAT)", "test"),
             "B1202-001": ("Hồ sơ B1202-001 (chứng chỉ chế tạo)", "test"), "B1202-002": ("Chứng chỉ thợ NDE (skid & ống)", "test"),
             "B1304": ("WPS & PQR (skid & ống)", "test")},
    "1031": {"A0001": ("Danh mục tài liệu & bản vẽ nhà cung cấp", "mr"), "A0103": ("P&ID cụm máy nén", "sys"),
             "A1001": ("Data sheet cụm máy nén", "ds"), "A1003": ("Tính toán chọn van an toàn", "ds"), "A1112": ("Bản vẽ nhãn thiết bị", "dw"),
             "A2001": ("Bản vẽ bố trí chung (GA)", "dw"), "A3006-002": ("Data sheet thiết bị đo", "ins"),
             "A3006-003": ("Sơ đồ lắp đặt thiết bị đo (hook-up)", "ins"), "A3007": ("Lịch cáp thiết bị đo", "ins"),
             "A4102": ("Data sheet động cơ điện", "el"), "A5015": ("Quy trình lắp đặt, khởi động & chạy thử", "test"),
             "A5016": ("Hướng dẫn vận hành & bảo dưỡng", "om"), "B1002": ("Kế hoạch kiểm tra & thử (ITP)", "test")},
}

docs, sizes = [], []


def add(p, t, g, tags, no="", src=""):
    docs.append({"p": R + "/" + p, "t": t, "g": G[g], "tags": tags, "no": no, "src": src, "kb": 0})


def asc(s):
    s = unicodedata.normalize("NFD", s.replace("đ", "d").replace("Đ", "D"))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^A-Za-z0-9 &().,-]", "", s).strip()


SECS = json.load(open(os.path.join(HERE, "databook_sections.json")))
SPLITNAMES = [f"{i:02d} - {c} - {asc(t)}.pdf" for i, (c, t, a, b, g) in enumerate(SECS, 1)]

if len(sys.argv) == 3:                        # tách lại data book
    src = os.path.join(sys.argv[1], "3. 30-K-5001", "data book.pdf")
    os.makedirs(sys.argv[2], exist_ok=True)
    for fn, (c, t, a, b, g) in zip(SPLITNAMES, SECS):
        subprocess.run(["qpdf", "--empty", "--pages", src, f"{a}-{b}", "--", os.path.join(sys.argv[2], fn)], check=True)
    print("đã tách", len(SECS), "file")

for line in open(os.path.join(HERE, "listing.txt"), encoding="utf-8"):
    line = line.strip()
    if not line:
        continue
    p, sz = line.rsplit("|", 1)
    sizes.append([R + "/" + p, int(sz)])
    fn = p.rsplit("/", 1)[-1]
    stem, ext = fn.rsplit(".", 1)
    ext = ext.lower()
    m = re.match(r"2539-(\d{4})-01-([AB]\d{4})-(\d{3})_([0-9A-Z]+)", fn)
    if m:
        mr, code, ser, rev = m.groups()
        d = VDOC[mr]
        k = f"{code}-{ser}" if f"{code}-{ser}" in d else code
        t, g = d[k]
        who = "máy sấy 30-DR-5002" if mr == "4171" else "máy nén 30-K-5001E"
        ref = "Tài Liệu Tham Khảo" in p
        add(p, f"{t} – {who} (rev {rev})", g, D2 if mr == "4171" else KE, no=f"2539-{mr}-01-{code}-{ser}",
            src=("Revamp · tài liệu tham khảo" if ref else "Revamp · mô tả công nghệ") + (" · MR 2539-00-MR-4171-01" if mr == "4171" else " · MR 2539-00-MR-1031-01"))
        continue
    if fn.startswith("30-K-5001A_D"):
        add(p, "Data sheet máy nén 30-K-5001A–D (Atlas Copco ZR200) & máy sấy 30-DR-5001 (Delair PDH-0716)", "ds", KAD + D1,
            no="2098-30-SP-1031-01 / SP-4171", src="Dự án gốc 2098")
    elif fn.startswith("Theo dõi máy nén"):
        add(p, "Theo dõi vận hành máy nén 30-K-5001A–E 2023–2024 (xlsx)", "om", KAD + KE[1:], src="Xưởng Phụ trợ")
    elif "CN-0009" in fn:
        add(p, f"Mô tả công nghệ Unit 35 (revamp) – 2539-35-CN-0009-01 ({ext})", "sys", SYS, no="2539-35-CN-0009-01", src="Revamp 2539")
    elif fn.startswith("Unit 30-Air Compression"):
        add(p, "Mô tả công nghệ hệ thống khí nén (tiếng Việt, docx)", "sys", SYS, src="Xưởng Phụ trợ")
    elif p.startswith("2. PI&D/") or "/PI&D Scan/" in p:
        dwg = re.search(r"2539-35-PID-0031-0\d-01", fn).group(0)
        n = dwg[-4]
        what = {"3": "bình chứa & máy sấy (revamp)", "5": "máy nén 30-K-5001E (mới)", "6": "máy sấy 30-DR-5002 (mới)"}[n]
        tags = {"3": ["30-V-5001", "30-V-5002", "30-DR-5001", "30-DR-5002"], "5": KE, "6": D2}[n]
        add(p, f"P&ID {dwg[:-3]} – {what}" + (" – điểm tie-in" if "Ties" in fn else " (bản scan rev 0)" if "Scan" in fn else " rev 0"),
            "rev", tags, no=dwg, src="Revamp 2539")
    elif fn.startswith("2539-35-SP-4171") or fn.startswith("2539-35-SP-1031"):
        dr = "4171" in fn
        add(p, f"Data sheet {'máy sấy 30-DR-5002' if dr else 'máy nén 30-K-5001E'} – {stem.split('_')[0]} rev {stem.split('_')[1]} ({ext})",
            "ds", D2 if dr else KE, no=stem.split("_")[0], src="Revamp 2539")
    elif re.match(r"(PVFCC0_)?T-T-P-003(09|14)", fn):
        dr = "00309" in fn
        add(p, f"Phiếu chuyển tài liệu T-T-P-{'00309' if dr else '00314'} ({ext})", "mr", D2 if dr else KE, src="Revamp 2539")
    elif "MSD-0011" in fn:
        add(p, "2539-35-MSD-0011-01-01 (scan)", "rev", SYS, no="2539-35-MSD-0011-01-01", src="Revamp 2539")
    elif "DW-0051" in fn:
        add(p, "Bản vẽ tham chiếu 2539-30-DW-0051-01-01", "rev", SYS, no="2539-30-DW-0051-01-01", src="Revamp 2539")
    elif "/PFD/" in p:
        add(p, "PFD 2539-35-PFD-0010-01-01 rev 0" + (" (bản scan)" if "Scan" in fn else ""), "rev", SYS, no="2539-35-PFD-0010-01-01", src="Revamp 2539")
    elif "/HAZOP Documentation/" in p:
        t = {"2539-35-PID-0031-03-01_C": ("P&ID 2539-35-PID-0031-03 rev C (hồ sơ HAZOP)", SYS),
             "Air compressor_GA_VDB_0": ("Bản vẽ GA máy nén 30-K-5001E (hồ sơ HAZOP)", KE),
             "Air compressor_PID_VDB_B": ("P&ID vendor máy nén 30-K-5001E rev B (hồ sơ HAZOP)", KE),
             "Air dryer_GA_VDB_A-C": ("Bản vẽ GA máy sấy 30-DR-5002 (hồ sơ HAZOP)", D2),
             "Air dryer_PID_VDB_B": ("P&ID vendor máy sấy 30-DR-5002 rev B (hồ sơ HAZOP)", D2)}
        k = next(k for k in t if stem.startswith(k))
        add(p, t[k][0], "rev", t[k][1], src="HAZOP revamp")
    elif p.startswith("3. 30-K-5001/data book"):
        add(p, "Vendor data book máy nén 30-K-5001A–D – Atlas Copco (bản gộp 269 trang)", "book", KAD, no="AC-7189", src="Atlas Copco · MR 2098-00-MR-1031-50")
    else:
        raise SystemExit("chưa xếp: " + p)

# file tách theo tài liệu của data book
SS = json.load(open(os.path.join(HERE, "split_sizes.json")))
for fn, (c, t, a, b, g) in zip(SPLITNAMES, SECS):
    p = SPLIT + "/" + fn
    sizes.append([R + "/" + p, SS.get(fn, 0)])
    d = {"p": R + "/" + p, "t": t, "g": G[g], "tags": KAD, "no": "" if c == "IO" else f"AC-7189-{c}",
         "src": "Atlas Copco ZR200 · MR 2098-00-MR-1031-50", "kb": 0, "bp": R + "/3. 30-K-5001/data book.pdf", "bpg": a}
    docs.append(d)

json.dump(docs, open(os.path.join(HERE, "docs.json"), "w"), ensure_ascii=False, indent=0)
json.dump(sizes, open(os.path.join(HERE, "sizes.json"), "w"), ensure_ascii=False)
print(len(docs), "tài liệu Air System")
