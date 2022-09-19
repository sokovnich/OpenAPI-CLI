import os


def get_file_dir(file_path):
    return os.path.dirname(os.path.abspath(file_path))
