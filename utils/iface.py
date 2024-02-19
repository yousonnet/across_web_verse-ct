from typing import Dict, List, Tuple, Union, TypedDict

twit_cookie_iface = {
    "auth_token": str,
    "ct0": str,
    "proxy_endpoint": str
}


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
    quoted_status_id_str: str | None
    retweeted_status_result: bool
