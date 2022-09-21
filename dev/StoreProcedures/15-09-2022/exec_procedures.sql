CREATE DEFINER = `eitan` @`localhost` PROCEDURE `exec_procedures`() BEGIN
SELECT
    'CALL proc_fx_outer()';

CALL proc_fx_outer();

SELECT
    'CALL proc_fx_exRate()';

CALL proc_fx_exRate();

SELECT
    'CALL proc_create_base_query_data()';

CALL proc_create_base_query_data();

SELECT
    'CALL proc_create_base_query_data_usd()';

CALL proc_create_base_query_data_usd();

END