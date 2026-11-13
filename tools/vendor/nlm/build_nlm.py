#!/usr/bin/env python3
"""Danh mục tài liệu "Vendor Data/Nuoc lam mat" (Unit 33 – nước làm mát) -> docs.json cho build_vendor.py.

Đầu vào (cùng thư mục):
  listing.json          danh sách file (p: đường dẫn tương đối trong "Nuoc lam mat", s: byte)
  pk3001_outline.json   mục lục (bookmark) của "30-PK-3001 .../Vendor Data Book.PDF" -> tách theo mục
  p3001_sections.json   (tuỳ chọn) mục của sách bơm Worthington 30-P-3001A Vol.1-5 và 30-P-3001-BCD
                        [[khoá sách, trang đầu, trang cuối, tên mục], ...] (tìm trang phân cách màu + OCR)
Ra: docs.json  [{p, t, g, tags, no, src, kb, bp, bpg}]
Tách file (tuỳ chọn): python3 build_nlm.py <thư mục "Nuoc lam mat"> <thư mục ra>
  -> <ra>/Nuoc lam mat/Tach theo muc/<...>.pdf
"""
import json, os, re, subprocess, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
R = "Nuoc lam mat"
SPLIT = R + "/Tach theo muc"

G_DS = "Data sheet & tài liệu chính"
G_DW = "Bản vẽ chế tạo"
G_OM = "Vận hành & bảo dưỡng"
G_INS = "Thiết bị đo & điều khiển"
G_EL = "Điện & tủ điều khiển"
G_SP = "Phụ tùng"
G_TEST = "Chạy thử"
G_SUB = "Tài liệu nhà sản xuất phụ kiện"
G_PIPE = "Đường ống & giá đỡ"
G_GEN = "Tổng quát, móng & lắp dựng"
G_SYS = "Hệ thống nước làm mát (P&ID, PFD, mô tả công nghệ)"
G_RV = "Dự án cải tạo 2016–2017 (Revamp)"
G_MR = "Đơn hàng & yêu cầu kỹ thuật (MR/SR)"
G_EV = "Sự cố & trao đổi"
G_BOOK = "Bộ sách đầy đủ"

LIST = json.load(open(os.path.join(HERE, "listing.json")))
SKIP_EXT = (".dwg", ".dwl", ".dwl2", ".db", ".bak", ".log", ".txt", ".rar")


def rng(prefix, letters):
    return [prefix + c for c in letters]


# cả cụm: gắn vào mã gốc, web tự hiện cho 30-CT-3001A..J (parentKeys bỏ chữ cuối)
CT = ["30-CT-3001"]
CTKL = ["30-CT-3001K", "30-CT-3001L"]
EX = ["30-E-3001"]
P1 = ["30-P-3001"]
P2 = ["30-P-3002"]
# tài liệu chung của hệ thống: gắn vào các cụm chính (tháp, bơm nước tuần hoàn)
SYS = ["30-CT-3001", "30-P-3001", "30-P-3002"]

# ---------- bỏ trùng: cùng tên file + cùng kích thước -> giữ bản ở thư mục "chính" ----------
PREF_LAST = ("MR 0910 54 (Amage)", "30-P-3001A/", "30-PK-3001 (MR-4046.50-51)/VENDOR DATA BOOK/",
             "30-P-3002ABC/30-P-3002 (MR-0910-54)/")


def rank(p):
    return sum(1 for x in PREF_LAST if p.startswith(x))


def base_key(p):
    b = p.rsplit("/", 1)[-1]
    b = re.sub(r"steam tur\.pdf$|steam turbine\.pdf$", "steam turbine", b)
    b = re.sub(r"for pu\.pdf$|for pump\.pdf$", "for pump", b)
    return b


seen, files = {}, []
for x in sorted(LIST, key=lambda x: (rank(x["p"]), x["p"])):
    p = x["p"]
    if p.lower().endswith(SKIP_EXT) or "/~$" in p or "desktop d" in p.lower():
        continue
    k = (base_key(p), x["s"])
    if k in seen:
        continue
    seen[k] = p
    files.append(x)

