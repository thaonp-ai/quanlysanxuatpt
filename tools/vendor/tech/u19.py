"""Công nghệ Unit 19A – Tuabin khí phát điện 10-GT-9001 (Nuovo Pignone MS5001PA DLN, job 170.5540).

Nguồn: PFD 2098-19-PFD-0010-01 (phát điện), P&ID 2098-19-PID-0031-01 as-built, bộ sách Nuovo Pignone
Vol I "Gas Turbine Description & Operation" và Vol II "Maintenance" (bản scan → OCR; các mục đã tách ở
"10GT9001/Tach theo muc"), mục lục thiết bị phụ Vol IV (Aux_index.doc).
"""
import json, os

R = "10GT9001/"
_S = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gt", "sections.json")))


def sec(vol, no):
    """[đường dẫn file tách, nhãn] của mục `no` trong Vol I / Vol II."""
    for book, v in _S.items():
        if v["tag"] == vol:
            for n, p0, t in v["s"]:
                if n == no:
                    return [R + "Tach theo muc/" + f"{vol} - {n:02d} {t}.pdf".replace("/", "-"), f"{vol} mục {n} – {t}"]
    raise KeyError((vol, no))


def sh(dwg, label):
    return ["sheet:" + dwg, label]


def ent(t, intro, s=None, src=None):
    return {"t": t, "intro": intro, "s": s or [], "src": src or []}


PFD = sh("2098-19-PFD-0010-01-1-0", "PFD 2098-19 Hệ thống phát điện")
PID = sh("2098-19-PID-0031-01", "P&ID 19-01 Tuabin khí 10-GT-9001")
S_AUX = [R + "Them/Vol. IV Auxialiary Equipment/Aux_index.doc", "Vol IV – bảng thiết bị phụ & tag"]

