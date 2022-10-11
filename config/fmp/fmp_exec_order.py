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
        'next': 'finished',
        'kwargs': fmp_arguments["cash_flow_kwargs"]
    }

    ownership = {
        'current': 'ownership',
        'next': 'finished',
        'kwargs': fmp_arguments["ownership_kwargs"]
    }
    
    outlook = {
        'current': 'outlook',
        'next': 'finished',
        'kwargs': fmp_arguments["outlook_kwargs"]
    }
    
    forex = {
        'current': 'forex',
        'next': 'finished',
        'kwargs': fmp_arguments["forex_kwargs"] 
    }
    
    return  [
        # profile,
        # incomeStatement,
        # balanceSheet,
        # cashFlow,
        ownership,
        # outlook,
        # forex
    ]
    