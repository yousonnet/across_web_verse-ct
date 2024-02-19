from twitter.account import Account
from glom import glom, Coalesce, T
from typing import List, Dict


class CustomAccount (Account):
    def __init__(self, cookies, session):
        super().__init__(cookies=cookies, session=session)

    def get_user_id_by_screen_name(self, screen_name: str) -> int:
        res = self.v1('users/lookup.json', {'screen_name': screen_name})
        return res[0]['id']
