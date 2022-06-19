from .download_params import *

profile = {
    'current': 'profile',
    'next': 'IS',
    'kwargs': profile_kwargs
}

incomeStatement = {
    'current': 'IS',
    'next': 'BS',
    'kwargs': income_statements_kwargs
}

balanceSheet = {
    'current': 'BS',
    'next': 'CF',
    'kwargs': balance_sheet_kwargs
}

cashFlow = {
    'current': 'CF',
    'next': 'finished',
    'kwargs': cash_flow_kwargs
}

exec_order = [
    profile,
    incomeStatement,
    balanceSheet,
    cashFlow
]
