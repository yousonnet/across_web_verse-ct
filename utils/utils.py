from datetime import datetime
import json
import pandas as pd


def x_api_timestr_to_time(original_time_str: str) -> str:

    datetime_obj = datetime.strptime(
        original_time_str, '%a %b %d %H:%M:%S %z %Y')
    simple_readable_time = datetime_obj.strftime('%Y-%m-%d %H:%M')

    return simple_readable_time


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


# def add_new_line_to_csv(csv_file_path: str, data: dict):
#     dataframe = pd.read_csv(csv_file_path)
#     new_row_df = pd.DataFrame([data])
#     df = dataframe.append(new_row_df, ignore_index=True)
#     df.to_csv(csv_file_path, index=False)
