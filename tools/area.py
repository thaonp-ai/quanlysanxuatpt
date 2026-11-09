import json, numpy as np, cv2
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = None
F = json.load(open('/home/claude/work/frames_final.json'))
def area(sid):
    f = F[sid]
    g = np.array(Image.open(f'/home/claude/work/site/img/{sid}.png').convert('L'))
    H, W = g.shape
    bw = (g < 128).astype(np.uint8) * 255
    m = 0.006
    X0, Y0, X1, Y1 = int((f['x0'] + m) * W), int((f['y0'] + m) * H), int((f['x1'] - m) * W), int((f['y1'] - m) * H)
    sub = bw[Y0:Y1, X0:X1]
    hl = cv2.morphologyEx(sub, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (int(W * 0.10), 1)))
    vl = cv2.morphologyEx(sub, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (1, int(H * 0.08))))
    L = cv2.bitwise_or(hl, vl)
    ys, xs = np.nonzero(L)
    if len(xs) < 50:
        return dict(f)
    # robust bounds: ignore extreme 0.1% pixels
    x_lo, x_hi = np.percentile(xs, [0.05, 99.95]); y_lo, y_hi = np.percentile(ys, [0.05, 99.95])
    mx, my = 0.012, 0.018
    return dict(x0=max(f['x0'], (x_lo + X0) / W - mx), y0=max(f['y0'], (y_lo + Y0) / H - my),
                x1=min(f['x1'], (x_hi + X0) / W + mx), y1=min(f['y1'], (y_hi + Y0) / H + my))
if __name__ == '__main__':
    out = {s: area(s) for s in F}
    json.dump(out, open('/home/claude/work/areas.json', 'w'), indent=0)
    ims = []
    for s in ['PID-024', 'PID-023', 'PID-035', 'PID-061', 'PID-094', 'PID-105', 'PFD-2539-31-PFD-0010-01-01-p1', 'PFD-2098-41-PFD-0010-1-2-p1', 'PID-046']:
        im = Image.open(f'/home/claude/work/site/img/{s}.png').convert('RGB'); W, H = im.size
        d = ImageDraw.Draw(im)
        for k, c in ((F[s], (0, 0, 255)), (out[s], (255, 0, 0))):
            d.rectangle([k['x0'] * W, k['y0'] * H, k['x1'] * W, k['y1'] * H], outline=c, width=14)
        ims.append(im.resize((660, int(660 * H / W))))
    canvas = Image.new('RGB', (1980, 3 * 480), 'white')
    for i, im in enumerate(ims): canvas.paste(im, ((i % 3) * 660, (i // 3) * 480))
    canvas.save('/home/claude/work/r/areas.png')
