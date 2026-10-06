-- 04: For each category (cat3), how many items and what percent sold within 90 days?
--
-- Return columns named: cat3, items, sold_90d
-- Only categories with at least 50 items. Fastest-selling first.
--
-- New ideas:
--   GROUP BY cat3        runs your COUNT and AVG once per category instead of once overall
--   HAVING COUNT(*) >= 50 is like WHERE, but filters groups after they're counted
--   ORDER BY sold_90d DESC sorts, biggest first
--
-- Same group of items as 02 and 03.
-- Check it:  python3 src/check_sql.py 04

SELECT cat3
    AVG(CASE WHEN sold = 1 AND days_to_sell <= 30 THEN 100.0 ELSE 0 END) AS sold_30d,
    AVG(CASE WHEN sold = 1 AND days_to_sell <= 90 THEN 100.0 ELSE 0 END) AS sold_90d,
    AVG(CASE WHEN sold = 1 AND days_to_sell <= 365 THEN 100.0 ELSE 0 END) AS sold_365d
FROM items
WHERE received >= '2021-01-01'
  AND age_days >= 365
  AND entered_at_sale = 0
GROUP BY cat3
HAVING COUNT(*) >= 50
ORDER BY sold_90d DESC;