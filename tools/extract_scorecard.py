"""Rebuild the school-search data built into index.html.

Usage:
  1. Download "Most Recent Institution-Level Data" from
     https://collegescorecard.ed.gov/data/ and unzip it.
  2. python3 tools/extract_scorecard.py Most-Recent-Cohorts-Institution.csv index.html

The script keeps currently operating, mainly bachelor's-degree schools with at
least 400 undergrads, and rewrites the <script id="schoolData"> block in
index.html. Each row is:
  [name, city, state, in-state tuition & fees, out-of-state tuition & fees,
   on-campus room & board (0 if unknown), alias, undergrad enrollment]
"""
import csv
import json
import re
import sys


def num(v):
    return int(float(v)) if v not in ("", "NULL") else None


def extract(csv_path):
    rows = []
    with open(csv_path, newline="", encoding="utf-8", errors="replace") as f:
        for d in csv.DictReader(f):
            try:
                if d["PREDDEG"] != "3" or d.get("CURROPER") != "1":
                    continue
                ug = num(d["UGDS"]) or 0
                tout = num(d["TUITIONFEE_OUT"])
                if ug < 400 or tout is None:
                    continue
                tin = num(d["TUITIONFEE_IN"])
                alias = d.get("ALIAS", "")
                rows.append([
                    d["INSTNM"], d["CITY"], d["STABBR"],
                    tin if tin is not None else tout,
                    tout,
                    num(d["ROOMBOARD_ON"]) or 0,
                    "" if alias in ("NULL", "NA") else alias[:60],
                    ug,
                ])
            except (KeyError, ValueError):
                continue
    rows.sort(key=lambda x: x[0])
    return rows


def main():
    csv_path, html_path = sys.argv[1], sys.argv[2]
    rows = extract(csv_path)
    data = json.dumps(rows, separators=(",", ":")).replace("</", "<\\/")
    html = open(html_path, encoding="utf-8").read()
    pattern = r'(<script id="schoolData" type="application/json">).*?(</script>)'
    html, n = re.subn(pattern, lambda m: m.group(1) + data + m.group(2), html, count=1, flags=re.S)
    if n != 1:
        sys.exit("Could not find the schoolData block in " + html_path)
    open(html_path, "w", encoding="utf-8").write(html)
    print(f"Wrote {len(rows)} schools into {html_path}")


if __name__ == "__main__":
    main()
