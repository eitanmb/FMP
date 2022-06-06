DROP PROCEDURE IF EXISTS proc_cursor_getLastChangeOfYear;
DELIMITER $$
CREATE PROCEDURE proc_cursor_getLastChangeOfYear(
	fromYear int,
	toYear int
)
BEGIN
   DECLARE _year INT DEFAULT fromYear;
   
   DROP TABLE IF EXISTS tiposDeCambio;
   CREATE TABLE tiposDeCambio (
    pair VARCHAR(255) NOT NULL,
    date DATE,
    clouse DOUBLE
	)  ENGINE=INNODB;
   
   WHILE _year <= toYear DO
	   SELECT * from forex where date =(SELECT max(date) FROM forex WHERE date = _year);
       SET _year = _year + 1;
   END WHILE;
END;
$$

SET @desde = 2017;
SET @hasta = 2021;
CALL proc_cursor_getLastChangeOfYear(@desde, @hasta);

