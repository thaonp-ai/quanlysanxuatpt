import sys, os, subprocess, json, csv, io, glob
import numpy as np, cv2
sys.path.insert(0, '/home/claude/work')
import ring
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
SRC = "/mnt/user-data/uploads/PIDvaQLSX"
OUT = "/home/claude/work/bub2"; os.makedirs(OUT, exist_ok=True)

def render(f, p):
    path = os.path.join(SRC, f)
    info = subprocess.check_output(["pdfinfo", "-f", str(p), "-l", str(p), path]).decode()
    line = [l for l in info.splitlines() if "size" in l and f" {p} " in l][0]
    w, h = [float(x) for x in line.split("size:")[1].split()[0:3:2]]
    dpi = int(min(800, 13000 / (max(w, h) / 72)))
    tmp = f"/tmp/claude-0/b_{os.getpid()}"
    subprocess.run(["pdftoppm", "-f", str(p), "-l", str(p), "-r", str(dpi), "-gray", "-singlefile", "-png", path, tmp], check=True)
    im = Image.open(tmp + ".png"); im.load(); os.remove(tmp + ".png")
    if im.height > im.width: im = im.rotate(90, expand=True)
    return np.array(im.convert("L"))

def detect(g):
    H, W = g.shape
    bw = (g < 140).astype(np.uint8) * 255
    items = []
    # circles
    small = cv2.resize(g, (W // 2, H // 2), interpolation=cv2.INTER_AREA)
    sm = cv2.medianBlur(small, 3)
    r0 = W / 2
    cs = cv2.HoughCircles(sm, cv2.HOUGH_GRADIENT, dp=1, minDist=int(r0 * 0.006), param1=120, param2=28,
                          minRadius=int(r0 * 0.0028), maxRadius=int(r0 * 0.0075))
    if cs is not None:
        for x, y, r in cs[0]:
            x, y, r = x * 2, y * 2, r * 2
            # verify ring: fraction of dark pixels on circumference
            ang = np.linspace(0, 2 * np.pi, 72, endpoint=False)
            px = (x + r * np.cos(ang)).astype(int).clip(0, W - 1); py = (y + r * np.sin(ang)).astype(int).clip(0, H - 1)
            ring = 0
            for d in (-3, -1, 0, 1, 3):
                pass
            hits = sum(1 for a, b in zip(px, py) if bw[max(0, b - 3):b + 4, max(0, a - 3):a + 4].any())
            if hits / 72 < 0.8: continue
            if x > W * 0.835: continue
            s = r * 1.0
            items.append(("c", int(x - s), int(y - s), int(2 * s), int(2 * s), float(r)))
    # small boxes (block valve tags): white interior components of rectangles
    n, lab, st, _ = cv2.connectedComponentsWithStats(255 - bw, connectivity=4)
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if W * 0.0022 < h < W * 0.006 and 1.8 < w / h < 4.8 and x < W * 0.835 and a > 0.4 * w * h:
            items.append(("b", int(x), int(y), int(w), int(h), 0.0))
    return items

def clean(crop, box=False):
    bw = (crop < 140).astype(np.uint8) * 255
    h, w = bw.shape
    # remove horizontal divider lines
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (max(10, int(w * 0.55)), 1))
    lines = cv2.morphologyEx(bw, cv2.MORPH_OPEN, k)
    bw = cv2.subtract(bw, lines)
    if not box:
        k = cv2.getStructuringElement(cv2.MORPH_RECT, (1, max(10, int(h * 0.8))))
        bw = cv2.subtract(bw, cv2.morphologyEx(bw, cv2.MORPH_OPEN, k))
    return 255 - bw

def run(job):
    f, p, sid = job
    if os.path.exists(f"{OUT}/{sid}.json"): return
    g = render(f, p)
    H, W = g.shape
    items = [it for it in detect(g) if it[1] > 0 and it[2] > 0]
    CW, CH = 400, 320
    cells = []
    NUMS = []
    for it in items:
        k, x, y, w, h, r = it
        crop = g[y:y + h, x:x + w].copy()
        nums = None
        if k == "c":
            big, bcx, bcy, br = ring.refine(g, x, y, w, h, r)
            e, st = ring.erase_ring(big, bcx, bcy, br)
            e = cv2.morphologyEx(e, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
            crop = e[int(max(0, bcy - br)):int(bcy + br), int(max(0, bcx - br)):int(bcx + br)]
            lo = crop[int(br * 1.05):int(br * 1.85), :]
            if lo.size:
                lo = cv2.copyMakeBorder(cv2.resize(lo, None, fx=1.5, fy=1.5), 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=255)
                ok_, bb = cv2.imencode(".png", lo)
                nums = subprocess.run(["tesseract", "stdin", "stdout", "--psm", "7", "-c", "tessedit_char_whitelist=0123456789ABCD/"],
                                      input=bb.tobytes(), capture_output=True).stdout.decode().strip()
            h, w = crop.shape
            NUMS.append(nums)
            cells.append(cv2.resize(crop, (max(1, int(w * min(200 / max(w, 1), 160 / max(h, 1), 3))), max(1, int(h * min(200 / max(w, 1), 160 / max(h, 1), 3)))), interpolation=cv2.INTER_CUBIC))
            continue
        NUMS.append(None)
        crop = clean(crop, k == 'b')
        sc = min(200 / max(w, 1), 160 / max(h, 1), 3)
        crop = cv2.resize(crop, (max(1, int(w * sc)), max(1, int(h * sc))), interpolation=cv2.INTER_CUBIC)
        cells.append(crop)
    res = []
    B = 400
    for s in range(0, len(cells), B):
        chunk = cells[s:s + B]
        cols = 8
        rows = (len(chunk) + cols - 1) // cols
        mont = np.full((rows * CH, cols * CW), 255, np.uint8)
        for i, c in enumerate(chunk):
            r_, c_ = divmod(i, cols)
            y0 = r_ * CH + (CH - c.shape[0]) // 2; x0 = c_ * CW + (CW - c.shape[1]) // 2
            mont[y0:y0 + c.shape[0], x0:x0 + c.shape[1]] = c
        texts = [[] for _ in chunk]
        kinds = [items[s + i][0] for i in range(len(chunk))]
        for wl, keep in (("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/", "c"), ("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-/", "b")):
          m2 = mont.copy()
          for i in range(len(chunk)):
            if kinds[i] != keep:
                r_, c_ = divmod(i, cols); m2[r_ * CH:(r_ + 1) * CH, c_ * CW:(c_ + 1) * CW] = 255
          ok, buf = cv2.imencode(".png", m2)
          out = subprocess.run(["tesseract", "stdin", "stdout", "--psm", "11", "-l", "eng",
                              "-c", "tessedit_char_whitelist=" + wl, "tsv"],
                             input=buf.tobytes(), capture_output=True).stdout.decode()
          for row in csv.DictReader(io.StringIO(out), delimiter="\t", quoting=csv.QUOTE_NONE):
            t = (row.get("text") or "").strip()
            if not t: continue
            cx = int(row["left"]) + int(row["width"]) // 2; cy = int(row["top"]) + int(row["height"]) // 2
            i = (cy // CH) * cols + cx // CW
            if 0 <= i < len(chunk) and kinds[i] == keep: texts[i].append((int(row["top"]), int(row["left"]), t, float(row["conf"])))
        out = ""
        for row in csv.DictReader(io.StringIO(out), delimiter="\t", quoting=csv.QUOTE_NONE):
            t = (row.get("text") or "").strip()
            if not t: continue
            cx = int(row["left"]) + int(row["width"]) // 2; cy = int(row["top"]) + int(row["height"]) // 2
            i = (cy // CH) * cols + cx // CW
            if 0 <= i < len(chunk): texts[i].append((int(row["top"]), int(row["left"]), t, float(row["conf"])))
        for i, tx in enumerate(texts):
            k, x, y, w, h, r = items[s + i]
            tx.sort()
            res.append({"num": NUMS[s + i], "k": k, "x": x / W, "y": y / H, "w": w / W, "h": h / H, "t": [t for _, _, t, _ in tx], "c": [c for *_, c in tx]})
    json.dump({"id": sid, "items": res}, open(f"{OUT}/{sid}.json", "w"))
    print(sid, len(res), flush=True)

if __name__ == "__main__":
    sys.path.insert(0, "/home/claude/work")
    import ocr
    k, n = int(sys.argv[1]), int(sys.argv[2])
    only = sys.argv[3] if len(sys.argv) > 3 else None
    for i, j in enumerate(ocr.jobs()):
        if only and j[2] != only: continue
        if only or i % n == k: run(j)
