"""Thay danh sách van tay (block/drain/vent/bypass) trong data.json bằng danh mục CMMS của X.PT (valves.json).

    python3 tools/valves/apply_valves.py web/data/data.json      # sửa tại chỗ
    (build.py gọi apply(sheets, tags) ở bước cuối)

- Bỏ mọi nhãn van chặn OCR (k=valve, s=BLOCK, tên kiểu "B1-01").
- Thêm từng van trong valves.json, tên = tagname CMMS, d = Name, p = Parent Asset, n = ghi chú.
- Vị trí (o):
  * Tag "UUNN-x/y-XX-nn": P&ID số NN của Unit UU, trang x/y. Chọn tờ có nhiều nhãn trùng nhất với danh mục,
    rồi lấy vị trí nhãn OCR "XX-nn" trên tờ đó (ocr_labels.json, chụp từ data.json trước khi thay).
  * Tag "AA-U1-FV8003" (U=trước, D=sau, B=bypass van điều khiển): vị trí van AA-FV-8003, cờ 3 (gần đúng).
  * Tag trùng tên tag đã có (HV/SV/XV…, kể cả bong bóng U1/D1/B1 đã sửa tên ở bubblefix.json): giữ vị trí tag đó.
  * Tag "AA-U1-FV8003" chưa có: tìm bong bóng "U1FV 8003" (bubbles.json: chữ OCR Tesseract + bộ đọc phông CAD)
    trên tờ có van điều khiển, so khớp có tính ký tự dễ nhầm (fuzzy.py).
  * Không tìm được: chỉ mở bản vẽ (tờ của thiết bị cha/van điều khiển), cờ 2 ([sheet, 0, 0, 1, 1, 2]) —
    không khoanh thiết bị cha để khỏi nhầm.
- Trước đó áp bubblefix.json (soát bằng mắt 11/2026): sửa tên van OCR đọc sai ở từng vị trí bong bóng
  ({sid, box, from, to}; to "" = bỏ vị trí đó, "L" = bỏ nếu tag còn vị trí khác — chú giải/ghi chú),
  thêm van điều khiển bị thiếu tìm thấy trong bong bóng.
"""
import collections, itertools, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fuzzy import clean, dist

HERE = os.path.dirname(os.path.abspath(__file__))
STD = re.compile(r"^(\d\d)(\d\d)-(\d+)/(\d+)-([A-Z]+\d*)-(\d+)$")
CV = re.compile(r"^(\d\d)-([UDB])\d-([A-Z]+)(\d+[A-Z]?)$")


VNAME = {"PV": "Van điều khiển áp suất", "FV": "Van điều khiển lưu lượng", "LV": "Van điều khiển mức",
         "TV": "Van điều khiển nhiệt độ", "HV": "Van điều khiển tay (HV)", "XV": "Van on/off (XV)", "PCV": "Van tự điều áp",
         "MOV": "Van điện", "AV": "Van khí điều khiển", "FCV": "Van điều khiển lưu lượng", "LCV": "Van điều khiển mức"}


def nk(s):
    return re.sub(r"[^A-Z0-9/]", "", str(s).upper())


def lab_key(s):
    m = re.match(r"^([A-Z]+\d*)-(\d+)$", s)
    return (m.group(1), int(m.group(2))) if m else None


def load_bubbles(sidx):
    f = os.path.join(HERE, "bubbles.json")
    out = collections.defaultdict(list)
    if os.path.exists(f):
        for sid, items in json.load(open(f)).items():
            if sid in sidx:
                out[sidx[sid]] = items
    return out


def match_bubble(bubbles, cand, target, used, maxd=1.25):
    """bong bóng khớp nhất với chuỗi target (vd 'U1FV8003') trên các tờ cand; trả [sheet,x,y,w,h] hoặc None."""
    target = clean(target)
    best = []
    for si in cand:
        for x, y, w, h, t1, t2 in bubbles.get(si, []):
            if any(abs(x - ux) < 0.004 and abs(y - uy) < 0.004 for ux, uy in used.get(si, ())):
                continue
            d = min(dist(clean(t1), target), dist(clean(t2), target))
            best.append((d, si, x, y, w, h))
    best.sort()
    if best and best[0][0] <= maxd and (len(best) < 2 or best[1][0] - best[0][0] >= 0.5):
        d, si, x, y, w, h = best[0]
        return [si, x, y, w, h]
    return None


