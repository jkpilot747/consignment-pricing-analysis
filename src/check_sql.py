"""Check the SQL exercises against the Python analysis.

For each file in sql/, this runs the query on data/pos.db, recomputes the same
number(s) in pandas, and says whether they match. The two versions are written
completely separately, so when they agree, both are probably right.

Run from the project folder:
    python3 src/check_sql.py          # check every exercise
    python3 src/check_sql.py 03       # check one exercise
"""
import glob
import os
import sqlite3
import sys

import pandas as pd

from time_to_sell import load_cohort, sold_by
from breakdown import by_group
from price_vs_time import load_sold, summarize as price_summary

DB = "data/pos.db"
TOLERANCE = 0.1   # numbers can differ by rounding; anything bigger is a real mismatch


# ---- what each exercise should return, computed in pandas ------------------------

def expect_01():
    items = pd.read_csv("data/clean/items.csv")
    return pd.DataFrame({"items": [len(items)]})


def expect_02():
    return pd.DataFrame({"items": [len(load_cohort())]})


def expect_03():
    s = sold_by(load_cohort()) * 100
    return pd.DataFrame({"sold_30d": [s[30]], "sold_90d": [s[90]], "sold_365d": [s[365]]})


def expect_04():
    t = by_group(load_cohort(), "cat3", 50)
    return t.reset_index()[["cat3", "items", "sold_90d"]]


def expect_05():
    sold = load_sold()
    t = sold.groupby("days_bucket", observed=True).apply(price_summary).reset_index()
    t["days_bucket"] = t.days_bucket.astype(str)
    return t[["days_bucket", "items", "avg_pct_of_tag"]]


EXPECTED = {"01": expect_01, "02": expect_02, "03": expect_03, "04": expect_04, "05": expect_05}


# ---- comparison -------------------------------------------------------------------

def compare(got: pd.DataFrame, want: pd.DataFrame):
    missing = [c for c in want.columns if c not in got.columns]
    if missing:
        return False, f"your result is missing column(s): {', '.join(missing)}. Name them with AS."
    if len(got) != len(want):
        return False, f"your result has {len(got)} row(s), expected {len(want)}"
    problems = []
    for i in range(len(want)):
        for col in want.columns:
            g, w = got[col].iloc[i], want[col].iloc[i]
            if isinstance(w, (int, float)) and not isinstance(w, bool):
                if g is None or abs(float(g) - float(w)) > TOLERANCE:
                    problems.append(f"row {i + 1}, {col}: got {g}, expected {round(float(w), 2)}")
            elif str(g) != str(w):
                problems.append(f"row {i + 1}, {col}: got {g!r}, expected {w!r}")
    if problems:
        return False, "; ".join(problems[:5]) + (" ..." if len(problems) > 5 else "")
    return True, f"{len(want)} row(s) match"


def run(path, con):
    code = os.path.basename(path)[:2]
    sql = open(path).read()
    body = "\n".join(l for l in sql.splitlines() if not l.strip().startswith("--")).strip()
    name = os.path.basename(path)
    if code not in EXPECTED:
        return
    if not body:
        print(f"  {name}: not written yet")
        return
    try:
        got = pd.read_sql_query(body, con)
    except Exception as e:
        print(f"  {name}: SQL error: {e}")
        return
    ok, msg = compare(got, EXPECTED[code]())
    print(f"  {name}: {'MATCH' if ok else 'NO MATCH'} ({msg})")
    if not ok:
        print("    your first rows:\n" + got.head(5).to_string(index=False).replace("\n", "\n    "))


if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    files = sorted(f for f in glob.glob("sql/[0-9][0-9]_*.sql") if os.path.basename(f).startswith(only))
    with sqlite3.connect(DB) as con:
        for f in files:
            run(f, con)
