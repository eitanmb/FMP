drop_exec_procedures = f'DROP procedure IF EXISTS `exec_procedures`;'
create_exec_procedures = "CREATE DEFINER = `eitan` @`localhost` PROCEDURE `exec_procedures`() BEGIN \
                            SELECT 'CALL proc_fx_outer()'; \
                            CALL proc_fx_outer(); \
                            SELECT 'CALL proc_fx_exRate()';\
                            CALL proc_fx_exRate();\
                            SELECT 'CALL proc_create_base_query_data()';\
                            CALL proc_create_base_query_data();\
                            SELECT 'CALL proc_create_base_query_data_usd()';\
                            CALL proc_create_base_query_data_usd();\
                            SELECT 'CALL db_general_summaries()';\
                            CALL db_general_summaries();\
                            SELECT 'CALL db_revenue_summaries()';\
                            CALL db_revenue_summaries();\
                            END"


drop_fieldExists = f'DROP procedure IF EXISTS `fieldExists`;'
create_fieldExists = "CREATE DEFINER = `eitan` @`localhost` PROCEDURE `fieldExists`(\
                    OUT _exists BOOLEAN,\
                    IN tableName CHAR(255),\
                    IN columnName CHAR(255),\
                    IN dbName CHAR(255)\
                ) BEGIN\
                SET\
                    @_dbName := IF(dbName IS NULL, database(), dbName);\
                IF CHAR_LENGTH(@_dbName) = 0 THEN\
                SELECT\
                    FALSE INTO _exists;\
                ELSE\
                SELECT\
                    IF(count(*) > 0, TRUE, FALSE) INTO _exists\
                FROM\
                    information_schema.COLUMNS c\
                WHERE\
                    c.TABLE_SCHEMA = @_dbName\
                    AND c.TABLE_NAME = tableName\
                    AND c.COLUMN_NAME = columnName;\
                END IF;\
                END"


drop_proc_fx_outer = f'DROP procedure IF EXISTS `proc_fx_outer`;'
create_proc_fx_outer = "CREATE DEFINER = `eitan` @`localhost` PROCEDURE `proc_fx_outer`() BEGIN DECLARE cursor_pair VARCHAR(20); \
                        DECLARE done INT DEFAULT FALSE; \
                        DECLARE cursor_forex_pair CURSOR FOR select DISTINCT(pair) from forex; \
                        DECLARE CONTINUE HANDLER FOR NOT FOUND \
                        SET done = TRUE; \
                        DROP TABLE IF EXISTS last_exchange_by_year_temp; \
                        CREATE TABLE last_exchange_by_year_temp \
                        SELECT pair, date, price FROM forex where MONTH(date) = 12; \
                        DROP TABLE IF EXISTS last_exchange_by_year; \
                        CREATE TABLE last_exchange_by_year(pair VARCHAR(255) NOT NULL, date DATE, close DOUBLE) ENGINE = INNODB; \
                        OPEN cursor_forex_pair; \
                        loop1: LOOP FETCH cursor_forex_pair INTO cursor_pair; \
                        IF done THEN LEAVE loop1; \
                        CLOSE cursor_forex_pair; \
                        END IF; \
                        CALL proc_fx_inner(cursor_pair); \
                        END LOOP; \
                        CALL proc_fx_add_usd(); \
                        DROP TABLE IF EXISTS last_exchange_by_year_temp; \
                        END"


drop_proc_fx_inner = f'DROP procedure IF EXISTS `proc_fx_inner`;'
create_proc_fx_inner = "CREATE DEFINER = `eitan` @`localhost` PROCEDURE `proc_fx_inner`( \
                         fx_pair varchar(20) \
                        ) BEGIN DECLARE _from INT DEFAULT 2017; \
                        DECLARE _till INT DEFAULT 2020; \
                        SET _from = ( SELECT MIN(YEAR(date)) from forex ); \
                        SET _till = ( SELECT MAX(YEAR(date)) from forex ); \
                        WHILE _from <= _till DO \
                        INSERT INTO last_exchange_by_year (pair, date, close) SELECT * \
                        from last_exchange_by_year_temp where pair = fx_pair and Year(date) = _from LIMIT 1; \
                        SET _from = _from + 1; \
                        END WHILE; \
                        END"


