import httpx
from custom_account import CustomAccount
from twitter.scraper import Scraper
from twitter.search import Search
from constants import twits_cookies


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


clients = list(map(lambda x: setupMultiClients(
    x['auth_token'], x['ct0'], x['proxy_endpoint']), twits_cookies))
