import httpx
from twitter_api.custom_account import CustomAccount
from twitter.scraper import Scraper
from twitter.search import Search
from twitter_api.constants import twits_cookies
from typing import List, Dict, TypedDict
import random
import functools
from custom_logger import logger
from utils.iface import UserIFace, TweetWithoutMediaIFace
from time import sleep


class ClientDict(TypedDict):
    account: CustomAccount
    search: Search
    scraper: Scraper


class MyCustomError(Exception):
    def __init__(self, message):
        super().__init__(message)


twitter_account_error = MyCustomError("Twitter account error")


def setupMultiClients(auth_token: str, ct0: str, proxy_url: str):
    proxies = {
        "http://": proxy_url,
        "https://": proxy_url,
    }
    account = CustomAccount(cookies={"ct0": ct0,
                                     "auth_token": auth_token}, session=httpx.Client(proxies=proxies))
    search = Search(cookies={"ct0": ct0,
                             "auth_token": auth_token}, session=httpx.Client(proxies=proxies))
    scraper = Scraper(cookies={"ct0": ct0,
                               "auth_token": auth_token}, session=httpx.Client(proxies=proxies))
    return {"account": account, "search": search, "scraper": scraper}


clients: List[ClientDict] = list(map(lambda x: setupMultiClients(
    x['auth_token'], x['ct0'], x['proxy_endpoint']), twits_cookies))


