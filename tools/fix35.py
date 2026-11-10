"""Decide 3 vs 5 by glyph shape (a '5' has a vertical stroke at the upper left, a '3' is open there)
for the 7-digit field of line numbers and the 4-digit field of equipment tags."""
import sys, os, json, re, collections
import cv2
sys.path.insert(0, "/home/claude/work")
import bubbles, digit35, ocr as O
OUT = "/home/claude/work/fix35"; os.makedirs(OUT, exist_ok=True)
LN = re.compile(r'^(.*?"-[A-Z]{1,4}-)(\d{7})(-.*)$')
EQ = re.compile(r"^(\d{2})-([A-Z]{1,3})-(\d{4})(.*)$")

def fix_line(t, segs, th, tag):
    m = LN.match(tag)
    if not m or not set(m.group(2)) & set("35") or len(segs) < 4: return None
    num = m.group(2)
    cells = digit35.field_cells(t, segs[-3], num, th)
    if not cells: return None
    new = "".join((digit35.decide35(c) or ch) if ch in "35" else ch for ch, c in zip(num, cells))
    return m.group(1) + new + m.group(3)

def fix_equip(t, segs, th, tag):
    m = EQ.match(tag)
    if not m or not set(m.group(3)) & set("35") or len(segs) < 2: return None
    rest = m.group(4)
    # drawn as e.g. "30-TK1003" or "30-PK1001/TK3": the field after the area code holds letters+digits+rest
    chars = m.group(2) + m.group(3) + rest
    cells = digit35.field_cells(t, [segs[1][0], segs[-1][1]], chars, th)
    if not cells: return None
    off = len(m.group(2))
    num = "".join((digit35.decide35(cells[off + j]) or ch) if ch in "35" else ch for j, ch in enumerate(m.group(3)))
    return f"{m.group(1)}-{m.group(2)}-{num}{rest}"

def main(k, n):
    d = json.load(open("/home/claude/work/site/data/data.json"))
    jobs = {j[2]: j for j in O.jobs()}
    per = collections.defaultdict(list)
    for t in d["tags"]:
        if t["k"] != "line": continue   # equipment labels segment too unreliably
        for o in t["o"]:
            if len(o) > 5: continue
            lab = t["l"][0] if t.get("l") else t["t"]
            per[o[0]].append((lab, t["k"], o[1], o[2], o[3], o[4]))
    for i, s in enumerate(d["sheets"]):
        if i % n != k or i not in per: continue
        out = f"{OUT}/{s['id']}.json"
        if os.path.exists(out): continue
        f, p, _ = jobs[s["id"]]
        g = bubbles.render(f, p); H, W = g.shape
        res = []
        for tag, kind, x, y, w, h in dict.fromkeys(per[i]):
            c = g[max(0, int(y * H) - 8):int((y + h) * H) + 8, max(0, int(x * W) - 8):int((x + w) * W) + 8]
            if c.size == 0: continue
            if c.shape[0] > c.shape[1] * 1.5: c = cv2.rotate(c, cv2.ROTATE_90_CLOCKWISE)
            try:
                t, segs, th = digit35.segments(c)
                if t is None: continue
                new = (fix_line if kind == "line" else fix_equip)(t, segs, th, tag)
            except Exception:
                new = None
            if new: res.append({"t": tag, "x": x, "y": y, "new": new})
        json.dump(res, open(out, "w"))
        print(s["id"], len(res), sum(r["new"] != r["t"] for r in res), flush=True)

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]))
