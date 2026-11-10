#!/usr/bin/env python3
"""Dựng web/data/vendor.json: danh mục tài liệu vendor + gắn vào tag thiết bị.

Nguồn (trong tools/vendor/):
  listing_lohoi.json   danh sách file thư mục "Vendor Data/Lo hoi phu tro" (đường dẫn tương đối, kích thước)
  titles_778.json      tên bản vẽ Macchi (Ref. 778) lấy từ mục lục Vendor Data Book (OCR)
  sections.json        trang bắt đầu các mục trong các sách gộp (Part 1B/1C/1D/1E), OCR
  10-V-8001_doclist.csv  danh mục tài liệu bình khử khí (SICES)
  base_url.txt         (tuỳ chọn) đường link OneDrive "View online" của thư mục Vendor Data

Chạy: python3 tools/vendor/build_vendor.py  -> ghi web/data/vendor.json
"""
import csv, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
ROOT = "Lo hoi phu tro"
F1 = ROOT + "/1. Cac cum thiet bi_tank lien quan"

LIST = json.load(open(os.path.join(HERE, "listing_lohoi.json")))
TITLES = json.load(open(os.path.join(HERE, "titles_778.json")))
SECTIONS = json.load(open(os.path.join(HERE, "sections.json"))) if os.path.exists(os.path.join(HERE, "sections.json")) else {}
BASE = open(os.path.join(HERE, "base_url.txt")).read().strip() if os.path.exists(os.path.join(HERE, "base_url.txt")) else ""
SIZE = {p: s for p, s in LIST}

GROUPS = [
    "Data sheet & tài liệu chính",
    "Bản vẽ chế tạo",
    "Vận hành & bảo dưỡng",
    "Tổng quát, móng & lắp dựng",
    "Phần áp lực (bao hơi, ống, quá nhiệt, hâm nước)",
    "Đầu đốt & BMS",
    "Quạt gió FD, turbine & motor",
    "Van an toàn & bộ tiêu âm",
    "Đường ống & giá đỡ",
    "Ống gió, ống khói, vỏ lò, chịu lửa & bảo ôn",
    "Sàn thao tác & cầu thang",
    "Thiết bị đo & điều khiển",
    "Tính toán & data sheet",
    "Chạy thử (Part 1C)",
    "Phụ tùng (Part 1E)",
    "Tài liệu nhà sản xuất phụ kiện",
    "Bộ sách đầy đủ",
]

B = "10-B-8001"
docs, tagmap = [], {}


def add(path, title, group, tags, no="", src="", pg=None):
    if path not in SIZE:
        raise SystemExit("Không thấy file: " + path)
    d = {"p": path, "t": title, "g": group, "kb": round(SIZE[path] / 1024)}
    if no: d["no"] = no
    if src: d["src"] = src
    if pg: d["pg"] = pg
    docs.append(d)
    i = len(docs) - 1
    for t in tags:
        tagmap.setdefault(t, []).append(i)
    return i


# ---------------- 1. Cụm thiết bị / bình liên quan ----------------
DS = "Data sheet & tài liệu chính"
DW = "Bản vẽ chế tạo"
OM = "Vận hành & bảo dưỡng"
add(F1 + "/10-B-8001.pdf", "Data sheet lò hơi phụ trợ (Technip)", DS, [B])
add(F1 + "/10-E-8001.pdf", "Data sheet thiết bị trao đổi nhiệt (Blow down cooler)", DS, ["10-E-8001"])
add(F1 + "/10-E-8002.pdf", "Data sheet thiết bị ngưng tụ làm mát bằng không khí (Air cooler)", DS, ["10-E-8002"])
add(F1 + "/10-P-8003 A&B.pdf", "Data sheet bơm ly tâm (Condensate pumps, Worthington)", DS, ["10-P-8003A", "10-P-8003B"])
add(F1 + "/10-PK-8004.pdf", "Data sheet tháp khử khí (Degassing tower)", DS, ["10-PK-8004"])
add(F1 + "/10-PK-8004 dwg.pdf", "Bản vẽ tháp khử khí", DW, ["10-PK-8004"])
for n in ("1", "2", "3"):
    add(F1 + f"/10-SL-800{n}.pdf", "Data sheet bộ tiêu âm hơi (Steam silencer, Bolorocchi)", DS, [f"10-SL-800{n}"])

