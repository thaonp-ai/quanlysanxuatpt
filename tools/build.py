import json, glob, re, os, collections, sys
sys.path.insert(0, "/home/claude/work")
import parse as P, ocr as O

UNIT_NAMES = json.load(open("/home/claude/work/units.json"))   # code -> name
SHEETFIX = json.load(open("/home/claude/work/sheetfix.json")) if os.path.exists("/home/claude/work/sheetfix.json") else {}

def title_info(sid, kind):
    tb = json.load(open(f"/home/claude/work/tb/{sid}.json"))["text"]
    lines = [l.strip(" |_[]{}!'\"") for l in tb.splitlines()]
    flat = " ".join(lines)
    proj = unit = serial = None
    m = re.search(r"(2098|2539)\s+(\d{2})\s+(PID|PFD)\s+(\d{4})\s*[-—~]?\s*([0-9A-Z]{2})?", flat)
    if m: proj, unit, serial = m.group(1), m.group(2), m.group(5)
    # title lines: after the "PLANT" line, before the "Section"/scale line
    t = []
    try:
        st = max(i for i, l in enumerate(lines) if "FERTILIZER PLANT" in l.upper() or "FERTILIZER PROJECT" in l.upper())
        for l in lines[st + 1:]:
            if re.search(r"NONE|Scale|Section|2098|2539", l, re.I): break
            l = re.sub(r"^[^A-Z0-9(]+|[^A-Z0-9)]+$", "", l.upper())
            l = re.sub(r"\s+[A-Z0-9]{1,2}$", "", l).strip()
            if len(l) > 3 and sum(c.isalpha() for c in l) > len(l) * 0.6 and l not in ("ENGINEERING", "TECHNIP"): t.append(l)
    except ValueError:
        pass
    return proj, unit, serial, " – ".join(t[:3])

VFN = re.compile(r"(PSV|PCV|FCV|LCV|TCV|PDV|SDV|MOV|BDV|HCV|TSV|PRV|PV|FV|LV|TV|HV|XV|UV|KV)$")

AREAS = json.load(open("/home/claude/work/areas_final.json"))
DESC = re.compile(r"^(TANK|TANKS|PUMP|PUMPS|MOTOR|MOTORS|COOLER|PACKAGE|AGITATOR|DRUM|VESSEL|FILTER|FILTERS|HEATER|COMPRESSOR|TURBINE|BLOWER|SEPARATOR|EXCHANGER|BASIN|TOWER|DEAERATOR|BOILER|SKID|SILENCER|EJECTOR|STRAINER|RECEIVER|DRYER|DRIER|MIXER|CLARIFIER|PIT|SUMP|CONDENSER|SCRUBBER|STRIPPER|COLUMN|STACK|FLARE|GENERATOR|FAN|DOSING|STORAGE|SOLUTION|TRANSFER|UNLOADING|LOADING|DEMINERALIZED|DEIONIZED|WATER|FOR)$")

FRAMES = json.load(open("/home/claude/work/frames_final.json"))
TABLEW = re.compile(r"^(TYPE|CAPACITY|DESIGN|SPEED|DIMENSION|DIMENSIONS|VOLUME|D\.?P\.?|D\.?T\.?|DUTY|SPECIFICATION|POWER|THICK\.?|INSULATION|RATED|RETENTION|NPSH)$")

def header_bottom(sid, words):
    fy0 = FRAMES[sid]["y0"]
    ys = []
    for wd in words:
        if wd[6] != 0 or wd[2] > 0.30 or wd[2] < fy0: continue
        if TABLEW.match(P.norm(wd[0])): ys.append(wd[2] + wd[4])
    eq = [t for t in P.extract({"words": words, "unit": ""}, None) if t[1] == "equipment" and t[4] < 0.30]
    for t in eq:
        if header_title(words, t): ys.append(t[4] + t[6] * 4)
    ys.sort()
    if len(ys) < 2 or ys[0] > 0.15: return fy0
    bottom = ys[0]
    for y in ys[1:]:
        if y - bottom > 0.07: break
        bottom = y
    return bottom + 0.006

HEADBOX = {}
INCLUDE_HEADER_ONLY = False   # user: list only equipment drawn in the main process area

REFW = re.compile(r"^\(?(FROM|FRM|FR|TO|FOR|SEE|VIA|EX)[.:]?$")

