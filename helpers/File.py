import json
import os
import os.path


class File:

    @staticmethod
    def write(file, data):
        with open(file, 'w') as file_object:
            file_object.write(data)

    @staticmethod
    def append(file, data):
        with open(file, 'a') as file_object:
            file_object.write(data)

    @staticmethod
    def read(file):
        archivo = open(file, "r")
        return archivo.read()

    @staticmethod
    def write_json(file, data):
        with open(file, 'w') as fp:
            json.dump(data, fp)

    @staticmethod
    def read_json(file):
        jd = open(file)
        data = json.load(jd)
        return data

    @staticmethod
    def count_files_in_folder(folder):
        # path = BASE_DIR + folder
        total_files = 0

        for base, dirs, files in os.walk(folder):
            for file in files:
                total_files += 1

        print(f'Total number of files {total_files} in folder {folder}')
        return total_files

    @staticmethod
    def files_in_folder(folder):
        # path = BASE_DIR + folder
        files_list = []

        for base, dirs, files in os.walk(folder):
            for file in files:
                files_list.append(file)

        return files_list

    @staticmethod
    def file_is_empty(file):
        if os.stat(file).st_size == 0:
            return True
        return False

    @staticmethod
    def file_exist(file):
        if os.path.exists(file):
            return True
        return False