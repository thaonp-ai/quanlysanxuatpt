"""Công nghệ Unit 36 – Hệ thống sản xuất nitơ 30-PK-6001 (Linde CryoPlants GAN 600, MR 4112-50).

Nguồn: PFD 2098-36-PFD-0010-2 as-built, P&ID 2098-36-PID-0031-01/02/03 (bảng thông số thiết bị),
Vol 1 O&M mục 4 "Process Description" (Linde, 2003), "Process calculation Phu My 7829 240+30" (Linde, 2002),
quy trình vận hành G2-30-QT-01-006, tài liệu đào tạo công nghệ (bản dịch tiếng Việt),
màn hình điều khiển & giá trị cài đặt 04/12/2016, báo cáo/thống kê sự cố 2009–2010, hội thảo giám sát đại tu 30-PK-6001.
"""
R = "8. Hệ thống Nito/"
V1 = R + "30-PK-6001 (MR-4112-50) Nitrogen/Vol 1 O&M/"


def sh(dwg, label):
    return ["sheet:" + dwg, label]


def ent(t, intro, s=None, src=None):
    return {"t": t, "intro": intro, "s": s or [], "src": src or []}


PFD = sh("2098-36-PFD-0010-2", "PFD 2098-36 Hệ thống sản xuất nitơ")
PID1 = sh("2098-36-PID-0031-01", "P&ID 36-01 Khí vào, chiller, cụm hấp phụ")
PID2 = sh("2098-36-PID-0031-02", "P&ID 36-02 Cold box & tuabin")
PID3 = sh("2098-36-PID-0031-03", "P&ID 36-03 Bồn LIN & thiết bị bay hơi")

S_DESC = [V1 + "Sect 4/Sect 4 Process Description.doc", "Linde – Mô tả công nghệ (Vol 1 mục 4)"]
S_CALC = [R + "Nitrogen BD 2011/Process calculation Phu My7829  240+30.doc", "Linde – Tính toán công nghệ 240 + 31 Nm³/h"]
S_QT = [R + "a30-QT-01-006_QTVH CỤM SẢN XUẤT NITƠ ok.doc", "Quy trình vận hành G2-30-QT-01-006"]
S_TR = [R + "Process Training Vietnam done.docx", "Tài liệu đào tạo công nghệ (tiếng Việt)"]
S_HMI = [R + "nito word ngày 04-12-2016.pdf", "Màn hình điều khiển & giá trị cài đặt (2016)"]
S_POI = [R + "Nitrogen BD 2011/116SAMa.doc", "Linde – Hướng dẫn vận hành GAN 600"]
S_SC = [R + "Su co Nito.xlsx", "Thống kê sự cố 2009–2010"]
S_BC = [R + "Bao cáo nito.docx", "Báo cáo hệ thống N2 09/2010"]
S_DT = [R + "HỘI THẢO TRAO ĐỔI KINH NGHIỆM KHI GS ĐẠI TU 30-PK-6001.pdf", "Hội thảo giám sát đại tu 30-PK-6001"]

