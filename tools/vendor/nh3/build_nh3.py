#!/usr/bin/env python3
"""Danh mục "Vendor Data/6. Bon chua amonia & Flare" (Unit 45 kho NH3, Unit 41 đuốc) -> docs.json + sizes.json.

Đầu vào: listing.txt (đường dẫn|byte). Đã bỏ: ảnh/video (Hinh 40…, Hình ảnh…, IMG…, .mov/.mp4), .dwg, .rar/.zip,
thư mục "Revamp/5. Tài Liệu Tham Khảo/…/New folder" (file cá nhân nhà thầu), ".../Superseded" (bản cũ),
"40-PK-1001-1002/old" (trùng), file tạm ~$.
flare_contents.csv = mục lục CD vendor đuốc (#Contents_CD.xls) → tên bản vẽ 2098-01850-Dxxx/Sxxx.
Tên tài liệu bồn 40-TK-5001 (L002xx) lấy từ trang bìa .xls/.doc; tài liệu revamp 2539-<MR>-… lấy từ trang bìa PDF.
"""
import csv, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
R = "6. Bon chua amonia & Flare"

G = {"ds": "Data sheet & tài liệu chính", "dw": "Bản vẽ chế tạo", "om": "Vận hành & bảo dưỡng", "ins": "Thiết bị đo & điều khiển",
     "el": "Điện & tủ điều khiển", "sp": "Phụ tùng", "test": "Chạy thử", "gen": "Tổng quát, móng & lắp dựng", "pipe": "Đường ống & giá đỡ",
     "mr": "Đơn hàng & yêu cầu kỹ thuật (MR/SR)", "sys": "Hệ thống (P&ID, mô tả công nghệ)", "rev": "Dự án cải tạo 2016–2017 (Revamp)",
     "inc": "Sự cố & trao đổi", "ref": "Tài liệu tham khảo", "book": "Bộ sách đầy đủ", "plat": "Sàn thao tác & cầu thang"}

TK, PK1, PK5 = "40-TK-5001", "40-PK-5001", "40-PK-5005"
P1, P2, P3 = "40-P-5001", "40-P-5002", "40-P-5003"
E1, E2 = "40-E-5001", "40-E-5002"
FA, FS, LP, KO = "40-PK-1001", "40-PK-1002", "20-PK-1005", "40-V-1001"
LA = ["40-LA-5003", "40-LA-5004", "40-LA-5005", "40-LA-5006"]
MP = ["40-PK-5003", "40-PK-5004"]
U45 = [TK, PK1, PK5, P1, P2, P3, E1, E2]

docs, sizes = [], []


def add(p, t, g, tags, no="", src=""):
    docs.append({"p": R + "/" + p, "t": t, "g": G[g], "tags": list(dict.fromkeys(tags)), "no": no, "src": src, "kb": 0})


def pk5_sub(low):
    """tag con cụm làm lạnh mới 40-PK-5005 theo tên tài liệu"""
    t = [PK5]
    for k, v in (("condenser", ["/E1"]), ("subcooler", ["/V1"]), ("receiver", ["/V2"]), ("oil separator", ["/V3A", "/V3B"]),
                 ("oil distiller", ["/V4"]), ("oil filter", ["/FL1A", "/FL1B"]), ("oil pump", ["/P1A", "/P1B", "/MP1A", "/MP1B"]),
                 ("compressor", ["/K1A", "/K1B"]), ("motor", ["/MK1A", "/MK1B"])):
        if k in low:
            t += [PK5 + x for x in v]
    for x in ("V3A", "V3B", "FL1A", "FL1B"):
        if x.lower() in low:
            t.append(PK5 + "/" + x)
    return t


# ---- tên tài liệu ----
FLARE = {}
for row in csv.reader(open(os.path.join(HERE, "flare_contents.csv"), encoding="utf-8", errors="replace")):
    if len(row) >= 5 and row[3].startswith("2098-01850"):
        FLARE[row[3].rsplit(".", 1)[0].upper()] = row[4].strip()
