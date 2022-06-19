CREATE OR REPLACE VIEW FMP_2022_06.forex_hist AS 
SELECT * from FMP_2022_06.forex
UNION DISTINCT
SELECT * from FMP_2022_05.forex
UNION DISTINCT
SELECT * from FMP_2022_04.forex 
UNION DISTINCT
SELECT * from FMP_2022_03.forex
UNION DISTINCT
SELECT * from FMP_2021_05.forex
where FMP_2021_05.forex.pair not like "%/=%"
ORDER BY date, pair