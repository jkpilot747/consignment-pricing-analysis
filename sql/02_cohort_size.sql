-- 02: How many items are in the analysis group from step 2a?
--
-- The group is items that:
--   - were received on or after 2021-01-01   (received is text like '2021-03-14 10:22:05',
--                                             and text dates compare correctly with >=)
--   - have been in the data at least a year   (age_days >= 365)
--   - were NOT entered at the register         (entered_at_sale = 0)
--
-- Return one column named: items
-- Hint: WHERE with three conditions joined by AND.
-- Check it:  python3 src/check_sql.py 02

SELECT
    COUNT(*) AS items
FROM items
WHERE received >= '2021-01-01'
  AND age_days >= 365
  AND entered_at_sale = 0 ;