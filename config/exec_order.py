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
    'next': 'outlook',
    'kwargs': cash_flow_kwargs
}

outlook = {
    'current': 'outlook',
    'next': 'forex',
    'kwargs': outlook_kwargs
}

forex = {
    'current': 'forex',
    'next': 'finished',
    'kwargs': forex_kwargs
}

exec_order = [
    profile,
    incomeStatement,
    balanceSheet,
    cashFlow,
    outlook,
    forex
]
