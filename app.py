import os
from config import setup
from helpers.utilities import *
from config.arguments import income_statements_kwargs, balance_sheet_kwargs, cash_flow_kwargs
from core.DataPersistence import SqlDataPersistence
from core.DataDownload import DataDownload
from config.setup import engine


income_statements_download = DataDownload(**income_statements_kwargs)
income_statements_download.create_folder()
income_statements_sql = SqlDataPersistence(engine, **income_statements_kwargs)

balance_sheet_download = DataDownload(**balance_sheet_kwargs)
balance_sheet_download.create_folder()
balance_sheet_sql = SqlDataPersistence(engine, **balance_sheet_kwargs)

cash_flow_download = DataDownload(**cash_flow_kwargs)
cash_flow_download.create_folder()
cash_flow_sql = SqlDataPersistence(engine, **cash_flow_kwargs)