P1 = F1 + "/10-P-8001-AB"
add(P1 + "/10-P-8001 A&B.pdf", "Data sheet bơm 10-P-8001 A/B", DS, ["10-P-8001", "10-P-8001A", "10-P-8001B"])
add(P1 + "/10-P8001 A_Data Book.pdf", "Data book bơm 10-P-8001A", OM, ["10-P-8001A", "10-P-8001"])
add(P1 + "/10-STP-8001.pdf", "Data sheet turbine dẫn động bơm 10-STP-8001", DS, ["10-STP-8001"])
P2 = F1 + "/10-P-8002-AB"
add(P2 + "/10-P-8002 A&B.pdf", "Data sheet bơm 10-P-8002 A/B", DS, ["10-P-8002", "10-P-8002A", "10-P-8002B"])
add(P2 + "/10-P8002 A_Instruction Book.pdf", "Instruction book bơm 10-P-8002A", OM, ["10-P-8002A", "10-P-8002"])
add(P2 + "/10-P8002 B_Instruction Book.pdf", "Instruction book bơm 10-P-8002B", OM, ["10-P-8002B", "10-P-8002"])
add(P2 + "/10-STP-8002.pdf", "Data sheet turbine dẫn động bơm 10-STP-8002", DS, ["10-STP-8002"])
M2 = P2 + "/10MP8002-88.109.08"
MP = ["10-MP-8002"]
for f, t in [
    ("2098-18-SP-1692 03 _A.pdf", "Data sheet motor 10-MP-8002 (2098-18-SP-1692)"),
    ("2Q10592.pdf", "Tài liệu motor 2Q10592"),
    ("PRIMA PAGINA INSPECTION BOOK.pdf", "Inspection book – trang bìa"),
    ("Indice Inspection Book.pdf", "Inspection book – mục lục"),
    ("TLCURV0.pdf", "Đường đặc tính TLCURV0"),
    ("UCURVE0.pdf", "Đường đặc tính UCURVE0"),
    ("TRANS0.pdf", "Transmittal TRANS0"),
    ("TRANS1.pdf", "Transmittal TRANS1"),
    ("TRANS2.pdf", "Transmittal TRANS2"),
]:
    add(M2 + "/" + f, t, OM, MP)
add(M2 + "/vendor data book/test report.pdf", "Biên bản thử nghiệm motor (test report)", OM, MP)
add(M2 + "/vendor data book/Vendor data book.doc", "Vendor data book motor (Word)", OM, MP)

for n in ("1", "2", "3"):
    d = F1 + f"/10-PK- 800{n}" if n != "1" else F1 + "/10-PK-8001"
    tg = [f"10-PK-800{n}"]
    add(d + f"/10-PK-800{n}.pdf", f"Data sheet cụm 10-PK-800{n}", DS, tg)
    add(d + f"/10-PK-800{n} P&ID.pdf", f"P&ID của nhà cung cấp cụm 10-PK-800{n}", DW, tg)
    add(d + f"/VDB ITEM 10-PK-800{n}.pdf", f"Vendor data book cụm 10-PK-800{n}", OM, tg)

V1 = F1 + "/10-V-8001"
add(V1 + "/10-V-8001.pdf", "Data sheet bình khử khí 10-V-8001", DS, ["10-V-8001"])
with open(os.path.join(HERE, "10-V-8001_doclist.csv"), encoding="utf-8", errors="replace") as fh:
    rows = list(csv.reader(fh))
desc = {}
for r in rows:
    if len(r) >= 5 and r[3].startswith("2098-041102-"):
        desc[r[3][:15]] = (r[1].strip(), r[4].strip().title())
for p, _ in LIST:
    if p.startswith(V1 + "/2098-041102-") and p.endswith(".pdf"):
        f = p.rsplit("/", 1)[1]
        no, t = desc.get(f[:15], ("", ""))
        extra = " (van đĩa lò xo)" if "van dia lo xo" in f else (" (deaerator)" if "deaerator" in f else "")
        add(p, (t or f[:-4]) + extra, DW if "CALCULATION" not in t.upper() else "Tính toán & data sheet", ["10-V-8001"], no=f[:18].rstrip(" -"), src="SICES · 2098 MR 041102")
