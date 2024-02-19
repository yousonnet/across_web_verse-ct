import dotenv
import os
import httpx
import json
from typing import Optional
dotenv.load_dotenv()
toto_key = os.getenv("TOTO_KEY")

# toto的数据一直不全(可能为了降低存储开销，预先用ml做了crypto account的filter?)，且metadata的follower肯定出错,实例一个username的follower 20几个，却显示200个


class TOTOClient:
    key: str
    httpx_client: httpx.Client

    def __init__(self, key: str):
        self.key = key
        self.httpx_client = httpx.Client(
            base_url="https://toto.oz.xyz/api", headers={'x-api-key': key, 'Content-Type': 'application/json', 'accept': 'application/json'})

    def get_account_historic_used_names(self, is_id: bool, user_id: Optional[int] = None, user_name: Optional[str] = None,):
        res = self.httpx_client.post("/metadata/get_metadata_history", json={
            "user": str(user_id) if is_id else user_name,
            "how": "userid" if is_id else "username",
            "page": 1
        })
        return res.json()['data']

    def get_whole_followers(self, is_id: bool, only_1_page: Optional[bool] = None, user_id: Optional[int] = None, user_name: Optional[str] = None,):
        return_array = []
        page_offset = 1
        while (True):
            res = self.httpx_client.post("/graph/get_followers", json={
                "user": str(user_id) if is_id else user_name,
                "how": "userid" if is_id else "username",
                "page": page_offset
            })
            if (len(res.json()['data']) == 0):
                break
            page_offset += 1
            return_array.extend(res.json()['data'])
            if only_1_page:
                break
        return return_array

    def get_user_degenscore(self, is_id: bool, user_id: Optional[int] = None, user_name: Optional[str] = None,):
        res = self.httpx_client.post("/alpha/get_score_history", json={
            "user": str(user_id) if is_id else user_name,
            "how": "userid" if is_id else "username",
        })
        # print(res.json())
        if len(res.json()['data']) == 0:
            return 0
        return res.json()['data'][0]['score']


toto_client = TOTOClient(toto_key)
