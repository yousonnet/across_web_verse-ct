import httpx
from twitter_api.custom_account import CustomAccount
from twitter.scraper import Scraper
from twitter.search import Search
from twitter_api.constants import twits_cookies
from typing import List, Dict, TypedDict, Union
import random
import functools
from custom_logger import logger
from utils.iface import UserIFace, TweetWithoutMediaIFace, ReplyIFace


class ClientDict(TypedDict):
    account: CustomAccount
    search: Search
    scraper: Scraper


class RepliesAndTweets(TypedDict):
    replies: List[ReplyIFace]
    tweets: List[TweetWithoutMediaIFace]


class MyCustomError(Exception):
    def __init__(self, message):
        super().__init__(message)


twitter_account_error = MyCustomError("Twitter account error")


def setupMultiClients(auth_token: str, ct0: str, proxy_url: str) -> ClientDict:
    proxies = proxy_url
    # {
    #     "http://": proxy_url,
    #     "https://": proxy_url,
    # }
    account = CustomAccount(cookies={"ct0": ct0,
                                     "auth_token": auth_token}, session=httpx.Client(proxies=proxies), pbar=False, save=False)
    search = Search(cookies={"ct0": ct0,
                             "auth_token": auth_token}, session=httpx.Client(proxies=proxies), pbar=False, save=False)
    scraper = Scraper(cookies={"ct0": ct0,
                               "auth_token": auth_token}, session=httpx.Client(proxies=proxies), pbar=False, save=False)
    return {"account": account, "search": search, "scraper": scraper}


clients: List[ClientDict] = list(map(lambda x: setupMultiClients(
    x['auth_token'], x['ct0'], x['proxy_endpoint']), twits_cookies))


