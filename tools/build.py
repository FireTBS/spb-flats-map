import json, re, sys, datetime

SRC = sys.argv[1]      # JSON from the sheet: {"values": [[...], ...]}
COORDS = sys.argv[2]   # lines: "<row no> <lat> <lon>"
TEMPLATE = sys.argv[3]
OUT_DIR = sys.argv[4]

v = json.load(open(SRC))["values"]
rows = [r + [""] * 21 for r in v[1:] if any(c.strip() for c in r)]
co = {}
for l in open(COORDS):
    p = l.split()
    if len(p) == 3:
        co[p[0]] = (float(p[1]), float(p[2]))

def num(s):
    s = re.sub(r"[^\d,\.]", "", s.replace(" ", "")).replace(",", ".")
    return float(s) if s else 0.0

flats, skipped = [], []
for r in rows:
    no = r[0].strip()
    if no not in co:
        skipped.append(no)
        continue
    # В публичную карту попадают только данные самого объявления.
    # Продавцы, плюсы/минусы и комментарии А.И. сюда не выгружаются.
    flats.append({
        "no": no,
        "addr": r[4].strip(),
        "district": r[5].strip(),
        "metro": r[6].strip(),
        "walk": r[7].strip(),
        "price": num(r[8]),
        "area": r[9].strip(),
        "ppm": r[10].strip(),
        "rooms": r[11].strip(),
        "floor": r[12].strip(),
        "fund": r[13].strip(),
        "cond": r[14].strip(),
        "parking": r[15].strip(),
        "link": r[3].strip(),
        "lat": co[no][0],
        "lon": co[no][1],
    })

html = open(TEMPLATE, encoding="utf-8").read()
html = html.replace("__DATA__", json.dumps(flats, ensure_ascii=False, separators=(",", ":")))
html = html.replace("__UPDATED__", datetime.date(2026, 11, 24).strftime("%d.%m.%Y"))
open(OUT_DIR + "/index.html", "w", encoding="utf-8").write(html)
print("flats", len(flats), "skipped", skipped)