VI = [("P & I  DIAGRAM FOR", "P&ID"), ("G.A. DRAWING FOR", "Bản vẽ GA"), ("LOADING & ANCHOR PLAN", "Tải trọng & bu lông neo"),
      ("FLARE TIP ASSEMBLY", "Đầu đuốc (flare tip)"), ("RISER ENG'G DWG FOR", "Ống đứng (riser)"), ("PLATFORM ASSEMBLY & DETAILS", "Sàn thao tác"),
      ("LADDER ASSEMBLY & DETAILS", "Cầu thang"), ("PIPING ARRANGEMENT", "Bố trí đường ống"), ("PIPING SUPPORT DETAILS", "Giá đỡ ống"),
      ("PIPING SPOOL DRAWING", "Spool ống"), ("F.F.G. SKID  G.A. DRAWING FOR", "Skid đánh lửa (FFG) –"),
      ("CONTROL PANEL OF F.F.G. FOR", "Tủ điều khiển đánh lửa (FFG) –"), ("WIRING DIAGRAM OF F.F.G. FOR", "Sơ đồ đấu dây FFG –"),
      ("THERMOCOUPLE WIRING ARRANGEMENT FOR", "Đấu dây cặp nhiệt –"), ("RADIATION  SHIELD", "tấm chắn bức xạ"), ("RAIATION SHEILD", "tấm chắn bức xạ"), ("RISER", "ống đứng"), ("GENERAL ASSEMBLY", "lắp ráp chung"), ("DETAIL OF BODY", "chi tiết thân"), ("DETAIL OF NOZZLE", "chi tiết đầu nối"), ("DEVELOPMENT", "khai triển"), ("FLARE", "đuốc"),
      ("AMMONIA FLARE", "đuốc NH3"), ("SYNTHESIS GAS FLARE", "đuốc khí tổng hợp"), ("SYN. GAS FLARE", "đuốc khí tổng hợp"),
      ("LOW PRESSURE FLARE", "đuốc áp thấp (LP)"), ("LP FLARE", "đuốc LP"), ("L.P  FLARE", "đuốc LP"), ("STORAGE TANK GAS", "khí bồn chứa")]


def flare_item(stem):
    t = FLARE.get(stem.upper(), stem)
    low = t.lower()
    tags = [FA, FS]
    if "ammonia" in low or "storage tank" in low:
        tags = [FA]
    if "synthesis" in low or "syn." in low:
        tags = [FS]
    if "low press" in low or "lp " in low or "l.p" in low or "lp gas" in low or low.endswith("lp flare"):
        tags = [LP]
    if "(main flares)" in low or "main flare system" in low:
        tags = [FA, FS]
    c = stem.split("-")[2]
    g = "dw"
    if c.startswith("D0") and re.search(r"P & I", t): g = "sys"
    elif re.search(r"PLATFORM|LADDER", t): g = "plat"
    elif re.search(r"PIPING", t): g = "pipe"
    elif c.startswith("D1"): g = "ins" if "INSTRUMENT" in t or "TERMINAL" in t else "el"
    elif c.startswith("D2") or "ANCHOR" in t or "TEMPLATE" in t: g = "gen"
    elif c.startswith("S1"): g = "ins" if "INSTRUMENT" in t or "JUNCTION" in t else "el"
    elif c.startswith("S0"):
        g = "sp" if "SPARE" in t else "gen" if "PAINT" in t else "test"
    return t, g, tags


TKDOC = {"L00202": ("Tính toán bền (bồn trong/ngoài)", "ds"), "L00203": ("Tính toán trần treo (tải dài hạn/ngắn hạn)", "ds"),
         "L00204": ("Tính toán kích thước & thể tích bồn", "ds"), "L00205": ("Tính toán dây neo (anchor strap)", "ds"),
         "L00206": ("Tính toán lưu lượng xả van an toàn (bay hơi)", "ds"), "L00207": ("Quy cách thép tấm A516", "mr"),
         "L00209": ("Quy cách mua sắm van thở / van an toàn (PVRV)", "mr"), "L00211": ("Quy cách mua sắm van an toàn (PVRV)", "mr"),
         "L00212": ("Quy cách mua sắm khớp giãn nở (expansion bellows)", "mr"), "L00213": ("Phụ tùng 2 năm vận hành", "sp"),
         "L00214": ("Phụ tùng chạy thử", "sp"), "L00215": ("Danh sách nhà thầu phụ", "mr"), "L00216": ("Quy cách mua sắm thiết bị đo nhiệt độ", "ins"),
         "L00217": ("Tính toán bền ống lồng & tấm gia cường (sleeve, pad)", "ds"), "L00221": ("ITP chế tạo tại xưởng", "test"),
         "L00222": ("ITP lắp dựng tại công trường", "test"), "L00223": ("Quy trình chế tạo", "test"), "L00224": ("Quy trình lắp dựng bồn", "gen"),
         "L00225": ("Quy trình thử thủy lực bồn trong & thử khí nén bồn ngoài", "test"), "L00226": ("Quy cách kết cấu & giá đỡ", "gen"),
         "L00239": ("Quy trình xử lý nhiệt sau hàn (PWHT)", "test"), "L00240": ("Hồ sơ L00240", "test"),
         "L00241": ("Kế hoạch tháo/lắp lại tôn thân S1b để PWHT", "test"), "L00242": ("Phân tích bền vòng nén (compression ring)", "ds"),
         "L00243": ("Quy trình đuổi khí & làm lạnh bồn (N₂ purge, cool down)", "om"), "L00244": ("Bản vẽ vendor cảm biến nhiệt độ", "ins"),
         "L00245": ("Bản vẽ vendor van an toàn (PVRV)", "ins")}