KHC = {200: "Bố trí chung – hình chiếu cạnh", 201: "Số liệu tải trọng", 202: "Mặt đứng", 203: 'Mặt bằng "1-1"',
       204: 'Mặt bằng "2-2"', 205: 'Mặt bằng "3-3"', 206: 'Mặt bằng "4-4"', 207: 'Mặt bằng "5-5"',
       208: 'Mặt cắt "10-10"', 209: 'Mặt cắt "11-11"', 210: 'Mặt bằng "12-12"', 211: 'Mặt bằng "13-13"',
       212: 'Mặt cắt "14-14"', 213: "Chi tiết chôn sẵn (embedded part)", 300: "Phần cơ khí (giá đỡ quạt, motor, hộp số)",
       301: "Đường dầu bôi trơn", 302: "Che chắn khớp nối / trục, giá đỡ ống", 303: "Ống loe quạt (fan stack)",
       304: "Bộ tách giọt (drift eliminator)", 305: "Chi tiết bộ tách giọt", 306: "Hệ thống phân phối nước",
       307: "Chi tiết hệ thống phân phối nước", 308: "Cụm vòi phun", 309: "Lắp đặt khối đệm (infill)",
       310: "Chi tiết khối đệm (infill)", 311: "Ống thử ăn mòn (corrosion coupon)", 312: "Lưới chắn bể (dual basin screen)",
       313: "Cẩu davit & palăng"}
CTDOC = {"003Ctdata172": ("Data sheet tháp giải nhiệt", G_DS), "004Perfcurva172": ("Đường cong hiệu suất tháp", G_DS),
         "005Svendor172": ("Danh sách nhà thầu phụ", G_MR), "006Fan(Drawing)": ("Bản vẽ quạt (Cofimco)", G_DW),
         "006Fan172": ("Data sheet quạt", G_DS), "007SR(drawing)": ("Bản vẽ hộp giảm tốc", G_DW),
         "007Srdata172": ("Data sheet hộp giảm tốc", G_DS), "008MtConn": ("Sơ đồ đấu dây motor quạt (Siemens)", G_EL),
         "008Mtcurve": ("Đặc tính motor quạt 150 kW (tiếng Đức)", G_EL), "008Mtdata172": ("Data sheet motor quạt", G_EL),
         "008MtTHERMAL_LIMIT_CURVE": ("Đường cong giới hạn nhiệt motor quạt", G_EL),
         "009Sftdata172": ("Data sheet trục truyền động", G_DS), "009Shaft": ("Thông số khớp nối / trục truyền động", G_DW),
         "010Vib": ("Sơ đồ công tắc rung", G_INS), "010Vibdata172": ("Data sheet công tắc rung", G_INS),
         "011spareE172": ("Phụ tùng lắp đặt & chạy thử", G_SP), "012SpareO172": ("Phụ tùng 2 năm vận hành", G_SP),
         "013Special172": ("Dụng cụ chuyên dùng", G_SP), "014Lublist172": ("Danh mục dầu mỡ bôi trơn", G_OM),
         "015Paintsp172": ("Quy cách sơn", G_GEN), "016Perf172": ("Bảng tính hiệu suất tháp", G_DS),
         "017Qplan172": ("Kế hoạch chất lượng (Quality plan)", G_TEST), "018Erection172": ("Hướng dẫn lắp dựng", G_GEN),
         "019Itpsite": ("Kế hoạch kiểm tra & thử tại công trường (ITP)", G_TEST),
         "020Comm172": ("Quy trình chạy thử (commissioning)", G_TEST),
         "021OmmAtt1(Fan)": ("Hướng dẫn lắp đặt, vận hành, bảo dưỡng quạt Cofimco", G_OM),
         "021OmmAtt2(Reducer)": ("Hướng dẫn bảo dưỡng hộp số Paramax (Sumitomo)", G_OM),
         "021OMMatt3(Motor)": ("Hướng dẫn vận hành motor Siemens 1LG4/1LG6", G_OM),
         "021OmmAtt5(VibSW)": ("Hướng dẫn lắp đặt công tắc rung Murphy VS2", G_OM),
         "021Oper172": ("Hướng dẫn vận hành tháp giải nhiệt", G_OM),
         "30-CT-3001A-J (1)": ("Data sheet phụ kiện hộp giảm tốc (KHC172-DD-007)", G_DS)}
