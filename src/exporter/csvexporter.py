"""
Gets data from the DB and writes into a CSV file

Copyright (c) 2017-2022 Fehmi Noyan ISI. All rights reserved.
See the LICENSE file for the end user license agreement.
"""
from src.exporter.fileexporter import FileExporter
from pathlib import PurePath

import csv
import datetime


# o - path to the output directory
# d - valid DBManager instance
class CsvExporter(FileExporter):
    def __init__(self, o, d):
        super().__init__(o, d)

        self.out_dir = o
        self.dbm = d

    # writes the data in table_name into the output file
    def write(self, table_name):
        now = datetime.datetime.now()
        timestamp = now.strftime('%Y-%m-%dT%H-%M-%S')
        out_file_name = table_name + "-" + str(timestamp) + '.csv'
        path_to_csv_file = PurePath(self.out_dir, out_file_name)

        with open(path_to_csv_file, 'w', newline='') as csv_file:
            csv_header = self.dbm.get_column_names(table_name)

            writer = csv.DictWriter(csv_file, fieldnames=csv_header, restval=self.missing_val_str)

            writer.writeheader()

            for row in self.dbm.get_rows(table_name):
                updated_row = {k: self.missing_val_str if not v else v for (k, v) in row.items()}
                writer.writerow(updated_row)

    # writes all the data in the database to the output file
    def write_all(self):
        for table_name in self.dbm.get_table_names():
            self.write(table_name)
