"""Gộp nhãn van OCR lại (relabel.py → thư mục hl/<sheet>.json) với nhãn OCR cũ (ocr_labels_old.json) → ocr_labels.json.

    python3 tools/valves/merge_labels.py <thư mục hl>

Nhãn OCR lại (nét vẽ đã làm mảnh, đọc rõ) được ưu tiên; nhãn cũ chỉ giữ khi không chồng lên khung nào của lần đọc lại
và tên chưa có trên tờ đó.
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
    for sid, items in old.items():
        if sid not in out:
            out[sid] = items
            continue
        have = {t for t, *_ in out[sid]}
        for t, *b in items:
            if t not in have and not any(overlap(b, n[1:]) for n in out[sid]):
                out[sid].append([t] + b)
    json.dump(out, open(os.path.join(HERE, "ocr_labels.json"), "w"), ensure_ascii=False, separators=(",", ":"))
    print(sum(map(len, out.values())), "nhãn")


if __name__ == "__main__":
    main(sys.argv[1])
