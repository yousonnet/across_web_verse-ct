from datetime import datetime
import json


def timestr_to_time(time_str: str):
    time_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%f%z')
    return time_obj


def load_json(file_path: str):
    with open(file_path, 'r') as f:
        return json.load(f)


def is_termination_msg(x: dict):
    if (x.get("content", "").rstrip().endswith("TERMINATE")):
        return True
    return False
