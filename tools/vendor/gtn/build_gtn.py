#!/usr/bin/env python3
"""Danh mục "Vendor Data/Giáo trình_New" (giáo trình đào tạo vận hành các hệ thống X.Phụ trợ) -> docs.json + sizes.json.

Mỗi giáo trình gắn vào tag gốc của hệ thống (web tự hiện cho thiết bị con). Bỏ file ~$ (khóa Word).
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
R = "Giáo trình_New"
G = "Tài liệu tham khảo"
NLM = ["30-CT-3001", "30-P-3001", "30-P-3002", "30-E-3001", "30-PK-3006", "30-V-3001"]
WW = ["40-PK-2001", "40-PK-2002", "40-PK-2003"]
RPF = ["30-P-2001", "30-P-2002", "30-PK-2001", "30-P-4001", "30-P-4002"]
NH3 = ["40-TK-5001", "40-PK-5001", "40-PK-5005", "40-PK-1001", "40-PK-1002"]
L = [
    ("GT Nuoc lam mat_Rev01.docx", 2047056, "Giáo trình vận hành nước làm mát & nước NHR (Rev01, Word)", NLM),
    ("STVB102393_G2-30-GT-02 GT dao tao HT nuoc lam mat - nuoc NHR_vps.pdf", 3467506, "Giáo trình G2-30-GT-02 – hệ thống nước làm mát & nước NHR", NLM),
    ("GT He thong xu ly nuoc thai_Rev01.docx", 1208213, "Giáo trình vận hành hệ thống xử lý nước thải (Rev01, Word)", WW),
    ("STVB102393_G2-30-GT-05 GT dao tao HT xu ly nuoc thai_vps.pdf", 2378848, "Giáo trình G2-30-GT-05 – hệ thống xử lý nước thải", WW),
    ("GT Nuoc tho-Sinh hoat-Cuu hoa_Rev01.docx", 1989388, "Giáo trình nước thô – sinh hoạt – cứu hỏa (Rev01, Word)", RPF),
    ("STVB102393_G2-30-GT-01 GT dao tao HT nuoc tho-sinh hoat-cuu hoa_vps.pdf", 2406119, "Giáo trình G2-30-GT-01 – nước thô, sinh hoạt, cứu hỏa", RPF),
    ("GT Lo hoi phu tro 10-B-8001_Rev01.docx", 2847482, "Giáo trình lò hơi phụ trợ 10-B-8001 (Rev01, Word)", ["10-B-8001"]),
    ("STVB102393_G2-30-GT-03 GT dao tao HT nuoc cap-lo hoi phu tro va khi nhien lieu_vps.pdf", 3479573, "Giáo trình G2-30-GT-03 – nước cấp, lò hơi phụ trợ & khí nhiên liệu", ["10-B-8001"]),
    ("GT Khi nen-Khi dieu khien_Rev01.docx", 4517670, "Giáo trình khí nén – khí điều khiển (Rev01, Word)", ["30-K-5001", "30-DR-5001", "30-DR-5002"]),
    ("STVB102393_G2-30-GT-04 GT dao tao HT khi nen-khi dieu khien_vps.pdf", 3182772, "Giáo trình G2-30-GT-04 – khí nén, khí điều khiển", ["30-K-5001", "30-DR-5001", "30-DR-5002"]),
    ("GT He thong san xuat nuoc khu khoang_Rev01.docx", 198195, "Giáo trình hệ thống sản xuất nước khử khoáng (Rev01, Word)", ["30-PK-1001"]),
    ("STVB102393_G2-30-GT-06 GT dao tao HT san xuat nuoc khu khoang_vps.pdf", 1883808, "Giáo trình G2-30-GT-06 – sản xuất nước khử khoáng", ["30-PK-1001"]),
    ("GT He thong san xuat Nito_Rev01.docx", 1369635, "Giáo trình hệ thống sản xuất nitơ (Rev01, Word)", ["30-PK-6001"]),
    ("STVB102393_G2-30-GT-07 GT dao tao HT san xuat Nito_vps.pdf", 2999921, "Giáo trình G2-30-GT-07 – sản xuất nitơ", ["30-PK-6001"]),
    ("GT Gasturbine_Rev01.docx", 12658224, "Giáo trình tuabin khí (Rev01, Word)", ["10-GT-9001"]),
    ("STVB102393_G2-30-GT-08 GT dao tao HT Gasturbine_vps.pdf", 5785989, "Giáo trình G2-30-GT-08 – tuabin khí", ["10-GT-9001"]),
    ("GT Bon chua NH3 & duoc thai_Rev01.docx", 299311, "Giáo trình bồn chứa NH3 & đuốc (Rev01, Word)", NH3),
    ("STVB102393_G2-30-GT-09 GT dao tao HT bon chua NH3 & flare_vps.pdf", 1646952, "Giáo trình G2-30-GT-09 – bồn chứa NH3 & đuốc", NH3),
]
docs = [{"p": R + "/" + p, "t": t, "g": G, "tags": tags, "no": "", "src": "Giáo trình đào tạo X.Phụ trợ", "kb": 0} for p, _, t, tags in L]
json.dump(docs, open(os.path.join(HERE, "docs.json"), "w"), ensure_ascii=False, indent=0)
json.dump([[R + "/" + p, s] for p, s, _, _ in L], open(os.path.join(HERE, "sizes.json"), "w"), ensure_ascii=False)
print(len(docs), "giáo trình")
