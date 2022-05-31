ENDPOINTS = {
    "outlook"     : "{url_base}/v4/company-outlook?symbol={ticker}&apikey={api}",
    "IS"          : "{url_base}/v3/income-statement/{ticker}?apikey={api}",
    "BS"          : "{url_base}/v3/balance-sheet-statement/{ticker}?apikey={api}",
    "CF"          : "{url_base}/v3/cash-flow-statement/{ticker}?apikey={api}",
    "holders"     : "{url_base}/v3/institutional-holder/{ticker}?apikey={api}",
    "profile"     : "{url_base}/v3/profile/{ticker}?apikey={api}",
    "floatshares" : "{url_base}/v4/shares_float?symbol={ticker}&apikey={api}"
}