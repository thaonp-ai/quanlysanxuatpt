import json, glob, re, collections

DASH = re.compile(r"[—–_‐−~]+")
def norm(t):
    t = DASH.sub("-", t)
    t = re.sub(r"-{2,}", "-", t)
    t = re.sub(r"(/[A-Z]{1,3}\d{1,2})[-_ ]([A-Z])$", r"\1\2", t)
    t = t.replace("”", '"').replace("“", '"').replace("’", "'").replace("‘", "'")
    t = t.strip(".,;:|()[]{}<>'`°*!_")
    return t.upper()

def fixdigits(s):
    return s.translate(str.maketrans({"O": "0", "D": "0", "Q": "0", "I": "1", "L": "1", "|": "1", "S": "5", "B": "8", "Z": "2", "G": "6"}))

LINE = re.compile(r'^(\d{1,2}(?:-?\d/\d)?|\d/\d)"?-([A-Z]{1,4})-([0-9OIDLSB]{6,8})-([A-Z0-9]{3,6})(?:-([A-Z]))?$')
EQUIP_TYPES = "PK|TK|STP|MP|P|E|V|K|T|BA|CT|F|GT|R|D|M|A|B|C|X|Y|AG|BL|FL|SK|H|MX|ST|DE|SP|FS|HE|BV|CV|PM|U|L|J|AF|CB|FA|TP|PT|SL|EJ|DS|TA"
EQUIP = re.compile(r"^(\d{2})-?(" + EQUIP_TYPES + r")-?(\d{4})([A-Z]{0,2})((?:/[A-Z0-9]{1,4})*)$")
VALVE_FUN = "PV|FV|LV|TV|HV|XV|PSV|PCV|FCV|LCV|TCV|SDV|BFV|MOV|PRV|HCV|UV|KV|ESDV|TSV|BDV|SV|VSV|AV|PDV|DV|TSE|PSE|NRV|CHV"
VALVE = re.compile(r"^(\d{2})-?(" + VALVE_FUN + r")-?(\d{4,6})([A-Z]?)((?:/[A-Z]){0,6})$")
BUBBLE_FUN = {"PV", "FV", "LV", "TV", "HV", "XV", "PSV", "PCV", "FCV", "LCV", "TCV", "SDV", "UV", "KV", "HCV", "TSV", "PRV", "PDV", "BDV", "MOV", "PDCV", "TSE", "PSE", "AV"}
BLOCK = re.compile(r"^[B8][1-9IL]-[0-9OIL]{2,3}$")
LOCAL = re.compile(r"^(BL|DP|DR|TK|PM|MBR|BF|SP|MX|AG|FP|CP|SV|V|P|T|BV|CV|FM|FT|PU|BS)-(\d{3})([A-Z]{0,2}\d?)((?:/[A-Z0-9~]{1,4})*)$")

VALVE_NAME = {"PV": "Van điều khiển áp suất", "FV": "Van điều khiển lưu lượng", "LV": "Van điều khiển mức", "TV": "Van điều khiển nhiệt độ",
              "HV": "Van điều khiển tay (HV)", "XV": "Van on/off (XV)", "PSV": "Van an toàn", "PRV": "Van giảm áp", "PCV": "Van tự điều áp",
              "FCV": "Van điều khiển lưu lượng", "LCV": "Van điều khiển mức", "TCV": "Van điều khiển nhiệt độ", "SDV": "Van ngắt khẩn cấp",
              "ESDV": "Van ngắt khẩn cấp", "BDV": "Van xả áp", "BFV": "Van bướm", "MOV": "Van điện", "UV": "Van on/off", "KV": "Van on/off",
              "HCV": "Van điều khiển tay", "TSV": "Van an toàn nhiệt", "PDV": "Van chênh áp", "BLOCK": "Van chặn (block)", "SV": "Van solenoid",
              "TSE": "Nút chảy an toàn", "PSE": "Đĩa nổ", "AV": "Van khí điều khiển", "DV": "Van", "NRV": "Van một chiều", "CHV": "Van một chiều", "VSV": "Van"}
