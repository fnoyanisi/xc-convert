"""
GUI Layout for xc-converter
"""
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from pathlib import PurePath

from xmlconverter import XmlConverter
from csvconverter import CsvConverter

class XcGuiApplication:
    """ GUI layout for xc-convert application """

    # Initialize the GUI
    def __init__(self, top):
        self.version = 'v0.5.1'
        self.in_file = None
        self.out_dir = None
        self.conversion_type = None
        self.csv_to_xml_operation= None

        self.top = top
        top.wm_title('xc-converter ' + self.version)
        top.resizable(width=False, height=False)
        # top.geometry('{}x{}'.format(400, 280))

        # Logo & Header
        self.logo_frame = Frame(top)
        self.logo_frame.grid(row=0, column=0, padx=4, pady=5)

        self.img_xml = PhotoImage(file='./img/img_xml.gif')
        self.img_csv = PhotoImage(file='./img/img_csv.gif')
        Label(self.logo_frame, image=self.img_xml).grid(row=0, column=0, sticky='ne')
        Label(self.logo_frame, image=self.img_csv).grid(row=0, column=1, sticky='nw')
        Label(self.logo_frame, text='Xml to Csv Converter ' + self.version, font=('bold')).grid(row=1, column=0,
                                                                                                columnspan=2)
        Label(self.logo_frame, text=('Simple file format conversion utility for Nokia OSS configration files.\n\n'
                                     'Please see the "About" section for the license information.')
              , wraplength=200, justify=LEFT).grid(row=2, column=0, columnspan=2)

        # Conversion type, input file, output folder selection
        self.config_frame = Frame(top)
        self.config_frame.grid(row=0, column=1, padx=4, pady=5)

        self.selection = StringVar()
        Label(self.config_frame, text='Convert the input file from').pack()
        Radiobutton(self.config_frame, text='XML to CSV', variable=self.selection, value='x2c',
                    command=self.SetSelection).pack()
        Radiobutton(self.config_frame, text='CSV to XML', variable=self.selection, value='c2x',
                    command=self.SetSelection).pack()

		# Operation type
		# This is another pack() manager inside the config_frame
        self.conversion_type_frame = Frame(self.config_frame)
        self.conversion_type_frame.pack()
        Label(self.conversion_type_frame, text='Type of operation :').pack(side=LEFT)

        self.csv_to_xml_operation = StringVar()
        self.csv_to_xml_operation.set('none')
        csv_to_xml_operation_types = ('update','create','delete')

        self.option_menu = OptionMenu(self.conversion_type_frame, self.csv_to_xml_operation, *csv_to_xml_operation_types)
        self.option_menu.config(state = DISABLED)
        self.option_menu.pack(side = RIGHT)

        # End of Operation Type

        # Just an empty row
        Label(self.config_frame, text=' ').pack()

        Button(self.config_frame, text='Select the input file', command=self.FileChooserDialog, width=25).pack()
        self.in_file_label = Label(self.config_frame, text='No file selected')
        self.in_file_label.pack(pady=2)

        Button(self.config_frame, text='Select the output directory', command=self.DirChooserDialog, width=25).pack()
        self.out_dir_label = Label(self.config_frame, text='No directory selected')
        self.out_dir_label.pack(pady=2)

        # Buttons
        self.bottom_frame = Frame(top)
        self.bottom_frame.grid(row=1, column=0, columnspan=2, padx=2, pady=2)

        Button(self.bottom_frame, text='Run', command=self.Run, width=60).pack(fill=X, pady=5)
        Button(self.bottom_frame, text='About', command=self.AboutDialog).pack(fill=X, pady=5)
        Button(self.bottom_frame, text='Quit', command=top.destroy).pack(fill=X, pady=5)

    # The selection result from opt1 and opt2 radio buttons
    # Determines the type of file conversion to be done, XML to CSV to CSV to XML
    def SetSelection(self):
        self.conversion_type = self.selection.get()

        if self.conversion_type == 'c2x':
            self.option_menu.config(state = NORMAL)
        elif self.conversion_type == 'x2c':
            self.option_menu.config(state = DISABLED)

    # File chooser for the input file
    def FileChooserDialog(self):
        f = filedialog.askopenfilename()
        if len(f) != 0:
            self.in_file_label.config(text=PurePath(f).name)
            self.in_file = f

    # Directory choose for the destination location
    def DirChooserDialog(self):
        d = filedialog.askdirectory()
        if len(d) != 0:
            self.out_dir_label.config(text=PurePath(d).name)
            self.out_dir = d

    # Displays the license information
    def AboutDialog(self):
        about_dialog = Toplevel(self.top)
        about_dialog.wm_title('About xc-converter ' + self.version)
        about_dialog.resizable(width=False, height=False)

        about_label_text = 'Use of this software is subject to license conditions given below.'
        about_label = Label(about_dialog, text=about_label_text)
        about_label.grid(row=0, column=0, columnspan=2, sticky=W + E + N + S, padx=10, pady=10)

        try:
            with open('../LICENSE') as licensefile:
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
    def Run(self):
        if not (self.in_file and self.out_dir and self.conversion_type) or \
        (self.conversion_type == 'c2x' and self.csv_to_xml_operation.get() == 'none'):
            msg = 'Please make sure you have\n' \
                  '  * Selected the type of operation\n' \
                  '  * Located the input file\n' \
                  '  * Specified an output directory\n'
            messagebox.showwarning("Missing Information", msg)
            return

        # we got two types of operations; either x2c or c2x for XML to CSV and CSV to XML, respectively
        if self.conversion_type == 'x2c':
            # XML to CSV Conversion
            try:
                xml_converter = XmlConverter(self.in_file)
                xml_converter.convert(self.out_dir)
            except RuntimeError as err:
                print(err)
                messagebox.showerror(title="Error", message=err)
                return

        elif self.conversion_type == 'c2x':
            # CSV to XML Conversion
            try:
                csv_converter = CsvConverter(self.in_file)
                csv_converter.set_operation(self.csv_to_xml_operation.get())
                csv_converter.convert(self.out_dir)
            except RuntimeError as err:
                print(err)
                messagebox.showerror(title="Error", message=err)
                return
        else:
            # never reached
            return

        messagebox.showinfo("Done", "File conversion has been completed!")