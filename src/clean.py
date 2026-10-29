import hashlib
import pandas as pd

RAW = "data/raw/liberty_full.csv"
OUT = "data/clean/items.csv"
FMT = "%m/%d/%Y %I:%M:%S %p"
DATA_END = pd.Timestamp("2026-09-18 23:59")

ACCOUNTS = "data/raw/accounts_review.csv"
QUICK_SALE_MINUTES = 15

LABELS = {"house": "Owned", "vendor": "New (vendor)", "consignment": "Consignment",
          "exclude": "Exclude", "house?": "Consignment"}


def load_raw(path=RAW):
    df = pd.read_csv(path, low_memory=False, encoding="utf-8-sig")
    df["rt"] = pd.to_datetime(df.RECEIVE_TS, format=FMT)
    df["st"] = pd.to_datetime(df.SALE_TS, format=FMT)
    return df


def load_salt(path="data/raw/salt.txt"):
    import os, secrets
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(secrets.token_hex(16))
    return open(path).read().strip()


def load_account_labels(path=ACCOUNTS):
    acc = pd.read_csv(path)
    label = acc.confirmed.fillna("").str.strip().str.lower()
    label = label.where(label != "", acc.claude_guess)
    return dict(zip(acc.client_id, label.map(LABELS)))


def build_items(df):
    g = df.groupby("ITEM_ID")
    units = g.QTY_ON_HAND.max() + g.QtyUnavail.max()

    base = g.agg(
        client=("CLIENT_ID", "first"),
        client_type=("CLIENT_TYPE_ID", "first"),
        received=("rt", "first"),
        price=("PRICE", "first"),
        name=("ITEM_NAME", "first"),
        desc=("ITEM_DESC", "first"),
        cat1=("CAT_L1_NAME", "first"),
        cat2=("CAT_L2_NAME", "first"),
        cat3=("CAT_L3_NAME", "first"),
        md_code=("OLD_MARKDOWN_CD", "first"),
        store_pct=("STORE_PCT", "first"),
        status=("STATUS_DESC", "last"),
    )
    base["units"] = units

    sold = df[df.DISPOSITION == "Sold"].drop_duplicates(["ITEM_ID", "receipt_num", "st"])
    refunds = df[df.DISPOSITION == "Refund"].groupby("ITEM_ID").size()
    n_sold = sold.groupby("ITEM_ID").size()
    last_sale = sold.sort_values("st").groupby("ITEM_ID").last()[["st", "PRICE_SOLD"]]

    base["net_sales"] = n_sold.reindex(base.index).fillna(0) - refunds.reindex(base.index).fillna(0)
    base = base.join(last_sale)
    base["sold"] = base.net_sales > 0
    base.loc[~base.sold, ["st", "PRICE_SOLD"]] = pd.NA
    base = base.rename(columns={"st": "sold_at", "PRICE_SOLD": "sold_price"})

    labels = load_account_labels()
    base["source"] = base.client.map(labels).fillna("Consignment")
    base = base[base.source != "Exclude"]
    base["days_to_sell"] = (base.sold_at - base.received).dt.days
    base["realized"] = base.sold_price / base.price
    minutes = (base.sold_at - base.received).dt.total_seconds() / 60
    base["entered_at_sale"] = base.sold & (minutes <= QUICK_SALE_MINUTES)
    base["age_days"] = (DATA_END - base.received).dt.days

    keep = (base.units <= 1) & (base.price > 0) & (base.status != "Needs Info")
    keep &= ~(base.sold & (base.days_to_sell < 0))
    items = base[keep].copy()

    salt = load_salt()
    items["consignor"] = items.client.map(
        lambda c: hashlib.sha256(f"{salt}-{c}".encode()).hexdigest()[:10])
    items = items.drop(columns=["client"])
    return items.reset_index()


if __name__ == "__main__":
    import os
    os.makedirs("data/clean", exist_ok=True)
    items = build_items(load_raw())
    items.to_csv(OUT, index=False)
    print(items.shape)
    print(items.source.value_counts())
    print("sold share", items.sold.mean().round(3))
    print("entered at sale (excluded from time-to-sell)", items.entered_at_sale.sum())