PKDWG = {"0716": ("Bố trí cụm châm hóa chất chống cáu cặn 30-PK-3002", G_DW, ["30-PK-3002"]),
         "0717": ("Bố trí cụm châm hóa chất ức chế ăn mòn 30-PK-3003", G_DW, ["30-PK-3003"]),
         "0746": ("Tủ điều khiển tại chỗ 30-PK-3002 – mặt trước", G_EL, ["30-PK-3002"]),
         "0746-1": ("Tủ điều khiển 30-PK-3002 – danh mục thiết bị điện", G_EL, ["30-PK-3002"]),
         "0747": ("Tủ điều khiển tại chỗ 30-PK-3003 – mặt trước", G_EL, ["30-PK-3003"]),
         "0747-1": ("Tủ điều khiển 30-PK-3003 – danh mục thiết bị điện", G_EL, ["30-PK-3003"]),
         "0748": ("Sơ đồ nguyên lý điện 30-PK-3002 (động lực)", G_EL, ["30-PK-3002"]),
         "0749": ("Sơ đồ nguyên lý điện 30-PK-3002 (điều khiển)", G_EL, ["30-PK-3002"]),
         "0750": ("Sơ đồ nguyên lý điện 30-PK-3003 (động lực)", G_EL, ["30-PK-3003"]),
         "0751": ("Sơ đồ nguyên lý điện 30-PK-3003 (điều khiển)", G_EL, ["30-PK-3003"]),
         "1110": ("P&ID cụm châm hóa chất chống cáu cặn 30-PK-3002", G_DW, ["30-PK-3002"]),
         "1111": ("P&ID cụm châm hóa chất ức chế ăn mòn 30-PK-3003", G_DW, ["30-PK-3003"]),
         "30-PK-3002": ("Bản vẽ 30-PK-3002", G_DW, ["30-PK-3002"]), "30-PK-3003": ("Bản vẽ 30-PK-3003", G_DW, ["30-PK-3003"])}
PKDOC = {"Check list-3002": ("Check list 30-PK-3002", G_TEST, ["30-PK-3002"]),
         "Check list-3003": ("Check list 30-PK-3003", G_TEST, ["30-PK-3003"]),
         "Start-up-3002": ("Quy trình khởi động 30-PK-3002", G_OM, ["30-PK-3002"]),
         "Start-up-3003": ("Quy trình khởi động 30-PK-3003", G_OM, ["30-PK-3003"]),
         "Panel List-3002": ("Danh mục tủ điện 30-PK-3002", G_EL, ["30-PK-3002"]),
         "Panel List-3003": ("Danh mục tủ điện 30-PK-3003", G_EL, ["30-PK-3003"]),
         "ChemList & Calculation": ("Danh mục & tính toán hóa chất", G_DS, None), "CorrshieldMD4100": ("Hóa chất Corrshield MD4100 (ức chế ăn mòn)", G_SUB, ["30-PK-3003"]),
         "Data sheet_B": ("Data sheet cụm châm hóa chất", G_DS, None), "INSPECTION": ("Hồ sơ kiểm tra", G_TEST, None),
         "INSTRUMENT": ("Danh mục thiết bị đo", G_INS, None), "interlock": ("Liên động (interlock)", G_INS, None),
         "Lubricants": ("Danh mục dầu mỡ bôi trơn", G_OM, None), "Motor": ("Tài liệu motor bơm định lượng", G_EL, None),
         "PROCESS": ("Mô tả công nghệ cụm châm hóa chất", G_DS, None), "Pump Catalogue": ("Catalogue bơm định lượng", G_SUB, None),
         "Pump data sheet": ("Data sheet bơm định lượng", G_DS, None), "PUMP DIMENSION": ("Kích thước bơm định lượng", G_DW, None),
         "Pump peformance": ("Đặc tính bơm định lượng", G_DS, None), "Pump spare part": ("Phụ tùng bơm định lượng", G_SP, None),
         "SCALETROL PDC9325": ("Hóa chất Scaletrol PDC9325 (chống cáu cặn)", G_SUB, ["30-PK-3002"]),
         "Spare part": ("Danh mục phụ tùng", G_SP, None), "SpectrusNX1100": ("Hóa chất Spectrus NX1100 (diệt khuẩn)", G_SUB, None),
         "Subvendor": ("Danh sách nhà thầu phụ", G_MR, None), "Utility": ("Tiêu thụ phụ trợ", G_DS, None),
         "BA_DUO_001_08_02_GB": ("Hướng dẫn vận hành bơm định lượng (BA DUO)", G_OM, None),
         "OM_11_00_DHV_RM_English": ("Hướng dẫn van an toàn / van giữ áp DHV-RM", G_OM, None)}
