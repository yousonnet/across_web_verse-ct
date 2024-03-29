from __future__ import annotations
from typing import Dict, List, Tuple, Type, Union, TypedDict, Literal

TweetTypes = Union[Literal['repost'], Literal['quote'],
                   Literal['tweet'], Literal['reply']]


class TwitCookieIface(TypedDict):
    auth_token: str
    ct0: str
    proxy_endpoint: str


class ReplyIFace(TypedDict):
    created_at: str
    conversation_id_str: str
    favorite_count: int
    # favorited:bool
    full_text: str
    in_reply_to_screen_name: str
    in_reply_to_status_id_str: str
    in_reply_to_user_id_str: str
    is_quote_status: bool
    lang: str
    quote_count: int
    reply_count: int
    retweet_count: int
    retweeted: bool
    user_id_str: str
    id_str: str


class UserIFace(TypedDict):
    # can_dm: bool
    # can_media_tag: bool
    created_at: str
    default_profile: bool
    default_profile_image: bool
    description: str
    # fast_followers_count: int
    favourites_count: int
    followers_count: int
    friends_count: int
    has_custom_timelines: bool
    is_translator: bool
    listed_count: int
    location: str
    media_count: int
    name: str
    normal_followers_count: int
    pinned_tweet_ids_str: List[str]
    # possibly_sensitive: bool
    # profile_banner_url: str
    # profile_image_url_https: str
    # profile_interstitial_type: str
    screen_name: str
    statuses_count: int
    translator_type: str
    url: str
    verified: bool
    want_retweets: bool


class TweetWithoutMediaIFace(TypedDict):
    bookmark_count: int
    # bookmarked:bool
    created_at: str
    conversation_id_str: str
    favorite_count: int
    # favorited:bool
    full_text: str
    is_quote_status: bool
    lang: str
    # possibly_sensitive: bool
    # possibly_sensitive_editable: bool
    quote_count: int
    reply_count: int
    retweet_count: int
    user_id_str: str
    id_str: str
    quoted_status_id_str: str
    # retweeted_status_result: bool


class TweetGeneralMessageIFace(TypedDict):
    created_at: str
    full_text: str
    # user_id_str: str
    screen_name: str
    replies: List[TweetGeneralMessageIFace]
    types: TweetTypes
    is_found_upstream_source: bool


# class ReConstructureTweetGeneralMessage():
#     def __init__(self, data: Union[TweetWithoutMediaIFace, ReplyIFace],parent:Union[None,ReConstructureTweetGeneralMessage]=None):
#         self.created_at = data['created_at']
#         self.full_text = data['full_text']
#         self.id_str = data['id_str']
#         self.replies: List[TweetGeneralMessageIFace] = []  # 确保 replies 是正确的类型
#         self.types = {'type': 'tweet'}  # 假设这是 TweetTypes 的有效值
#         self.is_found_upstream_source = True
#         self.parent = parent
#     def cross_tweet_pointer():
