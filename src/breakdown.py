"""Step 2c: what sells fast and what sits?

Same group of items as step 2a (received 2021+, a full year of history,
entered-at-sale excluded), split three ways:
  - by category (Liberty's most detailed level, e.g. Sofa, Rug, Lamp)
  - by tag price range
  - by brand / style keyword found in the description (src/brands.py)

For each group: how many items, share sold by day 30 / 90 / 365, and for the
ones that sold, average % of tag. Groups with too few items are dropped
because a handful of pieces can swing the percentages.

Run from the project folder:  python3 src/breakdown.py
"""
import os
import pandas as pd

from time_to_sell import load_cohort
from brands import BRANDS, STYLES, tag

MIN_ITEMS_CATEGORY = 50
MIN_ITEMS_BRAND = 30
PRICE_BANDS = [0, 100, 250, 500, 1000, 2000, 1_000_000]
PRICE_LABELS = ["<100", "100-250", "250-500", "500-1k", "1k-2k", "2k+"]


def summarize(df):
    sold = df[df.sold]
    return pd.Series({
        "items": len(df),
        "sold_30d": (df.dts <= 30).mean() * 100,
        "sold_90d": (df.dts <= 90).mean() * 100,
        "sold_365d": (df.dts <= 365).mean() * 100,
        "avg_pct_of_tag": sold.realized.clip(0, 1.2).mean() * 100,
        "median_tag": df.price.median(),
        "pct_consignment": (df.source == "Consignment").mean() * 100,
    })


def by_group(cohort, key, min_items):
    t = cohort.groupby(key, observed=True).apply(summarize)
    return t[t["items"] >= min_items].sort_values("sold_90d", ascending=False)


def by_keywords(cohort, patterns, min_items):
    hits = tag(cohort.desc, patterns)
    rows = {name: summarize(cohort[hits[name]]) for name in patterns if hits[name].sum() >= min_items}
    return pd.DataFrame(rows).T.sort_values("sold_90d", ascending=False)


if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)
    cohort = load_cohort()
    cohort["price_band"] = pd.cut(cohort.price, PRICE_BANDS, labels=PRICE_LABELS)

    baseline = summarize(cohort)
    print(f"All {len(cohort):,} items: sold by day 30 {baseline.sold_30d:.0f}%, "
          f"day 90 {baseline.sold_90d:.0f}%, day 365 {baseline.sold_365d:.0f}%\n")

    tables = {
        "category": by_group(cohort, "cat3", MIN_ITEMS_CATEGORY),
        "price_band": by_group(cohort, "price_band", 1).sort_index(),
        "brand": by_keywords(cohort, BRANDS, MIN_ITEMS_BRAND),
        "style": by_keywords(cohort, STYLES, MIN_ITEMS_BRAND),
    }
    for name, t in tables.items():
        print(f"By {name}")
        print(t.round(0).astype(int).to_string(), "\n")
        t.to_csv(f"outputs/2c_by_{name}.csv")
