drop_stp_getLastChangeOfYear = f'DROP procedure IF EXISTS `proc_cursor_getLastChangeOfYear`;'

create_stp_getLastChangeOfYear = \
    f'CREATE DEFINER=`eitan`@`localhost` PROCEDURE `proc_cursor_getLastChangeOfYear`( \
        fromYear int, \
        toYear int \
    ) \
    BEGIN \
    DECLARE _year INT DEFAULT fromYear; \
        \
    DROP TABLE IF EXISTS tiposDeCambioTable; \
    CREATE TABLE tiposDeCambioTable ( \
        pair VARCHAR(255) NOT NULL, \
        date DATE, \
        close DOUBLE \
        )  ENGINE=INNODB; \
        \
        \
    WHILE _year <= toYear DO \
        INSERT INTO tiposDeCambioTable (pair, date, close) SELECT * from forex where date =(SELECT max(date) FROM forex WHERE date = _year); \
        SET _year = _year + 1; \
    END WHILE; \
        \
    DROP VIEW IF EXISTS tiposCambioView; \
    CREATE VIEW tiposCambioView AS SELECT * FROM tiposDeCambioTable; \
        \
    END'

drop_stp_to_exRate = f'DROP procedure IF EXISTS `proc_cursor_to_exRate`;'
create_stp_to_exRate = \
    f'CREATE DEFINER=`eitan`@`localhost` PROCEDURE `proc_cursor_to_exRate`() \
    BEGIN \
    DECLARE CURSOR_REPORTED_CURRENCY VARCHAR(10); \
    DECLARE CURSOR_CALENDAR_YEAR VARCHAR(10); \
    DECLARE CURSOR_VALUE DOUBLE; \
    DECLARE done INT DEFAULT FALSE; \
    DECLARE cursor_exRate CURSOR FOR SELECT ReportedCurrency, CalendarYear, Value FROM exRate; \
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE; \
    \
    DROP TABLE IF EXISTS fundamental_filters_selection_usd; \
    CREATE TABLE fundamental_filters_selection_usd AS SELECT * FROM fundamental_filters_selection; \
    \
    OPEN cursor_exRate; \
    loop_through_rows: LOOP \
        FETCH cursor_exRate INTO CURSOR_REPORTED_CURRENCY, CURSOR_CALENDAR_YEAR, CURSOR_VALUE; \
        IF done THEN \
        LEAVE loop_through_rows; \
        END IF; \
        UPDATE fundamental_filters_selection_usd \
        SET `Revenue`= `Revenue`*CURSOR_VALUE,  \
            `Cost Of Revenue`= `Cost Of Revenue`*CURSOR_VALUE,  \
            `Gross Profit`= `Gross Profit`*CURSOR_VALUE,  \
            `Research And Development Expenses`= `Research And Development Expenses`*CURSOR_VALUE,  \
            `General And Administrative Expenses`= `General And Administrative Expenses`*CURSOR_VALUE,  \
            `Selling And Marketing Expenses`= `Selling And Marketing Expenses`*CURSOR_VALUE,  \
            `Other Expenses`= `Other Expenses`*CURSOR_VALUE,  \
            `Operating Expenses`= `Operating Expenses`*CURSOR_VALUE,  \
            `Cost And Expenses`= `Cost And Expenses`*CURSOR_VALUE,  \
            `Interest Expense`= `Interest Expense`*CURSOR_VALUE,  \
            `Depreciation And Amortization`= `Depreciation And Amortization`*CURSOR_VALUE,  \
            `Operating Income`= `Operating Income`*CURSOR_VALUE,  \
            `Cash And Cash Equivalents`= `Cash And Cash Equivalents`*CURSOR_VALUE,  \
            `Net Receivables`= `Net Receivables`*CURSOR_VALUE,  \
            `Inventory`= `Inventory`*CURSOR_VALUE,  \
            `Total Current Assets`= `Total Current Assets`*CURSOR_VALUE,  \
            `Total Non Current Assets`= `Total Non Current Assets`*CURSOR_VALUE,  \
            `Total Assets`= `Total Assets`*CURSOR_VALUE,  \
            `Account Payables`= `Account Payables`*CURSOR_VALUE,  \
            `Total Current Liabilities`= `Total Current Liabilities`*CURSOR_VALUE,  \
            `Total Non Current Liabilities`= `Total Non Current Liabilities`*CURSOR_VALUE,  \
            `Total Liabilities`=`Total Liabilities`*CURSOR_VALUE \
            WHERE Year = CURSOR_CALENDAR_YEAR and `Reported Currency` = CURSOR_REPORTED_CURRENCY ; \
    END LOOP; \
    CLOSE cursor_exRate; \
    END'

drop_stp_to_usd = f'DROP procedure IF EXISTS `proc_report_to_usd`;'
create_stp_to_usd = \
    f'CREATE DEFINER=`eitan`@`localhost` PROCEDURE `proc_report_to_usd`( \
        desde INT,  \
        hasta INT \
    ) \
    BEGIN \
    CALL proc_cursor_getLastChangeOfYear(desde,hasta); \
    DROP VIEW IF EXISTS exRate; \
    CREATE VIEW exRate as SELECT pair as Pair, SUBSTRING_INDEX(pair, "/", 1) as ReportedCurrency, year(date) as CalendarYear, close as Value \
    FROM tiposCambioView WHERE SUBSTRING_INDEX(pair, "/", 1) <> "USD" ORDER BY reportedCurrency asc, date DESC; \
    CALL proc_cursor_to_exRate(); \
    END'

stp_getLastChangeOfYear = {
    'drop': drop_stp_getLastChangeOfYear,
    'create': create_stp_getLastChangeOfYear,
    'name': 'getLastChangeOfYear'
}

stp_to_exRate = {
    'drop': drop_stp_to_exRate,
    'create': create_stp_to_exRate,
    'name': 'to_exRate'
}

stp_to_usd = {
    'drop': drop_stp_to_usd,
    'create': create_stp_to_usd,
    'name': 'to_usd'
}