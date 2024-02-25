from typing import List, Dict
from utils.iface import UserIFace, ReplyIFace, TweetWithoutMediaIFace


def map_from_raw_to_user_iface(array: List[Dict]) -> List[UserIFace]:
    return_list = []
    for data in array:
        return_list.append(
            {key: data[key] for key in UserIFace.__annotations__.keys() if key in data})
    return return_list


def map_from_raw_to_reply_iface(array: List[Dict]) -> List[ReplyIFace]:
    return_list = []

    for data in array:
        return_list.append(
            {key: data[key] for key in ReplyIFace.__annotations__.keys() if key in data})
    return return_list


def map_from_raw_to_tweet_iface(array: List[Dict]) -> List[TweetWithoutMediaIFace]:
    return_list = []
    for data in array:

        mapped_data = {"quoted_status_id_str": data.get(
            "quoted_status_id_str", "")}
        # mapped_data["retweeted_status_result"] = data.get(
        #     "retweeted_status_result", False)
        ad_mark = True
        for key in TweetWithoutMediaIFace.__annotations__.keys():
            if key == "quoted_status_id_str":
                continue
            # elif key == "retweeted_status_result":
            #     continue
            # 将数据格式转化一下
            elif key in data:
                mapped_data[key] = data[key]
                ad_mark = False
        if (not ad_mark):
            return_list.append(mapped_data)
    return return_list


def is_user_dict(dict: Dict) -> bool:
    if (dict.get('can_dm') != None):
        return True
    else:
        return False


def is_text_dict(dict: Dict) -> bool:
    if (dict.get('full_text') != None):
        return True
    else:
        return False
# 包含reply和tweet


def is_reply_dict(dict: Dict) -> bool:
    if (dict.get('in_reply_to_status_id_str') != None):
        return True
    else:
        return False


def save_textable_dict(array: List[Dict]) -> List[Dict]:
    return list(filter(lambda x:  is_text_dict(x), array))


def save_user_dict(array: List[Dict]) -> List[Dict]:
    return list(filter(lambda x: is_user_dict(x), array))


def save_reply_dict(array: List[Dict]) -> List[Dict]:
    return list(filter(lambda x: is_reply_dict(x), array))
