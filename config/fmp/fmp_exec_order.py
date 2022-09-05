from . import fmp_download_params

def init(DIRS, TICKERS_FILES):
    fmp_arguments = fmp_download_params.init(DIRS, TICKERS_FILES)
    
    profile = {
        'current': 'profile',
        'next': 'IS',
        'kwargs': fmp_arguments["profile_kwargs"]
    }

    incomeStatement = {
        'current': 'IS',
        'next': 'BS',
        'kwargs': fmp_arguments["income_statements_kwargs"]
    }
    
    balanceSheet = {
        'current': 'BS',
        'next': 'CF',
        'kwargs': fmp_arguments["balance_sheet_kwargs"]
    }
    
    cashFlow = {
        'current': 'CF',
        'next': 'outlook',
        'kwargs': fmp_arguments["cash_flow_kwargs"]
    }
    
    outlook = {
        'current': 'outlook',
        'next': 'forex',
        'kwargs': fmp_arguments["outlook_kwargs"]
    }
    
    forex = {
        'current': 'forex',
        'next': 'finished',
        'kwargs': fmp_arguments["forex_kwargs"] 
    }
    
    return  [
        profile,
        incomeStatement,
        balanceSheet,
        cashFlow,
        # outlook,
        forex
    ]
    