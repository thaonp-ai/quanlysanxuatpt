"""Công nghệ Unit 18 – Lò hơi phụ 10-B-8001 & hệ nước cấp lò.

Nguồn: sách vận hành Macchi Part 1D (mục 1, 2, 4, 7, 9, 14, 15, 17, 18 – bản scan, đọc bằng OCR),
778-C-073 (tiêu hao phụ trợ), data sheet thiết bị trong "1. Cac cum thiet bi_tank lien quan",
PFD 2539-18-PFD-0010-01-01 (as-built 08/03/2018, case 2: NH3 sang Urê).
"""
LH = "Lo hoi phu tro/"
EQ = LH + "1. Cac cum thiet bi_tank lien quan/"


def d1(n, name, label):
    return [LH + f"Tach theo muc/1D {n} - {name}.pdf", f"Macchi 1D-{n} · {label}"]


S_GEN = d1(1, "General Description", "Mô tả chung")
S_DS = d1(2, "Boiler Data Sheets", "Data sheet & hiệu suất lò")
S_BMS = d1(4, "Description Of BMS Operation", "Mô tả BMS")
S_LOGIC = d1(5, "BMS Logic Diagram", "Sơ đồ logic BMS")
S_CTRL = d1(7, "Control Functional Description", "Mô tả điều khiển")
S_CE = d1(9, "Cause and Effect Chart", "Cause & Effect")
S_PSV = d1(14, "Safety Valves Setting", "Chỉnh định van an toàn")
S_OP = d1(15, "Operating Procedures", "Quy trình vận hành")
S_VOT = d1(16, "Valves Operating Table", "Bảng trạng thái van")
S_SERV = d1(17, "Operation During Boiler Service", "Vận hành thường xuyên")
S_WT = d1(18, "Feed Water And Boiler Water Treatment", "Xử lý nước cấp & nước lò")
S_PRES = d1(19, "Boiler Preservation", "Bảo quản lò")
S_BURN = d1("22.1", "Burners and Pilots", "Đầu đốt & mồi")
S_FAN = d1("23.1", "FD Fan", "Quạt gió FD")
S_CLU = d1("23.2", "Automatic Clutches", "Khớp ly hợp tự động")
S_MOT = d1("23.3", "Electric Motor", "Motor quạt FD")
S_TUR = d1("23.4", "Steam Turbine", "Turbine quạt FD")
S_DSH = d1("26.4", "Desuperheater", "Bộ giảm ôn")
S_SUV = d1(35, "Start-Up Vent Silencer", "Bộ tiêu âm xả khởi động")
S_SAMP = d1(40, "Sampling System", "Hệ lấy mẫu")
S_UTIL = [LH + "PART 1F/VOL. 17/778-C-073.pdf", "778-C-073 · Tiêu hao phụ trợ"]
S_PID_S = [LH + "PART 1F/VOL. 17/778-S-001.pdf", "778-S-001 · P&ID nước/hơi, gió/khói"]
S_PID_F = [LH + "PART 1F/VOL. 17/778-S-006.pdf", "778-S-006 · P&ID khí nhiên liệu"]
S_TDS = [EQ + "10-B-8001.pdf", "Data sheet lò 10-B-8001 (Technip)"]
S_PFD = ["sheet:2539-18-PFD-0010-01-01 (trang 1)", "PFD 2539-18 case 2 (as-built)"]
S_PFD3 = ["sheet:2539-18-PFD-0010-11-01 (trang 1)", "PFD 2539-18 case 3 (as-built)"]
S_PID_FW = ["sheet:2098-18-PID-0031-01", "P&ID 2098-18-PID-0031-01 Nước cấp lò"]
S_PID_DOS = ["sheet:2098-18-PID-0031-02", "P&ID 2098-18-PID-0031-02 Châm hóa chất"]
S_PID_B = ["sheet:2098-18-PID-0031-03", "P&ID 2098-18-PID-0031-03 Lò hơi phụ"]
S_PID_BD = ["sheet:2098-18-PID-0031-04", "P&ID 2098-18-PID-0031-04 Giảm áp & xả đáy"]
S_PID_DUMP = ["sheet:2098-18-PID-0031-05", "P&ID 2098-18-PID-0031-05 Xả hơi LP (dump)"]
S_P1 = [EQ + "10-P-8001-AB/10-P-8001 A&B.pdf", "Data sheet bơm 10-P-8001A/B"]
S_T1 = [EQ + "10-P-8001-AB/10-STP-8001.pdf", "Data sheet turbine 10-STP-8001"]
S_P2 = [EQ + "10-P-8002-AB/10-P-8002 A&B.pdf", "Data sheet bơm 10-P-8002A/B"]
S_T2 = [EQ + "10-P-8002-AB/10-STP-8002.pdf", "Data sheet turbine 10-STP-8002"]
S_P3 = [EQ + "10-P-8003 A&B.pdf", "Data sheet bơm 10-P-8003A/B"]
S_DEG = [EQ + "10-PK-8004.pdf", "Data sheet tháp khử khí 10-PK-8004"]
S_V1 = [EQ + "10-V-8001/10-V-8001.pdf", "Data sheet bình khử khí 10-V-8001"]
S_V2 = [EQ + "10-V-8002/10-V-8002.pdf", "Data sheet bình 10-V-8002"]
S_V3 = [EQ + "10-V-8003/10-V-8003.pdf", "Data sheet bình 10-V-8003"]
S_V4 = [EQ + "10-V-8004/10-V-8004.pdf", "Data sheet bình 10-V-8004"]
S_E1 = [EQ + "10-E-8001.pdf", "Data sheet 10-E-8001"]
S_E2 = [EQ + "10-E-8002.pdf", "Data sheet 10-E-8002"]
S_K1 = [EQ + "10-PK-8001/10-PK-8001.pdf", "Data sheet cụm 10-PK-8001"]
S_K2 = [EQ + "10-PK- 8002/10-PK-8002.pdf", "Data sheet cụm 10-PK-8002"]
S_K3 = [EQ + "10-PK- 8003/10-PK-8003.pdf", "Data sheet cụm 10-PK-8003"]
S_SL1 = [EQ + "10-SL-8001.pdf", "Data sheet 10-SL-8001"]
S_SL2 = [EQ + "10-SL-8002.pdf", "Data sheet 10-SL-8002"]
S_SL3 = [EQ + "10-SL-8003.pdf", "Data sheet 10-SL-8003"]

