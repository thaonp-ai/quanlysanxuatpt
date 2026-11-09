import sys, os, subprocess, json, csv, io, glob
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
SRC = "/mnt/user-data/uploads/PIDvaQLSX"
OUT = "/home/claude/work/ocr"; IMG = "/home/claude/work/site/img"
os.makedirs(OUT, exist_ok=True); os.makedirs(IMG, exist_ok=True)

def jobs():
    J = []
    pid = "02. P&ID Xuong Phu Tro_2025.pdf"
    for p in range(2, 106):
        J.append((pid, p, f"PID-{p:03d}"))
    for f in sorted(os.listdir(SRC)):
        if "PFD" in f:
            n = int(subprocess.check_output(["pdfinfo", os.path.join(SRC, f)]).decode().split("Pages:")[1].split()[0])
            base = f.replace(" Model (1)", "").replace("_1.pdf", "").replace(".pdf", "")
            for p in range(1, n + 1):
                J.append((f, p, f"PFD-{base}-p{p}"))
    return J

def ocr(im):
    r = subprocess.run(["tesseract", "stdin", "stdout", "--psm", "11", "-l", "eng", "tsv"],
                       input=im, capture_output=True)
    rows = []
    for row in csv.DictReader(io.StringIO(r.stdout.decode("utf8", "ignore")), delimiter="\t", quoting=csv.QUOTE_NONE):
        t = (row.get("text") or "").strip()
        if t and float(row["conf"]) > 0:
            rows.append([t, int(row["left"]), int(row["top"]), int(row["width"]), int(row["height"]), float(row["conf"])])
    return rows

def png(im):
    b = io.BytesIO(); im.save(b, "PNG"); return b.getvalue()

def run(job):
    f, p, sid = job
    if os.path.exists(f"{OUT}/{sid}.json"): return
    path = os.path.join(SRC, f)
    sz = subprocess.check_output(["pdfinfo", "-f", str(p), "-l", str(p), path]).decode()
    line = [l for l in sz.splitlines() if l.startswith(f"Page") and "size" in l and f" {p} " in l][0]
    w, h = [float(x) for x in line.split("size:")[1].split()[0:3:2]]
    dpi = int(min(600, 9000 / (max(w, h) / 72)))
    tmp = f"/tmp/claude-0/r_{sid}"
    subprocess.run(["pdftoppm", "-f", str(p), "-l", str(p), "-r", str(dpi), "-gray", "-singlefile", "-png", path, tmp], check=True)
    im = Image.open(tmp + ".png"); im.load(); os.remove(tmp + ".png")
    if im.height > im.width:
        im = im.rotate(90, expand=True)  # landscape; fixed later by OSD check if needed
    W, H = im.size
    words = [[t, x / W, y / H, ww / W, hh / H, c, 0] for t, x, y, ww, hh, c in ocr(png(im))]
    r = im.rotate(90, expand=True)  # rotate CCW: text running bottom->top becomes horizontal
    for t, x, y, ww, hh, c in ocr(png(r)):
        # rotated image size (H, W); point (x', y') in rotated -> original (W - y' , x')... for CCW 90: x' = y, y' = W - x
        ox, oy = W - (y + hh), x
        words.append([t, ox / W, oy / H, hh / W, ww / H, c, 1])
    # web image: 1-bit-ish png, long side 3300
    s = 3300 / W
    web = im.resize((3300, int(H * s)), Image.LANCZOS).point(lambda v: 255 if v > 170 else 0).convert("1")
    web.save(f"{IMG}/{sid}.png", optimize=True)
    json.dump({"id": sid, "file": f, "page": p, "w": web.width, "h": web.height, "words": words}, open(f"{OUT}/{sid}.json", "w"))
    print(sid, len(words), flush=True)

if __name__ == "__main__":
    k, n = int(sys.argv[1]), int(sys.argv[2])
    for i, j in enumerate(jobs()):
        if i % n == k: run(j)
