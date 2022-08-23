import os
import sys
sys.path.append("..")

from datetime import datetime
from helpers.utilities import *


class Log:
    def __init__(self, log_name):
        self.log_name = log_name
        self.path = self.get_path()
        self.file = self.set_file()
    
   
    def get_path(self):
        BASE_DIR = os.path.dirname(os.path.abspath('exec.py'))
        LOGS_DIR = "logs"
        return f"{BASE_DIR}/{LOGS_DIR}"

   
    def set_file(self):
        return f"{self.path}/{self.log_name}_{get_string_timestamp()}.log"
    

    def append(self, data):
        with open(self.file, 'a') as file_object:
            file_object.write(f"{data}\n")

    