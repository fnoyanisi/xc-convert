"""
GUI Layout for xc-converter

Copyright (c) 2017-2022 Fehmi Noyan ISI. All rights reserved.
See the LICENSE file for the end user license agreement.
"""

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from pathlib import PurePath
from functools import partial

from src.exporter.xmlexporter import XmlExporter
from src.exporter.csvexporter import CsvExporter
from src.importer.xmlimporter import XmlImporter
from src.importer.csvimporter import CsvImporter
from src.updatemngr import UpdateManager
from src.dbmanager import DBManager

import src.utils as utils


class XcGuiApplication:
    """ GUI layout for xc-convert application """
    version = ""
    p = "../"

    def read_version(self):
        try:
            with open(self.p + "etc/VERSION") as f:
                self.version = f.readline().strip()
        except IOError as e:
            messagebox.showerror("IO Error", "Error while opening the VERSION file")
            exit(1)
        except:
            messagebox.showerror("Opps..", "Unknown error while processing the VERSION file")
            exit(1)

    # Initialize the GUI
    def __init__(self, root):
        self.conversion_out_dir_label = None
        self.conversion_out_dir = None

        self.conversion_in_file_label = None
        self.conversion_in_file = None

        self.audit_ref_file_label = None
        self.audit_ref_file = None

        self.audit_target_file_label = None
        self.audit_target_file = None

        self.audit_out_dir_label = None
        self.audit_out_dir = None

        self.option_menu = None
        self.read_version()

        self.conversion_type = None
        self.csv_to_xml_operation = None

        self.selection = StringVar()

        self.tab_width = 300
        self.tab_height = 220

        self.root = root
        root.wm_title('xcc')
        root.resizable(width=False, height=False)

        # Logo & Header
        self.left_frame = Frame(root)
        self.left_frame.grid(row=0, column=0)

        self.img_process = PhotoImage(file=self.p + 'img/process.gif')
        Label(self.left_frame, image=self.img_process).pack(padx=(10,5))
        Label(self.left_frame, text='\nRAN helper utility (v' + self.version + ')',
              font='Helvetica 13 bold').pack(padx=(10,5))
        Label(self.left_frame, text=('\nFile conversion and RAN audit utility.\n\n'
                                     'Please see the "About" section for the license information.')
              , wraplength=200, justify=LEFT).pack(padx=(10,5))

        # Buttons
        self.get_button_frame(self.left_frame, root).pack(fill=X)

        # RIGHT FRAME
        self.right_frame = Frame(root)
        self.right_frame.grid(row=0, column=1)

        self.notebook = ttk.Notebook(self.right_frame)
        self.notebook.pack()

        tab1_frame = Frame(self.notebook, width=self.tab_width, height=self.tab_height)
        tab2_frame = Frame(self.notebook, width=self.tab_width, height=self.tab_height)

        self.get_file_conversion_layout(tab1_frame)
        self.get_audit_layout(tab2_frame)

        self.notebook.add(tab1_frame, text="File Conversion")
        self.notebook.add(tab2_frame, text="Parameter Audit")

    def get_button_frame(self, parent, r):
        button_frame = Frame(parent)

        Button(button_frame, text='Check for Updates', command=self.check_for_updates).pack(fill=X, pady=5)
        Button(button_frame, text='About', command=self.about_dialog).pack(fill=X, pady=5)
        Button(button_frame, text='Quit', command=r.destroy).pack(fill=X, pady=5)

        return button_frame

    def get_file_conversion_layout(self, parent):
        file_conversion_frame = Frame(parent)

        Label(file_conversion_frame, text='Convert the input file from').pack(pady=(2, 15))
        Radiobutton(file_conversion_frame, text='XML to CSV', variable=self.selection, value='x2c',
                    command=self.set_selection).pack()
        Radiobutton(file_conversion_frame, text='CSV to XML', variable=self.selection, value='c2x',
                    command=self.set_selection).pack()

        # Operation type
        # This is another pack() manager inside the config_frame
        conversion_type_frame = Frame(file_conversion_frame)
        conversion_type_frame.pack()
        Label(conversion_type_frame, text='Type of operation :').pack(side=LEFT)

        self.csv_to_xml_operation = StringVar(parent)
        self.csv_to_xml_operation.set('none')
        csv_to_xml_operation_types = ['update', 'create', 'delete']

        self.option_menu = OptionMenu(conversion_type_frame, self.csv_to_xml_operation,
                                      *csv_to_xml_operation_types)
        self.option_menu.config(state=DISABLED)
        self.option_menu.pack(side=RIGHT)

        # End of Operation Type

        # Just an empty row
        Label(file_conversion_frame, text=' ').pack()

        file_chooser_function = partial(self.file_chooser_dialog, 1)
        Button(file_conversion_frame, text='Select the input file', command=file_chooser_function,
               width=25).pack()
        self.conversion_in_file_label = Label(file_conversion_frame, text='No file selected')
        self.conversion_in_file_label.pack(pady=(2, 15))

        dir_chooser_function = partial(self.dir_chooser_dialog, 1)
        Button(file_conversion_frame, text='Select the output directory', command=dir_chooser_function,
               width=25).pack()
        self.conversion_out_dir_label = Label(file_conversion_frame, text='No directory selected')
        self.conversion_out_dir_label.pack(pady=(2, 15))

        Button(file_conversion_frame, text='Run', command=self.run_conversion).pack(fill=X, pady=(20, 2))

        file_conversion_frame.pack()

    def get_audit_layout(self, parent):
        audit_frame = Frame(parent)

        Label(audit_frame, text='Audits the parameters in the target file against the ones in the reference.',
              wraplength=self.tab_width - 20, justify="center").pack(pady=(2, 15))

        ref_file_chooser_function = partial(self.file_chooser_dialog, 2)
        Button(audit_frame, text='Select the reference file', command=ref_file_chooser_function,
               width=25).pack()
        self.audit_ref_file_label = Label(audit_frame, text='No file selected')
        self.audit_ref_file_label.pack(pady=(2, 15))

        target_file_chooser_function = partial(self.file_chooser_dialog, 3)
        Button(audit_frame, text='Select the target file', command=target_file_chooser_function,
               width=25).pack()
        self.audit_target_file_label = Label(audit_frame, text='No file selected')
        self.audit_target_file_label.pack(pady=(2, 15))

        dir_chooser_function = partial(self.dir_chooser_dialog, 2)
        Button(audit_frame, text='Select the output directory', command=dir_chooser_function,
               width=25).pack()
        self.audit_out_dir_label = Label(audit_frame, text='No directory selected')
        self.audit_out_dir_label.pack(pady=(2, 15))

        Button(audit_frame, text='Run', command=self.run_audit).pack(fill=X, pady=(20, 2))

        audit_frame.pack()

    # The selection result from opt1 and opt2 radio buttons
    # Determines the type of file conversion to be done, XML to CSV or CSV to XML
    def set_selection(self):
        self.conversion_type = self.selection.get()

        if self.conversion_type == 'c2x':
            self.option_menu.config(state=NORMAL)
        elif self.conversion_type == 'x2c':
            self.option_menu.config(state=DISABLED)

    # File chooser for the input file
    def file_chooser_dialog(self, c):
        f = filedialog.askopenfilename()
        if len(f) != 0:
            t = utils.trim_str(PurePath(f).name, 30)

            if c == 1:
                self.conversion_in_file_label.config(text=t)
                self.conversion_in_file = f
            elif c == 2:
                self.audit_ref_file_label.config(text=t)
                self.audit_ref_file = f
            else:
                self.audit_target_file_label.config(text=t)
                self.audit_target_file = f

    # Directory choose for the destination location
    def dir_chooser_dialog(self, c):
        d = filedialog.askdirectory()
        if len(d) != 0:
            t = utils.trim_str(PurePath(d).name, 30)

            if c == 1:
                self.conversion_out_dir_label.config(text=t)
                self.conversion_out_dir = d
            elif c == 2:
                self.audit_out_dir_label.config(text=t)
                self.audit_out_dir = d

    def check_for_updates(self):
        # check for updates
        um = UpdateManager()
        um.check_for_updates(self.version, False)

    # Displays the license information
    def about_dialog(self):
        about_dialog = Toplevel(self.root)
        about_dialog.wm_title('About xc-converter ' + self.version)
        about_dialog.resizable(width=False, height=False)

        about_label_text = 'Use of this software is subject to license conditions given below.'
        about_label = Label(about_dialog, text=about_label_text)
        about_label.grid(row=0, column=0, columnspan=2, sticky=W + E + N + S, padx=10, pady=10)

        try:
            with open(self.p + 'etc/LICENSE') as licensefile:
                license_text = licensefile.read()
                dialog_text = Text(about_dialog, borderwidth=3, relief="sunken")
                dialog_text.insert(INSERT, license_text)
                dialog_text.config(state=DISABLED)
                dialog_text.grid(row=1, column=0, sticky=W + E + N + S, padx=2, pady=0)

                scrollbar = Scrollbar(about_dialog, command=dialog_text.yview)
                scrollbar.grid(row=1, column=1, sticky='nsew')
                dialog_text['yscrollcommand'] = scrollbar.set

        except OSError:
            error_text = ('Opps...Cannot find the LICENSE file.\n\n'
                          'Please get the LICENSE file from https://github.com/fnoyanisi/xc-convert')
            Label(about_dialog, text=error_text).grid(row=1, sticky=W + E + N + S, padx=10, pady=10)

        download_url = 'You can obtain the source code from https://github.com/fnoyanisi/xc-convert'
        Label(about_dialog, text=download_url, justify=LEFT).grid(row=2, column=0, columnspan=2, sticky=W + E + N + S,
                                                                  padx=10, pady=10)

        Button(about_dialog, text='Close', command=about_dialog.destroy, width=25).grid(row=3, column=0, columnspan=2,
                                                                                        sticky=N + S, padx=0, pady=10)

    # Performs the file conversion operation
    def run_conversion(self):
        if not (self.conversion_in_file and self.conversion_out_dir and self.conversion_type) or \
                (self.conversion_type == 'c2x' and self.csv_to_xml_operation.get() == 'none'):
            msg = 'Please make sure you have\n' \
                  '  * Selected the type of the operation\n' \
                  '  * Located the input file\n' \
                  '  * Specified an output directory\n'
            messagebox.showwarning("Missing Information", msg)
            return

        dbm = DBManager()

        # we got two types of operations; either x2c or c2x for XML to CSV and CSV to XML, respectively
        if self.conversion_type == 'x2c':
            # XML to CSV Conversion
            # XML importer -> DB -> CSV exporter
            try:
                xml_importer = XmlImporter(self.conversion_in_file, dbm)
                csv_exporter = CsvExporter(self.conversion_out_dir, dbm)

                xml_importer.read()
                csv_exporter.write_all()
            except RuntimeError as err:
                print(err)
                messagebox.showerror(title="Error", message=str(err))
                return
        elif self.conversion_type == 'c2x':
            # CSV to XML Conversion
            # CSV importer -> DB -> XML exporter
            try:
                csv_importer = CsvImporter(self.conversion_in_file, dbm)
                xml_exporter = XmlExporter(self.conversion_out_dir, dbm)
                xml_exporter.set_operation(self.csv_to_xml_operation.get())

                table_name = csv_importer.read()
                xml_exporter.write(table_name)
            except RuntimeError as err:
                print(err)
                messagebox.showerror(title="Error", message=str(err))
                return
        else:
            # never reached
            return

        messagebox.showinfo("Done", "File conversion has been completed!")

    # performs the parameter audit operation
    def run_audit(self):
        if not (self.audit_ref_file and self.audit_target_file and self.audit_out_dir):
            msg = 'Please make sure you have\n' \
                  '  * Located the reference file\n' \
                  '  * Located the target file\n' \
                  '  * Specified an output directory\n'
            messagebox.showwarning("Missing Information", msg)
            return

        dbm = DBManager()
        dbm.create_table("reference", ['CLASS', 'DISTNAME', 'PARAMETER', 'VALUE'])
        dbm.create_table("target", ['CLASS', 'DISTNAME', 'PARAMETER', 'VALUE'])
        dbm.create_table("audit_result", ['CLASS', 'REFERENCE_DISTNAME', 'TARGET_DISTNAME', 'PARAMETER',
                                    'REFERENCE_VALUE', 'TARGET_VALUE'])

        try:
            ref_file_importer = XmlImporter(self.audit_ref_file, dbm)
            target_file_importer = XmlImporter(self.audit_target_file, dbm)
            csv_exporter = CsvExporter(self.audit_out_dir, dbm)

            ref_file_importer.read_into(table_name="reference", unique=True, transpose=True)
            target_file_importer.read_into(table_name="target", unique=False, transpose=True)

            sql = """
            insert into audit_result
            select 
                target.CLASS as 'CLASS', 
                reference.DISTNAME as 'REFERENCE_DISTNAME', 
                target.DISTNAME as 'TARGET_DISTNAME', 
                target.PARAMETER as 'PARAMETER', 
                reference.VALUE as 'REFERENCE_VALUE', 
                target.VALUE as 'TARGET_VALUE'
            from target 
                join reference on target.CLASS = reference.CLASS 
                and target.PARAMETER = reference.PARAMETER 
                and target.VALUE != reference.VALUE;
            """

            dbm.query(sql)

            csv_exporter.write("audit_result")
        except RuntimeError as err:
            print(err)
            messagebox.showerror(title="Error", message=str(err))
            return

        messagebox.showinfo("Done", "Parameter audit has been completed!")
