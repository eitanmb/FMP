import sys
sys.path.append("..")

from helpers.utilities import get_year, get_month


_date: str = f"{get_month()}{get_year()}"

PROFILE_NOSQl =  {
    'collection_name':f'{_date}_profile',
    'indexes':
    {   
        'symbol_index':'[("symbol",1)], name="symbol_index", unique=True',
        'info_index': '[("companyName","text"),("description","text")], name="info_index", default_language="english"'
            
    }
}

IS_NOSQl = {
    'collection_name':f'{_date}_incomeStatements',
    'indexes': None
}

BS_NOSQl =  {
    'collection_name':f'{_date}_balanceSheet',
    'indexes': None
}

CF_NOSQl =   {
    'collection_name':f'{_date}_cashFlow',
    'indexes': None
}

OUTLOOK_NOSQL = {
    'collection_name':f'{_date}_outlook',
    'indexes': None
}