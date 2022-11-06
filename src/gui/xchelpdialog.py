"""
GUI Layout for xc-converter

Copyright (c) 2017-2022 Fehmi Noyan ISI. All rights reserved.
See the LICENSE file for the end user license agreement.
"""

from tkinter import *
from tkinter import ttk

class XcHelpDialog:

    # root      -   The root window this dialog is attached to
    # version   -   version info
    # fpath     -   Src path for LICENSE file
    def __init__(self, root, version, fpath):
        top_dialog = Toplevel(root)

        top_dialog.wm_title('About xcc ' + version)
        top_dialog.resizable(width=False, height=False)

        about_label_text = 'Use of this software is subject to license conditions given below.'
        about_label = Label(top_dialog, text=about_label_text)
        about_label.grid(row=0, column=0, columnspan=2, sticky=W + E + N + S, padx=10, pady=10)

        try:
            with open(fpath + 'etc/LICENSE') as license_file:
                license_text = license_file.read()
                dialog_text = Text(top_dialog, borderwidth=3, relief="sunken")
                dialog_text.insert(INSERT, license_text)
                dialog_text.config(state=DISABLED)
                dialog_text.grid(row=1, column=0, sticky=W + E + N + S, padx=2, pady=0)

                scrollbar = Scrollbar(top_dialog, command=dialog_text.yview)
                scrollbar.grid(row=1, column=1, sticky='nsew')
                dialog_text['yscrollcommand'] = scrollbar.set

        except OSError:
            error_text = ('Opps...Cannot find the LICENSE file.\n\n'
                          'Please get the LICENSE file from https://github.com/fnoyanisi/xc-convert')
            Label(top_dialog, text=error_text).grid(row=1, sticky=W + E + N + S, padx=10, pady=10)

        download_url = 'You can obtain the source code from https://github.com/fnoyanisi/xc-convert'
        Label(top_dialog, text=download_url, justify=LEFT).grid(row=2, column=0, columnspan=2, sticky=W + E + N + S,
                                                                padx=10, pady=10)

        Button(top_dialog, text='Close', command=top_dialog.destroy, width=25).grid(row=3, column=0, columnspan=2,
                                                                                    sticky=N + S, padx=0, pady=10)
