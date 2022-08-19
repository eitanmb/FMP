import sys
sys.path.append("..")

from noSql.definitions import FX_NOSQl


def init(DIRS):
    BASE_FOLDER: str = DIRS['CURRENT_JSON_FOLDER']

    INV_URLS = {
        "base": "https://www.investing.com",
        "fx": "/currencies"
    }
    
    TRACKER_FILE = 'inv_fetch_tracker.txt'

    fx_kwargs = {
        'domain':'forex',
        'folder': f'{BASE_FOLDER}/forex',
        'url_prefix': f"{INV_URLS['base']}{INV_URLS['fx']}",
        'date_range': {
            'start': '2008-01-01',
            'end':'2022-07-31'
        },
        'scrap': {
            "pick_calendar": "DatePickerWrapper_icon__2w6rl",
            "start_date": "//div[@class='NativeDateRangeInput_root__30aM8']//input[@type='date']",
            "end_date": "//div[@class='NativeDateInput_root__27QxI']//following-sibling::div//input[@type='date']",
            "apply_date_range": "//button[contains(@class,'apply-button__3sdPK')]",
            "price_table": {
                "theader_th": "//table[contains(@data-test,'historical')]/thead/tr/th//span/text()",
                "tbody_tr": "//table[contains(@data-test,'historical')]/tbody/tr",
                "tbody_td": "td//text()"
            }
        },
        'sql': None,
        'noSql': FX_NOSQl
    }


    SCRAP_POPUP_PROMO = {
        "close": "//i[@class='popupCloseIcon largeBannerCloser']"
    }

    AVAILABLE_PAIRS = [
                        ("EUR", "USD"), ("GBP", "USD"), ("USD", "JPY"), ("USD", "CHF"), ("AUD", "USD"), ("USD", "CAD"), 
                        ("NZD", "USD"), ("USD", "ZAR"), ("USD", "TRY"), ("USD", "MXN"), ("USD", "PLN"), ("USD", "SEK"), 
                        ("USD", "SGD"), ("USD", "DKK"), ("USD", "NOK"), ("USD", "ILS"), ("USD", "HUF"), ("USD", "CZK"), 
                        ("USD", "THB"), ("USD", "AED"), ("USD", "JOD"), ("USD", "KWD"), ("USD", "HKD"), ("USD", "SAR"), 
                        ("USD", "INR"), ("USD", "KRW"), ("BRL", "USD"), ("CAD", "USD"), ("CHF", "USD"), ("FJD", "USD"), 
                        ("GHS", "USD"), ("JPY", "USD"), ("KYD", "USD"), ("SGD", "USD"), ("USD", "AMD"), ("USD", "ANG"), 
                        ("USD", "ARS"), ("USD", "AUD"), ("USD", "BBD"), ("USD", "BDT"), ("USD", "BGN"), ("USD", "BHD"), 
                        ("USD", "BIF"), ("USD", "BND"), ("USD", "BOB"), ("USD", "BRL"), ("USD", "BSD"), ("USD", "BWP"), 
                        ("USD", "BZD"), ("USD", "CLP"), ("USD", "CNY"), ("USD", "COP"), ("USD", "CRC"), ("USD", "CUP"), 
                        ("USD", "DJF"), ("USD", "DOP"), ("USD", "DZD"), ("USD", "EGP"), ("USD", "ETB"), ("USD", "EUR"), 
                        ("USD", "FJD"), ("USD", "GBP"), ("USD", "GEL"), ("USD", "GHS"), ("USD", "GMD"), ("USD", "GNF"), 
                        ("USD", "GTQ"), ("USD", "HNL"), ("USD", "HRK"), ("USD", "HTG"), ("USD", "IDR"), ("USD", "IQD"), 
                        ("USD", "IRR"), ("USD", "ISK"), ("USD", "JMD"), ("USD", "KES"), ("USD", "KHR"), ("USD", "KMF"), 
                        ("USD", "KZT"), ("USD", "LAK"), ("USD", "LBP"), ("USD", "LKR"), ("USD", "LSL"), ("USD", "LYD"), 
                        ("USD", "MAD"), ("USD", "MDL"), ("USD", "MGA"), ("USD", "MKD"), ("USD", "MMK"), ("USD", "MOP"), 
                        ("USD", "MRO"), ("USD", "MUR"), ("USD", "MVR"), ("USD", "MWK"), ("USD", "MYR"), ("USD", "NAD"), 
                        ("USD", "NGN"), ("USD", "NIO"), ("USD", "NPR"), ("USD", "NZD"), ("USD", "OMR"), ("USD", "PAB"), 
                        ("USD", "PEN"), ("USD", "PGK"), ("USD", "PHP"), ("USD", "PKR"), ("USD", "PYG"), ("USD", "QAR"), 
                        ("USD", "RON"), ("USD", "RSD"), ("USD", "RUB"), ("USD", "RWF"), ("USD", "SCR"), ("USD", "SDG"), 
                        ("USD", "SOS"), ("USD", "STD"), ("USD", "SVC"), ("USD", "SYP"), ("USD", "SZL"), ("USD", "TND"), 
                        ("USD", "TTD"), ("USD", "TWD"), ("USD", "TZS"), ("USD", "UAH"), ("USD", "UGX"), ("USD", "UYU"), 
                        ("USD", "UZS"), ("USD", "VND"), ("USD", "VUV"), ("USD", "XAF"), ("USD", "XCD"), ("USD", "XOF"), 
                        ("USD", "XPF"), ("USD", "YER"), ("USD", "ZMK"), ("AED", "USD"), ("ARS", "USD"), ("CNY", "USD"), 
                        ("DKK", "USD"), ("HKD", "USD"), ("ILS", "USD"), ("MXN", "USD"), ("NOK", "USD"), ("PLN", "USD"), 
                        ("RUB", "USD"), ("SAR", "USD"), ("SEK", "USD"), ("TRY", "USD"), ("TWD", "USD"), ("ZAR", "USD"), 
                        ("UYU", "USD"), ("PYG", "USD"), ("CLP", "USD"), ("COP", "USD"), ("PEN", "USD"), ("NIO", "USD"), 
                        ("BOB", "USD"), ("KRW", "USD"), ("EGP", "USD"), ("USD", "BYN"), ("USD", "MZN"), ("INR", "USD"), 
                        ("JOD", "USD"), ("KWD", "USD"), ("USD", "AZN"), ("USD", "CNH"), ("USD", "KGS"), ("USD", "TJS"), 
                        ("MYR", "USD"), ("UAH", "USD"), ("HUF", "USD"), ("IDR", "USD"), ("USD", "AOA"), ("VND", "USD"), 
                        ("BYN", "USD"), ("XBR", "USD"), ("THB", "USD"), ("PHP", "USD"), ("USD", "TMT"), ("USD", "BRLT"), 
                        ("USD", "MNT"), ("USD", "AFN"), ("AFN", "USD"), ("SYP", "USD"), ("IRR", "USD"), ("IQD", "USD"), 
                        ("USD", "ZWL"), ("CZK", "USD")
                    ]

    return {
        "TRACKER_FILE": TRACKER_FILE,
        "fx_kwargs": fx_kwargs,
        "SCRAP_POPUP_PROMO": SCRAP_POPUP_PROMO,
        "AVAILABLE_PAIRS":AVAILABLE_PAIRS
    }