UNIT = {
    "t": "Công nghệ Unit 18 – Nước cấp lò hơi và lò hơi phụ trợ",
    "intro": "Unit 18 sinh hơi cao áp (HS, 39 barg / 380 °C) cho nhà máy bằng lò hơi phụ 10-B-8001 (Macchi TITAN M, đốt khí). "
             "Unit này cũng chuẩn bị và bơm nước cấp lò cho lò phụ và cho các nồi hơi thu hồi nhiệt (WHB) của xưởng Amoniac. "
             "Nước khử khoáng và nước ngưng được khử khí ở 10-PK-8004/10-V-8001, sau đó bơm 10-P-8001A/B (HHP, 144 barg) và 10-P-8002A/B (HP, 60 barg) đẩy đi. "
             "Hơi được phân phối qua các header VHS/KS, HS, LS. Trạm giảm áp, hệ xả đáy và hệ xả hơi LP (dump) giữ cân bằng áp suất.",
    "s": [
        {"h": "Sơ đồ dòng (PFD case 2, as-built)",
         "ul": ["Nước khử khoáng từ xưởng Demi (≈343 t/h, 43 °C) được gia nhiệt qua 10-E-8001, 10-E-3004/3005, 10-E-7004 lên ≈121 °C, cùng nước ngưng hồi về vào tháp khử khí 10-PK-8004 "
                "(lượng nước vào bình khử khí ≈357 t/h).",
                "Tháp khử khí 10-PK-8004 đặt trên bình chứa 10-V-8001 (1,9 barg, ≈132 °C), dùng hơi LS ≈6,7 t/h; khí không ngưng xả ra khí quyển. "
                "Oxygen scavenger (10-PK-8003) châm vào bình khử khí, chất kiềm hóa (10-PK-8002) châm vào nước cấp.",
                "Bơm HHP 10-P-8001A/B (một bơm dẫn động turbine 10-STP-8001, một bơm motor) cấp ≈236,6 t/h nước ở 144 barg cho nồi hơi thu hồi nhiệt (WHB) của xưởng Amoniac.",
                "Bơm HP 10-P-8002A/B (turbine 10-STP-8002 / motor) cấp ≈126,3 t/h nước ở 60 barg: ≈74,8 t/h vào lò phụ 10-B-8001, ≈50,5 t/h cho WHB, phần nhỏ cho giảm ôn trạm giảm áp.",
                "Lò phụ 10-B-8001 sinh ≈74,1 t/h hơi HS 39 barg / 380 °C (công suất thiết kế 140 t/h), đốt ≈4,6 t/h khí nhiên liệu LP ở 6,5 barg. Phosphate (10-PK-8001) châm vào bao hơi.",
                "Header HS cấp hơi cho turbine quạt FD 10-B-8001/STK1, turbine bơm 10-STP-8001/8002, turbine máy nén 10-STK-4041/4021/2001, hộ tiêu thụ Amoniac/Urê. "
                "Trạm giảm áp HS→LS (van giảm áp + giảm ôn, bộ tiêu âm 10-SL-4011) giữ áp header LS 3,4 barg.",
                "Xả đáy liên tục (≈0,75 t/h) về bình 10-V-8002: hơi chớp (≈0,3 t/h) về header LS, nước qua 10-E-8001 làm mát xuống 50 °C. "
                "Xả đáy định kỳ về bình 10-V-8003 (bộ tiêu âm 10-SL-8002).",
                "Hơi LS dư được xả về bình ngưng không khí 10-E-8002 (dump condenser, bình thường không có lưu lượng). Nước ngưng gom về 10-V-8004, rồi bơm 10-P-8003A/B đưa về bình khử khí."],
         "src": [S_PFD, S_PFD3, S_PID_FW, S_PID_B, S_PID_BD, S_PID_DUMP]},
        {"h": "Thiết bị chính",
         "tb": [["Tag", "Chức năng", "Thông số chính"],
                ["10-B-8001", "Lò hơi phụ Macchi TITAN M 7/96", "140 t/h; 39 barg / 380 °C; 4 đầu đốt Low-NOx khí; hiệu suất 90 % (LHV)"],
                ["10-PK-8004 / 10-V-8001", "Tháp khử khí kiểu đệm + bình chứa", "374 m³/h nước khử khí; 1,85 barg / 132 °C; bình Ø3.700 × 11.100 mm"],
                ["10-P-8001A/B", "Bơm nước cấp HHP (Nuovo Pignone DDHF 6×13, 10 cấp)", "283 / 351 m³/h (thường / định mức); đẩy 141,5 barg; cột áp 1.518 m"],
                ["10-STP-8001", "Turbine dẫn động bơm HHP (Tuthill-Coppus ALHA28)", "2.200 kW; 5.240 v/ph; hơi vào 38 barg / 370 °C, thoát 3,4 barg"],
                ["10-P-8002A/B", "Bơm nước cấp HP (Nuovo Pignone MSND 6×11, 6 cấp)", "100 / 230 m³/h; đẩy 53,2 barg; cột áp 561 m"],
                ["10-STP-8002", "Turbine dẫn động bơm HP (Tuthill-Coppus RLHB28)", "457 kW; 2.980 v/ph"],
                ["10-P-8003A/B", "Bơm nước ngưng", "3 / 30 m³/h; đẩy 4,73 barg; cột áp 48,2 m"],
                ["10-PK-8001/8002/8003", "Châm phosphate / chất kiềm hóa / oxygen scavenger", "Bơm piston định lượng, bồn 1,4 m³"],
                ["10-V-8002 / 10-V-8003", "Bình xả đáy liên tục / định kỳ", "Ø700 × 2.500 mm / Ø1.120 × 2.300 mm"],
                ["10-V-8004", "Bình nước ngưng", "Ø1.400 × 3.300 mm, nằm ngang"],
                ["10-E-8001", "Làm mát nước xả đáy (bằng nước khử khoáng)", "1,75 GJ/h; xả đáy 148 → 50 °C"],
                ["10-E-8002", "Bình ngưng xả hơi LP làm mát bằng không khí", "2 bay, quạt cưỡng bức; dự phòng tới ≈19 t/h hơi"]],
         "src": [S_TDS, S_DS, S_DEG, S_V1, S_P1, S_T1, S_P2, S_T2, S_P3, S_K1, S_K2, S_K3, S_V2, S_V3, S_V4, S_E1, S_E2]},
        {"h": "Các mức áp hơi & nước (PFD)",
         "tb": [["Header / dòng", "Áp (barg)", "Nhiệt độ (°C)", "Ghi chú"],
                ["VHS / KS (từ WHB Amoniac)", "108", "510", "≈234 t/h, cấp turbine 10-STK-4031"],
                ["HS – hơi cao áp", "38–39", "370–380", "Lò phụ ≈74 t/h + hơi thoát/giảm áp từ STK-4031 ≈212 t/h"],
                ["LS – hơi thấp áp", "3,4", "220", "Từ turbine thoát và trạm giảm áp; cấp bình khử khí, urê, các hộ dùng"],
                ["Nước cấp HHP", "144", "132", "Bơm 10-P-8001A/B → WHB Amoniac"],
                ["Nước cấp HP", "60", "132", "Bơm 10-P-8002A/B → lò phụ, WHB, giảm ôn"],
                ["Khí nhiên liệu LP vào lò phụ", "6,5", "19", "≈4,6 t/h"]],
         "src": [S_PFD]},
        {"h": "Chất lượng nước (hướng dẫn Macchi)",
         "kv": [["Nước cấp (bao hơi < 64 barg)", "O₂ < 0,02 mg/kg; độ cứng < 1 mg/kg CaCO₃; Fe < 0,05 mg/kg; Cu < 0,01 mg/kg; pH 25 °C 9–9,5; dầu < 1 mg/kg"],
                ["Nước lò (41–64 barg)", "Độ kiềm P < 150 mg/kg; SiO₂ < 8 mg/kg; PO₄ < 10 mg/kg (≤ 3 ppm khi nước cấp không có độ cứng); độ dẫn điện < 2.500 µS/cm; pH 10,5–10"],
                ["Hơi cấp turbine", "Độ dẫn điện sau trao đổi cation < 0,2 µS/cm; SiO₂ < 0,02 mg/kg; Fe < 0,02; Na+K < 0,01; Cu < 0,003 mg/kg. "
                 "Lò cấp hơi cho turbine nên áp giới hạn nước lò của dải 81–125 barg (trừ SiO₂)."],
                ["Xả đáy liên tục", "Dự kiến khoảng 1 % lưu lượng hơi khi vận hành; thiết kế cơ khí tính 3 %"]],
         "src": [S_WT, S_DS]},
        {"h": "Tiêu hao phụ trợ của lò phụ ở tải định mức (778-C-073)",
         "kv": [["Khí nhiên liệu GPP / AMF", "8,23 / 8,31 t/h, 6 barg (thiết kế 10 barg)"],
                ["Hơi cho turbine quạt FD", "11,2 t/h (tối đa 16,8 t/h), 38 barg / 370 °C"],
                ["Nước cấp lò", "141,4 t/h (tối đa 144,2 t/h), 52,8 barg, 130 °C"],
                ["Khí điều khiển / khí công nghệ", "100 / 80 Nm³/h"],
                ["Điện", "448 kW ở 6,6 kV (motor quạt FD); 3,3 kW ở 230 V"]],
         "src": [S_UTIL]},
    ],
}

