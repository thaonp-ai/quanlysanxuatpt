"""P&ID cụm tuabin khí của nhà cung cấp (Nuovo Pignone SOM09996/1, 19 tờ) -> vendor_pid_gt.json (sheets + tag thiết bị).
Vị trí nhãn đọc bằng mắt trên ảnh thu nhỏ (toạ độ hiển thị dx,dy của ảnh 2600 px cắt 2–98 % ngang, 3–97 % dọc, xem ở 2000 px),
rồi bám vào từ OCR gần nhất có chứa '9001'."""
import json, re, os
from PIL import Image
T = "10-GT-9001/"
TITLES = {1: "Trang bìa & danh mục tờ", 2: "Ký hiệu & chú giải", 3: "Điểm đấu nối (terminal point)", 4: "Hệ thống dầu bôi trơn",
          5: "Dầu thủy lực & ratchet thủy lực", 6: "Dầu điều khiển (control oil)", 7: "Bộ làm mát dầu (oil cooler)", 8: "Khí nhiên liệu",
          9: "Cụm khí nhiên liệu DLN", 10: "Điều khiển & bảo vệ tuabin", 11: "Khí làm mát & làm kín", 12: "Lọc gió đầu vào",
          13: "Hệ thống chữa cháy CO₂", 14: "Hệ thống thông gió", 15: "Rửa máy nén off-line & on-line", 16: "Hệ thống khởi động",
          17: "Hộp số & máy phát – dầu bôi trơn, rung, nhiệt độ", 18: "Máy phát – nhiệt độ cuộn dây stator & gió làm mát", 19: "Bộ tách hơi dầu"}
