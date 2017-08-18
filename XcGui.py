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
"""
from tkinter import *

class XcGuiApplication():
    def __init__(self, top):
        version = 'v0.1'
        self.top = top
        top.wm_title('xc-converter ' + version)
        top.resizable(width=False, height=False)
        top.geometry('{}x{}'.format(400, 200))

        label1 = Label(top, text='Xml to Csv Converter ' + version, font="bold")
        label1.grid(row=0, column=0, sticky=W + E + N + S, padx=5, pady=10)

        label2_text = 'Please select\n' \
                      '    * The type of operation\n' \
                      '    * The input file\n' \
                      '    * The output directory '
        label2 = Label(top, text=label2_text, justify=LEFT)
        label2.grid(row=1, column=0, sticky=W)

        # Operation Selections
        self.selection = StringVar()
        opt1 = Radiobutton(top, text='XML to CSV Conversion', variable=self.selection, value='x2c', command=self.OptSelection)
        opt1.grid(row=2, column=0)

        opt2 = Radiobutton(top, text='CSV to XML Conversion', variable=self.selection, value='c2x', command=self.OptSelection)
        opt2.grid(row=3, column=0)

        button_run = Button(top, text='    Run    ', command=self.FileChooser)
        button_run.grid(row=4, column=0, columnspan=2, sticky=W + E + N + S, padx=5, pady=5)

        button_fc = Button(top, text='Select input file', command=self.FileChooser)
        button_fc.grid(row=0, column=1, sticky=W + E, padx=5, pady=5)

        label3_text = 'No file selected'
        self.label3 = Label(top, text=label3_text)
        self.label3.grid(row=1, column=1)

        button_dc = Button(top, text='Select output directory', command=self.DirChooser)
        button_dc.grid(row=2, column=1, sticky=W + E + N + S, padx=5, pady=5)

        label4_text = 'No directory selected'
        label4 = Label(top, text=label4_text)
        label4.grid(row=3, column=1)

    def OptSelection(self):
        s = self.selection.get()
        self.label3.config(text=s)

    def FileChooser(self):
        pass

    def DirChooser(self):
        pass

root = Tk()
xc_gui = XcGuiApplication(root)
root.mainloop()