drop_proc_fx_exRate = f'DROP procedure IF EXISTS `proc_fx_exRate`;'
create_proc_fx_exRate = "CREATE DEFINER = `eitan` @`localhost` PROCEDURE `proc_fx_exRate`() BEGIN DROP VIEW IF EXISTS exRate; \
                        CREATE VIEW exRate as SELECT pair as Pair, SUBSTRING(pair, 4) as ReportedCurrency, date as `Date`, \
                        year(date) as CalendarYear, close as Value \
                        FROM last_exchange_by_year WHERE close <> 0 ORDER BY reportedCurrency asc, date DESC;\
                        END"


drop_proc_fx_add_usd = f'DROP procedure IF EXISTS `proc_fx_add_usd`;'
create_proc_fx_add_usd = "CREATE DEFINER = `eitan` @`localhost` PROCEDURE `proc_fx_add_usd`() BEGIN DECLARE _from INT DEFAULT 2017; \
                            DECLARE _till INT DEFAULT 2020; \
                            SET _from = (SELECT MIN(YEAR(date)) from forex); \
                            SET _till = (SELECT MAX(YEAR(date)) from forex); \
                            WHILE _from <= _till DO \
                            INSERT INTO last_exchange_by_year (pair, date, close) SELECT 'USDUSD', date, 1 \
                            from last_exchange_by_year_temp \
                            where YEAR(date) = _from limit 1; \
                            SET _from = _from + 1; \
                            END WHILE; \
                            END"


