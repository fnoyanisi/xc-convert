"""
GUI Layout for xc-converter

Copyright (c) 2017-2022 Fehmi Noyan ISI. All rights reserved.
See the LICENSE file for the end user license agreement.
"""

from tkinter import *
from tkinter import ttk


class XcHelpDialog:
    url = "https://github.com/fnoyanisi/xc-convert"
    license_file_path = "etc/LICENSE"
    fpath = None
    version = None
    root = None
    top_dialog = None

    # root      -   The root window this dialog is attached to
    # version   -   version info
    # fpath     -   Src path for LICENSE file
    def __init__(self, root, version, fpath):
        self.root = root
        self.version = version
        self.fpath = fpath

        self.top_dialog = Toplevel(root)
        self.top_dialog.wm_title('About xcc ' + version)
        self.top_dialog.resizable(width=False, height=False)

        top_frame = Frame(self.top_dialog)
        top_frame.pack()

        # notebook = ttk.Notebook(top_dialog)
        # notebook.pack()

        self.get_about_frame(top_frame)

    def get_about_frame(self, root):
        about_label_text = 'Use of this software is subject to license conditions given below.'
        about_label = Label(root, text=about_label_text)
        about_label.grid(row=0, column=0, columnspan=2, sticky=W + E + N + S, padx=10, pady=10)

        try:
            with open(self.fpath + self.license_file_path) as license_file:
                license_text = license_file.read()
                dialog_text = Text(root, borderwidth=3, relief="sunken")
                dialog_text.insert(INSERT, license_text)
                dialog_text.config(state=DISABLED)
                dialog_text.grid(row=1, column=0, sticky=W + E + N + S, padx=2, pady=0)

                scrollbar = Scrollbar(root, command=dialog_text.yview)
                scrollbar.grid(row=1, column=1, sticky='nsew')
                dialog_text['yscrollcommand'] = scrollbar.set

        except OSError:
            error_text = ('Opps...Cannot find the LICENSE file.\n\n'
                          'Please get the LICENSE file from ' + self.url)
            Label(root, text=error_text).grid(row=1, sticky=W + E + N + S, padx=10, pady=10)

        download_url_msg = 'You can obtain the source code from ' + self.url
        Label(root, text=download_url_msg, justify=LEFT).grid(row=2, column=0, columnspan=2, sticky=W + E + N + S,
                                                          padx=10, pady=10)

        Button(root, text='Close', command=self.top_dialog.destroy, width=25).grid(row=3, column=0, columnspan=2,
                                                                        sticky=N + S, padx=0, pady=10)
