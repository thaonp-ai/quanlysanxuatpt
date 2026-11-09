import numpy as np, cv2
def refine(g, x, y, w, h, r):
    pad = int(r * 0.3)
    X0, Y0 = max(0, x - pad), max(0, y - pad)
    big = g[Y0:y + h + pad, X0:x + w + pad].copy()
    dark = big < 140
    ang = np.linspace(0, 2 * np.pi, 180, endpoint=False); ca, sa = np.cos(ang), np.sin(ang)
    cx0, cy0 = x + w / 2 - X0, y + h / 2 - Y0
    best = (-1, cx0, cy0, r)
    for dr in np.arange(-0.15, 0.16, 0.03) * r:
        for dx in range(-10, 11, 2):
            for dy in range(-10, 11, 2):
                rr = r + dr
                px = (cx0 + dx + rr * ca).astype(int); py = (cy0 + dy + rr * sa).astype(int)
                ok = (px >= 0) & (py >= 0) & (px < big.shape[1]) & (py < big.shape[0])
                s = dark[py[ok], px[ok]].sum()
                if s > best[0]: best = (s, cx0 + dx, cy0 + dy, rr)
    return big, best[1], best[2], best[3]

def erase_ring(big, cx, cy, R):
    dark = big < 140
    H, W = big.shape
    # estimate stroke: median dark run length across the ring
    runs = []
    angs = np.linspace(0, 2 * np.pi, 720, endpoint=False)
    rad = np.arange(R * 0.75, R * 1.3, 0.5)
    prof = []
    for a in angs:
        px = (cx + rad * np.cos(a)).astype(int).clip(0, W - 1); py = (cy + rad * np.sin(a)).astype(int).clip(0, H - 1)
        prof.append((px, py, dark[py, px]))
    lens = []
    for px, py, d in prof:
        i = np.argmin(np.abs(rad - R))
        if not d[i]: lens.append(None); continue
        a = i
        while a > 0 and d[a - 1]: a -= 1
        b = i
        while b < len(d) - 1 and d[b + 1]: b += 1
        lens.append((a, b))
    L = [(b - a) for v in lens if v for a, b in [v]]
    st = np.median(L) if L else 6
    out = big.copy()
    for (px, py, d), v in zip(prof, lens):
        if not v: continue
        a, b = v
        if (b - a) <= st * 1.5:
            out[py[a:b + 1], px[a:b + 1]] = 255
            # also clear 1px neighbourhood
            out[np.clip(py[a:b + 1] + 1, 0, H - 1), px[a:b + 1]] = np.maximum(out[np.clip(py[a:b + 1] + 1, 0, H - 1), px[a:b + 1]], 0)
    # clear everything outside ring
    yy, xx = np.mgrid[0:H, 0:W]
    out[np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) > R + st] = 255
    return out, st
