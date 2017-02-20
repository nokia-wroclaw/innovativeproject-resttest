def read_from_file(filename):
    f = open(filename, "r")

    file_data = f.read()

    f.close()

    return file_data
