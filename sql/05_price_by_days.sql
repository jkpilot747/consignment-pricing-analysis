-- 05 (harder): For items that SOLD, what's the average sold price as a percent of tag,
-- grouped by how long they took to sell?
--
-- Return columns named: days_bucket, items, avg_pct_of_tag
-- Buckets, exactly these labels, in this order:
--   '0-7', '8-30', '31-60', '61-90', '91-180', '181-365', '365+'
--
-- Which items: sold = 1, received on or after 2021-01-01, entered_at_sale = 0
--   (no age_days filter here, same as step 2b)
--
-- Two new pieces:
--   1. Make the bucket with a CASE that has several WHEN lines:
--        CASE WHEN days_to_sell <= 7 THEN '0-7'
--             WHEN days_to_sell <= 30 THEN '8-30'
--             ... ELSE '365+' END
--   2. A few typos (sold for 10x the tag) would skew the average, so the Python caps
--      realized at 1.2. In SQLite: MIN(MAX(realized, 0), 1.2). Multiply by 100 for a percent.
--
-- To get the buckets in order, ORDER BY MIN(days_to_sell).
-- Check it:  python3 src/check_sql.py 05

SELECT
    CASE WHEN days_to_sell <= 7  THEN '0-7'
         WHEN days_to_sell <= 30 THEN '8-30'
         WHEN days_to_sell <= 60 THEN '31-60'
         WHEN days_to_sell <= 90 THEN '61-90'
         WHEN days_to_sell <= 180 THEN '91-180'
         WHEN days_to_sell <= 365 THEN '181-365'
         ELSE '365+'
    END AS days_bucket,
    COUNT(*) AS items,
    AVG(MIN(MAX(realized, 0), 1.2)) * 100 AS avg_pct_of_tag
FROM items
WHERE sold = 1
  AND received >= '2021-01-01'
  AND entered_at_sale = 0
GROUP BY days_bucket
ORDER BY MIN(days_to_sell);