import sys
sys.path.append("..")

from helpers.utilities import make_directory, join_path

def create_json_directory_structure(ROOT_JSON_DIR: str, subdirectories_list: list):
    year_path = join_path(
        ROOT_JSON_DIR, subdirectories_list[0])
    make_directory(year_path)

    month_path = join_path(year_path, subdirectories_list[1])
    make_directory(month_path)


def set_current_json_folder(ROOT_JSON_DIR: str, subdirectories_list: list):
    return join_path(ROOT_JSON_DIR, subdirectories_list[0], subdirectories_list[1])
