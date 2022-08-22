import sys
sys.path.append("..")

from helpers.utilities import get_year, get_month


# _date: str = f"{get_month()}{get_year()}"
_date: str = "082022"


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
    'indexes': {   
        'symbol_index':'[("symbol",1)], name="symbol_index", unique=False',    
    }
}

BS_NOSQl =  {
    'collection_name':f'{_date}_balanceSheet',
    'indexes': {   
        'symbol_index':'[("symbol",1)], name="symbol_index", unique=False',    
    }
}

CF_NOSQl =   {
    'collection_name':f'{_date}_cashFlow',
    'indexes': {   
        'symbol_index':'[("symbol",1)], name="symbol_index", unique=False',    
    }
}

OUTLOOK_NOSQL = {
    'collection_name':f'{_date}_outlook',
    'indexes': {   
        'symbol_index':'[("symbol",1)], name="symbol_index", unique=True',    
    }
}

FX_NOSQl = {
    'collection_name':'forex',
     'indexes':
    {   
        'pair_index':'[("Pair",1)], name="pair_index", unique=False',
    }
}


IS_FIELDS = [
    'revenue',
    'costOfRevenue',
    'grossProfit',
    'researchAndDevelopmentExpenses',
    'generalAndAdministrativeExpenses',
    'sellingAndMarketingExpenses',
    'sellingGeneralAndAdministrativeExpenses',
    'otherExpenses',
    'operatingExpenses',
    'costAndExpenses',
    'interestIncome',
    'interestExpense',
    'depreciationAndAmortization',
    'ebitda',
    'netIncome'
]

BS_FIELDS = [
    'cashAndCashEquivalents',
    'shortTermInvestments',
    'cashAndShortTermInvestments',
    'netReceivables',
    'inventory',
    'otherCurrentAssets',
    'totalCurrentAssets',
    'propertyPlantEquipmentNet',
    'goodwill',
    'intangibleAssets',
    'goodwillAndIntangibleAssets',
    'longTermInvestments',
    'taxAssets',
    'otherNonCurrentAssets',
    'totalNonCurrentAssets',
    'otherAssets',
    'totalAssets',
    'accountPayables',
    'shortTermDebt',
    'taxPayables',
    'deferredRevenue',
    'otherCurrentLiabilities',
    'totalCurrentLiabilities',
    'longTermDebt',
    'deferredRevenueNonCurrent',
    'deferredTaxLiabilitiesNonCurrent',
    'otherNonCurrentLiabilities',
    'totalNonCurrentLiabilities',
    'otherLiabilities',
    'capitalLeaseObligations',
    'totalLiabilities',
    'retainedEarnings',
    'accumulatedOtherComprehensiveIncomeLoss',
    'totalEquity',
    'totalLiabilitiesAndTotalEquity',
    'totalInvestments',
    'totalDebt',
    'netDebt'
]

CF_FIELDS = [
    'netIncome',
    'depreciationAndAmortization',
    'deferredIncomeTax',
    'stockBasedCompensation',
    'changeInWorkingCapital',
    'accountsReceivables',
    'inventory',
    'accountsPayables',
    'otherWorkingCapital',
    'otherNonCashItems',
    'netCashProvidedByOperatingActivities',
    'investmentsInPropertyPlantAndEquipment',
    'acquisitionsNet',
    'purchasesOfInvestments',
    'salesMaturitiesOfInvestments',
    'otherInvestingActivites',
    'netCashUsedForInvestingActivites',
    'debtRepayment',
    'dividendsPaid',
    'otherFinancingActivites',
    'netCashUsedProvidedByFinancingActivities',
    'effectOfForexChangesOnCash',
    'netChangeInCash',
    'cashAtEndOfPeriod',
    'cashAtBeginningOfPeriod',
    'operatingCashFlow',
    'capitalExpenditure',
    'freeCashFlow'
]