def retry_on_exception(max_retries=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Error occurred: {e}, retrying... {
                          retries+1}/{max_retries}")
                    retries += 1
            # 超过最大重试次数后，重新抛出最后一次的异常
            raise e
        return wrapper
    return decorator


def map_from_raw_to_user_iface(array: List[Dict]) -> List[UserIFace]:
    return_list = []
    for data in array:
        return_list.append(
            {key: data[key] for key in UserIFace.__annotations__.keys() if key in data})
    return return_list


def map_from_raw_to_tweet_iface(array: List[Dict]) -> List[TweetWithoutMediaIFace]:
    return_list = []
    for data in array:

        mapped_data = {"retweeted_status_result": True if data.get(
            "retweeted_status_result", False) else False}
        mapped_data["quoted_status_id_str"] = data.get(
            "quoted_status_id_str", None)
        ad_mark = True
        for key in TweetWithoutMediaIFace.__annotations__.keys():
            if key == "quoted_status_id_str":
                continue
            elif key == "retweeted_status_result":
                continue
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


class ClientsGroup:
    accounts_group: List[CustomAccount]
    search_group: List[Search]
    scraper_group: List[Scraper]

    def __init__(self, clients: List[ClientDict]):
        self.accounts_group = list(map(lambda x: x['account'], clients))
        self.search_group = list(map(lambda x: x['search'], clients))
        self.scraper_group = list(map(lambda x: x['scraper'], clients))

    def find_legacy_and_return(self, data, key_name: str):
        if isinstance(data, dict):
            for key, value in data.items():
                if key == key_name:
                    return value
                else:
                    found = self.find_legacy_and_return(value, key_name)
                    if found is not None:
                        return found
        elif isinstance(data, list):
            for item in data:
                found = self.find_legacy_and_return(item, key_name)
                if found is not None:
                    return found

    def find_legacy(self, data, legacy_array: List[Dict], key_name: str):
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

    @retry_on_exception(max_retries=10)
    def get_account_profile(self, screen_name: List[str]):
        # raise MyCustomError("hello")
        random_index = random.randint(0, len(self.accounts_group)-1)
        res = self.scraper_group[random_index].profile_spotlights(screen_name)
        if (res[0].get('errors')):
            logger.info(f"{random_index} :twitter account invalid")
            raise twitter_account_error
        return res[0]
    # [{'data': {'user_result_by_screen_name': {'result': {'__typename': 'User', 'legacy': {'blocking': False, 'blocked_by': False, 'protected': False, 'following': False, 'followed_by': False, 'name': 'yousonnet', 'screen_name': 'yousonnet'}, 'rest_id': '850553197923934209', 'profilemodules': {'v1': []}, 'id': 'VXNlcjo4NTA1NTMxOTc5MjM5MzQyMDk='}, 'id': 'VXNlclJlc3VsdHM6ODUwNTUzMTk3OTIzOTM0MjA5'}}}]

    @retry_on_exception(max_retries=10)
    def get_account_metadata(self, screen_name: List[str]):
        random_index = random.randint(0, len(self.accounts_group)-1)
        res = self.scraper_group[random_index].users(screen_name)
        if (res[0].get('errors')):
            logger.info(f"{random_index} :twitter account invalid")
            raise twitter_account_error
        return res[0]
# [{'data': {'user': {'result': {'__typename': 'User', 'id': 'VXNlcjo4NTA1NTMxOTc5MjM5MzQyMDk=', 'rest_id': '850553197923934209', 'affiliates_highlighted_label': {}, 'has_graduated_access': True, 'is_blue_verified': False, 'profile_image_shape': 'Circle', 'legacy': {'can_dm': False, 'can_media_tag': False, 'created_at': 'Sat Apr 08 03:37:39 +0000 2017', 'default_profile': True, 'default_profile_image': False, 'description': 'parasiempre', 'entities': {'description': {'urls': []}}, 'fast_followers_count': 0, 'favourites_count': 9614, 'followers_count': 389, 'friends_count': 3434, 'has_custom_timelines': True, 'is_translator': False, 'listed_count': 12, 'location': '', 'media_count': 86, 'name': 'yousonnet', 'normal_followers_count': 389, 'pinned_tweet_ids_str': ['1561584126037471232'], 'possibly_sensitive': False, 'profile_banner_url': 'https://pbs.twimg.com/profile_banners/850553197923934209/1670644584', 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1479474573846663170/I7ZeyR5h_normal.jpg', 'profile_interstitial_type': '', 'screen_name': 'yousonnet', 'statuses_count': 1640, 'translator_type': 'none', 'verified': False, 'want_retweets': False, 'withheld_in_countries': []}, 'smart_blocked_by': False, 'smart_blocking': False, 'legacy_extended_profile': {}, 'is_profile_translatable': False, 'verification_info': {}, 'business_account': {}}}}}]

    @retry_on_exception(max_retries=10)
    def get_account_followers(self, screen_name: List[str]):
        random_index = random.randint(0, len(self.accounts_group)-1)
        res = self.scraper_group[random_index].followers(screen_name)
        if (res[0].get('errors')):
            logger.info(f"{random_index} :twitter account invalid")
            raise twitter_account_error
        return res[0]

    @retry_on_exception(max_retries=10)
    def get_account_following(self, user_ids: List[str]):
        random_index = random.randint(0, len(self.accounts_group)-1)
        res = self.scraper_group[random_index].following(user_ids)
        if (res[0].get('errors')):
            logger.info(f"{random_index} :twitter account invalid")
            raise twitter_account_error
        return res
    # [0]

    @retry_on_exception(max_retries=10)
    def get_account_likes(self, screen_name: List[str]):
        random_index = random.randint(0, len(self.accounts_group)-1)
        res = self.scraper_group[random_index].likes(screen_name)
        if (res[0].get('errors')):
            logger.info(f"{random_index} :twitter account invalid")
            raise twitter_account_error
        return res[0]

    # @retry_on_exception(max_retries=10)
    def get_account_tweets_and_replies(self, screen_name: List[str]):
        random_index = random.randint(0, len(self.accounts_group)-1)
        res = self.scraper_group[random_index].tweets_and_replies(screen_name)
        # if (res[0].get('errors')):
        #     logger.info(f"{random_index} :twitter account invalid")
        #     raise twitter_account_error
        # print(res)
        return res

    @retry_on_exception(max_retries=10)
    def get_account_media(self, screen_name: List[str]):
        random_index = random.randint(0, len(self.accounts_group)-1)
        res = self.scraper_group[random_index].media(screen_name)
        if (res[0].get('errors')):
            logger.info(f"{random_index} :twitter account invalid")
            raise twitter_account_error
        return res[0]

    @retry_on_exception(max_retries=10)
    def get_account_tweets(self, user_ids: List[int]):
        random_index = random.randint(0, len(self.accounts_group)-1)
        res = self.scraper_group[random_index].tweets(user_ids)
        # print(res)
        if (res[0].get('errors')):
            logger.info(f"{random_index} :twitter account invalid")
            raise twitter_account_error
        # filtered_res = self.find_legacy(res, [], 'tweet_results')
        # result = []
        # previous_one = {}
        # for item in filtered_res:
        #     # result.append(item)
        #     if (previous_one != item and item.get('result').get('__typename') == "Tweet"):
        #         result.append(item)
        #     previous_one = item
        # return result
        return res

    @retry_on_exception(max_retries=10)
    def get_tweets_details(self, tweets_ids: List[str]):
        random_index = random.randint(0, len(self.accounts_group)-1)
        res = self.scraper_group[random_index].tweets_details(tweets_ids)
        if (res[0].get('errors')):
            logger.info(f"{random_index} :twitter account invalid")
            raise twitter_account_error
        return res[0]


clients_group = ClientsGroup(clients=clients)
# res = clients_group.get_user_id('Pandora_ERC404')
# res1 = clients_group.get_account_tweets_and_replies([res])
# # 得到所有该账号的tweet和reply，而不是tweet和其他账号的reply
# result = clients_group.find_legacy(res1, [], "result")
# for i in result:
#     print(i)
#     print("\n\n")
# res = clients_group.get_user_id('yousonnet')
# res1 = clients_group.get_account_tweets_and_replies([res])
# res2 = clients_group.find_legacy(res1, [], "legacy")
# i = []
# for item in res2:
#     # if (not is_user_dict(item)):
#     # i.append(item)
#     print(item)


# res3 = map_from_raw_to_tweet_iface(i)
# for i in res3:
#     print(i)
#     print("\n")
#     sleep(5)