REVDOC = {  # mã tài liệu vendor revamp (trang bìa)
    "0710": {"A1109-001": "Bản vẽ khung bó ống", "A1109-002": "Bản vẽ cụm quạt", "A1112-001": "Bản vẽ nhãn thiết bị",
             "A1113-001": "Bản vẽ chi tiết bó ống", "A1119-005": "Bản vẽ chi tiết cuộn gia nhiệt hơi", "A2001-001": "Bản vẽ bố trí chung (GA)"},
    "4025": {"A1001-001": "Data sheet cơ khí", "A1109-001": "Bản vẽ chi tiết khớp nối (coupler)", "A2001-001": "Bản vẽ GA (kèm nhãn thiết bị)",
             "A2006-001": "Bản vẽ móng & tải trọng", "A3303-002": "Bản vẽ tủ khí nén", "A3403-001": "Bản vẽ hộp đấu dây",
             "B1002-001": "Kế hoạch kiểm tra & thử (ITP)", "B1104-001": "Quy trình FAT"},
    "0910": {"A1101-001": "Bản vẽ mặt cắt & danh mục chi tiết", "A1102-001": "Hệ khí đệm (buffer gas) & danh mục chi tiết",
             "A2001-001": "Bản vẽ GA (outline)", "A4207-001": "Bản vẽ động cơ điện"},
    "1584": {"A2001-001": "Bản vẽ bố trí chung (GA)", "A2001-002": "Bản vẽ nâng hạ", "A2005-001": "Bản vẽ isometric ống", "A2007-001": "Bản vẽ kết cấu"},
}
REVTAG = {"0710": ([E2], "Bộ gia nhiệt NH3 40-E-5002"), "4025": (LA, "Cần nạp 40-LA-5003…5006"), "0910": ([P3], "Bơm 40-P-5003"),
          "1584": (MP, "Cụm đo đếm NH3 40-PK-5003/5004")}

# mã tài liệu 2539-4151-01 (cụm làm lạnh mới 40-PK-5005) → tên theo thư mục "Tài liệu PTSC gửi"
VI41 = {"Vendor Document List": "Danh mục tài liệu nhà cung cấp", "Control Philosophy": "Triết lý điều khiển", "Process Flow Diagram": "Sơ đồ PFD",
        "P&ID": "P&ID cụm", "Noise Datasheet": "Data sheet độ ồn", "Painting Specification": "Quy cách sơn", "Equipment Datasheet": "Data sheet thiết bị",
        "Performance Curve (Compressor & Oil Pump)": "Đường đặc tính máy nén & bơm dầu", "Thermal Rating for Heat Exchanger": "Tính toán nhiệt thiết bị trao đổi nhiệt",
        "Utility Consumption List": "Danh mục tiêu hao phụ trợ", "Operation & Maintenance Manual": "Hướng dẫn vận hành & bảo dưỡng",
        "Installation, Startup and Commissioning Manual": "Hướng dẫn lắp đặt, khởi động & chạy thử", "Cause & Effect Chart": "Cause & Effect",
        "Logic Diagrams": "Sơ đồ logic", "I-O List": "Danh mục I/O", "Modbus List": "Danh mục Modbus", "Instrument List": "Danh mục thiết bị đo",
        "Instrument Datasheet": "Data sheet thiết bị đo", "Instrument Hookup": "Sơ đồ lắp đặt thiết bị đo (hook-up)", "Motor Data Sheet": "Data sheet động cơ",
        "General Arrangement Drawing": "Bản vẽ bố trí chung (GA)", "Foundation Layout": "Bản vẽ móng", "Structural Drawing": "Bản vẽ kết cấu",
        "Structural Calculation": "Tính toán kết cấu", "Lifting Arrangement Drawing": "Bản vẽ nâng hạ", "Recommendation for Storage": "Khuyến nghị bảo quản",
        "List of spare parts for 2 year operation": "Phụ tùng 2 năm vận hành", "List of spares for commissioning": "Phụ tùng chạy thử",
        "Inspection Test Plan": "Kế hoạch kiểm tra & thử (ITP)", "Fabrication & Quality Plan": "Kế hoạch chế tạo & kiểm soát chất lượng",
        "Control Panel FAT Procedure": "Quy trình FAT tủ điều khiển", "Package FAT Procedure": "Quy trình FAT cụm", "Compressor Air Run test Procedure": "Quy trình chạy thử máy nén bằng không khí",
        "Control Valve & Relief Valve Calculation": "Tính toán van điều khiển & van an toàn", "Hydrostatic Test Procedure": "Quy trình thử thủy lực", "Leak test Procedure": "Quy trình thử kín",
        "NDT Procedure": "Quy trình NDT", "NDE Operator Qualification": "Chứng chỉ thợ NDE", "Welder Performance Qualification Certificate": "Chứng chỉ thợ hàn",
        "WPS-PQR": "WPS & PQR", "WPS-PQR for Structural": "WPS & PQR kết cấu", "WPS-PQR for Vessel & Piping": "WPS & PQR bình & ống", "Inspection Invitiation": "Thư mời kiểm tra",
        "Cable Block Diagram": "Sơ đồ khối cáp", "Cable Routing Diagram": "Sơ đồ đi cáp", "Cable Schedule": "Lịch cáp", "Electrical Interconnecting Diagram": "Sơ đồ đấu nối điện",
        "Local Control Panel GA Drawing & Wiring": "Tủ điều khiển tại chỗ – GA & đấu dây", "Starter Panel GA Drawing": "GA tủ khởi động", "Junction Box Drawing": "Bản vẽ hộp đấu dây",
        "Gauge Board & Support Drawing": "Bảng đồng hồ & giá đỡ", "Aux Drawing (Oil Pump)": "Bản vẽ phụ trợ (bơm dầu)", "Coupling & Guard Drawing": "Bản vẽ khớp nối & che chắn",
        "Major Piping Layout and Drawing (ISO dwg)": "Bố trí đường ống chính (isometric)", "Thermal Stress Calculation Note (Piping Stress)": "Tính toán ứng suất nhiệt đường ống"}
