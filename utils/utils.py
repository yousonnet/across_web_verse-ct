from datetime import datetime


def timestr_to_time(time_str: str):
    time_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%f%z')
    return time_obj