add(V1 + "/ASSEMBLY DRAWING.pdf", "Bản vẽ lắp (Assembly drawing)", DW, ["10-V-8001"])
add(V1 + "/dearator full drawing.pdf", "Toàn bộ bản vẽ bình khử khí", DW, ["10-V-8001"])
add(V1 + "/2098-041102-087-02.xls" if (V1 + "/2098-041102-087-02.xls") in SIZE else V1 + "/VENDOR DOCUMENT LIST.xls", "Bill of materials (Excel)", "Tính toán & data sheet", ["10-V-8001"], no="B.M. N° 6210")
add(V1 + "/VENDOR DOCUMENT LIST.xls", "Danh mục tài liệu vendor (Excel)", DS, ["10-V-8001"])
for n in ("2", "3", "4"):
    d = F1 + f"/10-V-800{n}"
    tg = [f"10-V-800{n}"]
    add(d + f"/10-V-800{n}.pdf", f"Data sheet bình 10-V-800{n}", DS, tg)
    add(d + "/Calculation Sheet.pdf", "Bảng tính bền (Calculation sheet)", "Tính toán & data sheet", tg)
    for p, _ in LIST:
        if p.startswith(d + "/Drawing/") and p.endswith(".pdf"):
            add(p, p.rsplit("/", 1)[1][:-4], DW, tg)

# ---------------- 2. Vendor Data Book lò hơi Macchi (Ref. 778) ----------------
SUB = {  # mã bản vẽ -> tag con
    "V1": "M-150 M-153 M-157 M-158 M-160 M-161 M-316 M-536 M-730 M-731 M-732 M-910",
    "V2": "M-151 M-153 M-536",
    "E1": "M-140 M-422 M-426 M-423 M-427 M-428 M-429 M-710 M-711",
    "SH1": "M-130 M-502 M-503 M-534 S-163",
    "SH2": "M-130 M-502 M-503 M-534 S-163",
    "K1": "M-211 M-024 M-410 M-414 M-415 M-416 C-321 A-230 A-231",
    "MK1": "S-880 S-106",
    "STK1": "M-217 C-327 S-019 S-534 M-310 M-719 A-260",
    "SK1": "M-022 M-430 M-431 M-423 M-427 M-428 M-429 M-605 M-606 M-715 M-716 M-717 C-720",
    "SL2": "M-272 C-330",
}
CODE2TAG = {}
for sub, codes in SUB.items():
    for c in codes.split():
        CODE2TAG.setdefault("778-" + c, []).append(B + "/" + sub)
CODE2TAG.setdefault("778-A-240", []).extend(["10-P-8001A", "10-P-8001B"])
CODE2TAG.setdefault("778-A-241", []).extend(["10-P-8001A", "10-P-8001B"])


def group_of(code):
    k, n = code.split("-")[1], int(code.split("-")[2])
    if k == "M":
        if n in (201, 202, 203, 309, 351): return "Đầu đốt & BMS"
        if n in (211, 217, 24, 719, 310): return "Quạt gió FD, turbine & motor"
        if n in (272, 276): return "Van an toàn & bộ tiêu âm"
        if n < 100 or n >= 900: return "Tổng quát, móng & lắp dựng"
        if n < 200: return "Phần áp lực (bao hơi, ống, quá nhiệt, hâm nước)"
        if n < 400: return "Đường ống & giá đỡ"
        if n < 700: return "Ống gió, ống khói, vỏ lò, chịu lửa & bảo ôn"
        return "Sàn thao tác & cầu thang"
    if k == "S":
        if n in (19, 534, 880, 106): return "Quạt gió FD, turbine & motor"
        if n in (30, 31, 83, 84, 456, 460, 520, 533): return "Đầu đốt & BMS"
        return "Thiết bị đo & điều khiển"
    if k == "A": return "Chạy thử (Part 1C)"
    if k == "C":
        if n in (305,): return "Đầu đốt & BMS"
        if n in (321, 327): return "Quạt gió FD, turbine & motor"
        if n in (315, 330): return "Van an toàn & bộ tiêu âm"
        return "Tính toán & data sheet"
    return "Tổng quát, móng & lắp dựng"