UNIT = {
    "t": "Công nghệ Unit 19A – Tuabin khí phát điện 10-GT-9001",
    "intro": "Tuabin khí 10-GT-9001 là tổ máy Nuovo Pignone (GE) MS5001PA một trục, chu trình đơn, buồng đốt DLN (Dry Low NOx), kéo máy phát đồng bộ Brush. "
             "Công suất điện ở 100 % tải là 21,2 MW (ghi chú PFD 2098-19). Nhiên liệu là khí cao áp từ bình 30-V-7001. "
             "Khói thải nóng đi sang lò hơi thu hồi nhiệt HRSG 10-B-9001 (Unit 19B) để sinh hơi cao áp, hoặc xả ra ống khói qua van chuyển hướng.",
    "s": [
        {"h": "Sơ đồ dòng (PFD 2098-19)",
         "ul": ["Khí nhiên liệu cao áp (HP fuel gas) từ bình 30-V-7001 (DWG 37-01) vào tuabin ở 24 barg, 30 °C. "
                "Lưu lượng 4.800 / 4.850 / 5.600 kg/h ứng với case 1 / 2 / 3. Lưu lượng được đo qua FE/FIT-9001, có bù nhiệt độ và áp suất.",
                "Khói thải tuabin vào HRSG 10-B-9001. Van chuyển hướng (điều khiển bằng HIC) cho phép xả khói thẳng ra ống khói khi HRSG không làm việc.",
                "HRSG có đốt bổ sung bằng khí nhiên liệu thấp áp (LP fuel gas từ 30-V-7002, 6 barg, bình thường không dùng). "
                "HRSG nhận nước cấp từ bơm 10-P-8002A/B (44.440 kg/h, 132 °C, 56 barg) và sinh hơi HPS 44.000 kg/h ở 38 barg, 370 °C về header (DWG 18-01).",
                "Máy được rửa máy nén bằng cụm rửa online/offline (turbine washing facilities)."],
         "src": [PFD, PID]},
        {"h": "Cấu tạo chính",
         "ul": ["Đường khí: cửa hút có lọc và tiêu âm → máy nén dọc trục → 10 buồng đốt ngược dòng (DLN) xếp quanh thân xả máy nén "
                "→ ống chuyển tiếp → tuabin 2 tầng → ống xả có cánh hướng dòng → plenum xả.",
                "Máy nén và tuabin nối cứng thành một rotor, đỡ trên 2 ổ đỡ chính có ổ chặn, bôi trơn bằng dầu áp lực. "
                "Đầu vào trục nối với hộp số phụ (accessory gear) dẫn động bơm dầu chính và bơm thủy lực; đầu ra nối hộp số tải sang máy phát qua khớp nối màng.",
                "Cánh hướng dòng đầu vào điều chỉnh được (IGV) và van xả khí tầng 10 chống surge khi khởi động và dừng máy.",
                "Làm mát tuabin và làm kín ổ đỡ bằng khí trích tầng 4, tầng 10 và khí xả máy nén."],
         "src": [sec("Vol I", 1), sec("Vol I", 2), sec("Vol I", 3), sec("Vol I", 5), sec("Vol I", 13)]},
        {"h": "Các chế độ đốt DLN",
         "tb": [["Chế độ", "Dải tải (theo sách)", "Nhiên liệu vào"],
                ["Primary", "Khởi động, tăng tốc, tới ≈20 % tải", "Chỉ 5 vòi sơ cấp, lửa ở vùng sơ cấp"],
                ["Lean-lean", "≈20–40 % tải", "Cả hai tầng (≈30 % vào vòi thứ cấp), lửa ở cả hai vùng"],
                ["Secondary transfer", "≈40 % tải (thoáng qua)", "Chỉ vòi thứ cấp; lửa vùng sơ cấp tắt"],
                ["Premix", "≈40–100 % tải", "≈80–83 % qua vòi sơ cấp để trộn trước, lửa chỉ ở vùng thứ cấp → NOx thấp"]],
         "p": ["Tỉ lệ chia nhiên liệu sơ cấp/thứ cấp do van chia VGS-3 thực hiện, theo nhiệt độ tham chiếu buồng đốt. "
               "Ống Venturi ngăn lửa quay ngược vào vùng trộn trước. "
               "Có 4 đầu dò lửa cho vùng sơ cấp và 4 cho vùng thứ cấp. 2 bugi đánh lửa kiểu cố định (không rút ra), vì cần đánh lửa lại cả khi đang mang tải."],
         "src": [sec("Vol I", 4), sec("Vol I", 10)]},
        {"h": "Khởi động",
         "ul": ["Theo sách Vol I, tuabin được quay bằng động cơ diesel qua bộ biến mô thủy lực (Voith), cơ cấu ratchet thủy lực và ly hợp vấu nối vào hộp số phụ. "
                "Ghi chú 2 của PFD lại ghi khởi động bằng motor điện lấy nguồn sự cố. Cần đối chiếu với hiện trạng.",
                "Ratchet giúp phá trạng thái đứng yên của rotor (breakaway): mỗi hành trình 10 giây xoay ly hợp ≈47°. "
                "Khi làm nguội sau dừng máy, ratchet tự chạy mỗi 3 phút một chu kỳ.",
                "Trình tự: quay máy → đạt tốc độ đánh lửa → đốt (primary) → khởi động ấm → tăng tốc. "
                "Ở ≈95 % tốc độ, van xả tầng 10 đóng và IGV mở về vị trí làm việc. Ở ≈3.100–3.200 v/ph, ly hợp tự nhả và diesel về chạy không tải rồi dừng.",
                "Không được đóng ly hợp vấu khi trục trượt đang quay. Trước khi vô hiệu hóa thiết bị nào của hệ khởi động, phải nhả và khóa ly hợp bằng van nhả ly hợp."],
         "src": [sec("Vol I", 8), PFD]},
        {"h": "Hệ thống dầu",
         "ul": ["Dầu bôi trơn: bồn ≈8.160 L trong bệ tuabin. Áp đầu ổ đỡ 1,7 barg do van VPR-2 điều chỉnh; lọc 5 µm; tuabin trip ở 0,96 barg. "
                "Có 3 bơm: bơm chính dẫn động từ hộp số phụ; bơm phụ motor AC 88QA (10-GT-9001/P-2), chạy khi khởi động/dừng máy tới ≈95 % tốc độ; "
                "bơm sự cố motor DC 88QE (P-3). Dầu được làm mát ở bộ làm mát dầu bằng không khí 10-GT-9001/E-1 (NP tag HXL-2).",
                "Độ nhớt dầu khi khởi động ≤ 800 SUS. Nhiệt độ dầu vào ổ đỡ danh định ≈130 °F (≈54 °C).",
                "Dầu thủy lực: bơm piston lưu lượng thay đổi trên hộp số phụ, lấy dầu từ header ổ đỡ, có bộ bù áp VPR-3 và van an toàn VR-21. "
                "Dầu được lọc 3 µm qua 2 lọc FH2-1/2 (chuyển đổi khi đang chạy; thay lõi khi chênh áp báo 5 bar). "
                "Dầu này dùng để điều khiển van khí nhiên liệu SRV/GCV và IGV (90TV, VC-1).",
                "Dầu trip: dầu ổ đỡ qua lỗ tiết lưu tạo dầu áp thấp OL. Van điện từ 20FG và thiết bị vượt tốc 12HA-1 xả dầu OL để đóng van chặn nhiên liệu."],
         "src": [sec("Vol I", 9), sec("Vol I", 11), sec("Vol I", 12), S_AUX]},
        {"h": "Hệ thống khí nhiên liệu",
         "ul": ["Lọc khí → van chặn/tỉ lệ (SRV) và van điều khiển (GCV) chung một thân → ống góp tới vòi đốt.",
                "SRV giữ áp trung gian giữa hai van theo tốc độ tuabin (transmitter 96FG-2A/B/C) và đóng ngắt nhiên liệu khi dừng hoặc trip. "
                "GCV định lượng nhiên liệu theo tín hiệu FSR của Speedtronic.",
                "Van trip VH5 xả dầu thủy lực của SRV khi áp dầu trip giảm. Van xả 20VG-1 xả khí tích trong khoang giữa hai van khi dừng máy."],
         "src": [sec("Vol I", 10)]},
        {"h": "Giới hạn vận hành (theo sách)",
         "ul": ["Độ chênh nhiệt độ khói thải (spread) dự kiến 45 ± 35 °F. Cần xử lý khi spread > 80 °F hoặc thay đổi > 35 °F so với số liệu gốc. Phải ghi số liệu gốc sau mỗi lần khởi động đầu, trước/sau dừng máy và trước/sau bảo dưỡng.",
                "Nhiệt độ khoang bánh tuabin (wheelspace): báo động 427 °C, mức tối đa 457 °C. Vượt mức chỉ báo động, không trip, nhưng phải báo nhà sản xuất.",
                "Rung: xử lý khi vận tốc rung > 0,5 in/s (12,7 mm/s); không được vượt 1,0 in/s (25,4 mm/s).",
                "Theo dõi nhiệt độ khói thải trong suốt quá trình khởi động. Trip máy nếu vượt mức trip hoặc tăng nhanh bất thường.",
                "Khi dừng lâu: chạy có tải ít nhất 1 giờ mỗi 2 tháng, chạy ratchet hằng tuần để tuần hoàn dầu, tránh gỉ cổ trục."],
         "src": [sec("Vol I", 14), sec("Vol II", 1)]},
        {"h": "Chu kỳ bảo dưỡng tiêu chuẩn (khí thiên nhiên, khởi động/dừng bình thường)",
         "tb": [["Loại kiểm tra", "Giờ đốt", "Số lần khởi động"],
                ["Kiểm tra buồng đốt (Combustion inspection)", "8.000", "400"],
                ["Kiểm tra đường khí nóng (HGP)", "24.000", "1.200"],
                ["Đại tu (Major inspection)", "48.000", "2.400"],
                ["Nội soi borescope", "Hằng năm hoặc khi kiểm tra buồng đốt", ""]],
         "p": ["Mỗi lần kiểm tra theo mốc giờ đốt hoặc số lần khởi động, mốc nào tới trước. "
               "Mốc được chia cho hệ số bảo dưỡng: nhiên liệu lỏng, trip khi đang mang tải (trip ở 100 % tải ≈ 8 lần khởi động), thay đổi tải đột ngột… "
               "Ví dụ trong sách: 6.000 giờ khí + 1.000 giờ dầu/năm, 100 lần khởi động và 10 lần trip/năm → đại tu sau ≈44.800 giờ (≈6,4 năm)."],
         "src": [sec("Vol II", 3), sec("Vol II", 1)]},
    ],
    "src": [sec("Vol I", 1), sec("Vol II", 3), PFD, PID],
}