drop_proc_create_base_query_data = f'DROP procedure IF EXISTS `proc_create_base_query_data`;'
create_proc_create_base_query_data = "CREATE DEFINER = `eitan` @`localhost` PROCEDURE `proc_create_base_query_data`() BEGIN DECLARE fieldExist INT; \
                                        CALL fieldExists( \
                                            @_exists, \
                                            'incomeStatement', \
                                            'calendarYear', \
                                            NULL \
                                        ); \
                                        DROP TABLE IF EXISTS base_query_data; \
                                        IF ( \
                                            select \
                                                @_exists = 0 \
                                        ) THEN CREATE TABLE base_query_data AS \
                                        SELECT \
                                            t0.companyName as `Company Name`, \
                                            t0.symbol as Symbol, \
                                            t0.exchangeShortName as `Exchange Short Name`,\
                                            t0.industry as `Industry`,\
                                            t0.website as `Website`,\
                                            t0.description as `Description`,\
                                            t0.sector as `Sector`,\
                                            t0.country as `Country`,\
                                            t0.fullTimeEmployees as `Full Time Employees`,\
                                            t1.date as Date,\
                                            t1.reportedCurrency as `Reported Currency`,\
                                            t1.period as `Period`,\
                                            t1.revenue as `Revenue`,\
                                            t1.costOfRevenue as `Cost Of Revenue`,\
                                            t1.grossProfit as `Gross Profit`,\
                                            t1.researchAndDevelopmentExpenses as `Research And Development Expenses`,\
                                            t1.generalAndAdministrativeExpenses as `General And Administrative Expenses`,\
                                            t1.sellingAndMarketingExpenses as `Selling And Marketing Expenses`,\
                                            t1.otherExpenses as `Other Expenses`,\
                                            t1.operatingExpenses as `Operating Expenses`,\
                                            t1.costAndExpenses as `Cost And Expenses`,\
                                            t1.InterestExpense as `Interest Expense`,\
                                            t1.depreciationAndAmortization as `Depreciation And Amortization`,\
                                            t1.operatingIncome as `Operating Income`,\
                                            t1.linkIncomestatement as `Link Incomestatement`,\
                                            t1.finalLinkIncomestatement as `Final Link Incomestatement`,\
                                            t2.cashAndCashEquivalents as `Cash And Cash Equivalents`,\
                                            t2.netReceivables as `Net Receivables`,\
                                            t2.inventory as `Inventory`,\
                                            t2.totalCurrentAssets as `Total Current Assets`,\
                                            t2.totalNonCurrentAssets as `Total Non Current Assets`,\
                                            t2.totalAssets as `Total Assets`,\
                                            t2.accountPayables as `Account Payables`,\
                                            t2.totalCurrentLiabilities as `Total Current Liabilities`,\
                                            t2.totalNonCurrentLiabilities as `Total Non Current Liabilities`,\
                                            t2.totalLiabilities as `Total Liabilities`,\
                                            t2.linkBalancesheet as `Link Balancesheet`,\
                                            t2.finalLinkBalancesheet as `Final Link Balancesheet`,\
                                            Year(t1.date) as `Year`\
                                        from\
                                            profile t0\
                                            INNER JOIN incomeStatement t1 on t0.symbol = t1.symbol\
                                            INNER JOIN balanceSheet t2 ON t2.symbol = t1.symbol\
                                        WHERE\
                                            t0.companyName <> \"\" \
                                            and (YEAR(t1.date) = YEAR(t2.date))\
                                            and YEAR(t1.date) >= 2008\
                                            and t0.isEtf = 0\
                                            and (\
                                                t1.reportedCurrency is not Null\
                                                and t1.reportedCurrency <> 'unknown'\
                                            );\
                                        ELSE CREATE TABLE base_query_data AS\
                                        SELECT\
                                            t0.companyName as `Company Name`,\
                                            t0.symbol as Symbol,\
                                            t0.exchangeShortName as `Exchange Short Name`,\
                                            t0.industry as `Industry`,\
                                            t0.website as `Website`,\
                                            t0.description as `Description`,\
                                            t0.sector as `Sector`,\
                                            t0.country as `Country`,\
                                            t0.fullTimeEmployees as `Full Time Employees`,\
                                            t1.date as Date,\
                                            t1.reportedCurrency as `Reported Currency`,\
                                            t1.period as `Period`,\
                                            t1.revenue as `Revenue`,\
                                            t1.costOfRevenue as `Cost Of Revenue`,\
                                            t1.grossProfit as `Gross Profit`,\
                                            t1.researchAndDevelopmentExpenses as `Research And Development Expenses`,\
                                            t1.generalAndAdministrativeExpenses as `General And Administrative Expenses`,\
                                            t1.sellingAndMarketingExpenses as `Selling And Marketing Expenses`,\
                                            t1.otherExpenses as `Other Expenses`,\
                                            t1.operatingExpenses as `Operating Expenses`,\
                                            t1.costAndExpenses as `Cost And Expenses`,\
                                            t1.InterestExpense as `Interest Expense`,\
                                            t1.depreciationAndAmortization as `Depreciation And Amortization`,\
                                            t1.operatingIncome as `Operating Income`,\
                                            t1.linkIncomestatement as `Link Incomestatement`,\
                                            t1.finalLinkIncomestatement as `Final Link Incomestatement`,\
                                            t2.cashAndCashEquivalents as `Cash And Cash Equivalents`,\
                                            t2.netReceivables as `Net Receivables`,\
                                            t2.inventory as `Inventory`,\
                                            t2.totalCurrentAssets as `Total Current Assets`,\
                                            t2.totalNonCurrentAssets as `Total Non Current Assets`,\
                                            t2.totalAssets as `Total Assets`,\
                                            t2.accountPayables as `Account Payables`,\
                                            t2.totalCurrentLiabilities as `Total Current Liabilities`,\
                                            t2.totalNonCurrentLiabilities as `Total Non Current Liabilities`,\
                                            t2.totalLiabilities as `Total Liabilities`,\
                                            t2.linkBalancesheet as `Link Balancesheet`,\
                                            t2.finalLinkBalancesheet as `Final Link Balancesheet`,\
                                            t1.calendarYear as `Year`\
                                        from\
                                            profile t0\
                                            INNER JOIN incomeStatement t1 on t0.symbol = t1.symbol\
                                            INNER JOIN balanceSheet t2 ON t2.symbol = t1.symbol\
                                        WHERE\
                                            t0.companyName <> \"\" \
                                            and (t1.calendarYear = t2.calendarYear)\
                                            and t1.calendarYear >= 2008\
                                            and t0.isEtf = 0\
                                            and (\
                                                t1.reportedCurrency is not Null\
                                                and t1.reportedCurrency <> 'unknown'\
                                            );\
                                        END IF;\
                                        ALTER TABLE\
                                            `base_query_data`\
                                        ADD FULLTEXT INDEX `Search` (`Description`),\
                                        ADD INDEX `ISectorYear` (`Sector` ASC, `Year` DESC) VISIBLE,\
                                        ADD INDEX `IIndustryYear` (`Industry` ASC, `Year` DESC) VISIBLE,\
                                        ADD INDEX `ICompanyYear` (`Company Name` ASC, `Year` DESC) VISIBLE,\
                                        ADD INDEX `ISymbolYear` (`Symbol` ASC, `Year` DESC) VISIBLE,\
                                        ADD INDEX `ISymbolYearRevenue` (`Symbol` ASC, `Year` DESC, `Revenue` ASC) VISIBLE,\
                                        ADD INDEX `ICountryYear` (`Country` ASC, `Year` DESC) VISIBLE,\
                                        ADD INDEX `ISectorIndustryYear` (`Sector` ASC, `Industry` ASC,`Year` DESC) VISIBLE,\
                                        ADD INDEX `ISectorIndustryRevenueYear` (`Sector` ASC, `Industry` ASC, `Revenue` ASC, `Year` DESC) VISIBLE,\
                                        ADD FULLTEXT INDEX `Search` (`Description`) VISIBLE;\
                                        END"