def is_reference(t, words):
    tag, typ, sub, x, y, w, h = t[:7]
    vert = h > w * 1.5
    th = w if vert else h
    for wd in words:
        tx = P.norm(wd[0])
        # "FROM" glued to the tag in one OCR word
        if wd[6] == (1 if vert else 0) and re.match(r"^\(?(FROM|TO|FOR)\d", tx) and abs(wd[1] - x) < th * 1.5 and abs(wd[2] - y) < th * 1.5:
            return True
        if not vert and wd[6] == 0 and abs((wd[2] + wd[4] / 2) - (y + h / 2)) < th * 0.8:
            gap = x - (wd[1] + wd[3])
            # "...TO" glued to the word before ("PRESSURIZATIONTO 10-T3002")
            if -th * 0.5 < gap < th * 2 and len(tx) > 6 and re.search(r"(TO|FROM)$", tx) and not re.search(r"AUTO$", tx): return True
            # signal / logic text after the tag ("30-P1003B STOP", "40-PK2001/P1A/B START", "... SPEED CONTROL")
            g2 = wd[1] - (x + w)
            if -th * 0.5 < g2 < th * 2.5 and re.match(r"^:?(START|STOP|SPEED|RUN|TRIP|RESET)", tx): return True
        if not REFW.match(tx): continue
        if vert:
            if wd[6] != 1: continue
            gap = wd[2] - (y + h)          # vertical text reads bottom->top: the word before is below
            if -th * 0.5 < gap < th * 4 and abs((wd[1] + wd[3] / 2) - (x + w / 2)) < th * 0.8: return True
        else:
            if wd[6] != 0: continue
            gap = x - (wd[1] + wd[3])
            if -th * 0.5 < gap < th * 4 and abs((wd[2] + wd[4] / 2) - (y + h / 2)) < th * 0.8: return True
    return False

PIPE_SIZES = {"1/2", "3/4", "1", "1-1/4", "1-1/2", "2", "2-1/2", "3", "4", "5", "6", "8", "10", "12", "14", "16", "18", "20",
              "22", "24", "26", "28", "30", "32", "34", "36", "40", "42", "44", "48", "52", "54", "56", "60", "64", "66", "72", "80"}

def pick_size(cur, votes):
    """New pipe size from the wide-crop re-read, or None to keep the current one.
    A truncated reading only ever loses leading characters, so a longer reading that ends with the
    shorter one wins as soon as it is seen at all."""
    v = {s: n for s, n in votes.items() if s in PIPE_SIZES}
    if not v: return None
    longest = max(v, key=len)
    if all(longest.endswith(s) for s in v) and (cur != longest) and (longest.endswith(cur) or cur not in PIPE_SIZES):
        return longest
    top, n = max(v.items(), key=lambda kv: kv[1])
    if top != cur and n >= 2 and cur not in PIPE_SIZES: return top
    if top != cur and n >= 3 and not cur.endswith(top): return top
    return None

def _overlap(a, b):
    ax0, ay0, ax1, ay1 = a[3], a[4], a[3] + a[5], a[4] + a[6]
    bx0, by0, bx1, by1 = b[3], b[4], b[3] + b[5], b[4] + b[6]
    iw = min(ax1, bx1) - max(ax0, bx0); ih = min(ay1, by1) - max(ay0, by0)
    if iw <= 0 or ih <= 0: return False
    return iw * ih > 0.3 * min(a[5] * a[6], b[5] * b[6])

def expand(tag):
    parts = tag.split("/")
    if len(parts) == 1: return {tag}
    out = []
    head = parts[0]
    cur = head
    items = [head] if not all(len(p) == 1 for p in parts[1:]) else [head]
    for p in parts[1:]:
        if len(p) == 1 and p.isalpha():
            prev = items[-1]
            items.append(prev[:-1] + p)
        else:
            items.append(head + "/" + p)
    if any(len(p) > 1 for p in parts[1:]):
        items = [i for i in items if i != head]
    return set(items)

CONF = {frozenset(p) for p in ["35", "38", "56", "8B", "0O", "1I", "1L", "5S", "2Z", "0D", "08", "68", "IL"]}

CANON = str.maketrans({"S": "3", "5": "3", "B": "8", "O": "0", "I": "1", "L": "1", "Z": "2", "G": "6"})

def near_dup(a, b):
    """Same label read two ways (3/5/S, 8/B, 0/O ... or one stray character)."""
    ca, cb = a.translate(CANON), b.translate(CANON)
    if ca == cb: return True
    if abs(len(ca) - len(cb)) == 1:
        s, l = (ca, cb) if len(ca) < len(cb) else (cb, ca)
        return any(l[:i] + l[i + 1:] == s for i in range(len(l)))
    return False

def lev1(a, b):
    if len(a) != len(b): return False
    diff = [(x, y) for x, y in zip(a, b) if x != y]
    return len(diff) == 1 and frozenset(diff[0]) in CONF

