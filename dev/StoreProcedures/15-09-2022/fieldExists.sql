CREATE DEFINER = `eitan` @`localhost` PROCEDURE `fieldExists`(
    OUT _exists BOOLEAN,
    IN tableName CHAR(255),
    IN columnName CHAR(255),
    IN dbName CHAR(255)
) BEGIN
SET
    @_dbName := IF(dbName IS NULL, database(), dbName);
IF CHAR_LENGTH(@_dbName) = 0 THEN
SELECT
    FALSE INTO _exists;
ELSE
SELECT
    IF(count(*) > 0, TRUE, FALSE) INTO _exists
FROM
    information_schema.COLUMNS c
WHERE
    c.TABLE_SCHEMA = @_dbName
    AND c.TABLE_NAME = tableName
    AND c.COLUMN_NAME = columnName;
END IF;
END