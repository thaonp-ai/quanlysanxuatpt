import sys, os, json, subprocess, io, csv
import numpy as np, cv2
sys.path.insert(0, "/home/claude/work")
import bubbles, ocr as O
OUT = "/home/claude/work/ocr2"; os.makedirs(OUT, exist_ok=True)

def tess(img):
    ok, buf = cv2.imencode(".png", img)
    r = subprocess.run(["tesseract", "stdin", "stdout", "--psm", "11", "tsv"], input=buf.tobytes(), capture_output=True)
    rows = []
    for row in csv.DictReader(io.StringIO(r.stdout.decode("utf8", "ignore")), delimiter="\t", quoting=csv.QUOTE_NONE):
        t = (row.get("text") or "").strip()
        if t and float(row["conf"]) > 0:
            rows.append((t, int(row["left"]), int(row["top"]), int(row["width"]), int(row["height"]), float(row["conf"])))
    return rows

def run(f, p, sid):
    if os.path.exists(f"{OUT}/{sid}.json"): return
    g = bubbles.render(f, p)
    H, W = g.shape
    TW, TH, OV = 3200, 2400, 450
    words = []
    for y in range(0, H, TH - OV):
        for x in range(0, int(W * 0.86), TW - OV):
            t = g[y:y + TH, x:x + TW]
            if t.size == 0 or (t < 128).mean() < 0.002: continue
            for tx, l, tp, w, h, c in tess(t):
                words.append([tx, (x + l) / W, (y + tp) / H, w / W, h / H, c, 0])
            r = cv2.rotate(t, cv2.ROTATE_90_COUNTERCLOCKWISE)  # text running bottom->top becomes horizontal
            th, tw = t.shape
            for tx, l, tp, w, h, c in tess(r):
                # rotated (CCW) coords: x' = y, y' = tw - x  ->  x = tw - y' - h', y = x'
                ox, oy = x + (tw - tp - h), y + l
                words.append([tx, ox / W, oy / H, h / W, w / H, c, 1])
    json.dump({"id": sid, "words": words}, open(f"{OUT}/{sid}.json", "w"))
    print(sid, len(words), flush=True)

if __name__ == "__main__":
    k, n = int(sys.argv[1]), int(sys.argv[2])
    only = sys.argv[3] if len(sys.argv) > 3 else None
    jobs = [j for j in O.jobs() if j[2].startswith("PID")]
    for i, (f, p, sid) in enumerate(jobs):
        if only and sid != only: continue
        if only or i % n == k: run(f, p, sid)
