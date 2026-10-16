-- for items that sold, what's the average sold price as a percent of tag,
-- grouped by how long they took to sell?

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