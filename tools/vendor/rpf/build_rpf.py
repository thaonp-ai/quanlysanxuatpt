#!/usr/bin/env python3
"""Danh mục "Vendor Data/9. Raw-Pot-Fire" (nước thô, nước sinh hoạt, nước cứu hỏa) -> docs.json + sizes.json.

Đầu vào: listing.txt  (đường dẫn tương đối trong "9. Raw-Pot-Fire" | byte), đã bỏ file rác
(thư mục FS15/FS16 của Acrobat Catalog, Thumbs.db, trang bìa mục 6-x chỉ có tên mục, file mục lục con).
Các tài liệu đã là file riêng theo mục nên không cần tách sách.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
R = "9. Raw-Pot-Fire"

G_DS = "Data sheet & tài liệu chính"
G_DW = "Bản vẽ chế tạo"
G_OM = "Vận hành & bảo dưỡng"
G_INS = "Thiết bị đo & điều khiển"
G_EL = "Điện & tủ điều khiển"
G_SP = "Phụ tùng"
G_TEST = "Chạy thử"
G_SUB = "Tài liệu nhà sản xuất phụ kiện"
G_GEN = "Tổng quát, móng & lắp dựng"
G_MR = "Đơn hàng & yêu cầu kỹ thuật (MR/SR)"
G_SYS = "Hệ thống (P&ID, mô tả công nghệ)"
G_BOOK = "Bộ sách đầy đủ"

RAW = ["30-P-2001"]          # bơm nước thô 30-P-2001A/B/C (web tự hiện cho A/B/C)
POT = ["30-P-2002"]          # bơm nước sinh hoạt 30-P-2002A/B
FIRE = ["30-P-4001", "30-P-4002"]  # cụm bơm cứu hỏa 30-PK-4001/4002 (bơm 30-P-4001A-C, 30-P-4002A/B)
PK = "30-PK-2001"
# tag con của cụm xử lý nước sinh hoạt 30-PK-2001 (theo P&ID 33/2001) – suy ra từ tên thiết bị
# theo "4 - Mechanical Equipment Specification": lọc than hoạt tính = FL2A/B, lọc tinh 1 µm = FL1A/B
CARBON = [PK + "/FL2A", PK + "/FL2B"]
MICRO = [PK + "/FL1A", PK + "/FL1B"]
DOSE = [PK + "/P1A", PK + "/P1B", PK + "/MP1A", PK + "/MP1B", PK + "/P2", PK + "/MP2"]
DRUM = [PK + "/P3", PK + "/MP3"]
TANK = [PK + "/TK1"]
MIXER = [PK + "/Z1"]

docs, sizes = [], []


def add(p, t, g, tags, no="", src=""):
    docs.append({"p": R + "/" + p, "t": t, "g": g, "tags": tags, "no": no, "src": src, "kb": 0})


PUMPSEC = {"Title": ("Bìa & mục lục", G_BOOK), "0": ("Bìa & mục lục", G_BOOK), "1": ("Mục 1 – Dữ liệu bơm hoàn công (data sheet, đặc tính, thử nghiệm)", G_DS),
           "2": ("Mục 2 – Hướng dẫn lắp đặt, vận hành, bảo dưỡng (IOM)", G_OM), "3": ("Mục 3 – Động cơ điện", G_EL),
           "4": ("Mục 4 – Danh mục phụ tùng khuyến nghị", G_SP), "5": ("Mục 5 – Tài liệu chung", G_GEN)}
PUMPDW = {"6-1": ("Bản vẽ bố trí chung (GA)", G_DW), "6-2": ("Bản vẽ mặt cắt & danh mục chi tiết", G_DW),
          "6-3": ("Bản vẽ phớt cơ khí", G_DW), "6-4": ("Khớp nối", G_DW), "6-5": ("Bản vẽ nhãn thiết bị", G_DW)}
FIRET = {"COVER": ("Bìa Vendor Data Book", G_BOOK), "Vendor Print Index-Schedule": ("Danh mục & tiến độ tài liệu nhà cung cấp", G_MR),
         "Equipment Filled-in Data Sheets": ("Data sheet thiết bị", G_DS), "Performance curves": ("Đường đặc tính bơm", G_DS),
         "Noise data sheet": ("Data sheet độ ồn", G_DS), "Calculation notes": ("Thuyết minh tính toán", G_DS),
         "Calculation sheet": ("Bảng tính toán", G_DS), "Utility Balance": ("Cân bằng phụ trợ", G_DS),
         "General Arrangement Drawings": ("Bản vẽ bố trí chung (GA)", G_DW),
         "Cross sectional assembly drawings-with part list": ("Bản vẽ mặt cắt lắp ráp & danh mục chi tiết", G_DW),
         "Drawings of auxiliaries and itemized equipments supplied loos": ("Bản vẽ thiết bị phụ & vật tư giao rời", G_DW),
         "Nameplate drawing": ("Bản vẽ nhãn thiết bị", G_DW), "Electric Motor Data Sheets": ("Data sheet động cơ điện", G_EL),
         "Electrical motor drawings": ("Bản vẽ động cơ điện", G_EL), "Electrical connection block diaggrams": ("Sơ đồ khối đấu nối điện", G_EL),
         "Panels arrangement drawings": ("Bản vẽ bố trí tủ điện", G_EL),
         "Torque versus Speed-Current-Power Factor Curves": ("Đặc tính mômen – tốc độ – dòng – hệ số công suất motor", G_EL),
         "Instrument Data Sheet": ("Data sheet thiết bị đo", G_INS), "List of Instruments": ("Danh mục thiết bị đo", G_INS),
         "Logic diagrams-interlock-safety sequence diagrams-cause-effec": ("Sơ đồ logic, liên động, cause & effect", G_INS),
         "Completed Lubricant chart": ("Bảng dầu mỡ bôi trơn", G_OM),
         "List of spare parts for 2 year Operation": ("Phụ tùng 2 năm vận hành", G_SP),
         "List of spare parts for erection commissioning-start -up": ("Phụ tùng lắp đặt, chạy thử", G_SP),
         "Fabrication-Quality  Control Plan": ("Kế hoạch chế tạo & kiểm soát chất lượng", G_TEST),
         "Testing Procedure": ("Quy trình thử nghiệm", G_TEST), "On Site Performance Test Procedure": ("Quy trình thử hiệu suất tại công trường", G_TEST),
         "Procedure Qualification Record": ("Hồ sơ chất lượng quy trình hàn (PQR)", G_TEST),
         "Welding Procedure Specification": ("Quy trình hàn (WPS)", G_TEST),
         "Engineering Procurement Manufacturing Test Schedule": ("Tiến độ thiết kế – mua sắm – chế tạo – thử", G_MR),
         "Sub-vendors-main  suppliers list": ("Danh sách nhà thầu phụ", G_MR), "Packing List": ("Danh sách đóng gói", G_GEN),
         "Painting Specification": ("Quy cách sơn", G_GEN),
         "Recommendation for protection during transportation": ("Bảo quản trong vận chuyển", G_GEN)}
TK = {"FRP TANK DATA": ("Data sheet bồn FRP", G_DS), "PE TANK DATA": ("Data sheet bồn PE", G_DS),
      "FABRICATION PROCEDURE": ("Quy trình chế tạo bồn", G_TEST), "INSPECTION PROCEDURE": ("Quy trình kiểm tra bồn", G_TEST),
      "FQCP": ("Kế hoạch kiểm soát chất lượng chế tạo", G_TEST), "INDEX": ("Mục lục tài liệu bồn", G_BOOK),
      "SPAREPARTLIST": ("Danh mục phụ tùng", G_SP)}


def pk_item(fn):
    """30-PK-2001: tên, nhóm, tag con theo tên file."""
    s = re.sub(r"\.pdf$", "", fn)
    low = s.lower()
    num = re.match(r"(B )?([\d.]+)\s*[-–]?\s*", s)
    title = s[num.end():] if num else s
    title = title.replace("THONG TIN CARBON ", "").replace("Satic", "Static").replace("Suzler", "Sulzer").replace("Miltron", "Milton")
    tags = [PK]
    if "carbon" in low: tags += CARBON
    if "micro filter" in low: tags += MICRO
    if "hypochlorite tank" in low: tags += TANK
    if "milton" in low or "miltron" in low or "metering" in low or "dosing" in low or "l-series" in low: tags += DOSE
    if "drum pump" in low: tags += DRUM
    if "static mixer" in low or "satic mixer" in low: tags += MIXER
    if "/section a" in fn.lower() or re.match(r"\d+ - (Shutdown|Trouble|Maintenance|Erection|Precommissioning|Scope|Mechanical|Chemicals|Recommendation)", s) or s[:2] in ("1.", "2.", "9."):
        pass
    g = G_OM
    if re.search(r"datasheet|data sheet|specification|scope|consumption|thickness", low): g = G_DS
    if re.search(r"drawing|diagram-p&id|block diagram|arrangement|welding key", low): g = G_DW
    if re.search(r"instrument|flow|chlorine|level|gauge|pressure gauge|differential|display|solenoid|cable|loop|hookup|plc|alarm|cause|sequence|control|ladder", low): g = G_INS
    if re.search(r"control panel|enclosure", low): g = G_EL
    if re.search(r"valve|actuator", low) and "solenoid" not in low: g = G_SUB
    if re.search(r"milton|thompson|filterite|sulzer|suzler", low): g = G_SUB
    if re.search(r"process description|p&id|block diagram|general arrangement", low): g = G_SYS
    if re.search(r"commissioning|start-up", low): g = G_TEST
    if re.search(r"safety guidelines|safety precautions|material safety|erection|transportation|table of contents|drawing list", low): g = G_GEN
    if re.search(r"maintenance|trouble|shutdown", low): g = G_OM
    return (num.group(2).rstrip(".") + " – " if num else "") + title.strip(" -"), g, tags


for line in open(os.path.join(HERE, "listing.txt"), encoding="utf-8"):
    line = line.strip()
    if not line:
        continue
    p, sz = line.rsplit("|", 1)
    sizes.append([R + "/" + p, int(sz)])
    fn = p.rsplit("/", 1)[-1]
    stem, ext = fn.rsplit(".", 1)
    if p.startswith("30-P-2002AB"):
        raw = "Raw Water" in p
        tags, src = (RAW, "Bơm nước thô · MR 0910-52") if raw else (POT, "Bơm nước sinh hoạt · MR 0910-52")
        if "/Drawings/" in p:
            k = re.search(r"/(6-\d) ", p).group(1)
            t, g = PUMPDW[k]
            if "Metastream" in fn:
                t, g = "Hướng dẫn lắp đặt & bảo dưỡng khớp nối Metastream", G_OM
            add(p, t, g, tags, no=stem, src=src)
        else:
            m = re.search(r"Section 0?(\d+)", stem)
            t, g = PUMPSEC[m.group(1) if m else "Title"]
            add(p, t, g, tags, src=src)
    elif p.startswith("30-PK 4001"):
        t, g = FIRET[stem]
        add(p, t + ("" if ext.lower() == "pdf" else " (ảnh scan .tif)"), g, FIRE, src="Bơm cứu hỏa 30-PK-4001/4002 · MR 0910-56")
    elif p.startswith("30-PK-2001"):
        t, g, tags = pk_item(fn)
        vol = re.search(r"Vol (\d) of 3", p)
        add(p, t, g, tags, src="Xử lý nước sinh hoạt · MR 0230-50" + (f" · Vol {vol.group(1)}/3" if vol else ""))
    elif p.startswith("30-TK-3002"):
        t, g = TK[stem]
        add(p, f"{t} ({ext.lower()})", g, ["30-TK-3002"], src="Bồn 30-TK-3002")
    elif p.startswith("Revamp"):
        add(p, "P&ID hệ thống cứu hỏa Unit 34 – điểm tie-in (revamp)", G_SYS, FIRE, no="2539-34-PID-0031-02-01", src="Revamp 2539")
    else:
        raise SystemExit("chưa xếp: " + p)

json.dump(docs, open(os.path.join(HERE, "docs.json"), "w"), ensure_ascii=False, indent=0)
json.dump(sizes, open(os.path.join(HERE, "sizes.json"), "w"), ensure_ascii=False)
print(len(docs), "tài liệu Raw-Pot-Fire")