# (sheet, tag suffix, dx, dy, vertical)
L = [
 (3,"E-1",112,152,0),(3,"PK-5",1055,42,0),(3,"PK-4",1462,92,0),(3,"PK-1",232,558,0),(3,"SL-1",232,732,0),(3,"SL-2",232,836,0),
 (3,"Z-5",652,898,0),(3,"V-4",1043,992,0),(3,"E-2",262,1282,0),(3,"PK-3",1568,962,0),(3,"PK-2",1146,1278,0),
 (4,"FL-1",396,262,0),(4,"FL-2",462,512,0),(4,"G-1",902,654,0),(4,"P-1",848,788,0),(4,"MP-2",530,870,1),(4,"P-2",440,1156,0),
 (4,"MP-3",707,850,1),(4,"P-3",612,1156,0),(4,"EH-2",866,1030,1),(4,"EH-1",938,1030,1),(4,"V-1",1214,1150,0),
 (5,"P-4",318,404,0),(5,"FL-3",676,358,0),(5,"FL-4",792,560,0),(5,"Z-2",1330,552,0),(5,"Z-1",1252,718,0),(5,"MP-5",1062,834,0),
 (5,"P-5",1138,988,0),(5,"Z-3",740,1020,0),
 (6,"FL-5",392,416,0),(6,"FL-6",392,688,0),
 (7,"MF-1",650,370,0),(7,"MF-2",922,366,0),(7,"MF-3",1206,362,0),(7,"F-1",580,468,0),(7,"F-2",852,468,0),(7,"F-3",1136,462,0),(7,"E-1",804,712,0),
 (12,"PK-5",144,486,0),(12,"F-4",92,880,0),(12,"F-5",226,880,0),(12,"MF-4",160,1002,0),(12,"MF-5",286,1002,0),
 (13,"G-2",1736,644,0),(13,"PK-1",190,790,0),
 (14,"MF-6",144,290,0),(14,"F-6",170,326,0),(14,"F-7",170,530,0),(14,"MF-7",140,600,0),
 (15,"V-2",354,978,0),(15,"V-3",746,916,0),(15,"P-6",712,1092,0),(15,"MP-6",754,1046,0),(15,"PK-2",462,1158,0),(15,"PK-3",1290,962,0),
 (16,"SL-1",82,88,0),(16,"SL-2",298,88,0),(16,"E-2",620,312,0),(16,"F-9",738,256,0),(16,"MF-9",754,340,0),(16,"Z-5",184,546,0),
 (16,"Z-4",1082,570,0),(16,"V-4",544,1248,0),
 (18,"MF-10",496,316,0),(18,"MF-11",688,316,0),(18,"MF-12",892,316,0),(18,"MF-13",1086,316,0),
 (18,"F-10",496,404,0),(18,"F-11",688,404,0),(18,"F-12",892,404,0),(18,"F-13",1086,404,0),
 (19,"PK-4",1192,858,0),
]
# service description (from the data tables on the sheets) -> s (type code), d (Vietnamese description)
D = {"E-1": ("E", "Bộ làm mát dầu bôi trơn bằng không khí (NP: HXL-2) – Astra, 680 kW"),
     "E-2": ("E", "Bộ làm mát nước động cơ diesel khởi động – 323 kW"),
     "PK-1": ("PK", "Cụm chai CO₂ chữa cháy (CBVF-1…26) – Sanco"),
     "PK-2": ("PK", "Xe rửa máy nén off-line (bồn V-2/V-3, bơm P-6)"),
     "PK-3": ("PK", "Xe rửa máy nén on-line (bồn TW-3, Rochem Marine)"),
     "PK-4": ("PK", "Cụm tách hơi dầu (PDS-1, quạt FNL-1) – Forain Lube Oil 900"),
     "PK-5": ("PK", "Nhà lọc gió đầu vào (inertial vane, lọc thô, lọc tinh)"),
     "SL-1": ("SL", "Bộ tiêu âm khí xả động cơ diesel"), "SL-2": ("SL", "Bộ tiêu âm khí xả động cơ diesel"),
     "Z-1": ("Z", "Ly hợp tự đồng bộ (SSS clutch)"), "Z-2": ("Z", "Bộ chấp hành IGV"),
     "Z-3": ("Z", "Cơ cấu ratchet thủy lực / bộ biến mô"), "Z-4": ("Z", "Bộ biến mô thủy lực (torque converter, Voith) & hộp số đảo chiều/ratchet"),
     "Z-5": ("Z", "Động cơ diesel khởi động"),
     "V-1": ("V", "Bồn dầu bôi trơn – 8.610 L (Deiuliis)"), "V-2": ("V", "Bồn nước rửa (rinsing) – 0,35 m³"),
     "V-3": ("V", "Bồn nước rửa + chất tẩy – 0,125 m³"), "V-4": ("V", "Bồn dầu diesel – 0,776 m³"),
     "P-1": ("P", "Bơm dầu bôi trơn chính (bánh răng, dẫn động từ hộp số phụ) – 1.187 L/ph"),
     "P-2": ("P", "Bơm dầu bôi trơn phụ – Aris Chiappa CVTG65/250A, 1.187 L/ph"),
     "P-3": ("P", "Bơm dầu bôi trơn sự cố – Aris Chiappa CVTG65/250E, 693 L/ph"),
     "P-4": ("P", "Bơm dầu thủy lực chính (dẫn động từ hộp số phụ)"),
     "P-5": ("P", "Bơm dầu thủy lực ratchet – Casappa PLP103.15"), "P-6": ("P", "Bơm nước rửa máy nén – 50 L/ph"),
     "MP-2": ("MP", "Motor bơm dầu phụ 88QA – ABB 37 kW, 400 V"), "MP-3": ("MP", "Motor bơm dầu sự cố 88QE – SICME 6,5 kW, 110 V DC"),
     "MP-5": ("MP", "Motor bơm ratchet 88HR – SICME 0,57 kW, 110 V DC"), "MP-6": ("MP", "Motor bơm nước rửa 88TW-1 – 2,2 kW"),
     "EH-1": ("EH", "Điện trở sấy dầu bôi trơn 23QT-1 – FATI 10 kW"), "EH-2": ("EH", "Điện trở sấy dầu bôi trơn 23QT-2 – FATI 10 kW"),
     "FL-1": ("FL", "Lọc dầu bôi trơn kép (duplex) 25 µm"), "FL-2": ("FL", "Lọc dầu bôi trơn kép (duplex) 25 µm"),
     "FL-3": ("FL", "Lọc dầu thủy lực kép (FH2-1) 3 µm"), "FL-4": ("FL", "Lọc dầu thủy lực kép (FH2-2) 3 µm"),
     "FL-5": ("FL", "Lọc dầu điều khiển kép – Murisengo 25/5 µm"), "FL-6": ("FL", "Lọc dầu điều khiển kép – Murisengo 25/5 µm"),
     "G-1": ("G", "Hộp số phụ (accessory gear)"), "G-2": ("G", "Hộp số tải (load gear)"),
     "F-1": ("F", "Quạt bộ làm mát dầu E-1"), "F-2": ("F", "Quạt bộ làm mát dầu E-1"), "F-3": ("F", "Quạt bộ làm mát dầu E-1"),
     "MF-1": ("MF", "Motor quạt làm mát dầu 88FC-1 – Siemens 11 kW"), "MF-2": ("MF", "Motor quạt làm mát dầu 88FC-2 – Siemens 11 kW"),
     "MF-3": ("MF", "Motor quạt làm mát dầu 88FC-3 – Siemens 11 kW"),
     "F-4": ("F", "Quạt hút bụi lọc quán tính (inertial filter)"), "F-5": ("F", "Quạt hút bụi lọc quán tính (inertial filter)"),
     "MF-4": ("MF", "Motor quạt lọc quán tính 88ED-1 – Flakt 7,5 kW"), "MF-5": ("MF", "Motor quạt lọc quán tính 88ED-2 – Flakt 7,5 kW"),
     "F-6": ("F", "Quạt thông gió vỏ máy chính/phụ – CBI 40.000 m³/h"), "F-7": ("F", "Quạt thông gió vỏ máy chính/phụ – CBI 40.000 m³/h"),
     "MF-6": ("MF", "Motor quạt thông gió 88BA-1 – ABB 37 kW"), "MF-7": ("MF", "Motor quạt thông gió 88BA-2 – ABB 37 kW"),
     "F-9": ("F", "Quạt bộ làm mát nước động cơ diesel"), "MF-9": ("MF", "Motor quạt làm mát diesel 88DW – 11 kW"),
     **{f"F-{n}": ("F", "Quạt làm mát máy phát") for n in (10, 11, 12, 13)},
     **{f"MF-{n}": ("MF", f"Motor quạt làm mát máy phát 88BG-{n-9} – 11 kW") for n in (10, 11, 12, 13)}}

