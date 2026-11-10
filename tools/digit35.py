import numpy as np, cv2
def number_cells(c, digits="0000000"):
    """c: grayscale horizontal crop of a line number. Returns list of 7 digit-cell images of the line-number field or None."""
    bw = (c < 140).astype(np.uint8)
    rows = np.where(bw.sum(1) > 0)[0]
    if len(rows) == 0: return None
    # remove long horizontal rules (underline / pipe)
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (max(15, int(c.shape[1] * 0.5)), 1))
    bw = cv2.subtract(bw, cv2.morphologyEx(bw, cv2.MORPH_OPEN, k))
    prof = bw.sum(1)
    rr = np.where(prof > bw.shape[1] * 0.02)[0]
    if len(rr) == 0: return None
    # text band = largest contiguous block of inked rows
    blocks = np.split(rr, np.where(np.diff(rr) > 2)[0] + 1)
    band = max(blocks, key=len)
    y0, y1 = band[0], band[-1] + 1
    th = y1 - y0
    t = bw[y0:y1]
    top = t[: int(th * 0.3)].sum(0) > 0
    bot = t[int(th * 0.7):].sum(0) > 0
    mid = t.sum(0) > 0
    glyph = top | bot
    # dash runs: middle ink but no top/bottom ink, long enough
    segs = []; cur = None; dash = 0
    for x in range(t.shape[1]):
        if glyph[x]:
            if cur is None: cur = [x, x]
            elif dash > th * 0.35 or (x - cur[1]) > th * 0.6:
                segs.append(cur); cur = [x, x]
            cur[1] = x; dash = 0
        elif mid[x]: dash += 1
    if cur: segs.append(cur)
    if len(segs) < 4: return None, segs, (y0, y1)
    nx0, nx1 = segs[-3]
    w = (nx1 - nx0 + 1) / 7
    if not (0.35 * th < w < 1.0 * th): return None, segs, (y0, y1)
    seg = t[:, nx0:nx1 + 1]
    ink = seg.sum(0) > 0
    pieces = []; st = None
    for x, v in enumerate(ink):
        if v and st is None: st = x
        if not v and st is not None: pieces.append((st, x)); st = None
    if st is not None: pieces.append((st, len(ink)))
    pieces = [p for p in pieces if p[1] - p[0] > th * 0.12]
    if len(pieces) == 7:
        return [seg[:, a:b] for a, b in pieces], segs, (y0, y1)
    wts = [0.6 if ch == "1" else 1.0 for ch in digits]
    tot = sum(wts); span = nx1 - nx0 + 1
    edges = [nx0 + span * sum(wts[:i]) / tot for i in range(8)]
    colsum = t.sum(0)
    aw = span / 7
    for i in range(1, 7):
        lo, hi = int(edges[i] - aw * 0.35), int(edges[i] + aw * 0.35) + 1
        lo = max(lo, int(edges[i - 1]) + 2); hi = min(hi, nx1)
        if hi > lo: edges[i] = lo + int(colsum[lo:hi].argmin())
    cells = []
    for i in range(7):
        a, b = int(edges[i]), int(edges[i + 1] + 0.5)
        cols = np.where(t[:, a:b].sum(0) > 0)[0]
        if len(cols): a, b = a + cols[0], a + cols[-1] + 1
        cells.append(t[:, a:b])
    return cells, segs, (y0, y1)
def is5(cell):
    h, w = cell.shape
    r = cell[int(h * 0.12):int(h * 0.42), :max(1, int(w * 0.3))]
    return r.mean()

W_CH = {"1": 0.55, "/": 0.6, "I": 0.45, "J": 0.85, "M": 1.15, "W": 1.2}

def segments(c):
    bw = (c < 140).astype(np.uint8)
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (max(15, int(c.shape[1] * 0.5)), 1))
    bw = cv2.subtract(bw, cv2.morphologyEx(bw, cv2.MORPH_OPEN, k))
    prof = bw.sum(1)
    rr = np.where(prof > bw.shape[1] * 0.02)[0]
    if len(rr) == 0: return None, None, None
    blocks = np.split(rr, np.where(np.diff(rr) > 2)[0] + 1)
    band = max(blocks, key=len)
    y0, y1 = band[0], band[-1] + 1
    th = y1 - y0
    t = bw[y0:y1]
    top = t[: int(th * 0.3)].sum(0) > 0
    bot = t[int(th * 0.7):].sum(0) > 0
    mid = t.sum(0) > 0
    glyph = top | bot
    segs = []; cur = None; dash = 0
    for x in range(t.shape[1]):
        if glyph[x]:
            if cur is None: cur = [x, x]
            elif dash > th * 0.35 or (x - cur[1]) > th * 0.6:
                segs.append(cur); cur = [x, x]
            cur[1] = x; dash = 0
        elif mid[x]: dash += 1
    if cur: segs.append(cur)
    return t, segs, th

def field_cells(t, seg, chars, th):
    nx0, nx1 = seg
    wts = [W_CH.get(ch, 1.0) for ch in chars]
    tot = sum(wts); span = nx1 - nx0 + 1
    aw = span / len(chars)
    if not (0.3 * th < aw < 1.1 * th): return None
    edges = [nx0 + span * sum(wts[:i]) / tot for i in range(len(chars) + 1)]
    colsum = t.sum(0)
    for i in range(1, len(chars)):
        lo, hi = int(edges[i] - aw * 0.35), int(edges[i] + aw * 0.35) + 1
        lo = max(lo, int(edges[i - 1]) + 2); hi = min(hi, nx1)
        if hi > lo: edges[i] = lo + int(colsum[lo:hi].argmin())
    cells = []
    for i in range(len(chars)):
        a, b = int(edges[i]), int(edges[i + 1] + 0.5)
        cols = np.where(t[:, a:b].sum(0) > 0)[0]
        if len(cols): a, b = a + cols[0], a + cols[-1] + 1
        cells.append(t[:, a:b])
    return cells

def decide35(cell):
    """'5' / '3' / None (undecided) from the upper-left vertical stroke of a '5'."""
    if cell.size == 0: return None
    h, w = cell.shape
    if not (0.5 * h <= w <= 0.95 * h): return None   # cell not cleanly isolated
    band = cell[int(h * 0.15):int(h * 0.42), :max(1, int(w * 0.28))]
    rows = (band.sum(1) > 0).mean()
    if rows >= 0.97 and band.mean() >= 0.2: return "5"
    if rows <= 0.5: return "3"
    return None
