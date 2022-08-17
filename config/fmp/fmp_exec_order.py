from . import fmp_download_params

def init(DIRS, TICKERS_FILES):
    arguments = fmp_download_params.init(DIRS, TICKERS_FILES)
    
    profile = {
        'current': 'profile',
        'next': 'IS',
        'kwargs': arguments["profile_kwargs"]
    }

    incomeStatement = {
        'current': 'IS',
        'next': 'BS',
        'kwargs': arguments["income_statements_kwargs"]
    }
    
    balanceSheet = {
        'current': 'BS',
        'next': 'CF',
        'kwargs': arguments["balance_sheet_kwargs"]
    }
    
    cashFlow = {
        'current': 'CF',
        'next': 'outlook',
        'kwargs': arguments["cash_flow_kwargs"]
    }
    
    outlook = {
        'current': 'outlook',
        'next': 'forex',
        'kwargs': arguments["outlook_kwargs"]
    }
    
    forex = {
        'current': 'forex',
        'next': 'finished',
        'kwargs': arguments["forex_kwargs"] 
    }
    
    return  [
        profile,
        incomeStatement,
        balanceSheet,
        cashFlow,
        outlook,
        forex
    ]
    