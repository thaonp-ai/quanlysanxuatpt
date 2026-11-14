"""Bổ sung / hiệu chỉnh Công nghệ theo "Giáo trình tham khảo các cương vị" (G2-30-GT-01…09, ban hành 01/2024)
và Operation Manual gốc của Technip (Utilities, WWT, Flare & Ammonia storage).

apply(units, tags) được build_tech.py gọi sau cùng:
  - UNITS_NEW: trang Unit mới (37 khí nhiên liệu, 19B HRSG…)
  - PATCH[unit] = {"intro": …(thay), "pre": [mục chèn đầu], "add": [mục thêm cuối], "drop": [tiêu đề bỏ], "src": [nguồn thêm]}
  - TAG_NEW: đoạn thiết bị mới (ghi đè nếu trùng)
  - TAG_ADD[tag] = {"intro": …(thay, tùy chọn), "s": [mục thêm], "src": [nguồn thêm]}
"""
GTF = "Giáo trình tham khảo các cương vị/"


def gt(n, name):
    return [GTF + "STVB102393_G2-30-GT-%02d %s_vps.pdf" % (n, name), "Giáo trình G2-30-GT-%02d" % n]


GT01 = gt(1, "GT dao tao HT nuoc tho-sinh hoat-cuu hoa")
GT03 = gt(3, "GT dao tao HT nuoc cap-lo hoi phu tro va khi nhien lieu")
GT04 = gt(4, "GT dao tao HT khi nen-khi dieu khien")
GT06 = gt(6, "GT dao tao HT san xuat nuoc khu khoang")
GT07 = gt(7, "GT dao tao HT san xuat Nito")
GT08 = gt(8, "GT dao tao HT Gasturbine")
GT09 = gt(9, "GT dao tao HT bon chua NH3 & flare")
OMU = [GTF + "Operation Manual Utilities.doc", "Operation Manual Utilities (Technip)"]
OMW = [GTF + "Operating Manual WWT.doc", "Operating Manual WWT (Technip)"]
OMF = [GTF + "Operation Manual flare&ammonia storage.doc", "Operation Manual Flare & Ammonia storage (Technip)"]


def sh(dwg, label):
    return ["sheet:" + dwg, label]


def ent(t, intro, s=None, src=None):
    return {"t": t, "intro": intro, "s": s or [], "src": src or []}


UNITS_NEW, PATCH, TAG_NEW, TAG_ADD = {}, {}, {}, {}

# ============================================================ Unit 32 (+34 cứu hỏa)
PATCH["32"] = {
    "t": "Công nghệ Unit 32 – Nước thô, nước sinh hoạt & nước cứu hỏa",
    "intro": "Nước công nghiệp (mạng nước đô thị) từ ngoài hàng rào được nạp vào bồn nước thô 30-TK-2001 (thiết kế/làm việc 7.155/6.800 m³) qua LV-32001. "
             "Trong đó 6.000 m³ dưới đáy được dành riêng cho chữa cháy, vì vòi hút của bơm nước thô 30-P-2001A/B/C đặt ở cao độ tương ứng 6.000 m³, còn vòi hút bơm cứu hỏa đặt ở đáy bồn. "
             "Bơm nước thô (1 chạy, 2 dự phòng; 160 m³/h mỗi bơm) cấp nước cho cụm khử khoáng 30-PK-1001, header nước service và cụm xử lý nước sinh hoạt 30-PK-2001. "
             "Cụm 30-PK-2001 khử trùng bằng NaOCl, chứa ở bồn 30-TK-2002 (260/240 m³, đủ 5 ngày). Sau đó bơm 30-P-2002A/B đẩy nước qua lọc than hoạt tính và lọc tinh, cấp cho vòi tắm và rửa mắt khẩn cấp toàn nhà máy. "
             "Hai bơm 30-P-2002A/B được nối với máy phát diesel dự phòng. "
             "Hệ thống cứu hỏa (Unit 34 cũ) gồm 3 bơm chính 500 m³/h: 30-P-4001A chạy motor, 30-P-4001B/C chạy diesel. Ngoài ra có 2 bơm Jockey 30-P-4002A/B giữ áp mạng.",
    "add": [
        {"h": "Thông số thiết kế (giáo trình G2-30-GT-01)",
         "tb": [["Hạng mục", "Giá trị"],
                ["Nước sinh hoạt", "150 người × 0,3 m³/ngày = 45 m³/ngày; đáp ứng đỉnh gấp 6 lần; tối đa 22 m³/h"],
                ["Áp suất", "Clo hóa: vào 4,5 / ra ≥ 2 barg; lọc than + lọc tinh: vào 5,0 / ra ≥ 4 barg"],
                ["Nước công nghiệp / service / sinh hoạt", "Vận hành 2,5–3 / 5 / 3 barg; thiết kế 5 / 7 / 7 barg"],
                ["Nước thô (phân tích)", "pH 6,17–7,77; độ đục 0–0,5 NTU; TDS 47,7–71,45 mg/l; TSS 0–33 mg/l; độ cứng 12,3–34,5 mg/l CaCO₃; Cl⁻ ≤ 38,7 mg/l; Fe 0,03–0,19 mg/l"],
                ["Nước sinh hoạt", "Không có trực khuẩn đường ruột trong 100 ml; Cl₂ dư ≤ 0,1 mg/l trong mạng phân phối"]]},
        {"h": "Vận hành nước thô & nước sinh hoạt (G2-30-QT-043)",
         "ul": ["LV-32001 cấp nước vào 30-TK-2001: đóng khi LIT-32001 = 94,1 %, mở khi 93,5 %.",
                "Bơm nước thô khởi động ở chế độ Man từ LCP, sau đó mở dần van đẩy. Bộ điều khiển hồi lưu FIC-32002 đặt 90 m³/h. Phân tích nước thô 1 lần/tuần.",
                "Cấp nước vào 30-TK-2002: PCV-32701 đặt 5 barg, lưu lượng 22–50 m³/h (FI-32701). LV-32002 mở ở 40 %, đóng ở 80 % (LIT-32002).",
                "Bơm NaOCl 30-PK-2001/P1A/B (stroke 40 %, van tuần hoàn về bồn mở 100 %):",
                "• tự chạy khi LV-32002 mở và AIT-32201 thấp (1,1 ppm);",
                "• tự dừng khi LV-32002 đóng hoặc AIT-32201 cao (3,5 ppm).",
                "Bơm shock 30-PK-2001/P2 châm NaOCl vào bồn nước thô 30-TK-2001 mỗi tháng 1 lần. Mức bồn NaOCl /TK1 giữ 25–100 cm; bồn mức thấp thì các bơm tự dừng.",
                "Lọc than /FL2A/B (1 chạy, 1 dự phòng) tự tái sinh sau 12 giờ hoặc khi ΔP cao PDAH-32201 = 0,7 bar:",
                "• rửa ngược 45 m³/h trong 10 phút (XV-32205/32202);",
                "• rửa xuôi 22 m³/h trong 5 phút (XV-32206/32204).",
                "Lọc tinh /FL1A/B chuyển và vệ sinh bằng tay khi PDI-32701 = 0,7 bar.",
                "Chỉ ngừng hệ thống khi nhà máy đã ngừng hoàn toàn. Ngừng ngắn hạn: giữ mức bồn cao nhất, không xả."]},
        {"h": "Liên động nước thô & nước sinh hoạt",
         "tb": [["Interlock", "Tín hiệu", "Tác động"],
                ["30-I-32001", "LIT-32001", "H 94,1 %: đóng LV-32001; L 93,5 %: mở LV-32001"],
                ["30-I-32002", "LIT-32001", "LL 86 %: dừng 30-P-2001A/B/C và 30-PK-1001/P3"],
                ["30-I-32003", "LIT-32002", "H 80 %: đóng LV-32002; L 40 %: mở LV-32002"],
                ["30-I-32004", "LIT-32002", "LL 20 %: dừng 30-P-2002A/B"]]},
        {"h": "Hệ thống nước cứu hỏa (Unit 34)",
         "ul": ["Nhu cầu nước chữa cháy lớn nhất 900 m³/h; 5.400 m³ trong bồn đủ chạy 6 giờ hết công suất. Khi thiếu nước thô có thể dùng nước sông từ bể tháp làm mát.",
                "30-P-4001A (motor 6,6 kV) và 30-P-4001B/C (động cơ diesel): mỗi bơm 500 m³/h (55 % nhu cầu lớn nhất), áp đẩy 9 barg. "
                "Vì vậy hệ vẫn đủ nước khi mất 1 bơm hoặc mất điện. Thiết kế theo NFPA 20.",
                "Bơm Jockey 30-P-4002A/B (1 chạy, 1 dự phòng): 50 m³/h, 7 barg. Bù rò rỉ, giữ áp mạng > 7 barg, để các bơm chính tự khởi động lần lượt khi áp giảm.",
                "Bơm chính tự khởi động theo áp mạng:",
                "• PSL-34201A = 6,0 barg → 30-P-4001A;",
                "• PSL-34201B = 5,5 barg → 30-P-4001B;",
                "• PSL-34201C = 5,0 barg → 30-P-4001C.",
                "Tủ LCP bơm 30-P-4001A có cần EMERGENCY RUN. Bơm diesel: MAIN SWITCH và công tắc trên động cơ để ở AUTO; 2 bộ ắc quy 24–28 V; bồn dầu diesel ≈141,5 gallon (chạy 8 giờ, 0,268 GPM).",
                "Thử định kỳ (G2-30-HD-022): đóng van đẩy, mở đường tuần hoàn về 30-TK-2001, xả áp để bơm tự chạy. "
                "Sau đó ghi áp PI-34507A ở 50 / 100 / 150 % lưu lượng (250 / 500 / 750 m³/h)."]},
    ],
    "src": [GT01, OMU],
}
P4001 = ent("Bơm cứu hỏa chính 30-P-4001A/B/C",
            "Ba bơm ly tâm 500 m³/h, đẩy 9 barg (thiết kế theo NFPA 20). 30-P-4001A chạy motor ABB 6,6 kV; 30-P-4001B/C chạy động cơ diesel (≈242 kW). "
            "Hút từ đáy bồn 30-TK-2001, phần 6.000 m³ dành riêng cho chữa cháy. Bơm tự khởi động lần lượt theo áp mạng: PSL-34201A 6,0 / B 5,5 / C 5,0 barg. "
            "Chuẩn bị chạy: van hút và van đẩy mở hoàn toàn, van tuần hoàn về bồn đóng, mức dầu bôi trơn và nước làm mát đủ, bồn diesel đủ, sạc ắc quy (24–28 V) và nguồn AC 220 V bật.",
            [{"h": "Thử liên động & thử tải (G2-30-HD-022)",
              "ul": ["Bơm Jockey đang chạy, áp mạng > 7 barg. Đóng van đẩy, mở van tuần hoàn của bơm cần thử, mở van xả đầu đẩy để hạ áp tới giá trị cài đặt thì bơm tự chạy.",
                     "Ghi áp PI-34507A khi bơm khởi động và ở 250 / 500 / 750 m³/h (50 / 100 / 150 %). Xong thì dừng bơm và đặt lại AUTO."]}],
            [GT01, OMU])
