ENDPOINTS = {
    "outlook"                 : "{url_base}/v4/company-outlook?symbol={ticker}&apikey={apikey}",
    "IS"                      : "{url_base}/v3/income-statement/{ticker}?apikey={apikey}",
    "BS"                      : "{url_base}/v3/balance-sheet-statement/{ticker}?apikey={apikey}",
    "CF"                      : "{url_base}/v3/cash-flow-statement/{ticker}?apikey={apikey}",
    "holders"                 : "{url_base}/v3/institutional-holder/{ticker}?apikey={apikey}",
    "profile"                 : "{url_base}/v3/profile/{ticker}?apikey={apikey}",
    "forex"                   : "{url_base}/v3/historical-price-full/{ticker}?apikey={apikey}",
    "floatshares"             : "{url_base}/v4/shares_float?symbol={ticker}&apikey={apikey}",
    "financial_list"          : "{url_base}/v3/financial-statement-symbol-lists?apikey={apikey}",
    "tradeble_list"           : "{url_base}/v3/available-traded/list?apikey={apikey}",
    "stock_list"              : "{url_base}/v3/stock/list?apikey={apikey}",
    "forex_pairs"             : "{url_base}/v3/symbol/available-forex-currency-pairs?apikey={apikey}",
    "holders_available_dates" : "{url_base}/v4/institutional-ownership/portfolio-date?cik={cik}&apikey={apikey}",
    "stock_ownership"         : "{url_base}/v4/institutional-ownership/institutional-holders/symbol-ownership?date={date}&symbol={symbol}&page={page}&apikey={apikey}",
}