drop_proc_create_base_query_data_usd = f'DROP procedure IF EXISTS `proc_create_base_query_data_usd`;'
create_proc_create_base_query_data_usd = "CREATE DEFINER = `eitan` @`localhost` PROCEDURE `proc_create_base_query_data_usd`() BEGIN DECLARE CURSOR_REPORTED_CURRENCY VARCHAR(10);\
                                            DECLARE CURSOR_CALENDAR_YEAR VARCHAR(10);\
                                            DECLARE CURSOR_VALUE DOUBLE;\
                                            DECLARE done INT DEFAULT FALSE;\
                                            DECLARE cursor_exRate CURSOR FOR\
                                            SELECT\
                                                ReportedCurrency,\
                                                CalendarYear,\
                                                Value\
                                            FROM\
                                                exRate;\
                                            DECLARE CONTINUE HANDLER FOR NOT FOUND\
                                            SET\
                                                done = TRUE;\
                                            DROP TABLE IF EXISTS base_query_data_usd;\
                                            CREATE TABLE base_query_data_usd AS\
                                            SELECT\
                                                *\
                                            FROM\
                                                base_query_data;\
                                            ALTER TABLE\
                                                base_query_data_usd\
                                            ADD\
                                                COLUMN `Indexed` TINYINT NULL DEFAULT 0\
                                            AFTER\
                                                `Year`;\
                                            OPEN cursor_exRate;\
                                            loop_through_rows: LOOP FETCH cursor_exRate INTO CURSOR_REPORTED_CURRENCY,\
                                            CURSOR_CALENDAR_YEAR,\
                                            CURSOR_VALUE;\
                                            IF done THEN CLOSE cursor_exRate;\
                                            LEAVE loop_through_rows;\
                                            END IF;\
                                            UPDATE\
                                                base_query_data_usd\
                                            SET\
                                                `Revenue` = `Revenue` / CURSOR_VALUE,\
                                                `Cost Of Revenue` = `Cost Of Revenue` / CURSOR_VALUE,\
                                                `Gross Profit` = `Gross Profit` / CURSOR_VALUE,\
                                                `Research And Development Expenses` = `Research And Development Expenses` / CURSOR_VALUE,\
                                                `General And Administrative Expenses` = `General And Administrative Expenses` / CURSOR_VALUE,\
                                                `Selling And Marketing Expenses` = `Selling And Marketing Expenses` / CURSOR_VALUE,\
                                                `Other Expenses` = `Other Expenses` / CURSOR_VALUE,\
                                                `Operating Expenses` = `Operating Expenses` / CURSOR_VALUE,\
                                                `Cost And Expenses` = `Cost And Expenses` / CURSOR_VALUE,\
                                                `Interest Expense` = `Interest Expense` / CURSOR_VALUE,\
                                                `Depreciation And Amortization` = `Depreciation And Amortization` / CURSOR_VALUE,\
                                                `Operating Income` = `Operating Income` / CURSOR_VALUE,\
                                                `Cash And Cash Equivalents` = `Cash And Cash Equivalents` / CURSOR_VALUE,\
                                                `Net Receivables` = `Net Receivables` / CURSOR_VALUE,\
                                                `Inventory` = `Inventory` / CURSOR_VALUE,\
                                                `Total Current Assets` = `Total Current Assets` / CURSOR_VALUE,\
                                                `Total Non Current Assets` = `Total Non Current Assets` / CURSOR_VALUE,\
                                                `Total Assets` = `Total Assets` / CURSOR_VALUE,\
                                                `Account Payables` = `Account Payables` / CURSOR_VALUE,\
                                                `Total Current Liabilities` = `Total Current Liabilities` / CURSOR_VALUE,\
                                                `Total Non Current Liabilities` = `Total Non Current Liabilities` / CURSOR_VALUE,\
                                                `Total Liabilities` = `Total Liabilities` / CURSOR_VALUE,\
                                                `Indexed` = 1\
                                            WHERE\
                                                Year = CURSOR_CALENDAR_YEAR\
                                                and `Reported Currency` = CURSOR_REPORTED_CURRENCY;\
                                            END LOOP;\
                                            DELETE FROM `base_query_data_usd` WHERE Indexed = 0;\
                                            ALTER TABLE `base_query_data_usd` DROP COLUMN `Indexed`;\
                                            UPDATE base_query_data_usd SET `Reported Currency` = 'USD';\
                                            ALTER TABLE `base_query_data_usd`\
                                            ADD FULLTEXT INDEX `Search` (`Description`),\
                                            ADD INDEX `ISectorYear` (`Sector` ASC, `Year` DESC) VISIBLE,\
                                            ADD INDEX `IIndustryYear` (`Industry` ASC, `Year` DESC) VISIBLE,\
                                            ADD INDEX `ICompanyYear` (`Company Name` ASC, `Year` DESC) VISIBLE,\
                                            ADD INDEX `ISymbolYear` (`Symbol` ASC, `Year` DESC) VISIBLE,\
                                            ADD INDEX `ISymbolYearRevenue` (`Symbol` ASC, `Year` DESC, `Revenue` ASC) VISIBLE,\
                                            ADD INDEX `ICountryYear` (`Country` ASC, `Year` DESC) VISIBLE,\
                                            ADD INDEX `ISectorIndustryYear` (`Sector` ASC, `Industry` ASC,`Year` DESC) VISIBLE,\
                                            ADD INDEX `ISectorIndustryRevenueYear` (`Sector` ASC, `Industry` ASC, `Revenue` ASC, `Year` DESC) VISIBLE,\
                                            ADD FULLTEXT INDEX `Search` (`Description`) VISIBLE;\
                                            END"


