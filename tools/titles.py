import json, glob, subprocess, os, sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
SRC = "/mnt/user-data/uploads/PIDvaQLSX"
out = {}
k, n = int(sys.argv[1]), int(sys.argv[2])
sys.path.insert(0, "/home/claude/work")
import ocr as O
for i, (fn, pg, sid) in enumerate(O.jobs()):
    if i % n != k or os.path.exists(f"/home/claude/work/tb/{sid}.json"): continue
    d = {"id": sid, "file": fn, "page": pg}
    path = os.path.join(SRC, d["file"])
    info = subprocess.check_output(["pdfinfo", "-f", str(d["page"]), "-l", str(d["page"]), path]).decode()
    line = [l for l in info.splitlines() if "size" in l and f" {d['page']} " in l][0]
    w, h = [float(x) for x in line.split("size:")[1].split()[0:3:2]]
    dpi = int(min(500, 9000 / (max(w, h) / 72)))
    tmp = f"/tmp/claude-0/t_{d['id']}"
    subprocess.run(["pdftoppm", "-f", str(d["page"]), "-l", str(d["page"]), "-r", str(dpi), "-gray", "-singlefile", "-png", path, tmp], check=True)
    im = Image.open(tmp + ".png"); im.load(); os.remove(tmp + ".png")
    if im.height > im.width: im = im.rotate(90, expand=True)
    W, H = im.size
    tb = im.crop((int(W * 0.82), int(H * 0.80), W, H))
    tb.save(f"/home/claude/work/tb/{d['id']}.png")
    txt = subprocess.run(["tesseract", f"/home/claude/work/tb/{d['id']}.png", "stdout", "--psm", "6", "-l", "eng"], capture_output=True).stdout.decode()
    json.dump({"id": d["id"], "text": txt}, open(f"/home/claude/work/tb/{d['id']}.json", "w"))
    print(d["id"], flush=True)
