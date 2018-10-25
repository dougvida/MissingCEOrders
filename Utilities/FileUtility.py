"""
    easygui : http://easygui.sourceforge.net/api.html
"""
import os


def write_file(file_path_name, data):
    """
    Write the file and populate with the data
    :param file_path_name:
    :param data:
    :return:
    """
    fp_name = os.path.join("", file_path_name)  # get the path correct based on OS
    with open(fp_name, "w+") as out_file:
        out_file.write(data + '\n')


def write_file_array(file_path_name, data_ar: [str]):
    """
    Write the file and populate with the data
    :param file_path_name:
    :param data_ar: [str]
    :return:
    """
    fp_name = os.path.join("", file_path_name)  # get the path correct based on OS
    with open(fp_name, "w+") as out_file:
        for data in data_ar:
            out_file.write(data + '\n')


def ensure_dir(file_path):
    """
    This script check if the folder exists
    Check if the argument is a fold.  if not split to get folder
    Verify if folder exists.  If not create it
   """
    if file_path.endswith(os.sep):
        file_path = os.path.join("", file_path[:-1])

    directory = file_path
    if not os.path.exists(directory):
        os.makedirs(directory)


def fix_path(folder):
    """This script will append the OS folder separator"""
    if not folder.endswith(os.sep):
        return folder + os.sep
    else:
        return folder


def folder_exists(srcfolder, mode=False):
    """Check if folder exits
    Arg: mode
        True create the folder if it does not exists
        False return False if folder does not exists
    """
    if len(srcfolder) > 0:
        try:
            if os.path.isdir(srcfolder):
                return True
            else:
                if mode is True:
                    os.mkdir(srcfolder)
                    return True
                else:
                    return False
        except Exception as exp:
            print(f"Exception {exp}")

    else:
        return False

# def separate_path_file1(filepath):
#    """This script returns the folder and or file name based on the argument
#    argument may only be file name, or only folder or both"""
#    rpath, fname = os.path.split(filepath)
#
#    # if path is empty and fname has value this could mean it a folder without
#    # ending os.sep
#    if len(rpath) <= 0:
#        # check if fname is a file
#        # if both filename and fileext are populated it's a valid file name
#        filename, fileext = os.path.splitext(fname)
#        if len(filename) and len(fileext):
#            # we only have a file name
#            return '.' + os.sep, fname
#
#        if len(filename) and len(fileext) <= 0:
#            # we have filename only this is a folder
#           return fix_path(filename), ''
#    else:
#        rpath = fix_path(rpath)
#
#    return rpath, fname
