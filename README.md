# Consignment Furniture: Pricing and Time-to-Sell Analysis

## Overview

I wanted to know what sells at the store I work at, and how long that usually takes. The short answer: an item's best chance of selling is its first month. Almost 4 in 10 pieces sell in 30 days. After six months on the floor the odds drop to about 4% a month, and the longer something sits, the less of its tag it brings in.

The store is a furniture and antiques consignment shop where I work on e-commerce and operations. For this project I pulled 17 years of point-of-sale data out of Liberty Consignment POS (85,436 rows, 2009 to September 2026) to answer two questions:

1. How fast do things sell, and what does waiting cost in price?
2. Can we predict sale price and time to sell when an item comes in? (the next part of this project)

## Data and method

I cleaned the export in Python (with pandas), loaded it into SQLite, and wrote the main counts and rates as SQL queries alongside the pandas analysis. Charts were done with matplotlib.

The export has a row when an item is entered plus a row for every sale or refund, so I collapsed it to one row per item and removed multi-quantity entries, unpriced items and anything marked "Needs Info". An item counts as sold if its sales minus refunds is above zero. I also split items by source: owned by the store, consigned, or new vendor stock.

Most of the numbers below use the 7,489 items that came in from January 2021 on and have had at least a year to sell, so the results reflect how the store runs now.

Consignor IDs are hashed, names are removed, and no row-level data is public. The repo only has code and charts.

## Finding 1: the first month matters most

Almost 4 in 10 pieces (38%) sell in the first 30 days, 58% by day 90 and 76% by the end of the year.

![How fast things sell](outputs/figures/1_how_fast_things_sell.png)

For items still on the floor, the odds of selling in the next 30 days fall fast: about 49% a month in the first two weeks, 28% in weeks three and four, and 4% after six months.

![Odds of selling by days on the floor](outputs/figures/2_odds_of_selling.png)

So if something hasn't sold by 60 to 90 days, it probably won't sell at that price anytime soon. That's the point to mark it down, move it somewhere else on the floor, or let the consignor know.

## Finding 2: waiting costs money

Items that sell in the first week bring in 95% of tag on average. After a year it's about 80%, mostly from discounting. Full-price sales fall even faster: 68% of first-week sales are at full tag, compared with 30% after a year. Typical tag prices are about the same in every group, so this isn't just cheap stuff selling first.

![What waiting costs](outputs/figures/3_what_waiting_costs.png)

## Finding 3: what sells fastest

Big furniture sells fastest and art sells slowest. Sectionals led with 81% sold within 90 days, against 58% overall, and dressers, bookcases, credenzas and sideboards were all over 70%. Fine art, framed art and misc. art were all under 40%, and rugs, ottomans, ceramics and lighting under 50%. Most of the art is consigned, which lines up with what the owner already does: he rarely buys art for the store because it doesn't move.

![What sells fast, by category](outputs/figures/4_by_category.png)

Price mattered less than I expected. Most price ranges sell at about the same rate (54% to 61% within 90 days). Only the most expensive pieces are slower, and they hold less of their tag: 85% on average, compared with 94% for the cheapest.

For brands, the mainstream contemporary names sell fastest: West Elm 84%, Crate & Barrel 83%, Article 82% and Room & Board 75% within 90 days. Timothy Oulton, Muuto, Gus Modern, Knoll and Restoration Hardware were around 50% or lower. Orange bars are brands that are mostly the store's own or new vendor stock (Article, Blu Dot, Muuto, Timothy Oulton and Gus).

![What sells fast, by brand](outputs/figures/5_by_brand.png)

Brands are tagged by searching item descriptions, so a piece only counts if whoever entered it wrote the brand down. Only brands with 30+ items are shown.

## Gaps

- Some high-ticket pieces sell through auctions and never go through Liberty, so some of the store's best finds aren't in here.
- When a tag price gets lowered in the system, the original price is lost, so the discounts above are a minimum.
- Pieces sold within 15 minutes of being entered (usually entered at the register before they could be tagged) are left out of the timing numbers.
- Items never closed out in the system count as unsold, so sell rates are probably a little low.
- Some store and vendor accounts are labeled as consignors. I relabeled the main ones with the owner's help, but the split isn't exact, so I didn't compare consigned items to store-owned ones.

## What happened next

I shared the findings with the owner in a simple dashboard. The work also turned up some problems with how items get entered into the POS, and those have been fixed. He plans to focus more on the fastest-selling categories when sourcing and be pickier about the slow ones.

To see if that changes anything, I'm tracking it against a baseline. Over the last three years, about 20% of intake came from the fast categories and about 20% from the slow ones. I'll check intake again in December, and 30- and 90-day sell-through in February. After that, the next project is the price predictor.

## Running it

Run from the project folder: `src/clean.py`, `src/load_db.py`, `src/time_to_sell.py`, `src/price_vs_time.py`, `src/breakdown.py`, `src/plots.py`. The queries in `sql/` run against the database `load_db.py` builds. The raw Liberty export is not included.