P4002 = ent("Bơm Jockey 30-P-4002A/B",
            "Hai bơm motor 400 V, 50 m³/h, đẩy 7 barg (1 chạy, 1 dự phòng). Giữ áp mạng nước cứu hỏa ổn định (> 7 barg) và bù lượng rò rỉ, để bơm chính chỉ chạy khi có nhu cầu chữa cháy. "
            "Vận hành tay: công tắc H-O-A trên LCP để HAND, rồi nhấn START/STOP. Bình thường để AUTO.",
            src=[GT01, OMU])
TAG_NEW.update({"30-P-4001": P4001, "30-P-4002": P4002, "30-MP-4001": P4001, "30-MP-4002": P4002})
TAG_ADD["30-TK-2001"] = {"s": [{"h": "Dành nước chữa cháy (giáo trình)",
                                 "ul": ["Thiết kế/làm việc 7.155/6.800 m³. 6.000 m³ dưới cùng chỉ dành cho bơm cứu hỏa, vì vòi hút bơm nước thô đặt cao hơn. "
                                        "Mức LL 86 % (LIT-32001) dừng bơm nước thô và 30-PK-1001/P3. Hằng tháng shock NaOCl bằng 30-PK-2001/P2."]}],
                         "src": [GT01]}
TAG_ADD["30-PK-2001"] = {"s": [{"h": "Vận hành (giáo trình G2-30-GT-01)",
                                 "ul": ["Bơm châm P1A/B tự chạy khi LV-32002 mở và AIT-32201 ≤ 1,1 ppm, tự dừng ở 3,5 ppm hoặc khi LV-32002 đóng.",
                                        "Lọc than FL2A/B tự tái sinh sau 12 giờ hoặc khi ΔP 0,7 bar: rửa ngược 45 m³/h trong 10 phút, rửa xuôi 22 m³/h trong 5 phút. Lọc tinh FL1A/B vệ sinh khi ΔP 0,7 bar.",
                                        "Than hoạt tính khử Cl₂ dư và hấp phụ CHCl₃ (giới hạn 100 ppb). Cl₂ dư trong mạng ≤ 0,1 mg/l."]}],
                         "src": [GT01]}
TAG_ADD["30-P-2002"] = {"s": [{"h": "Ghi chú (giáo trình)", "ul": ["22 m³/h + 1,4 m³/h tuần hoàn tối thiểu. Được cấp điện từ máy phát diesel dự phòng khi mất điện lưới. Dừng khi LIT-32002 LL 20 % (30-I-32004)."]}], "src": [GT01]}
TAG_ADD["30-P-2001"] = {"s": [{"h": "Ghi chú (giáo trình)", "ul": ["1 chạy, 2 dự phòng; khởi động Man từ LCP. FIC-32002 tuần hoàn về bồn đặt 90 m³/h. Dừng khi LIT-32001 LL 86 % (30-I-32002)."]}], "src": [GT01]}

# ============================================================ Unit 18
PATCH["18"] = {
    "add": [
        {"h": "Nước cấp lò & khử khí (giáo trình G2-30-GT-03)",
         "ul": ["Nước khử khoáng từ 30-P-1002A/B được gia nhiệt ở các TĐN của X.Amonia (10-E-3004/3005), rồi vào thiết bị khử khí 10-PK-8004 qua FV-8003 (FIC-8003 ≈350 t/h). "
                "Tại đây nước đi ngược chiều với hơi LP để khử O₂ và CO₂, sau đó chứa ở bồn 10-V-8001 (132,9 m³).",
                "Hộ tiêu thụ nước cấp HP: lò hơi phụ 10-B-8001, lò hơi nhiệt thừa 10-B-9001, lò HHP X.Amonia, xưởng UFC85, quench water.",
                "Thông số vận hành:",
                "• PIC-8001 1,2–1,5 barg; nước demi về bồn (TI-8004) 115–120 °C; nước trong bồn (TI-8003) 120–130 °C;",
                "• bơm 10-P-8002: áp hút 1,2–3,2 barg, áp đẩy 56–60 barg.",
                "Khởi động khi chưa có hơi LP: điền demi đến ≈80 % (LIC-8005), chạy bơm alkalinizing (pH 9–9,5) và oxyscavenger (stroke 70–80 %), chạy 10-P-8002B tuần hoàn. "
                "Khi có hơi LP: sục hơi đáy bồn tới ≈130 °C, rồi chuyển sang PV-8001.",
                "Chỉ tiêu nước cấp: O₂ < 0,02; độ cứng < 1; Fe < 0,05; Cu < 0,01; SiO₂ < 0,02; dầu < 1 mg/kg; pH 9–9,5."]},
        {"h": "Liên động nước cấp lò",
         "tb": [["Interlock", "Tín hiệu", "Cài đặt", "Tác động"],
                ["10-I-8020", "LIT-8001A/B/C (LALL-8001)", "45 % (≈5,6 % LIC-8005)", "Trip 10-I-8001/2/4/5"],
                ["10-I-8021", "LIT-8004 (LAHH-8004)", "47,3 % (≈95 % LIC-8005)", "Mở hoàn toàn HV-8004A"],
                ["10-I-8004 / 8005", "PIT-8004 / 8005 (PALL)", "1 barg", "Trip 10-P-8002A / B"],
                ["10-I-8006", "PIT-8006 (PALL)", "45 barg", "Tự khởi động 10-P-8002B"],
                ["10-I-8014 / 8015", "Nhiệt gối TE-8280/81, 8310/11; rung XE", "100 °C; 70 µm; 6 mm/s", "Trip 10-P-8002A / B"]]},
        {"h": "Khởi động lò 10-B-8001 (G2-30-QT-057)",
         "ul": ["Điều kiện:",
                "• khí nén 8–9 barg; khí điều khiển 7–8 barg; khí nhiên liệu ở 30-V-7002 6–6,5 barg;",
                "• nước cấp 55–60 barg; mức bao hơi LIC-8250 ≈70 %;",
                "• inlet damper FV-8250 đóng; air register XV-8212/22/32/42 mở; van xả khởi động HV-8251 và các van xả quá nhiệt mở.",
                "Chạy quạt FD MK1 tại chỗ. BMS tự purge 5 phút ở lưu lượng gió ≥ 25 % MCR (≈30.245 Nm³/h). Sau đó leak test từ DCS. "
                "Đánh lửa đầu đốt đầu tiên; nếu không thành công thì logic quay lại bước purge.",
                "Tốc độ gia nhiệt: khởi động nguội 30–50 °C/h, khởi động nóng 60–80 °C/h. Giữ mức bao hơi 55–70 %. Áp bao hơi 1,5–2 barg thì đóng vent bao hơi.",
                "Áp 15–20 barg: chạy bơm phosphate 10-PK-8001. Khi gần áp vận hành (thấp hơn ≈2 bar): sấy và cân bằng qua bypass HV-8250, rồi hòa hơi.",
                "Vận hành ổn định:",
                "• xả liên tục CBD ≈1 % tải; xả đáy IBD mỗi ca 1–5 phút;",
                "• HIC-8250A ở AUTO theo áp mạng HP (PIC-4048).",
                "Ngừng không giữ áp: giảm về 10 % MCR, tắt đầu đốt, quạt làm nguội 50 °C/h, mở vent ở 2 barg, dừng quạt khi nước < 80 °C, rồi bảo quản ướt hoặc khô. "
                "Ngừng giữ áp: tắt đầu đốt, đóng van hơi chính, van nước cấp và inlet damper."]},
        {"h": "Nguyên nhân MFT (Master Fuel Trip)",
         "tb": [["Nguyên nhân", "Tín hiệu", "Cài đặt"],
                ["Nút dừng khẩn BLP / CCR", "HS-8201 / HS-8202", "—"],
                ["Mức bao hơi thấp", "LIT-8251/52/53 (2oo3)", "7,1 %"],
                ["Gió vào buồng đốt thấp", "FIT-8254/55/56 (2oo3)", "24.916 Nm³/h"],
                ["Tốc độ quạt FD thấp", "SSLL-8290A/B/C (2oo3)", "900 v/ph"],
                ["Áp buồng đốt cao", "PIT-8251A/B/C (2oo3)", "45 mbarg"],
                ["Áp khí nhiên liệu thấp (sau khi burner đầu tiên tắt)", "PIT-8204A/B/C (2oo3)", "15 mbarg"],
                ["Áp khí nhiên liệu cao", "PIT-8203A/B/C (2oo3)", "2,6 barg"],
                ["Mất lửa / mất khí nhiên liệu", "XA-8204 / XA-8203", "—"]],
         "p": ["Leak test 2 bước:",
               "• Bước 1: đóng vent XV-8202; sau 2 phút PIT-8204 phải vẫn ≤ 0,02 barg.",
               "• Bước 2: FV-8201 mở 10 %, XV-8201 mở tới khi PIT-8203 đạt 1,8 barg rồi đóng; sau 2 phút áp phải vẫn ≥ 2 barg.",
               "Pilot: đánh lửa 10 giây; nếu không thấy lửa thì chờ 1 phút mới đánh lại. Pilot tự tắt sau 3 phút nếu không đốt burner."]},
        {"h": "Chỉ tiêu nước lò & hơi HP",
         "tb": [["Nước lò", "Giá trị", "Hơi HP", "Giá trị"],
                ["pH", "9–9,5", "Áp / nhiệt", "39 ± 0,5 barg / 380 ± 5 °C"],
                ["Độ dẫn", "< 150 µS/cm", "Độ dẫn", "< 0,2 µS/cm"],
                ["PO₄³⁻", "< 3 mg/kg (vận hành 3–5 mg/l)", "SiO₂ / Fe", "< 0,02 / < 0,02 mg/kg"],
                ["SiO₂ / độ kiềm", "< 3 / < 15 mg/kg", "Na⁺+K⁺ / Cu", "< 0,01 / < 0,003 mg/kg"]],
         "p": ["Không pha phosphate quá đặc: độ tan muối phosphate giảm mạnh ở ≈250 °C, dễ tắc đường châm. "
               "Nếu châm càng nhiều phosphate mà pH nước lò càng giảm và nước xả có màu nâu đỏ, có thể đang ăn mòn axit trong ống sinh hơi (Na₃PO₄ phản ứng với lớp magnetite)."]},
        {"h": "Blowdown & condensate",
         "ul": ["CBD của 10-B-8001 và 10-B-9001 về 10-V-8002 (3,5 barg, 148 °C). Hơi flash đi vào mạng LP; nước qua 10-E-8001 gia nhiệt nước demi (148 → 50 °C), rồi về 10-V-8003 cùng với IBD.",
                "Condensate LP và nước ngưng từ dump condenser 10-E-8002A~D (mỗi bộ 17 t/h hơi LP, quạt 135.322 m³/h) về 10-V-8004. "
                "Bơm 10-P-8003A/B (30 m³/h) đưa condensate về 10-PK-8004."]},
    ],
    "src": [GT03],
}
TAG_ADD["10-B-8001/K1"] = {"s": [{"h": "Thông số & chuyển đổi dẫn động (giáo trình)",
                                   "tb": [["Điểm vận hành", "Design", "100 % MCR", "50 % MCR", "10 % MCR"],
                                          ["Lưu lượng (kg/h)", "180.355", "156.830", "80.350", "39.250"],
                                          ["Áp ra (mmH₂O)", "814", "616", "159", "37"],
                                          ["Công suất (kW)", "448", "362", "196", "171"],
                                          ["Inlet damper (%)", "100", "60", "40", "20"],
                                          ["Hơi tuabin (kg/h)", "13.840", "11.170", "7.260", "6.680"]],
                                   "p": ["Quạt chạy 1.480 v/ph. Khi tốc độ < 1.390 v/ph (SAL-8290), MCC tự khởi động motor MK1. Nếu sau 5 giây vẫn còn tốc độ thấp thì báo động MXABM-8001 (không chuyển đổi được)."]}],
                           "src": [GT03]}