BOILER = {
    "t": "Lò hơi phụ 10-B-8001",
    "intro": "Lò ống nước tuần hoàn tự nhiên, hai bao hơi (Macchi TITAN M 7/96), đặt ngoài trời, đỡ từ đáy. Buồng đốt áp dương. "
             "Khói đi hết chiều dài buồng đốt rồi qua bộ quá nhiệt, chùm ống bốc hơi và bộ hâm nước, sau đó ra ống khói cao 30 m. "
             "Lò có 4 đầu đốt khí Low-NOx đặt ở mặt trước, dùng chung một hộp gió. Lò được giám sát bởi hệ điều khiển tự động và hệ quản lý đầu đốt (BMS).",
    "s": [
        {"h": "Thông số thiết kế",
         "kv": [["Sản lượng hơi", "140 t/h (không có tải đỉnh)"], ["Hơi quá nhiệt tại ranh giới", "39 ± 0,5 barg; 380 ± 5 °C"],
                ["Dải điều chỉnh nhiệt độ hơi", "40–100 % tải"], ["Dải điều chỉnh đầu đốt", "10–100 %"], ["Nhiệt độ nước cấp", "130 °C"],
                ["Hiệu suất (LHV)", "Bảo đảm 90 %, dự kiến 91 %"], ["Áp suất thiết kế lò / bộ hâm nước", "51 barg"],
                ["Bề mặt truyền nhiệt", "1.506 m² (bộ hâm nước có cánh 2.780 m²)"], ["Thể tích nước", "Tổng 50,2 m³; ở mức thường 41,8 m³"],
                ["Thể tích buồng đốt / EPRS", "236 m³ / 194 m²"], ["Công suất van xả khởi động", "14 t/h"], ["Tiêu chuẩn", "ASME Section I"]]},
        {"h": "Hiệu suất dự kiến (khí GPP)",
         "tb": [["Thông số", "100 % MCR", "80 % MCR", "50 % MCR"],
                ["Hơi (kg/h)", "140.000", "112.000", "70.000"], ["Nước phun giảm ôn (kg/h)", "4.790", "4.460", "3.300"],
                ["Nước cấp vào bộ hâm (kg/h)", "136.610", "108.660", "67.400"], ["Không khí dư ở đầu đốt (%)", "10", "10", "15"],
                ["O₂ trong khói ướt (%)", "1,69", "1,69", "2,43"], ["Khói ra ống khói (°C)", "203", "186", "164"],
                ["Nhiệt độ khói ra buồng đốt (°C)", "1.372", "1.320", "1.195"], ["Áp bao hơi (barg)", "44,5", "42,7", "40,6"],
                ["Áp nước vào bộ hâm (barg)", "46,7", "44,3", "41,6"], ["Áp gió sau quạt FD (mmH₂O)", "616", "385", "159"]]},
        {"h": "Cấu tạo",
         "ul": ["Bao hơi trên Ø1.500 × 60 mm (SA 516-70), dài phần trụ 10.800 mm. Bên trong có tấm chắn, cyclone tách hơi và bộ sấy hơi; có ống phân phối nước cấp, ống châm hóa chất và ống xả đáy liên tục.",
                "Bao nước dưới Ø1.000 × 50 mm, dài 10.000 mm, có các đầu xả, đặt trên gối đỡ bê tông.",
                "Vách buồng đốt là ống có cánh hàn kín (\"D-tubes\", vách trước, vách sau), bọc bông khoáng bên ngoài. Vật liệu chịu lửa chỉ dùng ở họng đầu đốt và sàn buồng đốt.",
                "Bộ quá nhiệt hai cấp (SH1 sơ cấp, SH2 cuối) bằng ống trơn SA 213 T11 Ø44,5 mm, có bộ giảm ôn phun nước ở giữa hai cấp.",
                "Chùm ống bốc hơi đi một pass ngang. Các hàng ống lạnh đóng vai trò ống xuống; ống lên và ống cấp đặt ngoài đường khói.",
                "Bộ hâm nước (E1) ống đứng có cánh, đặt ở đầu ra khói; khói đi ngang.",
                "Quạt gió FD (K1) ly tâm một cửa hút, dẫn động bằng motor điện (MK1) hoặc turbine hơi (STK1) qua hai khớp ly hợp tự động. "
                "Bình thường khởi động bằng motor, khi có hơi HP thì chuyển sang turbine. Lưu lượng gió điều chỉnh bằng damper hút FV-8250.",
                "Van an toàn: 2 van lò xo trên bao hơi, 1 van trên đường hơi quá nhiệt ra, 1 van trên đường hơi thoát của turbine quạt FD. "
                "Có bộ tiêu âm ở cửa hút quạt FD và ở van xả khởi động bộ quá nhiệt (HV-8251).",
                "Hệ lấy mẫu: làm mát mẫu nước lò, hơi bão hòa và hơi quá nhiệt; đo độ dẫn điện (3 điểm) và pH (nước lò)."],
         "src": [S_GEN, S_DS, S_SAMP]},
        {"h": "Điều khiển",
         "ul": ["Điều khiển chủ lò (\"two-element boiler follow\"): PIC-4048 giữ áp header HS ở 39 barg, cộng tín hiệu feed-forward theo tải hơi, tạo thành \"Boiler Demand\". "
                "Trạm HIC-8250 cho phép chạy tay. Nhu cầu bị giới hạn theo công suất các đầu đốt đang chạy; báo động WAH-8250 khi vượt quá.",
                "Gió – nhiên liệu kiểu cross-limit: nhu cầu gió lấy giá trị lớn hơn (FY-8250B), nhu cầu nhiên liệu lấy giá trị nhỏ hơn (FY-8201E). "
                "Nhờ vậy khi tăng tải thì gió tăng trước, khi giảm tải thì nhiên liệu giảm trước. Hệ số không khí dư thay đổi theo tải, có hiệu chỉnh O₂ (AIC-8250, đặt ≈1,7 % ở 80–100 % tải).",
                "Khí nhiên liệu: FIC-8201 điều khiển van FV-8201; bộ chọn PIC-8202 giới hạn áp khí tới đầu đốt ở 2,3 barg (trip PAHH-8203). FV-8201 tự đóng khi mồi đầu đốt thứ nhất.",
                "Mức bao hơi điều khiển 3 phần tử (mức, lưu lượng hơi, lưu lượng nước) bằng van 100 % FV-8251 (FIC-8251). "
                "Dưới khoảng 25–30 % tải dùng van 30 % LV-8250 (LIC-8250); trên 35 % tải tự chuyển về FV-8251. Mức có bù áp suất.",
                "Nhiệt độ hơi ra giữ ở 380 °C bằng vòng cascade TIC-8253 → lưu lượng nước giảm ôn qua van FV-8252."],
         "src": [S_CTRL]},
        {"h": "Bảo vệ (BMS – Master Fuel Trip)",
         "ul": ["Nguyên nhân MFT: nút dừng khẩn tại tủ đầu đốt (HS-8201) hoặc tại phòng điều khiển (HS-8202); mức bao hơi thấp-thấp (2/3 LIT-8251/8252/8253); "
                "lưu lượng gió thấp-thấp (2/3 FIT-8254/8255/8256); tốc độ quạt FD thấp-thấp (SSLL-8290); áp buồng đốt cao-cao (PIT-8251); "
                "áp khí nhiên liệu thấp-thấp (PIT-8204, có hiệu lực sau khi đầu đốt 1 cháy) hoặc cao-cao (PIT-8203); mất toàn bộ ngọn lửa (XA-8204); tất cả nhiên liệu bằng 0.",
                "Khi MFT: đóng van ngắt khí chính và van từng đầu đốt/mồi, mở các van xả (vent), cắt đánh lửa. Rơ-le MFT cắt trực tiếp nguồn các van điện từ.",
                "Thổi sạch buồng đốt (purge) ≥ 5 phút với lưu lượng gió ≥ 25 % MCR, bắt buộc trước khi mồi lần đầu sau MFT và khi đầu đốt thứ nhất không có lửa trong 5 giây. "
                "Kiểm tra rò van khí (leak test) là một phần của purge.",
                "Khi trip do gió thấp-thấp, damper FV-8250 giữ nguyên vị trí ít nhất 5 phút (\"waiting time for air trip\")."],
         "src": [S_BMS, S_CE, S_LOGIC]},
        {"h": "Khởi động & vận hành",
         "ul": ["Chuẩn bị: lò đã súc rửa hóa chất, thổi đường hơi và chỉnh van an toàn xong. Cấp nước tới mức trên mức tối thiểu 20–25 mm; đóng damper quạt FD, mở cửa gió từng đầu đốt; đặt các van theo bảng.",
                "Chạy bơm nước cấp và quạt FD → BMS yêu cầu tăng gió lên 25 % để purge → mồi đầu đốt 1 (từng bước hoặc tự động).",
                "Khi áp bao hơi đạt 150–200 kPa(g): đóng vent bao hơi và các xả bộ quá nhiệt, giữ mở van xả khởi động HV-8251. "
                "Sau đó tiết lưu dần van này để tăng nhiệt độ bão hòa theo gradient khuyến nghị.",
                "Khi áp hơi quá nhiệt thấp hơn áp vận hành khoảng 2 bar: mở van bypass để sấy đường ống, cân áp rồi mở van chặn hơi chính, đóng HV-8251. Mồi tiếp các đầu đốt 2–4 theo tải.",
                "Dừng lò không giữ áp: giảm tải tới mức ổn định thấp nhất, tắt đầu đốt, dùng quạt FD làm nguội cưỡng bức (giảm 50 °C/h), châm đầy nước bao hơi.",
                "Trong vận hành: kiểm tra ống thủy mức nước bằng cách xả ít nhất mỗi ca; xả đáy bao nước ít nhất mỗi ngày một lần. "
                "Không xả đáy qua các ống góp vách buồng đốt khi lò đang chạy. Châm phosphate vào bao hơi theo kết quả phân tích mẫu.",
                "Chỉnh định van an toàn sau khi thổi đường hơi, theo thứ tự: van bao hơi → thổi bộ quá nhiệt → van bộ quá nhiệt. Giữ mức nước ở mức thường hoặc thấp hơn khi thử."],
         "src": [S_OP, S_VOT, S_SERV, S_PSV]},
    ],
    "src": [S_TDS, S_PID_B, S_PID_S, S_PID_F],
}