CODEFAM = {"A11": "Bản vẽ thiết bị", "B13": "Hồ sơ hàn", "B11": "Quy trình thử", "C10": "Danh mục nhà thầu phụ / tài liệu thương mại", "A04": "Tài liệu kỹ thuật"}


def t41(name):
    if name in VI41:
        return VI41[name]
    for a, b in (("GA Drawing ", "Bản vẽ GA – "), ("Detail Drawing ", "Bản vẽ chi tiết – "), ("Mechanical Calculation ", "Tính toán cơ khí – "),
                 ("Nameplate Drawing ", "Bản vẽ nhãn – "), ("Weld Map ", "Sơ đồ mối hàn "), ("Compressor GA Drawing", "Bản vẽ GA máy nén")):
        if name.startswith(a):
            name = b + name[len(a):]
    return (name.replace("Condenser", "thiết bị ngưng tụ (E1)").replace("Oil Distiller", "bình chưng cất dầu (V4)")
            .replace("Oil Separator", "bình tách dầu").replace("Oil Filter", "lọc dầu").replace("Receiver", "bình chứa (V2)")
            .replace("Subcooler", "sub-cooler (V1)"))


CODE41 = {}
for line in open(os.path.join(HERE, "listing.txt"), encoding="utf-8"):
    m = re.search(r"Tài liệu PTSC gửi/([^/]+)/2539-4151-01-(?:A-)?([AB]\d{4}-\d{3})", line)
    if m:
        CODE41.setdefault(m.group(2), m.group(1))

