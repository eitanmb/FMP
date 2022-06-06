DROP PROCEDURE IF EXISTS proc_create_exRate_view;
DELIMITER $$
CREATE PROCEDURE proc_create_exRate_view()
BEGIN
DROP VIEW IF EXISTS exRate;
CREATE VIEW exRate as SELECT pair as Pair, SUBSTRING_INDEX(pair, "/", 1) as ReportedCurrency, year(date) as CalendarYear, close as Value
FROM tiposCambioView 
where SUBSTRING_INDEX(pair, "/", 1) <> 'USD'
order by reportedCurrency asc, date DESC;
END
$$


