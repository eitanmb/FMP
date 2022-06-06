from datetime import datetime
from helpers import File


def set_datetime_now() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


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

def is_list(data):
    return type(data) is list

def is_dict(data):
    return isinstance(data, dict)

def is_not_empty(data):
    return len(data) > 0
