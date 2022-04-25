# Requires the PyMongo package.
# https://api.mongodb.com/python/current
from pymongo import *
import pandas as pd
import re

client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false')
result = client['dbfmp']['outlook'].aggregate([
    {
        '$match': {
            '$and': [
                {
                    'profile.industry': 'Textile Manufacturing',
                    'profile.country': 'US',
                    'profile.description': re.compile(r"subsidia*"),
                    'financialsAnnual.income': {
                        '$elemMatch': {
                            'date': {
                                '$in': [
                                    re.compile(r"2020"), re.compile(r"2019"), re.compile(r"2018")
                                ]
                            },
                            'revenue': {
                                '$gt': 0
                            },
                            'costOfRevenue': {
                                '$gt': 0
                            },
                            'researchAndDevelopmentExpenses': {
                                '$eq': 0
                            }
                        }
                    }
                }
            ]
        }
    }, {
        '$addFields': {
            'financialsAnnual.income': {
                '$map': {
                    'input': '$financialsAnnual.income',
                    'as': 'is',
                    'in': {
                        'date': '$$is.date',
                        'symbol': '$$is.symbol',
                        'reportedCurrency': '$$is.reportedCurrency',
                        'fillingDate': '$$is.fillingDate',
                        'acceptedDate': '$$is.acceptedDate',
                        'period': '$$is.period',
                        'revenue': '$$is.revenue',
                        'costOfRevenue': '$$is.costOfRevenue',
                        'grossProfit': '$$is.grossProfit',
                        'grossProfitRatio': '$$is.grossProfitRatio',
                        'researchAndDevelopmentExpenses': '$$is.researchAndDevelopmentExpenses',
                        'generalAndAdministrativeExpenses': '$$is.generalAndAdministrativeExpenses',
                        'sellingAndMarketingExpenses': '$$is.sellingAndMarketingExpenses',
                        'sellingGeneralAndAdministrativeExpenses': '$$is.sellingGeneralAndAdministrativeExpenses',
                        'interestExpense': '$$is.interestExpense',
                        'depreciationAndAmortization': '$$is.depreciationAndAmortization',
                        'costAndExpenses': '$$is.costAndExpenses',
                        'gastosOperativos': {
                            '$subtract': [
                                '$$is.costAndExpenses', '$$is.costOfRevenue'
                            ]
                        },
                        'otherExpenses': '$$is.otherExpenses',
                        'operatingExpenses': '$$is.operatingExpenses',
                        'ebitda': '$$is.ebitda',
                        'ebitdaratio': '$$is.ebitdaratio',
                        'operatingIncome': '$$is.operatingIncome',
                        'operatingIncomeRatio': '$$is.operatingIncomeRatio',
                        'totalOtherIncomeExpensesNet': '$$is.totalOtherIncomeExpensesNet',
                        'incomeBeforeTax': '$$is.incomeBeforeTax',
                        'incomeBeforeTaxRatio': '$$is.incomeBeforeTaxRatio',
                        'incomeTaxExpense': '$$is.incomeTaxExpense',
                        'netIncome': '$$is.netIncome',
                        'netIncomeRatio': '$$is.netIncomeRatio',
                        'eps': '$$is.eps',
                        'epsdiluted': '$$is.epsdiluted',
                        'weightedAverageShsOut': '$$is.weightedAverageShsOut',
                        'weightedAverageShsOutDil': '$$is.weightedAverageShsOutDil',
                        'link': '$$is.link',
                        'finalLink': '$$is.finalLink'
                    }
                }
            }
        }
    }, {
        '$addFields': {
            'indicatordsSourceAnnual': {
                '$map': {
                    'input': {
                        '$range': [
                            0, {
                                '$size': '$financialsAnnual.income'
                            }, 1
                        ]
                    },
                    'as': 'rango',
                    'in': {
                        '$mergeObjects': [
                            {
                                '$arrayElemAt': [
                                    '$financialsAnnual.income', '$$rango'
                                ]
                            }, {
                                '$arrayElemAt': [
                                    '$financialsAnnual.balance', '$$rango'
                                ]
                            }
                        ]
                    }
                }
            }
        }
    }, {
        '$addFields': {
            'financialsAnnual.tpIndicators': {
                '$map': {
                    'input': '$indicatordsSourceAnnual',
                    'as': 's',
                    'in': {
                        'date': '$$s.date',
                        'symbol': '$$s.symbol',
                        'period': '$$s.period',
                        'MO': {
                            '$multiply': [
                                {
                                    '$divide': [
                                        '$$s.operatingIncome', '$$s.revenue'
                                    ]
                                }, 100
                            ]
                        },
                        'MOCG': {
                            '$multiply': [
                                {
                                    '$divide': [
                                        '$$s.operatingIncome', '$$s.costAndExpenses'
                                    ]
                                }, 100
                            ]
                        },
                        'MBV': {
                            '$multiply': [
                                {
                                    '$divide': [
                                        '$$s.grossProfit', '$$s.revenue'
                                    ]
                                }, 100
                            ]
                        },
                        'MBC': {
                            '$multiply': [
                                {
                                    '$divide': [
                                        '$$s.grossProfit', '$$s.costOfRevenue'
                                    ]
                                }, 100
                            ]
                        },
                        'ROCE': {
                            '$multiply': [
                                {
                                    '$divide': [
                                        '$$s.ebitda', {
                                            '$subtract': [
                                                '$$s.totalAssets', '$$s.totalCurrentLiabilities'
                                            ]
                                        }
                                    ]
                                }, 100
                            ]
                        }
                    }
                }
            }
        }
    }, {
        '$project': {
            '_id': 0,
            'profile.companyName': 1,
            # 'profile.description': 1,
            'profile.symbol': 1,
            'profile.exchange': 1,
            'profile.country': 1,
            'profile.sector': 1,
            'profile.industry': 1,
            'profile.website': 1,
            'financialsAnnual.income.reportedCurrency': 1,
            'financialsAnnual.income.date': 1,
            'financialsAnnual.income.revenue': 1,
            # 'financialsAnnual.income.costOfRevenue': 1,
            # 'financialsAnnual.income.costAndExpenses': 1,
            # 'financialsAnnual.income.operatingIncome': 1,
            'financialsAnnual.tpIndicators.MO': 1,
            'financialsAnnual.tpIndicators.MOCG': 1,
            # 'financialsAnnual.tpIndicators.MBV': 1,
            # 'financialsAnnual.tpIndicators.MBC': 1,
            # 'financialsAnnual.tpIndicators.ROCE': 1
        }
    }
])

for r in result:
    df1 = pd.DataFrame.from_dict(r['profile'], orient='index')
    df2 = pd.DataFrame.from_dict(r['financialsAnnual']['income'], orient='columns')
    df3 = pd.DataFrame.from_dict(r['financialsAnnual']['tpIndicators'], orient='columns')
    df4 = df2.join(df3, lsuffix='_caller', rsuffix='_other')
    df = df1.T.join(df4, on=None, how='right', lsuffix='', rsuffix='', sort=False).fillna(value=r['profile'])

    _index = ['companyName','symbol','exchange','country','sector','industry','website','reportedCurrency']
    print(df.pivot(index=_index,columns='date'))
