import os
import sys
sys.path.append("..")

from core.DataPersistenceSQL import SqlDataPersistence, drop_create_procedure, call_procedures
from core.DataPersistenceNoSQL import NoSqlDataPersistence
from core.fmp.FmpDataDownload import DataDownload
from config.fmp import fmp_tickers
from config.fmp import fmp_exec_order
from helpers.utilities import *
from helpers.File import File
from sql.procedures_PTRA import *
from sql.basics import *


def init(DIRS):

    def get_data_download(kargs):
        download = DataDownload(**kargs)
        download.create_folder()
        download.fetch_data()


    def is_financial_report(report):
        if (report == "IS" or report == "BS" or report == "CF"):
            return True


    def create_data_persistence_sql(kargs):
        sql = SqlDataPersistence(mysql_engine, **kargs)
        sql.drop_table()
        sql.create_table()
        sql.add_indexes()
        sql.insert_data_from_dataframe()
        sql.alter_table()


    def create_data_persistence_noSQL(kargs):
        noSql = NoSqlDataPersistence(**kargs)
        noSql.insert_collection_data_from_json_files()
        
        if is_financial_report(kargs['domain']):
            noSql.create_usd_financial_report_collections_version()


    def current_download_data():
        return get_lastTicker_info('fmp_fetch_tracker.txt')[0]


    def halt():
        sys.exit()


    def download_routine(data):
        print_messages("START:", data['current'])
        get_data_download(data['kwargs'])
        write_lastTicker_file('fmp_fetch_tracker.txt', data['next'], '0')
        print_messages("END:", data['current'])


    def drop_create_call_procedures():
        drop_create_procedure(stp_exec_procedures, mysql_engine)
        drop_create_procedure(stp_proc_fieldExists, mysql_engine)
        drop_create_procedure(stp_proc_fx_outer, mysql_engine)
        drop_create_procedure(stp_proc_fx_inner, mysql_engine)
        drop_create_procedure(stp_proc_fx_add_usd, mysql_engine)
        drop_create_procedure(stp_proc_fx_exRate, mysql_engine)
        drop_create_procedure(stp_proc_create_base_query_data, mysql_engine)
        drop_create_procedure(stp_proc_create_base_query_data_usd, mysql_engine)
        drop_create_procedure(stp_proc_general_date_filters, mysql_engine)
        drop_create_procedure(stp_proc_general_date_filters_selected_companies, mysql_engine)
        drop_create_procedure(stp_proc_companies_search_results, mysql_engine)
        drop_create_procedure(stp_proc_companies_search_results_usd, mysql_engine)
        drop_create_procedure(stp_proc_companies_search_selected_results_usd, mysql_engine)
        drop_create_procedure(stp_proc_companies_search_selected_results, mysql_engine)
        drop_create_procedure(stp_proc_db_general_summaries, mysql_engine)
        drop_create_procedure(stp_proc_db_revenue_summaries, mysql_engine)
        

    
    mysql_engine = engine_connetion()
    fmp_tickers.init(DIRS)
    TICKERS_FILES = fmp_tickers.get_fmp_tickers_info(DIRS)
    exec_order = fmp_exec_order.init(DIRS, TICKERS_FILES)
    
    current_download = ''

    if current_download_data() == 'finished':
        print_messages('FINISHED')
        halt()

    if File.file_is_empty('fmp_fetch_tracker.txt'):
        current_download = 'profile'
    else:
        current_download = current_download_data()

    for data in exec_order:
        print_messages(data['current'], ": expected to download ->", current_download)
        if data['current'] == current_download:
            download_routine(data)
            current_download = current_download_data()

    for data in exec_order:
        print_messages("Sql executions on:", data['current'])
        if data['kwargs']['sql'] is not None:
            create_data_persistence_sql(data['kwargs'])

    drop_create_call_procedures()


    # for data in exec_order:
    #     print_messages("NoSql executions on:", data['current'])
    #     if data['kwargs']['noSql'] is not None:
    #          create_data_persistence_noSQL(data['kwargs'])

    