TAG_ADD["10-B-8001/STK1"] = {"s": [{"h": "Thông số (giáo trình)", "ul": ["Min/Max governor 1.150/1.560 v/ph; vận hành 1.480 v/ph; quá tốc EOT 1.660 v/ph, MOT 1.720 v/ph.",
                                                                       "Tự khởi động MK1 ở 1.340 v/ph (SSL-8290). Từ Min.GS có thể chuyển sang ENABLE REM. SET POINT để chỉnh tốc độ từ DCS (GRA075)."]}],
                             "src": [GT03]}
TAG_ADD["10-B-8001/MK1"] = {"s": [{"h": "Thông số (giáo trình)", "ul": ["500 kW, 6,6 kV, 53 A, 1.483 v/ph. Điều kiện khởi động:",
                                                                      "• inlet damper FV-8250 đóng; air register mở;",
                                                                      "• không trong bước thông gió tự nhiên (XL-8203A/B);",
                                                                      "• đã reset tại trạm điện số 1."]}],
                            "src": [GT03]}
TAG_ADD["10-P-8002"] = {"s": [{"h": "Thông số & vận hành (giáo trình)",
                                "ul": ["Bơm ly tâm 6 cấp, 100/230 m³/h, đẩy 53,2 barg (ΔP 50,7 bar). Van tuần hoàn tự động ARV TDM137 (Q min 90 m³/h).",
                                       "Nước làm mát fresh 3,4 m³/h.",
                                       "Trip áp hút thấp 1 barg (10-I-8004/8005). PALL-8006 = 45 barg thì tự chạy 10-P-8002B.",
                                       "Tuabin 10-STP-8002A:",
                                       "• sấy tới ≈300 °C (phía HP) / 200 °C (phía LP); chạy Idle 1.100 v/ph trong 30 phút;",
                                       "• tốc độ vận hành 2.980 v/ph; điều khiển từ DCS được khi ≥ Min.GS 2.235 v/ph;",
                                       "• quá tốc điện 3.338 ± 50, quá tốc cơ 3.450 ± 60 v/ph."]}],
                        "src": [GT03]}
TAG_ADD["10-PK-8004"] = {"s": [{"h": "Thông số (giáo trình)", "ul": ["10-PK-8004: Ø2,6 × 4,5 m, 18,17 m³, thiết kế 3,9/−0,5 barg, 310 °C. Bồn 10-V-8001: Ø3,7 × 11,1 m, 132,92 m³, 3,9 barg, 157 °C.",
                                                                   "Vận hành: PIC-8001 1,2–1,5 barg; nước 120–130 °C; LALL-8001 45 %; LAHH-8004 47,3 % (mở HV-8004A)."]}],
                         "src": [GT03]}
TAG_ADD["10-V-8001"] = TAG_ADD["10-PK-8004"]

# ============================================================ Unit 37 khí nhiên liệu (mới)
PFD37 = sh("2539-37-PFD-0010-01-01 (trang 1)", "PFD 2539-37 Fuel gas (as-built)")
PID37 = sh("2098-37-PID-0031-01", "P&ID 2098-37-PID-0031-01 Fuel gas")
UNITS_NEW["37"] = {
    "t": "Công nghệ Unit 37 – Khí nhiên liệu",
    "intro": "Khí thiên nhiên từ trạm khí (B.L., 24,5 barg, 18–36 °C) được cấp trực tiếp làm khí nguyên liệu cho X.Amonia (feed gas) và cho xưởng NPK. "
             "Đồng thời khí được giảm áp qua PV-37001 vào bình đệm cao áp 30-V-7001 (24 barg) để cấp cho tuabin khí 10-GT-9001. "
             "Từ 30-V-7001, khí giảm áp tiếp qua PV-37002 vào bình đệm thấp áp 30-V-7002 (6 barg) để cấp cho lò reforming 10-H-2001, lò hơi phụ 10-B-8001, HRSG 10-B-9001, đuốc 40-PK-1001/1002 và cụm 20-PK-1005. "
             "Bình nhỏ 30-V-7003 (PIC-37003) cấp khí cho hệ thống đuốc. Đường khí được traced hơi để giữ nhiệt độ ≥ 18 °C (thường 19–50 °C), tránh ngưng hydrocacbon nặng.",
    "s": [
        {"h": "Lưu lượng (PFD 2539-37 as-built, kg/h)",
         "tb": [["Dòng", "Mô tả", "Case 2", "Case 3"],
                ["37.1", "Khí thiên nhiên từ B.L. (24,5 barg)", "58.082", "50.793"],
                ["37.3", "Feed gas sang X.Amonia", "32.069", "32.069"],
                ["37.2", "Khí HP vào 30-V-7001 (24 barg)", "20.914", "17.525"],
                ["37.4", "Khí HP tới tuabin khí 10-GT-9001", "5.637", "5.637"],
                ["37.9", "Khí LP tới lò reforming 10-H-2001 (6,5 barg)", "10.161", "10.133"],
                ["37.6", "Khí LP tới lò hơi 10-B-8001 / 10-B-9001", "5.076", "1.755"],
                ["37.5", "Khí LP tới hệ thống đuốc", "4.399", "499"],
                ["37.10", "Khí LP tới 20-PK-1005", "3.950", "0"],
                ["37.7 / 37.8", "Khí LP tới đuốc 40-PK-1002 / 40-PK-1001", "12 / 437", "12 / 437"],
                ["37.11", "Khí thiên nhiên tới nhà máy NPK", "700", "700"]],
         "p": ["Công suất van theo thiết kế: PV-37001 tối đa 34.317 Nm³/h; PV-37002 tối đa 27.053 Nm³/h."]},
        {"h": "Chất lượng khí thiên nhiên",
         "tb": [["Chỉ tiêu", "AMF", "GPP", "Revamp"],
                ["Nhiệt độ (°C)", "18–36", "18–36", "18–60"],
                ["Áp suất (barg)", "24,5 (39,2 max)", "24,5 (39,2 max)", "24,5–40"],
                ["Điểm sương HC @25 barg (°C)", "−1", "−42", "—"],
                ["Khối lượng phân tử (g/mol)", "20,65", "18,68", "18,78"],
                ["Nhiệt trị tổng (MJ/Nm³)", "46,92", "42,85", "38,995"],
                ["C1 / C2 / C3 (%mol)", "78,98 / 12,20 / 5,76", "83,31 / 14,57 / 1,60", "88,68 / 4,71 / 2,67"],
                ["CO₂ / N₂ (%mol)", "0,015 / 0,30", "0,014 / 0,26", "2,23 / 0,27"]],
         "p": ["Tổng lưu huỳnh tối đa 23 ppmv H₂S; lưu huỳnh hữu cơ tối đa 1 ppmv. AMF là nguồn khí trường hợp bất thường; GPP là nguồn khí bình thường (theo OM Technip)."]},
        {"h": "Thiết bị & cài đặt",
         "tb": [["Tag", "Chức năng", "Thông số", "Báo động"],
                ["30-V-7001", "Bình đệm khí nhiên liệu cao áp (đứng)", "Ø1.200 × 1.800 mm; 2,4 m³; vận hành 24 barg; thiết kế 28 barg / 60 °C", "PIC-37001: PAH 26,5 / PAL 21,5 barg"],
                ["30-V-7002", "Bình đệm khí nhiên liệu thấp áp (đứng)", "Ø1.100 × 1.500 mm; 1,7 m³; vận hành 6 barg; thiết kế 10 barg, −10/60 °C", "PIC-37002: PAH 6,7 / PAL 5,3 barg"],
                ["30-V-7003", "Bình khí nhiên liệu cho đuốc", "PIC-37003", "PAH 6,7 / PAL 5,3 barg"]],
         "p": ["Các bình đều có công tắc mức LAH-37001/2/3 báo khi có lỏng ngưng; xả lỏng bằng tay. "
               "Áp HP thấp-thấp sẽ dừng tuabin khí 10-GT-9001. Khi áp giảm, kiểm tra: lưu lượng tiêu thụ HP (FI-9001) và LP qua PV-37002, hoạt động của PIC-37001/PV-37001, và áp khí tại B.L."]},
        {"h": "Vận hành",
         "ul": ["Quy trình vận hành hệ thống khí nhiên liệu G2-30-QT-056.",
                "Trước khi khởi động lò hơi phụ: áp 30-V-7002 (PIT-37002) ở 6–6,5 barg."]},
    ],
    "src": [GT03, OMU, PFD37, PID37],
}
TAG_NEW["30-V-7001"] = ent("Bình đệm khí nhiên liệu cao áp 30-V-7001",
                           "Bình đứng Ø1.200 × 1.800 mm (2,4 m³). Vận hành 24 barg, 18–36 °C; thiết kế 28 barg / 60 °C. Van an toàn 12\". "
                           "Nhận khí thiên nhiên qua PV-37001 (PIC-37001, tối đa 34.317 Nm³/h). Cấp khí HP cho tuabin khí 10-GT-9001 và cho bình thấp áp 30-V-7002 qua PV-37002. "
                           "Báo động PAH 26,5 / PAL 21,5 barg; áp HP thấp-thấp dừng tuabin khí. LAH-37001 báo có lỏng ngưng.",
                           src=[GT03, OMU, PFD37, PID37])