for line in open(os.path.join(HERE, "listing.txt"), encoding="utf-8"):
    line = line.strip()
    if not line:
        continue
    p, sz = line.rsplit("|", 1)
    sizes.append([R + "/" + p, int(sz)])
    fn = p.rsplit("/", 1)[-1]
    stem, ext = fn.rsplit(".", 1)
    ext = ext.lower()
    low = p.lower()
    x = f" ({ext})" if ext not in ("pdf",) else ""
    if "/" not in p:
        if "DW-0051" in fn: add(p, "Mặt bằng chi tiết khu bồn chứa NH3 (2539-40-DW-0051-01-01)", "sys", U45, no="2539-40-DW-0051-01-01")
        elif fn.startswith("40-PK-5005 PFD"): add(p, "PFD cụm làm lạnh 40-PK-5005", "sys", [PK5])
        elif fn.startswith("G2-00-PA-410"): add(p, "PA phối hợp đưa NH3 lỏng từ X.NH3 về bồn chứa 40-TK-5001 (G2-00-PA-410)", "inc", [TK, P1])
        elif fn.startswith("Local Panel"): add(p, "Tủ điều khiển tại chỗ & skid máy nén K1A (ppt)", "el", [PK1, PK1 + "/K1A"])
        elif fn.startswith("seal 40P5002"): add(p, "Phớt cơ khí bơm 40-P-5002", "dw", [P2])
        else: raise SystemExit("chưa xếp: " + p)
    elif p.startswith("40-P-5001AB 5002/"):
        if stem == "Datasheet": add(p, "Data sheet & biên bản thử bơm 40-P-5001A/B, 40-P-5002 (Flowserve 100 WUC-2R-6)", "ds", [P1, P2], src="Flowserve / Worthington")
        elif stem.startswith("40-P-5001-2-3"): add(p, "Tài liệu bơm 40-P-5001/5002/5003", "ds", [P1, P2, P3])
        else:
            n = stem.split("-")[-1].strip()
            t = [P1] if stem.startswith("5001") else [P2]
            add(p, f"Vendor data book bơm {t[0]}{'A/B' if t[0] == P1 else ''} – phần {n}", "book", t, src="Flowserve / Worthington")
    elif p.startswith("40-PK-1001-1002/"):
        if fn == "02-2014-CNSX.pdf": add(p, "Đề nghị thay đổi: purge mạng đuốc bằng N₂ thay khí nhiên liệu (2014)", "inc", [FA, FS])
        elif fn.startswith("Report flare"): add(p, "Báo cáo kiểm tra đuốc BDTT 2023 (rev 1)", "inc", [FA, FS, KO])
        elif fn.startswith("Utilityflares"): add(p, "Tài liệu tham khảo: Utility flares (ppt)", "ref", [FA, FS])
        elif fn == "descrip.doc": add(p, "Mô tả công nghệ hệ thống đuốc (descrip.doc)", "sys", [FA, FS, KO])
        elif fn.startswith("#Contents"): add(p, "Mục lục CD tài liệu vendor đuốc (xls)", "book", [FA, FS, LP])
        elif fn.startswith("Tài liệu tổng"): add(p, "Tài liệu tổng hợp vendor đuốc 40-PK-1001/1002 (bản gộp)", "book", [FA, FS])
        elif stem.upper().startswith("2098-01850"):
            t, g, tags = flare_item(stem)
            t = re.sub(r"\s+", " ", t).strip().replace("P & I DIAGRAM", "P&ID").replace("G.A.", "GA").replace("F.F.G.", "FFG").replace("A.C.W.L.", "ACWL")
            t = t[0] + t[1:].lower()
            for w in ("P&id", " ga ", "ffg", "acwl", "lp ", "l.p ", "eef-u", "ar-", "nde", "ndt", "wps", "pqr", "korea", "japan", "dwg"):
                t = t.replace(w, w.upper() if w not in ("korea", "japan") else w.capitalize())
            add(p, t[0].upper() + t[1:], g, tags, no=stem.upper(), src="Vendor đuốc · MR 2098-01850")
        else: raise SystemExit("chưa xếp: " + p)
    elif p.startswith("40-PK-5001/"):
        src = "Industrie Technofrigo Dell'Orto · MR 2098-MR-4151-50"
        if "/Inspection Book/" in p:
            add(p, "Inspection book – " + {"A": "bình áp lực & thiết bị trao đổi nhiệt", "B": "máy nén & bơm", "C": "động cơ", "D": "thiết bị đo",
                                           "E": "đường ống", "G": "toàn cụm"}[stem[0]], "test", [PK1], src=src)
        elif "/Operating manual/" in p:
            t = {"A": ("A – Data sheet (máy nén Mycom N200MUD-HE, động cơ, bơm dầu, bình, thiết bị đo…)", "ds"),
                 "B": ("B – Hướng dẫn lắp đặt & khởi động", "om"), "C": ("C – Mô tả hệ thống & logic điều khiển", "sys"),
                 "D": ("D – Mô tả kỹ thuật thiết bị chính (máy nén, bơm dầu, động cơ, khớp nối, làm mát dầu…)", "om"),
                 "E": ("E – Thiết bị đo", "ins"), "F": ("F – An toàn", "gen"), "G": ("G – Bảo dưỡng", "om"),
                 "H": ("H – Bản vẽ cơ khí", "dw"), "I": ("I – Bản vẽ điện", "el"), "O": ("Mục lục sổ tay vận hành", "book")}[stem[0]]
            tags = [PK1] + ([PK1 + "/K1A", PK1 + "/K1B"] if stem[0] in "AD" else [])
            add(p, t[0], t[1], tags, src=src)
        elif "PLC Installation" in p: add(p, "Hướng dẫn lắp đặt & vận hành PLC", "el", [PK1], src=src)
        elif "Software List" in p: add(p, "Danh mục phần mềm", "el", [PK1], src=src)
        else: raise SystemExit("chưa xếp: " + p)
    elif p.startswith("40-TK-5001/"):
        if "Kiểm soát áp suất" in fn: add(p, "Kiểm soát áp suất bồn chứa NH3 (doc)", "om", [TK])
        elif "/dwg/" in p:
            if fn.startswith("full drawing"): add(p, "Bộ bản vẽ đầy đủ bồn 40-TK-5001 (bản gộp)", "book", [TK], src="Samsung Heavy Industries")
            else: add(p, f"Bản vẽ bồn 40-TK-5001 – {stem}", "dw", [TK], no=stem, src="Samsung Heavy Industries")
        elif fn.startswith("Pilot safety"): add(p, "Van an toàn kiểu pilot (catalogue)", "ins", [TK])
        elif fn.startswith("temperature transmitter"): add(p, "Cảm biến nhiệt độ (catalogue)", "ins", [TK])
        else:
            k = stem[:6]
            t, g = TKDOC[k]
            part = stem[7:] if len(stem) > 6 else ""
            kind = {"xls": "trang bìa", "doc": "nội dung", "pdf": "nội dung"}.get(ext, ext)
            add(p, f"{t} ({kind}{' ' + part if part else ''}, {ext})", g, [TK], no=k, src="Samsung Heavy Industries")
    elif p.startswith("Dữ liệu KO/"):
        add(p, {"du lieu 40V1001 truoc BDTT2023": "Dữ liệu mức 40-V-1001 trước BDTT 2023", "DULIEU 40V1001_40LI41011_BDTT2023": "Dữ liệu 40-V-1001 / 40-LI-41011 BDTT 2023",
                "DULIEU 40V1001_40LI41011": "Dữ liệu 40-V-1001 / 40-LI-41011", "Theo dõi mức bồn 40V1001": "Theo dõi mức bình 40-V-1001"}[stem] + " (xlsx)", "om", [KO])
    elif p.startswith("Quy trình phương án"):
        if "PA-406" in fn: add(p, "PA purge sửa chữa van B1-44, B1-56 bơm 40-P-5002 (G2-30-PA-406)", "inc", [P2])
        elif "knock out" in fn: add(p, "PA xử lý nước nhiễm NH3 tại knock-out drum 40-V-1001", "inc", [KO, FA, FS])
        else: add(p, "Hướng dẫn: trường hợp đang purge NH3 (docx)", "inc", [TK, P2])
    elif p.startswith("SCC NH3 Tank/"):
        add(p, {"01-": "Ăn mòn ứng suất (SCC) bồn NH3 – Module 1 (Fertilizer Academy)", "02-": "Ăn mòn ứng suất (SCC) bồn NH3 – Module 2 (Fertilizer Academy)",
                "Amm": "Sự cố vỡ bồn NH3 tại Nam Phi", "Gui": "Hướng dẫn kiểm tra bồn NH3 lạnh áp suất khí quyển",
                "Tri": "SCC trong bồn chứa NH3 khan – chứng chỉ Fertilizer Academy"}[fn[:3]], "ref", [TK])
    elif p.startswith("Revamp/1. PROCESS DESCRIPTION/"):
        t = {"2539-45-CN-0009-01_0": "Mô tả công nghệ Unit 45 (revamp) – 2539-45-CN-0009-01", "Process Description": "Process description kho NH3 (docx)",
             "Unit 45 PROCESS DESCRIPTION VIE": "Mô tả công nghệ kho NH3 (tiếng Việt)", "Tài liệu bồn chứa NH3&đuốc thải (đang cập nhật)": "Tài liệu bồn chứa NH3 & đuốc (bản nháp)"}[stem]
        add(p, t + x, "sys", U45, no="2539-45-CN-0009-01" if "CN-0009" in stem else "", src="Revamp 2539")
    elif p.startswith("Revamp/2. PI&D/"):
        dwg = re.search(r"2539-45-PID-0031-0\d-0\d", fn).group(0)
        add(p, f"P&ID {dwg} rev 0" + (" – điểm tie-in" if "Ties" in fn else ""), "rev", U45, no=dwg, src="Revamp 2539")
    elif p.startswith("Revamp/4. DATASHEET/"):
        folder = p.split("/")[2]
        tags = {"40-E-5002": [E2], "40-LA-5003,04,05,06": LA, "40-P-5003": [P3], "40-PK-5005": [PK5], "40-PSV-45512": [TK],
                "40-PV-45004 A": [TK, PK5], "40-TV-45017": [E2]}[folder]
        if stem.startswith(("T-T-P", "PVFCC0_T-T-P")):
            add(p, f"Phiếu chuyển tài liệu {re.search(r'T-T-P-\d+', stem).group(0)}{x}", "mr", tags, src="Revamp 2539")
        else:
            add(p, f"Data sheet {folder} – {stem.split('_')[0]} rev {stem.split('_')[-1]}{x}", "ds", tags, no=stem.split("_")[0], src="Revamp 2539")
    elif p.startswith("Revamp/5. Tài Liệu Tham Khảo/"):
        rest = p[len("Revamp/5. Tài Liệu Tham Khảo/"):]
        m = re.match(r"(?:.*/)?2539-(\d{4})-0[13]-(?:A-)?([AB]\d{4})-(\d{3})(?:[._]\S*)?", fn)
        if rest.startswith("03. Reference Engineering Document/"):
            if "LAYOUT" in rest: add(p, "Mặt bằng khu bồn chứa NH3 (2539-40-DW-0051 rev 0)", "rev", U45, no="2539-40-DW-0051-01-01", src="Revamp 2539"); continue
            mr, code = m.group(1), f"{m.group(2)}-{m.group(3)}"
            rev = re.search(r"-\d{3}_([0-9A-Z]+)", fn).group(1)
            if mr == "4151":
                add(p, f"{t41(CODE41.get(code, code))} – cụm làm lạnh 40-PK-5005 (rev {rev})", "dw", pk5_sub(CODE41.get(code, '').lower()), no=f"2539-4151-01-{code}", src="Revamp · tài liệu tham khảo")
            else:
                tags, who = REVTAG[mr]
                t = REVDOC[mr].get(code, code)
                g = "test" if code.startswith("B") else "ds" if code.startswith("A1001") else "ins" if code.startswith(("A33", "A34")) else "el" if code.startswith("A42") else "dw"
                add(p, f"{t} – {who} (rev {rev})", g, tags, no=f"2539-{mr}-0{'3' if mr == '0910' else '1'}-{code}", src="Revamp · tài liệu tham khảo")
        elif rest.startswith("HAZOP Documentation/"):
            t = {"Refrigeration Package_GA": ("Bản vẽ GA cụm làm lạnh 40-PK-5005 (hồ sơ HAZOP)", [PK5]), "Refrigeration Package_PID": ("P&ID vendor cụm làm lạnh 40-PK-5005 (hồ sơ HAZOP)", [PK5]),
                 "2539-45-PID-0031-02-01_C": ("P&ID 2539-45-PID-0031-02 rev C – cần nạp hiện hữu (hồ sơ HAZOP)", LA + [P2]),
                 "2539-45-PID-0031-04-01_C": ("P&ID 2539-45-PID-0031-04 rev C – cần nạp mới (hồ sơ HAZOP)", LA + [P3, E2]),
                 "Loading Arm_GA": ("Bản vẽ GA cần nạp 40-LA-5003…5006 (hồ sơ HAZOP)", LA)}
            k = next(k for k in t if fn.startswith(k))
            add(p, t[k][0], "rev", t[k][1], src="HAZOP revamp")
        elif rest.startswith("INTERLOCK PROCESS DESCRIPTION/"):
            if "CN-0009-02" in fn: add(p, f"Mô tả liên động (interlock) kho NH3 – 2539-45-CN-0009-02{x}", "ins", U45, no="2539-45-CN-0009-02", src="Revamp 2539")
            else: add(p, f"Danh mục 2539-45-NM-0013-01{x}", "ins", U45, no="2539-45-NM-0013-01", src="Revamp 2539")
        elif rest.startswith("PFD/"): add(p, "PFD 2539-45-PFD-0010-01-01 rev 0" + (" (bản scan)" if "Scan" in fn else ""), "rev", U45, no="2539-45-PFD-0010-01-01", src="Revamp 2539")
        elif rest.startswith("PI&D Scan/"):
            dwg = re.search(r"2539-45-PID-0031-0\d-0\d", fn).group(0)
            add(p, f"P&ID {dwg} rev 0 (bản scan)", "rev", U45, no=dwg, src="Revamp 2539")
        elif rest.startswith("Process Description  Control Philosophy/"): add(p, "Mô tả công nghệ & triết lý điều khiển cụm 40-PK-5005 (rev A)", "sys", [PK5], no="2539-4151-01-A0101-001", src="Revamp 2539")
        elif rest.startswith("2539-00-MS-"): add(p, f"Biện pháp thi công PTSC {stem.split('_')[0]}{x}", "rev", [PK5], no=stem.split("_")[0], src="PTSC")
        elif rest.startswith("2539-4151-01-A5015"): add(p, "Hướng dẫn lắp đặt, khởi động & chạy thử cụm 40-PK-5005 (rev 0)", "test", [PK5], no="2539-4151-01-A5015-001", src="Revamp 2539")
        elif fn == "40-PK-5005 operation.pdf": add(p, "Hướng dẫn vận hành cụm làm lạnh 40-PK-5005", "om", pk5_sub("compressor oil pump"), src="Revamp 2539")
        elif fn == "Set point list PLC.pdf": add(p, "Danh mục set point PLC cụm làm lạnh 40-PK-5005", "ins", [PK5], src="Revamp 2539")
        elif fn.startswith("T-T-P-01668"): add(p, "Phiếu chuyển tài liệu T-T-P-01668", "mr", [PK5], src="Revamp 2539")
        elif rest.startswith("Tài liệu PTSC gửi/"):
            folder = rest.split("/")[1]
            if folder == "Hazop Response Sheet":
                add(p, f"Phản hồi HAZOP cụm 40-PK-5005 ({rest.split('/')[2]}){x}", "rev", [PK5], src="PTSC")
                continue
            code = m.group(2) + "-" + m.group(3) if m else ""
            t = t41(folder)
            g = ("sys" if folder in ("Control Philosophy", "Process Flow Diagram", "P&ID") else "om" if "Manual" in folder else
                 "ins" if re.search(r"Instrument|Cause|Logic|I-O|Modbus|Gauge|Junction|Valve", folder) else "el" if re.search(r"Cable|Electrical|Panel|Motor", folder) else
                 "sp" if "spare" in folder.lower() else "test" if re.search(r"Test|FAT|Inspection|NDE|NDT|Weld|WPS|Fabrication|Hydro|Leak", folder, re.I) else
                 "ds" if re.search(r"Datasheet|Calculation|Curve|Rating|Utility|Noise", folder, re.I) else "gen" if re.search(r"Foundation|Structural|Lifting|Storage|Painting", folder) else "dw")
            add(p, t + (f" ({fn[:14]}…)" if "534E0497" in fn else "") + x, g, pk5_sub(folder.lower()), no=f"2539-4151-01-{code}" if code else "", src="PTSC · MR 2539-00-MR-4151-01")
        elif rest.startswith("Tài liệu nhà thầu gửi MR-4151-01"):
            code = f"{m.group(2)}-{m.group(3)}" if m else fn
            rev = re.search(r"-\d{3}_([0-9A-Z]+)", fn)
            name = CODE41.get(code)
            if not name and code[:3] in CODEFAM:
                name = f"{CODEFAM[code[:3]]} {code}"
            if not name:
                name = {"A0101-001": "Control Philosophy", "A0102-001": "Process Flow Diagram", "A0103-001": "P&ID", "A0105-001": "Noise Datasheet",
                        "A0106-001": "Painting Specification", "A0403-001": "Hồ sơ A0403", "A1001-001": "Equipment Datasheet"}.get(code, "Tài liệu " + code)
            add(p, f"{t41(name)} – cụm 40-PK-5005 (rev {rev.group(1) if rev else '?'})", "dw", pk5_sub(name.lower()), no=f"2539-4151-01-{code}" if m else "", src="Nhà thầu · MR-4151-01")
        else:
            raise SystemExit("chưa xếp: " + p)
    else:
        raise SystemExit("chưa xếp: " + p)