VOLNAME = {"vol-1": "Vol.1", "vol-2": "Vol.2", "vol-3": "Vol.3", "vol-4": "Vol.4", "vol-5": "Vol.5", "vol-6": "Vol.6"}
SPECIAL_1A = {
    "04-778-F-001_01.pdf": ("778-F-001", "Erection Procedure Titan M Boiler in Field"),
    "05-wb778-02.pdf": ("WB778-02", "Boiler Welding Map (Field Welding), Welding Procedure Specifications (WPS)"),
    "06-778-Q-202-1.pdf": ("778-Q-202/1", "Boiler Assembling"),
    "07-778p003.pdf": ("778-P-003", "List of Spare Parts and Special Tools for Commissioning and Start-up"),
    "08-778-A-001.pdf": ("778-A-001", "Procedure of Preparation of Equipment for Commissioning"),
    "09-schedule-site-erection.pdf": ("", "Detailed Schedule for Site Erection"),
    "02-778-erection-part-1a-index.pdf": ("", "Mục lục Part 1A (Erection & operating instruction manual)"),
}
VENDORS_1A = {  # vol-6, Section 3: tài liệu nhà sản xuất phụ kiện
    "02-lafarge.pdf": ("Lafarge – Recommendations for the installation of dense castables", [B]),
    "03-euromisure.pdf": ("Euromisure – Orifice assembly, meter run, flow nozzle, multistage restriction orifice", [B]),
    "04-psv1700.pdf": ("Dresser – Safety valve type 1700", [B]),
    "05-psv2700.pdf": ("Dresser – Safety valve type 2700", [B]),
    "06-psv1811.pdf": ("Dresser – Safety valve type 1811", [B]),
    "07-klinger.pdf": ("Klinger – Level gauges, installation and service guide", [B, B + "/V1"]),
    "08-Bonetti.pdf": ("Cesare Bonetti – Continuous blow down valves type BLB", [B]),
    "09-vitas.pdf": ("Vitas – Final valves drawing", [B]),
    "10-lvf.pdf": ("LVF – Manufacturing data report (valves)", [B]),
    "11-ALFA-VALVOLE.pdf": ("Alfa Valvole – Final valves drawing", [B]),
    "12-douglas.pdf": ("Douglas Italia – Bimetallic thermostatic steam traps BD60L A105", [B]),
    "13-alflex.pdf": ("Alflex – Multilayer textile expansion joint", [B, B + "/K1"]),
    "14-marland-1.pdf": ("Marland – Clutch installation, lubrication and maintenance (1)", [B, B + "/K1", B + "/MK1", B + "/STK1"]),
    "15-marland-2.pdf": ("Marland – Clutch installation, lubrication and maintenance (2)", [B, B + "/K1", B + "/MK1", B + "/STK1"]),
}

for p, _ in LIST:
    if not p.startswith(ROOT + "/PART 1A/") or not p.endswith(".pdf"):
        continue
    vol, f = p.split("/")[2], p.split("/")[3]
    src = "Part 1A " + VOLNAME.get(vol, vol) + " · Erection manual"
    if "COVER" in f.upper() or "SECTION" in f.upper() or (f.startswith("02-778-erection") and vol != "vol-1"):
        continue
    if f.startswith("full vol"):
        add(p, f"Toàn bộ Part 1A {VOLNAME.get(vol, vol)} (gộp)", "Bộ sách đầy đủ", [B], src=src)
        continue
    if f in SPECIAL_1A:
        no, t = SPECIAL_1A[f]
        g = "Bộ sách đầy đủ" if f.startswith("full") or "index" in f else "Tổng quát, móng & lắp dựng"
        add(p, t, g, [B] + CODE2TAG.get(no, []), no=no, src=src)
        continue
    if f in VENDORS_1A:
        t, tg = VENDORS_1A[f]
        add(p, t, "Tài liệu nhà sản xuất phụ kiện", tg, src=src)
        continue
    m = re.match(r"778M(\d{3})(?:_(\d+))?\.pdf$", f)
    if not m:
        print("bỏ qua", p)
        continue
    code = "778-M-" + m.group(1)
    t = TITLES.get(code, "Bản vẽ " + code)
    if m.group(2) is not None:
        t += f" – tờ {int(m.group(2))}"
    add(p, t, group_of(code), [B] + CODE2TAG.get(code, []), no=code, src=src)

