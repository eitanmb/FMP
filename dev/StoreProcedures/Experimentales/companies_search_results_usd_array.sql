CREATE DEFINER=`eitan`@`localhost` PROCEDURE `proc_companies_search_results_usd_array`(
	IN object_params JSON
)
BEGIN
  DECLARE symbol_selected VARCHAR(50);
  DECLARE symbols_selected_query TEXT;
  DECLARE symbols_condition longtext;
  DECLARE companies_query_condition longtext;
  DECLARE operator_or VARCHAR(10) DEFAULT ' OR ';
  DECLARE operator_and VARCHAR(10) DEFAULT ' AND ';
  DECLARE username varchar(50);
  DECLARE symbols_params TEXT;
  DECLARE count_symbols INT;
  DECLARE count INT DEFAULT 1;
  DECLARE fundamental_filters_param TEXT;
  DECLARE date_filters_param TEXT;
  DECLARE fundamental_filters_query TEXT;
  DECLARE create_views_query TEXT;
  DECLARE insert_views_query TEXT;
  DECLARE result_search_filters TEXT;
  
  SET username = (SELECT JSON_UNQUOTE(JSON_EXTRACT(object_params, '$.username')));
  SET symbols_params = (SELECT JSON_UNQUOTE(JSON_EXTRACT(object_params, '$.symbols')));
  SET count_symbols = (SELECT JSON_UNQUOTE(JSON_EXTRACT(object_params, '$.count_symbols')));
  SET date_filters_param = (SELECT JSON_UNQUOTE(JSON_EXTRACT(object_params, '$.date_filters')));
  SET fundamental_filters_param = (SELECT JSON_UNQUOTE(JSON_EXTRACT(object_params, '$.fundamental_filters')));
  
  SET @create_views_query = CONCAT('CREATE OR REPLACE VIEW ', username, '_companies_search_result_usd_array AS SELECT * from base_query_data_usd WHERE 1=2');
  PREPARE create_views FROM @create_views_query;
  EXECUTE create_views;
  DEALLOCATE PREPARE create_views;
  
  SET symbols_condition = '(';
  
  IF count_symbols > 0 THEN
      SET insert_views_query = CONCAT('INSERT INTO ', username, '_companies_search_result_usd_array SELECT * from base_query_data_usd WHERE ');
      
  	  WHILE count <= count_symbols DO
		SET symbol_selected = TRIM(SUBSTRING_INDEX(symbols_params, ',', 1));
	    SET symbols_params= SUBSTRING(symbols_params, LOCATE(',',symbols_params) + 1);
        
        SET symbols_selected_query = CONCAT('`Symbol` = ',  '"', symbol_selected, '"');
        
        IF count_symbols = 1 THEN
			SET companies_query_condition = CONCAT(symbols_condition, symbols_selected_query, ')');
		ELSE
			IF count < count_symbols THEN
				SET symbols_condition = CONCAT(symbols_condition, symbols_selected_query, operator_or);
			else
				SET companies_query_condition = CONCAT(symbols_condition, symbols_selected_query, ')');
			END IF;
		END IF;
        
		
        SET count = count + 1;
	  END WHILE;
      
	  IF fundamental_filters_param <> '' THEN
		SET @fundamental_filters_query = CONCAT(insert_views_query, companies_query_condition, operator_and, fundamental_filters_param, operator_and, date_filters_param);
	  ELSE
		SET @fundamental_filters_query = CONCAT(insert_views_query, companies_query_condition,  operator_and, date_filters_param);
	  END IF;
      
      SELECT @fundamental_filters_query;
	 
	  #PREPARE result_search_filters FROM @fundamental_filters_query;
	  #EXECUTE result_search_filters;
	  #DEALLOCATE PREPARE result_search_filters;
  END IF;
END