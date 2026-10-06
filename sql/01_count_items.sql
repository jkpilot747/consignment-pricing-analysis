-- 01: How many items are in the table?
--
-- Return one column named: items
-- Hint: same shape as the example, with no WHERE.
-- Check it:  python3 src/check_sql.py 01

SELECT
    COUNT(*) AS items
FROM items;