REVT = {  # Revamp: Doc. Title đọc từ trang bìa
    "2539-0310-01-A0106-001": "Quy cách sơn", "2539-0310-01-A0201-001": "Mặt bằng & mặt đứng",
    "2539-0310-01-A1001-001": "Data sheet thiết bị", "2539-0310-01-A1101-002": "Bản vẽ lắp & dữ liệu trục truyền động",
    "2539-0310-01-A1109-001": "Chi tiết ống loe quạt (fan stack)", "2539-0310-01-A1109-002": "Chi tiết hệ phân phối & vòi phun",
    "2539-0310-01-A1109-003": "Chi tiết khối đệm (fill grid)", "2539-0310-01-A1109-004": "Chi tiết bộ tách giọt",
    "2539-0310-01-A1109-005": "Chi tiết hệ thống dầu bôi trơn", "2539-0310-01-A1109-006": "Chi tiết công tắc rung",
    "2539-0310-01-A1109-007": "Chi tiết giá đỡ cơ khí", "2539-0310-01-A1109-008": "Chi tiết lan can sàn trên",
    "2539-0310-01-A1109-009": "Chi tiết lan can cầu thang", "2539-0310-01-A1109-010": "Chi tiết lối đi bên trong",
    "2539-0310-01-A1109-011": "Chi tiết lưới chắn rác", "2539-0310-01-A2001-001": "Bản vẽ bố trí chung (GA)",
    "2539-0310-01-A3006-001": "Gói thiết bị đo", "2539-0310-01-A4102-001": "Data sheet motor điện",
    "2539-0310-01-A5015-001": "Hướng dẫn lắp đặt, vận hành, bảo dưỡng (IOM)", "2539-0310-01-B1202-001": "Quy trình NDT",
    "2539-0910-01-A1001-001": "Data sheet bơm", "2539-0910-01-A2001-001": "Bản vẽ bố trí chung (GA) bơm",
    "2539-0910-01-A5015-001": "Hướng dẫn lắp đặt, vận hành, bảo dưỡng (IOM) bơm",
    "2539-0848-01-A1001-001": "Data sheet bộ lọc", "2539-0848-01-A1001-002": "Data sheet thiết bị cụm lọc (A1001-002)", "2539-0848-01-A1001-003": "Data sheet (A1001-003)",
    "2539-0848-01-A1109-002": "Bản đồ mối hàn NDT bộ lọc", "2539-0848-01-A1112-001": "Bản vẽ nhãn thiết bị",
    "2539-0848-01-A1112-002": "Bản vẽ nhãn thiết bị (A1112-002)", "2539-0848-01-A2001-001": "Mặt bằng đường ống & thiết bị",
    "2539-0848-01-A2001-002": "Bản vẽ bố trí chung bộ lọc", "2539-0848-01-A3006-003": "Vị trí & chi tiết lắp đặt thiết bị đo",
    "2539-0848-01-A5016-001": "Hướng dẫn vận hành cụm lọc", "2539-0848-01-A0101-001": "Triết lý điều khiển cụm lọc 30-PK-3006"}
REVG = {"A01": G_DS, "A10": G_DS, "A11": G_DW, "A20": G_DW, "A30": G_INS, "A41": G_EL, "A50": G_OM, "B12": G_TEST, "A02": G_DW}

docs = []


def add(p, t, g, tags, no="", src="", **kw):
    d = {"p": R + "/" + p, "t": t, "g": g, "tags": sorted(set(tags), key=tags.index), "no": no, "src": src, "kb": 0}
    d.update(kw)
    docs.append(d)


