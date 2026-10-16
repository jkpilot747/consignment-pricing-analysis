
--counting how many items in the analysis group

SELECT
    COUNT(*) AS items
FROM items
WHERE received >= '2021-01-01'
  AND age_days >= 365
  AND entered_at_sale = 0 ;