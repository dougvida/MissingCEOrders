import os
import datetime
import glob
from Utilities.FileUtility import file_exists


def sort_number_ext(s):
    try:
        return int(os.path.splitext(s)[1][1:])
    except FileNotFoundError:
        return s


def rotate_file(file, keep=30):
    """ Rotate a file if needed. If the file wasn't modified today then we
    rotate it around and remove old files """

    if file_exists(file) is False:
        return False

    modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(file))

    if modified_date.date() == datetime.datetime.today().date():
        return False

    old_files = glob.glob(file + ".*")
    old_files.sort(key=sort_number_ext, reverse=True)

    for f in old_files:
        try:
            number = int(os.path.splitext(f)[1][1:])
        except ValueError:
            continue

        if number >= keep:
            # If at or above keep limit, remove.
            os.unlink(f)
        else:
            # Increment.
            new = "%s.%s" % (os.path.splitext(f)[0], number + 1)
            os.rename(f, new)

    # Finally rename our log.
    os.rename(file, "%s.1" % file)

    return True
