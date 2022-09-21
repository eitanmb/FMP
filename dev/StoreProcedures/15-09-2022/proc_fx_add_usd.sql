CREATE DEFINER = `eitan` @`localhost` PROCEDURE `proc_fx_add_usd`() BEGIN DECLARE _from INT DEFAULT 2017;
DECLARE _till INT DEFAULT 2020;
SET _from = (SELECT MIN(YEAR(date)) from forex);
SET _till = (SELECT MAX(YEAR(date)) from forex);
WHILE _from <= _till DO
INSERT INTO last_exchange_by_year (pair, date, close) SELECT 'USDUSD', date, 1
from last_exchange_by_year_temp
where YEAR(date) = _from limit 1;
SET _from = _from + 1;
END WHILE;
END