drop_proc_db_general_summaries = f'DROP procedure IF EXISTS `db_general_summaries`;'
create_proc_db_general_summaries = f"CREATE DEFINER=`eitan`@`localhost` PROCEDURE `db_general_summaries`()\
                                    BEGIN\
                                        DECLARE companies_sql TEXT;\
                                        DECLARE by_exchange_sql TEXT;\
                                        DECLARE by_sector_sql TEXT;\
                                        DECLARE by_industry_sql TEXT;\
                                        DECLARE by_country_sql TEXT;\
                                        \
                                        SET @companies_sql = 'CREATE OR REPLACE VIEW total_companies as SELECT count(DISTINCT(companyName)) as `Companies` from profile;';\
                                        PREPARE result_companies FROM @companies_sql;\
                                        EXECUTE result_companies;\
                                        \
                                        SET @by_exchange_sql = 'CREATE OR REPLACE VIEW companies_by_exchange as SELECT `exchange` as Exchange, count(*) as `Companies` from profile GROUP BY `exchange` ORDER BY `Companies` DESC LIMIT 10;';\
                                        PREPARE result_exchange FROM @by_exchange_sql;\
                                        EXECUTE result_exchange;\
                                            \
                                        SET @by_sector_sql = 'CREATE OR REPLACE VIEW companies_by_sector as SELECT sector as Sector, count(*) as `Companies` from profile WHERE sector <> \"\" GROUP BY `Sector` ORDER BY `Companies` DESC LIMIT 10;';\
                                        PREPARE result_sector FROM @by_sector_sql;\
                                        EXECUTE result_sector;\
                                            \
                                        SET @by_industry_sql = 'CREATE OR REPLACE VIEW companies_by_industry as SELECT industry as Industry, count(*) as `Companies` from profile WHERE industry <> \"\" GROUP BY `Industry` ORDER BY `Companies` DESC LIMIT 10;';\
                                        PREPARE result_industry FROM @by_industry_sql;\
                                        EXECUTE result_industry;\
                                        \
                                        SET @by_country_sql = 'CREATE OR REPLACE VIEW companies_by_country as SELECT country as Country,  count(*) as `Companies` FROM profile WHERE (country <> \"\" and country <> \"N/A\" ) GROUP BY `Country` ORDER BY `Companies` DESC LIMIT 10;';\
                                        PREPARE result_country FROM @by_country_sql;\
                                        EXECUTE result_country;\
                                        \
                                        DEALLOCATE PREPARE result_companies;\
                                        DEALLOCATE PREPARE result_exchange;\
                                        DEALLOCATE PREPARE result_sector;\
                                        DEALLOCATE PREPARE result_industry;\
                                        DEALLOCATE PREPARE result_country;\
                                    END"


