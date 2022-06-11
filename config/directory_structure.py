import os
from datetime import datetime


def get_date() -> str:
    return datetime.now().strftime('%Y-%m')


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


def create_data_dir_path_by_date(root, subdirs) -> None:
    for i in range(0, len(subdirs)):
        path = join_path(root, subdirs[i])
        return path


def create_data_subdirs_path_by_subject(path, subdirs, financials_subdirs):
    for subdir in subdirs:
        subpath = join_path(path, subdir)

        if subdir != 'financials':
            make_directory(subpath)

        if subdir == 'financials':
            create_data_financials_subdirs(subpath, financials_subdirs)


def create_data_financials_subdirs(subpath, financials_subdirs):
    for financial_subdir in financials_subdirs:
        fin_subpath = join_path(subpath, financial_subdir)
        make_directory(fin_subpath)


def create_json_directory_structure(ROOT_JSON_DIR: str, subdirectories_list: list):
    json_sudirs_by_date: list = [
        subdirectories_list[0], subdirectories_list[1]
    ]
    json_data_subdirs: list = [
        'financials', 'outlook', 'institutional-holders-originales',
        'institutional-holders', 'profiles', 'shares', 'sic'
    ]
    json_financials_subdirs: list = ['IS', 'BS', 'CF']

    path_dir_by_date = create_data_dir_path_by_date(
        ROOT_JSON_DIR, json_sudirs_by_date)
    make_directory(path_dir_by_date)
    create_data_subdirs_path_by_subject(
        path_dir_by_date, json_data_subdirs, json_financials_subdirs)


def set_current_json_folder(ROOT_JSON_DIR: str, subdirectories_list: list):
    return join_path(ROOT_JSON_DIR, subdirectories_list[0], subdirectories_list[1])
