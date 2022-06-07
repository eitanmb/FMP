import os
from config import setup
from helpers.utilities import *
from app import profile, company_outlook, \
    financial_info, institutional_holders as holders, \
    float_shares as floatshares, shareholders, forex
from typing import NoReturn, Callable, List, Dict
import sys

# Configura lo necesario para la descarga desde FMP
setup.init()


execution_func:str = '';

def execution_routine( func_name:str, func, argument, next_func_name:str ) -> NoReturn:
    global execution_func

    print(f"START {func_name}")
    
    if argument is None :
        func.init()
    else:
        func.init(argument) 
    
    write_lastTicker_file( 'lastTicker.txt', next_func_name,'0')
    execution_func = get_lastTicker_info( 'lastTicker.txt' )[0]
    print(f"END {func_name}")


# Registra la funcion que se esta ejecutando
# Si el script se detiene, se retoma desde la funcion en ejecución
if get_lastTicker_info( 'lastTicker.txt' )[0] == 'finished':
    print('FINISHED')
    sys.exit()


if os.path.getsize('lastTicker.txt') == 0:
    execution_func = 'profile'
else:
    execution_func = get_lastTicker_info( 'lastTicker.txt' )[0]


if execution_func == "profile":
    execution_routine('PROFILE', profile, None, 'outlook')

if execution_func == "outlook":
    execution_routine('COMPANY OUTLOOK', company_outlook, None, 'IS')

if execution_func == "IS":
    execution_routine('INCOME STATEMENT', financial_info, 'IS', 'BS')

if execution_func == "BS":
    execution_routine('BALANCE SHEET', financial_info, 'BS', 'CF')

if execution_func == "CF":
    execution_routine('CASH FLOW', financial_info, 'CF', 'holders')

if execution_func == "holders":
    execution_routine('INSTITUTIONAL HOLDERS', holders, None, 'floatshares')

if execution_func == "floatshares":
    execution_routine('FLOAT SHARES', floatshares, None, 'shareholders')

if execution_func == "shareholders":
    execution_routine('SHAREHOLDERS', shareholders, None, 'forex')

# HARD CODED - REVISAR E IMPLEMENTAR MEJOR
if execution_func == "forex":
    execution_routine('FOREX', forex, None, 'finished')

if execution_func == "finished":
    print('FINISHED')



# PRUEBA
# profile.init()
# company_outlook.init()
# financial_info.init('IS')
# financial_info.init('BS')
# financial_info.init('CF')
# holders.init()
# floatshares.init()
# shareholders.init()

