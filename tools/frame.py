import json, sys, os, glob
import numpy as np, cv2
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
sys.path.insert(0, "/home/claude/work")
import ocr as O

def long_lines(bw, axis, frac):
    H, W = bw.shape
    if axis == "v":
        k = cv2.getStructuringElement(cv2.MORPH_RECT, (1, int(H * frac)))
        m = cv2.morphologyEx(bw, cv2.MORPH_OPEN, k)
        prof = (m > 0).sum(axis=0)
        idx = np.where(prof > H * frac)[0]
    else:
        k = cv2.getStructuringElement(cv2.MORPH_RECT, (int(W * frac), 1))
        m = cv2.morphologyEx(bw, cv2.MORPH_OPEN, k)
        prof = (m > 0).sum(axis=1)
        idx = np.where(prof > W * frac)[0]
    # group consecutive indices
    groups = []
    for i in idx:
        if groups and i - groups[-1][-1] <= 3: groups[-1].append(i)
        else: groups.append([i])
    return [int(np.mean(g)) for g in groups]

def frame(sid):
    g = np.array(Image.open(f"/home/claude/work/site/img/{sid}.png").convert("L"))
    H, W = g.shape
    bw = (g < 128).astype(np.uint8) * 255
    vs = long_lines(bw, "v", 0.55)
    hs = long_lines(bw, "h", 0.45)
    # left: first vertical line after the outer border region (x < 0.1W); take the rightmost one in that zone
    left = [x for x in vs if x < W * 0.1]
    right = [x for x in vs if W * 0.6 < x < W * 0.97]
    top = [y for y in hs if y < H * 0.12]
    bot = [y for y in hs if y > H * 0.85]
    x0 = max(left) if left else int(W * 0.012)
    # right edge of the main area = leftmost long vertical line in the right zone (notes / title column separator)
    x1 = min(right) if right else int(W * 0.835)
    y0 = max(top) if top else int(H * 0.012)
    y1 = min(bot) if bot else int(H * 0.972)
    return {"x0": x0 / W, "y0": y0 / H, "x1": x1 / W, "y1": y1 / H, "vs": [round(v / W, 3) for v in vs], "hs": [round(v / H, 3) for v in hs]}

if __name__ == "__main__":
    out = {}
    for f, p, sid in O.jobs():
        out[sid] = frame(sid)
        print(sid, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in out[sid].items()}, flush=True)
    json.dump(out, open("/home/claude/work/frames.json", "w"))
