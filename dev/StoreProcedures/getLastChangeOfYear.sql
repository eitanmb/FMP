PROCEDURE `proc_getLastChangeOfYear`(
	fromYear int,
	toYear int
)
BEGIN
   DECLARE _year INT DEFAULT fromYear;
   
   DROP TABLE IF EXISTS tiposDeCambioTable;
   CREATE TABLE tiposDeCambioTable (
    pair VARCHAR(255) NOT NULL,
    date DATE,
    close DOUBLE
	)  ENGINE=INNODB;
   
   
   WHILE _year <= toYear DO
	   INSERT INTO tiposDeCambioTable (pair, date, close) SELECT * from forex where date =(SELECT max(date) FROM forex WHERE date = _year);
       SET _year = _year + 1;
   END WHILE;
   
   DROP VIEW IF EXISTS tiposCambioView;
   CREATE VIEW tiposCambioView AS SELECT * FROM tiposDeCambioTable;
   
END