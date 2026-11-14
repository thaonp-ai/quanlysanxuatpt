#!/usr/bin/env python3
"""Tách giáo trình GT-01…09 theo mục lục để mở trực tiếp trên OneDrive (OneDrive không mở PDF tới trang cụ thể).
Mỗi trang bắt đầu của một mục lục (gộp các mục cùng trang) → 1 file gồm trang đó tới trước trang bắt đầu kế tiếp.
Ghi gtcv_split.json {GT: [[trang đầu, trang cuối, tên file]]}; file đặt ở OneDrive
"Vendor Data/Giáo trình tham khảo các cương vị/Tach theo muc/GT-0x/".
Dùng: python3 gtcv_split.py <thư mục Giáo trình tham khảo các cương vị> <thư mục ra>   (cần qpdf)
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
auto = json.load(open(os.path.join(HERE, "gtcv_auto.json")))


def clean(t):
    import unicodedata  # tên file không dấu để giải nén zip trên Windows không lỗi font
    t = t.replace("Đ", "D").replace("đ", "d")
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    t = re.sub(r'[\\/:*?"<>|]', "-", t)
    t = re.sub(r"\s+", " ", t).strip(" .-")
    return t[:70].rstrip(" .-")


def plan(npages):
    out = {}
    for k, e in auto.items():
        starts = {}
        for lv, t, p in e["toc"]:
            if p and p not in starts:
                starts[p] = t
        ps = sorted(starts)
        rows = []
        for i, p in enumerate(ps):
            end = (ps[i + 1] - 1) if i + 1 < len(ps) else npages[k]
            end = max(end, p)
            rows.append([p, end, "%s tr.%03d-%03d %s.pdf" % (k.replace("GT", "GT-"), p, end, clean(starts[p]))])
        out[k] = rows
    return out


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    files = {re.search(r"GT-0\d", f).group().replace("-", ""): os.path.join(src, f) for f in os.listdir(src) if re.search(r"G2-30-GT-0\d.*\.pdf$", f)}
    npages = {k: int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", f], capture_output=True, text=True).stdout).group(1)) for k, f in files.items()}
    pl = plan(npages)
    for k, rows in pl.items():
        d = os.path.join(dst, k.replace("GT", "GT-"))
        os.makedirs(d, exist_ok=True)
        for a, b, name in rows:
            subprocess.run(["qpdf", "--empty", "--compress-streams=y", "--object-streams=generate", "--pages", files[k], "%d-%d" % (a, b), "--", os.path.join(d, name)], check=True)
    json.dump(pl, open(os.path.join(HERE, "gtcv_split.json"), "w"), ensure_ascii=False, indent=0)
    print({k: len(v) for k, v in pl.items()})
