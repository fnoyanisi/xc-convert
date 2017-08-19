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
from tkinter import filedialog
from tkinter import messagebox
from pathlib import PurePath

class XcGuiApplication:
    """ GUI layout for xc-convert application """
    def __init__(self, top):
        self.version = 'v0.1'
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

    def SetSelection(self):
        self.operation = self.selection.get()

    def FileChooserDialog(self):
        f = filedialog.askopenfilename()
        if len(f) != 0:
            self.label3.config(text=PurePath(f).name)
            self.in_file = f

    def DirChooserDialog(self):
        d = filedialog.askdirectory()
        if len(d) != 0:
            self.label4.config(text=PurePath(d).name)
            self.out_dir = d

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

    def Run(self):
        pass


root = Tk()
xc_gui = XcGuiApplication(root)
root.mainloop()