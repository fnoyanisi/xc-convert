from fileexporter import FileExporter
from pathlib import PurePath

import csv
import datetime
import utils


# o - path to the output directory
# d - valid DBManager instance
class CsvExporter(FileExporter):
    def __init__(self, o, d):
        super().__init__(o, d)

        self.out_dir = o
        self.dbm = d

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
                writer.writerow(row)

    def write_all(self):
        for table_name in self.dbm.get_table_names():
            self.write(table_name)