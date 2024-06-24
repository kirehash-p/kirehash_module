import sqlite3

from module.sql.sql_template import SQLTemplate

class Sqlite(SQLTemplate):
    def __init__(self, db_config):
        self.conn = sqlite3.connect(db_config['db_path'])
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def execute(self, query, params=None, commit=True):
        if params is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        if commit:
            self.conn.commit()
            return self.cursor.fetchall()

    def create_table(self, table_name, columns):
        query = self.create_table_query(table_name, columns)
        self.execute(query)

    def insert(self, table_name, columns, values, commit=True):
        query = self.insert_query(table_name, columns)
        self.execute(query, values)
        if commit:
            self.conn.commit()