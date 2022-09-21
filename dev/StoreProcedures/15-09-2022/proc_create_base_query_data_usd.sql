CREATE DEFINER = `eitan` @`localhost` PROCEDURE `proc_create_base_query_data_usd`() BEGIN DECLARE CURSOR_REPORTED_CURRENCY VARCHAR(10);
DECLARE CURSOR_CALENDAR_YEAR VARCHAR(10);
DECLARE CURSOR_VALUE DOUBLE;
DECLARE done INT DEFAULT FALSE;
DECLARE cursor_exRate CURSOR FOR
SELECT
	ReportedCurrency,
	CalendarYear,
	Value
FROM
	exRate;
DECLARE CONTINUE HANDLER FOR NOT FOUND
SET
	done = TRUE;
DROP TABLE IF EXISTS base_query_data_usd;
CREATE TABLE base_query_data_usd AS
SELECT
	*
FROM
	base_query_data;
ALTER TABLE
	base_query_data_usd
ADD
	COLUMN `Indexed` TINYINT NULL DEFAULT 0
AFTER
	`Year`;
OPEN cursor_exRate;
loop_through_rows: LOOP FETCH cursor_exRate INTO CURSOR_REPORTED_CURRENCY,
CURSOR_CALENDAR_YEAR,
CURSOR_VALUE;
IF done THEN CLOSE cursor_exRate;
LEAVE loop_through_rows;
END IF;
UPDATE
	base_query_data_usd
SET
	`Revenue` = `Revenue` / CURSOR_VALUE,
	`Cost Of Revenue` = `Cost Of Revenue` / CURSOR_VALUE,
	`Gross Profit` = `Gross Profit` / CURSOR_VALUE,
	`Research And Development Expenses` = `Research And Development Expenses` / CURSOR_VALUE,
	`General And Administrative Expenses` = `General And Administrative Expenses` / CURSOR_VALUE,
	`Selling And Marketing Expenses` = `Selling And Marketing Expenses` / CURSOR_VALUE,
	`Other Expenses` = `Other Expenses` / CURSOR_VALUE,
	`Operating Expenses` = `Operating Expenses` / CURSOR_VALUE,
	`Cost And Expenses` = `Cost And Expenses` / CURSOR_VALUE,
	`Interest Expense` = `Interest Expense` / CURSOR_VALUE,
	`Depreciation And Amortization` = `Depreciation And Amortization` / CURSOR_VALUE,
	`Operating Income` = `Operating Income` / CURSOR_VALUE,
	`Cash And Cash Equivalents` = `Cash And Cash Equivalents` / CURSOR_VALUE,
	`Net Receivables` = `Net Receivables` / CURSOR_VALUE,
	`Inventory` = `Inventory` / CURSOR_VALUE,
	`Total Current Assets` = `Total Current Assets` / CURSOR_VALUE,
	`Total Non Current Assets` = `Total Non Current Assets` / CURSOR_VALUE,
	`Total Assets` = `Total Assets` / CURSOR_VALUE,
	`Account Payables` = `Account Payables` / CURSOR_VALUE,
	`Total Current Liabilities` = `Total Current Liabilities` / CURSOR_VALUE,
	`Total Non Current Liabilities` = `Total Non Current Liabilities` / CURSOR_VALUE,
	`Total Liabilities` = `Total Liabilities` / CURSOR_VALUE,
	`Indexed` = 1
WHERE
	Year = CURSOR_CALENDAR_YEAR
	and `Reported Currency` = CURSOR_REPORTED_CURRENCY;
END LOOP;
DELETE FROM
	`base_query_data_usd`
WHERE
	Indexed = 0;
ALTER TABLE
	`base_query_data_usd` DROP COLUMN `Indexed`;
ALTER TABLE
	`base_query_data_usd`
ADD
	FULLTEXT INDEX `Search` (`Description`),
ADD
	INDEX `ISector` (`Sector` ASC),
ADD
	INDEX `IIndustry` (`Industry` ASC),
ADD
	INDEX `IYear` (`Year` DESC),
ADD
	INDEX `ICompany` (`Company Name` ASC);
UPDATE
	base_query_data_usd
SET
	`Reported Currency` = 'USD';
END