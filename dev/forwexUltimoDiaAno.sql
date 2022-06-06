select * from forex where (date = LAST_DAY("2021-12-01") or date = LAST_DAY("2020-12-01") 
or date = LAST_DAY("2019-12-01")) ORDER By pair ASC, date DESC 
