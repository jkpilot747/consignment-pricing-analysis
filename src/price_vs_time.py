"""Step 2b: what does waiting cost in price?

For every sold item, compare the sold price to the tag price, then group by
how long the item sat before selling.

Caveat: sometimes the tag price itself gets lowered in the system, which erases
the original price. So this measures the discount AT LEAST; the real one is
bigger for some items.

Run from the project folder:  python3 src/price_vs_time.py
"""
import os
import pandas as pd

ITEMS = "data/clean/items.csv"
START = "2021-01-01"
BUCKETS = [-1, 7, 30, 60, 90, 180, 365, 100_000]
LABELS = ["0-7", "8-30", "31-60", "61-90", "91-180", "181-365", "365+"]


def load_sold():
    items = pd.read_csv(ITEMS, parse_dates=["received", "sold_at"])
    sold = items[items.sold & (items.received >= START) & ~items.entered_at_sale].copy()
    # a few typos (sold for 10x tag, or a tiny fraction of it); cap so they can't skew averages
    sold["pct_of_tag"] = sold.realized.clip(0, 1.2)
    sold["days_bucket"] = pd.cut(sold.days_to_sell, BUCKETS, labels=LABELS)
    return sold


def summarize(df):
    return pd.Series({
        "items": len(df),
        "median_pct_of_tag": df.pct_of_tag.median() * 100,
        "avg_pct_of_tag": df.pct_of_tag.mean() * 100,
        "share_at_full_price": (df.pct_of_tag >= 0.99).mean() * 100,
        "median_tag": df.price.median(),
    })


if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)
    sold = load_sold()
    print(f"{len(sold):,} items sold, received {START} or later\n")

    overall = sold.groupby("days_bucket", observed=True).apply(summarize)
    print("Sold price as % of tag, by days on the floor")
    print(overall.round(1).to_string(), "\n")

    for src, grp in sold.groupby("source"):
        t = grp.groupby("days_bucket", observed=True).apply(summarize)
        print(f"{src}")
        print(t[["items", "avg_pct_of_tag", "share_at_full_price"]].round(1).to_string(), "\n")

    overall.to_csv("outputs/2b_price_by_days.csv")
