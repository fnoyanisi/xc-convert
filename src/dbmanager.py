"""
A class to manage the database operations
"""
import sqlite3


class DBManager():
    cursor = None
    conn = None

    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()

    # table_name - name of the table
    # cols - a list containing the column names
    def create_table(self, table_name, column_names):
        sql = 'CREATE TABLE ' + table_name + ' (' + ', '.join(column_names) + ')'
        self.cursor.execute(sql)
        self.conn.commit()

    # table_name - name of the table that the data will be inserted into
    # map - a dictionary containing header:value pairs
    def insert_values(self, table_name, map):
        self.cursor.execute("begin transaction")
        for entry in map:
            columns = ', '.join(entry.keys())
            values = ', '.join(f"'{w}'" for w in entry.values())
            sql = 'INSERT INTO ' + table_name + ' ({}) VALUES ({})'.format(columns, values)
            self.cursor.execute(sql)
        self.conn.commit()