miss = []
for x in files:
    p = x["p"]
    fn = p.rsplit("/", 1)[-1]
    stem = fn.rsplit(".", 1)[0]
    ext = fn.rsplit(".", 1)[-1].upper()
    m = re.match(r"(\d\d\.\d\d\.\d{4})\)?\s*(.*)", fn.lstrip("("))
    if p.startswith("30-CT-3001 K/"):
        dt, rest = (m.group(1), m.group(2)) if m else ("", stem)
        add(p, "Email: " + rest.rsplit(".", 1)[0], G_EV, ["30-CT-3001K"], src=f"Outlook .msg · {dt}")
    elif p.startswith("30-CT-3001A-J"):
        mm = re.match(r"KHC-172-DD-(\d+)", stem)
        if mm:
            add(p, KHC.get(int(mm.group(1)), stem), G_DW, CT, no=stem, src="Hamon/KHC · MR 0311-50")
        elif stem in CTDOC:
            t, g = CTDOC[stem]
            add(p, t, g, CT, no=stem, src="MR 0311-50 · " + ext)
        else:
            miss.append(p)
    elif p.startswith("30-E-3001A-H"):
        t = {"Cover": "Bìa Vendor Data Book (Alfa Laval)", "Index": "Mục lục Vendor Data Book",
             "Tag 1": "Mục 1 – Danh mục tài liệu", "Tag 2": "Mục 2 – Mô tả công nghệ (không áp dụng)",
             "Tag 3": "Mục 3 – Data sheet thiết bị trao đổi nhiệt tấm", "Tag 4": "Mục 4 – Hướng dẫn lắp đặt, vận hành & bảo dưỡng",
             "Tag 5": "Mục 5 – Danh mục phụ tùng", "Tag 6": "Mục 6 – Tài liệu & bản vẽ"}[stem]
        g = {"Tag 3": G_DS, "Tag 4": G_OM, "Tag 5": G_SP, "Tag 6": G_DW}.get(stem, G_BOOK)
        add(p, t, g, EX, src="Alfa Laval · MR 0660-60")
    elif p.startswith("30-P-3001ABCD/Thông số chạy thử"):
        e = stem[-1]
        add(p, f"Bảng theo dõi độ rung, nhiệt độ khi chạy thử 30-P-3001{e}", G_TEST, ["30-P-3001" + e], src="Biểu mẫu nhà máy")
    elif p.startswith("30-P-3001ABCD/") and "Vol.5.3" in p:
        t = {"30-P-3001A~D1": ("Data sheet bơm 30-P-3001A~D (Excel)", G_DS, P1), "30-P-3002A~C1": ("Data sheet bơm 30-P-3002A~C (Excel)", G_DS, P2),
             "ITP-0910.54": ("Kế hoạch kiểm tra & thử (ITP)", G_TEST, P1 + P2), "MR-0910.54-App. Vendor": ("Danh sách nhà cung cấp được duyệt", G_MR, P1 + P2),
             "MR-0910.54-Signed Cover": ("Bìa MR 0910-54 (đã ký)", G_MR, P1 + P2), "MR-0910.54-Spare Part": ("Phụ tùng theo MR 0910-54", G_SP, P1 + P2),
             "00-MR-0910-54-0": ("Yêu cầu mua hàng (MR) bơm ly tâm mixed flow", G_MR, P1 + P2),
             "00-SR-0910-54-0": ("Phạm vi cung cấp (SR)", G_MR, P1 + P2), "00-VR-0910-54-0": ("Yêu cầu tài liệu nhà cung cấp (VR)", G_MR, P1 + P2)}
        if stem.startswith("33-PID-0031"):
            add(p, f"P&ID nước làm mát {stem}", G_SYS, SYS, no=stem, src="P&ID gốc (2098)")
        elif stem.startswith("CP Mixed flow"):
            kind = {"cover": "Bìa", "extent": "Phạm vi (SP)", "scope": "Phạm vi cung cấp (SR)"}.get(stem.split()[2].split("-")[0], "Yêu cầu tài liệu (VR)")
            add(p, f"{kind} – bơm mixed flow (Word)", G_MR, P1 + P2, no=stem)
        elif stem in t:
            a, g, tg = t[stem]
            add(p, a, g, tg, src="MR 0910-54")
        else:
            miss.append(p)
    elif p.startswith("30-P-3001ABCD/") and ("Vol.5.1/INDEX" in p or "Vol.5.2/INDEX" in p):
        continue  # trang mục lục điều hướng, không cần
    elif p.startswith("30-P-3001ABCD/") and p.endswith(".pdf") and "Manual" in p:
        b = "BCD" if "BCD" in stem else "A" + stem[-1]
        tg = rng("30-P-3001", "BCD") if b == "BCD" else ["30-P-3001A"]
        name = "Vendor Data Book bơm 30-P-3001B/C/D (Worthington, toàn bộ)" if b == "BCD" else f"Vendor Data Book bơm 30-P-3001A – Vol. {stem[-1]} (toàn bộ)"
        add(p, name, G_BOOK, tg, src="Worthington · 2002 SMS 10016" + ("61" if b == "BCD" else "51"), book=b)
    elif p.startswith("30-P-3002ABC/") or p.startswith("MR 0910 54"):
        mm = re.match(r"Vol\. (\d+) - (.*)", stem)
        vol, t = mm.group(1), mm.group(2)
        g = G_DS if "data sheet" in t.lower() else G_SP if "spare" in t.lower() else G_OM if re.search("manual|storage|Governor", t, re.I) else G_INS if "3500" in t else G_DW
        tg = P2 + (["30-STP-3002A"] if re.search("turbine|Governor|Gear|Lub", t, re.I) else [])
        add(p, t.replace("&", " & ").replace("  ", " ").strip(), g, tg, src=f"MR 0910-54 · Vol. {vol}")
    elif p.startswith("30-PK-3001 (MR-4046.50-51)/Vendor Data Book"):
        add(p, "Vendor Data Book 30-PK-3001 (toàn bộ, 984 tr.)", G_BOOK, ["30-PK-3001"], src="MR 4046.50-51", book="PK")
    elif "VENDOR DATA BOOK/DWG/" in p:
        t, g, tg = PKDWG[stem]
        add(p, t, g, tg, no=stem, src="MR 4046-50")
    elif "VENDOR DATA BOOK/" in p and p.startswith("30-PK-3002"):
        t, g, tg = PKDOC[stem]
        add(p, t + (" (" + ext.lower() + ")" if ext not in ("PDF",) else ""), g, tg or ["30-PK-3002", "30-PK-3003"], src="MR 4046-50")
    elif p.startswith("Revamp"):
        q = p[len("Revamp_COOLING WATER SYSTEM_revamp/"):]
        mm = re.search(r"(2539-\d{4}-01-[AB]\d{4}-\d{3})", stem)
        if mm and mm.group(1) in REVT:
            code = mm.group(1)
            tg = CTKL if "-0310-" in code else ["30-P-3001E"] if "-0910-" in code else ["30-PK-3006"]
            rev = re.search(r"_(\w+?)(?:_Code|\.|-C|$)", stem[len(code):] + ".")
            add(p, REVT[code] + (f" (rev {rev.group(1)})" if rev else ""), REVG.get(code.split("-")[3][:3], G_DW), tg, no=code, src="Revamp 2539 · vendor")
            continue
        if q.startswith("4. DATASHEET/"):
            eq = q.split("/")[1].replace(" ", "")
            tg = {"30-CT-3001K-L": CTKL, "30-FE-33104": ["30-FE-33104", "FE-33104"], "30-FV-33105": ["30-FV-33105", "FV-33105"]}.get(eq, [eq])
            what = {"30-BA-3003": "Data sheet bể 30-BA-3003", "30-BA-3004": "Data sheet bể 30-BA-3004 (bể lắng)",
                    "30-CT-3001K-L": "Data sheet tháp giải nhiệt cơ khí 30-CT-3001K/L", "30-FE-33104": "Data sheet lưu lượng kế 30-FE-33104",
                    "30-FV-33105": "Data sheet van điều khiển 30-FV-33105", "30-P-3001A": "Data sheet bơm 30-P-3001A (revamp)",
                    "30-P-3001E": "Data sheet bơm 30-P-3001E", "30-P-3002A": "Data sheet bơm 30-P-3002A (revamp)",
                    "30-PK-3006": "Yêu cầu kỹ thuật cụm lọc nước bổ sung 30-PK-3006"}[eq]
            if stem.startswith("T-T-P"):
                what = "Phiếu chuyển tài liệu " + stem
            add(p, what + ("" if ext == "PDF" else f" ({ext.lower()})"), G_DS, tg, no=stem, src="Revamp 2539")
        elif q.startswith("1. PROCESS"):
            add(p, "Mô tả công nghệ Unit 33 – hệ thống nước làm mát" + ("" if ext == "PDF" else f" ({ext.lower()})"), G_SYS, SYS, no=stem, src="Revamp 2539")
        elif q.startswith("2. PI&D/PDF/"):
            sh = re.search(r"PID-0031-(\d\d-\d\d)", stem).group(1)
            add(p, f"P&ID Unit 33 tờ {sh}" + (" (điểm tie-in)" if "Ties-in" in stem else ""), G_SYS, SYS, no=stem.split(" ")[0], src="Revamp 2539")
        elif q.startswith("3. "):
            if fn.lower().endswith(".png"):
                add(p, "Ảnh điểm tie-in " + stem, G_RV, SYS, src="Ties-in chuẩn bị đấu nối")
            else:
                add(p, "Danh sách các điểm tie-in Unit 33" if "Danh" in fn else "Tie-in nước làm mát (Word)", G_RV, SYS, src="Revamp 2539")
        elif q.startswith("5. Tài Liệu Tham Khảo/PID Scan/"):
            sh = re.search(r"PID-0031-(\d\d-\d\d)", stem).group(1)
            add(p, f"P&ID Unit 33 tờ {sh} (bản scan có ký)", G_SYS, SYS, no=stem, src="Revamp 2539 · scan")
        elif q.startswith("5. Tài Liệu Tham Khảo/PFD/"):
            sh = re.search(r"PFD-0010-(\d\d-\d\d)", stem).group(1)
            add(p, f"PFD Unit 33 tờ {sh}" + (" (scan)" if "Scan" in stem else ""), G_SYS, SYS, no=stem, src="Revamp 2539")
        elif q.startswith("5. Tài Liệu Tham Khảo/INTERLOCK"):
            t = "Mô tả liên động (interlock) Unit 33" if "CN-0009" in stem else "Danh sách liên động / cause & effect Unit 33"
            add(p, t + ("" if ext == "PDF" else f" ({ext.lower()})"), G_SYS, SYS, no=stem, src="Revamp 2539")
        elif "T-T-P-00850" in q:
            t = {"2539-00-DL-0848-01_0": "Danh mục tài liệu (DL)", "2539-00-ITP-0848-01_0": "Kế hoạch kiểm tra & thử (ITP)",
                 "2539-00-MR-0848-01_0": "Yêu cầu mua hàng (MR) cụm lọc", "2539-00-MR-0848-01-ATT-1_ COVER": "Phụ lục 1 – bìa",
                 "2539-00-MR-0848-01-ATT-1_0": "Phụ lục 1 – danh sách nhà cung cấp", "2539-00-MR-0848-01-ATT-2_ COVER": "Phụ lục 2 – bìa",
                 "2539-00-MR-0848-01-ATT-2_PackageDS _0": "Phụ lục 2 – data sheet cụm", "2539-00-SP-0848-01_0": "Yêu cầu kỹ thuật riêng (SP)",
                 "2539-00-SR-0848-01_0": "Phạm vi cung cấp (SR)", "2539-33-SP-0848-01_1": "Yêu cầu kỹ thuật Unit 33 (SP-01)",
                 "2539-33-SP-0848-02_1": "Yêu cầu kỹ thuật Unit 33 (SP-02, đã thay thế)", "T-T-P-00850": "Phiếu chuyển tài liệu T-T-P-00850"}[stem]
            add(p, t + ("" if ext == "PDF" else f" ({ext.lower()})"), G_MR, ["30-PK-3006"], no=stem, src="MR 0848-01 · Revamp")
        elif q.startswith("5. Tài Liệu Tham Khảo/03. Reference Engineering Document/"):
            t = {"3.PIPING GA": ("Mặt bằng đường ống & thiết bị – xử lý nước làm mát", G_PIPE, ["30-PK-3006"]),
                 "QP 0001 - 16 ALSD - Rev. 1": ("Ghi chú chung đường ống (QP 0001-16)", G_PIPE, ["30-PK-3006"]),
                 "IOM QL pump": ("Hướng dẫn Worthington bơm đứng QL/QLC", G_OM, ["30-P-3001E", "30-P-3001"]),
                 "2539-30-DW-0051-01-01_0": ("Mặt bằng bố trí Unit 30 (layout)", G_GEN, SYS)}[stem]
            add(p, t[0], t[1], t[2], no=stem, src="Revamp 2539")
        elif q.startswith("5. Tài Liệu Tham Khảo/"):
            t = {"2539-00-ML-950-01_0": ("Danh sách vật tư (ML-950)", G_RV), "2539-00-MS-0940-002_1": ("Quy trình (MS-0940-002)", G_RV),
                 "2539-0848-01-A0101-001_B_Code 1": ("Triết lý điều khiển cụm lọc 30-PK-3006", G_INS),
                 "2539-33-MSD-0011-01-01_A_SCAN": ("Sơ đồ MSD Unit 33 (scan)", G_SYS), "T-T-P-01659": ("Phiếu chuyển tài liệu T-T-P-01659", G_RV),
                 "T-T-P-01667": ("Phiếu chuyển tài liệu T-T-P-01667", G_RV)}.get(stem)
            if not t:
                miss.append(p); continue
            add(p, t[0] + ("" if ext == "PDF" else f" ({ext.lower()})"), t[1], ["30-PK-3006"] if "0848" in stem else SYS, no=stem, src="Revamp 2539")
        elif fn.startswith("G2-30-QT-045"):
            add(p, "Quy trình vận hành hệ thống nước sông làm mát (G2-30-QT-045)", G_OM, SYS, no="G2-30-QT-045", src="Quy trình nhà máy")
        elif fn.startswith("Ready for commissioning"):
            add(p, "Thông báo sẵn sàng chạy thử 30-PK-3006", G_TEST, ["30-PK-3006"], src="Revamp 2539")
        else:
            miss.append(p)
    else:
        miss.append(p)

