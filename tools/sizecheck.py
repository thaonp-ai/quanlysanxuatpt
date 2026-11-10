"""Re-read the pipe size of every line number from a crop that extends well before the label,
so a size digit that fell outside the first OCR box ("0" for "20") is recovered."""
import sys, os, json, re, subprocess, io, csv, collections
import numpy as np, cv2
sys.path.insert(0, "/home/claude/work")
import bubbles, ocr as O, parse as P
OUT = "/home/claude/work/sizecheck"; os.makedirs(OUT, exist_ok=True)
TARGETS = [16, 20, 24]
SIZE = re.compile(r"^(\d{1,2}|\d/\d|\d-\d/\d)$")
LN = re.compile(r'^(.*?)"-([A-Z]{1,4})-(\d{7})-(.*)$')

def read_size(words, svc, num):
    """words: list of tokens in reading order. Find the token holding '-SVC-NUM' and the size in front of it."""
    toks = [P.norm(w) for w in words]
    for i, t in enumerate(toks):
        t2 = re.sub(r"[^0-9A-Z/-]", "", t)
        mm = re.search(rf"-{svc}-\d{{3}}", t2)
        j = mm.start() if mm else -1
        if j < 0:
            j2 = 0 if re.match(rf"{svc}-\d{{3}}", t2) else -1
            if j2 == 0 and i > 0:      # size is a separate token before
                prev = re.sub(r"[^0-9/-]", "", toks[i - 1]).strip("-")
                if i > 1 and re.fullmatch(r"\d/\d", prev) and re.fullmatch(r"\d", toks[i - 2]): prev = toks[i - 2] + "-" + prev
                return prev if SIZE.match(prev) else None
            continue
        pre = t2[:j]
        pre = re.sub(r"^[^0-9]+", "", pre)
        if re.fullmatch(r"\d/\d", pre) and i > 0 and re.fullmatch(r"\d", toks[i - 1]): pre = toks[i - 1] + "-" + pre
        pre = re.sub(r"^(\d)(\d/\d)$", r"\1-\2", pre)
        return pre if SIZE.match(pre) else None
    return None

def main(k, n):
    d = json.load(open("/home/claude/work/site/data/data.json"))
    jobs = {j[2]: j for j in O.jobs()}
    per = collections.defaultdict(list)
    for t in d["tags"]:
        if t["k"] != "line": continue
        for o in t["o"]: per[o[0]].append((t["t"], o[1], o[2], o[3], o[4]))
    for si, s in enumerate(d["sheets"]):
        if si % n != k or si not in per: continue
        out = f"{OUT}/{s['id']}.json"
        if os.path.exists(out): continue
        f, p, _ = jobs[s["id"]]
        g = bubbles.render(f, p); H, W = g.shape
        crops = []
        for tag, x, y, w, h in per[si]:
            X0, Y0, X1, Y1 = int(x * W), int(y * H), int((x + w) * W), int((y + h) * H)
            vert = (Y1 - Y0) > (X1 - X0) * 1.5
            th = (X1 - X0) if vert else (Y1 - Y0)
            ext = int(th * 4)
            if vert:   # text runs bottom -> top: the start of the label is below
                c = g[max(0, Y0 - 6):min(H, Y1 + ext), max(0, X0 - 6):X1 + 6]
                c = cv2.rotate(c, cv2.ROTATE_90_CLOCKWISE)
            else:
                c = g[max(0, Y0 - 6):Y1 + 6, max(0, X0 - ext):min(W, X1 + 6)]
            crops.append((c, max(th, 8)))
        votes = [collections.Counter() for _ in crops]
        for T in TARGETS:
            rows = []
            for c, th in crops:
                s_ = T / th
                rows.append(cv2.resize(c, None, fx=s_, fy=s_, interpolation=cv2.INTER_AREA if s_ < 1 else cv2.INTER_CUBIC))
            RH = max(r.shape[0] for r in rows) + 3 * T
            WW = min(max(r.shape[1] for r in rows) + 60, 12000)
            mont = np.full((RH * len(rows), WW), 255, np.uint8)
            for i, r in enumerate(rows):
                r = r[:, :WW - 60]; y0 = i * RH + (RH - r.shape[0]) // 2
                mont[y0:y0 + r.shape[0], 30:30 + r.shape[1]] = r
            for s0 in range(0, len(rows), 120):
                ok, buf = cv2.imencode(".png", mont[s0 * RH:(s0 + 120) * RH])
                tsv = subprocess.run(["tesseract", "stdin", "stdout", "--psm", "4", "tsv"], input=buf.tobytes(), capture_output=True).stdout.decode("utf8", "ignore")
                text = collections.defaultdict(list)
                for row in csv.DictReader(io.StringIO(tsv), delimiter="\t", quoting=csv.QUOTE_NONE):
                    tt = (row.get("text") or "").strip()
                    if tt: text[s0 + (int(row["top"]) + int(row["height"]) // 2) // RH].append((int(row["left"]), tt))
                for i, ws in text.items():
                    if i >= len(crops): continue
                    m = LN.match(per[si][i][0])
                    if not m: continue
                    sz = read_size([t for _, t in sorted(ws)], m.group(2), m.group(3))
                    if sz: votes[i][sz] += 1
        res = [{"t": tag, "x": x, "y": y, "votes": dict(v)} for (tag, x, y, w, h), v in zip(per[si], votes)]
        json.dump(res, open(out, "w"))
        print(s["id"], len(res), flush=True)

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]))
