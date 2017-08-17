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

def OptSelection():
    s = selection.get()
    label3.config(text=s)

top=Tk()

label1 = Label(top, text = "Xml to Csv Converter", font="bold")
label1.grid(row=0, column=0, sticky=W)

label2_text = 'Please select\n' \
          '    * The type of operation\n' \
          '    * The input file\n' \
          '    * Output directory '
label2 = Label(top, text = label2_text, justify=LEFT)
label2.grid(row=1, column=0, sticky=W)

# Operation Selections
selection = StringVar()
opt1 = Radiobutton(top, text = 'XML to CSV Conversion', variable=selection, value='x2c', command=OptSelection)
opt1.grid(row=2, column=0)

opt2 = Radiobutton(top, text = 'CSV to XML Conversion', variable=selection, value='c2x', command=OptSelection)
opt2.grid(row=3, column=0)

label3_text='test'
label3 = Label(top,text=label3_text)
label3.grid(row=4, column=0)

top.mainloop()