# ---------- tách sách theo mục ----------


def safe(s):
    s = s.replace("đ", "d").replace("Đ", "D").replace("–", "-").replace("&", "and").replace('"', "")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r'[\\/:*?<>|;]+', " ", s)
    return re.sub(r"\s+", " ", s).strip()[:90]


SRC = sys.argv[1] if len(sys.argv) > 2 else None
OUT = sys.argv[2] if len(sys.argv) > 2 else None
parts = []  # (book file, from, to, title, group, tags, label)
PKB = "30-PK-3001 (MR-4046.50-51)/Vendor Data Book.PDF"
pk = json.load(open(os.path.join(HERE, "pk3001_outline.json")))
PKSUB = {"5.5.1": ["30-PK-3001/Z1B", "30-PK-3001/Z2B", "30-PK-3001/Z3"],
         "5.5.2": ["30-PK-3001/P1A", "30-PK-3001/P1B", "30-PK-3001/P1C", "30-PK-3001/P2", "30-PK-3001/P5A"],
         "5.5.3": ["30-PK-3001/F1A", "30-PK-3001/F1B"],
         "5.9.1": ["30-PK-3001/MP1A", "30-PK-3001/MP1B", "30-PK-3001/MP1C", "30-PK-3001/MP2", "30-PK-3001/MP5B", "30-PK-3001/MF1A", "30-PK-3001/MF1B"]}
