-- what % sold within 30, 90 and 365 days?

SELECT
    AVG(CASE WHEN sold = 1 AND days_to_sell <= 30 THEN 100.0 ELSE 0 END) AS sold_30d,
    AVG(CASE WHEN sold = 1 AND days_to_sell <= 90 THEN 100.0 ELSE 0 END) AS sold_90d,
    AVG(CASE WHEN sold = 1 AND days_to_sell <= 365 THEN 100.0 ELSE 0 END) AS sold_365d
FROM items
WHERE received >= '2021-01-01'
  AND age_days >= 365
  AND entered_at_sale = 0;