TAGS = {
    "10-GT-9001": ent("Tuabin khí 10-GT-9001",
                      "Tổ máy phát điện tuabin khí Nuovo Pignone MS5001PA (một trục, buồng đốt DLN 10 buồng), job 170.5540, kéo máy phát Brush. "
                      "Công suất 21,2 MW ở 100 % tải. Khí nhiên liệu cao áp 24 barg từ bình 30-V-7001. Khói thải sang HRSG 10-B-9001. "
                      "Hệ điều khiển Speedtronic Mark VI TMR, HMI riêng, giám sát rung/nhiệt Bently Nevada 3500, hệ phát hiện cháy khí riêng (F&G GT9001). "
                      "Trên P&ID 2098-19-PID-0031-01, cụm tuabin được vẽ dạng hộp đen, chỉ có các đường tiện ích: "
                      "nước khử khoáng rửa máy nén (cụm rửa online/offline), khí điều khiển, nước làm mát sạch, khí nhiên liệu, dầu sang bộ làm mát E-1 (HXL-2). "
                      "Chi tiết bên trong xem P&ID của nhà cung cấp (SOM 09996/1, \"PID GT9001.pdf\").",
                      [{"h": "Chu kỳ bảo dưỡng tiêu chuẩn",
                        "tb": [["Kiểm tra", "Giờ đốt", "Khởi động"], ["Buồng đốt", "8.000", "400"], ["Đường khí nóng", "24.000", "1.200"], ["Đại tu", "48.000", "2.400"]]}],
                      [PFD, PID, sec("Vol I", 1), sec("Vol II", 3), [R + "PID GT9001.pdf", "P&ID cụm tuabin của nhà cung cấp"]]),
    "10-GT-9001/E-1": ent("Bộ làm mát dầu 10-GT-9001/E-1 (HXL-2)",
                            "Bộ làm mát dầu bôi trơn bằng không khí (airfin) của tuabin khí, Astra, 680 kW: dầu 78 → 55 °C, áp thiết kế 12 bar, 3 quạt F-1/2/3 với motor MF-1/2/3 (Siemens 11 kW, 1.440 v/ph). "
                            "Van 3 ngã nhiệt TCV-9700 (VTR-1) chia dòng qua/bypass bộ làm mát. Trên P&ID 2098-19-PID-0031-01 ghi theo NP tag HXL-2. "
                            "Dầu từ bồn trong bệ tuabin qua các đường 8\"-LO-1901001/1901003 sang HXL-2 và trở về, rồi qua lọc 5 µm vào header ổ đỡ (1,7 barg). "
                            "Theo sách, nhiệt độ dầu vào ổ đỡ danh định ≈54 °C; với hệ làm mát bằng không khí, ở nhiệt độ môi trường cao nhất có thể tới ≈71 °C. "
                            "Tài liệu nhà cung cấp ở Vol IV mục 5 (Oil aircooler).",
                            src=[PID, sh("SOM09996/1 tờ 7", "P&ID nhà cung cấp tờ 7 – Bộ làm mát dầu"), sec("Vol I", 9), S_AUX]),
}
