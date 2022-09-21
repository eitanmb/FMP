CREATE DEFINER = `eitan` @`localhost` PROCEDURE `proc_general_date_filters_selected_companies`(IN object_params JSON) BEGIN DECLARE base_query TEXT;
DECLARE username varchar(50);
DECLARE general_filters_param TEXT default 'Revenue <> Null';
DECLARE date_filters_param TEXT;
DECLARE num_years INT DEFAULT 3;
DECLARE append_query TEXT;
DECLARE operator TEXT;
DECLARE general_date_filters_query TEXT;
SET
	username = (
		SELECT
			JSON_UNQUOTE(JSON_EXTRACT(object_params, '$.username'))
	);
SET
	base_query = CONCAT(
		'CREATE OR REPLACE VIEW ',
		username,
		'_general_date_filters_selected_companies AS SELECT DISTINCT(`Company Name`),Symbol, count(*) 
					  from base_query_data t0 WHERE '
	);
SET
	append_query = ' GROUP BY `Company Name`, Symbol HAVING COUNT(*) = ';
SET
	operator = " AND ";
SET
	general_filters_param = (
		SELECT
			JSON_UNQUOTE(JSON_EXTRACT(object_params, '$.general_filters'))
	);
SET
	date_filters_param = (
		SELECT
			JSON_UNQUOTE(JSON_EXTRACT(object_params, '$.date_filters'))
	);
SET
	num_years = (
		SELECT
			JSON_EXTRACT(object_params, '$.num_years')
	);
IF general_filters_param <> '' THEN
SET
	@general_date_filters_query = CONCAT(
		base_query,
		general_filters_param,
		operator,
		date_filters_param,
		append_query,
		num_years
	);
ELSE
SET
	@general_date_filters_query = CONCAT(
		base_query,
		date_filters_param,
		append_query,
		num_years
	);
END IF;
PREPARE result_general_date_filters
FROM
	@general_date_filters_query;
EXECUTE result_general_date_filters;
deallocate prepare result_general_date_filters;
END