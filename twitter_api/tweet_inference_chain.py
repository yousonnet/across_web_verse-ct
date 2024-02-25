from typing import Optional, Union, List, Literal, Dict

from numpy import full
from utils.iface import TweetWithoutMediaIFace, ReplyIFace, TweetGeneralMessageIFace
from twitter_api.tweets_utils import is_reply_dict, is_text_dict, is_user_dict


def map_from_raw_to_general_message_iface(array: List[Dict]) -> List[TweetGeneralMessageIFace]:
    return_list = []
    for data in array:
        return_list.append(
            {key: data[key] for key in TweetGeneralMessageIFace.__annotations__.keys() if key in data})
        break
    return return_list[0]


def is_repost(full_text: str) -> bool:
    if full_text.startswith("RT @"):
        return True
    else:
        return False


def is_start_with_at(full_text: str) -> bool:
    if full_text.startswith("@"):
        return True
    else:
        return False


def tweet_inference(array: List[Union[TweetWithoutMediaIFace, ReplyIFace]]):
    # prev_one:Optional[Union[TweetWithoutMediaIFace,ReplyIFace]] = None
    prev_list: List[TweetGeneralMessageIFace]
    for index in range(len(array)-1, -1, -1):
        last_one = array[index]
