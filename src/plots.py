"""Charts for steps 2a-2c. Reads the CSVs the analysis scripts wrote to outputs/
(plus the cleaned items for the daily curve) and saves PNGs to outputs/figures/.

Run from the project folder, after the analysis scripts:  python3 src/plots.py
"""
import os
import matplotlib.pyplot as plt
import pandas as pd

from time_to_sell import load_cohort

OUT = "outputs/figures"
BLUE, ORANGE = "#2a78d6", "#eb6834"
INK, MUTED, GRID = "#1f1f1d", "#6b6a66", "#e6e5e1"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 10,
    "axes.edgecolor": MUTED, "axes.labelcolor": MUTED,
    "xtick.color": MUTED, "ytick.color": MUTED, "text.color": INK,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8,
    "axes.axisbelow": True,
    "figure.dpi": 100, "savefig.dpi": 200, "savefig.bbox": "tight",
})


def title(ax, main, sub):
    ax.set_title(main, loc="left", fontsize=13, fontweight="bold", pad=24)
    ax.annotate(sub, (0, 1), xycoords="axes fraction", xytext=(0, 8),
                textcoords="offset points", fontsize=9.5, color=MUTED)


def pct_axis(axis):
    axis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}%"))


def fig_sell_curve(cohort):
    """2a: share of items sold by each day, 0-365."""
    days = range(0, 366)
    share = [(cohort.dts <= d).mean() * 100 for d in days]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(days, share, color=BLUE, linewidth=2)
    for d in (30, 90, 180, 365):
        ax.plot(d, share[d], "o", color=BLUE, markersize=7, markeredgecolor="white", markeredgewidth=2)
        ax.annotate(f"{share[d]:.0f}% by day {d}", (d, share[d]), xytext=(6, -14),
                    textcoords="offset points", fontsize=9, color=INK)
    ax.set_xlim(0, 380); ax.set_ylim(0, 100); pct_axis(ax.yaxis)
    ax.set_xticks([0, 30, 60, 90, 180, 270, 365]); ax.set_xlabel("Days on the floor")
    title(ax, "How fast things sell",
          f"Share of items sold, by days since intake ({len(cohort):,} items received 2021 or later)")
    fig.savefig(f"{OUT}/1_how_fast_things_sell.png"); plt.close(fig)


def fig_odds():
    """2a: chance of selling in the next 30 days, given still unsold."""
    o = pd.read_csv("outputs/2a_odds_by_age.csv")
    labels = ["First 2 weeks", "Days 14-30", "Days 30-60", "Days 60-90", "Days 90-180", "Days 180-365"]
    vals = o.per_30_days * 100
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(labels, vals, color=BLUE, width=0.6)
    ax.bar_label(bars, labels=[f"{v:.0f}%" for v in vals], padding=3, fontsize=9, color=INK)
    ax.set_ylim(0, 60); pct_axis(ax.yaxis); ax.grid(axis="x", visible=False)
    title(ax, "The longer it sits, the less likely it sells",
          "Chance an unsold item sells in the next 30 days, by how long it has been on the floor")
    fig.savefig(f"{OUT}/2_odds_of_selling.png"); plt.close(fig)


def fig_price():
    """2b: sold price as % of tag, and share sold at full tag, by days on floor."""
    p = pd.read_csv("outputs/2b_price_by_days.csv")
    x = range(len(p))
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for col, color, name in [("avg_pct_of_tag", BLUE, "Avg sold price, % of tag"),
                             ("share_at_full_price", ORANGE, "Share sold at full tag")]:
        ax.plot(x, p[col], color=color, linewidth=2, marker="o", markersize=7,
                markeredgecolor="white", markeredgewidth=2, label=name)
        for i in (0, len(p) - 1):
            ax.annotate(f"{p[col][i]:.0f}%", (i, p[col][i]), xytext=(0, 9),
                        textcoords="offset points", ha="center", fontsize=9, color=INK)
    ax.set_xticks(list(x), p.days_bucket); ax.set_xlabel("Days on the floor before selling")
    ax.set_ylim(0, 105); pct_axis(ax.yaxis)
    ax.legend(frameon=False, loc="lower left")
    title(ax, "What waiting costs",
          "Items sold 2021 or later. Discounts are a minimum: some markdowns overwrite the tag")
    fig.savefig(f"{OUT}/3_what_waiting_costs.png"); plt.close(fig)


def ranked_bars(t, name_col, fname, main, sub, baseline, color_by_new=False):
    t = t.sort_values("sold_90d")
    colors = [ORANGE if color_by_new and c < 30 else BLUE for c in t.pct_consignment]
    fig, ax = plt.subplots(figsize=(8, 0.28 * len(t) + 1.6))
    bars = ax.barh(t[name_col], t.sold_90d, color=colors, height=0.65)
    ax.axvline(baseline, color=INK, linewidth=1, linestyle=(0, (4, 3)), zorder=1)
    ax.bar_label(bars, labels=[f"{v:.0f}%" for v in t.sold_90d], padding=3, fontsize=8.5, color=MUTED,
                 bbox=dict(facecolor="white", edgecolor="none", pad=0.6), zorder=3)
    ax.text(baseline + 1, len(t) - 0.4, f"All items {baseline:.0f}%", fontsize=8.5, color=INK)
    ax.set_xlim(0, 100); pct_axis(ax.xaxis); ax.grid(axis="y", visible=False)
    ax.tick_params(axis="y", length=0)
    if color_by_new:
        from matplotlib.patches import Patch
        ax.legend(handles=[Patch(color=BLUE, label="Mostly consignment / used"),
                           Patch(color=ORANGE, label="Mostly new vendor stock")],
                  frameon=False, loc="lower right")
    title(ax, main, sub)
    fig.savefig(f"{OUT}/{fname}"); plt.close(fig)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    cohort = load_cohort()
    baseline = (cohort.dts <= 90).mean() * 100

    fig_sell_curve(cohort)
    fig_odds()
    fig_price()
    ranked_bars(pd.read_csv("outputs/2c_by_category.csv"), "cat3", "4_by_category.png",
                "What sells fast, by category", "Share sold within 90 days (categories with 50+ items)",
                baseline)
    brands = pd.read_csv("outputs/2c_by_brand.csv").rename(columns={"Unnamed: 0": "brand"})
    ranked_bars(brands, "brand", "5_by_brand.png",
                "What sells fast, by brand", "Share sold within 90 days (brands named in 30+ item descriptions)",
                baseline, color_by_new=True)
    print("Saved:", *sorted(os.listdir(OUT)), sep="\n  ")