SUBS = {
    "10-B-8001/V1": {"t": "Bao hơi 10-B-8001/V1", "intro": "Bao hơi trên Ø1.500 × 60 mm, SA 516-70, phần trụ dài 10.800 mm, thiết kế 51 barg / 291 °C. "
                     "Đủ lớn để tích trữ hơi và hạn chế dao động mức. Thiết bị bên trong gồm tấm chắn và tấm tách, cyclone nằm ngang, bộ sấy hơi; "
                     "có ống phân phối nước cấp, ống châm phosphate, ống xả đáy liên tục. Mức đo bằng 3 transmitter LIT-8251/8252/8253 (trip mức thấp-thấp 2/3) và ống thủy Klinger.",
                     "s": [], "src": [S_GEN, S_DS, S_CTRL]},
    "10-B-8001/V2": {"t": "Bao nước 10-B-8001/V2", "intro": "Bao nước dưới Ø1.000 × 50 mm, SA 516-70, dài 10.000 mm. Đặt trên gối đỡ, có các đầu xả đáy định kỳ (xả ít nhất mỗi ngày một lần khi vận hành).",
                     "s": [], "src": [S_GEN, S_DS, S_SERV]},
    "10-B-8001/SH1": {"t": "Bộ quá nhiệt sơ cấp 10-B-8001/SH1", "intro": "Ống trơn SA 213 T11 Ø44,5 × 4,0 mm, 48 ống song song, 60 m², thiết kế 475 °C. "
                      "Hơi ra ≈326 °C ở 100 % MCR, sau đó đi qua bộ giảm ôn phun nước (FV-8252) trước khi vào bộ quá nhiệt cuối.", "s": [], "src": [S_DS, S_GEN, S_DSH]},
    "10-B-8001/SH2": {"t": "Bộ quá nhiệt cuối 10-B-8001/SH2", "intro": "Ống trơn SA 213 T11 Ø44,5 × 4,0 mm, 54 ống song song, 70 m², thiết kế 500 °C. "
                      "Hơi ra 380 °C, giữ bằng vòng cascade TIC-8253 → lưu lượng nước giảm ôn. Có van an toàn trên đường hơi ra và van xả khởi động HV-8251.", "s": [], "src": [S_DS, S_CTRL]},
    "10-B-8001/E1": {"t": "Bộ hâm nước 10-B-8001/E1", "intro": "Ống đứng có cánh (236 cánh/m), Ø51 × 3,2 mm, 2.780 m² kể cả cánh, thiết kế 51 barg. "
                     "Nước vào 130 °C, ra ≈193 °C; khói vào ≈412 °C, ra ống khói ≈203 °C (ở 100 % MCR). Có vỏ kín khí, xả cạn được.", "s": [], "src": [S_DS, S_GEN]},
    "10-B-8001/K1": {"t": "Quạt gió FD 10-B-8001/K1", "intro": "Quạt ly tâm một cửa hút, có bộ tiêu âm cửa hút và damper điều chỉnh FV-8250 (khí nén) ở cửa hút. "
                     "Dẫn động bằng motor MK1 hoặc turbine STK1 qua hai khớp ly hợp Marland tự động: khớp phía máy đang chạy thì đóng, phía kia nhả. "
                     "Áp gió sau quạt ≈616 mmH₂O ở 100 % MCR; tổng gió ≈121.000 Nm³/h. Trip lò khi tốc độ quạt thấp-thấp (SSLL-8290).",
                     "s": [], "src": [S_GEN, S_FAN, S_CLU, S_DS, S_CE]},
    "10-B-8001/MK1": {"t": "Motor quạt FD 10-B-8001/MK1", "intro": "Motor 6,6 kV (≈448 kW theo danh mục tiêu hao). Dùng để khởi động quạt FD; khi đủ điều kiện và có hơi HP thì chuyển sang turbine STK1.",
                      "s": [], "src": [S_MOT, S_UTIL, S_GEN]},
    "10-B-8001/STK1": {"t": "Turbine quạt FD 10-B-8001/STK1", "intro": "Turbine hơi dùng hơi HS (38 barg / 370 °C, ≈11,2 t/h thường, tối đa 16,8 t/h), thoát ra header LS. "
                       "Đường thoát có van an toàn. Có tủ điều khiển tại chỗ và bộ giám sát tốc độ.", "s": [], "src": [S_TUR, S_UTIL, S_GEN]},
    "10-B-8001/SK1": {"t": "Ống khói 10-B-8001/SK1", "intro": "Ống khói tự đứng cao 30 m. Có đầu đo phân tích khói AIT-8002, nhiệt độ khói TE/TT-8008, đầu lấy mẫu AP-8503, cửa kiểm tra ở chân và bọc bảo vệ người.",
                      "s": [], "src": [S_GEN]},
    "10-B-8001/SL2": {"t": "Bộ tiêu âm xả khởi động 10-B-8001/SL2", "intro": "Lắp trên đường xả khởi động bộ quá nhiệt (van HV-8251, công suất xả 14 t/h). Dùng khi khởi động lò, trước khi mở van chặn hơi chính.",
                      "s": [], "src": [S_SUV, S_OP, S_DS]},
    "10-B-8001/SL1": {"t": "Bộ tiêu âm cửa hút quạt FD 10-B-8001/SL1", "intro": "Giảm ồn tại cửa hút gió của quạt FD.", "s": [], "src": [S_GEN]},
}

