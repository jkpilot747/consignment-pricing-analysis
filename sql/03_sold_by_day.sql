-- 03: Of that same group, what percent sold within 30, 90 and 365 days?
--
-- Return three columns named: sold_30d, sold_90d, sold_365d   (as percents, e.g. 38.4)
--
-- New idea: CASE WHEN turns a condition into a number.
--   CASE WHEN <condition> THEN 100.0 ELSE 0 END
-- gives 100 for rows that pass and 0 for rows that don't. The AVG of that
-- column is the percent of rows that pass.
--
-- An item "sold within 30 days" if sold = 1 AND days_to_sell <= 30.
-- Use the same WHERE as 02.
-- Check it:  python3 src/check_sql.py 03



SELECT
    AVG(CASE WHEN sold = 1 AND days_to_sell <= 30 THEN 100.0 ELSE 0 END) AS sold_30d,
    AVG(CASE WHEN sold = 1 AND days_to_sell <= 90 THEN 100.0 ELSE 0 END) AS sold_90d,
    AVG(CASE WHEN sold = 1 AND days_to_sell <= 365 THEN 100.0 ELSE 0 END) AS sold_365d
FROM items
WHERE received >= '2021-01-01'
  AND age_days >= 365
  AND entered_at_sale = 0;