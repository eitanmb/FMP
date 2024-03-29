import os
from datetime import datetime
from helpers.File import File

def set_datetime_now() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_date() -> str:
    # return '2022-08'
    return datetime.now().strftime('%Y-%m')

def get_year() -> str:
    # return "2022"
    return datetime.now().strftime('%Y')

def get_month() -> str:
    # return "08"
    return datetime.now().strftime('%m')

def get_string_timestamp():
    return datetime.now().strftime("%d-%m-%Y_%H:%M:%S")

    
def get_subdirectories_by_date(date: str) -> list:
    return date.split('-')


def join_path(*routes):
    return os.path.join(*routes)


def make_directory(path: str):
    try:
        os.makedirs(path)
        print("Directory ", path,  " Created ")
    except FileExistsError:
        print("Directory ", path,  " already exists")

def set_init_end_time(ini_fin: str, data: str) -> str:
    return f"{ ini_fin } { data }: { set_datetime_now() }"


def set_init_time(data: str) -> str:
    return set_init_end_time("Inicio", data)


def set_end_time(data: str) -> str:
    return set_init_end_time("Fin", data)


def string_to_tuple(cadena: str) -> tuple:
    return tuple(cadena.split(','))


def write_lastTicker_file(last_ticker: str, caller: str, ticker_position: str) -> None:
    File.write(last_ticker, f'{caller},{ticker_position}')


def lastTicker_string_to_tuple(last_ticker_file):
    last_ticker_string: str = File.read(last_ticker_file)
    return string_to_tuple(last_ticker_string)


def get_lastTicker_info(last_ticker_file) -> tuple:
    last_ticker_tuple = lastTicker_string_to_tuple(last_ticker_file)
    return last_ticker_tuple


def print_messages(*messages):
    print(*messages)


def get_download_ticker_possition(tickers_list, ticker):
        return tickers_list.index(ticker)


def return_start_from_tickers(how_many_tickers, last_ticker):
    if how_many_tickers == 0:
        return 0
    return int(get_lastTicker_info(last_ticker)[1])