for a, z, t, path, kind in pk["items"]:
    if t in ("Vendor Data Book", "Index") or (kind and z - a < 2):
        continue  # trang bìa / trang phân cách mục
    top = (path[0] if path else t)
    num = re.match(r"([\d.]+)", t)
    num = num.group(1).rstrip(".") if num else ""
    g = {"1.0": G_GEN, "2.0": G_GEN, "3.0": G_OM, "4.0": G_SP}.get(top.split(".")[0] + ".0", G_DW)
    if "5.7" in " ".join(path) or t.startswith("5.7"):
        g = G_INS
    elif "5.8" in " ".join(path) or "5.9" in " ".join(path) or "MCC" in t or "Single line" in t:
        g = G_EL
    elif "5.6" in " ".join(path) or "Piping" in t or "Line list" in t:
        g = G_PIPE
    elif t.startswith("5.5"):
        g = G_DS
    title = t + (" (phần chính)" if kind else "")
    if path and not t[0].isdigit():
        title = path[-1].split(" ", 1)[-1] + " – " + t
    tags = ["30-PK-3001"] + PKSUB.get(num, [])
    parts.append((PKB, a, z, title, g, tags, "30-PK-3001"))

secf = os.path.join(HERE, "p3001_sections.json")
BOOKS = {"A1": "30-P-3001ABCD/30-P-3001 (MR-0910-54) Vol.5.2/Specifiche/Manuali/30-P-3001A Vol. 1.pdf",
         "A2": "30-P-3001ABCD/30-P-3001 (MR-0910-54) Vol.5.2/Specifiche/Manuali/30-P-3001A Vol. 2.pdf",
         "A3": "30-P-3001ABCD/30-P-3001 (MR-0910-54) Vol.5.2/Specifiche/Manuali/30-P-3001A Vol. 3.pdf",
         "A4": "30-P-3001ABCD/30-P-3001 (MR-0910-54) Vol.5.2/Specifiche/Manuali/30-P-3001A Vol. 4.pdf",
         "A5": "30-P-3001ABCD/30-P-3001 (MR-0910-54) Vol.5.2/Specifiche/Manuali/30-P-3001A Vol. 5.pdf",
         "BCD": "30-P-3001ABCD/30-P-3001 (MR-0910-54) Vol.5.1/Specifiche/Manuale/30-P-3001-BCD.pdf"}