def header_tags(sid, cands_all):
    H = set()
    for t, s in cands_all:
        if t[1] != "equipment": continue
        cx, cy = t[3] + t[5] / 2, t[4] + t[6] / 2
        if any(b[0] <= cx <= b[2] and b[1] <= cy <= b[3] for b in HEADBOX.get(sid, [])):
            H |= expand(t[0])
    return H

FIXLOG = []
HDRS = {}
HDRPOS = {}   # equipment name -> [(P&ID sheet, header label)]

def resolve(cands):
    """Readings of the same label from both OCR passes overlap: keep one per label.
    Prefer the high-resolution pass, then the longest (most complete) tag, then confidence."""
    cands = sorted(cands, key=lambda c: (-c[1], -len(c[0][0]), -c[0][7]))
    kept = []
    for t, s in cands:
        if any(k[1] == t[1] and _overlap(k, t) for k in kept): continue
        kept.append(t)
    return kept

HEADFIX = {"PID-045": 0.2}
EXCL = json.load(open("/home/claude/work/exclude.json")) if os.path.exists("/home/claude/work/exclude.json") else []
LINE_TOP = json.load(open("/home/claude/work/areas_final.json"))
STOPW = {"FROM", "TO", "FOR", "NOTE", "SEE", "DWG", "AND", "THE", "WITH", "VIA", "SH", "TYP", "LO", "LC", "NC", "NO"}

def described(words, t):
    """an equipment tag with a line of plain description words right below it (e.g. 'OIL DEGASSING POT')"""
    tag, typ, sub, x, y, w, h = t[:7]
    cx = x + w / 2
    for wd in words:
        if wd[6] != 0: continue
        tx = P.norm(wd[0])
        if len(tx) < 3 or not tx.isalpha() or tx in STOPW: continue
        if 0 < wd[2] - (y + h) < h * 2.2 and abs(wd[1] + wd[3] / 2 - cx) < max(w * 0.9, 0.03): return True
    return False

def header_boxes(sid, words):
    """Rectangles covering the equipment title/data blocks along the top edge of the sheet.
    Title rows (tag + description) must sit at the top edge; data-table keywords only count
    directly beneath those titles, so nothing inside the process diagram is swallowed."""
    fy0 = FRAMES[sid]["y0"]
    eqs = [t for t in P.extract({"words": words, "unit": ""}, None) if t[1] == "equipment" and fy0 <= t[4] < 0.32]
    top_titles = [t for t in eqs if t[4] < fy0 + 0.06 and (header_title(words, t) or described(words, t))]
    more_titles = [t for t in eqs if t[4] >= fy0 + 0.06 and header_title(words, t)]
    kws = [wd for wd in words if wd[6] == 0 and fy0 <= wd[2] < 0.32 and TABLEW.match(P.norm(wd[0]))]
    items = [(t[4], [t[3], t[4], t[3] + t[5], t[4] + t[6] * 4]) for t in top_titles + more_titles] + \
            [(k[2], [k[1], k[2], k[1] + k[3], k[2] + k[4]]) for k in kws]
    items.sort(key=lambda it: it[0])
    if not items or items[0][0] > fy0 + 0.06: return []      # the block must start at the top edge
    # never below the first long pipe line of the drawing (areas_final.json: top of the line work)
    line_top = LINE_TOP.get(sid, {}).get("y0", 1)
    if line_top < fy0 + 0.03:
        # no usable line-work boundary: data tables make a deep header, plain title rows a shallow one
        cap = fy0 + 0.2 if kws and min(k[2] for k in kws) < fy0 + 0.1 else items[0][0] + 0.05
    else:
        cap = min(fy0 + 0.2, max(line_top + 0.012, items[0][0] + 0.03))
    els = []; bottom = items[0][0]
    for y, e in items:                                          # grow downwards while elements stay contiguous
        if y - bottom > 0.035 or y > cap: break
        els.append(e); bottom = max(bottom, e[3])
    if len(els) < 2: return []
    # one small box per header element (title + its description lines, or a table keyword), so an
    # L-shaped header next to the process diagram does not swallow labels beside it
    x0 = min(e[0] for e in els) - 0.035; x1 = max(e[2] for e in els) + 0.035
    y0 = min(e[1] for e in els) - 0.012; y1 = max(e[3] for e in els) + 0.01
    y1 = min(y1, HEADFIX.get(sid, 1))       # checked by eye where the header sits beside the diagram
    return [[x0, y0, x1, y1]]

