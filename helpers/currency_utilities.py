import dateutil
from datetime import datetime

def add_ndate_element_to_date(starting_date, date_element, qty):
    return starting_date + create_relative_date_element(date_element, qty)
 


def substract_ndate_element_to_date(starting_date, date_element, qty):
    return starting_date - create_relative_date_element(date_element, qty)
 


def create_relative_date_element(date_element, qty):
    if date_element == "years":
        return  dateutil.relativedelta.relativedelta(years=qty)
    if date_element == "months":
        return  dateutil.relativedelta.relativedelta(months=qty)
    if date_element == "days":
        return  dateutil.relativedelta.relativedelta(days=qty)


def date_to_string(custom_date) -> str:
    return custom_date.strftime('%Y-%m-%d')



def get_dates_in_between(starting_date, _till, date_element = "days"):
    exchange_date_list =[]

    for n in range(0, _till):
        custom_date = date_to_string(add_ndate_element_to_date(starting_date, date_element, n))
        exchange_date_list.append(custom_date)
    
    return exchange_date_list



def get_year_to_str(year=datetime.now()) -> str:
    return year.strftime('%Y')




def get_year(str_year):
    return datetime.strptime(str_year, '%Y')



def create_currency_pairs(list):
    currency_pairs = []
    for currency in list:
        if currency == "USD":
            continue
        currency_pairs.append(tuple(("USD", currency)))
    
    return currency_pairs




