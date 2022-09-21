import os
import sys
sys.path.append("..")
from helpers.utilities import get_date, get_subdirectories_by_date, make_directory, join_path

def init():
    BASE_DIR: str = os.path.dirname(os.path.abspath('exec.py'))
    
    DIRS: object = {
        'ROOT_JSON_DIR': "",
        'CURRENT_JSON_FOLDER': ""
    }
    DIRS['ROOT_JSON_DIR'] = f'{ BASE_DIR }/json'

    subdirectories_list: list = []
    date: str = get_date()
    subdirectories_list = get_subdirectories_by_date(date)

    create_json_directory_structure(DIRS["ROOT_JSON_DIR"], subdirectories_list)

    if DIRS['CURRENT_JSON_FOLDER'] == "":
        DIRS['CURRENT_JSON_FOLDER'] = set_current_json_folder(
            DIRS['ROOT_JSON_DIR'], subdirectories_list)

    return DIRS


def create_json_directory_structure(ROOT_JSON_DIR: str, subdirectories_list: list):
    year_path = join_path(
        ROOT_JSON_DIR, subdirectories_list[0])
    make_directory(year_path)

    month_path = join_path(year_path, subdirectories_list[1])
    make_directory(month_path)


def set_current_json_folder(ROOT_JSON_DIR: str, subdirectories_list: list):
    return join_path(ROOT_JSON_DIR, subdirectories_list[0], subdirectories_list[1])