AUX = {
    "10-PK-8004": {"t": "Tháp khử khí 10-PK-8004", "intro": "Tháp khử khí kiểu đệm đặt trên bình chứa 10-V-8001. Hơi LS (≈3,4 barg / 220 °C) đi ngược chiều với nước khử khoáng và nước ngưng để đuổi O₂ và CO₂; khí không ngưng xả ra khí quyển.",
                   "s": [{"h": "Thông số (data sheet)", "kv": [["Nước khử khí", "374 m³/h ở 132 °C (khi khởi động 312 m³/h); dải 60–100 %"], ["Áp / nhiệt độ vận hành", "1,85 barg / 132 °C"],
                                                              ["Nước ngưng vào", "348 m³/h, 104 °C / 1,98 barg"], ["Thiết kế phía hơi", "6 barg / 310 °C"]]}],
                   "src": [S_DEG, S_PFD]},
    "10-V-8001": {"t": "Bình khử khí 10-V-8001", "intro": "Bình chứa nước đã khử khí (Ø3.700 × 11.100 mm, nằm ngang), đặt dưới tháp 10-PK-8004, vận hành ≈1,9 barg / 132 °C. "
                  "Cấp nước cho bơm 10-P-8001A/B và 10-P-8002A/B. Có đầu châm oxygen scavenger (10-PK-8003), đầu hồi lưu lưu lượng nhỏ nhất của bơm, đầu tràn. Mức điều khiển bằng LIC-8005.",
                  "s": [], "src": [S_V1, S_PFD, S_PID_FW]},
    "10-P-8001": {"t": "Bơm nước cấp HHP 10-P-8001A/B", "intro": "Bơm ly tâm nhiều cấp Nuovo Pignone DDHF 6×13 (10 cấp). 10-P-8001A dẫn động bằng turbine 10-STP-8001, 10-P-8001B bằng motor 10-MP-8001B. "
                  "Cấp nước HHP 144 barg cho nồi hơi thu hồi nhiệt (WHB) của xưởng Amoniac.",
                  "s": [{"h": "Thông số (data sheet)", "kv": [["Lưu lượng thường / định mức", "283 / 351 m³/h"], ["Áp hút max / định mức", "4,9 / 2,53 barg"],
                                                              ["Áp đẩy / chênh áp", "141,5 barg / 139 bar"], ["Cột áp", "1.518 m"], ["NPSHA", "7 m"],
                                                              ["Nhiệt độ bơm", "132 °C (áp hơi bão hòa 2,85 bara)"], ["Hiệu suất", "≈78 %"]]},
                         {"h": "Vận hành (PFD case 2)", "p": ["≈236,6 t/h nước HHP 144 barg cho WHB Amoniac. Có van hồi lưu lưu lượng nhỏ nhất về bình khử khí."]}],
                  "src": [S_P1, S_PFD, S_PID_FW]},
    "10-STP-8001": {"t": "Turbine bơm HHP 10-STP-8001", "intro": "Turbine hơi Tuthill-Coppus ALHA28 dẫn động 10-P-8001A. Công suất định mức 2.200 kW ở 5.240 v/ph, tối đa 2.637 kW; tốc độ liên tục max 5.502 v/ph. "
                    "Hơi vào 38 barg / 370 °C (min 37 barg / 365 °C, max 39 barg / 380 °C), thoát 3,4 barg vào header LS. Tiêu hao riêng 14,6 kg/kWh; lưu lượng qua nozzle max 43,9 t/h. "
                    "Gối đỡ trượt, gối chặn kiểu tilting pad, có trip từ xa bằng van điện từ.", "s": [], "src": [S_T1, S_PFD]},
    "10-P-8002": {"t": "Bơm nước cấp HP 10-P-8002A/B", "intro": "Bơm ly tâm nhiều cấp Nuovo Pignone MSND 6×11 (6 cấp). 10-P-8002A dẫn động bằng turbine 10-STP-8002, 10-P-8002B bằng motor 10-MP-8002B. "
                  "Cấp nước HP 60 barg cho lò phụ 10-B-8001 (qua van FV-8251 / LV-8250), cho WHB và cho giảm ôn trạm giảm áp.",
                  "s": [{"h": "Thông số (data sheet)", "kv": [["Lưu lượng thường / định mức / max", "100 / 230 / 302 m³/h"], ["Cột áp định mức", "561 m"], ["Áp hút", "2,53–4,9 barg"],
                                                              ["Áp đẩy", "53,2 barg"], ["Nhiệt độ bơm", "132 °C"], ["Lưu lượng nhỏ nhất", "90 m³/h (van hồi lưu tự động)"]]},
                         {"h": "Vận hành (PFD case 2)", "p": ["≈126,3 t/h ở 60 barg: ≈74,8 t/h vào lò phụ, ≈50,5 t/h cho WHB."]}],
                  "src": [S_P2, S_PFD, S_PID_FW]},
    "10-STP-8002": {"t": "Turbine bơm HP 10-STP-8002", "intro": "Turbine hơi Tuthill-Coppus RLHB28 dẫn động 10-P-8002A, 457 kW ở 2.980 v/ph. Hơi vào 38 barg / 370 °C, thoát 3,4 barg vào header LS; "
                    "≈6,4 t/h hơi HS theo PFD case 2. Gối đỡ bi, bôi trơn kiểu vòng dầu.", "s": [], "src": [S_T2, S_PFD]},
    "10-P-8003": {"t": "Bơm nước ngưng 10-P-8003A/B", "intro": "Bơm nước ngưng từ bình 10-V-8004 về bình khử khí. Lưu lượng thường 3 m³/h, định mức 30 m³/h; áp hút 0,2 barg, đẩy 4,73 barg; cột áp 48,2 m; NPSHA 3,14 m; nước ngưng ≈100 °C.",
                  "s": [], "src": [S_P3, S_PFD]},
    "10-V-8004": {"t": "Bình nước ngưng 10-V-8004", "intro": "Bình nằm ngang Ø1.400 × 3.300 mm, gom nước ngưng hơi (từ bình ngưng xả hơi 10-E-8002 và các bẫy hơi). "
                  "Cấp cho bơm 10-P-8003A/B; hơi chớp xả qua bộ tiêu âm 10-SL-8003. Mức điều khiển bằng LIC-8006.", "s": [], "src": [S_V4, S_PFD]},
    "10-V-8002": {"t": "Bình xả đáy liên tục 10-V-8002", "intro": "Bình đứng Ø700 × 2.500 mm, nhận nước xả đáy liên tục từ lò phụ (≈0,75 t/h) và từ 10-B-9001. "
                  "Hơi chớp (≈0,3 t/h, 3,5 barg) về header LS; nước qua LIC-8003 sang làm mát ở 10-E-8001.", "s": [], "src": [S_V2, S_PFD, S_PID_BD]},
    "10-V-8003": {"t": "Bình xả đáy định kỳ 10-V-8003", "intro": "Bình đứng Ø1.120 × 2.300 mm, nhận nước xả đáy định kỳ (bao nước, ống góp). Hơi xả ra khí quyển qua bộ tiêu âm 10-SL-8002, nước ra hệ thoát.",
                  "s": [], "src": [S_V3, S_SL2, S_PID_BD]},
    "10-E-8001": {"t": "Làm mát nước xả đáy 10-E-8001", "intro": "Thiết bị trao đổi nhiệt dùng nước khử khoáng (≈12 t/h, 45 → 80 °C) để làm mát nước xả đáy (≈4,3 t/h, 148 → 50 °C). "
                  "Nhiệt tải 1,75 GJ/h; tổn thất áp cho phép 0,7 bar; thiết kế 175 °C.", "s": [], "src": [S_E1, S_PFD]},
    "10-E-8002": {"t": "Bình ngưng xả hơi LP 10-E-8002", "intro": "Bình ngưng làm mát bằng không khí (quạt cưỡng bức, 2 bay 3,2 × 7,2 m, motor 11 kW mỗi quạt), thiết kế 6 barg / 310 °C. "
                  "Ngưng hơi LS dư khi header LS thừa hơi. Bình thường không có lưu lượng; thiết kế cho ≈19 t/h trong trường hợp bất thường. Nước ngưng về 10-V-8004.",
                  "s": [], "src": [S_E2, S_PFD, S_PID_DUMP]},
    "10-PK-8001": {"t": "Cụm châm phosphate 10-PK-8001", "intro": "Châm dung dịch phosphate vào bao hơi lò phụ (và nồi hơi khác qua các bơm riêng) để giữ độ kiềm nước lò và kết tủa độ cứng. "
                   "Bồn khuấy Ø1.000 × 1.700 mm (1,4 m³), bơm piston định lượng (chỉnh tay 0–100 %), vật liệu AISI 316. "
                   "Phosphate thường giữ 1–3 ppm trong nước lò khi nước cấp không có độ cứng.", "s": [], "src": [S_K1, S_WT, S_PID_DOS]},
    "10-PK-8002": {"t": "Cụm châm chất kiềm hóa 10-PK-8002", "intro": "Châm chất kiềm hóa (amine/ammonia bay hơi) vào nước cấp để giữ pH nước cấp 9–9,5 và chống ăn mòn đường nước ngưng. "
                   "Bơm piston: 12 L/h (thường), 50 L/h (thiết kế). Bồn 1,4 m³ có khuấy.", "s": [], "src": [S_K2, S_WT, S_PID_DOS]},
    "10-PK-8003": {"t": "Cụm châm oxygen scavenger 10-PK-8003", "intro": "Châm chất khử oxy vào bình khử khí 10-V-8001 để khử phần O₂ còn lại sau khử khí cơ học (nước cấp O₂ < 0,02 mg/kg). "
                   "2 bơm piston 10-PK-8003/P1A/B: 7 L/h (thường), 20 L/h (thiết kế). Bồn 1,4 m³.", "s": [], "src": [S_K3, S_WT, S_V1]},
    "10-SL-8001": {"t": "Bộ tiêu âm header LS 10-SL-8001", "intro": "Bộ tiêu âm Boldrocchi cho van xả hơi header LS ra khí quyển (PIC-8008). Lưu lượng 18,5 t/h, 220 °C, áp trước 0,1 barg.", "s": [], "src": [S_SL1, S_PFD]},
    "10-SL-8002": {"t": "Bộ tiêu âm 10-SL-8002", "intro": "Bộ tiêu âm trên đường xả hơi của bình xả đáy định kỳ 10-V-8003, ≈2,3 t/h.", "s": [], "src": [S_SL2]},
    "10-SL-8003": {"t": "Bộ tiêu âm 10-SL-8003", "intro": "Bộ tiêu âm trên đường xả hơi của bình nước ngưng 10-V-8004, ≈0,25 t/h.", "s": [], "src": [S_SL3]},
}
AUX["10-MP-8001"] = AUX["10-P-8001"]
AUX["10-MP-8002"] = AUX["10-P-8002"]

TAGS = {"10-B-8001": BOILER, **SUBS, **AUX}
