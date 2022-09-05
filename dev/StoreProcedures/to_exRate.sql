CREATE DEFINER=`eitan`@`localhost` PROCEDURE `proc_cursor_to_exRate`()
BEGIN
  DECLARE CURSOR_REPORTED_CURRENCY VARCHAR(10);
  DECLARE CURSOR_CALENDAR_YEAR VARCHAR(10);
  DECLARE CURSOR_VALUE DOUBLE;
  DECLARE done INT DEFAULT FALSE;
  DECLARE cursor_exRate CURSOR FOR SELECT ReportedCurrency, CalendarYear, Value FROM exRate;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
  
  DROP TABLE IF EXISTS fundamental_filters_selection_usd;
  CREATE TABLE fundamental_filters_selection_usd AS SELECT * FROM fundamental_filters_selection;

  OPEN cursor_exRate;
  loop_through_rows: LOOP
    FETCH cursor_exRate INTO CURSOR_REPORTED_CURRENCY, CURSOR_CALENDAR_YEAR, CURSOR_VALUE;
    IF done THEN
      LEAVE loop_through_rows;
    END IF;
    UPDATE fundamental_filters_selection_usd
	SET `Revenue`= `Revenue`*CURSOR_VALUE, 
		`Cost Of Revenue`= `Cost Of Revenue`*CURSOR_VALUE, 
		`Gross Profit`= `Gross Profit`*CURSOR_VALUE, 
		`Research And Development Expenses`= `Research And Development Expenses`*CURSOR_VALUE, 
		`General And Administrative Expenses`= `General And Administrative Expenses`*CURSOR_VALUE, 
		`Selling And Marketing Expenses`= `Selling And Marketing Expenses`*CURSOR_VALUE, 
		`Other Expenses`= `Other Expenses`*CURSOR_VALUE, 
		`Operating Expenses`= `Operating Expenses`*CURSOR_VALUE, 
		`Cost And Expenses`= `Cost And Expenses`*CURSOR_VALUE, 
		`Interest Expense`= `Interest Expense`*CURSOR_VALUE, 
		`Depreciation And Amortization`= `Depreciation And Amortization`*CURSOR_VALUE, 
		`Operating Income`= `Operating Income`*CURSOR_VALUE, 
		`Cash And Cash Equivalents`= `Cash And Cash Equivalents`*CURSOR_VALUE, 
		`Net Receivables`= `Net Receivables`*CURSOR_VALUE, 
		`Inventory`= `Inventory`*CURSOR_VALUE, 
		`Total Current Assets`= `Total Current Assets`*CURSOR_VALUE, 
		`Total Non Current Assets`= `Total Non Current Assets`*CURSOR_VALUE, 
		`Total Assets`= `Total Assets`*CURSOR_VALUE, 
		`Account Payables`= `Account Payables`*CURSOR_VALUE, 
		`Total Current Liabilities`= `Total Current Liabilities`*CURSOR_VALUE, 
		`Total Non Current Liabilities`= `Total Non Current Liabilities`*CURSOR_VALUE, 
		`Total Liabilities`=`Total Liabilities`*CURSOR_VALUE
		WHERE Year = CURSOR_CALENDAR_YEAR and `Reported Currency` = CURSOR_REPORTED_CURRENCY ;
  END LOOP;
  CLOSE cursor_exRate;
END





INSERT into base_query_data_usd (`Company Name`,`Symbol`,`Exchange Short Name`,`Industry`,`Website`,`Description`,`Sector`,`Country`,`Full Time Employees`,
  `Date`,`Reported Currency`,`Period`,`Revenue`,`Cost Of Revenue`,`Gross Profit`,`Research And Development Expenses`,
  `General And Administrative Expenses`,`Selling And Marketing Expenses`,`Other Expenses`,`Operating Expenses`,`Cost And Expenses`,
  `Interest Expense`,`Depreciation And Amortization`,`Operating Income`,`Link Incomestatement`,`Final Link Incomestatement`,`Cash And Cash Equivalents`,
  `Net Receivables`,`Inventory`,`Total Current Assets`,`Total Non Current Assets`,`Total Assets`,`Account Payables`,`Total Current Liabilities`,
  `Total Non Current Liabilities`,`Total Liabilities`,`Link Balancesheet`,`Final Link Balancesheet`, `Year`) 
   SELECT `Company Name`,`Symbol`,`Exchange Short Name`,`Industry`,`Website`,`Description`,`Sector`,`Country`,`Full Time Employees`,
  `Date`,`Reported Currency`,`Period`,`Revenue`,`Cost Of Revenue`,`Gross Profit`,`Research And Development Expenses`,
  `General And Administrative Expenses`,`Selling And Marketing Expenses`,`Other Expenses`,`Operating Expenses`,`Cost And Expenses`,
  `Interest Expense`,`Depreciation And Amortization`,`Operating Income`,`Link Incomestatement`,`Final Link Incomestatement`,
  `Cash And Cash Equivalents`,`Net Receivables`,`Inventory`,`Total Current Assets`,`Total Non Current Assets`,`Total Assets`,
  `Account Payables`,`Total Current Liabilities`,`Total Non Current Liabilities`,`Total Liabilities`,`Link Balancesheet`,`Final Link Balancesheet`,`Year` FROM base_query_data
   WHERE Year = CURSOR_CALENDAR_YEAR and (`Reported Currency` = CURSOR_REPORTED_CURRENCY OR `Reported Currency` = 'USD');