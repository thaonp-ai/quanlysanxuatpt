"""Thay danh sách van tay (block/drain/vent/bypass) trong data.json bằng danh mục CMMS của X.PT (valves.json).

    python3 tools/valves/apply_valves.py web/data/data.json      # sửa tại chỗ
    (build.py gọi apply(sheets, tags) ở bước cuối)

- Bỏ mọi nhãn van chặn OCR (k=valve, s=BLOCK, tên kiểu "B1-01").
- Thêm từng van trong valves.json, tên = tagname CMMS, d = Name, p = Parent Asset, n = ghi chú.
- Vị trí (o):
  * Tag "UUNN-x/y-XX-nn": P&ID số NN của Unit UU, trang x/y. Chọn tờ có nhiều nhãn trùng nhất với danh mục,
    rồi lấy vị trí nhãn OCR "XX-nn" trên tờ đó (ocr_labels.json, chụp từ data.json trước khi thay).
  * Tag "AA-U1-FV8003" (U=trước, D=sau, B=bypass van điều khiển): vị trí van AA-FV-8003, cờ 3 (gần đúng).
  * Tag trùng tên tag đã có (HV/SV/XV…): giữ vị trí tag đó, cập nhật d/p/n.
  * Không tìm được: vị trí thiết bị cha (Parent Asset) trên P&ID (ưu tiên đúng tờ), cờ 3;
    vẫn không có thì chỉ mở bản vẽ, cờ 2 ([sheet, 0, 0, 1, 1, 2]).
"""
import collections, itertools, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
STD = re.compile(r"^(\d\d)(\d\d)-(\d+)/(\d+)-([A-Z]+\d*)-(\d+)$")
CV = re.compile(r"^(\d\d)-([UDB])\d-([A-Z]+)(\d+[A-Z]?)$")


def nk(s):
    return re.sub(r"[^A-Z0-9/]", "", str(s).upper())


def lab_key(s):
    m = re.match(r"^([A-Z]+\d*)-(\d+)$", s)
    return (m.group(1), int(m.group(2))) if m else None


def apply(sheets, tags, valves=None, labels=None):
    """sheets: list; tags: list of tag dicts (data.json format). Returns new tag list."""
    valves = valves or json.load(open(os.path.join(HERE, "valves.json")))
    labels = labels or json.load(open(os.path.join(HERE, "ocr_labels.json")))
    sidx = {s["id"]: i for i, s in enumerate(sheets)}
    is_pid = lambda i: "PID" in sheets[i]["dwg"] or sheets[i]["id"].startswith("VGT")
    lab = collections.defaultdict(lambda: collections.defaultdict(list))  # sheet index -> key -> boxes
    for sid, items in labels.items():
        if sid in sidx:
            for t, x, y, w, h in items:
                k = lab_key(t)
                if k:
                    lab[sidx[sid]][k].append([x, y, w, h])
    # drop OCR block-valve labels
    tags = [t for t in tags if not (t["k"] == "valve" and t["s"] == "BLOCK")]
    byname = {}
    for t in tags:
        for n in [t["t"]] + t.get("a", []):
            byname.setdefault(nk(n), t)

    def pos_of(key, prefer=None):
        k = nk(key)
        while k:
            t = byname.get(k)
            if t:
                o = [p for p in t["o"] if is_pid(p[0]) and not (len(p) > 5 and p[5] == 1)] or [p for p in t["o"] if is_pid(p[0])]
                if prefer is not None and any(p[0] == prefer for p in o):
                    o = [p for p in o if p[0] == prefer]
                if o:
                    return [p[:5] for p in o]
            if "/" not in k:
                break
            k = k.rsplit("/", 1)[0]
        return None

    # choose the sheet of each drawing prefix by label overlap
    groups = collections.defaultdict(set)
    for v in valves:
        m = STD.match(v["t"])
        if m:
            groups[m.group(1, 2, 3, 4)].add((m.group(5), int(m.group(6))))
    # các trang x/y của cùng một bản vẽ phải rơi vào các tờ khác nhau: thử mọi cách gán, lấy tổng số nhãn trùng lớn nhất
    pick = {}
    bydw = collections.defaultdict(list)
    for g in groups:
        bydw[g[:2]].append(g)
    for (u, n), gs in bydw.items():
        cands = [i for i, s in enumerate(sheets) if re.search(rf"-{u}-PID-0031-{n}\b", s["dwg"])]
        if not cands:
            continue
        gs.sort(key=lambda g: int(g[2]))
        score = lambda g, i: len(groups[g] & set(lab[i]))
        if len(gs) <= len(cands):
            best = max(itertools.permutations(cands, len(gs)),
                       key=lambda pm: (sum(score(g, i) for g, i in zip(gs, pm)), -sum(abs(cands.index(i) - (int(g[2]) - 1)) for g, i in zip(gs, pm))))
            pick.update(zip(gs, best))
        else:
            for g in gs:
                pick[g] = max(cands, key=lambda i: (score(g, i), -cands.index(i)))
    stat = collections.Counter()
    out_new = []
    for v in valves:
        e = {"t": v["t"], "k": "valve", "s": v["s"], "d": v["d"]}
        for f in ("p", "n"):
            if v.get(f):
                e[f] = v[f]
        old = byname.get(nk(v["t"]))
        if old is not None and old["k"] == "valve":
            old.update({kk: vv for kk, vv in e.items() if kk in ("d", "p", "n")})
            old["cm"] = 1
            stat["trùng tag có sẵn"] += 1
            continue
        o, sh = None, None
        m = STD.match(v["t"])
        if m:
            sh = pick.get(m.group(1, 2, 3, 4))
            if sh is not None:
                b = lab[sh].get((m.group(5), int(m.group(6))))
                if b:
                    o = [[sh] + bb for bb in b]
                    stat["nhãn trên bản vẽ"] += 1
        if o is None:
            c = CV.match(v["t"])
            if c:
                p = pos_of(f"{c.group(1)}-{c.group(3)}-{c.group(4)}")
                if p:
                    o = [p_ + [3] for p_ in p]
                    stat["theo van điều khiển"] += 1
        if o is None and v.get("p"):
            p = pos_of(v["p"], sh)
            if p and (sh is None or any(q[0] == sh for q in p)):
                o = [p_ + [3] for p_ in p]
                stat["theo thiết bị cha"] += 1
        if o is None and sh is not None:
            o = [[sh, 0, 0, 1, 1, 2]]
            stat["chỉ biết bản vẽ"] += 1
        if o is None and v.get("p"):
            p = pos_of(v["p"])
            if p:
                o = [p_ + [3] for p_ in p]
                stat["theo thiết bị cha (tờ khác)"] += 1
        if o is None:
            stat["không định vị được"] += 1
            continue
        e["o"] = o
        e["cm"] = 1
        out_new.append(e)
    print("Van CMMS:", dict(stat), file=sys.stderr)
    return tags + out_new


if __name__ == "__main__":
    p = sys.argv[1]
    d = json.load(open(p))
    d["tags"] = apply(d["sheets"], d["tags"])
    json.dump(d, open(p, "w"), ensure_ascii=False, separators=(",", ":"))
