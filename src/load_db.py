"""Load the cleaned items into a SQLite database so the analysis can be redone in SQL.

Input:  data/clean/items.csv
Output: data/pos.db   (one table: items)  -- stays private, like everything in data/

Run from the project folder:  python3 src/load_db.py
"""
import sqlite3
import pandas as pd

ITEMS = "data/clean/items.csv"
DB = "data/pos.db"

COLUMNS = [
    "ITEM_ID", "received", "sold", "sold_at", "days_to_sell", "price", "sold_price",
    "realized", "source", "cat1", "cat2", "cat3", "age_days", "entered_at_sale",
]

if __name__ == "__main__":
    items = pd.read_csv(ITEMS)[COLUMNS].rename(columns={"ITEM_ID": "item_id"})
    # SQLite has no true/false, so store them as 1/0
    items["sold"] = items.sold.astype(int)
    items["entered_at_sale"] = items.entered_at_sale.astype(int)

    with sqlite3.connect(DB) as con:
        items.to_sql("items", con, if_exists="replace", index=False)
        n = con.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    print(f"Loaded {n:,} rows into {DB}, table 'items'")
    print("Columns:", ", ".join(items.columns))
