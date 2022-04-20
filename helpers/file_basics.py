import json
import os

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def write_file(file, data):
    with open( file, 'w') as file_object:
        file_object.write(data)


def append_to_file( file,data):
    with open( file, 'a') as file_object:
        file_object.write(data)


def write_json_file( file, data ):
    with open( file, 'w') as fp:
        json.dump(data, fp)


def read_json_file( file ):
    jd = open(file)
    data = json.load(jd)
    return data


def read_file(file):
    archivo = open(file, "r")
    return archivo.read()


def count_files_in_folder( folder ):
    # path = BASE_DIR + folder
    total_files = 0

    for base, dirs, files in os.walk(folder):
        for file in files:
            total_files += 1

    print(f'Total number of files {total_files} in folder {folder}')
    return total_files


def files_in_folder( folder ):
    # path = BASE_DIR + folder
    files_list = []

    for base, dirs, files in os.walk(folder):
        for file in files:
            files_list.append(file)

    return files_list
