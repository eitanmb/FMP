SET @desde = 2017;
SET @hasta = 2021;
CALL proc_cursor_getLastChangeOfYear(@desde, @hasta);

SELECT * FROM tiposCambioView order by pair, date desc;