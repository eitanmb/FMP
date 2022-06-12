# Funciones para la conección y operacion con BBDD
# MySql
import sys
import mysql.connector
from sqlalchemy import create_engine
import pandas as pd
from ..helpers.File import *

def engine_connetion(CONNECTION: object):
    engine = create_engine(
        f"mysql+pymysql://{CONNECTION['user']}:{CONNECTION['password']}@{CONNECTION['host']}/{CONNECTION['database']}")
    return engine


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


def create_db(CONNECTION):
    conn = mysql.connector.connect(
        host=CONNECTION['host'],
        user=CONNECTION['user'],
        password=CONNECTION['password']
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {CONNECTION['database']}")


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
