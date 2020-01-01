import re
import os


def tryint(s):
    try:
        return int(s)
    except:
        return s


def alphanum_key(s):
    return [tryint(c) for c in re.split('([0-9]+)', s)]


def sort_nicely(l):
    l.sort(key=alphanum_key)


def move():
    cpt = 0

    folder_in = "DARLING in the FRANXX - 1 cleared"
    folder_out = "a"

    for folder, subfolder, files in os.walk(folder_in):
        if len(files) == 0:
            continue
        sort_nicely(files)
        for f in files:
            path_in = os.path.join(folder, f)
            file, ext = os.path.splitext(path_in)
            name = "{:0>4}".format(cpt)
            path_out = os.path.join(folder_out, name + ext)
            cpt += 1
            # print(path_in, path_out)
            os.rename(path_in, path_out)