def in_area(sid, x, y):
    a = AREAS[sid]
    if not (a["x0"] <= x <= a["x1"] and a["y0"] <= y <= a["y1"]): return False
    return not any(b[0] <= x <= b[2] and b[1] <= y <= b[3] for b in HEADBOX.get(sid, []))

def header_title(words, t):
    # equipment title in the top header block: a description word sits just below the tag
    tag, typ, sub, x, y, w, h = t[:7]
    if typ != "equipment" or y > 0.30: return False
    cx = x + w / 2
    for wd in words:
        if wd[6] != 0: continue
        if 0 < wd[2] - (y + h) < h * 3.2 and wd[1] < x + w and wd[1] + wd[3] > x and wd[4] > h * 0.6 and DESC.match(P.norm(wd[0])):
            return True
    return False

def bubble_tags(sid, area, kind):
    p = f"/home/claude/work/bub/{sid}.json"
    if not os.path.exists(p): return []
    out = []
    items = json.load(open(p))["items"]
    p2 = f"/home/claude/work/bub2/{sid}.json"
    items2 = json.load(open(p2))["items"] if os.path.exists(p2) else []
    btags = []
    pend = []
    for idx, it in enumerate(items):
        if not in_area(sid, it["x"] + it["w"] / 2, it["y"] + it["h"] / 2): continue
        toks = [t for t in (re.sub(r"[^A-Z0-9/-]", "", t) for t in it["t"]) if t]
        if it["k"] == "c":
            alt = items2[idx] if idx < len(items2) and items2[idx]["k"] == "c" and abs(items2[idx]["x"] - it["x"]) < 0.002 else None
            toks2 = [t for t in (re.sub(r"[^A-Z0-9/-]", "", t) for t in (alt["t"] if alt else [])) if t]
            fns = collections.Counter()
            nums = collections.Counter()
            for i, tl in enumerate((toks, toks2)):
                for t in tl:
                    if re.match(r"^[A-Z/]+$", t):
                        m = VFN.search(t.strip("/"))
                        if m: fns[m.group(1)] += 1
                    else:
                        n = P.fixdigits(t.strip("/"))
                        if re.match(r"^\d{4,6}[A-D]?$", n): nums[n] += 1
            if alt and alt.get("num"):
                n = P.fixdigits(alt["num"].strip("/"))
                if re.match(r"^\d{4,6}[A-D]?$", n): nums[n] += 1.5
            if not fns or not nums: continue
            pend.append((it, fns, nums))
            continue

        elif it["k"] == "b":
            s = "".join(toks)
            mm = re.match(r"^([BC])([0-9IL]?)-([0-9OILSDQBZG]{2,3})$", s)
            if mm: s = mm.group(1) + P.fixdigits(mm.group(2)) + "-" + P.fixdigits(mm.group(3))
            m = re.match(r"^([BC])(\d?)-?(\d{2,3})$", s)
            if m and int(m.group(3)) == 0: m = None
            if m: btags.append((m, it))
    lens = collections.Counter()
    for _, _, nums in pend:
        for n in nums: lens[len(re.match(r"\d+", n).group(0))] += 1
    L = 5 if lens[5] >= lens[4] else 4
    for it, fns, nums in pend:
        sc = collections.Counter()
        for n, v in nums.items():
            dg = re.match(r"\d+", n).group(0); suf = n[len(dg):]
            if len(dg) == L + 1 and not suf and dg[-1] in "468":
                dg, suf = dg[:-1], ("B" if dg[-1] == "8" else "A")
            sc[dg + suf] += v * (1.0 if len(dg) == L else 0.3)
        num = sc.most_common(1)[0][0]
        fn = fns.most_common(1)[0][0]
        tag = f"{area}-{fn}-{num}" if area else f"{fn}-{num}"
        out.append((tag, "valve", fn, it["x"], it["y"], it["w"], it["h"], 90))
    pref = collections.Counter(m.group(2) for m, _ in btags if m.group(2))
    for m, it in btags:
        k, pnum, n = m.groups()
        if not pnum:
            if not pref: continue
            pnum = pref.most_common(1)[0][0]
        out.append((f"{k}{pnum}-{n}", "valve", "BLOCK" if k == "B" else "CHECK", it["x"], it["y"], it["w"], it["h"], 85))
    return out

def imsize(sid):
    from PIL import Image
    return Image.open(f"/home/claude/work/site/img/{sid}.png").size

