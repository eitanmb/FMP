import requests
import ast

def get_currency_list():
    url = "https://currency-converter5.p.rapidapi.com/currency/list"

    headers = {
        "X-RapidAPI-Key": "917edfaa46mshe1c92ce766bdd64p1457a6jsn102bd286b04b",
        "X-RapidAPI-Host": "currency-converter5.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)

    response_text = response.text
    response_dict = ast.literal_eval(response_text)
    currency_list = []

    for key in response_dict['currencies'].keys():
        currency_list.append(key)

    return currency_list