TAG_NEW["30-V-7002"] = ent("Bình đệm khí nhiên liệu thấp áp 30-V-7002",
                           "Bình đứng Ø1.100 × 1.500 mm (1,7 m³). Vận hành 6 barg; thiết kế 10 barg, −10/60 °C. Van an toàn 8\". "
                           "Nhận khí qua PV-37002 (PIC-37002, tối đa 27.053 Nm³/h). Cấp khí LP cho lò reforming 10-H-2001, lò hơi phụ 10-B-8001, HRSG 10-B-9001, đuốc và 20-PK-1005. "
                           "Báo động PAH 6,7 / PAL 5,3 barg. Trước khi đốt lò hơi phụ, áp phải ở 6–6,5 barg.",
                           src=[GT03, OMU, PFD37, PID37])

# ============================================================ Unit 35 khí nén – khí điều khiển
PATCH["35"] = {
    "add": [
        {"h": "Thiết kế & chỉ tiêu (giáo trình G2-30-GT-04)",
         "tb": [["Hạng mục", "Khí điều khiển", "Khí nén"],
                ["Nhu cầu thiết kế", "2.920 Nm³/h", "2.680 Nm³/h (tổng 5.600 Nm³/h, kể cả ≈500 Nm³/h hao ở máy sấy)"],
                ["Áp tại nơi sản xuất / tại hộ tiêu thụ", "8,5 / 7,5 barg (tối thiểu 4)", "9 / 8 barg"],
                ["Thiết kế", "11 barg / 75 °C", "11 barg / 75 °C"],
                ["Nhiệt độ / điểm sương", "45 °C / −25 °C", "45 °C / —"],
                ["Dầu, bụi", "Không có", "Không có"]],
         "p": ["Hộ tiêu thụ lớn:",
               "• cụm nitơ 30-PK-6001: tối đa 1.096 Nm³/h;",
               "• khí thụ động hóa X.Urê: 700 Nm³/h;",
               "• 20-E-1001, 20-K-1001: liên tục;",
               "• tiêu thụ gián đoạn: tối đa ≈150 Nm³/h.",
               "Bình 30-V-5001 (28,5 m³) và 30-V-5002 (154 m³) mỗi bình đủ cấp ≈10 phút khi áp giảm từ 8,1 xuống 5 barg. "
               "Có thêm dòng khí bổ sung từ máy nén khí công nghệ 10-K-4021 của X.Amonia về 30-V-5001."]},
        {"h": "Thiếu khí điều khiển (IS-6)",
         "ul": ["Khi 2/3 tín hiệu PIT-35004 xuống 5 barg: sau 3 giây đóng PV-35003 và PV-35004 (cắt khí nén để ưu tiên khí điều khiển); sau thêm 30 giây dừng X.Urê.",
                "Khi thiếu khí kéo dài (máy nén sự cố, hoặc 2 máy đang bảo dưỡng), X.Phụ trợ báo X.Amonia mở FV-4001 (FIC-4001) để cấp process air sang. "
                "Khi đó ưu tiên sản xuất khí điều khiển, chấp nhận giảm tải amoniac."]},
        {"h": "Cài đặt bảo vệ máy nén 30-K-5001A~E",
         "tb": [["Tag", "Thông số", "Cài đặt"],
                ["PDT-35215", "ΔP lọc gió", "PDAH −0,050 / PDAHH −0,060 bar"],
                ["PT-35207", "Áp vào cấp HP (intercooler)", "PAL 3 / PALL 1 bar"],
                ["PT-35206", "Áp dầu bôi trơn", "PAL 1,3 / PALL 1,2 bar"],
                ["PT-35208", "Áp ra cụm máy", "PAL 4 / PAH 10,4 / PAHH 10,5 bar"],
                ["TT-35210 / 35215", "Nhiệt ra cấp LP / HP", "TAH 225 / TAHH 235 °C"],
                ["TT-35214 / 35217", "Nhiệt vào cấp HP / dầu", "TAH 65 / TAHH 75 °C"],
                ["TT-35211 / 35212", "Nước làm mát vào / ra", "TAH 42 °C / TAH 50, TAHH 60 °C"],
                ["VAHK-35001E1~E5", "Rung các gối LP/HP, hộp số", "4,5 g"],
                ["TE-35218 / 35219", "Gối motor DE / NDE", "TAH 110 / TAHH 115 °C"]],
         "p": ["Khởi động: mức dầu ≥ 50 %, nước làm mát mở, reset tới khi màn hình báo \"All protection functions are OK\". "
               "Máy chạy không tải, sau 25 giây tự chuyển sang có tải. Giá trị load/unload chỉnh ở Menu → Regulation (Elektronikon)."]},
        {"h": "Máy sấy khí điều khiển",
         "tb": [["Thông số", "30-DR-5001 (Delair)", "30-DR-5002 (Hankison)"],
                ["Năng suất / khí vào", "1.820 / 2.120 Nm³/h", "1.100 / 1.265 Nm³/h"],
                ["Chu kỳ", "12 phút (sấy 6, tái sinh 6)", "10 phút (sấy 5, tái sinh 5)"],
                ["Xả áp / thổi / tăng áp", "25 s / 250 s / 60 s; song song 25 s", "— / 240 s / 60 s"],
                ["Khí tái sinh", "320 Nm³/h (chỉnh FI-35701 ≈300)", "165 Nm³/h (FI-35703 ≈200)"],
                ["Chất hấp phụ", "Activated alumina 450 kg/tháp (Ø700 × 1.600)", "Tháp Ø457 × 1.650"]],
         "p": ["Máy sấy không có tín hiệu tự dừng. 30-DR-5002 báo áp cao khi > 0,7 barg trong lúc thổi quá 30 giây, và báo áp thấp khi < 3,1 barg trong lúc tăng áp quá 45 giây. "
               "Điểm sương ra (AIT-35201) phải < −25 °C."]},
    ],
    "src": [GT04, OMU],
}
TAG_ADD["30-K-5001"] = {"s": [{"h": "Theo giáo trình G2-30-GT-04",
                                "ul": ["Máy nén trục vít không dầu 2 cấp: cấp 1 nén tới ≈3 barg, ≈200 °C → intercooler → cấp 2 nén tới 9 barg → aftercooler → 30-V-5001.",
                                       "Design (Atlas Copco): 1.498 Nm³/h ± 4 %; trục 189,8 kW; 1.485 v/ph; nước làm mát 37 °C, tăng 9 °C. Thường 4 máy chạy, 1 dự phòng.",
                                       "Bảo vệ: áp dầu PALL 1,2 bar; nhiệt ra cấp TAHH 235 °C; áp ra PAHH 10,5 bar; rung 4,5 g; gối motor 115 °C."]}],
                        "src": [GT04]}
for k in ("30-K-5001A", "30-K-5001B", "30-K-5001C", "30-K-5001D", "30-K-5001E"):
    TAG_ADD[k] = TAG_ADD["30-K-5001"]

