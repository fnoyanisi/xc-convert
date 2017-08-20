"""
GUI Layout for xc-converter

    +-----------------------+-----------------------+
    |       label           |         button        |
    +-----------------------+-----------------------+
    |       label           |         label         |
    +-----------------------+-----------------------+
    |    radio_button       |         button        |
    +-----------------------+-----------------------+
    |    radio_button       |         label         |
    +-----------------------+-----------------------+
    |                    button                     |
    +-----------------------------------------------+
    |                    button                     |
    +-----------------------------------------------+
    |                    button                     |
    +-----------------------------------------------+
"""
from tkinter import *
from tkinter import filedialog, messagebox
from pathlib import PurePath
from XcFunctions import *
import datetime

class XcGuiApplication:
    """ GUI layout for xc-convert application """

    # Initialize the GUI
    def __init__(self, top):
        self.version = 'v0.2'
        self.in_file = None
        self.out_dir = None
        self.operation = None

        self.top = top
        top.wm_title('xc-converter ' + self.version)
        top.resizable(width=False, height=False)
        top.geometry('{}x{}'.format(400, 280))

        label1 = Label(top, text='Xml to Csv Converter ' + self.version, font="bold")
        label1.grid(row=0, column=0, sticky=W + E + N + S, padx=5, pady=10)

        label2_text = 'Please select\n' \
                      '    * The type of operation\n' \
                      '    * The input file\n' \
                      '    * The output directory '
        label2 = Label(top, text=label2_text, justify=LEFT)
        label2.grid(row=1, column=0, sticky=W)

        # Operation Selections
        self.selection = StringVar()
        opt1 = Radiobutton(top, text='XML to CSV Conversion', variable=self.selection, value='x2c', command=self.SetSelection)
        opt1.grid(row=2, column=0)

        opt2 = Radiobutton(top, text='CSV to XML Conversion', variable=self.selection, value='c2x', command=self.SetSelection)
        opt2.grid(row=3, column=0)

        button_run = Button(top, text='Run', command=self.Run)
        button_run.grid(row=4, column=0, columnspan=2, sticky=W + E + N + S, padx=5, pady=5)

        button_about = Button(top, text='About', command=self.AboutDialog)
        button_about.grid(row=5, column=0, columnspan=2, sticky=W + E + N + S, padx=5, pady=5)

        button_quit = Button(top, text='Quit', command=top.destroy)
        button_quit.grid(row=6, column=0, columnspan=2, sticky=W + E + N + S, padx=5, pady=5)

        button_fc = Button(top, text='Select input file', command=self.FileChooserDialog)
        button_fc.grid(row=0, column=1, sticky=W + E, padx=5, pady=5)

        label3_text = 'No file selected'
        self.label3 = Label(top, text=label3_text)
        self.label3.grid(row=1, column=1)

        button_dc = Button(top, text='Select output directory', command=self.DirChooserDialog)
        button_dc.grid(row=2, column=1, sticky=W + E + N + S, padx=5, pady=5)

        label4_text = 'No directory selected'
        self.label4 = Label(top, text=label4_text)
        self.label4.grid(row=3, column=1)

    # The selection result from opt1 and opt2 radio buttons
    # Determines the type of file coversion to be done, XML to CSV ot CSV to XML
    def SetSelection(self):
        self.operation = self.selection.get()

    # File chooser for the input file
    def FileChooserDialog(self):
        f = filedialog.askopenfilename()
        if len(f) != 0:
            self.label3.config(text=PurePath(f).name)
            self.in_file = f

    # Directory choose for the destination location
    def DirChooserDialog(self):
        d = filedialog.askdirectory()
        if len(d) != 0:
            self.label4.config(text=PurePath(d).name)
            self.out_dir = d

    # Displays the license information
    def AboutDialog(self):
        about_dialog = Toplevel(self.top)
        about_dialog.wm_title('About xc-converter ' + self.version)
        about_dialog.resizable(width=False, height=False)
        about_dialog.geometry('{}x{}'.format(550, 500))

        about_label_text = 'Use of this software is subject to license conditions given below.'
        about_label = Label(about_dialog, text=about_label_text)
        about_label.grid(row=0, sticky=W + E + N + S, padx=10, pady=10)

        try:
            with open('LICENSE') as licensefile:
                license_text = licensefile.read()
                dialog_text = Text(about_dialog)
                dialog_text.insert(INSERT, license_text)
                dialog_text.config(state = DISABLED)
                dialog_text.grid(row=1, sticky=W + E + N + S, padx=0, pady=0)

        except OSError:
            error_text = 'Opps...Cannot find the LICENSE file.\n\nPlease get the LICENSE file from https://github.com/fnoyanisi/xc-convert'
            error_label = Label(about_dialog, text=error_text)
            error_label.grid(row=1, sticky=W + E + N + S, padx=10, pady=10)

        download_url = 'You can obtain the source code from https://github.com/fnoyanisi/xc-convert'
        url_label = Label(about_dialog, text=download_url, justify=LEFT)
        url_label.grid(row=2, sticky=W + E + N + S, padx=10, pady=10)

        exit_button = Button(about_dialog, text = 'Close', command=about_dialog.destroy)
        exit_button.grid(row=3, sticky=N + S, padx=0, pady=10)

    # Performs the file conversion operation
    def Run(self):
        if not (self.in_file and self.out_dir and self.operation):
            msg = 'Please make sure you have\n' \
                   '  * Selected the type of operation\n' \
                   '  * Located the input file\n'\
                   '  * Chosen the output directory\n'
            messagebox.showwarning("Missing Information",msg)
            return

        # we got two types of operations; either x2c or c2x for XML to CSV and CSV to XML, respectively
        if self.operation == 'x2c':
        # XML to CSV Conversion

            # Use DOM
            doc = minidom.parse(self.in_file)

            # Check XML file format
            if not examineXmlFormat(doc):
                messagebox.showerror('Unsupported XML file format!')
                return

            # Create a header dictionary
            header_dictionary = createManagedObjectDict(doc)
            if len(header_dictionary) == 0:
                messagebox.showerror('Error while processing the XML file!')
                return

            # Convert the file
            try:
                convertXmlToCsv(doc, self.out_dir, header_dictionary)
            except OSError:
                messagebox.showerror('IO Error : Cannot convert the XML file!')
                return

        elif self.operation == 'c2x':
            # CSV to XML Conversion

            # Check CSV file format
            if not examineCsvFormat(self.in_file):
                messagebox.showerror('Unsupported CSV file format!')
                return

            # Convert the file
            now = datetime.datetime.now()
            timestamp = now.strftime('%Y-%m-%d-T%H-%M-%S')
            out_file_name = PurePath(self.in_file).name + timestamp + '.xml'
            try:
                convertCsv2Xml(self.in_file, PurePath(self.out_dir, out_file_name))
            except OSError:
                messagebox.showerror('IO Error : Cannot convert the CSV file!')
                return
        else:
            # never reached
            return

        messagebox.showinfo("Done","File conversion has been completed!")