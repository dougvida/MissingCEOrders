"""
    easygui : http://easygui.sourceforge.net/api.html
"""
import os

import easygui
from easygui import *


def getfile(title, default_path, msg='Please select a file', filetype="*.*"):

    file_name = easygui.fileopenbox(msg=msg, title=title, default=filetype, multiple=False)
    if file_name:
        print("Selected file: " + file_name)

        # test if file exists
        if not os.path.isfile(file_name):
            s_tmp = "File not found"
            return None, s_tmp
        else:
            return file_name, ''
    else:
        return None, 'Cancel'


def gethl7file(title):
    msg = "Please select the HL7 file to search"
    # filename = easygui.fileopenbox(msg=msg, title=title, filetypes=filetypes, multiple=False)
    file_name = easygui.fileopenbox(msg=msg, title=title, default='*.hl7', multiple=False)
    if file_name:
        print("Selected file: " + file_name)
        name, ext = os.path.splitext(file_name)
        if ".hl7" != str(ext).lower():
            s_tmp = f"Invalid file name: {file_name}"
            return None, s_tmp

        # test if file exists
        if not os.path.isfile(file_name):
            s_tmp = "File not found"
            return None, s_tmp
        else:
            return file_name, ''
    else:
        return None, 'Cancel'


def hl7search(title):
    errmsg = ''
    field_names = ["Segment", "field", "data"]
    # field_names = []
    while True:
        if len(errmsg) > 0:
            msg = errmsg
        else:
            msg = "Enter search parameters {HL7 Segment, Field, value:[can be " \
                  "blank]}"

        field_values = multenterbox(msg, title, field_names)
        if field_values is None:
            return field_values, 'Cancel'

        errmsg = ''
        for i in range(len(field_names) - 1):  # don't make data required
            if field_values[i].strip() == "":
                errmsg = errmsg + f'Entry {field_names[i]} is required\n\n'
        if errmsg == "":
            break

    return field_values, ''
