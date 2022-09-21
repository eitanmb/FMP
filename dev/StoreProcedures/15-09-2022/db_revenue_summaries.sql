CREATE DEFINER=`eitan`@`localhost` PROCEDURE `db_revenue_summaries`()
BEGIN
DECLARE comercial_year double;
DECLARE count double DEFAULT 1;
DECLARE revenue_query_by_sector TEXT;
DECLARE revenue_query_by_industry TEXT;
DECLARE revenue_query_by_country TEXT;

SET comercial_year = CAST(SUBSTRING(DATABASE(), 6,4) as double);

WHILE count <= 3 DO
	SET @revenue_query_by_sector = CONCAT('CREATE OR REPLACE VIEW revenue_by_sector_', comercial_year - count, ' as SELECt Sector, FORMAT(SUM(Revenue)/1000, 2) as ', CONCAT('`Revenue ', comercial_year - count, ' (en miles USD)`'),' FROM base_query_data_usd WHERE Year = ', comercial_year - count, ' and (Sector <> "" and Sector <> "N/A") GROUP BY Sector ORDER BY SUM(Revenue) Desc LIMIT 10');
	PREPARE result_by_Sector FROM @revenue_query_by_sector;
	EXECUTE result_by_Sector;
	
    
    SET @revenue_query_by_industry = CONCAT('CREATE OR REPLACE VIEW revenue_by_industry_', comercial_year - count, ' as SELECT Industry, FORMAT(SUM(Revenue)/1000, 2) as ', CONCAT('`Revenue ', comercial_year - count, ' (en miles USD)`'),' FROM base_query_data_usd WHERE Year = ', comercial_year - count, ' and (Industry <> "" and Industry <> "N/A") GROUP BY Industry ORDER BY SUM(Revenue) Desc LIMIT 10');
	PREPARE result_by_Industry FROM @revenue_query_by_industry;
	EXECUTE result_by_Industry;
	
    SET @revenue_query_by_country = CONCAT('CREATE OR REPLACE VIEW revenue_by_country_', comercial_year - count, ' as SELECT Country, FORMAT(SUM(Revenue)/1000, 2) as ', CONCAT('`Revenue ', comercial_year - count, ' (en miles USD)`'),' FROM base_query_data_usd WHERE Year = ', comercial_year - count, ' and (Country <> "" and Country <> "N/A") GROUP BY Country ORDER BY SUM(Revenue) Desc LIMIT 10');
	PREPARE result_by_Country FROM @revenue_query_by_country;
	EXECUTE result_by_Country;
	

	set count = count + 1;
END WHILE;
DEALLOCATE PREPARE result_by_Sector;
DEALLOCATE PREPARE result_by_Industry;
DEALLOCATE PREPARE result_by_Country;
END