#!/usr/bin/env python3
"""Tách các sách gộp (Part 1C/1D/1E) thành từng file theo mục, để bấm vào là mở đúng trang đầu của mục.

Đọc tools/vendor/sections.json, cắt PDF bằng qpdf từ bản sao thư mục "Vendor Data",
ghi file vào <thư mục ra>/Lo hoi phu tro/Tach theo muc/ và ghi tools/vendor/sections_split.json:
  {"<sách>|<mã mục>": {"p": đường dẫn tương đối, "from": trang đầu, "to": trang cuối, "pages": số trang, "kb": ...}}
Các file này được chép vào OneDrive: Vendor Data\\Lo hoi phu tro\\Tach theo muc\\ (sách gốc giữ nguyên).
Mục lớn đã chia mục con (22, 23, 25 …) chỉ tách các mục con để khỏi trùng dung lượng.
Chạy: python3 split_sections.py <thư mục chứa "Lo hoi phu tro"> <thư mục ra>
"""
import json, os, re, subprocess, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = sys.argv[1], sys.argv[2]
S = json.load(open(os.path.join(HERE, "sections.json")))
SUBDIR = "Lo hoi phu tro/Tach theo muc"
os.makedirs(os.path.join(OUT, SUBDIR), exist_ok=True)
D1 = "Lo hoi phu tro/PART 1D/Vendor Data Book Part 1D_Part1.pdf"
D2 = "Lo hoi phu tro/PART 1D/Vendor Data Book Part 1D_Part2.pdf"


def npages(p):
    out = subprocess.run(["pdfinfo", os.path.join(SRC, p)], capture_output=True, text=True).stdout
    return int(re.search(r"Pages:\s+(\d+)", out).group(1))


def num(no):
    m = re.search(r"(\d+(?:\.\d+)?)", no)
    return tuple(int(x) for x in m.group(1).split(".")) if m else None


def safe(s):
    s = s.replace("đ", "d").replace("Đ", "D").replace("–", "-").replace("…", "-").replace(";", ",").replace("&", "and")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r'[\\/:*?"<>|]+', " ", s)
    return re.sub(r"\s+", " ", s).strip()[:90]


res = {}
for book, secs in S.items():
    n = npages(book)
    tag = "1D" if "Part 1D" in book else ("1C" if "Part 1C" in book else "1E")
    nums = [num(x[0]) for x in secs] if tag == "1D" else []
    for i, (no, title, pg, subs, g) in enumerate(secs):
        k = num(no) if tag == "1D" else None
        if k and len(k) == 1 and any(x and len(x) == 2 and x[0] == k[0] for x in nums):
            continue
        end = n
        for no2, _, pg2, _, _ in secs[i + 1:]:
            end = pg2 - 1
            break
        end = max(end, pg)
        ranges = [(book, pg, end)]
        if book == D1 and i == len(secs) - 1 and S.get(D2):  # mục cuối phần 1 nối sang đầu phần 2
            ranges.append((D2, 1, S[D2][0][2] - 1))
        label = re.sub(r"^1E\s*", "", no.replace("§", "").strip()) or "muc luc"
        name = safe(f"{tag} {label} - {re.sub(r'^Mục [0-9.]+ – ', '', title)}") + ".pdf"
        rel = SUBDIR + "/" + name
        dst = os.path.join(OUT, rel)
        if not os.path.exists(dst):
            args = ["qpdf", "--empty", "--pages"]
            for b, a, z in ranges:
                args += [os.path.join(SRC, b), f"{a}-{z}"]
            r = subprocess.run(args + ["--", dst], capture_output=True, text=True)
            if r.returncode not in (0, 3):
                raise SystemExit(r.stderr)
        res[book + "|" + no] = {"p": rel, "from": pg, "to": end, "pages": sum(z - a + 1 for _, a, z in ranges),
                                "kb": round(os.path.getsize(dst) / 1024)}

json.dump(res, open(os.path.join(HERE, "sections_split.json"), "w"), ensure_ascii=False, indent=1)
print(len(res), "file,", sum(v["kb"] for v in res.values()) // 1024, "MB")
