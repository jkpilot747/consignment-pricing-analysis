-- for each category, how many items and what percent sold within 90 days?

SELECT
    cat3,
    COUNT(*) AS items,
    AVG(CASE WHEN sold = 1 AND days_to_sell <= 90 THEN 100.0 ELSE 0 END) AS sold_90d
FROM items
WHERE received >= '2021-01-01'
  AND age_days >= 365
  AND entered_at_sale = 0
GROUP BY cat3
HAVING COUNT(*) >= 50
ORDER BY sold_90d DESC;
