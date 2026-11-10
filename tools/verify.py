"""Second-opinion pass: re-read every line / equipment / block-valve tag from a tight crop
at several text sizes and take a majority vote. Writes corrections.json."""
import sys, os, json, re, subprocess, io, csv, collections
import numpy as np, cv2
sys.path.insert(0, "/home/claude/work")
import bubbles, parse as P, ocr as O

TARGETS = [16, 20, 24, 28, 34]   # text height in px
DILS = [0, 1]
OUT = "/home/claude/work/verify"; os.makedirs(OUT, exist_ok=True)

def parse_one(s, area):
    s = s.replace(" ", "")
    w = [[P.norm(s), 0, 0, 0.05, 0.01, 90, 0]]
    r = [t for t in P.extract({"words": w, "unit": ""}, area)]
    return r[0][0] if r else None

def run(sid, f, p, occs, area):
    out = f"{OUT}/{sid}.json"
    if os.path.exists(out): return
    g = bubbles.render(f, p)
    H, W = g.shape
    crops = []
    for tag, k, x, y, w, h in occs:
        X0, Y0, X1, Y1 = int(x * W), int(y * H), int((x + w) * W), int((y + h) * H)
        th = min(X1 - X0, Y1 - Y0)
        pad = max(6, int(th * 0.35))
        c = g[max(0, Y0 - pad):Y1 + pad, max(0, X0 - pad):X1 + pad]
        if (Y1 - Y0) > (X1 - X0) * 1.5: c = cv2.rotate(c, cv2.ROTATE_90_CLOCKWISE)
        crops.append((c, max(th, 8)))
    votes = [collections.Counter() for _ in occs]
    for T in TARGETS:
        for dil in DILS:
            rows = []
            for c, th in crops:
                s = T / th
                cc = cv2.resize(c, None, fx=s, fy=s, interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)
                if dil: cc = cv2.erode(cc, np.ones((2, 2), np.uint8))
                rows.append(cc)
            if not rows: continue
            RH = max(r.shape[0] for r in rows) + 3 * T
            WW = min(max(r.shape[1] for r in rows) + 60, 12000)
            mont = np.full((RH * len(rows), WW), 255, np.uint8)
            for i, r in enumerate(rows):
                r = r[:, :WW - 60]
                y0 = i * RH + (RH - r.shape[0]) // 2
                mont[y0:y0 + r.shape[0], 30:30 + r.shape[1]] = r
            # tesseract struggles with very tall images: process in chunks
            for s0 in range(0, len(rows), 120):
                sub = mont[s0 * RH:(s0 + 120) * RH]
                ok, buf = cv2.imencode(".png", sub)
                tsv = subprocess.run(["tesseract", "stdin", "stdout", "--psm", "4", "tsv"], input=buf.tobytes(), capture_output=True).stdout.decode("utf8", "ignore")
                text = collections.defaultdict(list)
                for row in csv.DictReader(io.StringIO(tsv), delimiter="\t", quoting=csv.QUOTE_NONE):
                    t = (row.get("text") or "").strip()
                    if not t: continue
                    i = s0 + (int(row["top"]) + int(row["height"]) // 2) // RH
                    text[i].append((int(row["left"]), t))
                for i, ws in text.items():
                    if i >= len(occs): continue
                    rd = parse_one("".join(t for _, t in sorted(ws)), area)
                    if rd and P_kind(rd) == occs[i][1]: votes[i][rd] += 1
    res = []
    for (tag, k, x, y, w, h), v in zip(occs, votes):
        res.append({"t": tag, "x": x, "y": y, "votes": dict(v)})
    json.dump(res, open(out, "w"))
    print(sid, len(occs), flush=True)

def P_kind(tag):
    if re.match(r'^[\d/-]+"-', tag): return "line"
    if re.match(r"^[BC]\d-\d", tag): return "valve"
    return "equipment"

if __name__ == "__main__":
    k, n = int(sys.argv[1]), int(sys.argv[2])
    d = json.load(open("/home/claude/work/site/data/data.json"))
    jobs = {j[2]: j for j in O.jobs()}
    per = collections.defaultdict(list)
    for t in d["tags"]:
        if t["k"] == "valve" and not re.match(r"^[BC]\d-\d", t["t"]): continue
        for o in t["o"]:
            if len(o) > 5: continue
            per[o[0]].append((t["l"][0] if t.get("l") else t["t"], t["k"], o[1], o[2], o[3], o[4]))
    for i, s in enumerate(d["sheets"]):
        if i % n != k: continue
        occs = list(dict.fromkeys(per.get(i, [])))  # combined labels appear once per expanded name
        if not occs: continue
        f, p, _ = jobs[s["id"]]
        eq = [o for o in occs if o[1] == "equipment"]
        cnt = collections.Counter(o[0][:2] for o in eq)
        area = cnt.most_common(1)[0][0] if cnt else None
        run(s["id"], f, p, occs, area)