UNIT = {
    "t": "Công nghệ Unit 36 – Hệ thống sản xuất nitơ",
    "intro": "Cụm 30-PK-6001 (Linde CryoPlants, kiểu GAN 600) tách nitơ từ không khí bằng chưng cất nhiệt độ thấp. "
             "Công suất thiết kế 240 Nm³/h khí N₂ độ tinh khiết 99,9 % (thiết kế ≤ 3 ppm O₂), kèm khoảng 31 Nm³/h nitơ lỏng. "
             "Nitơ lỏng được đưa vào bồn 30-PK-6001/TK1 (25 m³). Khi cụm dừng hoặc nhu cầu vượt công suất, LIN trong bồn được hóa hơi qua 30-PK-6001/E1A/B để cấp bù cho mạng. "
             "Khí N₂ cấp cho mạng phân phối ở 7 barg, 10–20 °C, tới các xưởng Amoniac, Urê và Phụ trợ.",
    "s": [
        {"h": "Sơ đồ dòng (PFD as-built)",
         "ul": ["Khí nén công nghệ từ mạng khí nén (bình 30-V-5001, DWG 35-01) vào cụm: ≈875 Nm³/h, 8,5 barg, 45 °C (dòng 36.1). "
                "Theo tính toán của Linde, cần ≈1.139 Nm³/h khí khô ở 8,4 barg cho chế độ 240 Nm³/h khí + 31 Nm³/h lỏng.",
                "Khí đi qua bình đệm V1, được làm lạnh và tách nước (chiller ACC1, E5/E6, bộ lọc), rồi qua cụm hấp phụ DR1 (V2/V3) để loại H₂O, CO₂, CO và hydrocacbon nhẹ.",
                "Trong cold box: khí được làm lạnh sâu ở trao đổi nhiệt chính E3 và vào đáy tháp T1. N₂ tinh khiết ra ở đỉnh, lỏng giàu O₂ ở đáy. "
                "Lạnh cho quá trình do tuabin giãn nở EK1 tạo ra.",
                "Sản phẩm N₂ (dòng 36.2) ≈190 Nm³/h, 7,0 barg, 20 °C, 99,9 % N₂. Chia cho xưởng Amoniac (≈83 Nm³/h), Urê (≈101 Nm³/h) và Phụ trợ (≈6 Nm³/h).",
                "Khí thải giàu O₂ (dòng 36.6, ≈685 Nm³/h, 21–40 % O₂) quay về tái sinh bình hấp phụ rồi xả ra khí quyển; khí xả tái sinh ≈320 Nm³/h (dòng 36.7).",
                "Ghi chú PFD: lưu lượng tối đa 1.096 Nm³/h khi nhà máy chạy công suất thiết kế. Đỉnh 1.000 Nm³/h khi purge nhà máy, lấy bằng cách hóa hơi nitơ lỏng."],
         "src": [PFD, S_CALC, S_DESC]},
        {"h": "Chỉ tiêu sản phẩm",
         "tb": [["Chỉ tiêu", "Giá trị"], ["Áp suất cấp", "7 barg"], ["Nhiệt độ cấp", "10–20 °C"], ["Độ tinh khiết", "99,9 %tt N₂"], ["O₂", "≤ 0,1 %tt"]],
         "p": ["Áp suất và nhiệt độ N₂ cấp ra mạng được giữ bằng PIC-36241 và TSL-36242, tác động lên van PV-36241 và TV-36370."],
         "src": [S_QT]},
        {"h": "Thiết bị chính (bảng trên P&ID)",
         "tb": [["Tag", "Chức năng", "Thông số"],
                ["30-PK-6001/V1", "Bình đệm khí vào", "1.200 D × 2.300 L; 14 barg; 75 °C"],
                ["30-PK-6001/ACC1", "Chiller nước giải nhiệt gió", "18 kW"],
                ["30-PK-6001/E5", "TĐN tấm gioăng không khí – nước lạnh", "≈10 kW; 6,21 m²; 12 barg"],
                ["30-PK-6001/E6", "TĐN tấm gioăng không khí – không khí", "≈9 kW; 6,21 m²; 12 barg"],
                ["30-PK-6001/DR1 (V2/V3)", "Cụm hấp phụ tái sinh nhiệt (TSA), 2 bình MS", "1.096 Nm³/h @ 8 barg; CO₂ ra < 0,1 ppm; bình 800 D × 2.030 L, 13 barg"],
                ["30-PK-6001/E3", "TĐN chính kiểu plate-fin", "143 kW; 46 m²; −196/60 °C"],
                ["30-PK-6001/T1", "Tháp chưng cất áp cao (HP column)", "356 × 10.567 mm; 52 đĩa lý thuyết (thực tế đệm cấu trúc 9,5 m); 12 barg"],
                ["30-PK-6001/V4", "Bình tách pha", "305/1.270 D × 1.477 H; 12 barg"],
                ["30-PK-6001/E4", "Thiết bị ngưng tụ chính kiểu plate-fin", "49 kW ngưng tụ N₂; 46 m²"],
                ["30-PK-6001/EK1", "Tuabin giãn nở (turbo expander)", "308 Nm³/h; ΔP 7,4 bar"],
                ["30-PK-6001/ABC1", "Quạt làm mát mạch phanh tuabin", "340 Nm³/h; ΔP 0,1 bar"],
                ["30-PK-6001/TK1", "Bồn nitơ lỏng cách nhiệt chân không", "25 m³; 2.180 ID × 10.700 H; 11 barg; −196/60 °C"],
                ["30-PK-6001/E1A/B", "Thiết bị hóa hơi LIN kiểu khí quyển (luân phiên)", "460.000 kJ/h mỗi bộ; 11 barg"],
                ["30-PK-6001/E2A/B", "Thiết bị hóa hơi tạo áp bồn (luân phiên)", "2.336 kJ/h; 11 barg"]],
         "src": [PID1, PID2, PID3]},
        {"h": "Các chế độ vận hành",
         "ul": ["Chế độ 1 và 2 (tuabin): tuabin EK1 tạo lạnh, cụm cho cả khí và lỏng. Có thể chọn làm lạnh nhanh (rapid cool-down), dùng thêm LIN từ bồn. "
                "Khi tải thay đổi, sản lượng khí điều chỉnh được trong khoảng 190–240 Nm³/h.",
                "Chế độ 5 (economiser): không chạy tuabin, LIN từ bồn được phun vào cold box để cấp lạnh (van XY-36288, HV-36339).",
                "Chế độ 0: dừng cold box, dùng khi thổi khô (purge) cold box.",
                "Khi nhu cầu nhỏ hơn sản lượng tối thiểu, khí dư được xả qua bộ tiêu âm và áp mạng vẫn giữ trong dải hẹp. "
                "Khi bồn LIN đầy, cụm tự hóa hơi LIN để giữ mức bồn 95–100 % mà không phải dừng cụm."],
         "src": [S_QT, S_DESC]},
        {"h": "Khởi động và làm lạnh",
         "ul": ["Điều kiện trước khởi động:",
                "• áp bình đệm PG-36701 > 8,5 barg;",
                "• áp bồn LIN trong khoảng 7,4–7,8 barg;",
                "• áp bổ sung N₂ đặt thấp hơn áp mạng 0,5 barg (7,0 barg tại PT-36241).",
                "Khởi động từ HMI (Plant on): hệ thống tăng áp, mở van cấp khí, đưa cụm APU vào chạy, rồi chọn chế độ vận hành.",
                "Ở chế độ tuabin, trước khi làm lạnh phải thổi mạch tuabin để làm sạch bụi bẩn trong HX1A (XY-36282, XY-36284 mở). "
                "Theo quy trình bước này mất 4 giờ; thực tế đặt 260 phút. Bỏ qua bước này có thể làm hỏng tuabin.",
                "Van vào cold box XY-36224 mở và PV-36230 điều khiển áp tháp, sau đó van vào tuabin mở. TT-36225 giảm tới ≈160 K. "
                "Lỏng tích dần ở đáy tháp và thiết bị ngưng tụ; LV-36232 bắt đầu điều khiển mức.",
                "Khi độ tinh khiết đạt, XV-36245 mở và FV-36227 điều khiển lưu lượng sản phẩm. "
                "LV-36226 thổi sạch đường ống rồi bắt đầu chuyển LIN về bồn.",
                "Nếu O₂ vượt 3,5 ppm, hệ thống tự đóng XV-36245 và LV-36226."],
         "src": [S_QT, S_POI, S_HMI]},
        {"h": "Thổi khô cold box và dừng máy",
         "ul": ["Thổi cold box (thủ công) theo các bước:",
                "1. Chuyển sang chế độ 5, đóng HV-36748 (đường LIN về bồn). Chờ hết lỏng trong tháp, cụm tự dừng.",
                "2. Chuyển sang chế độ 0, mở 100 % HV-36330 (đầu xả) và HV-36331 (đầu vào).",
                "3. Khí khô ≈300 K từ APU thổi ngược qua HX1A. Thổi tới khi hết tuyết ở HV-36330, thêm 6 giờ, đến khi độ ẩm đầu xả < 5 ppm.",
                "Bắt buộc thổi khi khởi động lần đầu, hoặc khi cụm đã chạy liên tục trên 4.000 giờ rồi dừng khoảng 48 giờ.",
                "Dừng ngắn hạn: dừng từ HMI và đóng HV-36748 để cô lập bồn LIN. "
                "Dừng dài hạn: thổi thêm cold box, cô lập thiết bị phân tích (HV-36343) và cắt điện. Chiller vẫn chạy khi các thiết bị khác đã dừng."],
         "src": [S_QT, S_TR]},
        {"h": "Sự cố thường gặp (2009–2010 và quy trình)",
         "ul": ["Bình V2/V3 trip áp cao khi chuyển sang tái sinh. Nguyên nhân: van XV-36260/36262 không chạy (solenoid, đường khí điều khiển), van XV-36260/61/62/67 đóng không kín, van một chiều CH-36743/744 hỏng, hoặc van giảm áp XY-36226 không mở.",
                "Tuabin trip do áp gối đỡ thấp hoặc lỗi PSH-36236. Lỗi cold box \"analogue bad quality fault\" do tín hiệu thiết bị đo xấu.",
                "Chiller trip tổng (XA-36299), ví dụ do kẹt van tiết lưu môi chất; trip cả cụm khi mất điện.",
                "LV-36226 rò làm đóng băng trong cold box. PV-36230 rò ở chân van. O₂ trong sản phẩm cao hoặc dao động (phải chuyển XV-36245 sang tay).",
                "O₂ dao động khi lưu lượng tiêu thụ của Urê/Amoniac thay đổi nhiều.",
                "Áp khí vào thấp khi máy nén khí trip hoặc nhà máy dùng nhiều khí nén: cần chạy máy nén dự phòng.",
                "Thời tiết lạnh (khí vào 22–23 °C): TV-36218 đóng nhỏ (≈24 %), áp vào cold box dao động, có thể trip tuabin ở 8 barg. "
                "Cách xử lý: đặt lại nhiệt độ khí vào cold box (TT-36218) sao cho TV-36218 mở 60–100 %."],
         "src": [S_QT, S_SC, S_BC]},
        {"h": "Lưu ý khi đại tu",
         "ul": ["Dừng cụm từ HMI, xả áp hệ thống, cắt điện chiller và quạt ABC1.",
                "Khi cụm dừng, logic điều khiển áp bồn TK1 không làm việc; áp bồn phải chỉnh hoàn toàn bằng van tay.",
                "Các van dự phòng TV-36370, PV-36241, XV-36253 có thể bảo dưỡng sau khi cụm đã chạy lại và cho sản phẩm.",
                "Trước khi tháo van/thiết bị: ghi tagname, đánh dấu chiều lưu chất và chụp ảnh. Bịt kín đầu ống hở."],
         "src": [S_DT]},
    ],
    "src": [S_DESC, S_QT, S_TR, PFD],
}

