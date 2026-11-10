#!/usr/bin/env python3
"""Tạo tools/vendor/sections.json: trang bắt đầu các mục trong sách gộp Vendor Data Book lò hơi.

Đầu vào: thư mục OCR từng trang (<trang>.txt) của Part 1D phần 1/phần 2 (OCR bằng tesseract),
cùng các mục Part 1C / Part 1E xác định bằng mắt (ghi cứng bên dưới).
Chạy: python3 sections_from_ocr.py <ocr Part1D_Part1> <ocr Part1D_Part2> [<ocr 1B vol1> <ocr 1B vol2>]
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
R = "Lo hoi phu tro"
D1 = R + "/PART 1D/Vendor Data Book Part 1D_Part1.pdf"
D2 = R + "/PART 1D/Vendor Data Book Part 1D_Part2.pdf"
C = R + "/PART 1C/Vendor Data Book Part 1C.pdf"
E = R + "/PART 1E/Vendor Data Book Part 1E.pdf"

OMG = "Vận hành & bảo dưỡng"
G_BMS = "Đầu đốt & BMS"
G_FAN = "Quạt gió FD, turbine & motor"
G_INS = "Thiết bị đo & điều khiển"
G_PIPE = "Đường ống & giá đỡ"
G_PS = "Phần áp lực (bao hơi, ống, quá nhiệt, hâm nước)"
G_DUCT = "Ống gió, ống khói, vỏ lò, chịu lửa & bảo ôn"
G_SV = "Van an toàn & bộ tiêu âm"
G_DS = "Data sheet & tài liệu chính"


def rule(no):
    """mã mục Part 1D -> (nhóm, [tag con])"""
    top = int(no.split(".")[0])
    sub = {"23.1": ["K1"], "23.2": ["K1", "MK1", "STK1"], "23.3": ["MK1"], "23.4": ["STK1"], "23.5": ["STK1"],
           "23.6": ["STK1"], "23.7": ["K1"], "26.4": ["SH1", "SH2"], "31.4": ["SL2"]}.get(no, [])
    if top == 30: sub = ["V1"]
    if top == 35: sub = ["SL2"]
    if top == 2: g = G_DS
    elif top in (4, 5, 6, 22): g = G_BMS
    elif top in (3, 7, 8, 9, 26, 28, 29, 30, 31, 32, 33, 34, 40): g = G_INS
    elif top in (10, 38): g = G_PS
    elif top == 23: g = G_FAN
    elif top in (24, 35): g = G_SV
    elif top in (25, 27, 37): g = G_PIPE
    elif top in (36, 39): g = G_DUCT
    else: g = OMG
    return g, sub


def find_sections(ocr_dir):
    out = []
    pages = sorted(int(f[:-4]) for f in os.listdir(ocr_dir) if f.endswith(".txt"))
    for p in pages:
        txt = open(os.path.join(ocr_dir, f"{p}.txt"), errors="replace").read()
        words = txt.split()
        if len(words) > 45:
            continue
        flat = " ".join(words)
        m = re.search(r"(SUB-?\s*)?SECTION\s+(\d{1,2}(?:\.\d{1,2})?)\s+(.+)$", flat, re.I)
        if not m:
            continue
        no = m.group(2)
        title = re.sub(r"[^A-Za-z0-9&/(),.' -]+", " ", m.group(3))
        title = re.sub(r"\s+", " ", title).strip(" -.,")
        title = re.sub(r"\b(a|ry|u|Cc|fal|C|ww|w)$", "", title).strip()
        if not title or len(title) < 3:
            continue
        out.append((no, title.title().replace("Bms", "BMS").replace("Fd ", "FD ").replace("P&L", "P&I").replace("P&l", "P&I"), p))
    # bỏ trùng, giữ thứ tự tăng dần của mã mục và tên mục đọc được (loại trang OCR nhiễu)
    key = lambda no: tuple(int(x) for x in no.split("."))
    seen, res, last = set(), [], (0,)
    for no, t, p in out:
        toks = t.split()
        good = sum(1 for w in toks if w in ("&", "&/") or re.fullmatch(r"[A-Za-z/()'.,-]{2,}", w) and (re.search(r"[aeiouyAEIOUY]", w) or len(w) <= 3))
        if no in seen or key(no) <= last or good < max(1, 0.7 * len(toks)):
            continue
        seen.add(no); last = key(no)
        res.append((no, t, p))
    return res


FIX = {"25.2": "Gate, Globe And Check Valves (Sizes Up To 2\")", "25.3": "Gate, Globe And Check Valves (Sizes Over 2\")",
       "25.5": "Continuous Blowdown Valves", "32.1": "Flow Transmitters", "34": "Oxygen, CO, Conductivity And pH Analyzers",
       "34.2": "Conductivity And pH Analyzer"}
S = {}
for book, d in ((D1, sys.argv[1]), (D2, sys.argv[2])):
    lst = []
    for no, t, p in find_sections(d):
        g, sub = rule(no)
        lst.append([("§" + no), f"Mục {no} – {FIX.get(no, t)}", p, sub, g])
    S[book] = lst

S[C] = [
    ["778-A-001", "Checks & operations before commissioning; danh sách hệ thống / thiết bị (778-A-001…004)", 19, [], "Chạy thử (Part 1C)"],
    ["778-A-100", "Biểu mẫu thử cơ khí van an toàn", 25, [], "Chạy thử (Part 1C)"],
    ["778-A-120", "Biểu mẫu thử thiết bị đo & van (778-A-120…202)", 26, [], "Chạy thử (Part 1C)"],
    ["778-A-230", "Biểu mẫu thử cơ khí quạt gió FD (778-A-230/231)", 40, ["K1"], "Chạy thử (Part 1C)"],
    ["778-A-240", "Biểu mẫu thử cơ khí bơm nước cấp (778-A-240/241)", 43, ["10-P-8001A", "10-P-8001B"], "Chạy thử (Part 1C)"],
    ["778-A-260", "Biểu mẫu thử cơ khí turbine quạt FD", 46, ["STK1"], "Chạy thử (Part 1C)"],
]
P = "Phụ tùng (Part 1E)"
S[E] = [
    ["1E", "Danh mục phụ tùng 2 năm vận hành – mục lục", 19, [], P],
    ["1E §1–3", "Phụ tùng lò hơi, đầu đốt, hệ thống đốt", 20, [], P],
    ["1E §5", "Phụ tùng quạt gió FD & khớp ly hợp Marland", 52, ["K1"], P],
    ["1E §6", "Phụ tùng turbine quạt FD (RLHA-24)", 57, ["STK1"], P],
    ["1E §7", "Phụ tùng motor quạt FD", 59, ["MK1"], P],
    ["1E §8", "Phụ tùng van an toàn", 63, [], P],
    ["1E §9", "Phụ tùng van đóng cắt khí nén", 66, [], P],
    ["1E §10", "Phụ tùng van điều khiển (Fisher)", 72, [], P],
    ["1E §13", "Phụ tùng van tay", 85, [], P],
    ["1E §14", "Phụ tùng thiết bị đo", 114, [], P],
    ["1E §15", "Phụ tùng tủ BMS", 146, [], P],
]

if len(sys.argv) > 4:
    B1 = R + "/PART 1B/erection book part 1b vol1.pdf"
    B2 = R + "/PART 1B/erection book part 1b vol2.pdf"
    for book, d in ((B1, sys.argv[3]), (B2, sys.argv[4])):
        lst = []
        for no, t, p in find_sections(d):
            lst.append(["1B §" + no, f"Mục {no} – {t}", p, [], G_INS])
        if lst:
            S[book] = lst

json.dump(S, open(os.path.join(HERE, "sections.json"), "w"), ensure_ascii=False, indent=1)
for b, l in S.items():
    print(b.rsplit("/", 1)[1], len(l))
    for x in l:
        print("   ", x[0], x[2], x[1][:70], x[3])
