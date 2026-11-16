"""Gộp nhãn van OCR lại (relabel.py → thư mục hl/<sheet>.json) với nhãn OCR cũ (ocr_labels_old.json) → ocr_labels.json.

    python3 tools/valves/merge_labels.py <thư mục hl>

Mỗi tờ lấy nguồn đọc được nhiều nhãn hơn làm chính, thêm nhãn của nguồn kia nếu không chồng khung và tên chưa có.
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def norm(t):
    m = re.match(r"^([A-Z]+)([A-Z0-9]?)-(\d+[A-Z]?)$", t)
    if not m:
        return None
    a, b, n = m.groups()
    if a in ("B", "C") and b in ("L", "I", "T"):
        b = "1"
    if a + b in ("BL", "BI"):
        a, b = "B", "1"
    return f"{a}{b}-{n}"


def overlap(a, b):
    return not (a[0] + a[2] < b[0] or b[0] + b[2] < a[0] or a[1] + a[3] < b[1] or b[1] + b[3] < a[1])


def main(hl):
    old = json.load(open(os.path.join(HERE, "ocr_labels_old.json")))
    out = {}
    for f in glob.glob(os.path.join(hl, "*.json")):
        sid = os.path.basename(f)[:-5]
        new = []
        for t, x, y, w, h in json.load(open(f)):
            t = norm(t)
            if t:
                new.append([t, x, y, w, h])
        out[sid] = new
    # mỗi tờ: lấy nguồn đọc được nhiều nhãn khác nhau hơn làm chính (bản 2098 nét đậm → đọc lại tốt hơn;
    # bản 2539 chữ mảnh sẵn → OCR cũ tốt hơn), rồi thêm nhãn của nguồn kia không chồng khung và chưa có tên
    for sid, items in old.items():
        new = out.get(sid, [])
        main, other = (new, items) if len({t for t, *_ in new}) > len({t for t, *_ in items}) else (items, new)
        res = [list(x) for x in main]
        have = {t for t, *_ in res}
        for t, *bx in other:
            if t not in have and not any(overlap(bx, n[1:]) for n in res):
                res.append([t] + bx)
        out[sid] = res
    json.dump(out, open(os.path.join(HERE, "ocr_labels.json"), "w"), ensure_ascii=False, separators=(",", ":"))
    print(sum(map(len, out.values())), "nhãn")


if __name__ == "__main__":
    main(sys.argv[1])