# ============================================================ Unit 31 Demi
PATCH["31"] = {
    "add": [
        {"h": "Theo giáo trình G2-30-GT-06",
         "ul": ["3 chuyền giống nhau, bình thường 2 chạy, 1 dự phòng hoặc tái sinh.",
                "Chuyền khử ion: nước thô đã khử Cl₂ bằng Na₂SO₃ (P6A/B) trộn với nước ngưng công nghệ → cation V1 → khử khí V2 (tách CO₂) → anion V3 → bồn nước khử ion 30-TK-1001 (500 m³). "
                "Bồn này nhận thêm nước ngưng hơi và nước ngưng tuabin. Nước ngưng tuabin nếu nhiễm nước sông thì đưa về đầu chuyền cation hoặc degasifier.",
                "30-P-1001A/B → mixed bed V4A/B/C (2 chạy, 1 dự phòng/tái sinh) → bồn nước khử khoáng 30-TK-1002 (9.000 m³, đủ 24 giờ) → 30-P-1002A/B cấp đi.",
                "Nước tái sinh nhiễm hóa chất về bể trung hòa /BA1, trung hòa bằng H₂SO₄ hoặc NaOH rồi sang bể 30-BA-3001. "
                "Nước rửa ống góp giữa, rửa ngược và rửa cuối đi thẳng về 30-BA-3001.",
                "Điều kiện khởi động: mức 30-TK-2001 > 86 %, có ít nhất 1 bơm nước thô chạy; P2A~C, K2A~C, P6A/B ở Auto; công tắc chuyền ở \"SVC\". "
                "Rửa anion phải xuống < 20 µS/cm, rửa mixed bed < 0,2 µS/cm, trong vòng 10 phút; nếu không đạt thì báo động (hoặc người vận hành nhấn Advance).",
                "Quy trình liên quan: G2-30-QT-040 (vận hành), G2-00-PA-380 (nước khử khoáng nhiễm axit), G2-00-PA-388 (vệ sinh bồn axit)."]},
        {"h": "Thông số bình trao đổi (giáo trình)",
         "tb": [["Bình", "Kích thước", "Nhựa", "Chu kỳ / ngưỡng tái sinh", "Hóa chất / lần"],
                ["Cation V1A/B/C", "Ø2.000 × 2.600, lót cao su 3 mm", "3.960 l Amberlite IRC 120NA", "150 m³/h; 1.800 m³ nước thô (4.000 m³ nước hỗn hợp) hoặc 20 µS/cm", "396 kg H₂SO₄ 100 % (2 bước 1,6 % → 4 %)"],
                ["Khử khí V2A/B/C", "Tháp Ø1.800 × 3.300 + bồn ngang Ø2.400 × 4.500", "—", "Bơm P2 170 m³/h, 30 m; quạt K2 3.100 m³/h", "—"],
                ["Anion V3A/B/C", "Ø2.000 × 3.000", "4.800 l Amberlite 402Cl", "12 giờ", "480 kg NaOH 100 % (5 %)"],
                ["Mixed bed V4A/B/C", "—", "2.650 l HPR 1200NA + 2.650 l HPR 4200CL", "200 m³/h; 24.000 m³ (120 giờ) hoặc ≥ 0,2 µS/cm", "265 kg H₂SO₄ + 265 kg NaOH"]],
         "p": ["Tái sinh cation theo 2 bước: H₂SO₄ 1,6 % trước để tránh kết tủa CaSO₄/MgSO₄ bám lên hạt nhựa, sau đó 4 %. "
               "Nước thải mỗi lần tái sinh cation ≈71 m³ (56 m³ về bể trung hòa). Rửa axit trên PLC hiện đặt 30 phút. "
               "Tái sinh mixed bed có bước trộn khí nén 0,4 barg trong 10 phút, rửa cuối 200 m³/h."]},
        {"h": "Chỉ tiêu nước khử khoáng (giáo trình)",
         "tb": [["Chỉ tiêu", "Giá trị"], ["pH", "6,5–7"], ["Độ dẫn điện", "< 0,2 µS/cm"], ["SiO₂ / Fe", "< 0,02 / < 0,02 mg/l"],
                ["Cl⁻ / Na⁺", "< 0,1 / < 0,02 mg/l"], ["NH₃ / urê", "≤ 3 / ≤ 3 ppm"], ["Áp / nhiệt", "Ra ≥ 2,5 barg; 45 °C"]]},
    ],
    "src": [GT06, OMU],
}

# ============================================================ Unit 36 nitơ
PATCH["36"] = {
    "add": [
        {"h": "Theo giáo trình G2-30-GT-07",
         "ul": ["Khí nén vào bình đệm /V1 (≈9,1 barg). Khi khởi động, XYS-36257 tăng áp từ từ; XV-36205 chỉ mở khi chênh áp /V1–TSA ≈0,5 bar. "
                "Không khí được làm lạnh 7–10 °C ở /E5, /E6 bằng nước glycol của chiller /ACC1 (nước chiller không xuống dưới 0 °C, yêu cầu ≥ 5 °C). "
                "Sau đó qua tách cyclone WS100 và lọc coalescing FIL1509A/B (< 0,01 mg lỏng/m³).",
                "APU (/V2, /V3) gồm 3 lớp:",
                "• activated alumina 186 kg (300 mm) – khử ẩm;",
                "• xúc tác 35 kg – khử CO;",
                "• rây phân tử 13X 611 kg (1.050 mm) – khử CO₂, C₂H₂, C₃H₈ (các chất có thể đóng băng ở /E3, /E4 hoặc gây nổ ở /V4).",
                "Chu kỳ APU kết thúc khi tổng lưu lượng đạt 7.148 m³/h hoặc sau 680 phút. Các bước: chờ → xả áp → gia nhiệt (tới TT-36216 = 100 °C) → làm nguội (ΔT vào/ra < 4 °C) → kiểm tra van → tăng áp → chạy song song.",
                "Độ tinh khiết điều khiển gián tiếp bằng tỉ lệ thu hồi N₂/Air = FT36227 / (FT36227 + FT36223 − lưu lượng qua tuabin), qua FV-36223. "
                "Độ tinh khiết rất nhạy với tỉ lệ này, đặt quá cao sẽ tụt nhanh.",
                "Mức /V4, /E4 giữ bằng LV-36232 để dòng ra khỏi /E4 có > 80 % pha lỏng. Nếu sôi khô ở đây, tạp chất (nhất là băng acetylene) có thể đóng rắn và gây nổ. "
                "XYS-36249 xả lỏng giàu O₂ (≈60 %) mỗi giờ 1 lần qua bộ bay hơi VP-2.",
                "Khí thải sau /E3 dùng tái sinh APU hoặc xả qua PV-36221; áp khí thải ≤ 0,5 barg để không tạo áp ngược lên tuabin. "
                "Sản phẩm điều khiển áp qua FV-36227 (PT-36229), tốc độ thay đổi tối đa ≈50 % trong 30 phút. Áp mạng thấp thì bồn /TK1 hóa hơi bù (chênh ≈0,5 bar); áp cao thì PV-36229 xả.",
                "Tuabin giãn nở hướng tâm, ổ đỡ khí (IA qua PCV-36753). Phanh bằng máy nén tuần hoàn làm mát ở /ABC1; áp phanh PCV-36710 ≈0,4 barg. Khí vào < 140 K có thể sinh nước đá, nên có bộ gia nhiệt điện E-36234.",
                "Khởi động:",
                "• Plant On ở Mode 0, chạy hết 1 chu kỳ tái sinh cả /V2 và /V3;",
                "• thổi coldbox qua HV-36231/36230 tới khi ẩm < 5 ppm;",
                "• Mode 1: purge tuabin 260 phút. Nếu APU đang heating/cooling thì nâng Min Output của PV-36219 từ 16 % lên 19 %;",
                "• áp /T1 ≈7,6 barg: interlock tuabin clear, ZV-36298 mở 55 % và bắt đầu làm lạnh (có thể làm lạnh nhanh bằng lỏng từ /TK1);",
                "• TT-36225 ≈ −160 °C thì có lỏng ở /T1; AIT-36245 < 5 ppm O₂ thì XV-36245 mở cấp sản phẩm.",
                "Sản phẩm: 7 barg, 10–20 °C, N₂ ≥ 99,9 %V (O₂ ≤ 0,1 %V)."]},
    ],
    "src": [GT07, OMU],
}

# ============================================================ Unit 19A tuabin khí
START19 = {"h": "Khởi động",
           "ul": ["Tuabin được quay khởi động bằng động cơ diesel, qua bộ biến mô Voith (torque converter) có cơ cấu ratchet thủy lực, và ly hợp vấu (starting jaw clutch) nối vào hộp số phụ. "
                  "Sách Vol I và giáo trình G2-30-GT-08 thống nhất điểm này (ghi chú trên PFD 2098-19 về motor điện là không đúng với hiện trạng).",
                  "Ratchet phá trạng thái đứng yên của rotor (breakaway): mỗi hành trình 10 giây xoay ly hợp ≈47°. Khi làm nguội sau dừng máy, ratchet tự chạy mỗi 3 phút một chu kỳ.",
                  "Trình tự: quay máy → đạt tốc độ đánh lửa → đốt (primary) → khởi động ấm → tăng tốc. "
                  "Ở ≈95 % tốc độ, van xả tầng 10 đóng và IGV mở về vị trí làm việc. Ở ≈3.100–3.200 v/ph, ly hợp tự nhả, diesel về chạy không tải rồi dừng.",
                  "Không được đóng ly hợp vấu khi trục trượt đang quay. Trước khi vô hiệu hóa thiết bị nào của hệ khởi động, phải nhả và khóa ly hợp bằng van nhả ly hợp."]}
