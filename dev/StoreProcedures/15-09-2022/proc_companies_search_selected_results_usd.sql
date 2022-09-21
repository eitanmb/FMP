CREATE DEFINER=`eitan`@`localhost` PROCEDURE `proc_companies_search_selected_results_usd`(
	IN object_params JSON
)
BEGIN
  DECLARE CURSOR_SYMBOL VARCHAR(200);
  DECLARE CURSOR_SYMBOL_QUERY VARCHAR(200);
  DECLARE symbol_condition LONGBLOB;
  DECLARE done INT DEFAULT FALSE;
  DECLARE operator_or VARCHAR(10) DEFAULT ' OR ';
  DECLARE operator_and VARCHAR(10) DEFAULT ' AND ';
  DECLARE companies_query_condition LONGBLOB;
  DECLARE rows_number INT;
  DECLARE count INT DEFAULT 1;
  DECLARE fundamental_filters_param TEXT;
  DECLARE username varchar(50);
  DECLARE date_filters_param TEXT;
  DECLARE fundamental_filters_query TEXT;
  DECLARE result_base_query TEXT;
  DECLARE result_search_filters TEXT;
  DECLARE cursor_general_date_filters CURSOR FOR SELECT `Symbol` from `tmp_general_date_filters_selected_companies`;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
  
  SET username = (SELECT JSON_UNQUOTE(JSON_EXTRACT(object_params, '$.username')));
  SET @cursor_table = concat('CREATE OR REPLACE VIEW tmp_general_date_filters_selected_companies as SELECT Symbol FROM ', username, '_general_date_filters_selected_companies');
  PREPARE create_cursor_table FROM @cursor_table;
  EXECUTE create_cursor_table;
  DEALLOCATE PREPARE create_cursor_table;
  
  SET symbol_condition = '(';
  
  OPEN cursor_general_date_filters;
  SET rows_number = (SELECT FOUND_ROWS());

  IF rows_number > 0 THEN
	  loop_through_rows: LOOP
		FETCH cursor_general_date_filters INTO CURSOR_SYMBOL;
		
		IF done THEN
			CLOSE cursor_general_date_filters;
		  LEAVE loop_through_rows;
		END IF;
		
		SET CURSOR_SYMBOL_QUERY = CONCAT('`Symbol` = ',  '"', CURSOR_SYMBOL, '"');
		
		IF rows_number = 1 THEN
			SET companies_query_condition = CONCAT(symbol_condition, CURSOR_SYMBOL_QUERY, ')');
		ELSE
			IF count < rows_number THEN
				SET symbol_condition = CONCAT(symbol_condition, CURSOR_SYMBOL_QUERY, operator_or);
			else
				SET companies_query_condition = CONCAT(symbol_condition, CURSOR_SYMBOL_QUERY, ')');
			END IF;
		END IF;
		
		SET count = count + 1;
	  END LOOP;

      SET result_base_query = CONCAT('CREATE OR REPLACE VIEW ', username, '_companies_search_selected_result_usd AS SELECT * from base_query_data_usd t0 WHERE ');
	  SET date_filters_param = (SELECT JSON_UNQUOTE(JSON_EXTRACT(object_params, '$.date_filters')));
	  SET fundamental_filters_param = (SELECT JSON_UNQUOTE(JSON_EXTRACT(object_params, '$.fundamental_filters')));
		
	  IF fundamental_filters_param <> '' THEN
		SET @fundamental_filters_query = CONCAT(result_base_query, companies_query_condition, operator_and, fundamental_filters_param, operator_and, date_filters_param);
	  ELSE
		SET @fundamental_filters_query = CONCAT(result_base_query, companies_query_condition,  operator_and, date_filters_param);
	  END IF;
  
  ELSE
	SET @fundamental_filters_query = CONCAT('CREATE OR REPLACE VIEW ', username, '_companies_search_selected_result_usd AS SELECT * from base_query_data_usd t0 WHERE 1=2');
  END IF;
  
  PREPARE result_search_filters FROM @fundamental_filters_query;
  EXECUTE result_search_filters;
  DEALLOCATE PREPARE result_search_filters;
  
  DROP VIEW IF EXISTS tmp_general_date_filters_selected_companies;
END