def bubble_fix(sheets, tags, sidx):
    """bubblefix.json: sửa tên/bỏ từng vị trí tag (van, cả thiết bị) đã soát bằng mắt."""
    f = os.path.join(HERE, "bubblefix.json")
    if not os.path.exists(f):
        return tags
    byt = {t["t"]: t for t in tags}
    near = lambda p, si, b: p[0] == si and abs(p[1] - b[0]) < 0.002 and abs(p[2] - b[1]) < 0.002
    n = collections.Counter()
    for fx in json.load(open(f)):
        si = sidx.get(fx["sid"]);t = byt.get(fx["from"])
        if si is None or t is None:
            n["không thấy"] += 1
            continue
        occ = [p for p in t["o"] if near(p, si, fx["box"])]
        if not occ:
            n["không thấy"] += 1
            continue
        if fx["to"] == "L" and len(t["o"]) == len(occ):
            continue
        t["o"] = [p for p in t["o"] if p not in occ]
        if fx["to"] in ("", "L"):
            n["bỏ"] += 1
            continue
        m = re.match(r"^\d\d-(?:[UDB]\d-)?([A-Z]+)", fx["to"])
        nt = byt.get(fx["to"])
        if nt is None:
            fn = m.group(1) if m else "V"
            if t["k"] != "valve":
                nt = {"t": fx["to"], "k": t["k"], "s": t["s"], "d": t["d"], "o": []}
            else:
                nt = {"t": fx["to"], "k": "valve", "s": fn if not re.match(r"^\d\d-[UDB]\d-", fx["to"]) else "BLOCK",
                      "d": t["d"] if not re.match(r"^\d\d-[UDB]\d-", fx["to"]) else "Van tay", "o": []}
            if not t["o"]:
                nt["a"] = sorted(set([t["t"]] + t.get("a", [])))
            byt[fx["to"]] = nt
            tags.append(nt)
        nt["o"] += occ
        n["đổi tên"] += 1
    print("Sửa bong bóng:", dict(n), file=sys.stderr)
    return [t for t in tags if t["o"]]


def sheet_codes(sheets, pick):
    """chỉ số tờ -> "UUNN-x/y" theo cách đánh số của danh mục CMMS (pick: (UU,NN,x,y) -> tờ)."""
    code = {si: f"{u}{n}-{x}/{y}" for (u, n, x, y), si in pick.items()}
    grp = collections.defaultdict(list)
    for i, s in enumerate(sheets):
        m = re.search(r"-(\d\d)-PID-0031-(\d\d)\b", s["dwg"])
        if m:
            grp[m.groups()].append(i)
    for (u, n), sis in grp.items():
        used = {int(code[i].split("-")[1].split("/")[0]) for i in sis if i in code}
        ys = {int(code[i].split("/")[1]) for i in sis if i in code}
        y = max(ys | {len(sis)})
        free = [k for k in range(1, y + 1) if k not in used]
        for i in sis:
            if i not in code:
                x = free.pop(0) if free else sis.index(i) + 1
                code[i] = f"{u}{n}-{x}/{max(y, x)}"
    return code


