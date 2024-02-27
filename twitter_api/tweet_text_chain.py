from typing import Optional, Union, List, Literal, Dict
from utils.utils import x_api_timestr_to_time
from numpy import full
from utils.iface import TweetWithoutMediaIFace, ReplyIFace, TweetGeneralMessageIFace, UserIFace
from twitter_api.tweets_utils import is_reply_dict, is_text_dict, is_user_dict


# def map_from_raw_to_general_message_iface(data: Dict) -> TweetGeneralMessageIFace:
#     # return_list = []
#     # for data in array:
#     #     return_list.append(
#     #         {key: data[key] for key in TweetGeneralMessageIFace.__annotations__.keys() if key in data})
#     #     break
#     if data.get('full_text',''):

#     res = {key: data[key] for key in TweetGeneralMessageIFace.__annotations__.keys() if key in data}

#     return res


def is_repost(full_text: str) -> bool:
    if full_text.startswith("RT @"):
        return True
    else:
        return False


# def is_reply(data: Dict) -> bool:
#     if data.get('in_reply_to_screen_name'):
#         return True
#     else:
#         return False


def tweet_inference(array: List[Union[TweetWithoutMediaIFace, ReplyIFace]]) -> str:
    output_text = ""
    for index in range(0, len(array)):
        if (is_repost(array[index]["full_text"])):
            output_text += f"reposted from {array[index]
                                            ['user_id_str']}: {array[index]['full_text']}\n{x_api_timestr_to_time(array[index]['created_at'])}\n"
        elif (array[index].get('in_reply_to_screen_name')):
            output_text += f"replied to {array[index].get('in_reply_to_user_id_str')}:\n{array[index]['user_id_str']} reply: {
                array[index]['full_text']}\n{x_api_timestr_to_time(array[index]['created_at'])}\n"

        elif (array[index].get('is_quote_status')):
            output_text += f"quoted from above: \n{array[index]['user_id_str']} quote:{
                array[index]['full_text']}\n{x_api_timestr_to_time(array[index]['created_at'])}\n"
        else:
            output_text += f"{array[index]['user_id_str']
                              } tweet: {array[index]['full_text']}\n{x_api_timestr_to_time(array[index]['created_at'])}\n"
    return output_text


def replace_user_id_to_screen_name(text: str, user_id: str, screen_name: str) -> str:
    return text.replace(user_id, screen_name)
