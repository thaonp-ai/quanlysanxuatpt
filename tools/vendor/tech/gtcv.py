"""Phần "Giáo trình" của trang Unit: tóm tắt giáo trình đào tạo các cương vị (G2-30-GT-01…09, ban hành 01/2024)
trong "Vendor Data/Giáo trình tham khảo các cương vị".

build(): {"gt": {mã: {...}}, "gtu": {unit: [mã…]}} — build_tech.py ghi vào tech.json.
  - Mục lục (toc: [cấp, tiêu đề, trang]) và câu hỏi ôn tập (q) lấy tự động từ PDF → gtcv_auto.json
    (đã sửa các dòng mục lục bị ngắt; xem /tmp script trong lịch sử commit).
  - Tóm tắt (sum), điểm cần nhớ (key) viết tay từ nội dung giáo trình.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
F = "Giáo trình tham khảo các cương vị/"


def p(n, name):
    return F + "STVB102393_G2-30-GT-%02d %s_vps.pdf" % (n, name)


GT = {
    "GT01": dict(no="G2-30-GT-01", t="Hệ thống nước thô – nước sinh hoạt – nước cứu hỏa", units=["32"],
        f=p(1, "GT dao tao HT nuoc tho-sinh hoat-cuu hoa"),
        cv="Cương vị vận hành nước thô, nước sinh hoạt và bơm cứu hỏa",
        sum=["Chương I: chỉ tiêu chất lượng nước (vật lý, hóa học, vi sinh) và lý thuyết khử trùng bằng clo, khử clo dư, các hóa chất gốc clo.",
             "Chương II: hệ thống nước thô 30-TK-2001 / bơm 30-P-2001A/B/C và nước sinh hoạt 30-TK-2002 / 30-PK-2001 (châm NaOCl, lọc than hoạt tính FL2A/B, lọc tinh FL1) / bơm 30-P-2002A/B; quy trình khởi động – ngừng và các interlock.",
             "Phần III: hệ thống nước cứu hỏa – bơm chính 30-P-4001A (motor) / B, C (diesel), bơm Jockey 30-P-4002A/B; hướng dẫn vận hành và thử liên động, thử tải định kỳ.",
             "Phụ lục: datasheet thiết bị chính, cách tính lượng Javel tiêu hao."],
        key=["6.000 m³ dưới đáy 30-TK-2001 dành riêng cho chữa cháy (vòi hút bơm nước thô đặt cao hơn).",
             "FIC-32002 tuần hoàn về bồn 90 m³/h; 30-P-2001 dừng khi LIT-32001 LL 86 %; 30-P-2002 dừng khi LIT-32002 LL 20 %.",
             "Clo dư nước sinh hoạt ≈ 2 ppm (AIT-32201 bật/tắt bơm 30-PK-2001/P1A/B).",
             "Bơm cứu hỏa tự chạy theo áp mạng: PSL-34201A 6,0 / B 5,5 / C 5,0 barg; Jockey giữ > 7 barg."]),
    "GT02": dict(no="G2-30-GT-02", t="Hệ thống nước làm mát – nước ngoài hàng rào", units=["33"],
        f=p(2, "GT dao tao HT nuoc lam mat - nuoc NHR"),
        cv="Cương vị vận hành nước làm mát (nước sông, nước sạch) và trạm bơm nước ngoài hàng rào",
        sum=["Chương I: lý thuyết tháp giải nhiệt (tự nhiên/cưỡng bức), hiệu suất tháp, range, heat load, nhiệt độ bầu ướt; kiểm soát chất lượng nước (blowdown, chống cáu cặn, ăn mòn, vi sinh).",
             "Chương II: thiết kế và mô tả công nghệ vòng nước sông (tháp 30-CT-3001A~L, bơm 30-P-3001A~E) và vòng kín nước sạch (trao đổi nhiệt tấm 30-E-3001A~I, bơm 30-P-3002A~D, bình giãn nở 30-V-3001).",
             "Hệ thống nước ngoài hàng rào (bơm 30-P-3010A/B) và cụm lọc nước sông bổ sung 30-PK-3006: mô tả công nghệ, quy trình vận hành chi tiết.",
             "Hóa chất nước làm mát, quy trình đổi bơm, các interlock nước sông và nước sạch."],
        key=["Nước sông cấp 34 °C / về 43 °C; nước sạch cấp 37 °C / về 46 °C.",
             "Hệ số cô đặc (C.O.C) giữ ≈ 1,2; châm H₂SO₄ chỉnh pH, chất chống cáu cặn, NaOCl diệt vi sinh.",
             "Bình giãn nở 30-V-3001 đệm N₂ 2–2,3 barg (30-PIC-33101); mức rất thấp LSLL-33102 dừng mọi bơm nước sạch.",
             "Bể tháp đủ cấp 10 phút vận hành; 12 khoang × 3.109,2 m³/h."]),
    "GT03": dict(no="G2-30-GT-03", t="Hệ thống nước cấp – lò hơi phụ trợ và khí nhiên liệu", units=["18", "37"],
        f=p(3, "GT dao tao HT nuoc cap-lo hoi phu tro va khi nhien lieu"),
        cv="Cương vị vận hành nước cấp lò hơi, lò hơi phụ trợ 10-B-8001 và khí nhiên liệu",
        sum=["Chương I: yêu cầu chất lượng nước lò hơi, truyền nhiệt và tính chất hơi nước, các dạng ăn mòn trong lò hơi, phương pháp xử lý nước cấp (khử khí, hóa chất).",
             "Hệ thống nước cấp: khử khí 10-PK-8004 / 10-V-8001, châm hóa chất 10-PK-8001/8002/8003, bơm 10-P-8001A/B, 10-P-8002A/B (turbine 10-STP-8002A); interlock, quy trình vận hành, datasheet.",
             "Hệ thống khí nhiên liệu: bình 30-V-7001 (cao áp) và 30-V-7002 (thấp áp), chỉ tiêu khí, quy trình vận hành.",
             "Lò hơi phụ 10-B-8001 (Macchi Titan M 140 t/h): quạt FD 10-B-8001/K1 (turbine STK1 / motor MK1), quy trình khởi động – ngừng, nguyên nhân MFT, các logic BMS-1; hệ condensate và blowdown; giám sát vận hành.",
             "Phụ lục: công thức bù nhiệt độ/áp suất cho lưu lượng khí, mức bao hơi, lưu lượng hơi HP; datasheet van và thiết bị."],
        key=["Nước cấp: O₂ < 0,02 mg/kg, pH 9–9,5, SiO₂ < 0,02 mg/kg, độ cứng < 1 mg/kg.",
             "Hơi lò phụ 39 barg / 380 °C; ống khói 30 m; BMS-1 giám sát đầu đốt.",
             "10-P-8002: trip áp hút thấp 1 barg; PALL-8006 = 45 barg tự chạy 10-P-8002B.",
             "Khí nhiên liệu: PV-37001 (34.317 Nm³/h) vào 30-V-7001, PV-37002 (27.053 Nm³/h) vào 30-V-7002."]),
    "GT04": dict(no="G2-30-GT-04", t="Hệ thống khí nén – khí điều khiển", units=["35"],
        f=p(4, "GT dao tao HT khi nen-khi dieu khien"),
        cv="Cương vị vận hành máy nén khí và máy sấy khí điều khiển",
        sum=["Chương I–II: lý thuyết nén (đẳng nhiệt, đoạn nhiệt, đa biến, nén nhiều cấp) và các loại máy nén: piston, trục vít, ly tâm, dọc trục.",
             "Chương III: không khí ẩm (điểm sương, độ ẩm) và nguyên lý làm khô khí bằng hấp phụ.",
             "Chương IV: hệ thống tại nhà máy – máy nén 30-K-5001A~E, bình 30-V-5001, máy sấy 30-DR-5001/5002, bình 30-V-5002; quy trình khởi động máy nén và máy sấy, chỉ tiêu công nghệ."],
        key=["Nhu cầu thiết kế 5.600 Nm³/h (khí điều khiển 2.920, khí nén 2.680).",
             "Máy nén 9 barg, 45 °C; máy sấy 1.820 + 1.100 Nm³/h, điểm sương −25 °C.",
             "Bình 30-V-5001 (28,5 m³) và 30-V-5002 (154 m³) mỗi bình đủ ≈ 10 phút.",
             "IS-6: 2/3 PIT-35004 = 5 barg → sau 3 s đóng 30-PV-35003/35004, sau 30 s dừng X.Urê."]),
    "GT05": dict(no="G2-30-GT-05", t="Hệ thống xử lý nước thải", units=["42"],
        f=p(5, "GT dao tao HT xu ly nuoc thai"),
        cv="Cương vị vận hành xử lý nước thải nhiễm dầu, nước thải sinh hoạt và trạm XLNT mới",
        sum=["Phần I – cơ sở lý thuyết: chỉ tiêu nước thải, lắng và tuyển nổi, lọc nhanh/chậm, keo tụ – tạo bông, khử trùng.",
             "Chương I: cụm nước thải nhiễm dầu 40-PK-2001 (API V1 → CPI V4 → phá nhũ, keo tụ → tuyển nổi DAF → lọc); quy trình vận hành, pha và bổ sung hóa chất.",
             "Chương II: cụm nước thải sinh hoạt cũ 40-PK-2002 (bùn hoạt tính sục khí kéo dài, 50 m³/ngày).",
             "Chương III: hệ thống mới 40-PK-2003 (khử nitơ + màng MBR, ≈ 680 m³/ngày): hóa chất, dữ liệu thiết kế, mô tả chi tiết; quy trình vận hành, rửa màng MBR, shock javel bể 40-PK-2002/BA8."],
        key=["Nước sau 40-PK-2001: dầu ≤ 5 mg/l; 40-PK-2003 nhận 200 m³/ngày sinh hoạt + 480 m³/ngày nước nhiễm dầu đã xử lý.",
             "Chuỗi 40-PK-2003: TK-100 → FS-101 → TK-102 → khử nitơ TK-103 → TK-104 → MBR TK-105; bùn dư → TK-201.",
             "Màng MBR rửa bằng NaClO / axit oxalic; cần duy trì lưu lượng khí sục màng."]),
    "GT06": dict(no="G2-30-GT-06", t="Hệ thống sản xuất nước khử khoáng", units=["31"],
        f=p(6, "GT dao tao HT san xuat nuoc khu khoang"),
        cv="Cương vị vận hành sản xuất nước khử khoáng (Demi)",
        sum=["Chương I: chỉ tiêu nước (pH, độ cứng, độ kiềm), tác hại tạp chất, trao đổi cation/anion, hạt nhựa trao đổi ion, hóa chất H₂SO₄, NaOH, Na₂SO₃.",
             "Chương II: thông số thiết bị chính 30-PK-1001 (cation V1, khử CO₂ V2, anion V3, mixed bed V4, các bồn định lượng, bể trung hòa BA1…); chỉ tiêu nước cấp, sản phẩm, tiêu hao hóa chất.",
             "Thông số tái sinh cation, anion, mixed bed; nguyên lý hoạt động; quy trình khởi động, tái sinh và ngừng cụm khử ion và mixed bed."],
        key=["3 chuyền: 2 chạy, 1 dự phòng/tái sinh; bồn 30-TK-1001 500 m³, 30-TK-1002 9.000 m³ (đủ 24 giờ).",
             "Nước khử khoáng: độ dẫn < 0,2 µS/cm, SiO₂ < 0,02 ppm, Na⁺ < 0,02 ppm, pH 6,5–7.",
             "Tái sinh cation phun axit 2 nồng độ (1,6 % rồi 4 %) để tránh kết tủa muối trên hạt nhựa.",
             "Nước thải tái sinh trung hòa ở 30-PK-1001/BA1 rồi xả sang 30-BA-3001."]),
    "GT07": dict(no="G2-30-GT-07", t="Hệ thống sản xuất nitơ", units=["36"],
        f=p(7, "GT dao tao HT san xuat Nito"),
        cv="Cương vị vận hành cụm sản xuất nitơ 30-PK-6001",
        sum=["Chương I: tính chất N₂/O₂, cơ sở lý thuyết chưng cất – hóa lỏng không khí: chiller, làm sạch không khí (hấp phụ), chưng cất.",
             "Chương II: cấu tạo và vai trò thiết bị (V1, ACC1, E5/E6, APU V2/V3, coldbox E3/T1/V4/E4, turbine giãn nở, TK1, E1A/B, E2A/B); chỉ tiêu N₂; quy trình khởi động, làm lạnh, các mode turbine/economiser, thổi coldbox, ngừng.",
             "Hướng dẫn thao tác trên HMI (alarm, trang vận hành/công nghệ, vòng PID, van, turbine, APU, ngừng khẩn cấp, trend).",
             "Phụ lục: kiểm tra van trước khởi động, khóa liên động, giá trị cài đặt HMI và bộ điều khiển, datasheet."],
        key=["N₂ sản phẩm 99,9 %, khoảng 7 barg.",
             "Không khí làm lạnh 7–10 °C ở E5/E6; nước chiller không dưới 5 °C (tránh đóng băng).",
             "APU chuyển bình khi tổng lưu lượng 7.148 m³ hoặc 680 phút; tái sinh bằng khí thải coldbox."]),
    "GT08": dict(no="G2-30-GT-08", t="Hệ thống Gas Turbine", units=["19A", "19B"],
        f=p(8, "GT dao tao HT Gasturbine"),
        cv="Cương vị vận hành máy phát điện 10-GT-9001 và HRSG",
        sum=["Phần I: chu trình Brayton (hở đơn giản, có trao đổi nhiệt, hỗn hợp), ảnh hưởng điều kiện môi trường, máy nén dọc trục, buồng đốt, turbine.",
             "Phần II: turbine khí MS-5001 – đường đi không khí/khí cháy, máy nén, IGV, van IBH, buồng đốt DLN, turbine, hệ thống không khí vào và khí thải.",
             "Hệ thống phụ trợ: dẫn động phụ, khởi động (diesel, torque converter, hydraulic ratchet, khớp SSS), dầu bôi trơn, khí nhiên liệu (SRV/GCV, DLN), dầu thủy lực, dầu điều khiển, khí làm mát và làm kín; lưu ý vận hành.",
             "Điều khiển Mark VI: khởi động, dừng khẩn cấp/bình thường, thiết bị phụ, phòng cháy, dò khí; các vòng điều khiển (khởi động, tốc độ – tải, nhiệt độ, khí nhiên liệu); bảng sự cố thường gặp và cảnh báo."],
        key=["MS-5001 một trục, 10 buồng đốt dòng ngược, turbine 2 cấp.",
             "Đánh lửa ở 1.120 rpm (22 %); van trích tầng 10 mở và IGV 41° khi khởi động.",
             "101 % tốc độ (5.100 rpm): van trích đóng, IGV mở tới 46°.",
             "Khởi động bằng động cơ diesel qua torque converter và khớp SSS."]),
    "GT09": dict(no="G2-30-GT-09", t="Hệ thống bồn chứa NH₃ – flare", units=["41", "45"],
        f=p(9, "GT dao tao HT bon chua NH3 & flare"),
        cv="Cương vị vận hành kho NH₃ và hệ thống đuốc",
        sum=["Phần I: hệ thống đuốc – năng suất, các trường hợp xả khẩn cấp và thành phần khí, mô tả công nghệ đuốc NH₃ 40-PK-1001 và đuốc khí tổng hợp 40-PK-1002 (KO drum 40-V-1001), nguyên lý làm việc và vận hành.",
             "Phần II: bồn chứa NH₃ 40-TK-5001 – thông số thiết kế, logic bảo vệ, tác động của NH₃ tới sức khỏe; quy trình khởi động và ngừng.",
             "Hướng dẫn vận hành cụm làm lạnh 40-PK-5001, đưa hơi NH₃ sang máy nén 10-K-4051 X.Amo, bơm NH₃ lỏng (cấp X.Urê/Amo/NPK, nạp xe bồn).",
             "Cụm làm lạnh mới 40-PK-5005: quy trình công nghệ, màn hình HMI, quá tải, logic, dầu bôi trơn, xả dầu V4, khởi động và ngừng."],
        key=["40-TK-5001: 35.000/29.500 m³, 20.000 tấn, −33 °C, 0,04–0,10 barg, bồn kép hai vách.",
             "40-PK-5001 600 kg/h, 40-PK-5005 250 kg/h hơi NH₃; bơm 40-P-5001A/B, 5002/5003: 85 m³/h, 368 m.",
             "Đuốc NH₃ 298.190 kg/h, đuốc khí tổng hợp 349.674 kg/h, cao 45 m; dòng CO/CO₂ tách khỏi dòng NH₃ để tránh carbamate."]),
}

OM = {  # Operation Manual gốc của Technip (tham khảo thêm)
    "Utilities": ([F + "Operation Manual Utilities.doc", "Operation Manual Utilities (Technip, bản Word)"], [F + "OM Utility.pdf", "Operation Manual Utilities (bản scan)"],
                  ["18", "31", "32", "33", "35", "36", "37"]),
    "WWT": ([F + "Operating Manual WWT.doc", "Operating Manual WWT (Technip)"], None, ["42"]),
    "Flare": ([F + "Operation Manual flare&ammonia storage.doc", "Operation Manual Flare & Ammonia storage (Technip)"], None, ["41", "45"]),
}


def build():
    auto = json.load(open(os.path.join(HERE, "gtcv_auto.json")))
    gt, gtu = {}, {}
    for k, e in GT.items():
        e = dict(e, toc=auto[k]["toc"], q=auto[k]["q"])
        gt[k] = e
        for u in e["units"]:
            gtu.setdefault(u, []).append(k)
    om = {}
    for k, (a, b, us) in OM.items():
        for u in us:
            om.setdefault(u, []).extend([x for x in (a, b) if x])
    return {"gt": gt, "gtu": gtu, "gtom": om}
