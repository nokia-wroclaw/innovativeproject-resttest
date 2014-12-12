# coding=utf-8
__author__ = 'Bartosz Zięba, Tomasz M. Wlisłocki, Damian Mirecki, Sławomir Domagała'

import os


def read_from_file(filename):
    this_dir, this_filename = os.path.split(__file__)

    logo_file_path = os.path.join(this_dir, "logo.txt")
    logo_file = open(logo_file_path, "r")
    logo = logo_file.read()
    print(logo)

    f = open(filename, "r")

    file_data = f.read()

    f.close()

    return file_data