drop_proc_db_revenue_summaries = f'DROP procedure IF EXISTS `db_revenue_summaries`;'
create_proc_db_revenue_summaries = f"CREATE DEFINER=`eitan`@`localhost` PROCEDURE `db_revenue_summaries`()\
                                    BEGIN\
                                    DECLARE comercial_year double;\
                                    DECLARE count double DEFAULT 1;\
                                    DECLARE revenue_query_by_sector TEXT;\
                                    DECLARE revenue_query_by_industry TEXT;\
                                    DECLARE revenue_query_by_country TEXT;\
\
                                    SET comercial_year = CAST(SUBSTRING(DATABASE(), 6,4) as double);\
\
                                    WHILE count <= 3 DO\
                                        SET @revenue_query_by_sector = CONCAT('CREATE OR REPLACE VIEW revenue_by_sector_', comercial_year - count, ' as SELECt Sector, FORMAT(SUM(Revenue)/1000, 2) as ', CONCAT('`Revenue ', comercial_year - count, ' (en miles USD)`'),' FROM base_query_data_usd WHERE Year = ', comercial_year - count, ' and (Sector <> \"\" and Sector <> \"N/A\") GROUP BY Sector ORDER BY SUM(Revenue) Desc LIMIT 10');\
                                        PREPARE result_by_Sector FROM @revenue_query_by_sector;\
                                        EXECUTE result_by_Sector;\
                                        \
                                        \
                                        SET @revenue_query_by_industry = CONCAT('CREATE OR REPLACE VIEW revenue_by_industry_', comercial_year - count, ' as SELECT Industry, FORMAT(SUM(Revenue)/1000, 2) as ', CONCAT('`Revenue ', comercial_year - count, ' (en miles USD)`'),' FROM base_query_data_usd WHERE Year = ', comercial_year - count, ' and (Industry <> \"\" and Industry <> \"N/A\") GROUP BY Industry ORDER BY SUM(Revenue) Desc LIMIT 10');\
                                        PREPARE result_by_Industry FROM @revenue_query_by_industry;\
                                        EXECUTE result_by_Industry;\
                                        \
                                        SET @revenue_query_by_country = CONCAT('CREATE OR REPLACE VIEW revenue_by_country_', comercial_year - count, ' as SELECT Country, FORMAT(SUM(Revenue)/1000, 2) as ', CONCAT('`Revenue ', comercial_year - count, ' (en miles USD)`'),' FROM base_query_data_usd WHERE Year = ', comercial_year - count, ' and (Country <> \"\" and Country <> \"N/A\") GROUP BY Country ORDER BY SUM(Revenue) Desc LIMIT 10');\
                                        PREPARE result_by_Country FROM @revenue_query_by_country;\
                                        EXECUTE result_by_Country;\
                                        \
\
                                        set count = count + 1;\
                                    END WHILE;\
                                    DEALLOCATE PREPARE result_by_Sector;\
                                    DEALLOCATE PREPARE result_by_Industry;\
                                    DEALLOCATE PREPARE result_by_Country;\
                                    END"


