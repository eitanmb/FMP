
base_url = "https://www.investing.com"

scrap_fx = {
    "pick_calendar": "DatePickerWrapper_icon__2w6rl",
    "start_date": "//div[@class='NativeDateRangeInput_root__30aM8']//input[@type='date']",
    "end_date": "//div[@class='NativeDateInput_root__27QxI']//following-sibling::div//input[@type='date']",
    "apply": "//button[contains(@class,'apply-button__3sdPK')]",
    "price_table": {
        "theader_th": "//table[contains(@data-test,'historical')]/thead/tr/th//span/text()",
        "tbody_tr": "//table[contains(@data-test,'historical')]/tbody/tr",
        "tbody_td": "td//text()"
    }
}

scrap_popup_promo = {
    "close": "//i[@class='popupCloseIcon largeBannerCloser']"
}

