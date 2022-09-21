CREATE DEFINER = `eitan` @`localhost` PROCEDURE `proc_fx_outer`() BEGIN DECLARE cursor_pair VARCHAR(20);
DECLARE done INT DEFAULT FALSE;
DECLARE cursor_forex_pair CURSOR FOR
select
    DISTINCT(pair)
from
    forex;
DECLARE CONTINUE HANDLER FOR NOT FOUND
SET
    done = TRUE;
DROP TABLE IF EXISTS last_exchange_by_year_temp;
CREATE TABLE last_exchange_by_year_temp
SELECT
    pair,
    date,
    price
FROM
    forex
where
    MONTH(date) = 12;
DROP TABLE IF EXISTS last_exchange_by_year;
CREATE TABLE last_exchange_by_year(
    pair VARCHAR(255) NOT NULL,
    date DATE,
    close DOUBLE
) ENGINE = INNODB;
OPEN cursor_forex_pair;
loop1: LOOP FETCH cursor_forex_pair INTO cursor_pair;
IF done THEN LEAVE loop1;
CLOSE cursor_forex_pair;
END IF;
CALL proc_fx_inner(cursor_pair);
END LOOP;
CALL proc_fx_add_usd();
DROP TABLE IF EXISTS last_exchange_by_year_temp;
END