def retry_on_exception(max_retries=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            init_exception = None
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Error occurred: {e}, retrying... {
                          retries+1}/{max_retries}")
                    retries += 1
                    init_exception = e
            if init_exception is not None:
                raise init_exception
        return wrapper
    return decorator

# def map_from_raw_to_reply_iface_bydict(data: Dict) -> ReplyIFace:
#     reply_iface_instance: ReplyIFace = {key: data[key] for key in ReplyIFace.__annotations__.keys() if key in data }
#     return reply_iface_instance

# def to_typed_dict(data: dict, typed_dict_type: type) -> TypedDict:
#     typed_dict = {key: data[key] for key in typed_dict_type.__annotations__.keys() if key in data}
#     return typed_dict
# 注意：这里没有类型检查或转换


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
        mapped_data["retweeted_status_result"] = data.get(
            "retweeted_status_result", False)
        ad_mark = True
        for key in TweetWithoutMediaIFace.__annotations__.keys():
            if key == "quoted_status_id_str":
                continue
            elif key == "retweeted_status_result":
                continue
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
    if (dict.get('in_reply_to_user_id_str') != None):
        return True
    else:
        return False


def save_textable_dict(array: List[Dict]) -> List[Dict]:
    return list(filter(lambda x:  is_text_dict(x), array))


def save_user_dict(array: List[Dict]) -> List[Dict]:
    return list(filter(lambda x: is_user_dict(x), array))


def save_reply_dict(array: List[Dict]) -> List[Dict]:
    return list(filter(lambda x: is_reply_dict(x), array))

# def sort_viewable_tweet_chain(tweet_array:List[TweetWithoutMediaIFace],replies_array:List[ReplyIFace],main_user_id:int):


class ClientsGroup:
    accounts_group: List[CustomAccount]
    search_group: List[Search]
    scraper_group: List[Scraper]

    def __init__(self, clients: List[ClientDict]):
        self.accounts_group = list(map(lambda x: x['account'], clients))
        self.search_group = list(map(lambda x: x['search'], clients))
        self.scraper_group = list(map(lambda x: x['scraper'], clients))

    # def find_legacy_and_return(self, data, key_name: str) -> List[Dict]:
    #     if isinstance(data, dict):
    #         for key, value in data.items():
    #             if key == key_name:
    #                 return value
    #             else:
    #                 found = self.find_legacy_and_return(value, key_name)
    #                 if found is not None:
    #                     return found
    #     elif isinstance(data, list):
    #         for item in data:
    #             found = self.find_legacy_and_return(item, key_name)
    #             if found is not None:
    #                 return found
    #     return []

    def find_legacy(self, data, legacy_array: List[Dict], key_name: str) -> List[Dict]:
        if isinstance(data, dict):  # 如果当前对象是字典
            for key, value in data.items():
                if key == key_name:
                    # return value  # 如果找到 'legacy' 键，返回对应的值
                    legacy_array.append(value)
                    # return legacy_array
                else:
                    self.find_legacy(value, legacy_array,
                                     key_name)  # 否则，递归搜索当前键对应的值
        elif isinstance(data, list):  # 如果当前对象是列表
            for item in data:
                self.find_legacy(item, legacy_array, key_name)  # 递归搜索列表中的每一项

        return legacy_array

    @retry_on_exception(max_retries=10)
    def get_user_id(self, screen_name: str):
        random_index = random.randint(0, len(self.accounts_group)-1)
        res = self.accounts_group[random_index].get_user_id_by_screen_name(
            screen_name)
        return res

    # @retry_on_exception(max_retries=10)
    # def get_account_profile(self, screen_name: List[str]):
    #     # raise MyCustomError("hello")
    #     random_index = random.randint(0, len(self.accounts_group)-1)
    #     res = self.scraper_group[random_index].profile_spotlights(screen_name)
    #     if (res[0].get('errors')):
    #         logger.info(f"{random_index} :twitter account invalid")
    #         raise twitter_account_error
    #     return res
    # [{'data': {'user_result_by_screen_name': {'result': {'__typename': 'User', 'legacy': {'blocking': False, 'blocked_by': False, 'protected': False, 'following': False, 'followed_by': False, 'name': 'yousonnet', 'screen_name': 'yousonnet'}, 'rest_id': '850553197923934209', 'profilemodules': {'v1': []}, 'id': 'VXNlcjo4NTA1NTMxOTc5MjM5MzQyMDk='}, 'id': 'VXNlclJlc3VsdHM6ODUwNTUzMTk3OTIzOTM0MjA5'}}}]

    @retry_on_exception(max_retries=10)
    def get_account_metadata(self, screen_name: List[int]) -> UserIFace:
        random_index = random.randint(0, len(self.accounts_group)-1)
        res = self.scraper_group[random_index].users_by_ids(screen_name)
        if (res[0].get('errors')):
            logger.info(f"{random_index} :twitter account invalid")
            raise twitter_account_error
        res = self.find_legacy(res, [], 'legacy')
        res = save_user_dict(res)
        res = map_from_raw_to_user_iface(res)
        return res[0]
# [{'data': {'user': {'result': {'__typename': 'User', 'id': 'VXNlcjo4NTA1NTMxOTc5MjM5MzQyMDk=', 'rest_id': '850553197923934209', 'affiliates_highlighted_label': {}, 'has_graduated_access': True, 'is_blue_verified': False, 'profile_image_shape': 'Circle', 'legacy': {'can_dm': False, 'can_media_tag': False, 'created_at': 'Sat Apr 08 03:37:39 +0000 2017', 'default_profile': True, 'default_profile_image': False, 'description': 'parasiempre', 'entities': {'description': {'urls': []}}, 'fast_followers_count': 0, 'favourites_count': 9614, 'followers_count': 389, 'friends_count': 3434, 'has_custom_timelines': True, 'is_translator': False, 'listed_count': 12, 'location': '', 'media_count': 86, 'name': 'yousonnet', 'normal_followers_count': 389, 'pinned_tweet_ids_str': ['1561584126037471232'], 'possibly_sensitive': False, 'profile_banner_url': 'https://pbs.twimg.com/profile_banners/850553197923934209/1670644584', 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1479474573846663170/I7ZeyR5h_normal.jpg', 'profile_interstitial_type': '', 'screen_name': 'yousonnet', 'statuses_count': 1640, 'translator_type': 'none', 'verified': False, 'want_retweets': False, 'withheld_in_countries': []}, 'smart_blocked_by': False, 'smart_blocking': False, 'legacy_extended_profile': {}, 'is_profile_translatable': False, 'verification_info': {}, 'business_account': {}}}}}]

    @retry_on_exception(max_retries=10)
    def get_account_followers(self, user_ids: List[int]):
        random_index = random.randint(0, len(self.accounts_group)-1)
        res = self.scraper_group[random_index].followers(user_ids)
        if (res[0].get('errors')):
            logger.info(f"{random_index} :twitter account invalid")
            raise twitter_account_error
        res = self.find_legacy(res, [], 'legacy')
        res = save_user_dict(res)
        res = map_from_raw_to_user_iface(res)
        return res

    @retry_on_exception(max_retries=10)
    def get_account_following(self, user_ids: List[int]):
        random_index = random.randint(0, len(self.accounts_group)-1)
        res = self.scraper_group[random_index].following(user_ids)
        if (res[0].get('errors')):
            logger.info(f"{random_index} :twitter account invalid")
            raise twitter_account_error
        res = self.find_legacy(res, [], 'legacy')
        res = save_user_dict(res)
        res = map_from_raw_to_user_iface(res)
        return res

    @retry_on_exception(max_retries=10)
    def get_account_likes(self, user_ids: List[int]):
        random_index = random.randint(0, len(self.accounts_group)-1)
        res = self.scraper_group[random_index].likes(user_ids)
        if (res[0].get('errors')):
            logger.info(f"{random_index} :twitter account invalid")
            raise twitter_account_error
        res = self.find_legacy(res, [], 'legacy')
        res = save_textable_dict(res)
        res = map_from_raw_to_tweet_iface(res)
        return res

    @retry_on_exception(max_retries=10)
    def get_account_tweets_and_replies(self, user_ids: List[int]) -> List[Union[ReplyIFace, TweetWithoutMediaIFace]]:
        random_index = random.randint(0, len(self.accounts_group)-1)
        res = self.scraper_group[random_index].tweets_and_replies(
            user_ids, limit=50)
        if (res[0].get('errors')):
            logger.info(f"{random_index} :twitter account invalid")
            raise twitter_account_error
        res = self.find_legacy(res, [], 'legacy')
        res = save_textable_dict(res)
        return_array: List[Union[ReplyIFace, TweetWithoutMediaIFace]] = []
        for item in res:
            if (item.get('in_reply_to_user_id_str') != None):
                return_array.append(map_from_raw_to_tweet_iface([item])[0])
            else:
                return_array.append(map_from_raw_to_reply_iface([item])[0])
        return return_array

    # @retry_on_exception(max_retries=10)
    # def get_account_media(self, user_ids: List[int]):
    #     random_index = random.randint(0, len(self.accounts_group)-1)
    #     res = self.scraper_group[random_index].media(user_ids)
    #     if (res[0].get('errors')):
    #         logger.info(f"{random_index} :twitter account invalid")
    #         raise twitter_account_error
    #     return res[0]

    @retry_on_exception(max_retries=10)
    def get_account_tweets(self, user_ids: List[int]):
        """get posts from tab result"""
        random_index = random.randint(0, len(self.accounts_group)-1)
        res = self.scraper_group[random_index].tweets(user_ids)
        # print(res)
        if (res[0].get('errors')):
            logger.info(f"{random_index} :twitter account invalid")
            raise twitter_account_error
        res = self.find_legacy(res, [], 'legacy')
        res = save_textable_dict(res)
        res = map_from_raw_to_tweet_iface(res)

        return res

    @retry_on_exception(max_retries=10)
    def get_tweets_details(self, tweets_ids: List[int]):
        random_index = random.randint(0, len(self.accounts_group)-1)
        res = self.scraper_group[random_index].tweets_details(tweets_ids)
        if (res[0].get('errors')):
            logger.info(f"{random_index} :twitter account invalid")
            raise twitter_account_error
        res = self.find_legacy(res, [], 'legacy')
        res = save_reply_dict(res)
        res = map_from_raw_to_reply_iface(res)

        return res


clients_group = ClientsGroup(clients=clients)
res = clients_group.get_user_id('yousonnet')
# print(res)
res1 = clients_group.get_account_tweets_and_replies([res])
for i in res1:
    print(i)