EQUIP_NAME = {"P": "Bơm", "PK": "Cụm thiết bị (package)", "TK": "Bồn chứa", "STP": "Turbine dẫn động bơm", "MP": "Motor bơm", "E": "Thiết bị trao đổi nhiệt",
              "V": "Bình/Thiết bị", "K": "Máy nén", "T": "Tháp", "BA": "Bể", "CT": "Tháp giải nhiệt", "F": "Lò/Bộ lọc", "GT": "Turbine khí",
              "B": "Lò hơi", "R": "Thiết bị phản ứng", "D": "Thiết bị", "A": "Thiết bị", "M": "Motor", "X": "Thiết bị", "AG": "Máy khuấy", "BL": "Máy thổi khí",
              "DP": "Bơm định lượng", "DR": "Thùng hóa chất", "PM": "Bơm", "MBR": "Bể MBR", "BF": "Bể/Thiết bị lọc", "H": "Thiết bị gia nhiệt",
              "ST": "Turbine hơi", "SK": "Skid", "FL": "Đuốc", "MX": "Máy trộn", "C": "Thiết bị", "Y": "Thiết bị"}

def is_process(x, y, kind):
    if x > 0.835 or y > 0.972 or y < 0.012 or x < 0.012: return False
    if kind == "PFD" and y > 0.74: return False  # stream table
    return True

