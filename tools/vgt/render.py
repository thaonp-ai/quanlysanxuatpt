import subprocess, os, sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
SRC = "/mnt/user-data/uploads/Vendor Data/10GT9001/PID GT9001.pdf"
def page(p):
    sid = f"VGT-{p:02d}"
    if os.path.exists(f"ocr_{sid}.png") and os.path.exists(f"{sid}.png"): return
    subprocess.run(["pdftoppm", "-f", str(p), "-l", str(p), "-r", "200", "-gray", "-singlefile", "-png", SRC, f"ocr_{sid}"], check=True)
    im = Image.open(f"ocr_{sid}.png").convert("L")
    w = im.resize((4800, int(im.height * 4800 / im.width)), Image.LANCZOS)
    w = w.point(lambda v: 255 if v > 205 else (0 if v < 60 else v)).quantize(colors=8, dither=Image.Dither.NONE)
    w.save(f"{sid}.png", optimize=True)
    print(sid, im.size, w.size, os.path.getsize(f"{sid}.png") // 1024, "KB", flush=True)
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(3) as ex: list(ex.map(page, range(1, 20)))
