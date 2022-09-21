CREATE DEFINER = `eitan` @`localhost` PROCEDURE `proc_fx_exRate`() BEGIN DROP VIEW IF EXISTS exRate;
CREATE VIEW exRate as SELECT pair as Pair, SUBSTRING(pair, 4) as ReportedCurrency, date as `Date`, year(date) as CalendarYear, close as Value
FROM last_exchange_by_year WHERE close <> 0 ORDER BY reportedCurrency asc, date DESC;
END