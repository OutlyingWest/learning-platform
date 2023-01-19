from datetime import datetime
from os.path import splitext


def get_timestamp_path_user(instance, filename):
    return f'users/{datetime.now().timestamp()}{splitext(filename)[1]}'
