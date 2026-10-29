import os
import pandas as pd

ITEMS = "data/clean/items.csv"
COHORT_START = "2021-01-01"
MIN_AGE_DAYS = 365
CHECKPOINTS = [7, 14, 30, 60, 90, 180, 365]
WINDOWS = [(0, 14), (14, 30), (30, 60), (60, 90), (90, 180), (180, 365)]


def load_cohort():
    items = pd.read_csv(ITEMS, parse_dates=["received", "sold_at"])
    cohort = items[(items.received >= COHORT_START) & (items.age_days >= MIN_AGE_DAYS)
                   & ~items.entered_at_sale].copy()
    cohort["dts"] = cohort.days_to_sell.where(cohort.sold, float("inf"))
    return cohort


def sold_by(cohort):
    return pd.Series({d: (cohort.dts <= d).mean() for d in CHECKPOINTS}, name="share_sold")


def odds_by_age(cohort):
    rows = []
    for lo, hi in WINDOWS:
        still_there = cohort[cohort.dts > lo] if lo else cohort
        sold_in_window = (still_there.dts <= hi).sum()
        share = sold_in_window / len(still_there)
        per_30 = 1 - (1 - share) ** (30 / (hi - lo))
        rows.append({"days_on_floor": f"{lo}-{hi}", "still_unsold_at_start": len(still_there),
                     "sold_in_window": sold_in_window, "share": share, "per_30_days": per_30})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)
    cohort = load_cohort()
    print(f"Cohort: {len(cohort):,} items received {COHORT_START} or later, each with 1+ year of history\n")

    s = sold_by(cohort)
    print("Share sold by day X")
    print((s * 100).round(1).astype(str).add("%").to_string(), "\n")

    o = odds_by_age(cohort)
    print("Odds of selling, given it hasn't sold yet")
    print(o.assign(share=(o.share * 100).round(1), per_30_days=(o.per_30_days * 100).round(1)).to_string(index=False))

    by_source = pd.DataFrame({src: sold_by(g) for src, g in cohort.groupby("source")})
    by_source.loc["items"] = cohort.source.value_counts()
    print("\nShare sold by day X, by source")
    print(by_source.T.assign(**{str(d): lambda t, d=d: (t[d] * 100).round(1) for d in CHECKPOINTS})
          [["items"] + [str(d) for d in CHECKPOINTS]].to_string())

    s.to_csv("outputs/2a_share_sold_by_day.csv")
    by_source.to_csv("outputs/2a_share_sold_by_source.csv")
    o.to_csv("outputs/2a_odds_by_age.csv", index=False)