# nhóm cho tài liệu nhà thầu 4151 (đặt "dw" tạm) theo tên
for d in docs:
    if d["src"].startswith("Nhà thầu") or d["src"].startswith("Revamp · tài liệu tham khảo") and "40-PK-5005" in d["t"]:
        t = d["t"].lower()
        d["g"] = (G["sys"] if re.search(r"triết lý|pfd|p&id", t) else G["om"] if "hướng dẫn" in t else G["ins"] if re.search(r"thiết bị đo|cause|logic|i/o|modbus", t)
                  else G["sp"] if "phụ tùng" in t else G["test"] if re.search(r"itp|kiểm tra|thử|fat|mối hàn|wps|nde|ndt|chế tạo|hồ sơ hàn|chứng chỉ", t)
                  else G["ds"] if re.search(r"data sheet|tính toán|đặc tính|tiêu hao", t) else G["el"] if re.search(r"cáp|động cơ|tủ|điện", t)
                  else G["gen"] if re.search(r"móng|kết cấu|nâng|bảo quản|sơn", t) else d["g"])

json.dump(docs, open(os.path.join(HERE, "docs.json"), "w"), ensure_ascii=False, indent=0)
json.dump(sizes, open(os.path.join(HERE, "sizes.json"), "w"), ensure_ascii=False)
print(len(docs), "tài liệu NH3 & Flare")
