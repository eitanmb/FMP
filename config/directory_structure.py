import os
from datetime import datetime

def get_date() -> str:
    return datetime.now().strftime('%Y-%m')


def get_subdirectories_by_date( date: str ) -> list: 
    return date.split('-')


def make_directory( path: str ):
    try:
        # Create target Directory
        os.makedirs( path )
        print("Directory " , path ,  " Created ") 

    except FileExistsError:
        print("Directory " , path ,  " already exists") 



def create_json_directory_structure( ROOT_JSON_DIR: str, subdirectories_list: list ):
    
    json_sudirs_by_date: list = [ subdirectories_list[0], subdirectories_list[1] ]
    json_data_subdirs: list = [ 'financials', 'outlook', 'institutional-holders-originales', 'institutional-holders', 'profiles', 'shares', 'sic' ]
    json_financials_subdirs: list = [ 'IS', 'BS', 'CF' ]

    # Create json directory structure
    path: str = ROOT_JSON_DIR

    for i in range(0, len(json_sudirs_by_date)):
        path = os.path.join( path, json_sudirs_by_date[i] )
        make_directory( path )
            
    for subdir in json_data_subdirs:
        subpath = os.path.join( path, subdir )

        if subdir == 'financials':
            for financial_subdir in json_financials_subdirs:
                fin_subpath = os.path.join( subpath, financial_subdir )
                make_directory(fin_subpath)
        else:
            make_directory(subpath)


def set_current_json_folder( ROOT_JSON_DIR: str, subdirectories_list: list ):
    return os.path.join( ROOT_JSON_DIR, subdirectories_list[0], subdirectories_list[1] )
