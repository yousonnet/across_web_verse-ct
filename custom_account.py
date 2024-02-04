from twitter.account import Account


class CustomAccount (Account):
    def __init__(self, cookies, session):
        super().__init__(cookies=cookies, session=session)

    def get_user_id_by_screen_name(self, screen_name):
        res = self.v1('users/lookup.json', {'screen_name': screen_name})
        return res[0]['id']
