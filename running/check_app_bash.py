#!/usr/bin/env python3

import psutil
import subprocess
from dotenv import load_dotenv
import os
from datetime import datetime


load_dotenv()

DIR = os.environ.get("BASE_DIR")
status = False


# obtain de process PID
output = os.popen('ps l | grep app.py')
processes = output.readlines()
process_list = []

for process in processes:
    if process.find('python app.py') != -1:
        process_list = process.split(' ')


if process_list != []:
    while ('' in process_list):
        process_list.remove('')

    PID = int(process_list[2])

    print(PID)

    if psutil.pid_exists(PID):
        status = True

    print('status', True)

if status != True:
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("Not running")

    #Colocarse en el directorio Investing para correr el programa
    os.chdir(DIR)

    # Define command as string
    cmd = 'tmux kill-server'
    sp = subprocess.Popen(cmd, shell=True)
    sp.wait()

    # cmd1 = 'tmux new -d -s Scraping\; send-keys "pipenv run python inv_explorer_bot.py | tee -a log/exp.log" Enter'
    cmd1 = 'tmux new -d -s FMP\; send-keys "pipenv run python app.py" Enter'
    print(cmd1)
    # Use shell to execute the command and store it in sp variable
    sp1 = subprocess.Popen(cmd1, shell=True)

    # Store the return code in rc variable
    rc=sp1.wait()

    # Print the content of sp variable
    print(sp1)
    print("\n")
