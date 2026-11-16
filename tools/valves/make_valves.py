"""Excel danh mục block valve (X.PT, CMMS) → tools/valves/valves.json.

    python3 tools/valves/make_valves.py "tools/valves/Tagname cho block valve - X.PT-rev3.xlsx"

Cột dùng: Parent Asset, Asset number (tagname), Name, X.PT Note, Ghi chú 1.
Tag trùng trong Excel được gộp (tên nối bằng " / ").
"""
import json, os, re, sys
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))


def kind(name):
    n = name.lower()
    if "bypass" in n or "bybass" in n:
        return "BYPASS"
    if "drain" in n or n.startswith("van xả"):
        return "DRAIN"
    if "vent" in n:
        return "VENT"
    return "BLOCK"


def main(xlsx):
    ws = openpyxl.load_workbook(xlsx, data_only=True).worksheets[0]
    hdr = [str(c or "").strip() for c in next(ws.iter_rows(min_row=1, max_row=1, values_only=True))]
    col = {h: i for i, h in enumerate(hdr)}
    out, seen = [], {}
    for r in ws.iter_rows(min_row=2, values_only=True):
        tag = str(r[col["Asset number (tagname)"]] or "").strip()
        if not tag:
            continue
        name = " ".join(str(r[col["Name"]] or "").split())
        name = re.sub(r"^Van(n)? (bloc|block)\b", "Van block", name)
        name = re.sub(r"^Vandrain", "Van drain", name)
        e = {"t": tag, "s": kind(name), "d": name, "p": str(r[col["Parent Asset"]] or "").strip()}
        note = "; ".join(x for x in (str(r[col.get("X.PT Note", -1)] or "").strip() if "X.PT Note" in col else "",
                                     str(r[col.get("Ghi chú 1", -1)] or "").strip() if "Ghi chú 1" in col else "") if x)
        if note:
            e["n"] = " ".join(note.split())
        if tag in seen:
            p = seen[tag]
            if name and name not in p["d"]:
                p["d"] += " / " + name
            continue
        seen[tag] = e
        out.append(e)
    json.dump(out, open(os.path.join(HERE, "valves.json"), "w"), ensure_ascii=False, indent=0)
    print(len(out), "van")


if __name__ == "__main__":
    main(sys.argv[1])
