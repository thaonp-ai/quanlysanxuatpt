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

def resolve(cands):
    """Readings of the same label from both OCR passes overlap: keep one per label.
    Prefer the high-resolution pass, then the longest (most complete) tag, then confidence."""
    cands = sorted(cands, key=lambda c: (-c[1], -len(c[0][0]), -c[0][7]))
    kept = []
    for t, s in cands:
        if any(k[1] == t[1] and _overlap(k, t) for k in kept): continue
        kept.append(t)
    return kept

def header_boxes(sid, words):
    """Rectangles covering the equipment title/data blocks at the top of the sheet."""
    fy0 = FRAMES[sid]["y0"]
    els = []
    for wd in words:
        if wd[6] != 0 or wd[2] > 0.32 or wd[2] < fy0: continue
        if TABLEW.match(P.norm(wd[0])): els.append([wd[1], wd[2], wd[1] + wd[3], wd[2] + wd[4]])
    for t in P.extract({"words": words, "unit": ""}, None):
        if t[1] == "equipment" and t[4] < 0.32 and header_title(words, t):
            els.append([t[3], t[4], t[3] + t[5], t[4] + t[6] * 4])
    boxes = [[e[0] - 0.035, e[1] - 0.012, e[2] + 0.035, e[3] + 0.03] for e in els]
    changed = True
    while changed:
        changed = False
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, c = boxes[i], boxes[j]
                vov = min(a[3], c[3]) - max(a[1], c[1])
                if (a[0] <= c[2] and c[0] <= a[2] and a[1] <= c[3] and c[1] <= a[3]) or vov > 0.5 * min(a[3] - a[1], c[3] - c[1]):
                    boxes[i] = [min(a[0], c[0]), min(a[1], c[1]), max(a[2], c[2]), max(a[3], c[3])]
                    boxes.pop(j); changed = True; break
            if changed: break
    # a single stray keyword is not a header block
    return [bx for bx, n in ((bx, sum(1 for e in els if bx[0] <= e[0] and e[2] <= bx[2] and bx[1] <= e[1] and e[3] <= bx[3])) for bx in boxes) if n >= 2]

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
        if 0 < wd[2] - (y + h) < h * 3.2 and abs(wd[1] + wd[3] / 2 - cx) < max(w * 1.6, 0.05) and DESC.match(P.norm(wd[0])):
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
        HEADBOX[sid] = header_boxes(sid, d["words"])
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
        cands = [(t, s) for t, s in cands if in_area(sid, t[3] + t[5] / 2, t[4] + t[6] / 2) and not header_title(d["words"], t)]
        found = resolve(cands)
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
        ff = f"/home/claude/work/fix35/{sid}.json"
        if os.path.exists(ff):
            F35 = json.load(open(ff))
            fixed = []
            for t in found:
                for r in F35:
                    if r["t"] == t[0] and abs(r["x"] - t[3]) < 1e-3 and abs(r["y"] - t[4]) < 1e-3:
                        if r["new"] != t[0]: FIXLOG.append((sid, t[0], r["new"])); t = (r["new"],) + tuple(t[1:])
                        break
                fixed.append(t)
            found = fixed
        names_here = set()
        for t in found:
            names_here |= expand(t[0]) if t[1] == "equipment" else {t[0]}
        seen_h = set()
        import difflib
        for nm, t in hdr:
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
    for e in tags.values():
        if "l" in e: e["l"] = sorted(e["l"])
        s = e["s"]
        if e["k"] == "valve": e["d"] = P.VALVE_NAME.get(s, "Van") if s != "CHECK" else "Van một chiều (check)"
        elif e["k"] == "equipment": e["d"] = P.EQUIP_NAME.get(s, "Thiết bị")
        else: e["d"] = f"Dịch vụ {s}"
    used = sorted({s["unit"] for s in sheets})
    units = [{"code": u, "name": UNIT_NAMES.get(u, "Unit " + u)} for u in used]
    out = {"updated": sys.argv[1] if len(sys.argv) > 1 else "", "units": units, "sheets": sheets,
           "tags": sorted(tags.values(), key=lambda e: e["t"])}
    os.makedirs("/home/claude/work/site/data", exist_ok=True)
    json.dump(FIXLOG, open("/home/claude/work/fixlog.json", "w"))
    json.dump({"areas": AREAS, "head": HEADBOX}, open("/home/claude/work/areas_used.json", "w"))
    json.dump(out, open("/home/claude/work/site/data/data.json", "w"), ensure_ascii=False, separators=(",", ":"))
    print(len(sheets), "sheets", len(tags), "tags", collections.Counter(e["k"] for e in tags.values()))

if __name__ == "__main__":
    main()
