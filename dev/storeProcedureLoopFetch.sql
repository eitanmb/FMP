DROP PROCEDURE IF EXISTS proc_cursor_getLastChangeOfYear;
DELIMITER $$
CREATE PROCEDURE proc_cursor_getLastChangeOfYear(
	fromYear int,
	toYear int
)
BEGIN
  DECLARE fecha varchar(100) DEFAULT "";
  DECLARE done INT DEFAULT FALSE;
  DECLARE cursor_years CURSOR FOR 
  SELECT DISTINCT(calendarYear) FROM incomeStatement where (calendarYear >= fromYear and calendarYear <= toYear);
  
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
  OPEN cursor_years;
  loop_through_rows: LOOP
    FETCH cursor_years INTO fecha;
    IF done THEN
      LEAVE loop_through_rows;
    END IF;
	SELECT * FROM forex WHERE date = LAST_DAY(CONCAT(fecha, '-12-01'));
 
  END LOOP;
  CLOSE cursor_years;
END;
$$

SET @desde = 2020;
SET @hasta = 2021;
CALL proc_cursor_getLastChangeOfYear(@desde, @hasta);