if os.path.exists(secf):
    for b, a, z, t, g in json.load(open(secf)):
        tg = ["30-P-3001A"] if b != "BCD" else ["30-P-3001B", "30-P-3001C", "30-P-3001D"]
        if re.search(r"turbin|governor", t, re.I):
            tg = tg + (["30-STP-3001A"] if b != "BCD" else [])
        parts.append((BOOKS[b], a, z, t, g, tg, "30-P-3001A Vol." + b[1] if b != "BCD" else "30-P-3001B/C/D"))

for book, a, z, t, g, tags, lab in parts:
    name = safe(f"{lab} - {t}") + ".pdf"
    sub = "30-PK-3001" if lab == "30-PK-3001" else "30-P-3001"
    rel = f"{SPLIT}/{sub}/{name}"
    kb = 0
    if OUT:
        dst = os.path.join(OUT, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if not os.path.exists(dst):
            r = subprocess.run(["qpdf", os.path.join(SRC, book), "--pages", ".", f"{a}-{z}", "--", dst], capture_output=True, text=True)
            if r.returncode not in (0, 3):
                raise SystemExit(r.stderr)
        kb = round(os.path.getsize(dst) / 1024)
    n = z - a + 1
    docs.append({"p": rel, "t": t if lab == "30-PK-3001" else t, "g": g, "tags": tags, "no": "", "kb": kb,
                 "src": f"{lab} · trang {a}" + (f"–{z} ({n} tr.)" if n > 1 else ""), "bp": R + "/" + book, "bpg": a})

for d in docs:
    d.pop("book", None)
SIZES = {R + "/" + x["p"]: x["s"] for x in LIST}
json.dump(docs, open(os.path.join(HERE, "docs.json"), "w"), ensure_ascii=False, indent=0)
json.dump([[k, v] for k, v in SIZES.items()], open(os.path.join(HERE, "sizes.json"), "w"), ensure_ascii=False)
print(len(docs), "tài liệu nước làm mát;", len(parts), "mục tách")
if miss:
    print("CHƯA XẾP:", *miss, sep="\n  ")
