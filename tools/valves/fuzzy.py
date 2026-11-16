"""So khớp chuỗi OCR với tên tag, coi các ký tự hay bị OCR nhầm trên bản vẽ CAD là gần nhau."""
CONF = [("8", "3"), ("8", "B"), ("3", "B"), ("8", "S"), ("5", "S"), ("6", "8"), ("0", "O"), ("0", "D"), ("1", "I"),
        ("1", "L"), ("B", "F"), ("B", "E"), ("F", "E"), ("B", "R"), ("2", "8"), ("9", "8"), ("7", "T"), ("8", "0"),
        ("5", "6"), ("3", "5"), ("2", "Z"), ("1", "7"), ("U", "D"), ("U", "L"), ("1", "T"), ("C", "G"), ("0", "Q")]
_C = {frozenset(p) for p in CONF}


def sub(a, b):
    if a == b:
        return 0.0
    return 0.35 if frozenset((a, b)) in _C else 1.0


def dist(a, b):
    """Khoảng cách Levenshtein có trọng số (thêm/bớt 1, nhầm ký tự gần nhau 0.35)."""
    n, m = len(a), len(b)
    prev = [float(j) for j in range(m + 1)]
    for i in range(1, n + 1):
        cur = [float(i)] + [0.0] * m
        for j in range(1, m + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + sub(a[i - 1], b[j - 1]))
        prev = cur
    return prev[m]


def clean(s):
    return "".join(ch for ch in str(s).upper() if ch.isalnum())