def rename_checks(sheets, tags, pick, labels, sidx):
    """Van một chiều: nhãn "C1-01" trên P&ID → tag "1801-1/4-C1-01" (cùng kiểu tag van block CMMS).
    Gộp vị trí OCR cũ (tag s=CHECK) với nhãn đọc lại (ocr_labels.json), sửa/bỏ theo checkfix.json."""
    code = sheet_codes(sheets, pick)
    ov = lambda a, b: not (a[0] + a[2] < b[0] or b[0] + b[2] < a[0] or a[1] + a[3] < b[1] or b[1] + b[3] < a[1])
    occ = collections.defaultdict(list)
    for t in tags:
        if t["k"] == "valve" and t["s"] == "CHECK":
            for o in t["o"]:
                occ[o[0]].append([t["t"]] + o[1:5])
    for sid, items in labels.items():
        si = sidx.get(sid)
        if si is None:
            continue
        for lb, *b in items:
            if lb.startswith("C") and not any(ov(b, c[1:]) for c in occ[si]):
                occ[si].append([lb] + b)
    fx = os.path.join(HERE, "checkfix.json")
    fixes = json.load(open(fx)) if os.path.exists(fx) else []
    tags = [t for t in tags if not (t["k"] == "valve" and t["s"] == "CHECK")]
    new = {}
    for si, items in occ.items():
        for lb, x, y, w, h in items:
            f = next((f for f in fixes if sidx.get(f["sid"]) == si and abs(f["x"] - x) < 0.002 and abs(f["y"] - y) < 0.002), None)
            if f is not None:
                if not f["to"]:
                    continue
                lb = f["to"]
            m = re.match(r"^C(\d?)-(\d{1,2})$", lb)
            if not m or si not in code:
                continue
            name = f"{code[si]}-C{m.group(1) or '1'}-{int(m.group(2)):02d}"
            e = new.setdefault(name, {"t": name, "k": "valve", "s": "CHECK", "d": "Van một chiều", "o": [], "a": []})
            e["o"].append([si, x, y, w, h])
    print("Van một chiều:", len(new), "tag", file=sys.stderr)
    for e in new.values():
        e.pop("a")
    return tags + list(new.values())


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
    tags = bubble_fix(sheets, tags, sidx)
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
    bubbles = load_bubbles(sidx)
    used = collections.defaultdict(list)
    for t in tags:
        if t["k"] == "valve":
            for q in t["o"]:
                used[q[0]].append((q[1], q[2]))
    # van điều khiển được nhắc tới trong danh mục (AA-U1-FV8003 → AA-FV-8003) nhưng OCR bỏ sót: tìm bong bóng
    for v in valves:
        c = CV.match(v["t"])
        if not c:
            continue
        cvt = f"{c.group(1)}-{c.group(3)}-{c.group(4)}"
        if byname.get(nk(cvt)):
            continue
        pp = pos_of(v.get("p", ""))
        cand = sorted({q[0] for q in pp}) if pp else []
        hit = match_bubble(bubbles, cand, c.group(3) + c.group(4), used, maxd=0.75)
        if hit:
            nt = {"t": cvt, "k": "valve", "s": c.group(3), "d": VNAME.get(c.group(3), "Van"), "o": [hit]}
            tags.append(nt);byname[nk(cvt)] = nt;used[hit[0]].append((hit[1], hit[2]))
            stat["thêm van điều khiển từ bong bóng"] += 1
    for v in valves:
        e = {"t": v["t"], "k": "valve", "s": v["s"], "d": v["d"]}
        for f in ("p", "n"):
            if v.get(f):
                e[f] = v[f]
        old = byname.get(nk(v["t"]))
        if old is not None and old["k"] == "valve":
            old.update({kk: vv for kk, vv in e.items() if kk in ("s", "d", "p", "n")})
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
        c = CV.match(v["t"])
        if o is None and c:
            cvt = f"{c.group(1)}-{c.group(3)}-{c.group(4)}"
            p = pos_of(cvt)
            cand = sorted({q[0] for q in p}) if p else []
            if sh is not None and sh not in cand:
                cand.append(sh)
            pp = pos_of(v.get("p", ""))
            if not cand and pp:
                cand = sorted({q[0] for q in pp})
            hit = match_bubble(bubbles, cand, v["t"].split("-", 1)[1].replace("-", ""), used)
            if hit:
                o = [hit];used[hit[0]].append((hit[1], hit[2]))
                stat["bong bóng trên bản vẽ"] += 1
            elif p:
                o = [[q[0], 0, 0, 1, 1, 2] for q in p[:1]]
                stat["chỉ biết bản vẽ (van điều khiển)"] += 1
        if o is None and sh is not None:
            o = [[sh, 0, 0, 1, 1, 2]]
            stat["chỉ biết bản vẽ"] += 1
        if o is None and v.get("p"):
            p = pos_of(v["p"])
            if p:
                o = [[p[0][0], 0, 0, 1, 1, 2]]
                stat["chỉ biết bản vẽ (thiết bị cha)"] += 1
        if o is None:
            stat["không định vị được"] += 1
            continue
        e["o"] = o
        e["cm"] = 1
        out_new.append(e)
    print("Van CMMS:", dict(stat), file=sys.stderr)
    tags = rename_checks(sheets, tags + out_new, pick, labels, sidx)
    tags = bubble_fix(sheets, tags, sidx)  # lần 2: sửa cả van điều khiển vừa thêm từ bong bóng
    return tags


if __name__ == "__main__":
    p = sys.argv[1]
    d = json.load(open(p))
    d["tags"] = apply(d["sheets"], d["tags"])
    json.dump(d, open(p, "w"), ensure_ascii=False, separators=(",", ":"))
