import sys, os, subprocess, json
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
sys.path.insert(0, "/home/claude/work")
import ocr as O
k, n = int(sys.argv[1]), int(sys.argv[2])
sizes = {}
for i, (f, p, sid) in enumerate(O.jobs()):
    if i % n != k: continue
    out = f"/home/claude/work/site/img/{sid}.png"
    path = os.path.join(O.SRC, f)
    info = subprocess.check_output(["pdfinfo", "-f", str(p), "-l", str(p), path]).decode()
    line = [l for l in info.splitlines() if "size" in l and f" {p} " in l][0]
    w, h = [float(x) for x in line.split("size:")[1].split()[0:3:2]]
    target = 6000 if sid.startswith("PFD-2539") else 4800
    dpi = target / (max(w, h) / 72) * 1.5
    tmp = f"/tmp/claude-0/i_{sid}"
    subprocess.run(["pdftoppm", "-f", str(p), "-l", str(p), "-r", str(int(dpi)), "-gray", "-singlefile", "-png", path, tmp], check=True)
    im = Image.open(tmp + ".png").convert("L"); im.load(); os.remove(tmp + ".png")
    if im.height > im.width: im = im.rotate(90, expand=True)
    s = target / im.width
    im = im.resize((target, int(im.height * s)), Image.LANCZOS)
    im = im.point(lambda v: 255 if v > 205 else (0 if v < 60 else v)).quantize(colors=8, dither=Image.Dither.NONE)
    im.save(out, optimize=True)
    print(sid, im.size, os.path.getsize(out) // 1024, "KB", flush=True)
