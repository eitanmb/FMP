CREATE PROCEDURE `proc_fx_outer`()
BEGIN
  DECLARE cursor_pair VARCHAR(20);
  DECLARE done INT DEFAULT FALSE;
  DECLARE cursor_forex_pair CURSOR FOR select DISTINCT(pair) from forex;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

  DROP TABLE IF EXISTS last_exchange_by_year_temp;
  CREATE TABLE last_exchange_by_year_temp SELECT pair,date,price FROM forex where MONTH(date) = 12;

  
   DROP TABLE IF EXISTS last_exchange_by_year;
   CREATE TABLE last_exchange_by_year(
    pair VARCHAR(255) NOT NULL,
    date DATE,
    close DOUBLE
   )  ENGINE=INNODB;

  OPEN cursor_forex_pair;
  loop1: LOOP
  FETCH cursor_forex_pair INTO cursor_pair;
    IF done THEN
      LEAVE loop1;
      CLOSE cursor_forex_pair;
    END IF;
    CALL proc_fx_inner(cursor_pair);
    
  END LOOP;
END


CREATE PROCEDURE `proc_fx_inner`(
    fx_pair varchar(20)
)
BEGIN
  DECLARE _from INT DEFAULT 2017;
  DECLARE _till INT DEFAULT 2020;
   
  SET _from = (SELECT MIN(YEAR(date)) from forex);
  SET _till = (SELECT MAX(YEAR(date)) from forex);

  WHILE _from <= _till DO
      INSERT INTO last_exchange_by_year (pair, date, close) SELECT * from last_exchange_by_year_temp where pair = fx_pair and Year(date) = _from LIMIT 1;
      SET _from = _from + 1;
  END WHILE;

END