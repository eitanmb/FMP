import sys
sys.path.append("..")
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

from helpers.File import *
from helpers.utilities import get_year, get_month
from sql.definitions import CONNECTION


def set_dbname():
    CONNECTION['database'] = f'FMP_{ get_year() }_{ get_month() }'

def create_db():
    set_dbname()
    conn = mysql.connector.connect(
        host=CONNECTION['host'],
        user=CONNECTION['user'],
        password=CONNECTION['password']
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {CONNECTION['database']}")


def engine_connetion():
    create_db()
    return create_engine(f"mysql+pymysql://{CONNECTION['user']}:{CONNECTION['password']}@{CONNECTION['host']}/{CONNECTION['database']}")


def create_table_from_dataframe(df, engine, table_name):
    try:
        df.to_sql(table_name, engine, index=False, if_exists='append')
        return f"Tabla {table_name} y datos añadidos"
    except Exception as e:
        return e


def execute_query(sql, engine):
    try:
        engine.execute(sql)
        return "Query executed"
    except Exception as e:
        return e


def creat_dataframe_from_data(folder: str, engine, table_name: str):
    count = 1
    for file in File.files_in_folder(folder):
        print(f"Counter financials = {count}")

        try:
            df = pd.read_json(f"{folder}/{file}", orient='columns')

            if df.empty == False:
                print(file, df)
                print(create_table_from_dataframe(df, engine, table_name))
            else:
                print("Dataframe vacío")

        except Exception as e:
            print(e)

        count += 1