stp_exec_procedures = {
    'name': 'exec_procedures',
    'drop': drop_exec_procedures,
    'create': create_exec_procedures,
    'call': 'CALL exec_procedures()'
}

stp_proc_fx_outer = {
    'drop': drop_proc_fx_outer,
    'create': create_proc_fx_outer,
    'name': 'proc_fx_outer'
}

stp_proc_fx_inner = {
    'drop': drop_proc_fx_inner,
    'create': create_proc_fx_inner,
    'name': 'proc_fx_inner'
}

stp_proc_fieldExists = {
    'drop': drop_fieldExists,
    'create': create_fieldExists,
    'name': 'fieldExists'
}

stp_proc_fx_exRate = {
    'drop': drop_proc_fx_exRate,
    'create': create_proc_fx_exRate,
    'name': 'proc_fx_exRate'
}

stp_proc_fx_add_usd = {
    'drop': drop_proc_fx_add_usd,
    'create': create_proc_fx_add_usd,
    'name': 'proc_fx_add_usd'
}

stp_proc_create_base_query_data = {
    'drop': drop_proc_create_base_query_data,
    'create': create_proc_create_base_query_data,
    'name': 'proc_create_base_query_data'
}

stp_proc_create_base_query_data_usd = {
    'drop': drop_proc_create_base_query_data_usd,
    'create': create_proc_create_base_query_data_usd,
    'name': 'proc_create_base_query_data_usd'
}


stp_proc_db_general_summaries = {
    'drop': drop_proc_db_general_summaries,
    'create': create_proc_db_general_summaries,
    'name': 'db_general_summaries',
    'call': 'CALL db_general_summaries()'
}

stp_proc_db_revenue_summaries = {
    'drop': drop_proc_db_revenue_summaries,
    'create': create_proc_db_revenue_summaries,
    'name': 'db_revenue_summaries',
    'call': 'CALL db_revenue_summaries()'
}
