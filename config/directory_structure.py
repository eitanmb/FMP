import os
from datetime import datetime


def get_date() -> str:
    return '2023-01'
    # return datetime.now().strftime('%Y-%m')


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


def create_json_directory_structure(ROOT_JSON_DIR: str, subdirectories_list: list):
    year_path = join_path(
        ROOT_JSON_DIR, subdirectories_list[0])
    make_directory(year_path)

    month_path = join_path(year_path, subdirectories_list[1])
    make_directory(month_path)


def set_current_json_folder(ROOT_JSON_DIR: str, subdirectories_list: list):
    return join_path(ROOT_JSON_DIR, subdirectories_list[0], subdirectories_list[1])
