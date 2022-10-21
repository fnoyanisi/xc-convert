"""
GUI Layout for xc-converter
"""
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from pathlib import PurePath

from src.exporter.xmlexporter import XmlExporter
from src.importer.xmlimporter import XmlImporter
from src.exporter.csvexporter import CsvExporter
from src.importer.csvimporter import CsvImporter
from updatemngr import UpdateManager
from dbmanager import DBManager

import utils


class XcGuiApplication:
    """ GUI layout for xc-convert application """
    version = ""
    p = "../"
    selection = ""

    def read_version(self):
        try:
            with open(self.p + "VERSION") as f:
                self.version = f.readline().strip()
        except IOError as e:
            messagebox.showerror("IO Error", "Error while opening the VERSION file")
            exit(1)
        except:
            messagebox.showerror("Opps..", "Unknown error while processing the VERSION file")
            exit(1)

    # Initialize the GUI
    def __init__(self, root):
        self.read_version()

        self.in_file = None
        self.out_dir = None
        self.conversion_type = None
        self.csv_to_xml_operation = None

        self.root = root
        root.wm_title('xcc')
        root.resizable(width=False, height=False)

        # Logo & Header
        self.logo_frame = Frame(root)
        self.logo_frame.grid(row=0, column=0, padx=4, pady=5)

        self.img_process = PhotoImage(file=self.p + 'img/process.gif')
        Label(self.logo_frame, image=self.img_process).grid(row=0, column=0, sticky='ne')
        Label(self.logo_frame, text='\nRAN helper utility (v' + self.version + ')',
              font='Helvetica 13 bold').grid(row=1, column=0, columnspan=2)
        Label(self.logo_frame, text=('\nFile conversion and RAN audit utility.\n\n'
                                     'Please see the "About" section for the license information.')
              , wraplength=200, justify=LEFT).grid(row=2, column=0, columnspan=2)

        # Creating the tab control
        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=0, column=1)

        tab1_frame = Frame(self.notebook, width=300, height=200)
        tab2_frame = Frame(self.notebook, width=300, height=200)

        self.get_file_conversion_layout(tab1_frame)
        self.get_audit_layout(tab2_frame)

        self.notebook.add(tab1_frame, text="File Conversion")
        self.notebook.add(tab2_frame, text="Parameter Audit")

        # Buttons
        self.bottom_frame = Frame(root)
        self.bottom_frame.grid(row=1, column=0, columnspan=2, padx=2, pady=2)

        Button(self.bottom_frame, text='Run', command=self.run, width=60).pack(fill=X, pady=5)
        Button(self.bottom_frame, text='Check for Updates', command=self.check_for_updates).pack(fill=X, pady=5)
        Button(self.bottom_frame, text='About', command=self.about_dialog).pack(fill=X, pady=5)
        Button(self.bottom_frame, text='Quit', command=root.destroy).pack(fill=X, pady=5)

    def get_file_conversion_layout(self, parent):
        file_conversion_frame = Frame(parent)

        Label(file_conversion_frame, text='Convert the input file from').pack()
        Radiobutton(file_conversion_frame, text='XML to CSV', variable=self.selection, value='x2c',
                    command=self.set_selection).pack()
        Radiobutton(file_conversion_frame, text='CSV to XML', variable=self.selection, value='c2x',
                    command=self.set_selection).pack()

        # Operation type
        # This is another pack() manager inside the config_frame
        conversion_type_frame = Frame(file_conversion_frame)
        conversion_type_frame.pack()
        Label(conversion_type_frame, text='Type of operation :').pack(side=LEFT)

        csv_to_xml_operation = StringVar()
        csv_to_xml_operation.set('none')
        csv_to_xml_operation_types = ('update', 'create', 'delete')

        option_menu = OptionMenu(conversion_type_frame, csv_to_xml_operation,
                                      *csv_to_xml_operation_types)
        option_menu.config(state=DISABLED)
        option_menu.pack(side=RIGHT)

        # End of Operation Type

        # Just an empty row
        Label(file_conversion_frame, text=' ').pack()

        Button(file_conversion_frame, text='Select the input file', command=self.file_chooser_dialog,
               width=25).pack()
        self.in_file_label = Label(file_conversion_frame, text='No file selected')
        self.in_file_label.pack(pady=2)

        Button(file_conversion_frame, text='Select the output directory', command=self.dir_chooser_dialog,
               width=25).pack()
        self.out_dir_label = Label(file_conversion_frame, text='No directory selected')
        self.out_dir_label.pack(pady=2)

        file_conversion_frame.pack()

    def get_audit_layout(self, parent):
        Label(parent, text="TEST").pack()

    # The selection result from opt1 and opt2 radio buttons
    # Determines the type of file conversion to be done, XML to CSV to CSV to XML
    def set_selection(self):
        self.conversion_type = self.selection

        if self.conversion_type == 'c2x':
            self.option_menu.config(state=NORMAL)
        elif self.conversion_type == 'x2c':
            self.option_menu.config(state=DISABLED)

    # File chooser for the input file
    def file_chooser_dialog(self):
        f = filedialog.askopenfilename()
        if len(f) != 0:
            self.in_file_label.config(text=utils.trim_str(PurePath(f).name, 30))
            self.in_file = f

    # Directory choose for the destination location
    def dir_chooser_dialog(self):
        d = filedialog.askdirectory()
        if len(d) != 0:
            self.out_dir_label.config(text=utils.trim_str(PurePath(d).name, 30))
            self.out_dir = d

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
            with open(self.p + 'LICENSE') as licensefile:
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
    def run(self):
        if not (self.in_file and self.out_dir and self.conversion_type) or \
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
                xml_importer = XmlImporter(self.in_file, dbm)
                csv_exporter = CsvExporter(self.out_dir, dbm)

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
                csv_importer = CsvImporter(self.in_file, dbm)
                xml_exporter = XmlExporter(self.out_dir, dbm)
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
