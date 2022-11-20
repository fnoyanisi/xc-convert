"""
Manages the database operations

Copyright (c) 2017-2022 Fehmi Noyan ISI. All rights reserved.
See the LICENSE file for the end user license agreement.
"""
import sqlite3

# This class prepends the "table_name" parameter passed to any of
# its methods with "t_" to guarantee SQLite table naming convention
# which prevents table name starting with numeric characters
class DBManager:
    cursor = None
    conn = None

    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        # DBManager always returns rows in the form of a dict
        # with header:value format
        self.conn.row_factory = self.__dict_factory
        self.cursor = self.conn.cursor()

    # runs a given SQL query
    def query(self, sql):
        self.cursor.execute("begin transaction")
        self.cursor.execute(sql)
        self.conn.commit()

    # table_name - name of the table
    # cols - a list containing the column names
    def create_table(self, table_name, column_names):
        table_name = "t_" + table_name
        sql = 'DROP TABLE IF EXISTS ' + table_name
        self.cursor.execute(sql)
        self.conn.commit()
        # wrap the column names within quotes to escape special chars
        updated_column_names = ["'" + w + "'" for w in column_names]
        sql = 'CREATE TABLE ' + table_name + ' (' + ', '.join(updated_column_names) + ')'
        self.cursor.execute(sql)
        self.conn.commit()

    # table_name - name of the table that the data will be inserted into
    # map - a list of dictionaries containing header:value pairs
    # unlike the insert_values_transpose() method, this method uses a dictionary for
    # each SQL INSERT operation and column names are explicity passed to the database.
    def insert_values(self, table_name, map):
        table_name = "t_" + table_name
        self.cursor.execute("begin transaction")
        for entry in map:
            # wrap the column names within quotes to escape special chars
            columns = ', '.join(f"'{w}'" for w in entry.keys())
            values = ', '.join(f"'{w}'" for w in entry.values())
            sql = 'INSERT INTO ' + table_name + ' ({}) VALUES ({})'.format(columns, values)
            self.cursor.execute(sql)
        self.conn.commit()

    # table_name - name of the table that the data will be inserted into
    # tuples - list of tuples containing the values to be inserted into the table. Unlike to
    # insert_values() method, this method requires the items in the tuple to be in the right
    # order (i.e. follow the column arrangement of the table)
    def insert_values_transpose(self, table_name, tuples):
        table_name = "t_" + table_name
        self.cursor.execute("begin transaction")
        for tp in tuples:
            values = ', '.join(f"'{w}'" for w in tp)
            sql = 'INSERT INTO ' + table_name + ' VALUES ({})'.format(values)
            self.cursor.execute(sql)
        self.conn.commit()

    # table_name - name of the table
    # returns a generator which yields one row from them target DB table
    # in each iteration
    def get_rows(self, table_name):
        table_name = "t_" + table_name
        for row in self.conn.execute("select * from " + table_name):
            yield row

    # returns a list of columns names for the table_name
    def get_column_names(self, table_name):
        res = []
        sql = "PRAGMA table_info('" + table_name + "')"
        for c in self.cursor.execute(sql).fetchall():
            res.append(c['name'])
        return res

    def get_table_names(self):
        res = []
        sql = "SELECT name FROM sqlite_master WHERE type='table'"
        for t in self.cursor.execute(sql).fetchall():
            tn = t['name'][2:]
            res.append(tn)
        return res

    def __dict_factory(self, cursor, row):
        col_names = [col[0] for col in cursor.description]
        return {key: value for key, value in zip(col_names, row)}