for p, _ in LIST:
    if p.startswith(ROOT + "/PART 1F/") and p.endswith(".pdf"):
        code = p.rsplit("/", 1)[1][:-4]
        add(p, TITLES.get(code, code), group_of(code), [B] + CODE2TAG.get(code, []), no=code, src="Part 1F Vol.17 · Final technical documentation")

BOOKS = [
    (ROOT + "/PART 1B/erection book part 1b vol1.pdf", "Part 1B Vol.1 – Erection manual (điện & đo lường), bản gộp"),
    (ROOT + "/PART 1B/erection book part 1b vol2.pdf", "Part 1B Vol.2 – Erection manual (điện & đo lường), bản gộp"),
    (ROOT + "/PART 1C/Vendor Data Book Part 1C.pdf", "Part 1C – Precommissioning & commissioning manual"),
    (ROOT + "/PART 1D/Vendor Data Book Part 1D.pdf", "Part 1D – Operation & maintenance manual (toàn bộ)"),
    (ROOT + "/PART 1D/Vendor Data Book Part 1D_Part1.pdf", "Part 1D – Operation & maintenance manual, phần 1"),
    (ROOT + "/PART 1D/Vendor Data Book Part 1D_Part2.pdf", "Part 1D – Operation & maintenance manual, phần 2"),
    (ROOT + "/PART 1E/Vendor Data Book Part 1E.pdf", "Part 1E – Recommended spare parts list for 2 years operation"),
]
for p, t in BOOKS:
    add(p, t, "Bộ sách đầy đủ", [B], src="Vendor Data Book Macchi · Ref. 778")

# Các mục trong sách gộp (trang bắt đầu lấy từ OCR): {đường dẫn sách: [[mã mục, tên, trang, [tag con...], nhóm], ...]}
SPLIT = {}  # không dùng file tách mục: người dùng muốn mở sách gốc đúng trang
for p_, v in SPLIT.items():
    SIZE[v["p"]] = v["kb"] * 1024
for book, secs in SECTIONS.items():
    short = {"1B": "Part 1B", "1C": "Part 1C", "1D": "Part 1D", "1E": "Part 1E"}
    lab = next((v for k, v in short.items() if "Part " + k in book or "part " + k.lower() in book), "")
    if "1b vol1" in book: lab = "Part 1B Vol.1"
    if "1b vol2" in book: lab = "Part 1B Vol.2"
    if "1D_Part1" in book: lab = "Part 1D (phần 1)"
    if "1D_Part2" in book: lab = "Part 1D (phần 2)"
    for no, title, pg, subs, g in secs:
        tags = [B] + [B + "/" + s if not s.startswith("10-") else s for s in subs]
        sp = SPLIT.get(book + "|" + no)
        if sp:  # file đã tách theo mục: mở là đúng trang đầu của mục
            add(sp["p"], title, g, tags, no=no, src=f"{lab} · trang {sp['from']}–{sp['to']} ({sp['pages']} tr.)")
        elif SPLIT and "Part 1D" in book and any(x[0].startswith(no + ".") for x in secs):
            continue  # mục lớn đã có các mục con
        else:
            add(book, title, g, tags, no=no, src=lab, pg=pg)

out = {
    "base": BASE,
    "root": "Vendor Data",
    "groups": GROUPS,
    "pkgs": {B: "Lò hơi phụ trợ – Macchi (Ref. 778)"},
    "docs": docs,
    "tags": tagmap,
}
dst = os.path.join(REPO, "web", "data", "vendor.json")
json.dump(out, open(dst, "w"), ensure_ascii=False, separators=(",", ":"))
print(f"{len(docs)} tài liệu, {len(tagmap)} tag -> {dst} ({os.path.getsize(dst)//1024} KB)")
for t in sorted(tagmap):
    print(f"  {t:22s} {len(tagmap[t])}")
