"""
A class to manage the database operations
"""
import sqlite3


class DBManager():
    cursor = None
    conn = None

    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        # DBManager always returns rows in the form of a dict
        # with header:value format
        self.conn.row_factory = self.__dict_factory
        self.cursor = self.conn.cursor()

    # table_name - name of the table
    # cols - a list containing the column names
    def create_table(self, table_name, column_names):
        # replace {} with "_CompactItem" in the column names
        refined_column_names = [sub.replace("{}", "_CompactItem") for sub in column_names]
        sql = 'CREATE TABLE ' + table_name + ' (' + ', '.join(refined_column_names) + ')'
        self.cursor.execute(sql)
        self.conn.commit()

    # table_name - name of the table that the data will be inserted into
    # map - a sequence of dictionaries containing header:value pairs
    def insert_values(self, table_name, map):
        self.cursor.execute("begin transaction")
        for entry in map:
            # update the dict keys in case "{}" is included
            updated_keys = {k.replace("{}", "_CompactItem"): v for k, v in entry.items()}
            columns = ', '.join(updated_keys)
            values = ', '.join(f"'{w}'" for w in entry.values())
            sql = 'INSERT INTO ' + table_name + ' ({}) VALUES ({})'.format(columns, values)
            self.cursor.execute(sql)
        self.conn.commit()

    # table_name - name of the table
    # returns a generator which yields one row from them target DB table
    # in each iteration
    def get_rows(self, table_name):
        for row in self.conn.execute("select * from " + table_name):
            yield row

    def __dict_factory(self, cursor, row):
        col_names = [col[0] for col in cursor.description]
        return {key: value for key, value in zip(col_names, row)}
