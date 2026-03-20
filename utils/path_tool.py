import os



def get_root_path():
    cureent_path=os.path.abspath(__file__)
    cureent_dir=os.path.dirname(cureent_path)
    return os.path.dirname(cureent_dir)


def get_abs_path(relative_path):
    project_root_path=get_root_path()

    return os.path.join(project_root_path, relative_path)


