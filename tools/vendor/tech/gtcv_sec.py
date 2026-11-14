"""Tóm tắt chi tiết từng chương của giáo trình cương vị (đọc từ PDF G2-30-GT-01…09, 01/2024).
SEC[mã] = [(tiêu đề mục, [dòng; dòng bắt đầu "• " = ý con]), …] — gtcv.build() gắn vào gt[mã]["sec"].
"""

SEC = {
"GT01": [
 ("Chương I – Lý thuyết nước sinh hoạt", [
  "Chỉ tiêu chất lượng nước: vật lý (độ đục, màu, mùi vị, nhiệt độ), hóa học (pH, độ cứng, độ kiềm, Fe, NH₄⁺, Cl⁻, SO₄²⁻, TDS…), vi sinh (coliform, E.coli).",
  "Khử trùng bằng clo: HOCl/OCl⁻ phụ thuộc pH; clo tự do diệt khuẩn nhanh hơn clo liên kết; hiệu quả phụ thuộc clo dư, thời gian lưu, nhiệt độ, pH, chất lơ lửng.",
  "Phải hạn chế sản phẩm phụ CHCl₃ (≤ 100 ppb) → dùng than hoạt tính hấp phụ; clo dư trên mạng ≥ 0,1 mg/l ở điểm xa nhất.",
  "Than hoạt tính khử clo dư: C + 2Cl₂ + 2H₂O → 4HCl + CO₂."]),
 ("Hệ thống nước thô", [
  "Nước công nghiệp (mạng đô thị, 2,5–3 barg) nạp vào bồn 30-TK-2001 (7.155/6.800 m³) qua 30-LV-32001: đóng khi LIT-32001 = 94,1 %, mở khi 93,5 %.",
  "6.000 m³ đáy bồn dành cho chữa cháy: vòi hút bơm nước thô đặt ở cao độ tương ứng 6.000 m³, vòi hút bơm cứu hỏa ở đáy.",
  "Bơm 30-P-2001A/B/C (160 m³/h, 1 chạy – 2 dự phòng) cấp cho cụm Demi 30-PK-1001, header nước service và cụm nước sinh hoạt 30-PK-2001; FIC-32002 tuần hoàn về bồn, đặt 90 m³/h.",
  "Khởi động bơm: điền nước, xả khí, chọn Man, Start từ LCP, mở dần van đẩy. Phân tích chất lượng nước thô 1 lần/tuần.",
  "Ngừng: chỉ dừng khi nhà máy đã ngừng hoàn toàn; ngừng ngắn hạn giữ mức bồn cao nhất, dài hạn xả hết nước."]),
 ("Hệ thống nước sinh hoạt 30-PK-2001", [
  "Thiết kế cho 150 người × 0,3 m³/ngày = 45 m³/ngày, đáp ứng đỉnh gấp 6 lần; năng suất 22 m³/h; bồn 30-TK-2002 260/240 m³ (đủ 5 ngày).",
  "Clo hóa: NaOCl 10 % từ bồn /TK1 → bơm /P1A/B qua bộ trộn tĩnh /Z1 vào đường nước nạp 30-TK-2002.",
  "• LV-32002 mở khi LIT-32002 = 40 %, đóng khi 80 %; bơm /P1 tự chạy khi LV-32002 mở và AIT-32201 thấp 1,1 ppm, dừng khi LV đóng hoặc AIT cao 3,5 ppm; stroke đặt 40 %.",
  "• Bơm /P2 shock NaOCl vào bồn nước thô 30-TK-2001 định kỳ 1 lần/tháng; các bơm NaOCl dừng khi /TK1 mức thấp (giữ 25–100 cm).",
  "Bơm 30-P-2002A/B (22 + 1,4 m³/h) đẩy qua lọc than hoạt tính /FL2A/B (cát, sỏi, than; 1 chạy – 1 dự phòng) và lọc tinh /FL1A/B ra mạng nước sinh hoạt (≥ 4 barg) – cấp cho vòi tắm, vòi rửa mắt khẩn cấp. Bơm được cấp điện từ máy phát diesel dự phòng.",
  "Lọc than tự tái sinh sau 12 giờ hoặc PDAH-32201 = 0,7 bar: rửa ngược 45 m³/h × 10 phút (XV-32205/32202), rửa xuôi 22 m³/h × 5 phút (XV-32206/32204).",
  "Lọc tinh: khi PDI-32701 = 0,7 bar thì cô lập, xả, vệ sinh/thay lõi (thao tác tay).",
  "Interlock: 30-I-32001 (LV-32001), 30-I-32002 LL 86 % dừng 30-P-2001A/B/C và 30-PK-1001/P3, 30-I-32003 (LV-32002), 30-I-32004 LL 20 % dừng 30-P-2002A/B."]),
 ("Hệ thống nước cứu hỏa", [
  "Nhu cầu chữa cháy lớn nhất 900 m³/h; 5.400 m³ dự trữ đủ 6 giờ chạy hết công suất.",
  "3 bơm chính 30-P-4001A/B/C mỗi bơm 500 m³/h (55 % nhu cầu), 9 barg: A motor 6,6 kV, B/C diesel – vẫn đủ nước khi mất điện hoặc 1 bơm hỏng. Thiết kế theo NFPA 20.",
  "Bơm Jockey 30-P-4002A/B (50 m³/h, 7 barg, 1 chạy – 1 dự phòng) giữ áp mạng, bù rò rỉ.",
  "Tự khởi động theo áp mạng: PSL-34201A 6,0 / B 5,5 / C 5,0 barg; bơm A có cần EMERGENCY RUN; bơm diesel để MAIN SWITCH và công tắc trên động cơ ở AUTO.",
  "Chuẩn bị: van hút/đẩy mở hoàn toàn, van tuần hoàn về bồn đóng, dầu bôi trơn và nước làm mát đủ, bồn diesel đủ, ắc quy 24–28 V, nguồn AC 220 V.",
  "Thử liên động định kỳ (G2-30-HD-022): Jockey chạy, áp > 7 barg; đóng van đẩy, mở van tuần hoàn của bơm thử, xả áp đến điểm đặt cho bơm tự chạy; ghi PI-34507A ở 0 / 250 / 500 / 750 m³/h; xong đặt lại AUTO.",
  "Thiếu nước thô để chữa cháy thì dùng nước sông từ bể tháp giải nhiệt.",
  "Phụ lục: bồn diesel tính cho 8 giờ chạy (0,268 GPM × 480 phút ≈ 128,6 gal + 10 %)."]),
 ("Quy trình liên quan", [
  "G2-30-QT-043 vận hành nước thô, sinh hoạt, cứu hỏa; G2-30-HD-021 vận hành bơm cứu hỏa; G2-30-HD-022 thử liên động/thử tải bơm cứu hỏa; G2-30-PA-289 vệ sinh bồn 30-TK-2001; G2-30-PA-214 khi PM3 cắt nước sông bổ sung."]),
],
"GT02": [
 ("Chương I – Lý thuyết nước làm mát", [
  "Tháp giải nhiệt tự nhiên và cưỡng bức (hút/đẩy, dòng ngược/dòng chéo); khái niệm range, approach, heat load, nhiệt độ bầu ướt.",
  "Hiệu suất tháp = (T vào − T ra)/(T vào − T bầu ướt). Lượng bay hơi, blowdown và hệ số cô đặc (C.O.C) quyết định lượng nước bổ sung.",
  "Kiểm soát nước: blowdown, chống cáu cặn (CaCO₃/CaSO₄), kiểm soát ăn mòn, vi sinh (clo hóa)."]),
 ("Thiết kế và mô tả công nghệ", [
  "Làm mát gián tiếp: vòng hở nước sông qua tháp 30-CT-3001A~L; vòng kín nước sạch nhận nhiệt các xưởng rồi nhả cho nước sông ở trao đổi nhiệt tấm 30-E-3001A~I.",
  "Nước sông dùng trực tiếp cho bình ngưng tuabin X.Amo/X.Urê và bình ngưng NH₃ (titan, chịu clo). Vòng kín cho phép dùng thép cacbon (không dùng đồng vì NH₃).",
  "Nước sông: cấp 34 °C / về 43 °C, áp đi/về 4/2 barg; nước sạch: cấp 37 °C / về 46 °C, đi/về 5/3 barg, thiết kế 14.800 m³/h, pH 7,5.",
  "Tháp 12 khoang × 3.109,2 m³/h (1 dự phòng); bể đủ cấp 10 phút; blowdown qua 30-FV-33002; mất nước sông bổ sung thì dùng nước công nghiệp vào khoang 30-CT-3001A.",
  "Bình giãn nở 30-V-3001: đệm N₂ 2–2,3 barg (30-PIC-33101 split range), bù nước Demi qua 30-LIT-33101, tách khí khi rò từ xưởng."]),
 ("Nước sông làm mát", [
  "Nước sông bổ sung rất mặn: Cl⁻ 15.556–19.810 mg/l, TDS 11.700–29.200 mg/l, TSS 6–120 mg/l.",
  "Hóa chất: NaOCl 3.000 kg mỗi 36 giờ; H₂SO₄ liên tục 12 wppm theo blowdown (pH 6,8–7,3, AIT-33001); chống cáu cặn 30-PK-3002 liên tục (Hydrex 2330: 2,59 ppmw hoặc 3DT394: 1,6 ppmw theo blowdown).",
  "Bơm 30-P-3001A~E: 10.100 m³/h, 40 m; tối thiểu 6.000, bình thường 9.060–10.100 m³/h; dòng 145–160 A; motor 60–85 °C.",
  "Khởi động: bể ≥ 70 % (chạy bơm NHR trước), nước làm mát/làm kín trục 2,5–3,5 bar, mở van đẩy 10–15 %, mở van 3 trao đổi nhiệt/bơm, mở ~3 tháp, xả khí, Start tại chỗ, mở dần van đẩy; rồi chạy bơm hóa chất, mở axit, chạy quạt (160–190 A).",
  "Ngừng: dừng châm chống cáu cặn → dừng axit → dừng quạt → dừng bơm NHR → dừng bơm nước sông.",
  "Interlock 30-I-33006: rung vỏ VE-33301 trip 11 mm/s (báo 8 mm/s); nhiệt độ motor TE-33308/33309 trip 100 °C. Bồn axit 30-TK-3001: LV-33006 mở ở 25 %, đóng ở 65 %."]),
 ("Nước ngoài hàng rào (NHR) và lọc 30-PK-3006", [
  "Bơm 30-P-3010A/B: tổng 3.740 m³/h (bổ sung bể 2.930 + làm nguội kênh xả 810), 2,9 barg. Trước khi chạy phải mở hoàn toàn van đẩy BV1/BV2, LV-33001 (hoặc bypass); hướng dẫn thao tác tủ trung thế, tiếp địa.",
  "30-PK-3006: 9 skid × 8 cell anthracite, mỗi skid 500 m³/h. 6 skid lọc nước sông bổ sung (MUF, 3.000 m³/h), 3 skid lọc dòng bên nước tuần hoàn (SSF, 1.325 m³/h: 1.125 về 30-BA-3001, 200 dùng rửa ngược).",
  "PLC tự đổi MUF ↔ SSF theo thời gian; chỉ ở SSF mới rửa ngược: lần lượt 1/8 cell, 3 phút/cell, 30 phút/skid; chế độ Normal (6 MUF + 3 SSF), Peak (6 + 2, 1 dự phòng).",
  "Nước rửa ngược về bể lắng 30-BA-3004 (2 ngăn), châm keo tụ/trợ keo tụ 30-PK-3005 trước bể; cặn hút bằng bơm di động ra xe bồn.",
  "Không có phân tích online – chất lượng do KCS phân tích; dP cell chỉ để tham khảo TSS."]),
 ("Nước sạch làm mát", [
  "Bơm 30-P-3002A~D (2 chạy): 4.200–7.590 m³/h mỗi bơm, đẩy 6–6,5 barg; dưới 4.200 m³/h mở bypass ở đầu đẩy 30-P-3002D.",
  "Khởi động: điền bồn giãn nở ≥ 80 % (LV-33101, đối chiếu LG-33601A/B/C), xả khí, nâng áp N₂ ~2,0 barg (PV-33101A), mở van hút, mở 3 trao đổi nhiệt/bơm, mở van đẩy 5–10 %, Start, mở dần van đẩy. Rung báo 8 / trip 11 mm/s.",
  "Chất ức chế ăn mòn châm bằng 30-PK-3003 vào đầu hút bơm; giữ NaNO₂ theo phân tích.",
  "Interlock: LSLL-33102 bình giãn nở rất thấp dừng tất cả bơm; rung gối VE-33351/52 trip 11 mm/s; nhiệt độ gối bơm/motor trip 90 °C."]),
 ("Quy trình liên quan", [
  "G2-30-QT-045 nước sông làm mát; G2-30-QT-046 nước sạch làm mát; G2-30-QT-058 bơm NHR; G2-00-HD-039/040 xử lý trip bơm 30-P-3001/3002; G2-00-HD-030 trip 30-P-3010, mất nước sông bổ sung."]),
],
"GT03": [
 ("Chương I – Lý thuyết nước lò hơi", [
  "Tạp chất trong nước (khí hòa tan O₂/CO₂, độ cứng, silica, sắt, dầu) gây cáu cặn, ăn mòn, sủi bọt, cuốn theo hơi; chỉ tiêu cho phép giảm khi áp suất lò tăng.",
  "Truyền nhiệt, quá trình hóa hơi, hơi bão hòa/quá nhiệt; các dạng ăn mòn (oxy, kiềm, axit, giòn kiềm, ăn mòn điện hóa).",
  "Xử lý nước cấp: khử khí nhiệt (hơi LP ngược chiều) + khử oxy hóa học; kiềm hóa bằng amine; phosphate trong bao hơi để kết tủa độ cứng và giữ độ kiềm."]),
 ("Hệ thống nước cấp lò hơi", [
  "Chỉ tiêu nước cấp: O₂ < 0,02 mg/kg, độ cứng < 1, Fe < 0,05, Cu < 0,01, SiO₂ < 0,02 mg/kg, pH 9–9,5, dầu < 1.",
  "Hộ dùng nước cấp HP: lò phụ 10-B-8001, HRSG 10-B-9001, lò hơi HHP X.Amo, X.UFC85, quench water.",
  "Nước Demi (30-P-1002A/B) gia nhiệt ở 10-E-3004/3005 X.Amo → 10-PK-8004 qua 10-FV-8003 (~350 t/h) → khử khí bằng hơi LP → bồn 10-V-8001; châm amine 10-PK-8002 và chất khử oxy 10-PK-8003.",
  "Vận hành: 10-PIC-8001 1,2–1,5 barg; nước Demi về 115–120 °C; nước trong bồn 120–130 °C; áp hút bơm 1,2–3,2 barg, đẩy 56–60 barg.",
  "Khởi động khi chưa có hơi LP: điền 10-V-8001 ~80 %, châm amine giữ pH 9–9,5, khử oxy stroke 70–80 %, chạy 10-P-8002B tuần hoàn; có hơi LP: mở 4\" vào đáy bồn gia nhiệt, đưa hơi vào 10-PK-8004 qua PV-8001, đóng 4\" khi TI-8003 ~130 °C, giảm chất khử oxy.",
  "10-P-8002A (turbine 10-STP-8002A): sấy ở 3–5 barg tới ~300 °C phía HP / 200 °C phía LP, reset DCS + Woodward, nâng hơi ~30 barg, Start → idle ~1.100 rpm 30 phút → 2.980 rpm; từ 2.235 rpm (Min GS) chuyển điều khiển DCS. 10-P-8002B chạy motor.",
  "Interlock: 10-I-8020 LALL-8001 (2/3) 45 % trip các bơm nước cấp; 10-I-8021 LAHH-8004 47,3 % mở 10-HV-8004A; 10-I-8004/8005 áp hút 1 barg trip 10-P-8002A/B; PALL-8006 45 barg tự chạy 10-P-8002B."]),
 ("Hệ thống khí nhiên liệu", [
  "Khí trạm khí 24,5 barg cấp thẳng X.NPK, X.Amo (reforming); qua PV-37003 vào 30-V-7003 (đuốc); qua PV-37001 (34.317 Nm³/h) vào 30-V-7001 cao áp → tuabin khí 10-GT-9001 và PV-37002 (27.053 Nm³/h) → 30-V-7002 thấp áp → nhiên liệu reforming, lò phụ, HRSG.",
  "Thành phần khí sau revamp: CH₄ 88,7 %, nhiệt trị ≈ 39 MJ/Nm³; áp 30-V-7002 khi khởi động lò ~6–6,5 barg."]),
 ("Quạt gió FD 10-B-8001/K1", [
  "Dẫn động kép: turbine hơi 10-B-8001/STK1 (1.480 rpm, điều tốc Woodward) hoặc motor 10-B-8001/MK1 (500 kW, 6,6 kV, 53 A, 1.483 rpm).",
  "Tự chuyển turbine → motor: tốc độ quạt < 1.390 rpm (SAL-8290) → MCC tự khởi động MK1; có báo động khi không chuyển được (MXABM-8001)."]),
 ("Lò hơi phụ trợ 10-B-8001", [
  "Macchi Titan M 7/96: 2 bao (hơi V1, nước V2), tuần hoàn tự nhiên, 140 t/h, 380 ± 5 °C, 4 đầu đốt Low-NOx, bộ hâm nước E1, quá nhiệt SH1/SH2 + giảm ôn DSH, ống khói 30 m; điều chỉnh nhiệt độ hơi 40–100 % tải, đầu đốt 10–100 %.",
  "Chuẩn bị: khí nén 8–9 / khí điều khiển 7–8 barg, nước cấp 55–60 barg, mức bao hơi ~70 %, inlet damper 10-FV-8250 đóng, air register mở.",
  "Khởi động: Reset/ACK (STATUS-GRA075) → chạy quạt → BMS tự purge (≥ 25 % MCR ≈ 30.245 Nm³/h, 5 phút) → Leak test → mở PCV-8702/8701 → đánh lửa đầu đốt đầu tiên (thất bại thì quay lại purge).",
  "Gia nhiệt 30–50 °C/h (nguội) hoặc 60–80 °C/h (nóng), mức bao 55–70 %; 1,5–2 barg đóng vent bao hơi; 15–20 barg châm phosphate 10-PK-8001/P1; còn ~2 bar dưới áp mạng thì mở bypass 10-HV-8250 cân áp rồi hòa hơi.",
  "Ổn định: CBD 1 % tải, xả IBD mud drum 1 lần/ca × 1–5 phút; lò chạy Auto 10-HIC-8250A theo áp mạng HP (PIC-4048).",
  "Ngừng: giảm về 10 % MCR, tắt đầu đốt, làm nguội cưỡng bức 50 °C/h bằng quạt; 2 barg mở vent; < 80 °C dừng quạt; bảo quản ướt/khô. Ngừng giữ áp: đóng van hơi chính, van nước cấp và inlet damper.",
  "MFT (2/3 voting): nút khẩn BLP/CCR; mức bao thấp 7,1 %; gió < 24.916 Nm³/h; tốc độ quạt < 900 rpm; áp buồng đốt 45 mbarg; áp khí nhiên liệu thấp 15 mbarg (sau khi tắt đầu đốt đầu) / cao 2,6 barg; mất lửa; mất khí nhiên liệu.",
  "Logic purge: không MFT, ≥ 2 air register mở, mọi van S/O đóng – vent mở, không có lửa, không ở Natural draft / Waiting time for air trip, gió ≥ 30.245 Nm³/h, không Leak test failure."]),
 ("Condensate, blowdown và giám sát", [
  "Blowdown: xả liên tục (CBD) của 10-B-8001 và 10-B-9001 về 10-V-8002 – hơi flash vào mạng LP, nước nóng gia nhiệt nước Demi ở 10-E-8001 (148 → 50 °C) rồi về 10-V-8003 cùng xả định kỳ (IBD).",
  "Condensate: nước ngưng LP và nước ngưng của dump condenser 10-E-8002A~D (hơi LP thừa) về bồn 10-V-8004 → bơm 10-P-8003A/B (30 m³/h) về khử khí 10-PK-8004.",
  "Giám sát ca: mức bao hơi, chất lượng nước cấp/nước lò, xả cặn, phân tích mẫu, kiểm tra xung quanh lò, ghi logsheet.",
  "Phụ lục: công thức bù nhiệt độ/áp suất cho lưu lượng khí nhiên liệu, mức bao hơi, lưu lượng hơi HP."]),
],
"GT04": [
 ("Chương I–III – Lý thuyết", [
  "Tỷ số nén, thể tích riêng; nén đẳng nhiệt/đoạn nhiệt/đa biến; nén nhiều cấp có làm mát trung gian để giảm công nén và nhiệt độ.",
  "Máy nén piston, trục vít (không dầu/phun dầu), ly tâm (đặc tuyến, surge), dọc trục – cấu tạo, ưu nhược điểm.",
  "Không khí ẩm: độ ẩm tuyệt đối/tương đối, điểm sương; làm khô bằng hấp phụ (alumina, rây phân tử) kiểu không gia nhiệt, tái sinh bằng một phần khí khô."]),
 ("Thiết kế hệ thống tại nhà máy", [
  "Nhu cầu 5.600 Nm³/h (khí điều khiển 2.920 + khí nén 2.680); hộ lớn: cụm nitơ ≤ 1.096 Nm³/h, thụ động hóa X.Urê 700 Nm³/h, 20-E-1001/20-K-1001, tiêu thụ gián đoạn ~150 Nm³/h; tổn thất ở máy sấy ~500 Nm³/h.",
  "Máy nén 30-K-5001A~E: 1.400 Nm³/h, 9 barg, 45 °C (4 chạy + 1 dự phòng). Bình 30-V-5001 28,5 m³; bình 30-V-5002 154 m³ – mỗi bình ~10 phút (30-V-5002 từ 8,1 xuống 5 barg).",
  "Khí điều khiển: 8,5 barg tại nơi sản xuất, 7,5 barg tại hộ dùng, tối thiểu 4 barg; điểm sương −25 °C; không dầu, không bụi.",
  "IS-6: 2/3 PIT-35004 = 5 barg → 3 s đóng 30-PV-35003/35004 (cắt khí nén để ưu tiên khí điều khiển) → 30 s sau dừng X.Urê. Thiếu khí kéo dài: phối hợp X.Amo mở 10-FV-4001 cấp process air."]),
 ("Máy nén 30-K-5001A~E", [
  "Trục vít không dầu 2 cấp: cấp 1 nén ~3 barg, ~200 °C → intercooler + tách nước → cấp 2 → aftercooler → 30-V-5001.",
  "Load/Unload bằng Elektronikon và van điện từ Y1: áp lên giới hạn trên thì chạy không tải (van UV xả qua giảm âm, van một chiều đóng), áp xuống giới hạn dưới thì có tải lại.",
  "Khởi động: dầu ≥ 50 %, đóng xả nước ngưng tay, mở nước làm mát, mở khóa E-stop, reset đến khi \"All protection functions are OK\", mở van ra, Start → chạy không tải, 25 s sau tự có tải.",
  "Cài đặt Load/Unload: Menu → Regulation → Modify (4 cặp: 8,4/9,0 – 8,6/9,2 – 8,8/9,4 – 9,0/9,6 barg)."]),
 ("Máy sấy 30-DR-5001 / 30-DR-5002", [
  "30-DR-5001: 1.820 Nm³/h (vào 2.120), chu kỳ 12 phút – sấy 6, tái sinh 6 (xả áp 25 s, thổi 250 s, tăng áp 60 s, song song 25 s), khí tái sinh 320 Nm³/h.",
  "30-DR-5002: 1.100 Nm³/h (vào 1.265), chu kỳ 10 phút – sấy 5, tái sinh 5 (thổi 240 s, tăng áp 60 s), khí tái sinh 165 Nm³/h.",
  "Trình tự: sấy (khí từ đáy lên) → xả áp → thổi khí khô ngược chiều ra giảm âm → tăng áp → chạy song song → đổi bình; lọc trước/sau theo dõi PDI-35705/35706; điểm sương đo ở AIT-35201.",
  "Khởi động 30-DR-5001: đặt đúng vị trí van (V20–V43, XV-35701…35706), tăng áp từ từ, cấp khí cho solenoid (V29), bật ON, chỉnh dòng tái sinh ~300 Nm³/h ở FI-35701 bằng V41/V42."]),
],
"GT05": [
 ("Phần I – Cơ sở lý thuyết", [
  "Chỉ tiêu nước thải: pH, TSS, BOD₅, COD, dầu mỡ, N, P, coliform; tiêu chuẩn thải (TCVN cột A/B) và ngưỡng tiếp nhận của KCN.",
  "Lắng, lắng có keo tụ, tuyển nổi; lọc nhanh/lọc chậm; keo tụ – tạo bông (cấu tạo hạt keo, cơ chế trung hòa điện tích, bắc cầu); khử trùng (vật lý, hóa học – clo)."]),
 ("Cụm nước thải nhiễm dầu 40-PK-2001", [
  "Nước nhiễm dầu các xưởng → lưới vớt rác /Z1 → bể tách dầu trọng lực API /V1 (dây đai gạt dầu /Z2 → bể dầu /BA3) → bể /BA1 → bơm /P1A/B → CPI /V4 (tấm song song).",
  "→ bồn trộn nhanh /TK3 (chất phá nhũ Klaraid CDP1317 – AlCl₃) → bồn keo tụ /TK4 (BetzDearborn CE1154) → tuyển nổi khí hòa tan DAF /Z5 (bơm cao áp /P7, bình bão hòa /V5, bọt 30–120 µm) → bồn cuối /TK5 → bơm /P8A/B sang TK-102 của 40-PK-2003.",
  "Dầu ở /BA3 → bơm /P3A/B → coalescer /V2 (dầu ra phuy, nước về /V1).",
  "Liên động: /P1A/B chạy thì /P5, /Z3, /P9, /Z4, van khí XV-42211 (~4 l/ph, 450 kPa) và DAF tự chạy; /P8A/B chạy/dừng theo LSHL-42208 (H 1.450 / L 500 mm).",
  "Ngừng: chuyển cống về bể dự phòng /BA2, dừng /P1A/B, đưa thiết bị về Dừng.",
  "Pha hóa chất: chất phá nhũ – /TK1 còn 30 cm, nước thô tới 130 cm, hóa chất tới 180 cm, khuấy 30 phút; chất keo tụ – /TK6 còn 15 cm, hóa chất tới 20 cm, nước tới 50 cm, khuấy 30 phút."]),
 ("Cụm nước thải sinh hoạt cũ 40-PK-2002", [
  "Bùn hoạt tính sục khí kéo dài, 50 m³/ngày (đỉnh 13 m³/h); đầu vào BOD₅ 220, COD 500 mg/l.",
  "Bể cân bằng /BA1 → /P1A/B → bể oxy hóa /BA2A/B (quạt /K1A/B/C) → bể lắng /BA3A/B → clo hóa /BA5 (NaOCl) → /P4A/B qua lọc /FL1 → /BA7 → /BA8 → ra KCN.",
  "Bùn: ổn định /BA4, tuần hoàn /P2A/B, lên men hiếu khí /BA6A/B, xe bồn /P3A~D."]),
 ("Hệ thống mới 40-PK-2003 (khử nitơ + MBR)", [
  "Công suất ~680 m³/ngày: sinh hoạt 200 + nhiễm dầu đã xử lý 480 m³/ngày (thêm nước CO₂, UFC85 gián đoạn).",
  "TK-100 (31,5 m³, bơm PM-100A/B theo mức 1,5–2,8 m) → sàng rác tinh FS-101 (> 1 mm) → bể điều hòa TK-102 (256 m³, sục khí BL-102A/B) → PM-102A/B vào TK-103, PM-102C/D 50 m³/ngày sang 40-PK-2002.",
  "• Đặt thời gian chạy/dừng bơm PM-102 theo lưu lượng thực, 2 lần khởi động cách nhau ≥ 15 phút (ví dụ chạy 60 / dừng 15 phút).",
  "Bể khử nitơ TK-103 (147 m³, khuấy chìm, thiếu khí) nhận nước điều hòa, nước tuần hoàn giàu nitrat từ TK-104, bùn tuần hoàn từ MBR, H₃PO₄ (dinh dưỡng) và mật rỉ (nguồn cacbon).",
  "Bể đệm TK-104 (sục khí chìm JE-104, nitrat hóa NH₄⁺ → NO₂⁻ → NO₃⁻; PM-104C/D tuần hoàn về TK-103) → bể MBR TK-105 (2 ngăn, 8 module × 200 tấm màng, thổi khí BL-105A/B/C 120–200 m³/h/module; bơm hút PM-105).",
  "MLSS khởi động 5.000–6.000 mg/l; thiết kế MBR 15.000 mg/l; bùn dư → TK-201 (hiện đưa ra sân phơi bùn TK-202A/B thay máy ép BF-202).",
  "Nước ra → bể 40-PK-2002/BA8 → KCN. Shock javel /BA8: hạ mức ~20 %, dừng /P6, thêm 30 l javel 10 % (Cl₂ dư ≥ 1 mg/l), đến 80 % và Cl₂ < 2 mg/l thì bơm ra.",
  "Rửa màng MBR: dừng bơm hút/quạt, ngâm javel 0,5 % ~2 giờ (hữu cơ), rồi axit oxalic 1 % ~1 giờ (vô cơ), chạy lại – áp màng ~−0,1 mbarg. 1 module: 30 l javel 10 % → 600 l; 6 kg axit oxalic → 600 l.",
  "Vi sinh bổ sung 10–20 ml/m³ bể (khởi động 20–40); công thức tính H₃PO₄ và mật rỉ theo TN, BOD, lưu lượng (Phụ lục 1)."]),
],
"GT06": [
 ("Chương I – Lý thuyết trao đổi ion", [
  "Chỉ tiêu nước: pH, độ cứng, độ kiềm; tác hại tạp chất khí (O₂, CO₂) và rắn (muối Ca/Mg, silica) với lò hơi.",
  "Trao đổi cation (R-H giữ Na⁺, Ca²⁺, Mg²⁺ → nước ra có tính axit, CO₂ thoát ở tháp khử khí) và anion (R-OH giữ Cl⁻, SO₄²⁻, HSiO₃⁻ → nước ra kiềm).",
  "Nhựa Amberlite IR120Na (cation), IRA420Cl (anion); dung lượng trao đổi; hóa chất H₂SO₄, NaOH, Na₂SO₃ (khử clo dư bảo vệ nhựa)."]),
 ("Thiết bị chính 30-PK-1001", [
  "Sơ đồ 2B3T + MBP: 3 chuyền × 150 m³/h (cation V1A/B/C → tháp khử CO₂ V2A/B/C + quạt K2 → anion V3A/B/C) và 3 mixed bed V4A/B/C × 200 m³/h.",
  "Bồn định lượng axit TK3/TK4, xút TK5/TK6, pha loãng TK10/TK11, Na₂SO₃ TK7, bể trung hòa BA1 (656 m³) với quạt sục K1A/B, axit TK9 / xút TK8 trung hòa, bình khí nén V5 cho trộn nhựa mixed bed."]),
 ("Nguyên lý và vận hành", [
  "2 chuyền chạy, 1 dự phòng/tái sinh. Nước thô đã khử clo + nước ngưng công nghệ → cation → khử CO₂ → anion → 30-TK-1001 (500 m³) cùng nước ngưng hơi/tuabin.",
  "30-P-1001A/B → mixed bed (2 chạy, 1 tái sinh) → 30-TK-1002 (9.000 m³, đủ 24 giờ) → 30-P-1002A/B cấp đi. Nước ngưng tuabin nhiễm nước sông được đưa về đầu cation/khử khí.",
  "Nước khử khoáng: độ dẫn < 0,2 µS/cm, SiO₂ < 0,02, Na⁺ < 0,02, Cl⁻ < 0,1 ppm, pH 6,5–7, NH₃/Urê ≤ 3 ppm.",
  "Ngừng chuyền: tay (SVC → OFF) hoặc PLC tự dừng khi độ dẫn AI-31202 cao hoặc tổng lưu lượng FIQ-31201 vượt đặt; anion dừng trước, cation chạy đến khi bể khử khí LAH-31205. Mixed bed dừng theo AIT-31203/FIQ-31202."]),
 ("Tái sinh", [
  "Điều kiện: không chuyền khác đang tái sinh, BA1 < 10 % (LT-31232), ≥ 1 chuyền khác đang chạy, bể khử khí ≥ 80 %, bơm khử khí và bơm tái sinh ở Auto; chế độ SEMI-AUTO hoặc MANUAL (nút ADVANCE).",
  "Chuẩn bị hóa chất: 30-P-1003A/B điền axit vào /TK3 đến LS-31206 80 %; /P1A/B điền nước rồi xút vào /TK5.",
  "Cation: rửa ống góp giữa 28 m³/h × 5 phút → phun axit 1,6 % 40 m³/h × 23 phút → axit 4 % 20 m³/h × 12 phút → rửa axit (PLC đặt 30 phút) → rửa cuối 150 m³/h × 5 phút. Phun 2 nồng độ để tránh kết tủa CaSO₄ trên hạt nhựa.",
  "Anion: rửa ống góp 9 m³/h → phun xút 5 % 19,2 m³/h × 30 phút → rửa xút 30 phút → rửa cuối 150 m³/h × 15 phút (dùng nước khử khí/khử khoáng).",
  "Mixed bed: rửa ngược tách lớp → phun xút + axit đồng thời 21,2 m³/h × 15 phút → rửa → xả nước → trộn khí nén 0,4 barg × 10 phút → ép ổn định/điền đầy → rửa cuối 200 m³/h × 10 phút.",
  "Nước thải có hóa chất → BA1 (trung hòa bằng /P7 xút, /P8 axit, sục khí K1) → /P5 ra 30-BA-3001; nước rửa sạch xả thẳng về 30-BA-3001."]),
],
"GT07": [
 ("Chương I – Cơ sở lý thuyết", [
  "Tính chất N₂ (sôi −195,8 °C) và O₂ (sôi −183 °C) – khác nhiệt độ sôi là cơ sở chưng cất không khí lỏng.",
  "Chiller làm lạnh khí nén để ngưng ẩm; làm sạch không khí bằng hấp phụ (alumina, xúc tác CO, rây phân tử 13X); lý thuyết chưng cất."]),
 ("Thiết bị và dòng công nghệ", [
  "V1 bình đệm khí nén (~9,1 barg) → E5/E6 làm lạnh 7–10 °C bằng nước glycol của chiller ACC1 (không dưới 5 °C) → tách nước cyclone WS100 + lọc coalescer FIL1509A/B (< 0,01 mg lỏng/m³).",
  "APU V2/V3 (1 làm việc, 1 tái sinh): 186 kg alumina, 35 kg xúc tác khử CO, 611 kg rây phân tử 13X; chuyển bình theo 7.148 m³ hoặc 680 phút; bước: hấp phụ – xả áp – gia nhiệt (đến TT-36216 = 100 °C) – làm nguội – tăng áp – song song.",
  "Coldbox (cách nhiệt perlite, purge N₂): E3 làm lạnh khí vào bằng N₂ sản phẩm và khí thải → cột T1; N₂ ở đỉnh ngưng ở E4, 55–65 % hồi lưu; lỏng giàu O₂ ở đáy sang V4 rồi bay hơi làm lạnh E4.",
  "Độ tinh khiết điều khiển gián tiếp qua FV-36223 (tỷ lệ N₂/Air = tỷ lệ thu hồi đặt trước). V4 xả lỏng (~60 % O₂) 1 lần/giờ qua XYS-36249 để tránh tích tụ hydrocacbon.",
  "Khí thải về APU tái sinh hoặc vent qua PV-36221 (không vượt 0,5 barg). Sản phẩm điều khiển áp bằng FV-36227 (PT-36229); thiếu thì bồn N₂ lỏng hóa hơi bù, thừa thì PV-36229 vent.",
  "Turbine giãn nở hướng tâm, ổ đỡ khí (IA qua PCV-36753); có gia nhiệt khí vào khi < 140 K để tránh đóng băng; N₂ lỏng về bồn TK1 qua LV-36226.",
  "Sản phẩm: 7 barg, 10–20 °C, 99,9 % N₂, O₂ ≤ 0,1 %."]),
 ("Khởi động và các chế độ", [
  "Kiểm tra van theo Phụ lục 1 → Plant On ở Mode 0, chạy hết 1 chu kỳ tái sinh 2 bình APU.",
  "Thổi coldbox bằng khí 300 K (HV-36231 vào, HV-36230 xả) đến khi ẩm < 5 ppm.",
  "Mode 1: purge turbine tự động 260 phút (XV-36282/84); nếu APU đang Heating/Cooling thì tăng Min Output PV-36219 từ 16 lên 19 % để tránh trip áp thấp.",
  "Làm lạnh: XV-36224 mở, PV-36230 giữ áp cột; ~7,6 barg turbine CLEAR, ZV-36298 mở 55 %; có thể làm lạnh nhanh bằng lỏng từ TK1 (XV-36252, XV-36288/91). TT-36225 ~−160 °C thì có lỏng.",
  "AIT-36245 < 5 ppm O₂ thì XV-36245 mở cấp sản phẩm, LV-36226 đưa lỏng về bồn; > 5 ppm thì đóng LV-36226.",
  "Mode 5 (Economiser): dùng lỏng từ bồn thay turbine. Thổi coldbox ở Mode 0 sau ngừng: thổi 6 giờ, ẩm < 5 ppm."]),
 ("HMI và phụ lục", [
  "Hướng dẫn thao tác trên HMI: alarm, đăng nhập, trang vận hành/công nghệ, vòng PID, van, turbine, nhiệt độ xả condenser, APU, tín hiệu ngừng khẩn cấp, emergency stop relay, trend, trang hệ thống.",
  "Phụ lục: vị trí van trước khởi động, khóa liên động, hoạt động APU, lưu ý hệ điều khiển, giá trị cài đặt HMI và các bộ điều khiển, datasheet thiết bị."]),
],
"GT08": [
 ("Phần I – Lý thuyết tuabin khí", [
  "Chu trình Brayton hở đơn giản: nén đoạn nhiệt – cấp nhiệt đẳng áp – giãn nở – thải nhiệt; hiệu suất tăng theo tỷ số nén; chu trình có trao đổi nhiệt và chu trình hỗn hợp (kết hợp HRSG).",
  "Nhiệt độ/áp suất môi trường ảnh hưởng công suất (không khí nóng → khối lượng riêng giảm → công suất giảm).",
  "Cấu tạo chung: máy nén dọc trục, buồng đốt, tuabin."]),
 ("Tuabin khí MS-5001 (Phần II)", [
  "Một trục, chu trình hở, 10 buồng đốt dòng ngược; đặt trên một bệ, dưới khoang phụ trợ là thùng dầu bôi trơn.",
  "Đường đi khí: lọc → máy nén dọc trục (IGV, van trích tầng 10, van IBH) → buồng đốt DLN (liner, transition piece) → tuabin 2 cấp → bộ khuếch tán có cánh dẫn → ống khói/HRSG.",
  "Khởi động: van trích mở, IGV 41°; 1.120 rpm (22 %) đánh lửa, lửa lan qua cross-fire, đầu dò lửa xác nhận; 101 % (5.100 rpm) đóng van trích, IGV 46°.",
  "Buồng đốt DLN: các chế độ đốt, dò lửa, đánh lửa; tuabin: stator, rotor, ổ đỡ, khớp nối; hệ không khí vào (lọc coalescer SP20, M80, DuraVee) và khí thải."]),
 ("Hệ thống phụ trợ 10-GT-9001", [
  "Dẫn động phụ (accessory gear): bơm dầu chính, bơm thủy lực…",
  "Khởi động: động cơ diesel → torque converter → hydraulic ratchet → khớp jaw/SSS.",
  "Dầu bôi trơn: bơm chính trên accessory gear, bơm phụ P2 (AC), bơm khẩn P3 (DC); lọc kép FL1/2; van điều áp; bảo vệ nhiệt độ/áp; oil mist eliminator.",
  "Khí nhiên liệu: van stop/ratio SRV (10-FV-9205) và gas control GCV (10-FV-9207), lọc khí, bảo vệ, hệ DLN.",
  "Dầu thủy lực (điều khiển IGV), dầu điều khiển và cơ cấu trip quá tốc; khí làm mát và làm kín (trích tầng 4 và tầng 10).",
  "Lưu ý vận hành: nhiệm vụ người vận hành, giá trị cảnh báo/trip nhiệt độ tầng cánh."]),
 ("Điều khiển Mark VI", [
  "Trình tự khởi động: bơm dầu phụ P2 → tách khí dầu F8 → quạt thông gió F6/F7, F10–F13 → quạt làm mát dầu F1–F3 → Master protective L4 → làm mát diesel F9.",
  "Diesel warm-up 1.000–1.100 v/ph × 5 phút → 1.800–1.900 v/ph quay tuabin, purge 3 phút → 2.100 v/ph mở van nhiên liệu → 3.500 v/ph diesel tách, cooldown 5 phút.",
  "95 % tốc độ và áp dầu PIT-9218 đủ 1,7 barg thì dừng P2; 100 % \"Ready to sync\"; chọn hòa đồng bộ (43SEL) tại IB2/BT/IB1, Auto hoặc Manual; đóng IB2 rồi tăng tải tới spinning reserve.",
  "Dừng khẩn cấp: L4 mất → đóng van nhiên liệu, chạy P2 (hoặc P3 nếu mất AC, PSL-9202), mở máy cắt IB2, cắt kích từ; tốc độ 0 thì làm mát (cooldown) 24 giờ.",
  "Điều khiển thiết bị phụ, phòng cháy, dò khí; vòng điều khiển khởi động, tốc độ – tải, nhiệt độ, khí nhiên liệu.",
  "Bảng sự cố thường gặp và bảng cảnh báo (nguyên nhân, cách xử lý)."]),
],
"GT09": [
 ("Hệ thống đuốc", [
  "Hai đuốc riêng: khí tổng hợp 40-PK-1002 (349.674 kg/h; TH1 gas break-through 10-T-3002, TH2 tắc đầu ra reforming) và NH₃ 40-PK-1001 (298.190 kg/h; từ máy nén 10-K-4031/4041/4051, bồn NH₃, 40-PK-5001, 40-T-2001). Dòng CO/CO₂ tách khỏi NH₃ để không tạo carbamate.",
  "Khí tổng hợp gom header 36\" → KO drum 40-V-1001 → đuốc; NH₃: header 40\" từ X.Amo và đường 10\" từ bồn 40-TK-5001 (đuốc nhỏ/đuốc lớn).",
  "Khí nhiên liệu bổ sung ở đỉnh đuốc NH₃ (FO-41501, HV-41002, HIC-41002 / FIC-41001A); purge liên tục giữ áp dương; 3 đầu đốt mồi có dò lửa, tủ đánh lửa đặt ngoài vùng bức xạ.",
  "Cao 45 m: bức xạ ≤ 3.000 Btu/h·ft² ở công trình, ≤ 1.450 Btu/h·ft² trong bán kính 60 m. Giới hạn cháy khí đuốc 4,0–72,5 % thể tích.",
  "Vận hành: chuẩn bị (lắp đặt, thổi sạch, thử van, thiết bị đo, POWER ON), đánh lửa, xả nước ngưng KO drum/đoạn ống trũng."]),
 ("Bồn chứa NH₃ 40-TK-5001", [
  "Bồn kép 2 vách, 35.000/29.500 m³, 20.000 tấn, −33 °C, 0,04–0,10 barg (thiết kế 0,15/−0,005 barg); bay hơi cho phép 0,04 %/ngày; nạp tối đa 82,7 m³/h, tháo 170 m³/h. NH₃ ≥ 99,8 %, H₂O ≤ 0,2 %.",
  "IS-45001 (2/3): mức 94 % đóng LV-45001; 2 % dừng bơm NH₃; áp đẩy 15,3 barg dừng 40-P-5001B/5002/5003.",
  "IS-45002 (2/3 PIT-45001): 130 mbarg mở hoàn toàn PV-45005 (ra đuốc); 10 mbarg đóng HV-45002, dừng máy nén 40-PK-5001/5005 và bơm; 5 mbarg mở PV-45001 cấp N₂ giữ áp.",
  "Tác động NH₃: 5 ppm có mùi nhẹ, 20–50 ppm có mùi, 150–200 ppm khó chịu – chảy nước mắt; nồng độ cao gây nguy hiểm tính mạng."]),
 ("Cụm làm lạnh 40-PK-5001 và thu hồi hơi sang X.Amo", [
  "40-PK-5001: 600 kg/h, 2 máy nén trục vít K1A/B (180 kW), bơm dầu P1A/B, tách dầu V3, làm mát dầu E2.",
  "Khởi động: mở van hơi từ bồn và PV-45004; ACK/RESET; chọn trình tự bơm dầu (HS-45720), Start bơm dầu – sau 10 s không đủ áp thì hủy; chọn máy nén (HS-45712), Man/Auto Start; máy nén chỉ chạy khi slide valve ZI-45701 = 0 %.",
  "Đưa hơi sang máy nén 10-K-4051 X.Amo khi áp bồn ≥ 70 mbarg (mở TH-PT1 / TH-NH3_1; 10-PIC-5022 đặt 10 mbarg nhánh surge, 30 mbarg nhánh load); giữ áp bồn 50–100 mbarg, PV-45005 không mở.",
  "Áp bồn xuống 100 mbarg dừng 40-PK-5001 về dự phòng; xuống 60 mbarg nâng setpoint 10-PIC-5022 lên 20/40 mbarg; lên 115 mbarg (PV-45005 mở) chạy lại 40-PK-5001; xuống 50 mbarg hoặc 10-K-4051 dừng thì ngừng đưa hơi, chạy lại 40-PK-5001."]),
 ("Bơm NH₃ và cụm 40-PK-5005", [
  "Bơm 40-P-5001A/B cấp NH₃ lỏng cho X.Urê/Amo/NPK; 40-P-5002/5003 nạp xe bồn qua bộ gia nhiệt 40-E-5001/5002 (20.000 kg/h, 933 kW). Mỗi bơm 85 m³/h, 368 m.",
  "40-PK-5005 (250 kg/h, lắp khi revamp): sub-cooler V1, máy nén trục vít K1A/B, tách dầu V3, ngưng E1, bình chứa V2, chưng dầu V4, xả khí trơ; HMI, quá tải, logic, dầu bôi trơn, xả dầu V4, khởi động/ngừng, pump-out V5."]),
],
}