def main():
    sheets, tags = [], {}
    for f, pg, sid in O.jobs():
        if not os.path.exists(f"/home/claude/work/ocr/{sid}.json"): continue
        d = json.load(open(f"/home/claude/work/ocr/{sid}.json"))
        kind = "PFD" if sid.startswith("PFD") else "PID"
        proj, unit, serial, title = title_info(sid, kind)
        fx = SHEETFIX.get(sid, {})
        if fx.get("skip"): continue
        unit = fx.get("unit", unit)
        if kind == "PFD" and not unit:
            unit = sid.split("-")[2]
            proj = sid.split("-")[1]
        title = fx.get("title", title)
        dwg = fx.get("dwg") or (f"{proj}-{unit}-{kind}-" + (f"0031-{serial}" if kind == "PID" else "0010") if proj and unit else sid)
        if kind == "PFD": dwg = fx.get("dwg") or sid[4:]
        d["unit"] = unit
        if os.path.exists(f"/home/claude/work/ocr/{sid}.inv.json"):
            d["words"] += json.load(open(f"/home/claude/work/ocr/{sid}.inv.json"))
        # area prefix for instrument tags = majority equipment area code on page
        eq = [t for t in P.extract(d, None) if t[1] == "equipment"]
        cnt = collections.Counter(t[0][:2] for t in eq)
        AREA = {"18": "10", "19": "10", "30": "30", "31": "30", "32": "30", "33": "30", "34": "30", "35": "30", "36": "30", "37": "30", "40": "40", "41": "40", "42": "40", "43": "40", "45": "40", "61": "30"}
        area = fx.get("area") or (cnt.most_common(1)[0][0] if cnt else AREA.get(unit))
        a = dict(FRAMES[sid]); a.update({k: AREAS[sid][k] for k in ("y1",)})
        if sid.startswith("PFD-2539") and sid.endswith("p1"): a = dict(AREAS[sid])
        AREAS[sid] = a
        _p2 = f"/home/claude/work/ocr2/{sid}.json"
        HEADBOX[sid] = header_boxes(sid, d["words"] + (json.load(open(_p2))["words"] if os.path.exists(_p2) else []))
        cands = [(t, 1) for t in P.extract(d, area)]
        p2 = f"/home/claude/work/ocr2/{sid}.json"
        if os.path.exists(p2):
            d2 = {"words": json.load(open(p2))["words"], "unit": unit}
            cands += [(t, 2) for t in P.extract(d2, area)]
        HT = header_tags(sid, cands)
        OKH = re.compile(r"^\d{2}-[A-Z]{1,3}-\d{4}[A-F]?(/[A-Z]{1,2}\d{1,2}[A-Z]?|/[A-Z]{1,2})?$")
        hdr = []
        hc = [(t, s_) for t, s_ in cands if t[1] == "equipment" and any(bx[0] <= t[3] + t[5] / 2 <= bx[2] and bx[1] <= t[4] + t[6] / 2 <= bx[3] for bx in HEADBOX.get(sid, []))]
        for t in resolve(hc):
            cx, cy = t[3] + t[5] / 2, t[4] + t[6] / 2
            if any(bx[0] <= cx <= bx[2] and bx[1] <= cy <= bx[3] for bx in HEADBOX.get(sid, [])):
                for nm in expand(t[0]):
                    nm = re.sub("^50-", "30-", nm)
                    if OKH.match(nm) and not nm.startswith("39-"): hdr.append((nm, t))
        HDRS[sid] = sorted({nm for nm, _ in hdr})
        if kind == "PID":
            for nm, t in hdr: HDRPOS.setdefault(nm, []).append((sid, t))
        cands = [(t, s) for t, s in cands if in_area(sid, t[3] + t[5] / 2, t[4] + t[6] / 2) and not header_title(d["words"], t)]
        found = resolve(cands)
        # equipment named only in a stream label ("FROM 10-E3005", "TO 10-V8001", "(FOR 10-P8001A") is a reference, not the equipment
        allw = d["words"] + (d2["words"] if os.path.exists(p2) else [])
        found = [t for t in found if not (t[1] == "equipment" and is_reference(t, allw))]
        # stream/signal labels checked by eye on the drawings (tools/exclude.json: [sheet, x, y] = centre of the label)
        found = [t for t in found if not (t[1] == "equipment" and any(e[0] == sid and abs(e[1] - (t[3] + t[5] / 2)) < 0.01 and abs(e[2] - (t[4] + t[6] / 2)) < 0.01 for e in EXCL))]
        if False and HT:
            have = {t[0] for t in found if t[1] == "equipment"}
            missing = HT - have
            fixed = []
            for t in found:
                if t[1] == "equipment" and t[0] not in HT:
                    m = [h for h in missing if lev1(h, t[0])]
                    if len(m) == 1:
                        FIXLOG.append((sid, t[0], m[0])); missing.discard(m[0]); t = (m[0],) + tuple(t[1:])
                fixed.append(t)
            found = fixed
        found += bubble_tags(sid, area, kind)
        si = len(sheets)
        sheets.append({"id": sid, "kind": kind, "unit": unit or "?", "dwg": dwg, "title": title,
                       "img": f"img/{sid}.png", "w": imsize(sid)[0], "h": imsize(sid)[1], "src": f"{f} – trang {pg}"})
        # second-opinion re-read (verify.py): majority vote over several text sizes
        vf = f"/home/claude/work/verify/{sid}.json"
        if os.path.exists(vf):
            V = json.load(open(vf))
            fixed = []
            for t in found:
                for r in V:
                    if re.match(r"^[BC]\d-", t[0]): break
                    if r["t"] == t[0] and abs(r["x"] - t[3]) < 1e-3 and abs(r["y"] - t[4]) < 1e-3 and r["votes"]:
                        win, n = max(r["votes"].items(), key=lambda kv: kv[1])
                        if win != t[0] and n >= 4 and n >= 2 * r["votes"].get(t[0], 0):
                            FIXLOG.append((sid, t[0], win)); t = (win,) + tuple(t[1:])
                        break
                fixed.append(t)
            found = fixed
        found = [(re.sub(r'^(\d)-?(\d/\d)"', r'\1-\2"', t[0]),) + tuple(t[1:]) if t[1] == "line" else t for t in found]
        sf = f"/home/claude/work/sizecheck/{sid}.json"
        if os.path.exists(sf):
            SC = json.load(open(sf))
            fixed = []
            for t in found:
                if t[1] == "line":
                    for r in SC:
                        if abs(r["x"] - t[3]) < 1e-3 and abs(r["y"] - t[4]) < 1e-3:
                            ns = pick_size(t[0].split('"')[0], r["votes"])
                            if ns: FIXLOG.append((sid, t[0], ns + t[0][t[0].index('"'):])); t = (ns + t[0][t[0].index('"'):],) + tuple(t[1:])
                            break
                fixed.append(t)
            found = fixed
        ff = f"/home/claude/work/fix35/{sid}.json"
        if os.path.exists(ff):
            F35 = json.load(open(ff))
            fixed = []
            for t in found:
                for r in F35:
                    if t[1] == "line" and abs(r["x"] - t[3]) < 1e-3 and abs(r["y"] - t[4]) < 1e-3:
                        mn = re.search(r'"-[A-Z]{1,4}-(\d{7})-', r["new"]); mt = re.search(r'("-[A-Z]{1,4}-)(\d{7})(-)', t[0])
                        if mn and mt and mn.group(1) != mt.group(2):
                            nt = t[0][:mt.start(2)] + mn.group(1) + t[0][mt.end(2):]
                            FIXLOG.append((sid, t[0], nt)); t = (nt,) + tuple(t[1:])
                        break
                fixed.append(t)
            found = fixed
        names_here = set()
        for t in found:
            names_here |= expand(t[0]) if t[1] == "equipment" else {t[0]}
        seen_h = set()
        import difflib
        for nm, t in ([] if not INCLUDE_HEADER_ONLY else hdr):
            if nm in names_here or nm in seen_h: continue
            if any(near_dup(nm, o) for o in names_here | seen_h): continue
            seen_h.add(nm)
            e = tags.setdefault(nm, {"t": nm, "k": "equipment", "s": t[2], "o": []})
            e["o"].append([si, round(t[3], 4), round(t[4], 4), round(t[5], 4), round(t[6], 4), 1])
        for tag, typ, sub, x, y, w, h, conf in found:
            if typ == "line":
                tag = re.sub(r"-([A-Z])(\d{2})8(N?)(-|$)", r"-\g<1>\g<2>B\3\4", tag)  # B248 -> B24B
            # a combined label such as 10-P8003A/B names two pieces of equipment: index each one
            names = sorted(expand(tag)) if typ == "equipment" and "/" in tag else [tag]
            for nm in names:
                e = tags.setdefault(nm, {"t": nm, "k": typ, "s": sub, "o": []})
                if nm != tag: e.setdefault("l", set()).add(tag)
                if not any(o[0] == si and abs(o[1] - x) < 0.01 and abs(o[2] - y) < 0.01 for o in e["o"]):
                    e["o"].append([si, round(x, 4), round(y, 4), round(w, 4), round(h, 4)])
    # area 50 does not exist on these drawings: "5" is a misread "3" when the 30- tag is known
    for k in [k for k in tags if k.startswith("50-")]:
        k3 = "30-" + k[3:]
        e = tags.pop(k)
        if k3 in tags: tags[k3]["o"] += e["o"]
        else: e["t"] = k3; tags[k3] = e
        FIXLOG.append(("*", k, k3))
    # equipment read two ways (3/5, P/R) on different sheets: fold the weakly attested reading into the strong one
    V = collections.Counter()
    for f in glob.glob("/home/claude/work/verify/*.json"):
        for r in json.load(open(f)):
            for k, v in r["votes"].items():
                for e in (expand(k) if "/" in k else {k}): V[e] += v
    def base(k): return k.split("/")[0]
    CAN = str.maketrans({"5": "3"})
    groups = collections.defaultdict(list)
    for k, e in tags.items():
        if e["k"] != "equipment": continue
        m = re.match(r"^(\d{2})-([A-Z]{1,3})-(\d{4})(.*)$", k)
        if not m: continue
        ty = "P" if m.group(2) == "R" else m.group(2)
        groups[(m.group(1), ty, m.group(3).translate(CAN), m.group(4))].append(k)
    for ks in groups.values():
        if len(ks) < 2: continue
        ks.sort(key=lambda k: (not re.match(r"^\d{2}-R-", k), V[k], len(tags[k]["o"])), reverse=True)
        win = ks[0]
        for lo in ks[1:]:
            if lo not in tags: continue
            strong_bases = V[base(win)] >= 5 and V[base(lo)] >= 5 and base(win) != base(lo)
            r_misread = re.match(r"^\d{2}-R-", lo) and not re.match(r"^\d{2}-R-", win)
            if r_misread or (not strong_bases and len(tags[win]["o"]) >= len(tags[lo]["o"]) and
                             ((V[lo] <= 2 and V[win] >= 8) or (V[lo] == 0 and V[win] >= 3))):
                e = tags.pop(lo); tags[win]["o"] += e["o"]
                if "l" in e: tags[win].setdefault("l", set()).update(e["l"] if isinstance(e["l"], set) else set(e["l"]))
                FIXLOG.append(("*", lo, win))
    # service codes OCR confuses: I->L, a trailing I dropped or added
    SVC_FIX = {"LA": "IA", "W": "WI", "VTI": "VT"}
    for k in [k for k, e in tags.items() if e["k"] == "line"]:
        m = re.match(r'^(.*?"-)([A-Z]{1,4})(-.*)$', k)
        if m and m.group(2) in SVC_FIX:
            nk = m.group(1) + SVC_FIX[m.group(2)] + m.group(3)
            e = tags.pop(k); e["t"] = nk; e["s"] = SVC_FIX[m.group(2)]
            if nk in tags: tags[nk]["o"] += e["o"]
            else: tags[nk] = e
            FIXLOG.append(("svc", k, nk))
    # manual corrections checked on the drawings (tools/overrides.json)
    if os.path.exists("/home/claude/work/overrides.json"):
        for old, new in json.load(open("/home/claude/work/overrides.json")).items():
            if old.startswith("_") or old not in tags: continue
            e = tags.pop(old)
            FIXLOG.append(("manual", old, new))
            if not new: continue                      # "" = not a real tag (reference text, misread duplicate)
            e["t"] = new
            al = set(e.get("a", ())) | {old}
            if new in tags:
                tags[new]["o"] += e["o"]; tags[new]["a"] = set(tags[new].get("a", ())) | al
            else:
                e["a"] = al; tags[new] = e
    # per-position fixes (tools/posfix.json): {"sid", "x", "y", "to"} renames the occurrence whose box starts at (x, y);
    # with "w", "h" and no existing occurrence the position is added (label OCR could not read)
    if os.path.exists("/home/claude/work/posfix.json"):
        sidx = {s_["id"]: i for i, s_ in enumerate(sheets)}
        for fx in json.load(open("/home/claude/work/posfix.json")):
            if isinstance(fx, str): continue
            si = sidx[fx["sid"]]; occ = None
            for k, e in list(tags.items()):
                for o in e["o"]:
                    if o[0] == si and abs(o[1] - fx["x"]) < 0.004 and abs(o[2] - fx["y"]) < 0.004:
                        occ = (k, o); break
                if occ: break
            if occ and not fx.get("add"):
                k, o = occ
                if k == fx["to"]: continue
                tags[k]["o"].remove(o)
                if not tags[k]["o"]: e = tags.pop(k)
                kind = tags[k]["k"] if k in tags else e["k"]; sub = tags[k]["s"] if k in tags else e["s"]
                t2 = tags.setdefault(fx["to"], {"t": fx["to"], "k": kind, "s": sub, "o": []})
                t2["o"].append(o); t2["a"] = set(t2.get("a", ())) | {k}
                FIXLOG.append(("pos", k, fx["to"]))
            if (not occ or fx.get("add")) and "w" in fx:
                t2 = tags.setdefault(fx["to"], {"t": fx["to"], "k": fx.get("k", "equipment"), "s": fx.get("s", ""), "o": []})
                t2["o"].append([si, fx["x"], fx["y"], fx["w"], fx["h"]])
                FIXLOG.append(("pos+", "", fx["to"]))
    # equipment is indexed from the P&IDs only: PFD positions are dropped (a PFD repeats the P&ID equipment,
    # often with a different OCR reading). Lines/valves on both P&ID and PFD keep only the P&ID positions.
    for k in list(tags):
        e = tags[k]
        kinds = {sheets[o[0]]["kind"] for o in e["o"]}
        if e["k"] == "equipment" and "PFD" in kinds:
            e["o"] = [o for o in e["o"] if sheets[o[0]]["kind"] == "PID"]
            FIXLOG.append(("pfd-drop", e["t"], ""))
            if not e["o"]:
                # not labelled in the P&ID process area: fall back to the P&ID title-block entry, else drop it
                sidx = {s_["id"]: i for i, s_ in enumerate(sheets)}
                for sid_, t in HDRPOS.get(k, []) + [p_ for a in e.get("a", ()) for p_ in HDRPOS.get(a, [])]:
                    o = [sidx[sid_], round(t[3], 4), round(t[4], 4), round(t[5], 4), round(t[6], 4), 1]
                    if not any(q[0] == o[0] for q in e["o"]): e["o"].append(o)
                if e["o"]: FIXLOG.append(("pid-header", k, ""))
                else: tags.pop(k); FIXLOG.append(("pfd-only-drop", k, ""))
        elif kinds >= {"PID", "PFD"}:
            e["o"] = [o for o in e["o"] if sheets[o[0]]["kind"] == "PID"]
            FIXLOG.append(("pfd-drop", e["t"], ""))
    for e in tags.values():
        if "l" in e: e["l"] = sorted(e["l"])
        if "a" in e:
            al = sorted(set(e["a"]) - {e["t"]})
            if al: e["a"] = al
            else: del e["a"]
        s = e["s"]
        if e["k"] == "valve": e["d"] = P.VALVE_NAME.get(s, "Van") if s != "CHECK" else "Van một chiều (check)"
        elif e["k"] == "equipment": e["d"] = P.EQUIP_NAME.get(s, "Thiết bị")
        else: e["d"] = f"Dịch vụ {s}"
    # tools/unitmerge.json: units shown together on the web, and units removed from the web
    if os.path.exists("/home/claude/work/unitmerge.json"):
        UM = json.load(open("/home/claude/work/unitmerge.json"))
        keep = [i for i, s_ in enumerate(sheets) if s_["unit"] not in UM.get("drop", [])]
        newidx = {o: n for n, o in enumerate(keep)}
        sheets = [sheets[i] for i in keep]
        for s_ in sheets:
            s_["unit"] = UM.get("merge", {}).get(s_["unit"], s_["unit"])
            su = UM.get("sheet", {}).get(s_["id"])
            if su:
                su = [su] if isinstance(su, str) else su
                s_["unit"] = su[0]
                if su[1:]: s_["also"] = su[1:]
        for k in list(tags):
            e = tags[k]
            e["o"] = [[newidx[o[0]]] + o[1:] for o in e["o"] if o[0] in newidx]
            if not e["o"]:
                tags.pop(k)
    used = sorted({u for s in sheets for u in [s["unit"]] + s.get("also", [])})
    units = [{"code": u, "name": UNIT_NAMES.get(u, "Unit " + u)} for u in used]
    out = {"updated": sys.argv[1] if len(sys.argv) > 1 else "", "units": units, "sheets": sheets,
           "tags": sorted(tags.values(), key=lambda e: e["t"])}
    os.makedirs("/home/claude/work/site/data", exist_ok=True)
    json.dump(FIXLOG, open("/home/claude/work/fixlog.json", "w"))
    json.dump(HDRS, open("/home/claude/work/headers.json", "w"))
    json.dump({"areas": AREAS, "head": HEADBOX}, open("/home/claude/work/areas_used.json", "w"))
    json.dump(out, open("/home/claude/work/site/data/data.json", "w"), ensure_ascii=False, separators=(",", ":"))
    print(len(sheets), "sheets", len(tags), "tags", collections.Counter(e["k"] for e in tags.values()))

if __name__ == "__main__":
    main()
