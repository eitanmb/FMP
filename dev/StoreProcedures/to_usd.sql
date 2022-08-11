CREATE DEFINER=`eitan`@`localhost` PROCEDURE `proc_report_to_usd`(
	desde INT, 
    hasta INT
)
BEGIN
CALL proc_cursor_getLastChangeOfYear(desde,hasta);

DROP VIEW IF EXISTS exRate;
CREATE VIEW exRate as SELECT pair as Pair, SUBSTRING_INDEX(pair, "/", 1) as ReportedCurrency, year(date) as CalendarYear, close as Value
FROM tiposCambioView WHERE SUBSTRING_INDEX(pair, "/", 1) <> 'USD'ORDER BY reportedCurrency asc, date DESC;

CALL proc_cursor_to_exRate();

END