PATCH["19A"] = {
    "replace": {"Khởi động": START19},
    "add": [
        {"h": "Giới hạn & cảnh báo vận hành (giáo trình G2-30-GT-08)",
         "ul": ["Áp dầu bôi trơn ở ống góp 1,7 barg (25 psig); tuabin trip ở 0,96 barg (14 psig).",
                "Rung: xử lý khi > 0,5 in/s; không vượt quá 1 in/s theo mọi hướng.",
                "Nhiệt độ không gian tầng cánh (cấp 1 và 2, mặt trước và sau): cảnh báo 420 °C, trip 457 °C. Giá trị này phải đọc ít nhất từ 2 cặp nhiệt đối diện.",
                "Spread nhiệt độ khói thải: tốt nhất 45 ± 35 °F. Phải tìm nguyên nhân khi > 80 °F hoặc lệch 35 °F so với baseline. "
                "Baseline được lập khi mới khởi động, trước và sau mỗi lần dừng, trước và sau bảo dưỡng.",
                "Không chạy khi hỏng quá 2 cặp nhiệt khói thải, và 2 cặp hỏng không được cùng nằm trong 3 cặp liền nhau.",
                "Thấy khói đen đột ngột thì dừng máy ngay, không cho ai vào gian máy (áp trong gian cao hơn bên ngoài). Kiểm tra toàn bộ buồng đốt.",
                "Hệ chữa cháy CO₂ tác động sẽ trip tuabin và đóng các cửa thông gió. Phải mở lại cửa thông gió bằng tay trước khi chạy lại.",
                "Sau khi trip mà rotor không được quay bằng ratchet:",
                "• trong 15 phút: khởi động lại bình thường;",
                "• từ 15 phút đến 48 giờ: phải quay ratchet 1–2 giờ trước khi khởi động;",
                "• sau 48 giờ: khởi động được, nhưng phải theo dõi rung chặt chẽ. Rung > 1 in/s thì dừng và quay ratchet ≥ 1 giờ.",
                "Nếu trip do nghi hỏng bên trong thì không quay rotor. Nếu rotor bị kẹt khi quay ratchet, giữ nguyên ≥ 30 giờ hoặc tới khi rotor tự do."]},
        {"h": "Sự cố thường gặp (giáo trình)",
         "tb": [["Hiện tượng", "Nguyên nhân cần kiểm tra"],
                ["Không quay được (crank)", "Ratchet, ly hợp SSS, bơm của torque converter, diesel hỏng, rotor cọ xát"],
                ["Không đánh lửa", "Mạch firing (VCE), mạch đánh lửa, áp khí nhiên liệu, van stop không mở, tốc độ đánh lửa"],
                ["Mất lửa", "Hiệu chuẩn, mạch hoặc độ sạch đầu dò lửa; van GCV; SRV đặt quá cao; FSR"],
                ["Đang gia nhiệt nhưng không tăng tốc", "Thiết bị khởi động, rò PCD, hệ nhiên liệu, áp giữa SRV và GCV"],
                ["Rung cao khi khởi động", "Rotor cong (kiểm tra ratchet khi làm nguội), stall máy nén (van bleed)"],
                ["Nhiệt khói thải cao / spread cao", "Đường TTX theo PCD, hiệu chuẩn cặp nhiệt, đầu phun tắc hoặc rò gioăng, một buồng đốt mất lửa, hư hỏng đường khí nóng"]],
         "p": ["Một số cảnh báo Speedtronic: L52QA_ALM (bơm dầu phụ chạy do áp bơm chính không đủ), L52HQ_ALM (bơm dầu thủy lực phụ chạy), "
               "L27BLN_ALM (sạc ắc quy hoặc điện áp DC thấp; không chạy tuabin nếu nguồn DC cho bơm dầu khẩn cấp không sẵn sàng), "
               "L30SPA (sự cố cháy), L86CB1 (van xả tầng 10 sai vị trí, phải Master Reset), L12HF (mất tín hiệu tốc độ, dừng khẩn)."]},
    ],
    "src": [GT08],
}

# ============================================================ Unit 45 bồn NH3 & Unit 41 đuốc
PATCH["45"] = {
    "add": [
        {"h": "Thiết kế (giáo trình G2-30-GT-09)",
         "tb": [["Thiết bị", "Thông số"],
                ["40-TK-5001", "Bồn kép hai vách đều chứa được toàn bộ NH₃; 35.000 / 29.500 m³ (≈20.000 t)"],
                ["40-PK-5001 / 40-PK-5005", "Làm lạnh hơi NH₃ 600 / 250 kg/h; mỗi cụm 2 máy nén trục vít phun dầu (1 chạy, 1 dự phòng)"],
                ["40-P-5001A/B, 40-P-5002/5003", "85 m³/h; 368 m (40-P-5001B dự phòng chung cho P-5001A và P-5002)"],
                ["40-E-5001/5002", "Gia nhiệt NH₃ 933,1 kW; 20.000 kg/h"],
                ["NH₃ tồn trữ", "≥ 99,8 %wt; H₂O ≤ 0,2 %; dầu ≤ 5 ppm; Fe ≤ 2 ppm"]],
         "p": ["Hơi NH₃ trong bồn sinh ra do hấp thụ nhiệt môi trường, do nạp lỏng làm thu hẹp không gian hơi, do làm lạnh bồn khi khởi động và do hơi hồi lưu từ xe bồn. "
               "Hơi được thu hồi về máy nén 10-K-4051 (X.Amonia) hoặc về các cụm làm lạnh. Khi cụm làm lạnh mất điện thì xả ra đuốc qua bypass van điều áp."]},
        {"h": "Logic bảo vệ bồn (giáo trình)",
         "tb": [["Logic", "Tín hiệu (2oo3)", "Tác động"],
                ["40-IS-45001", "LIT-45001A/B/C = 94 %", "Đóng LV-45001 (ngừng nhận NH₃)"],
                ["40-IS-45001", "LIT-45001A/B/C = 2 %", "Dừng các bơm NH₃ lỏng"],
                ["40-IS-45001", "PIT-45013/15/16 = 15,3 barg", "Dừng 40-P-5001B, 40-P-5002/5003"],
                ["40-IS-45002", "PIT-45001A/B/C = 130 mbarg", "Mở hoàn toàn PV-45005 (ra đuốc)"],
                ["40-IS-45002", "PIT-45001A/B/C = 10 mbarg", "Đóng HV-45002, dừng máy nén 40-PK-5001/5005, dừng bơm NH₃ lỏng"],
                ["40-IS-45002", "PIT-45001A/B/C = 5 mbarg", "Mở PV-45001 cấp N₂ giữ áp bồn"]]},
        {"h": "Thu hồi hơi về 10-K-4051 & vận hành",
         "ul": ["Khi áp bồn ≥ 70 mbarg: mở van TH-PT1 (X.Phụ trợ) và TH-NH3_1 (X.Amonia) đưa hơi về máy nén 10-K-4051. "
                "Đặt PIC-5022 xuống 10 mbarg (nhánh surge) và 30 mbarg (nhánh load/unload). Giữ áp bồn 50–100 mbarg; PV-45005 không được mở.",
                "Áp bồn xuống 100 mbarg: cho 40-PK-5001/K1 về dự phòng. Xuống 60 mbarg: nâng PIC-5022 lên 20 / 40 mbarg. "
                "Lên 115 mbarg và PV-45005 mở: chạy lại 40-PK-5001. Xuống 50 mbarg hoặc 10-K-4051 dừng: đóng TH-PT1/TH-NH3_1 và chạy lại 40-PK-5001.",
                "Khởi động bồn mới / sau đại tu:",
                "• trơ hóa N₂ tới O₂ < 2 %;",
                "• thổi bằng hơi NH₃ (< 0,5 t/h rồi < 1 t/h, tối thiểu 1,5 t/1.000 m³) tới N₂ < 5 %;",
                "• làm lạnh bằng NH₃ lỏng ≈2 °C/h (≤ 5 °C/h), chênh nhiệt giữa 2 điểm gần nhau < 15 °C, giữa 2 điểm bất kỳ < 30 °C, áp bồn < 100 mbarg; thường mất 40–50 giờ;",
                "• tăng lưu lượng nạp khi TI-45001 đạt −32 °C.",
                "Bơm NH₃ lỏng: làm lạnh bằng hơi từ bồn, mồi qua bypass van ARC, mở đường min flow, N₂ làm kín, khởi động tay từ LCP, rồi mở dần van đẩy theo PI-45503A/B."]},
        {"h": "Cụm làm lạnh mới 40-PK-5005 (giáo trình)",
         "ul": ["250 kg/h (95 kW lạnh) ở −33 °C, chạy song song với 40-PK-5001. Máy nén trục vít phun dầu K1A/B, load/unload bằng slide valve. "
                "Tín hiệu điều khiển chọn trên HMI: áp bồn PIC-45004, áp vào hệ PIT-45466, hoặc áp hút PIT-45453 / 45459.",
                "Hơi từ bồn → sub-cooler /V1 (demister) → máy nén → tách dầu /V3A/B (≤ 5 ppm dầu) → ngưng tụ /E1 bằng nước fresh → bình chứa /V2. Lỏng từ /V2 chia 2 dòng:",
                "• một dòng tiết lưu vào vỏ /V1 làm lạnh (LV-45410 giữ mức);",
                "• một dòng đi trong ống /V1, được làm lạnh sâu tới ≈ −30 °C, rồi qua LV-45409 về bồn.",
                "Tải thấp (slide < 25 %, áp /V1 dưới setpoint, máy chạy > 1 phút): hot gas bypass qua PV-45466. Oil distiller /V4 gom dầu từ /V1, xả tay theo LG-45712. Air purger /V5 tách khí trơ."]},
    ],
    "src": [GT09, OMF],
}
PATCH["41"] = {
    "add": [
        {"h": "Thiết kế (giáo trình G2-30-GT-09)",
         "tb": [["Đuốc", "Công suất", "Trường hợp thiết kế"],
                ["40-PK-1002 khí tổng hợp (header 36\", KO drum 40-V-1001)", "349.674 kg/h", "Gas break-through 10-T-3002 (75 °C; H₂ 60 %, N₂ 19,7 %, CO₂ 18 %); nghẹt đầu ra reforming 213.056 kg/h (360 °C)"],
                ["40-PK-1001 NH₃ (header 40\" + đường 10\" từ bồn)", "298.190 kg/h", "Từ 10-K-4031 (298.190 kg/h, khí giàu H₂), 10-K-4041 (83.185), 10-K-4051 (6.940), bồn NH₃ (1.140), 40-PK-5001 (2.508), 40-T-2001"]],
         "p": ["Các dòng chứa CO/CO₂ và dòng chứa NH₃ được tách riêng để tránh tạo carbamate trong hệ đuốc. "
               "Ống đuốc cao 45 m để bức xạ không vượt 3.000 Btu/h·ft² ở các tòa nhà và 1.450 Btu/h·ft² trên bán kính 60 m. "
               "Mỗi đuốc có 3 pilot kèm đầu dò lửa. Đuốc NH₃ được bổ sung khí nhiên liệu ở đỉnh qua FO-41501 và HV-41002 (HIC-41002 / FIC-41001A)."]},
        {"h": "Vận hành (G2-30-HD-055)",
         "ul": ["Chuẩn bị: IA ≈1,0 barg (PI-41701/41711); FG ≈1,0 barg (PI-41703/41713); mạng N₂ > 6 barg.",
                "Purge đuốc NH₃: N₂ qua 10-RO-4503 ≈50 Nm³/h và 10-RO-5532 ≈2 Nm³/h, FG 10-FI-41501 ≈22 Nm³/h. "
                "Purge đuốc khí tổng hợp: 10-RO-2500 ≈1, 10-RO-3501 ≈20, 10-RO-4502 ≈1,5 Nm³/h N₂, FG 10-FI-41511 ≈20 Nm³/h. Purge tới O₂ ở đáy đuốc ≤ 8 %.",
                "Đánh lửa: cảm biến tự đánh lửa TE-41201~04 / TE-41211~13 đặt 120 °C; PCV-41701/41711 đặt 1,0 barg, PCV-41702/03 và 41712/13 đặt 0,7 barg. "
                "Chọn từng pilot ở chế độ Manual (điền hỗn hợp 20 giây, XV-41703 mở) rồi nhấn Ignition. Sau đó chuyển FFG sang Auto để tự đánh lửa lại khi có Pilot Failure.",
                "Vận hành: duy trì purge liên tục, xả lỏng KO drum định kỳ, chỉnh khí hỗ trợ đuốc NH₃ bằng HV-41002. "
                "Nếu mạng N₂ < 6 barg thì báo ĐĐSX để thay purge N₂ bằng FG.",
                "Liên quan: G2-30-PA-137 (cô lập bảo dưỡng flare), G2-30-PA-140 (vận hành cụm làm lạnh và bồn khi không có flare)."]},
    ],
    "src": [GT09, OMF],
}

