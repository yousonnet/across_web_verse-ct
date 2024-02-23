from numpy import dtype
import pandas as pd
from utils.utils import load_json


def init_knowledge_base():
    twitter_api_researcher_knowledge_base_dtype = load_json(
        "openai_agents_only/twitter_api_researcher.json")["knowledge_base_dtype"]
    check_and_create("openai_agents_only/twitter_api_researcher.csv",
                     twitter_api_researcher_knowledge_base_dtype)


def check_and_create(csv_path: str, dtype_dict):
    try:
        df = pd.read_csv(csv_path)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        df = pd.DataFrame({col: pd.Series(dtype=type_)
                          for col, type_ in dtype_dict.items()})
        df.to_csv(csv_path, index=False)
    return df


init_knowledge_base()
