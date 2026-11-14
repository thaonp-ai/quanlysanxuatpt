import sys, os, json, subprocess, io, csv
import numpy as np, cv2
from concurrent.futures import ThreadPoolExecutor
def tess(img):
    ok, buf = cv2.imencode(".png", img)
    r = subprocess.run(["tesseract", "stdin", "stdout", "--psm", "11", "tsv"], input=buf.tobytes(), capture_output=True)
    rows = []
    for row in csv.DictReader(io.StringIO(r.stdout.decode("utf8", "ignore")), delimiter="\t", quoting=csv.QUOTE_NONE):
        t = (row.get("text") or "").strip()
        if t and float(row["conf"]) > 0:
            rows.append((t, int(row["left"]), int(row["top"]), int(row["width"]), int(row["height"]), float(row["conf"])))
    return rows
def run(p):
    sid = f"VGT-{p:02d}"; out = f"ocr_{sid}.json"
    if os.path.exists(out): return
    g = cv2.imread(f"ocr_{sid}.png", cv2.IMREAD_GRAYSCALE)
    H, W = g.shape
    TW, TH, OV = 2400, 1800, 350
    words = []
    for y in range(0, H, TH - OV):
        for x in range(0, W, TW - OV):
            t = g[y:y + TH, x:x + TW]
            if t.size == 0 or (t < 128).mean() < 0.002: continue
            for tx, l, tp, w, h, c in tess(t):
                words.append([tx, (x + l) / W, (y + tp) / H, w / W, h / H, c, 0])
            r = cv2.rotate(t, cv2.ROTATE_90_COUNTERCLOCKWISE); th, tw = t.shape
            for tx, l, tp, w, h, c in tess(r):
                words.append([tx, (x + (tw - tp - h)) / W, (y + l) / H, h / W, w / H, c, 1])
    json.dump(words, open(out, "w"))
    print(sid, len(words), flush=True)
with ThreadPoolExecutor(3) as ex: list(ex.map(run, range(1, 20)))