PATCH["33"] = {"src": [OMU]}
PATCH["42"] = {"src": [OMW]}


# ---- Đoạn "Mô tả công nghệ" đầu trang Unit: ưu tiên lấy từ giáo trình cương vị (11/2026) ----
GT02 = gt(2, "GT dao tao HT nuoc lam mat - nuoc NHR")
GT05 = gt(5, "GT dao tao HT xu ly nuoc thai")
INTRO = {
    "18": ("Hệ thống nước cấp lò hơi điều chỉnh pH và khử oxy cho nước trước khi cấp tới các hộ tiêu thụ. "
           "Nước khử khoáng từ bơm 30-P-1002A/B được gia nhiệt ở các trao đổi nhiệt bên X.Amo, rồi vào thiết bị khử khí 10-PK-8004 qua van 10-FV-8003. "
           "Tại đây nước phân phối từ trên xuống, tiếp xúc ngược chiều với hơi LP đi từ dưới lên để loại khí hòa tan (chủ yếu O₂, CO₂). "
           "Nước đã khử khí chứa ở bồn 10-V-8001, được chỉnh pH bằng hóa chất kiềm hóa (10-PK-8002) và khử oxy bằng hóa chất (10-PK-8003). "
           "Bơm 10-P-8002A/B (nước cấp HP) và 10-P-8001A/B (nước cấp HHP, X.Amo quản lý) cấp nước cho lò hơi phụ 10-B-8001, lò thu hồi nhiệt 10-B-9001, lò hơi HHP X.Amo, X.UFC85 và nước quench. "
           "\nLò hơi phụ 10-B-8001 là lò Macchi \u201cTitan M\u201d 140 t/h, kiểu ống nước, tuần hoàn tự nhiên, đốt khí. "
           "Quạt gió FD 10-B-8001/K1 cấp không khí cháy dưới áp suất dương. Khói đi hết buồng đốt, qua bộ quá nhiệt, chùm ống sinh hơi và bộ hâm nước E1, rồi ra ống khói cao 30 m. "
           "Nước trong ống sinh hơi hóa hơi và đối lưu tự nhiên về bao hơi V1. Hơi bão hòa qua bộ quá nhiệt SH1/SH2 (có giảm ôn DSH) thành hơi cao áp 39 barg / 380 °C. "
           "Hệ thống BMS-1 giám sát tự động lò và các đầu đốt.", [GT03]),
    "31": ("Nước khử khoáng được sản xuất bằng nhựa trao đổi ion dương, ion âm và nhựa tầng hỗn hợp. Nhựa loại bỏ Na⁺, Mg²⁺, Ca²⁺, Cl⁻, SO₄²⁻, HCO₃⁻, HSiO₃⁻… trong nước thô và nước ngưng công nghệ. "
           "\nHệ thống có 3 chuyền giống nhau: 2 chuyền chạy, 1 chuyền dự phòng hoặc tái sinh. "
           "Nước thô đã khử clo bằng Na₂SO₃, trộn với nước ngưng công nghệ, lần lượt qua bình cation 30-PK-1001/V1, tháp khử CO₂ V2 và bình anion V3 để thành nước khử ion. "
           "Nước khử ion chứa ở bồn 30-TK-1001 (500 m³), cùng nước ngưng hơi và nước ngưng tuabin từ các xưởng. Nếu nước ngưng tuabin nhiễm nước sông thì được đưa về đầu chuyền cation hoặc tháp khử khí. "
           "Bơm 30-P-1001A/B đưa nước khử ion qua các bình trao đổi tầng hỗn hợp (2 chạy, 1 dự phòng/tái sinh), rồi vào bồn nước khử khoáng 30-TK-1002 (9.000 m³, đủ cho toàn nhà máy dùng 24 giờ). "
           "Bơm 30-P-1002A/B cấp nước từ đây tới các hộ tiêu thụ. Chỉ tiêu nước khử khoáng: độ dẫn điện < 0,2 µS/cm, SiO₂ < 0,02 ppm, Na⁺ < 0,02 ppm, pH 6,5–7. "
           "\nNước thải tái sinh nhiễm hóa chất gom về bể 30-PK-1001/BA1, trung hòa bằng axit sunfuric hoặc xút rồi xả sang bể nước sông làm mát 30-BA-3001. "
           "Nước rửa không nhiễm hóa chất xả thẳng về 30-BA-3001.", [GT06]),
    "33": ("Nhà máy dùng hệ thống làm mát gián tiếp: nước sông giải nhiệt cho nước sạch làm mát. "
           "Nước sông tuần hoàn qua tháp giải nhiệt 30-CT-3001A~L (12 khoang × 3.109,2 m³/h, 1 khoang dự phòng); bể tháp đủ cấp cho 10 phút vận hành. "
           "Bơm 30-P-3001A~E (trục đứng, 10.100 m³/h, 40 mH₂O; A~D ở bể 30-BA-3001, E ở bể mới 30-BA-3003) cấp nước sông đi ba hướng. "
           "Hướng thứ nhất làm mát trực tiếp các bình ngưng tuabin hơi X.Amo/X.Urê. Hướng thứ hai làm mát bình ngưng NH₃ bằng titan, chịu được clo trong nước sông. "
           "Hướng thứ ba giải nhiệt nước sạch tại các trao đổi nhiệt tấm 30-E-3001A~I. Nước về tháp ở khoảng 43 °C và cấp đi ở 34 °C. "
           "\nNước sạch làm mát chạy trong vòng kín, nhận nhiệt của các thiết bị X.Amo, X.Urê và X.Phụ trợ. Nhờ vòng kín, các thiết bị này dùng được thép cacbon thay cho titan (không dùng đồng vì NH₃ hòa tan gây ăn mòn). "
           "Bơm 30-P-3002A~D (2 chạy) tuần hoàn nước sạch, cấp ở 37 °C và nhận về ở 46 °C. "
           "Bình giãn nở 30-V-3001 đệm N₂ ở 2–2,3 barg (30-PIC-33101, split range) giữ áp đầu hút và tách khí khi có rò từ các xưởng. Nước Demi bổ sung qua 30-LIT-33101. "
           "\nNước sông được bơm từ sông qua cụm lọc 30-PK-3006 để bù lượng bay hơi và xả đáy (30-FV-33002). Hệ số cô đặc giữ ở 1,2 để tránh tích tụ clorua và đóng cặn CaCO₃/CaSO₄. "
           "Chất lượng nước được kiểm soát bằng H₂SO₄ (pH), hóa chất chống cặn và NaOCl diệt vi sinh, châm vào bể 30-BA-3001/3003.", [GT02]),
    "35": ("Hệ thống cấp khí nén (plant air) và khí điều khiển (instrument air) cho toàn nhà máy, nhu cầu thiết kế 5.600 Nm³/h (khí điều khiển 2.920, khí nén 2.680). "
           "Các hộ dùng lớn là cụm nitơ (tối đa 1.096 Nm³/h), thụ động hóa X.Urê (700 Nm³/h) và 20-E-1001/20-K-1001. "
           "Các máy nén 30-K-5001A~E đẩy khí vào bình chứa khí nén 30-V-5001 (28,5 m³). Theo giáo trình có 4 máy chạy, 1 dự phòng, mỗi máy 1.400 Nm³/h, 9 barg, 45 °C. "
           "\nTừ đây một nhánh cấp khí nén cho nhà máy. Nhánh còn lại qua hai máy sấy hấp phụ chạy song song 30-DR-5001 (1.820 Nm³/h) và 30-DR-5002 (1.100 Nm³/h) để đạt điểm sương −25 °C, rồi vào bình khí điều khiển 30-V-5002 (154 m³). "
           "Mỗi bình chứa đủ cấp khí cho khoảng 10 phút; 30-V-5002 giảm áp từ 8,1 xuống 5 barg trong thời gian đó. Nhà máy còn nhận khí bổ sung từ 10-K-4021 của X.Amo. "
           "\nKhí điều khiển được ưu tiên hơn khí nén. Khi 2/3 tín hiệu PIT-35004 xuống 5 barg, IS-6 tác động: sau 3 s đóng 30-PV-35003/35004, sau 30 s tiếp theo dừng X.Urê. "
           "Khi thiếu khí kéo dài, X.Phụ trợ liên lạc với X.Amo để mở 10-FV-4001, lấy process air từ X.Amo bù sang.", [GT04]),
    "36": ("Cụm 30-PK-6001 sản xuất N₂ bằng chưng cất không khí ở nhiệt độ thấp. "
           "Khí nén vào bình trung gian V1 để tách nước và ổn định áp suất, lưu lượng. Khi khởi động, 30-XYS-36257 mở cho hệ tăng áp từ từ; 30-XV-36205 chỉ mở khi chênh áp V1–TSA khoảng 0,5 bar. "
           "Không khí được làm lạnh xuống 7–10 °C ở E5/E6 bằng nước glycol của chiller ACC1 (nhiệt độ nước không dưới 5 °C để tránh đóng băng). Sau đó khí qua bộ tách nước kiểu cyclone WS100 và lọc coalescer FIL1509A/B. "
           "\nTiếp theo khí vào cụm hấp phụ APU gồm 2 bình V2/V3 (1 làm việc, 1 tái sinh). Mỗi bình có ba lớp: alumina hoạt tính khử ẩm, xúc tác khử CO, rây phân tử 13X giữ CO₂ và hydrocacbon nhẹ, tránh đóng băng ở E3/E4 và nguy cơ nổ ở V4. "
           "Bình chuyển khi tổng lưu lượng đạt 7.148 m³ hoặc sau 680 phút. Bình tái sinh bằng khí thải từ coldbox được gia nhiệt. "
           "\nTrong coldbox, không khí sạch được làm lạnh ở trao đổi nhiệt chính E3 rồi vào cột chưng cất T1. N₂ lấy ở đỉnh cột; bình tách pha V4 và thiết bị ngưng tụ chính E4 tạo dòng hồi lưu. "
           "Lạnh cho quá trình do turbine giãn nở EK1 tạo ra (giáo trình ghi K1), có bộ làm mát ABC1. Sản phẩm là N₂ khí 99,9 %, khoảng 7 barg, cấp cho nhà máy. "
           "N₂ lỏng chứa ở bồn TK1. Khi cụm dừng hoặc thiếu N₂, nitơ lỏng được bay hơi qua E1A/B; E2A/B là bộ bay hơi tạo áp cho bồn.", [GT07]),
    "37": ("Khí thiên nhiên từ trạm khí (24,5 barg, 18–36 °C) được cấp trực tiếp cho X.NPK và cho X.Amo làm nguyên liệu reforming. "
           "Khí cũng qua 30-PV-37003 vào bình 30-V-7003 cấp cho hệ thống đuốc, và qua 30-PV-37001 (thiết kế 34.317 Nm³/h) vào bình khí nhiên liệu cao áp 30-V-7001. "
           "Từ 30-V-7001, khí cấp cho tuabin khí 10-GT-9001, đồng thời qua 30-PV-37002 (27.053 Nm³/h) vào bình thấp áp 30-V-7002. "
           "Bình 30-V-7002 cấp nhiên liệu cho lò reforming X.Amo, lò hơi phụ 10-B-8001 và lò thu hồi nhiệt 10-B-9001.", [GT03]),
    "41": ("Hệ thống đuốc đốt các dòng khí chứa NH₃ hoặc hydrocacbon dễ cháy, xả ra khi van an toàn hoặc van thở trên đường ống tác động và trong lúc khởi động, dừng nhà máy. "
           "Có hai cụm đuốc riêng: đuốc NH₃ 40-PK-1001 (thiết kế 298.190 kg/h) và đuốc khí tổng hợp 40-PK-1002 (349.674 kg/h). Các dòng chứa CO/CO₂ được tách riêng khỏi dòng chứa NH₃ để không tạo carbamate trong hệ thống đuốc. "
           "\nĐuốc khí tổng hợp nhận khí từ các van an toàn và khí xả công đoạn cuối X.Amo. Khí gom vào header 36\u2033, qua bình tách lỏng KO drum 40-V-1001 rồi lên đuốc cao 45 m. Chiều cao này giữ bức xạ ≤ 1.450 Btu/h·ft² trong bán kính 60 m. "
           "Một dòng purge liên tục giữ hệ thống ở áp suất dương. Đầu đuốc có ba đầu đốt với thiết bị đánh lửa; tủ điều khiển đánh lửa đặt dưới đất, ngoài vùng ảnh hưởng của đuốc. "
           "\nĐuốc NH₃ nhận khí từ các máy nén 10-K-4031/4041/4051, bồn chứa NH₃, cụm 40-PK-5001 và 40-T-2001.", [GT09]),
    "42": ("Nước thải của nhà máy được xử lý qua ba cụm. "
           "\n(1) Cụm nước thải nhiễm dầu 40-PK-2001: lưới vớt rác Z1, bể tách dầu trọng lực V1 có dây đai gạt dầu Z2, rồi thiết bị tách CPI V4. Sau đó nước được phá nhũ, keo tụ (khuấy nhanh TK3, keo tụ TK4) và tuyển nổi khí hòa tan (bộ bão hòa khí V5, bể tuyển nổi Z5). Cuối cùng nước qua lọc đa lớp V6 và than hoạt tính V7. Dầu thu về bể BA3. "
           "\n(2) Cụm nước thải sinh hoạt cũ 40-PK-2002 (50 m³/ngày): bể cân bằng BA1, bể oxy hóa BA2A/B, bể lắng ổn định BA3A/B, bể clo hóa BA5, lọc FL1. Bùn được ổn định ở BA4 và lên men hiếu khí ở BA6A/B. "
           "\n(3) Hệ thống mới 40-PK-2003 (khoảng 680 m³/ngày) xử lý chung nước sinh hoạt (200 m³/ngày) với nước nhiễm dầu đã qua 40-PK-2001 nhưng chưa đạt chuẩn thải (480 m³/ngày). "
           "Nước đi qua bể thu gom TK-100, sàng rác tinh FS-101, bể điều hòa TK-102, bể khử nitơ TK-103 (có bùn tuần hoàn và bổ sung photpho), bể đệm TK-104 rồi bể sinh học màng MBR TK-105. Màng được rửa bằng NaClO hoặc axit oxalic. "
           "Nước sau MBR đạt tiêu chuẩn thải. Bùn dư được nén ở TK-201 rồi xử lý tiếp (máy ép bùn BF-202 theo thiết kế).", [GT05]),
    "45": ("Hệ thống tồn chứa NH₃ gồm bồn chứa NH₃ lỏng 40-TK-5001 (35.000/29.500 m³, 20.000 tấn, −33 °C, 0,04–0,10 barg), hai cụm làm lạnh hơi 40-PK-5001 (600 kg/h) và 40-PK-5005 (250 kg/h), "
           "bơm chuyển 40-P-5001A/B và bơm nạp xe bồn 40-P-5002/5003 (85 m³/h, 368 m), cùng bộ gia nhiệt NH₃ 40-E-5001/5002 (20.000 kg/h). "
           "\nKhi chạy bình thường, một phần NH₃ của X.Amo cấp thẳng cho X.Urê. Phần còn lại ở dạng lỏng −33 °C theo đường ống bảo ôn về bồn chứa. "
           "40-TK-5001 là bồn kép hai vách kim loại; vách trong và vách ngoài đều chứa được toàn bộ lượng NH₃. "
           "Hơi NH₃ sinh ra do bồn hấp thụ nhiệt hoặc khi xuất lỏng được đưa về máy nén 10-K-4051 (X.Amo) hoặc cụm làm lạnh 40-PK-5001/5005. Tại đó hơi được nén, hóa lỏng rồi trả lại bồn, tránh tăng áp phải xả ra đuốc.", [GT09]),
    "19A": ("Tuabin khí 10-GT-9001 (MS-5001) chạy chu trình hở đơn giản, một trục từ máy nén tới tuabin, có 10 buồng đốt kiểu dòng khí nén chạy ngược (reverse flow). "
            "Tổ máy gồm năm phần: hệ thống không khí vào, máy nén dọc trục, hệ thống buồng đốt, tuabin hai cấp và hệ thống khói thải. "
            "\nKhi khởi động, khớp SSS nối thiết bị khởi động (diesel) với trục tuabin. Không khí được lọc rồi nén trong máy nén dọc trục. Để chống rung (surge), hai van trích khí ở tầng nén thứ 10 mở hoàn toàn và cánh dẫn hướng IGV ở vị trí nhỏ nhất 41°. "
            "Ở 1.120 rpm (22 % tốc độ), bugi đánh lửa và van khí nhiên liệu mở. Ngọn lửa lan qua các ống cross-fire tới mọi buồng đốt, các đầu dò lửa xác nhận cháy ổn định. "
            "Ở 101 % tốc độ (5.100 rpm), hai van trích khí đóng và IGV mở tới vị trí vận hành 46°. "
            "\nKhí cháy qua 10 ống chuyển dòng (transition piece) vào tuabin hai cấp. Tại các dãy vòi phun, động năng tăng và áp suất giảm; một phần năng lượng chuyển thành cơ năng quay rotor, kéo máy phát. "
            "Sau cấp 2, khí đi qua bộ khuếch tán có cánh dẫn hướng để giảm tổn thất, rồi ra ống khói hoặc sang lò hơi thu hồi nhiệt 10-B-9001.", [GT08]),
}
for _u, (_t, _s) in INTRO.items():
    PATCH.setdefault(_u, {})["intro"] = _t
    PATCH[_u]["src"] = _s + [x for x in PATCH[_u].get("src", []) if x not in _s]


