-- 00: worked example (not checked). Read this one, then do 01.
--
-- Question: how many sofas are in the data, and what's their average tag price?
--
--   SELECT   picks the columns you want back. COUNT(*) counts rows, AVG() averages.
--   AS       names a result column. The checker looks for these names.
--   FROM     says which table. There's only one here: items.
--   WHERE    keeps only the rows that pass the test. Text goes in single quotes.
--
-- Result: sofas = 1942, plus their average tag.

SELECT
    COUNT(*)   AS sofas,
    AVG(price) AS avg_tag
FROM items
WHERE cat3 = 'Sofa';