def frac(dx, dy):
    return 0.02 + dx * 1.3 / 2600 * 0.96, 0.03 + dy * 1.3 / 1852 * 0.94

out_sheets, tags = [], {}
for p in range(1, 20):
    sid = f"VGT-{p:02d}"
    im = Image.open(f"{sid}.png")
    out_sheets.append({"id": sid, "kind": "PID", "unit": "19A", "dwg": f"SOM09996/1 tờ {p}", "title": "GT 10-GT-9001 – " + TITLES[p],
                       "img": f"img/{sid}.png", "w": im.width, "h": im.height, "src": "Vendor Data/10GT9001/PID GT9001.pdf – trang %d" % p})
log = []
for p, suf, dx, dy, vert in L:
    sid = f"VGT-{p:02d}"
    x, y = frac(dx, dy)
    w, h = (0.012, 0.062) if vert else (0.058, 0.013)
    W = json.load(open(f"ocr_{sid}.json"))
    best = None
    for t, wx, wy, ww, wh, c, r in W:
        if not re.search(r"9[0O]{2}[1Il]", t): continue
        m = re.search(r"/([A-Za-z]+)", t)
        if not m or m.group(1).upper() != re.match(r"[A-Z]+", suf).group(0): continue
        d = abs(wx - x) + abs(wy - y)
        if d < 0.035 and (best is None or d < best[0]): best = (d, wx, wy, ww, wh)
    if best:
        _, x, y, ww, wh = best
        if not vert: w, h = (max(ww, 0.05) if ww > 0.045 else w), max(0.010, min(wh, 0.02))
    log.append((sid, suf, bool(best)))
    tag = T + suf
    s, d = D[suf]
    e = tags.setdefault(tag, {"t": tag, "k": "equipment", "s": s, "d": d, "o": []})
    e["o"].append([sid, round(x, 4), round(y, 4), round(w, 4), round(h, 4)])
json.dump({"sheets": out_sheets, "tags": list(tags.values())}, open("vendor_pid_gt.json", "w"), ensure_ascii=False, indent=0)
print(len(tags), "tags,", sum(1 for l in log if l[2]), "/", len(log), "snapped to OCR")
print([l[:2] for l in log if not l[2]])
