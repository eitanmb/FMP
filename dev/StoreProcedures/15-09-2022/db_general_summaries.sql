CREATE DEFINER=`eitan`@`localhost` PROCEDURE `db_general_summaries`()
BEGIN
	DECLARE companies_sql TEXT;
	DECLARE by_exchange_sql TEXT;
	DECLARE by_sector_sql TEXT;
	DECLARE by_industry_sql TEXT;
	DECLARE by_country_sql TEXT;

	SET @companies_sql = 'CREATE OR REPLACE VIEW total_companies as SELECT count(DISTINCT(companyName)) as `Companies` from profile;';
	PREPARE result_companies FROM @companies_sql;
	EXECUTE result_companies;

	SET @by_exchange_sql = 'CREATE OR REPLACE VIEW companies_by_exchange as SELECT `exchange` as Exchange, count(*) as `Companies` from profile GROUP BY `exchange` ORDER BY `Companies` DESC LIMIT 10;';
	PREPARE result_exchange FROM @by_exchange_sql;
	EXECUTE result_exchange;
		
	SET @by_sector_sql = 'CREATE OR REPLACE VIEW companies_by_sector as SELECT sector as Sector, count(*) as `Companies` from profile WHERE sector <> "" GROUP BY `Sector` ORDER BY `Companies` DESC LIMIT 10;';
	PREPARE result_sector FROM @by_sector_sql;
	EXECUTE result_sector;
		
	SET @by_industry_sql = 'CREATE OR REPLACE VIEW companies_by_industry as SELECT industry as Industry, count(*) as `Companies` from profile WHERE industry <> "" GROUP BY `Industry` ORDER BY `Companies` DESC LIMIT 10;';
	PREPARE result_industry FROM @by_industry_sql;
	EXECUTE result_industry;

	SET @by_country_sql = 'CREATE OR REPLACE VIEW companies_by_country as SELECT country as Country,  count(*) as `Companies` FROM profile WHERE (country <> "" and country <> "N/A" ) GROUP BY `Country` ORDER BY `Companies` DESC LIMIT 10;';
	PREPARE result_country FROM @by_country_sql;
	EXECUTE result_country;

	DEALLOCATE PREPARE result_companies;
	DEALLOCATE PREPARE result_exchange;
	DEALLOCATE PREPARE result_sector;
	DEALLOCATE PREPARE result_industry;
	DEALLOCATE PREPARE result_country;
END