def apply(units, tags):
    for u, e in UNITS_NEW.items():
        units[u] = e
    for u, p in PATCH.items():
        e = units[u]
        if "t" in p:
            e["t"] = p["t"]
        if "intro" in p:
            e["intro"] = p["intro"]
        drop, rep = set(p.get("drop", [])), p.get("replace", {})
        e["s"] = p.get("pre", []) + [dict(s, **rep[s["h"]]) if s["h"] in rep else s for s in e.get("s", []) if s["h"] not in drop] + p.get("add", [])
        e["src"] = list(e.get("src", [])) + [x for x in p.get("src", []) if x not in e.get("src", [])]
        if u in INTRO:  # nguồn giáo trình của đoạn mô tả lên đầu, bỏ trùng đường dẫn
            first = INTRO[u][1]
            seen = {x[0] for x in first}
            e["src"] = first + [x for x in e["src"] if x[0] not in seen]
    tags.update(TAG_NEW)
    for k, p in TAG_ADD.items():
        if k not in tags:
            continue
        e = dict(tags[k])
        if "intro" in p:
            e["intro"] = p["intro"]
        e["s"] = list(e.get("s", [])) + p.get("s", [])
        e["src"] = list(e.get("src", [])) + [x for x in p.get("src", []) if x not in e.get("src", [])]
        tags[k] = e
    import pumps  # đường đi của bơm (đọc trên P&ID)
    pumps.apply(tags)