TAGS = {
    "30-PK-6001": ent("Cụm sản xuất nitơ 30-PK-6001",
                      "Cụm tách khí kiểu GAN 600 của Linde CryoPlants (MR 4112-50): 240 Nm³/h N₂ 99,9 % ở 7,5 barg (thiết kế ≤ 3 ppm O₂), kèm ≈31 Nm³/h nitơ lỏng. "
                      "Có các khối: bình đệm V1; làm lạnh khí vào (chiller ACC1, E5, E6); hấp phụ DR1 (V2/V3); "
                      "cold box (E3, T1, V4, E4, tuabin EK1 + ABC1); bồn LIN TK1 với các bộ hóa hơi E1A/B, E2A/B. "
                      "Điều khiển bằng PLC tại tủ LCP001, có màn hình HMI; một số tín hiệu và van bypass nối về DCS.",
                      [{"h": "Cân bằng thiết kế (Linde, 2002)",
                        "tb": [["Thông số", "Giá trị"], ["Khí vào (khô)", "1.139 Nm³/h; 8,4 barg"], ["Tải lạnh chiller", "12,9 kW"],
                               ["Tuabin", "304 Nm³/h; 7,58 → 0,20 barg; 151,7 → 101,9 K; 4,8 kW"],
                               ["Tháp", "Ống 14\", đệm Linde A750Y cao 9,5 m; 7,7 barg; khí thải 415 Nm³/h, 34,6 % O₂"],
                               ["Thiết bị ngưng tụ", "25,6 kW; áp phía lỏng thải ≈3,6 barg"], ["Sản phẩm", "240 Nm³/h khí 7,5 barg + 31 Nm³/h lỏng"]]}],
                      [S_CALC, S_DESC, PFD]),
    "30-PK-6001/V1": ent("Bình đệm khí vào 30-PK-6001/V1",
                         "Bình 1.200 D × 2.300 L (14 barg) nhận khí nén vào cụm. Bình tách phần lớn nước, chặn cặn bẩn từ đường ống, và giảm dao động áp/lưu lượng để hệ điều khiển kịp phản ứng. "
                         "Khi khởi động, XYS-36257 mở để tăng áp từ từ. XV-36205 chỉ mở khi chênh áp giữa V1 và cụm TSA đủ nhỏ (≈0,5 bar), tránh dòng lớn làm hỏng lọc và bình hấp phụ. "
                         "Áp tại PG-36701 phải > 8,5 barg mới khởi động được.",
                         src=[S_TR, S_QT, PID1]),
    "30-PK-6001/ACC1": ent("Chiller 30-PK-6001/ACC1",
                           "Chiller nước giải nhiệt gió 18 kW, gồm máy nén môi chất lạnh, dàn ngưng, bồn và bơm nước. Nước pha ethylene glycol chống đông. "
                           "Nước lạnh làm mát khí vào xuống ≈7–10 °C để ngưng tụ hơi nước trước cụm hấp phụ. "
                           "Nước lạnh không được dưới 0 °C, vì băng hình thành trong khí nén sẽ làm hỏng hoặc tắc lọc phía sau; đặt tối thiểu 5 °C để có dự phòng. "
                           "PLC báo động khi nhiệt độ nước ngoài giới hạn. Chiller trip tổng (XA-36299) sẽ dừng cả cụm. Chiller vẫn chạy khi cụm dừng, nên phải cô lập điện trước khi bảo dưỡng.",
                           src=[S_TR, S_QT, S_BC, PID1]),
    "30-PK-6001/E5": ent("Trao đổi nhiệt 30-PK-6001/E5",
                         "TĐN tấm có gioăng (≈10 kW, 6,21 m², 12 barg), trao đổi giữa không khí và nước lạnh từ chiller ACC1. "
                         "Cùng với E6, đưa khí vào xuống ≈7–10 °C để tách nước. Nước ngưng được tách tiếp ở bộ tách xoáy và lọc coalescing FIL-1509A/B. "
                         "Khí vào cold box được giữ ≈20 °C bằng TV-36218 (TT-36218). Khi trời lạnh, E5 trao đổi ít nên khí vào thấp hơn đặt trị; khi đó cần chỉnh đặt trị để TV-36218 mở 60–100 %.",
                         src=[PID1, S_TR, S_QT, S_CALC]),
    "30-PK-6001/E6": ent("Trao đổi nhiệt 30-PK-6001/E6",
                         "TĐN tấm có gioăng không khí – không khí (≈9 kW, 6,21 m², 12 barg), đặt trước E5 trong cụm làm lạnh khí vào (chiller / refrigeration drier). "
                         "Theo tính toán của Linde, tổng tải làm lạnh khí vào là 12,9 kW: làm mát 6,3 kW và ngưng tụ hơi nước 6,3 kW.",
                         src=[PID1, S_CALC]),
    "30-PK-6001/DR1": ent("Cụm hấp phụ 30-PK-6001/DR1",
                          "Cụm làm sạch không khí (APU) kiểu hấp phụ tái sinh nhiệt (TSA), 2 bình V2/V3: một bình làm việc, bình kia tái sinh. "
                          "Công suất 1.096 Nm³/h @ 8 barg, CO₂ ra < 0,1 ppm. "
                          "Loại bỏ H₂O, CO₂, CO và hydrocacbon nhẹ (C₂H₂, C₃H₈). Nếu không loại, các chất này sẽ đóng băng trong E3/E4, gây tắc hoặc nguy cơ nổ nhỏ ở V4. "
                          "Khí tái sinh là khí thải giàu O₂ từ cold box, được gia nhiệt bằng điện trở đặt trong từng bình (EY-36212/36213).",
                          [{"h": "Chu trình (bước 1–7 / 11–17)",
                            "ul": ["Bình đang hấp phụ, đồng thời bình kia lần lượt qua các bước: chờ → giảm áp → gia nhiệt (tới khi đầu bình đạt ≈100 °C) "
                                   "→ làm nguội (tới khi chênh nhiệt độ vào/ra < 4 °C) → kiểm tra van → tăng áp và chờ → chạy song song.",
                                   "Chỉ bước chạy song song và bước giảm áp tính theo thời gian. Bước hấp phụ kết thúc theo tổng lưu lượng khí qua bình (theo tài liệu đào tạo: 7.148 m³) hoặc tổng thời gian chạy (680 phút). "
                                   "Vì vậy khi sản lượng thấp, chu kỳ dài ra và tiết kiệm điện gia nhiệt.",
                                   "Khí thải tái sinh xả qua PV-36221 (đặt ≈0,23 barg). Áp này không được vượt 0,5 barg vì gây áp ngược lên tuabin."]}],
                          [S_TR, PID1, S_HMI]),
    "30-PK-6001/V2": ent("Bình hấp phụ 30-PK-6001/V2",
                         "Bình rây phân tử 800 D × 2.030 L, 13 barg / 75 °C, làm việc luân phiên với V3 trong cụm DR1. "
                         "Bình gồm 3 lớp: alumina hoạt tính 300 mm (186 kg) để tách nước; xúc tác (35 kg) để loại CO — yêu cầu riêng của dự án; "
                         "rây phân tử MS13X 1.050 mm (611 kg) để tách CO₂ và hydrocacbon nhẹ. Mỗi bình có điện trở gia nhiệt khí tái sinh đặt bên trong. "
                         "Sự cố hay gặp: trip áp cao khi vào tái sinh, do van chuyển đổi XV-36260/36262 hoặc van giảm áp không làm việc, hoặc van đóng không kín.",
                         src=[S_TR, PID1, S_QT, S_DT]),
    "30-PK-6001/E3": ent("Trao đổi nhiệt chính 30-PK-6001/E3",
                         "TĐN nhôm plate-fin (143 kW, 46 m², −196/60 °C) trong cold box, gồm các khối HX1A, HX1B, HX1C. "
                         "Khí vào được làm lạnh ngược chiều với dòng N₂ sản phẩm, khí thải và khí ra tuabin. Một phần khí có thể hóa lỏng trước khi vào đáy tháp T1. "
                         "N₂ sản phẩm và khí thải ra khỏi cold box ở nhiệt độ môi trường. "
                         "HX1A được thổi ngược bằng khí khô từ APU khi thổi cold box; trước khi làm lạnh, thổi mạch tuabin để làm sạch bụi.",
                         src=[S_DESC, S_TR, S_QT, PID2]),
    "30-PK-6001/T1": ent("Tháp chưng cất 30-PK-6001/T1",
                         "Tháp áp cao Ø356 mm, cao 10.567 mm, làm việc ≈7,7 barg, dùng đệm cấu trúc dạng tấm (Linde A750Y, cao 9,5 m) thay vì đĩa. Tháp có bộ phân phối và bộ phân phối lại lỏng. "
                         "Khí vào ở đáy được tách thành N₂ tinh khiết ở đỉnh và lỏng giàu O₂ (≈35 %) ở đáy. "
                         "Một phần N₂ đỉnh được ngưng ở E4 và hồi lưu (55–65 % lượng N₂ đỉnh). Một phần nhỏ LIN hồi lưu được lấy qua LV-36226 về bồn TK1 khi độ tinh khiết đạt. "
                         "Độ tinh khiết được điều khiển gián tiếp qua tỉ lệ thu hồi: FT-36227 / (FT-36227 + FT-36223 − lưu lượng tuabin), chỉnh bằng FV-36223. "
                         "Đặt tỉ lệ thu hồi quá cao làm độ tinh khiết xấu đi chỉ trong vài phút.",
                         src=[S_DESC, S_TR, S_CALC, PID2]),
    "30-PK-6001/V4": ent("Bình tách pha 30-PK-6001/V4",
                         "Bình tách pha (305/1.270 D × 1.477 H, 12 barg) của hệ thiết bị ngưng tụ chính. "
                         "Lỏng giàu O₂ từ đáy tháp qua van LV-36232 được giảm áp, bay hơi một phần và lạnh xuống, rồi vào V4 và E4. "
                         "LV-36232 giữ V4 và E4 ngập hoàn toàn để hỗn hợp ra khỏi E4 vẫn còn > 80 % lỏng. "
                         "Nếu bay hơi khô, tạp chất (nhất là C₂H₂) có thể kết tinh, gây nguy cơ nổ nhỏ. "
                         "Áp V4 (PT-36233, ≈3,6–3,9 barg) thay đổi theo lưu lượng qua FV-36223: áp thấp làm tăng chênh nhiệt độ ở E4, tăng hồi lưu.",
                         src=[S_TR, S_CALC, S_HMI, PID2]),
    "30-PK-6001/E4": ent("Thiết bị ngưng tụ chính 30-PK-6001/E4",
                         "TĐN plate-fin 49 kW (46 m²): ngưng N₂ đỉnh tháp bằng lỏng giàu O₂ đã giảm áp. N₂ lỏng hồi lưu về đỉnh tháp; lỏng thải bay hơi và qua E3 ra ngoài. "
                         "Hydrocacbon dư tích tụ ở đây được xả định kỳ: van XY-36249 mở một lúc để xả một ít lỏng (≈60 % O₂) qua bộ hóa hơi VP-2, cao 2–3 m. "
                         "PLC theo dõi chu kỳ nhiệt độ ở TT-36231 và dừng cụm nếu không thấy nhiệt độ dao động quanh đặt trị trong 1 giờ.",
                         src=[S_DESC, S_TR, S_QT, PID2]),
    "30-PK-6001/EK1": ent("Tuabin giãn nở 30-PK-6001/EK1",
                          "Tuabin hướng tâm vào trong (Linde), gối đỡ khí, 308 Nm³/h. Khí áp cao từ E3 giãn nở gần đoạn nhiệt ≈7,6 → 0,2 barg, lạnh xuống ≈102 K, rồi quay về E3 để cấp lạnh. "
                          "Khí gối đỡ lấy từ khí điều khiển qua PCV-36753 và lọc FIL-6102. "
                          "Năng lượng được thải qua bánh phanh trên trục, tuần hoàn khí qua quạt làm mát ABC1. Tốc độ được giữ bằng áp mạch phanh (≈0,4 barg). "
                          "Van vào tuabin XV/ZV-36298 đóng khi tuabin dừng và mở 55 % khi liên động được xóa và quạt ABC1 đã chạy. "
                          "Điện trở E-36234 bật khi khí vào lạnh tới ≈−130 °C, để tránh tạo lỏng trong tuabin (dưới ≈140 K). "
                          "Trip thường gặp: áp gối đỡ thấp, PSH-36236, áp vào cao (8 barg).",
                          src=[S_TR, S_HMI, S_CALC, S_BC, PID2]),
    "30-PK-6001/ABC1": ent("Quạt làm mát tuabin 30-PK-6001/ABC1",
                           "Dàn làm mát không khí (air blast cooler, 340 Nm³/h) của mạch phanh tuabin EK1. Bánh phanh tuần hoàn khí qua ABC1 để thải nhiệt lấy ra từ tuabin. "
                           "Van vào tuabin chỉ mở khi quạt ABC1 đã chạy. Khi đại tu cần cắt điện ABC1, và kiểm tra chiều quay sau vệ sinh.",
                           src=[S_DESC, S_TR, S_HMI, S_DT]),
    "30-PK-6001/TK1": ent("Bồn nitơ lỏng 30-PK-6001/TK1",
                          "Bồn 25 m³, Ø2.180 × 10.700 mm, cách nhiệt chân không, 11 barg. Nhận LIN từ cold box hoặc từ xe bồn. "
                          "LIN dùng cho khởi động nhà máy, làm lạnh nhanh/chế độ economiser, và cấp bù N₂ khi cụm dừng.",
                          [{"h": "Kiểm soát áp suất và mức",
                            "ul": ["Khi cụm chạy, áp bồn được giữ thấp hơn áp tháp bằng XY-36201 theo PT-36202 (xả hơi dư). Vận hành thường 7,4–7,8 barg.",
                                   "Khi cụm dừng, áp do bộ điều áp PCV-36751 (đặt 7,7 barg) giữ, và XV-36252 tự cô lập cụm khỏi bồn. "
                                   "Theo kinh nghiệm đại tu, lúc này logic áp bồn không làm việc và phải chỉnh bằng van tay.",
                                   "Chống đầy bồn: LC-36203 mở khi LT-36203 > 98 % và đóng khi < 95 %. FO-36772 đặt lưu lượng cao hơn sản lượng LIN ≈50 % để mức giảm chậm.",
                                   "Thiết bị hóa hơi tạo áp E2A/B giữ áp bồn khi rút LIN tới 1.000 Nm³/h."]}],
                          [S_TR, S_QT, S_DT, PID3]),
    "30-PK-6001/E1": ent("Thiết bị hóa hơi LIN 30-PK-6001/E1A/B",
                         "Hai bộ hóa hơi khí quyển dạng ống cánh (460.000 kJ/h mỗi bộ), chạy luân phiên, cho phép hóa hơi liên tục tới 1.000 Nm³/h. "
                         "Mỗi bộ được tính để sau 8 giờ chạy 1.000 Nm³/h ở môi trường 15 °C, khí ra vẫn > 10 °C. "
                         "Khi nhu cầu vượt sản lượng, áp mạng giảm; PC-36241 (PT-36241, đặt thấp hơn áp mạng ≈0,5 bar) mở để hóa hơi LIN cấp bù.",
                         [{"h": "Điều khiển nhiệt độ khí cấp bù",
                           "ul": ["TV-36370 đóng bớt để giảm lưu lượng khi khí ra lạnh dưới 10 °C (TT-36242), tức là bộ hóa hơi đang quá tải.",
                                  "TV-36366 bypass một ít LIN quanh bộ hóa hơi khi trời nóng và lưu lượng thấp, giữ khí ≤ 20 °C.",
                                  "XY-36253: đường bypass quanh PC-36241 / TV-36370, dùng khi bảo dưỡng hoặc khi cần lưu lượng lớn hơn thiết kế. Van fail-close, chỉ mở được từ DCS."]}],
                         [S_TR, PID3]),
    "30-PK-6001/E2": ent("Thiết bị hóa hơi tạo áp 30-PK-6001/E2A/B",
                         "Hai bộ hóa hơi không khí môi trường (luân phiên, 11 barg). Bộ hóa hơi rút một ít LIN từ đáy bồn TK1, hóa hơi rồi trả hơi về đỉnh bồn, để giữ áp bồn khi rút LIN với tốc độ tới 1.000 Nm³/h. "
                         "Trên P&ID, cụm có van XYS-36764/36765 và PCV-36763/36747. Khi cụm chạy, các bộ hóa hơi của bồn được cô lập ở XV-36764/36765.",
                         src=[S_TR, PID3]),
}
TAGS["30-PK-6001/V3"] = dict(TAGS["30-PK-6001/V2"], t="Bình hấp phụ 30-PK-6001/V3",
                             intro=TAGS["30-PK-6001/V2"]["intro"].replace("luân phiên với V3", "luân phiên với V2"))
