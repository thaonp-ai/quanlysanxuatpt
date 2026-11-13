#!/usr/bin/env python3
"""Danh mục "Vendor Data/4. Demi" (Unit 31 – nước khử khoáng) -> docs.json + sizes.json.

Đầu vào: listing.txt (đường dẫn tương đối trong "4. Demi" | byte). Đã bỏ: ảnh (Hình ảnh demi),
.dwg, file Acrobat Catalog (FS13/FS14/FS18, .cat/.abt/...), Thumbs/desktop.db.
Sách vendor cụm 30-PK-1001 (6 volume) đã là file riêng theo mục nên không cần tách.
Tag con 30-PK-1001/... theo bảng thiết bị trên P&ID 2098-31-PID-0031-02…07.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
R = "4. Demi"

G_DS = "Data sheet & tài liệu chính"
G_DW = "Bản vẽ chế tạo"
G_OM = "Vận hành & bảo dưỡng"
G_INS = "Thiết bị đo & điều khiển"
G_EL = "Điện & tủ điều khiển"
G_SP = "Phụ tùng"
G_TEST = "Chạy thử"
G_SUB = "Tài liệu nhà sản xuất phụ kiện"
G_GEN = "Tổng quát, móng & lắp dựng"
G_PIPE = "Đường ống & giá đỡ"
G_MR = "Đơn hàng & yêu cầu kỹ thuật (MR/SR)"
G_SYS = "Hệ thống (P&ID, mô tả công nghệ)"
G_REV = "Dự án cải tạo 2016–2017 (Revamp)"
G_INC = "Sự cố & trao đổi"
G_REF = "Tài liệu tham khảo"
G_BOOK = "Bộ sách đầy đủ"

PK = "30-PK-1001"


def S(*x):
    return [PK + "/" + i for i in x]


CAT = S("V1")                      # bình cation V1A/B/C (web tự hiện cho A/B/C)
DG = S("V2", "P2", "MP2", "K2", "MK2", "SL1", "FL1")
AN = S("V3")
MB = S("V4")
PAR = S("V5")
ACID = S("TK3", "TK4", "TK10", "TK11", "J1", "J2")
CAUS = S("TK5", "TK6", "J3", "J4", "Z2", "Z3", "MZ2", "MZ3")
NA2 = S("TK7", "Z1", "MZ1", "P6", "MP6")
NP = S("BA1", "K1", "MK1", "SL2", "P5", "MP5", "TK8", "Z4", "MZ4", "P7", "MP7", "TK9", "P8", "MP8")
REG = S("P1", "MP1", "P3", "MP3")

docs, sizes = [], []


def add(p, t, g, tags, no="", src=""):
    tags = list(dict.fromkeys([PK] + tags if tags and tags[0].startswith(PK) else tags))
    docs.append({"p": R + "/" + p, "t": t, "g": g, "tags": tags, "no": no, "src": src, "kb": 0})


def kw_tags(low):
    """tag con theo từ khóa trong tên file sách vendor 30-PK-1001"""
    t = []
    if re.search(r"cation|\bsac\b", low): t += CAT
    if re.search(r"anion|\bsba\b", low): t += AN
    if re.search(r"degas|\bdg\b|dgwt", low): t += DG
    if re.search(r"mixed bed|\bmb\b|mbp|polisher", low): t += MB
    if re.search(r"process air receiver|\bpar\b", low): t += PAR
    if re.search(r"sodium sulphite|na2so3", low): t += NA2
    if re.search(r"neutrali|\bnp\b", low): t += NP
    if re.search(r"acid|h2so4", low) and not re.search(r"\bnp\b|neutrali", low): t += ACID
    if re.search(r"caustic|naoh", low) and not re.search(r"\bnp\b|neutrali", low): t += CAUS
    if re.search(r"regeneration area|regn area", low): t += ACID + CAUS
    if re.search(r"tk ?3|tk ?4", low): t += S("TK3", "TK4")
    if re.search(r"tk5|tk6", low): t += S("TK5", "TK6")
    if "tk8" in low: t += S("TK8")
    if "tk9" in low: t += S("TK9")
    if "tk10" in low: t += S("TK10")
    if "tk11" in low: t += S("TK11")
    if re.search(r"dm water tank", low): t += ["30-TK-1002"]
    return t


TANK17 = {"1": (S("TK3"), "Bồn đong axit cho cation (TK3)"), "2": (S("TK4"), "Bồn đong axit cho mixed bed (TK4)"),
          "3": (S("TK9"), "Bồn axit cho hố trung hòa (TK9)"), "4": (S("TK10"), "Bồn pha loãng axit cho cation (TK10)"),
          "5": (S("TK11"), "Bồn pha loãng axit cho mixed bed (TK11)"), "6": (NA2, "Bồn chứa Na₂SO₃ (TK7)"),
          "7": (S("TK5"), "Bồn xút cho anion (TK5)"), "8": (S("TK6"), "Bồn xút cho mixed bed (TK6)"),
          "9": (S("TK8"), "Bồn xút cho hố trung hòa (TK8)"), "10": (S("BA1"), "Hố trung hòa – phần xây dựng (BA1)"),
          "11": (S("TK3", "TK4"), "Giá đỡ bồn TK3 & TK4")}
PUMP4 = {"1.1.1": (S("P6", "MP6"), "Bơm châm Na₂SO₃ (P6A/B)"), "1.1.2": (S("P7", "MP7"), "Bơm châm NaOH hố trung hòa (P7A/B)"),
         "1.1.3": (S("P8", "MP8"), "Bơm châm H₂SO₄ hố trung hòa (P8A/B)"), "1.1.4": (REG, "Bơm nước tái sinh (P1A/B, P3)"),
         "1.1.5": (S("P2", "MP2"), "Bơm sau tháp khử CO₂ (P2A/B/C)"), "1.1.6": (S("P5", "MP5"), "Bơm nước trung hòa (P5A/B)"),
         "1.2.1": (S("K1", "MK1"), "Quạt sục hố trung hòa (K1A/B)"), "1.2.2": (S("K2", "MK2"), "Quạt tháp khử CO₂ (K2A/B/C)"),
         "1.3": (S("Z1", "Z2", "Z3", "Z4", "MZ1", "MZ2", "MZ3", "MZ4"), "Máy khuấy Lightnin (Z1–Z4)")}
VOL1 = {"1": ("An toàn", G_GEN), "2": ("Mô tả hệ thống", G_SYS), "3": ("Tóm tắt phạm vi cung cấp", G_MR),
        "5": ("Tiêu hao hóa chất & phụ trợ", G_DS), "6": ("Vận chuyển, bốc xếp & lưu kho", G_GEN), "7": ("Lắp dựng", G_GEN),
        "8": ("Tiền chạy thử, chạy thử & khởi động", G_TEST), "9": ("Vận hành – khởi động & dừng bình thường", G_OM),
        "10": ("Vận hành – tái sinh", G_OM), "11": ("Giám sát vận hành (phân tích, thông số)", G_OM), "12": ("Bảo dưỡng", G_OM),
        "13": ("Xử lý sự cố", G_OM), "14": ("Biểu mẫu nhật ký vận hành", G_OM)}
PUMPSEC = {"1": ("Mục 1 – Dữ liệu bơm hoàn công (data sheet, đặc tính, thử nghiệm)", G_DS), "2": ("Mục 2 – Hướng dẫn lắp đặt, vận hành, bảo dưỡng (IOM)", G_OM),
           "3": ("Mục 3 – Động cơ điện", G_EL), "4": ("Mục 4 – Danh mục phụ tùng khuyến nghị", G_SP), "5": ("Mục 5 – Tài liệu chung", G_GEN)}
PUMPDW = {"6-1": ("Bản vẽ bố trí chung (GA)", G_DW), "6-2": ("Bản vẽ mặt cắt & danh mục chi tiết", G_DW), "6-3": ("Bản vẽ phớt cơ khí", G_DW),
          "6-4": ("Khớp nối", G_DW), "6-5": ("Bản vẽ nhãn thiết bị", G_DW), "6-6": ("Bản vẽ nhãn thiết bị", G_DW)}
PUMPBOOK = {"30-P-1001AB": (["30-P-1001", "30-MP-1001"], "Bơm nước khử ion · MR 0910-52"),
            "30-P-1003AB": (["30-P-1003", "30-MP-1003"], "Bơm nhận/chuyển H₂SO₄ · MR 0910-52"),
            "30-P-1004 (": (["30-P-1004", "30-MP-1004"], "Bơm nhận NaOH · MR 0910-52")}
# 30-E-1001 (Alfa Laval?) – sách theo "Tag": nội dung theo mục lục Index.pdf
E1001 = {"Cover": ("Bìa", G_BOOK), "Index": ("Mục lục", G_BOOK)}
E1001_TAG = json.load(open(os.path.join(HERE, "e1001_tags.json"))) if os.path.exists(os.path.join(HERE, "e1001_tags.json")) else {}
REVDS = {"A0106": "Danh mục tài liệu nhà cung cấp", "A1001": "Data sheet", "A1003": "Bản vẽ bố trí chung (GA)", "A1012": "Danh mục vật liệu",
         "A1109": "Thuyết minh tính toán", "A2001": "Kế hoạch kiểm tra & thử (ITP)", "B1103": "Hướng dẫn lắp đặt, vận hành, bảo dưỡng",
         "B1202": "Danh mục phụ tùng"}
ROOT = {
    "2022 - Thermal power plant seminar": ("Hội thảo nhà máy nhiệt điện 2022 (slide chia sẻ)", G_REF, [PK]),
    "25-05-TTr-PT Phan tich mau": ("Tờ trình phân tích mẫu nước cụm Demi – nguyên nhân nhiễm vi sinh", G_INC, [PK]),
    "2539-31-PFD-0010-01-01_1": ("PFD 2539-31-PFD-0010-01-01 (as-built)", G_SYS, [PK, "30-TK-1001", "30-TK-1002"]),
    "30-P-1002 AB": ("Vendor data book bơm nước khử khoáng 30-P-1002A/B", G_BOOK, ["30-P-1002", "30-MP-1002"]),
    "30P1002 1": ("Bơm 30-P-1002 (tài liệu bổ sung 1)", G_DS, ["30-P-1002"]),
    "30P1002": ("Bơm 30-P-1002 (tài liệu bổ sung)", G_DS, ["30-P-1002"]),
    "30tk1001_R2": ("Bản vẽ bồn 30-TK-1001 (rev 2)", G_DW, ["30-TK-1001"]),
    "30tk1002_R2": ("Bản vẽ bồn 30-TK-1002 (rev 2)", G_DW, ["30-TK-1002"]),
    "G2-20-PA-403": ("PA vận hành khi độ dẫn nước ngưng turbine X.Urê cao (G2-20-PA-403)", G_INC, [PK, "30-E-1001", "30-E-1002", "30-TK-1001"]),
    "Lưu lượng tái sinh mixbed": ("Lưu lượng tái sinh mixed bed (bảng tính)", G_OM, MB),
    "PA phê duyệt": ("Phương án đã phê duyệt", G_INC, [PK]),
    "STVB116695": ("Báo cáo: cụm Demi tiếp nhận nước ngưng công nghệ nồng độ NH₃ cao", G_INC, [PK]),
    "STVB136132": ("FTA: rò SiO₂ qua train B hệ thống sản xuất nước khử khoáng", G_INC, S("V1", "V3") + [PK]),
    "STVB153884_G2-30-PA-359": ("PA cô lập & vận hành Demi khi vệ sinh tuyến ống WS đầu vào các train (G2-30-PA-359)", G_INC, [PK]),
    "STVB153884_PID": ("P&ID đính kèm PA G2-30-PA-359", G_INC, [PK]),
    "STVB30963": ("Biên bản khảo sát, đánh giá tình trạng cụm 30-PK-1001 & đề xuất PA xử lý", G_INC, [PK]),
    "STVB82680": ("Biên bản khảo sát tình trạng hệ thống nước Demi sau BDTT 2023", G_INC, [PK]),
    "Thông báo xưởng 25-05": ("Thông báo xưởng: cô lập các van block hóa chất hệ thống Demi", G_INC, ACID + CAUS + [PK]),
    "Uoc tinh luu luong": ("Ước tính lưu lượng làm việc – thay hạt nhựa train C", G_OM, CAT + AN + [PK]),
}


def clean(s):
    s = re.sub(r"\.+$", "", s.strip())
    s = re.sub(r"\s*-{3,}\s*$", "", s)
    return re.sub(r"\s+", " ", s).strip(" -")


for line in open(os.path.join(HERE, "listing.txt"), encoding="utf-8"):
    line = line.strip()
    if not line:
        continue
    p, sz = line.rsplit("|", 1)
    fn = p.rsplit("/", 1)[-1]
    stem, ext = fn.rsplit(".", 1)
    low = p.lower()
    if re.search(r"/table of conten|/1\.\d? .*content|/2\.1 .*content|main content|contents\.pdf$|/1\.0 mechanical", low) and "Main Table" not in p and not p.startswith("30-P"):
        continue                                        # trang mục lục con
    if p.startswith("30-P-") and "/Drawings/" in p and stem.startswith(("6-", "Section 6-")) and int(sz) < 60000:
        continue                                        # trang bìa mục bản vẽ của sách bơm
    sizes.append([R + "/" + p, int(sz)])
    m = re.match(r"Demineralised Volume (\d) of 6/(.*)", p)
    if m:
        vol, rest = m.group(1), m.group(2)
        src = f"Cụm khử khoáng 30-PK-1001 · Vol {vol}/6"
        sec = re.match(r"Section (1\.\d+)/(?:(\d+)\s*-\s*)?(.*)", rest)
        if vol == "1":
            n = re.match(r"(\d+) - ", fn)
            if n:
                t, g = VOL1[n.group(1)]
                add(p, f"{n.group(1)} – {t}", g, [PK], src=src)
            elif stem.startswith("Mechanical"):
                add(p, "Thông số thiết bị cơ khí (Mechanical Equipment Specifications)", G_DS, [PK] + CAT + AN + DG + MB + PAR + ACID + CAUS + NA2 + NP + REG, src=src)
            else:
                add(p, "Mục lục Vol 1", G_BOOK, [PK], src=src)
            continue
        if "Main Table" in rest:
            add(p, f"Mục lục chính Vol {vol}", G_BOOK, [PK], src=src)
            continue
        if sec:
            s, num, title = sec.group(1), sec.group(2), clean(re.sub(r"\.pdf$", "", sec.group(3)))
            tags = kw_tags(title.lower())
            if s == "1.1":
                g = G_SYS
                if re.search(r"stream (\d)", title.lower()):
                    tags = CAT + DG + AN
                if "dm water tank" in title.lower():
                    tags = PAR + ["30-TK-1002"]
                if "instrument air" in title.lower():
                    tags = PAR
                t = "P&ID vendor – " + title
            elif s == "1.2":
                g, t = G_GEN, title if not title.startswith("section") else "Bố trí thiết bị (" + title + ")"
            elif s == "1.3":
                g, t = G_SYS, title
                if "valve" in title.lower() or "sequence" in title.lower():
                    g = G_INS
            elif s == "1.4":
                g, t = G_GEN, title
            elif s in ("1.5", "1.6"):
                g, t = G_DW, title
                if "level switch" in title.lower():
                    g = G_INS
            elif s == "1.7":
                g = G_DW
                if num in TANK17:
                    tags, t = TANK17[num][0], "GA " + TANK17[num][1]
                else:
                    t = title
            elif s == "1.8":
                g, t = G_PIPE, title if not title.startswith("section") else "Đường ống (" + title + ")"
            elif s == "1.9":
                g, t = G_EL, "Bố trí & sơ đồ đấu dây tủ điện – " + ("Main panel" if num == "1" else f"Local panel {int(num) - 1}" if num else title)
                if "Contents" in title:
                    continue
            elif s == "1.10":
                g, t = G_INS, "Sơ đồ lắp đặt thiết bị đo (hook-up)"
            elif s in ("1.11", "1.12"):
                g, t = G_EL, ("Bản vẽ tủ điều khiển – " if s == "1.11" else "Danh mục vật tư tủ điều khiển – ") + title
            else:
                g, t = G_GEN, title
            add(p, (f"{s}.{num} – " if num else f"{s} – ") + t, g, [PK] + tags, src=src)
            continue
        # Vol 4–6: data sheet & manual thiết bị
        mm = re.search(r"/(1\.\d\.\d|1\.\d) ([^/]+)\.pdf$", p)
        if vol == "4" and mm:
            k, title = mm.group(1), mm.group(2)
            if k in PUMP4:
                tags, t = PUMP4[k]
                add(p, f"{k} – {t}: data sheet & hướng dẫn", G_DS, [PK] + tags, src=src)
            else:
                add(p, f"{k} – Van: {title.split(' ', 1)[1] if ' ' in title else title}", G_SUB, [PK], src=src)
            continue
        mm = re.search(r"/(2\.1\.\d+) ([^/]+)\.pdf$", p)
        if mm:
            title = clean(mm.group(2))
            g = G_EL if re.search(r"plc|speed controller", title.lower()) else G_INS
            add(p, f"{mm.group(1)} – {title}", g, [PK], src=src)
            continue
        raise SystemExit("chưa xếp: " + p)
    hit = next((k for k in PUMPBOOK if p.startswith(k)), None)
    if hit:
        tags, src = PUMPBOOK[hit]
        if "/Drawings/" in p or "/Section 6 - Drawings/" in p:
            k = re.search(r"/(?:Section )?(6-\d)", p).group(1)
            t, g = PUMPDW[k]
            if "Metastream" in fn:
                t, g = "Hướng dẫn lắp đặt & bảo dưỡng khớp nối Metastream", G_OM
            elif "6-5 Vessel" in p:
                t, g = "Bình/thiết bị phụ – bản vẽ & data sheet: " + clean(stem), G_DW
            add(p, t, g, tags, no=stem if re.match(r"[A-Z0-9]+-[0-9]", stem) else "", src=src)
        elif stem.startswith("Title"):
            add(p, "Bìa & mục lục", G_BOOK, tags, src=src)
        elif stem == "30P1001A_B":
            add(p, PUMPSEC["1"][0], G_DS, tags, src=src)
        elif stem.startswith("I O Ms"):
            add(p, PUMPSEC["2"][0], G_OM, tags, src=src)
        else:
            n = re.search(r"Section 0?(\d)", stem).group(1)
            t, g = PUMPSEC[n]
            add(p, t, g, tags, src=src)
        continue
    if p.startswith("30-E-1001/"):
        if stem in E1001:
            t, g = E1001[stem]
        else:
            t, g = E1001_TAG.get(stem, [stem, G_DS])
        add(p, t, g, ["30-E-1001"], src="Làm mát nước ngưng turbine 30-E-1001 · Alfa Laval · MR 0660-60")
        continue
    if p.startswith("Revamp_."):
        src = "Revamp 2539"
        if "/1. PROCESS DESCRIPTION/" in p:
            t = "Mô tả công nghệ Unit 31 (revamp) – 2539-31-CN-0009-01" if "CN-0009" in fn else "Mô tả công nghệ Unit 31 (bản Word)"
            add(p, t + (" (.docx)" if ext == "docx" else ""), G_SYS, [PK, "30-E-1001", "30-E-1002", "30-TK-1001", "30-TK-1002"], no="2539-31-CN-0009-01" if "CN-0009" in fn else "", src=src)
        elif "/2. PI&D/" in p:
            add(p, "P&ID 2539-31-PID-0031-01" + (" – điểm tie-in" if "Ties" in fn else " (bản scan)"), G_REV, ["30-E-1001", "30-E-1002", "30-TK-1001", "30-P-1001"], no="2539-31-PID-0031-01-01", src=src)
        elif "/3. Các Điểm Ties-in/" in p:
            add(p, "Danh sách điểm tie-in Unit 31" if ext == "xlsx" else "Tie-in Demi chuẩn bị đấu nối", G_REV, [PK, "30-E-1002"], src=src)
        elif "/30-PSV-31509" in p:
            add(p, f"Data sheet van an toàn 30-PSV-31509 (30-E-1002) ({ext})", G_DS, ["30-E-1002"], no="2539-30-SP-1500-45", src=src)
        elif "/4. DATASHEET/30-E1002/" in p:
            add(p, f"Data sheet 30-E-1002 – 2539-31-SP-0660-01 ({ext})", G_DS, ["30-E-1002"], no="2539-31-SP-0660-01", src=src)
        elif "30-E-1002_Vendor data" in p:
            code = re.search(r"-(A\d{4}|B\d{4})-", fn).group(1)
            rev = re.search(r"-\d{3}_([0-9A-Z]+)", fn).group(1)
            ref = "Tài Liệu Tham Khảo" in p
            add(p, f"30-E-1002 – {REVDS.get(code, code)} (rev {rev}{', bản tham khảo' if ref else ''})", G_DS if code[0] == "A" and code != "A2001" else (G_OM if code == "B1103" else G_SP if code == "B1202" else G_TEST),
                ["30-E-1002"], no=stem.split("_")[0], src=src)
        elif "/PFD/" in p:
            add(p, "PFD 2539-31-PFD-0010-01-01 rev 0" + (" (bản scan)" if "Scan" in fn else ""), G_REV, [PK], no="2539-31-PFD-0010-01-01", src=src)
        elif "MS-6895" in fn:
            add(p, "Tài liệu tham chiếu 2539-00-MS-6895-05", G_REV, [PK], no="2539-00-MS-6895-05", src=src)
        elif "MSD-0011" in fn:
            add(p, "2539-31-MSD-0011-01-01 (scan)", G_REV, [PK], no="2539-31-MSD-0011-01-01", src=src)
        elif "DW-0051" in fn:
            add(p, "Bản vẽ tham chiếu 2539-30-DW-0051-01-01", G_REV, [PK], no="2539-30-DW-0051-01-01", src=src)
        else:
            raise SystemExit("chưa xếp: " + p)
        continue
    if p.startswith("Phân tích đầu vào demi"):
        t = {"3703": "Kết quả phân tích nước đầu vào Demi (Quatest 3)", "M01-": "Phiếu yêu cầu thử nghiệm (Quatest 3)",
             "MT-H": "Hướng dẫn lấy mẫu nước cấp (Quatest 3)", "STVB": "Tờ trình phân tích mẫu nước cụm Demi"}[fn[:4]]
        add(p, t, G_INC, [PK], src="Phân tích Quatest 3")
        continue
    if p.startswith("Tài liệu demi đạm cà mau"):
        t = {"05. ": "P&ID nước thô & khử khoáng – Đạm Cà Mau", "07087-20100": "PFD hệ thống nước – Đạm Cà Mau", "07087-20200": "PFD WT15-01~05 – Đạm Cà Mau",
             "16. ": "P&ID hệ RO1/RO2 – Đạm Cà Mau", "2025": "Hướng dẫn vận hành hệ thống sản xuất nước khử khoáng – Đạm Cà Mau",
             "3-GT": "Giáo trình đào tạo hệ thống sản xuất nước Demi – Đạm Cà Mau"}
        k = next(k for k in t if fn.startswith(k))
        add(p, t[k], G_REF, [PK], src="Tham khảo Đạm Cà Mau")
        continue
    k = next((k for k in ROOT if fn.startswith(k)), None)
    if k and "/" not in p:
        t, g, tags = ROOT[k]
        add(p, t + (f" ({ext})" if ext in ("xlsx", "docx", "doc") else ""), g, tags)
        continue
    raise SystemExit("chưa xếp: " + p)

json.dump(docs, open(os.path.join(HERE, "docs.json"), "w"), ensure_ascii=False, indent=0)
json.dump(sizes, open(os.path.join(HERE, "sizes.json"), "w"), ensure_ascii=False)
print(len(docs), "tài liệu Demi")