def extract(d, area):
    words = [[norm(w[0])] + w[1:] for w in d["words"]]
    found = []  # (tag, type, sub, x, y, w, h, conf)
    def add(tag, typ, sub, w, conf):
        found.append((tag, typ, sub, w[1], w[2], w[3], w[4], conf))
    cands = [(w[0], w) for w in words]
    # split glued labels like "30-J3001__[30-MP3003A/B|" and repair common leading misreads
    extra = []
    for w in words:
        raw = w[0]
        parts = [p for p in re.split(r"[\[\]{}|()]+|-{2,}(?=\d)|\s+", raw) if p]
        if len(parts) > 1 or raw != w[0]:
            for p in parts:
                p = norm(p)
                if len(p) >= 6: extra.append((p, w))
    for t, w in list(cands) + extra:
        t2 = re.sub(r"^\$(\d)", r"3\1", t)
        m = re.match(r"^(\d)(\d)(\d)-(.*)$", t2)
        if m:
            for a in ("10", "20", "30", "40", "60"):
                if a in m.group(1) + m.group(2) + m.group(3):
                    extra.append((a + "-" + m.group(4), w)); break
        if t2 != t: extra.append((t2, w))
    cands += extra
    # join neighbours on same line (horizontal OCR) to catch split tags
    hz = [w for w in words if w[6] == 0]
    buckets = collections.defaultdict(list)
    for w in hz: buckets[int(w[2] / 0.004)].append(w)
    def neigh(a):
        k = int(a[2] / 0.004)
        for kk in (k - 1, k, k + 1):
            for b in buckets.get(kk, ()):
                if b is not a and b[1] > a[1]: yield b
    for a in hz:
        for b in neigh(a):
            if abs(b[2] - a[2]) < a[4] * 0.6 and -a[4] * 0.6 <= b[1] - (a[1] + a[3]) < a[4] * (3.0 if b[0].startswith("/") else 1.6):
                j = [a[0] + b[0], a[1], a[2], b[1] + b[3] - a[1], max(a[4], b[4])] + a[5:]
                cands.append((j[0], j))
                if not a[0].endswith("-") and not b[0].startswith("-"):
                    j2 = list(j); j2[0] = a[0] + "-" + b[0]; cands.append((j2[0], j2))
    for t, w in cands:
        if len(t) < 4: continue
        conf = w[5]
        m = LINE.match(t)
        if m:
            size, svc, num, spec, ins = m.groups()
            num = fixdigits(num)
            if not num.isdigit() or len(num) != 7: continue
            spec = spec[0] + spec[1:].replace("O", "0") if spec else spec
            spec = re.sub(r"^([A-Z])(\d)8$", r"\g<1>\g<2>B", spec)
            m2 = re.match(r"^([A-Z])([0-9SIO]{2})([A-Z0-9]{1,2})(N?)$", spec)
            if not m2: continue
            mid = fixdigits(m2.group(2)); last = m2.group(3).replace("8", "B").replace("0", "O") if not m2.group(3).isalpha() else m2.group(3)
            if not mid.isdigit() or not last.isalpha(): continue
            spec = m2.group(1) + mid + last + m2.group(4)
            size = re.sub(r'^(\d)-?(\d/\d)$', r'\1-\2', size)
            tag = f'{size}"-{svc}-{num}-{spec}' + (f"-{ins}" if ins else "")
            add(tag, "line", svc, w, conf); continue
        m = re.match(r"^(XV|PSV|SV|HV|PV|FV|LV|TV|BFV|PCV|FCV|LCV|TCV|SDV|MOV|HCV)-(\d{4,5})([A-H]?)$", t)
        if m and area:
            add(f"{area}-{m.group(1)}-{m.group(2)}{m.group(3)}", "valve", m.group(1), w, conf); continue
        m = VALVE.match(t)
        if m:
            a, f, n, s, alt = m.groups()
            add(f"{a}-{f}-{n}{s}{alt}", "valve", f, w, conf); continue
        m = EQUIP.match(t)
        if m:
            a, ty, n, s, alt = m.groups()
            alt = "/".join(("B" if p == "8" else re.sub(r"^([A-Z]{1,2})[IL]([A-Z]?)$", r"\g<1>1\g<2>", re.sub(r"^([A-Z])8$", r"\1", p))) for p in alt.split("/"))
            add(f"{a}-{ty}-{n}{s}{alt}", "equipment", ty, w, conf); continue
        m = LOCAL.match(t)
        if m and d["unit"] == "WWTP":
            ty = m.group(1)
            add(t, "valve" if ty in ("SV", "BV", "CV") else "equipment", ty, w, conf); continue
        if BLOCK.match(t) and w[6] == 0 and w[4] < 0.02:
            tt = "B" + t[1:]
            p, q = tt.split("-")
            p = "B" + fixdigits(p[1:]); q = fixdigits(q)
            if re.match(r"^B\d-\d{2,3}$", p + "-" + q):
                add(p + "-" + q, "valve", "BLOCK", w, conf)
    # instrument bubbles: function word above number
    hzw = [w for w in words if w[6] == 0]
    funs = [w for w in hzw if w[0] in BUBBLE_FUN]
    for f in funs:
        cx = f[1] + f[3] / 2
        best = None
        for w in hzw:
            if w is f: continue
            num = fixdigits(w[0]) if re.match(r"^[0-9OIDLSB]{3,6}[A-C]?(/[A-C])*$", w[0]) else None
            if not num or not re.match(r"^\d{3,6}", num): continue
            dy = w[2] - (f[2] + f[4])
            if -f[4] * 0.3 < dy < f[4] * 1.8 and abs((w[1] + w[3] / 2) - cx) < max(f[3], w[3]) * 0.9:
                if best is None or dy < best[0]: best = (dy, w, num)
        if best:
            _, w, num = best
            m = re.match(r"^(\d{4,6})([A-C]?)((?:/[A-C])*)$", num)
            if not m: continue
            n = m.group(1)
            tag = f"{area}-{f[0]}-{n}{m.group(2)}{m.group(3)}" if area else f"{f[0]}-{n}{m.group(2)}"
            bx = [min(f[1], w[1]), f[2], max(f[1] + f[3], w[1] + w[3]) - min(f[1], w[1]), w[2] + w[4] - f[2]]
            found.append((tag, "valve", f[0], *bx, min(f[5], w[5])))
    return found
