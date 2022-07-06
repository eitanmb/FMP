import sys
sys.path.append("..")

from sql.basics import execute_query, creat_dataframe_from_data
from helpers.utilities import print_messages


class SqlDataPersistence():

    def __init__(self, engine, **kwargs):
        self.engine = engine
        self.table = kwargs['sql']['table']
        self.drop_table_query = kwargs['sql']['drop_table']
        self.create_table_query = kwargs['sql']['create_table']
        self.add_indexes_query = kwargs['sql']['add_indexes']
        self.alter_table_query = kwargs['sql']['alter_table']
        self.folder = kwargs['folder']

    def drop_table(self):
        result = execute_query(self.drop_table_query, self.engine)
        print_messages("Drop table:", result)

    def create_table(self):
        result = execute_query(self.create_table_query, self.engine)
        print_messages("Create table:", result)

    def add_indexes(self):
        result = execute_query(self.add_indexes_query, self.engine)
        print_messages("Add indexes:", result)

    def alter_table(self):
        result = execute_query(self.alter_table_query, self.engine)
        print_messages("Alter table:", result)

    def insert_data_from_dataframe(self):
        creat_dataframe_from_data(self.folder, self.engine, self.table)


def drop_create_procedure(stp, engine):
    print_messages(f"Drop {stp['name']} Procedure",
                   execute_query(stp['drop'], engine))
    print_messages(f"Create {stp['name']} Procedure",
                   execute_query(stp['create'], engine))
